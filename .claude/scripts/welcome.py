# -*- coding: utf-8 -*-
"""Print the paste-ready welcome message after setup.

Reads wiki/identity.md, fills the templates in
.claude/skills/aegis-setup/WELCOME.md, and prints one block to stdout.
The agent pastes the output into chat verbatim.

    python .claude/scripts/welcome.py           # the short close (default)
    python .claude/scripts/welcome.py --tour    # the two-minute tour, only if asked

Wording lives in WELCOME.md, not here. Edit that file to change what is said.
Run from the vault root.
"""
import io
import os
import re
import sys
import textwrap

IDENTITY = os.path.join('wiki', 'identity.md')
TEMPLATES = os.path.join('.claude', 'skills', 'aegis-setup', 'WELCOME.md')

BLANK_MARKERS = ('not yet set', 'nothing stated', 'none', '<or', 'tbd', '')

# field label in identity.md -> what to call it when reporting it as blank
FRIENDLY = {
    'timezone / hours': 'your timezone and working hours',
    'answers to': 'who you answer to',
    'role': 'what you do',
    'explicitly not for': 'what this is not for',
    'never without asking': 'what I should never do without asking',
    'never enters this vault': 'what must never go in the vault',
    'stated dislikes': 'what annoys you about AI assistants',
    'writing for': 'who this writes for',
}


def read(path):
    if not os.path.exists(path):
        return None
    return io.open(path, encoding='utf-8').read()


def parse_identity(text):
    """Pull '- **Label:** value' pairs out of identity.md."""
    fields = {}
    for label, value in re.findall(r'^\s*[-*]\s*\*\*(.+?):\*\*\s*(.*)$', text, re.M):
        fields[label.strip().lower()] = value.strip()
    # bullets under '## Writing for' that are not label/value pairs
    m = re.search(r'##\s*Writing for\s*\n(.*?)(?:\n##|\Z)', text, re.S)
    if m:
        items = [l.strip('-* ').strip() for l in m.group(1).strip().split('\n') if l.strip().startswith(('-', '*'))]
        items = [i.split(':')[0].strip() for i in items if i]
        fields['writing for'] = ', '.join(i for i in items if i)
    return fields


def is_blank(value):
    v = (value or '').strip().lower().strip('*_` ')
    return v in BLANK_MARKERS or v.startswith('<')


def get_block(templates, name):
    """Extract the fenced block under '## BLOCK: <name>'."""
    m = re.search(r'##\s*BLOCK:\s*' + name + r'\b.*?```\n(.*?)```', templates, re.S)
    if not m:
        sys.exit("welcome.py: no BLOCK '%s' found in %s" % (name, TEMPLATES))
    return m.group(1).rstrip('\n')


def main():
    tour = '--tour' in sys.argv

    templates = read(TEMPLATES)
    if templates is None:
        sys.exit('welcome.py: %s not found. Run from the vault root.' % TEMPLATES)

    if tour:
        print(get_block(templates, 'tour'))
        return

    ident = read(IDENTITY)
    if ident is None:
        sys.exit('welcome.py: %s not found. Run the setup interview first.' % IDENTITY)

    f = parse_identity(ident)
    name = f.get('name') or 'there'
    assistant = f.get('called') or 'AEGIS'

    blank_labels = [FRIENDLY.get(k, k) for k, v in sorted(f.items())
                    if k in FRIENDLY and is_blank(v)]

    if blank_labels:
        if len(blank_labels) == 1:
            listed = blank_labels[0]
        else:
            listed = ', '.join(blank_labels[:-1]) + ' and ' + blank_labels[-1]
        blanks = get_block(templates, 'blanks').replace('{blanks_list}', listed)
        blanks = os.linesep.join(textwrap.wrap(' '.join(blanks.split()), width=76))
        blanks = blanks.replace('\r\n', '\n')
    else:
        blanks = ''

    out = get_block(templates, 'short')
    out = out.replace('{name}', name)
    out = out.replace('{assistant}', assistant)
    out = out.replace('{clients}', f.get('writing for', ''))
    out = out.replace('{bluntness}', f.get('bluntness', ''))
    out = out.replace('{coaching}', f.get('coaching', ''))
    out = out.replace('{blanks}', blanks)

    # collapse the gap left when there are no blanks to report
    out = re.sub(r'\n{3,}', '\n\n', out)
    print(out)


if __name__ == '__main__':
    main()
