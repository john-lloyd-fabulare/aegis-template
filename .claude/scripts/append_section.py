"""Append a line under a heading without loading the page into context.

Why this exists: back-linking a participant means reading their whole page to add one line.
A mature person page runs to several thousand words; an email involving two of them can cost
well over ten thousand tokens to add two bullets. This does it for about twenty.

    python .claude/scripts/append_section.py "wiki/people/Some Person.md" "## Communications"         "- [[Some Email (2026-08-26)]] - one-line summary."

    --top     insert directly under the heading instead of at the end of the section
    --create  add the heading at end of file if it is missing (default: fail loudly)
    --dry     show the 3 lines around the insert point and change nothing

Prints only what changed. Never echoes the file.
"""
import io, os, sys

# A cp1252 Windows console cannot print emoji, so the success message used to crash after
# a correct write. Replace unprintable characters instead of raising.
try:
    sys.stdout.reconfigure(errors='replace')
except AttributeError:
    pass

args = [a for a in sys.argv[1:] if not a.startswith('--')]
FLAGS = {a for a in sys.argv[1:] if a.startswith('--')}
if len(args) != 3:
    print(__doc__)
    sys.exit(1)

path, heading, line = args
heading = heading.strip()
if not line.endswith('\n'):
    line += '\n'

if not os.path.exists(path):
    print("MISSING FILE: %s" % path)
    sys.exit(1)

lines = io.open(path, encoding='utf-8', errors='replace').readlines()

# locate the heading
idx = None
for i, l in enumerate(lines):
    if l.strip() == heading:
        idx = i
        break

if idx is None:
    if '--create' not in FLAGS:
        heads = [l.strip() for l in lines if l.startswith('## ')]
        print("HEADING NOT FOUND: %s" % heading)
        print("  existing headings: %s" % ' | '.join(heads[:12]))
        print("  pass --create to add it at end of file")
        sys.exit(2)
    if lines and lines[-1].strip():
        lines.append('\n')
    lines.append(heading + '\n\n')
    idx = len(lines) - 2

# find where the section ends (next '## ' heading, or EOF)
end = len(lines)
for j in range(idx + 1, len(lines)):
    if lines[j].startswith('## '):
        end = j
        break

if '--top' in FLAGS:
    at = idx + 1
    while at < end and not lines[at].strip():
        at += 1
else:
    at = end
    while at - 1 > idx and not lines[at - 1].strip():
        at -= 1

if lines and at > 0 and lines[at - 1].strip().startswith('#'):
    lines.insert(at, '\n')
    at += 1

lines.insert(at, line)

if '--dry' in FLAGS:
    lo, hi = max(0, at - 2), min(len(lines), at + 3)
    print("DRY RUN, would insert at line %d of %s" % (at + 1, os.path.basename(path)))
    for k in range(lo, hi):
        print("  %s %s" % ('>>' if k == at else '  ', lines[k].rstrip()[:100]))
    sys.exit(0)

io.open(path, 'w', encoding='utf-8', newline='').write(''.join(lines))
print("appended to %s under %s (line %d)" % (os.path.basename(path), heading, at + 1))
