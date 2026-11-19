# AEGIS

**Augmented Executive Guidance & Intelligence System**: a file-based executive assistant that remembers.

No database, no app, no vendor. Plain Markdown, YAML frontmatter and `[[wikilinks]]` on disk, plus a constitution your AI agent reads at the start of every session and a set of procedures it loads only when the work calls for them.

This is a **template**. Clone it, open it with an agent, and it will interview you and rewrite itself to be yours.

---

## Quick start

1. **Copy this folder** to wherever you want your vault to live. Rename it if you like.
2. `git init`: you want history from day one. Every rule in here assumes nothing is ever really deleted.
3. **Open the folder with an AI coding agent**: Claude Code, or anything that reads `AGENTS.md` and can write files.
4. **Say anything.** The first thing it does is notice `wiki/identity.md` is missing, and run the setup interview.

That's it. Setup takes about five minutes and ends with your vault configured, your name in the constitution, and the first-run gate removed.

**Then read [GUIDE.md](GUIDE.md)**: how to actually use it, what it's good at, where it falls down, and how to set up backup and sync.

### What setup asks you

Who you are and what you do · what you want to call the assistant · the two or three things you most want it to handle · who it will be writing for · how blunt you want it · whether you want coaching or just answers · anything that annoys you about AI assistants · what it must never do without asking.

"I don't know yet" is a valid answer to all of it. Blanks get marked and can be filled in later by just saying so.

---

## How it works

### The bet

**The expensive resource is context, not storage.** A vault can hold half a million words as long as any single session reads only the few hundred it needs. Every rule in `AGENTS.md` exists to keep that true.

That's the whole difference between this and a folder of notes. A folder of notes gets slower to use as it grows. This is designed so it doesn't.

### The four layers

Material moves in one direction and is never edited upstream of where it landed.

```
input/   →   raw/   →   wiki/
 queued     source     synthesis
```

- **`input/`**: your drop box. Nothing here has been read. A file sitting here is the visible signal that it's still queued.
- **`raw/`**: source material, once filed. **Write-once.** Never edited, never auto-deleted.
- **`wiki/`**: everything the assistant writes. People, projects, topic hubs, meeting notes, decisions. This is the layer that answers questions.
- **`AGENTS.md`**: the constitution. Model-neutral. `CLAUDE.md` is a thin adapter that imports it; add your own for another runtime.

### The context budget

This is the load-bearing part.

| File | When it's read |
|---|---|
| `wiki/hot.md` | **Every session.** ~500 words, capped. What's active now. |
| `wiki/priorities.md` | Only when the task turns on goals or a long-term trade-off. |
| `wiki/identity.md` | Only when the task turns on who you are or how you work. |
| `wiki/index.md` | **Never at session start.** It's a catalogue for humans. The agent uses `grep`. |

Procedures work the same way: the six skills in `.claude/skills/` cost nothing until a prompt matches one.

### The procedures

| When | What it does |
|---|---|
| Something lands in `input/` | Files it end to end: raw, wiki page, back-links, hub routing, index |
| You ask what the vault knows | Answers at the shallowest reliable depth, with citations |
| You want content for a client | **Loads that client's voice guide first.** Mandatory gate. |
| You ask what's broken | Lints the vault's own machinery and proposes repairs |
| Anything gets written to `wiki/` | Applies the folder, filename and frontmatter conventions |

---

## Using it day to day

**To remember something:** drop it in `input/` and say *"ingest this"*. Transcripts, emails, PDFs, articles, a whole folder of them. It reads the source, writes the pages, links the people, and files it.

**To recall something:** just ask. *"What do we know about X?"* · *"What did we decide about Y?"* · *"Who is Z?"* · *"What's the status of the thing I was doing last week?"*

**To keep working across sessions:** work items carry a `## Resume from` line, written *before* you stop rather than after. Close the laptop mid-task and the next session picks up from a truthful checkpoint.

**To fix the vault itself:** *"what's broken?"* runs a lint pass: broken links, orphan pages, malformed frontmatter, hubs that outgrew their cap.

---

## What's in here

