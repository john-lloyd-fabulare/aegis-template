"""AEGIS vault linter. Read-only. Alias-aware. Run from vault root."""
import os, re, json, collections, sys

ROOT = os.getcwd()
SKIP = {'.git', '.claude', '.obsidian', 'node_modules', '.venv'}
# Add any folder that is not part of the vault proper (nested repos, scratch dirs).


def walk():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            out.append(rel.replace(os.sep, '/'))
    return out


files = walk()
mds = [f for f in files if f.lower().endswith('.md')]

# ---------- name index, alias aware ----------
byname = collections.defaultdict(list)
for f in files:
    b = os.path.basename(f)
    byname[b].append(f)
    if b.lower().endswith('.md'):
        byname[b[:-3]].append(f)

for f in mds:
    t = open(f, encoding='utf-8', errors='replace').read()
    m = re.search(r'^---\n(.*?)\n---', t, re.S)
    if not m:
        continue
    a = re.search(r'^aliases:\s*(\[.*\])\s*$', m.group(1), re.M)
    if a:
        try:
            vals = json.loads(a.group(1))
        except Exception:
            vals = re.findall(r'"([^"]+)"', a.group(1))
        for v in vals:
            byname[v].append(f)

# Capture the whole target, then strip display-alias and heading.
# NB: inside markdown tables Obsidian requires an ESCAPED pipe (\|). A naive
# [^|] class treats the backslash as part of the filename and reports a false
# positive. Split on the pipe, then drop any trailing backslash.
LR = re.compile(r'\[\[([^\]]+?)\]\]')


def link_target(raw):
    t = raw.split('|')[0]          # drop display alias
    t = t.split('#')[0]            # drop heading anchor
    return t.rstrip('\\').strip()  # drop table-escape backslash

inbound = collections.Counter()
broken_live = []
for f in mds:
    txt = open(f, encoding='utf-8', errors='replace').read()
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    txt = re.sub(r'`[^`\n]*`', '', txt)
    live = not (f.startswith('raw/') or f.endswith('log.md'))
    for mm in LR.finditer(txt):
        tgt = link_target(mm.group(1))
        if not tgt:
            continue
        if tgt in byname:
            for t2 in set(byname[tgt]):
                inbound[t2] += 1
        elif live:
            broken_live.append((f, tgt))

# ---------- frontmatter ----------
bad_sources, no_fm = [], []
for f in mds:
    if not f.startswith('wiki/'):
        continue
    t = open(f, encoding='utf-8', errors='replace').read()
    if not t.startswith('---'):
        no_fm.append(f)
        continue
    end = t.find('\n---', 3)
    fm = t[3:end] if end > 0 else ''
    for line in fm.splitlines():
        mm = re.match(r'^(sources|participants|aliases|tags):\s*(\[\[.*)$', line)
        if mm:
            bad_sources.append((f, mm.group(1)))

# ---------- results ----------
dupes = {k: sorted(set(v)) for k, v in byname.items()
         if k.endswith('.md') and len(set(v)) > 1}
orphans = [f for f in mds if inbound[f] == 0]
root_md = [f for f in files if '/' not in f and f.endswith('.md')]

print("=" * 62)
print("AEGIS LINT")
print("=" * 62)
print("files total            %5d" % len(files))
print("markdown               %5d" % len(mds))
print("wiki pages             %5d" % len([f for f in mds if f.startswith('wiki/')]))
print("raw markdown           %5d" % len([f for f in mds if f.startswith('raw/')]))
print("-" * 62)
print("broken links (live)    %5d   <- target 0" % len(broken_live))
print("bad frontmatter arrays %5d   <- target 0" % len(bad_sources))
print("orphan pages           %5d   <- target 0" % len(orphans))
print("duplicate filenames    %5d   <- must stay 0" % len(dupes))
print("pages w/o frontmatter  %5d" % len(no_fm))
print("root .md files         %5d   %s" % (len(root_md), root_md))
print("-" * 62)

if '-v' in sys.argv:
    if broken_live:
        print("\nBROKEN LINKS:")
        for f, t in broken_live:
            print("  %-56s [[%s]]" % (f[:56], t[:40]))
    if bad_sources:
        print("\nBAD FRONTMATTER ARRAYS:")
        for f, k in bad_sources:
            print("  %-56s %s:" % (f[:56], k))
    if orphans:
        print("\nORPHANS:")
        for f in orphans:
            print("  ", f)
    if dupes:
        print("\nDUPLICATE FILENAMES:")
        for k, v in dupes.items():
            print("  ", k, "->", v)

# ---------- sizes ----------
print("\nSTARTUP COST")
tot = 0
for f in ['CLAUDE.md', 'wiki/hot.md', 'wiki/index.md']:
    if os.path.exists(f):
        w = len(open(f, encoding='utf-8', errors='replace').read().split())
        tot += w
        print("  %-22s %6d w" % (f, w))
print("  %-22s %6d w" % ('TOTAL', tot))

print("\nHUB SIZES")
hd = 'wiki/topic-hubs'
if os.path.isdir(hd):
    rows = []
    for f in sorted(os.listdir(hd)):
        if not f.endswith('.md'):
            continue
        t = open(os.path.join(hd, f), encoding='utf-8', errors='replace').read()
        # companion evidence files are exempt from the hub cap by design
        comp = 'type: topic-hub-details' in t[:400]
        rows.append((len(t.split()), t.count('\n### '), f[:-3], comp))
    for w, s, n, comp in sorted(rows, reverse=True):
        if comp:
            flag = '   (companion, exempt)'
        else:
            flag = '  <-- OVER 8000' if w > 8000 else ''
        print("  %-44s %6d w  %3d sections%s" % (n[:44], w, s, flag))
