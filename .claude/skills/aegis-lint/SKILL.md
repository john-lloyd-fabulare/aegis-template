---
name: aegis-lint
description: >
  Diagnose and repair defects in the vault itself: broken wikilinks, orphan pages, duplicate
  filenames, malformed frontmatter, oversized hubs, stale caches. Use when asked what's broken,
  for a health check, a cleanup, an audit, a lint pass, or when told something in the vault
  looks wrong, redundant, or out of date. Not for business problems: only the vault's own
  machinery.
---

## Read first, in this order

1. **`wiki/health.md`**: what is already known to be open, and what was examined and **deliberately left alone**. Without this you will re-derive the same findings every pass.
2. **`wiki/concepts/Vault Failure Modes.md`**, once it exists: the defect classes this vault actually produces, and the diagnosis for each. **Most "new" problems are one of those wearing a different hat.**

## Measure before proposing

*"This looks redundant"* is an opinion. *"Three of these four have zero inbound links"* settles it. **Propose, then apply what's confirmed, then log it.**

## The checker must be right before its output is

A link checker that is not **alias-aware**, **code-fence-aware** and **escaped-pipe-aware** will report confident nonsense. A checker with three blind spots produced 28, then 7, then 1 false positives as each was fixed: its reported count fell 24 → 17 → 2 with the vault unchanged. The number measured the tool, not the vault.

**Before reporting any number, confirm the checker handles:**

- `aliases:` in frontmatter: the editor resolves `[[Alias]]` to its canonical page
- fenced ```` ``` ```` blocks: documentation examples are **not** broken links
- backticked spans: `` `[[Example]]` `` is deliberately inert
- escaped pipes in tables: `[[Page\|Display]]` is correct syntax, not a filename ending in a backslash
- non-`.md` targets: PDFs, CSVs and images are legitimate link targets
- companion files: `type: topic-hub-details` is exempt from the hub size cap

**Never assert a vault fact without opening the file.** "This file is empty," inferred from "I have not written to it," is the classic error and it is reliably wrong.

## The tools

- **`.claude/scripts/aegis_lint.py`**: run from the vault root. Alias-aware, code-fence-aware, escaped-pipe-aware, and exempts `type: topic-hub-details` companions from the hub cap. `-v` lists every finding. **This is the canonical measure; `wc` disagrees by a few percent on multibyte text.**
- **`.claude/scripts/gen_index.py`**: regenerates `index.md` from the filesystem, preserving every hand-written description and section intro. **`index.md` is never hand-edited.**
- **`.claude/scripts/append_section.py`**: add a line under a heading without loading the page.
- **`.claude/scripts/hub_audit.py`**: for any hub restructure, classifies every Details section by whether its content exists elsewhere. **Run it before compressing or deleting anything.**

## Standard checks

| Check | Target |
|---|---|
| Broken wikilinks in live files | 0 |
| Malformed frontmatter arrays | 0 |
| Orphan pages | 0 |
| Duplicate filenames, **including the vault root** | 0 |
| Hubs over ~8,000 words | 0 |
| `hot.md` | under ~500 words |
| Pages past `freshness_date` | classified, not silently trusted |

## Repair rules

- **De-link external entities; do not stub them.** A stub for an organisation nobody references becomes an orphan: the defect one level up.
- **Fix the rule when reality disagrees with it.** A large batch of filename/title mismatches is usually the *rule* being wrong, not the files.
- **`raw/` is write-once and nothing auto-deletes.** Deleting from `raw/` requires explicit approval, every time.
- **Append-only means append-only.** `log.md`, `decisions.md` and `outcomes.md` are never rewritten to look tidier. Corrections go forward.

## Afterwards

Fixed entries **leave `health.md`** and get one line in `log.md`. A defect seen a third time **graduates to `wiki/concepts/Vault Failure Modes.md`** as a named class: create that page on the third occurrence, not before. Keep `health.md` under ~40 lines; hitting the cap schedules a pass, it does not justify a bigger file.