```
AGENTS.md            the constitution: model-neutral core
CLAUDE.md            thin runtime adapter
SETUP.md             the first-run interview (deletes itself when done)
README.md            this file: what AEGIS is, and quickstart
GUIDE.md             how to use it: features, strengths, weaknesses, Obsidian, git, sync

input/               unread, unfiled
raw/                 write-once source material
wiki/                everything generated
  hot.md             READ EVERY SESSION. ~500 words, capped.
  identity.md        written by setup, who you are, how you work
  priorities.md      standing goals
  index.md           generated, never hand-edited, never read at start
  health.md          open defects in the vault itself
  decisions.md       append-only: what was decided
  outcomes.md        append-only: whether it was right
  log.md             append-only: edits to the wiki
  people/ concepts/ projects/ topic-hubs/ sources/
  meetings/ communications/ work-items/ cases/
  answers/ journal/ content-drafts/

.claude/
  skills/            six procedures, loaded on demand
  scripts/           six Python maintenance scripts
```

### The scripts

Run from the vault root. Python 3, no dependencies.

```bash
python .claude/scripts/aegis_lint.py -v
```

| Script | Does |
|---|---|
| `aegis_lint.py` | Health check. Alias-, code-fence- and escaped-pipe-aware: a naive link checker reports confident nonsense. |
| `gen_index.py` | Regenerates `index.md`, preserving hand-written descriptions. `--apply` to write. |
| `append_section.py` | Adds a line under a heading **without loading the page**. Thousands of tokens → about twenty. |
| `hub_audit.py` | Before splitting an oversized hub, says which sections are the only copy of their content. |
| `owner_tasks.py` | Lists one owner's open `- [ ] Owner:` task lines from every page's `## Tasks` section, newest first. `--owner Alex`, plus `--days` and `--json`. Reads only, so tasks never get a second copy. |
| `welcome.py` | Prints the paste-ready welcome message after setup. `--tour` for the longer version. |

---

## Design notes

**Why no embeddings?** The corpus is small, the link graph is hand-curated, and `grep` over a few hundred files is instant. A vector store adds an index that goes stale, a similarity score nobody can audit, and a second source of truth. The synthesis layer does the work embeddings would do: a topic hub *already is* the answer to a class of question, written once by a model that read every source.

**Why is `index.md` forbidden at session start?** Because it's useful *to a human*. Models don't browse; they pay full price for every token. Past a few thousand words it becomes the most expensive file in the vault and the least load-bearing.

**Why append-only ledgers?** A decision log that gets tidied is a log of what you currently believe you decided. `outcomes.md` is separate so a decision and its verdict can disagree in writing.

**Why does every rule read like it was written after an incident?** Because it was. None of these constraints were designed in advance, each is a repair for a specific failure. That's why the reasons are attached: a rule whose reason is lost gets deleted by the next person who finds it inconvenient.

**What should you re-measure rather than inherit?** Every threshold. The ~500-word cache cap, the ~8,000-word hub ceiling, the ~40-line health file, the ~100-page point where linting starts paying: all tuned against one vault's size and one model's context window. The *existence* of a cap transfers; the number may not.

**What kills a vault like this?** It dies from being read, not from being written. The sequence is always the same: an index grows because it's useful to a human → the model starts reading it because it's there → every session pays for it → the assistant gets slower and vaguer as the vault gets richer. **Cap what loads, or the system inverts.**

---

## Viewing the vault

The vault is plain Markdown with `[[wikilinks]]`, so any editor can open it. A Markdown knowledge-base app makes it far easier to see.

- **[Obsidian](https://obsidian.md)** (recommended): open the folder as a vault. The graph view shows how people, projects and topics connect, backlinks show every page that points at the one you are reading, and Dataview can query the frontmatter. The template ships an `.obsidian/` folder ready to use. See [GUIDE.md](GUIDE.md) for setup.
- **[Foam](https://foambubble.github.io/foam/)** for VS Code: wikilinks, backlinks and a graph inside the editor, useful if you already work there.
- **[Logseq](https://logseq.com)** can also open a folder of Markdown files, though it is outline-first and may reformat pages, so test it on a copy first.

The agent does not need any of these. They are for you, to browse and check what it has written.

## Adapting it

- **Another runtime?** Write a new adapter next to `CLAUDE.md` that imports `AGENTS.md` and describes that runtime's tool access. Don't fork the core.
- **Don't need clients?** Delete the `aegis-content` skill and the `content-drafts/` folder. Setup will notice you said "just me" and can do this for you.
- **Different folder taxonomy?** Change it in `aegis-vault-writing`, `AGENTS.md`, and `gen_index.py`'s `SECTIONS` list: the three places that know about folders.
- **Don't create folders before you need them.** Empty folders invite filing decisions made in the abstract, and those get re-litigated for months.

---

**New here?** [GUIDE.md](GUIDE.md) is the walkthrough: your first hour, the daily loop, every feature explained, an honest list of what this is bad at, and how to put the vault in Obsidian and back it up to a private repo.
