"""Convert a binary source into Markdown so the vault can read it in slices.

Why this exists: a book-length PDF cannot be read cheaply. The Read tool takes 20 pages
per call and renders page images, so a 300-page book costs 15 expensive calls to skim
once. The same book as Markdown is greppable: find the section, read 100 lines, done.
It also unlocks formats that cannot be read at all otherwise (DOCX, PPTX, XLSX, audio).

The Markdown is an EXTRACTION, not a second source. The original binary stays the
citable source file. Both move to raw/ together at filing time, same basename, and
both take the type prefix then. See the aegis-ingest skill.

    python .claude/scripts/ingest_convert.py                 convert everything in input/
    python .claude/scripts/ingest_convert.py FILE [FILE...]  convert specific files
    python .claude/scripts/ingest_convert.py --list          show the queue, convert nothing
    python .claude/scripts/ingest_convert.py --force         re-convert even if .md exists
    python .claude/scripts/ingest_convert.py --out DIR       write elsewhere (default: beside source)
    python .claude/scripts/ingest_convert.py --ocr           force OCR on (scanned pages)
    python .claude/scripts/ingest_convert.py --no-ocr        force OCR off (fast, text-layer PDFs)
    python .claude/scripts/ingest_convert.py --threads N     worker threads (default: all cores)

OCR is the expensive part by a wide margin, and it is wasted on a PDF that already
carries an embedded text layer, which most published books and exports do. By default
this samples pages and turns OCR off when the text is already there. Override with
--ocr when a source is scanned or photographed.

Needs the venv: .venv/Scripts/python.exe on Windows, .venv/bin/python elsewhere.
Prints a token estimate per file so the cost of reading the result is known before reading it.
"""
import os
import sys
import time

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(VAULT, "input")

# Formats Docling handles. Anything else is left alone and reported as skipped.
SUPPORTED = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm", ".xhtml",
    ".md", ".csv", ".asciidoc", ".adoc",
    ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp",
}
# Already plain text. Converting these gains nothing.
PASSTHROUGH = {".md", ".txt", ".vtt", ".srt", ".json", ".yaml", ".yml"}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
FLAGS = {a for a in sys.argv[1:] if a.startswith("--")}
LIST_ONLY = "--list" in FLAGS
FORCE = "--force" in FLAGS
FORCE_OCR = "--ocr" in FLAGS
NO_OCR = "--no-ocr" in FLAGS

if FORCE_OCR and NO_OCR:
    print("--ocr and --no-ocr contradict each other. Pick one.")
    sys.exit(1)


def _valued_flag(name, cast, default):
    if name not in sys.argv:
        return default
    i = sys.argv.index(name)
    if i + 1 >= len(sys.argv):
        print("%s needs a value" % name)
        sys.exit(1)
    val = sys.argv[i + 1]
    if val in args:
        args.remove(val)
    try:
        return cast(val)
    except ValueError:
        print("%s: bad value %r" % (name, val))
        sys.exit(1)


out_dir = _valued_flag("--out", str, None)
THREADS = _valued_flag("--threads", int, os.cpu_count() or 4)


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f%s" % (n, unit)
        n /= 1024.0
    return "%.1fTB" % n


def gather():
    """Return the list of files to convert."""
    if args:
        found = []
        for a in args:
            if not os.path.exists(a):
                print("MISSING: %s" % a)
                sys.exit(1)
            found.append(os.path.abspath(a))
        return found
    if not os.path.isdir(INPUT_DIR):
        print("No input/ directory at %s" % INPUT_DIR)
        sys.exit(1)
    return [
        os.path.join(INPUT_DIR, f)
        for f in sorted(os.listdir(INPUT_DIR))
        if os.path.isfile(os.path.join(INPUT_DIR, f))
    ]


def target_for(path):
    base = os.path.splitext(os.path.basename(path))[0] + ".md"
    return os.path.join(out_dir or os.path.dirname(path), base)


