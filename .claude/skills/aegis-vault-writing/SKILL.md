---
name: aegis-vault-writing
description: >
  Conventions for creating or editing any page in the wiki, which folder it belongs in,
  filename rules, frontmatter schema, topic-hub format, and the safe rename procedure. Use
  whenever writing a new wiki page, renaming or moving one, deciding where something belongs,
  or editing frontmatter. Load before creating a page, not after.
---

## Folders

| Folder | Contents |
|---|---|
| `people/` | One page per person: the principal (the hub of the wiki), colleagues, clients, public figures. |
| `topic-hubs/` | One page per *answerable topic*. The synthesis layer. |
| `concepts/` | Ideas, frameworks, terminology, **and reference material about a specific person, org, tool or named framework** (voice guides, tech stack, operating models). |
| `projects/` | Goals and initiatives: anything with a status and a direction. |
| `sources/` | One page per ingested source, 1:1 with a file in `raw/`. *Exception:* a source directly about the principal folds into their person page. |
| `meetings/<person>/` | One folder per person whose meetings are tracked. The principal's own folder = meetings they attended. **Ask before creating a new context folder.** |
| `communications/<person>/` | Same participant split. |
| `journal/` | Dated reflection entries, `YYYY-MM-DD Short Title.md`. |
| `answers/` | Substantial query answers worth keeping. |
| `content-drafts/<Client>/` | Client drafts. **No index pages inside**: drafts are found by folder and linked from the client's project page. Built files go in `content-drafts/<Client>/assets/` alongside the script that made them; the markdown stays the source of truth. |
| `work-items/` | `type: work-item`. One flat folder: **status lives in frontmatter, never in the folder path.** Storing it twice means syncing two things by hand forever, and they will drift. |
| `cases/` | `type: case`. Reusable solved-problem records, retrieved by `problem_patterns:` in frontmatter. **No global case index**: it would drift into another oversized navigation page. |

**One page per event, never cross-list.** A meeting or communication lives in exactly one folder. Discovery from a second person's angle is handled by **index entries and `participants:`**, never a duplicate file.

**Meetings vs communications: the deciding test:** was there a transcript of people talking in real time? → **meeting**. Is it a message someone composed and sent? → **communication**. A video call is always a meeting, whatever the platform. A long email thread is a communication however many people are on it.

## Filenames

**Filenames match the page title exactly, in Title Case: including index pages.** Obsidian resolves wikilinks by **filename**, never by `title:`. An `index.md` with a nice title is unlinkable.

**The one exception is a date or period suffix.** A filename may carry a trailing disambiguator the `title:` omits: a date (`Foo (2026-08-05).md` titled `Foo`), a week range, or an edition. The suffix keeps filenames unique, which is what prevents the ambiguity trap. **The filename wins.**

### Safe rename

1. Grep the whole vault for the old name, including `[[Old\|Display]]` piped forms and any alias.
2. Rename the file.
3. Update every hit, or add the old name to `aliases:` in the renamed page's frontmatter if inbound links are numerous.
4. Re-run the linter. A rename that leaves one broken link has failed.

## Frontmatter

```yaml
---
title: Page Title
type: person   # person | topic-hub | topic-hub-details | concept | project | source |
               # work-item | case | identity |
               # meeting | communication | journal | answer | content-draft | health
tags: []
created: 2026-01-01
updated: 2026-01-01
sources: []
---
```

Optional: `aliases:` · `claims:` (claim + source + verification date + confidence tag: `evidence-based` | `practitioner` | `contested` | `folklore`) · `freshness_date:` for time-sensitive material.

Meetings add `participants:` and `parent:`. Communications add `participants:`, `channel:` (`email`|`slack`|`whatsapp`|`sms`|`discord`|`other`) and `direction:` (`inbound`|`outbound`|`thread`). **`parent:` is meetings-only.** Work items add `status:` (`open`|`blocked`|`awaiting-input`|`done`). Cases add `problem_patterns:`.

**Multi-value fields are JSON arrays, always:**
- ✅ `sources: ["[[Page A]]", "[[Page B]]"]`
- ❌ `sources: [[Page A]], [[Page B]]`: a top-level comma is a YAML error that discards the **entire** frontmatter block
- ❌ `sources: [[Page A]]`: parses as a *nested list*; renders no link at all, and errors nowhere, so it propagates silently across dozens of pages

**`sources:` uses `[[wikilinks]]` for anything that is a file in this vault**, including non-markdown and raw files (with `.md`). Plain strings only for external URLs or files not archived here. **Never wrap a wikilink in backticks**: code spans are not parsed as links. Conversely, wikilinks *inside documentation or examples* **should** be backticked so the editor doesn't create phantom graph nodes.

## Topic hubs

`type: topic-hub`, then exactly three sections: **`## Synthesis`** (your analysis across every source, written as an opinion addressed to the principal, saying so wherever sources disagree), **`## Details`** (one `###` per source: Summary · Key takeaway · How it applies · inline `Source:` link), **`## Related Topics`** (plain links, **bidirectional**, so if A links to B the reverse goes on B in the same edit).

**Hub or concept?** Hub = *"what do we know about ___?"*. Concept = *"what is ___ / how does ___ work?"*

**Size rule.** Past ~8,000 words or ~25 Details sections, move `## Details` to `<Hub> — Source Details.md` (`type: topic-hub-details`) and **rewrite the Synthesis in the same pass**. Sections duplicating a `wiki/sources/` page collapse to a roster line carrying the key takeaway verbatim; sections with no source page move **verbatim**. **A hub is capped by what it must answer, not by how much it has read.**

## Work items

The point of a work item is **resume-from**. Three headings, minimum: `## Goal` (why this exists, one paragraph), `## State` (what is true now), `## Resume from` (the literal next action, specific enough to start without re-reading the whole page). Update it *before* switching tasks, not after.
