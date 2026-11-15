---
name: aegis-ingest
description: >
  File a new source into the vault end to end: move it to raw/, write its wiki page,
  back-link participants, route it into a topic hub, and update the indexes. Use whenever a
  file appears in input/, when source content is pasted directly, or when told to "ingest
  this", "file this", "add this to the vault", "here's a transcript/recording/email", or
  pointed at something in the input folder. Covers transcripts, meetings, communications,
  articles, videos and multi-file corpora.
---

**Batch the queue.** An ingest session costs a large fixed overhead regardless of how many files it processes, so two files cost nearly what ten do. **Do everything sitting in `input/` in one session, then close it**: the sources have no value once the pages are written, and carrying them into later work taxes every message.

Collaborative filing, not one-shot summarisation. **Read sources in full, including referenced images.** Discuss the key takeaways with the principal before writing, unless they've said to just proceed.

## Binary sources: convert before reading

**A PDF, DOCX, PPTX, XLSX or scanned image is converted to Markdown first, before any of it is read.** Reading a book-length PDF directly costs 20 pages per call with page images rendered. The same book as Markdown is greppable and reads in 100-line slices. DOCX, PPTX and XLSX cannot be read at all without this step.

**Setup (once):** create a Python virtual environment in the vault root and install Docling into it: `python -m venv .venv`, then `.venv/Scripts/pip install docling` on Windows (`.venv/bin/pip` elsewhere). `.venv/` is gitignored and skipped by the linter.

```
.venv/Scripts/python.exe .claude/scripts/ingest_convert.py --list
.venv/Scripts/python.exe .claude/scripts/ingest_convert.py
```

`--list` shows the queue and file sizes without converting. The converter prints a **token estimate per output file**. **Read that number before opening the result.** A book-length file can be larger than the context window: locate the part you need with `grep -n`, then read only that range. Never open one whole.

**The Markdown is an extraction, not a second source.** The original binary stays the citable source file. Both move to `raw/` together with the same basename, and both take the type prefix at filing time. One `wiki/sources/` page covers the pair, and `sources:` cites the `.md`.

Conversion is local and costs no tokens, but it takes time: budget roughly a second per page on CPU. Run it as a batch and let it finish.

## Definition of done

Verify each and **report the result** before saying it is complete. Work reported done without a verification step is the failure this checklist exists to prevent.

- [ ] Every processed file has **moved** out of `input/` to exactly **one** location in `raw/`: a move, not a copy. Grep `raw/` for the title *and any earlier working name* to confirm a single copy.
- [ ] Each source has **one** wiki page in the correct folder, with valid frontmatter: JSON arrays, correct `type:`, and `sources:` wikilinking the raw file **with its `.md`**.
- [ ] **Never read a page just to append to it.** Use `python .claude/scripts/append_section.py "<file>" "## Communications" "- line"`: it finds the heading and inserts without loading the page. On a large person page that is the difference between thousands of tokens and about twenty. Use `--dry` first if unsure, `--create` if the heading is missing.
- [ ] Every name in `participants:` has **that person's page updated**: the meeting or communication added to their `## Meetings` / `## Communications` section with a one-line summary, or a stub created if they have no page.
- [ ] The source is **routed into a Topic Hub**. If nothing fits, **ask**, never invent a hub or force a bad fit.
- [ ] `log.md` reflects it; `hot.md` if time-sensitive; `decisions.md` if a real decision was settled.
- [ ] **Do not hand-edit `index.md`.** Run `python .claude/scripts/gen_index.py --apply` once at the end of the batch. Editing it by hand means reading the whole catalogue on every ingest, and it drifts anyway. New pages appear as bare lines; add a description later if the page deserves one.
- [ ] **Any standing extraction hook has run.** If the principal maintains a recurring collection: quotable praise, testimonials, pricing data, competitor mentions: it is harvested now, with a timestamp, not rediscovered later by re-reading everything. These are listed in `wiki/identity.md`.
- [ ] **No page created has zero inbound links.**

## Filenames: the collision trap

**Every `raw/` file carries a type prefix, without exception:** `Transcript - <Title>.md`, `<Channel> - <Counterparty> - <Subject> (<date>).md`, `Deck - `, `Web - `, or `<Corpus> - <section> - <file>.md` for a multi-file corpus.

Obsidian resolves wikilinks by **filename across the whole vault, ignoring folders.** A raw file sharing a filename with its own wiki page makes every citation ambiguous and orphans both.

**Run a duplicate-filename scan after creating files, and check the vault root**: clicking an unresolved wikilink creates a note wherever the editor's default location points, which is how a 0-byte duplicate of a very large page ends up at the top level.

## Two ingest modes: ask which applies if it isn't obvious

| Mode | Source is | Pages record |
|---|---|---|
| **Applied** | About the principal's business, clients, or a model they're evaluating | Frameworks **plus** what they mean for the situation now. "How it applies" is the point. |
| **Library** | General reference they want as durable capability | **Applicability conditions only**: when a framework applies, what it gates on, when it fails, where it contradicts another. **No verdicts on their current state.** |

**The default reflex is *applied*, and it is wrong for reference material.** A library page saying "they haven't done X yet" goes stale the moment they do, and narrows a reusable asset into a snapshot of one week. **Write the condition, not the verdict.**

## Hub routing

A source gets a full Details section in its **primary** hub and a one-line pointer in secondaries.

**Check hub size on every ingest.** Past ~8,000 words or ~25 Details sections, `## Details` moves to a companion `<Hub> — Source Details.md` and the Synthesis is rewritten in the same pass. Sections duplicating a `wiki/sources/` page collapse to a roster line; sections with no source page move **verbatim**: they are the only copy.

**Never split a hub by source type or provenance**: that produces two hubs answering the same question. Sub-hub splits are triggered by an incoherent synthesis and are **proposed, never made unilaterally**.

## Chat report after a meeting ingest

**Every meeting or call ingest ends with this report in chat, in this order, whether or not the owner asked for tasks.** A layout kept only as a habit does not survive a new session, so it lives here.

1. **Filed.** One line: what was filed, the page links, and any duplicate, empty or misdated source found.
2. **Summary, one section per meeting.** Heading: name, local date and time, length, and whether the owner attended. Then the main outcome first, followed by the substance in short bullets with timestamps where useful.
3. **Your tasks.** The owner's actions. Each one also lives as a `- [ ]` line on its owning page.
4. **Tasks for others.** One block per other person with actions (for example, the principal the owner supports). Same rule.
5. **Flags.** Risks, unverified figures, contradictions with the vault, and the assistant's own view where the owner may be wrong. Say "none" if empty.
6. **Questions for the owner.** Batched: checkboxes to tick, missing inputs (emails, surnames), routing calls.

**File everything, personal detail included.** The vault is the owner's private record, so nothing heard on a call is withheld from it. Put personal or sensitive detail under a `## Personal context` heading on the meeting page, so it is easy to find and easy to exclude if a page is ever shared.

## Cautions earned the hard way

- **A derived artifact is not a second source.** An auto-summary generated from a defective transcript reproduces its errors and reads as independent corroboration. When speaker labels are suspect, the recording is the only check.
- **Verify the files in a drop belong to the same session.** A participant list from the wrong week will pass every routing check.
- **`raw/` is write-once.** Note source defects on the wiki page; never edit the raw file.