def has_text_layer(path, sample=8, min_chars=200):
    """True when the PDF already carries extractable text, making OCR wasted work.

    Samples pages spread through the document rather than the first few: front matter
    is often an image even in a fully digital book, which would read as 'scanned'.
    """
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return False
    try:
        doc = pdfium.PdfDocument(path)
        n = len(doc)
        if n == 0:
            return False
        idxs = sorted({int(n * (i + 0.5) / sample) for i in range(min(sample, n))})
        hits = 0
        for i in idxs:
            try:
                if len(doc[i].get_textpage().get_text_range().strip()) >= min_chars:
                    hits += 1
            except Exception:
                pass
        return hits >= max(1, len(idxs) // 2)
    except Exception:
        return False


files = gather()
if not files:
    print("Nothing in input/.")
    sys.exit(0)

queue, skipped = [], []
for f in files:
    ext = os.path.splitext(f)[1].lower()
    dest = target_for(f)
    if ext in PASSTHROUGH and ext != ".md":
        skipped.append((f, "already plain text"))
    elif ext not in SUPPORTED:
        skipped.append((f, "unsupported format %s" % ext))
    elif os.path.abspath(dest) == os.path.abspath(f):
        skipped.append((f, "would overwrite itself"))
    elif os.path.exists(dest) and not FORCE:
        skipped.append((f, "%s exists (use --force)" % os.path.basename(dest)))
    else:
        queue.append((f, dest))

for f, why in skipped:
    print("SKIP  %-52s %s" % (os.path.basename(f)[:52], why))

if not queue:
    print("\nNothing to convert.")
    sys.exit(0)

# Decide OCR per file before printing the plan, so the queue shows the real cost.
plan = []
for f, dest in queue:
    if FORCE_OCR:
        ocr, why = True, "forced"
    elif NO_OCR:
        ocr, why = False, "forced off"
    elif os.path.splitext(f)[1].lower() == ".pdf":
        ocr = not has_text_layer(f)
        why = "no text layer" if ocr else "text layer found"
    else:
        ocr, why = False, "not a PDF"
    plan.append((f, dest, ocr, why))

total = sum(os.path.getsize(f) for f, _, _, _ in plan)
print("\n%d file(s) to convert, %s total, %d threads:" % (len(plan), human(total), THREADS))
for f, _, ocr, why in plan:
    print("  %-46s %8s  OCR %-3s (%s)" % (
        os.path.basename(f)[:46], human(os.path.getsize(f)), "ON" if ocr else "off", why))

if any(ocr for _, _, ocr, _ in plan):
    print("\nOCR is on for at least one file. That is roughly 10x slower per page.")

if LIST_ONLY:
    print("\n--list: nothing converted.")
    sys.exit(0)

try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
except ImportError:
    print("\nDocling is not installed in this interpreter (%s)." % sys.executable)
    print("Run it with the venv: .venv/Scripts/python.exe .claude/scripts/ingest_convert.py")
    sys.exit(1)

_converters = {}


def converter_for(ocr):
    """One converter per OCR setting. Building one loads models, so they are reused."""
    if ocr not in _converters:
        opts = PdfPipelineOptions()
        opts.do_ocr = ocr
        opts.accelerator_options = AcceleratorOptions(
            num_threads=THREADS, device=AcceleratorDevice.AUTO
        )
        _converters[ocr] = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
    return _converters[ocr]


print("\nLoading Docling models (first run downloads them, several minutes)...")

ok, failed, run_start = 0, 0, time.time()
for f, dest, ocr, _ in plan:
    print("\n-> %s" % os.path.basename(f))
    start = time.time()
    try:
        result = converter_for(ocr).convert(f)
        md = result.document.export_to_markdown()
    except Exception as e:
        # One bad file must not kill the batch. Report and keep going.
        print("   FAILED after %.0fs: %s: %s" % (time.time() - start, type(e).__name__, e))
        failed += 1
        continue
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(md)
    chars = len(md)
    print("   %s  %s  ~%s tokens  %.0fs" % (
        os.path.basename(dest), human(chars), format(chars // 4, ","), time.time() - start))
    ok += 1

print("\n%d converted, %d failed, %d skipped in %.0fs." % (
    ok, failed, len(skipped), time.time() - run_start))
if ok:
    print("The .md files are extractions. The originals remain the citable sources;")
    print("move both to raw/ together and apply the type prefix at filing time.")
