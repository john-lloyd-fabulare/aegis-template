"""Regenerate wiki/index.md from the filesystem, preserving everything already written by hand.

Why this exists: index.md was hand-maintained during every ingest. That cost ~20,000 tokens per
ingest session (the file must be read to be edited) and it drifted anyway, with 81 pages missing
from it on 2026-08-21. Generating it makes drift structurally impossible and removes the read.

It never invents a description and never deletes prose. Pages it has not seen before get a bare
line for a human to fill in; section intros, sub-lists and notes are carried through untouched.

    python .claude/scripts/gen_index.py          # dry run, reports the delta
    python .claude/scripts/gen_index.py --apply  # rewrite wiki/index.md
"""
import os, re, io, sys

APPLY = '--apply' in sys.argv
INDEX = 'wiki/index.md'

SECTIONS = [
    ('people',          '## People'),
    ('topic-hubs',      '## Topic Hubs'),
    ('concepts',        '## Concepts'),
    ('projects',        '## Projects'),
    ('work-items',      '## Work Items'),
    ('cases',           '## Cases'),
    ('meetings',        '## Meetings'),
    ('communications',  '## Communications'),
    ('sources',         '## Sources'),
    ('journal',         '## Journal'),
    ('answers',         '## Answers'),
    ('content-drafts',  '## Content Drafts'),
]
ROOT_SECTION = '## Vault meta'
ROOT_EXTRA = ['AGENTS.md', 'CLAUDE.md', 'README.md', 'GUIDE.md']

ENTRY = re.compile(r'^\s*-\s*\[\[([^\]\|#]+?)(?:\|[^\]]*)?\]\]\s*(?::|—|-)?\s*(.*)$')
LINK = re.compile(r'\[\[([^\]\|#]+?)(?:\|[^\]]*)?\]\]')


def existing_descriptions(path):
    out = {}
    if not os.path.exists(path):
        return out
    for line in io.open(path, encoding='utf-8', errors='replace'):
        m = ENTRY.match(line)
        if m:
            name, d = m.group(1).strip(), m.group(2).rstrip()
            if d and name not in out:
                out[name] = d
    return out


def preamble(path):
    if not os.path.exists(path):
        return "---\ntitle: Index\ntype: index\n---\n\n# Index\n"
    t = io.open(path, encoding='utf-8', errors='replace').read()
    i = t.find("\n## ")
    return t[:i + 1] if i > 0 else t


def parse_sections(path):
    """{heading: [raw lines]} so hand-written section prose survives regeneration."""
    out, cur = {}, None
    if not os.path.exists(path):
        return out
    for line in io.open(path, encoding='utf-8', errors='replace'):
        line = line.rstrip("\n")
        if line.startswith('## '):
            cur = line.strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def keep_prose(lines):
    """Drop plain '- [[Page]] - desc' entries; keep intros, bolded sub-lists, notes."""
    out = []
    for l in lines:
        if ENTRY.match(l) and not l.lstrip().startswith('- **'):
            continue
        out.append(l)
    while out and not out[-1].strip():
        out.pop()
    while out and not out[0].strip():
        out.pop(0)
    return out


def pages_in(folder):
    base = os.path.join('wiki', folder)
    if not os.path.isdir(base):
        return []
    found = []
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if f.endswith('.md'):
                found.append(f[:-3])
    return sorted(found, key=str.lower)


def main():
    desc = existing_descriptions(INDEX)
    sections = parse_sections(INDEX)
    before = len(io.open(INDEX, encoding='utf-8', errors='replace').read().split()) if os.path.exists(INDEX) else 0

    root = [f[:-3] for f in os.listdir('wiki') if f.endswith('.md') and f != 'index.md']
    root += [f[:-3] for f in ROOT_EXTRA if os.path.exists(f)]
    blocks = [(ROOT_SECTION, sorted(root, key=str.lower))]
    blocks += [(h, pages_in(f)) for f, h in SECTIONS]

    out = [preamble(INDEX).rstrip() + "\n"]
    seen, added, kept, prose_words = set(), [], 0, 0

    for head, names in blocks:
        if not names and head not in sections:
            continue
        out.append("\n" + head + "\n\n")
        prose = keep_prose(sections.get(head, []))
        in_prose = set()
        if prose:
            prose_words += sum(len(l.split()) for l in prose)
            out.append("\n".join(prose) + "\n\n")
            in_prose = set(LINK.findall("\n".join(prose)))
        for n in names:
            seen.add(n)
            if n in in_prose:
                continue
            if n in desc:
                kept += 1
                out.append("- [[%s]]: %s\n" % (n, desc[n]))
            else:
                added.append(n)
                out.append("- [[%s]]\n" % n)

    text = "".join(out)
    removed = sorted(set(desc) - seen)

    print("pages indexed       : %d" % len(seen))
    print("descriptions kept   : %d" % kept)
    print("section prose kept  : %d words" % prose_words)
    print("new, no description : %d" % len(added))
    for n in added[:12]:
        print("    + %s" % n[:68])
    if len(added) > 12:
        print("    + ... %d more" % (len(added) - 12))
    print("dropped (page gone) : %d" % len(removed))
    for n in removed[:10]:
        print("    - %s" % n[:68])
    print("index.md            : %d -> %d words" % (before, len(text.split())))

    if APPLY:
        io.open(INDEX, 'w', encoding='utf-8', newline='').write(text)
        print("\nAPPLIED")
    else:
        print("\nDRY RUN - nothing written")


if __name__ == '__main__':
    main()
