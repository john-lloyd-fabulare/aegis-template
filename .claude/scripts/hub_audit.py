"""Destination audit. Before collapsing or splitting an oversized topic hub, determine for
every Details section whether its content already exists somewhere else in the vault.

Why this exists: the size rule moves `## Details` into a companion file and collapses any
section that duplicates a `wiki/sources/` page down to a roster line. A section with NO source
page is the only copy of that material, and collapsing it destroys it. This tells you which is
which before you touch anything.

    python .claude/scripts/hub_audit.py                       # audit every hub over the cap
    python .claude/scripts/hub_audit.py "Some Hub" "Another"  # audit named hubs

Read-only. Prints a verdict per section:

    HAS PAGE   - content exists in wiki/sources/. Safe to collapse to a roster line.
    ONLY COPY  - no source page found. Must move VERBATIM, never summarised.
    NO SOURCE  - section cites nothing. Inspect by hand; often a synthesis fragment
                 that belongs in ## Synthesis rather than ## Details.
"""
import os, re, io, sys, collections

HUB_DIR = 'wiki/topic-hubs'
WORD_CAP = 8000

SRC = re.compile(r'\*\*Source:\*\*\s*(.+)')
LINK = re.compile(r'\[\[([^\]\|#]+)')


def vault_names():
    """Every filename and page-name in the vault, for existence checks."""
    names = set()
    for dp, dn, fn in os.walk('.'):
        dn[:] = [d for d in dn if d not in {'.git', '.claude', '.obsidian', 'node_modules'}]
        for f in fn:
            names.add(f)
            if f.endswith('.md'):
                names.add(f[:-3])
    return names


def hubs_over_cap():
    out = []
    if not os.path.isdir(HUB_DIR):
        return out
    for f in sorted(os.listdir(HUB_DIR)):
        if not f.endswith('.md') or f.endswith('— Source Details.md'):
            continue
        txt = io.open(os.path.join(HUB_DIR, f), encoding='utf-8').read()
        if len(txt.split()) >= WORD_CAP:
            out.append(f[:-3])
    return out


def audit(hub, names):
    path = os.path.join(HUB_DIR, hub + '.md')
    if not os.path.exists(path):
        print('  ! not found: %s' % path)
        return collections.Counter()

    txt = io.open(path, encoding='utf-8').read()
    body = txt.split('## Details', 1)[1] if '## Details' in txt else txt
    sections = re.split(r'\n### ', body)[1:]

    tally = collections.Counter()
    print('\n%s  (%d words, %d Details sections)' % (hub, len(txt.split()), len(sections)))
    print('-' * 72)

    for sec in sections:
        title = sec.split('\n', 1)[0].strip()
        m = SRC.search(sec)
        if not m:
            verdict = 'NO SOURCE'
        else:
            cited = LINK.findall(m.group(1))
            cited = [c.strip() for c in cited]
            # a source page exists if any cited name resolves to a file in the vault
            hit = any(c in names or (c + '.md') in names for c in cited)
            verdict = 'HAS PAGE' if hit else 'ONLY COPY'
        tally[verdict] += 1
        print('  %-10s %s' % (verdict, title[:58]))

    return tally


def main():
    names = vault_names()
    targets = sys.argv[1:] or hubs_over_cap()

    if not targets:
        print('No hubs over the %d-word cap. Nothing to audit.' % WORD_CAP)
        return

    total = collections.Counter()
    for hub in targets:
        total.update(audit(hub, names))

    print('\n' + '=' * 72)
    for k in ('HAS PAGE', 'ONLY COPY', 'NO SOURCE'):
        if total[k]:
            print('  %-10s %d' % (k, total[k]))
    if total['ONLY COPY']:
        print('\n  %d section(s) are the only copy of their content.' % total['ONLY COPY'])
        print('  Move those VERBATIM into the companion file. Do not summarise them.')


if __name__ == '__main__':
    main()
