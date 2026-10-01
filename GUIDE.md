# Using AEGIS

**Read this after setup.** The README explains what AEGIS is; this explains how to actually work with it, what it's good at, where it will let you down, and how to set up backups and sync.

You don't need to read it all now. Sections 1 to 3 get you working. The rest is there when you hit it.

---

## 1. The mental model, in sixty seconds

You have an assistant with a filing cabinet. **Three things go in the cabinet, and they go in one direction:**

```
you drop a file        it files the source        it writes what it learned
   input/        →          raw/           →           wiki/
  "unread"              "never edited"            "the part that answers"
```

Everything you ask it later gets answered from `wiki/`, not from the original files, and not from the model's memory of your conversation. **If it isn't written down, it doesn't exist.** That's the deal. It's also why this works: a conversation ends, but a file doesn't.

The one habit that makes AEGIS work: **when something matters, say so, and let it get written down.** Everything else follows.

---

## 2. Your first hour

Do these in order. Each takes a few minutes and teaches you one part of the loop.

### Step 1: Feed it something real

Find one file you'd genuinely want to remember. A meeting transcript, a long email thread, a PDF you keep re-reading, notes from a call. Put it in `input/`.

Then say:

> **ingest this**

Watch what happens. It reads the source, moves it to `raw/`, writes a page in `wiki/sources/`, creates pages for any people mentioned, files it under a topic, and updates the index. Ask it to walk you through what it did if you want to see the shape.

**This is the single most important thing to try first**, because until pages exist, nothing else in the system has anything to work with.

### Step 2: Ask it something only that file knows

> **what do we know about \<something from the file\>?**

It should answer with citations: `[[links]]` to the pages it drew from. If it answers without citing anything, tell it so; that's a rule it's supposed to follow.

### Step 3: Ask it something it can't know

> **what do we know about \<something you never told it\>?**

The correct answer is *"the vault doesn't record this."* If you get a confident invented answer instead, you've found the failure mode that matters most: see §7.

### Step 4: Start something and abandon it

Ask it to help with a multi-step task: a plan, a draft, a piece of research. Get partway. Then say:

> **I'm stopping here, save the state**

It should write a work item with a `## Resume from` line. Close the session. Open a new one tomorrow and say *"what was I doing?"*: if the checkpoint is good, you'll pick up without re-explaining.

### Step 5: Break something on purpose

> **what's broken?**

Runs a health check on the vault itself. On a young vault it'll mostly say "orphan pages," which is normal until pages start linking to each other.

---

## 3. The daily loop

Most days you'll use four phrases.

| You say | What happens |
|---|---|
| **"ingest this"** (with files in `input/`) | Source gets filed, pages get written, people get linked |
| **"what do we know about X?"** | Answered from the vault, with citations, at the shallowest depth that's reliable |
| **"what was I doing?"** | Reads `hot.md` and the open work items |
| **"save the state"** / **"I'm stopping"** | Writes the checkpoint before you lose it |

That's the whole system in daily use. Everything below is refinement.

### Batch your ingests

An ingest session has a large fixed cost regardless of how many files it handles. **Two files cost nearly what ten do.** Let `input/` accumulate for a few days, then clear it in one sitting. Don't ingest one file at a time as it arrives: that's the most expensive possible pattern.

---

## 4. The features, one at a time

### Ingest: putting things in

Handles transcripts, emails, PDFs, articles, decks, images, and whole folders of related files. It reads sources **in full**, including images, rather than skimming.

It'll ask you one question worth understanding: **applied or library?**

- **Applied**: the source is about *your* business. Pages record the framework *and* what it means for your situation now.
- **Library**: general reference you want as durable capability. Pages record **only the conditions under which something applies**, never verdicts about your current state.

The distinction matters because a library page saying *"you haven't done X yet"* goes stale the moment you do, and turns a reusable asset into a snapshot of one week. If it guesses wrong, correct it: the default reflex is "applied," and that's wrong for reference material.

### Query: getting things out

It reads in layers and stops at the shallowest one that answers reliably: the hot cache → the topic hub's synthesis → the source details → the individual source page → the original raw file. Most questions are answered at layer two.

**Provenance questions are different from content questions.** *"Do we have the complete recording?"* is answered by checking the disk: one copy, cited correctly, full source not an excerpt. Ask it that way when you need to be sure something is actually archived.

### Topic hubs: where synthesis lives

A hub answers *"what do we know about ___?"* across every source that touched the topic. It has a **Synthesis** section (the assistant's actual opinion, written for you, flagging where sources disagree) and a **Details** section with one entry per source.

This is the part that makes the vault smarter than the sum of its files. It's also the part that needs maintenance: past ~8,000 words a hub gets split, and the synthesis is rewritten. Let it do that when it offers.

### Work items: surviving interruption

The point isn't tracking. It's **resume-from**. Each carries a goal, current state, and the literal next action, written *before* you stop rather than after.

Status lives in the file's frontmatter, never in a folder name, so nothing has to be moved when something changes state.

### Decisions and outcomes: kept separate on purpose

`decisions.md` records what you decided and why. `outcomes.md` records whether it was right. **Both are append-only and never tidied**, so a decision and its verdict can disagree in writing.

That separation is the most under-used feature here. A decision log that gets edited once you know the answer is a log of what you currently believe you decided. Reviewing outcomes against decisions every month or two is where the actual learning happens.

### Voice guides: content for other people

If you write anything published under a client's name, the assistant is **required** to load that client's voice guide first, in full, every time. It won't draft without one, and if the guide doesn't exist, it should stop and build one with you from real samples.

Getting this right early is worth the hour. A voice set by accident gets defended for a year.

### Cases: hard problems, solved once

When something takes real diagnosis to figure out, and it'll probably happen again, it becomes a case. Retrieved by problem pattern, not by browsing.

**Deliberately rare.** Routine success doesn't qualify. If it's not written as a case, the lesson stays on the work item until the problem shows up a second time.

### The scripts

Run from the vault root. Python 3, no dependencies.

```bash
python .claude/scripts/aegis_lint.py -v
```

`aegis_lint.py` health-checks the vault · `gen_index.py` regenerates the catalogue · `append_section.py` adds a line to a page without loading it · `hub_audit.py` checks what's safe to collapse before splitting a hub · `welcome.py` printed the message you saw after setup.

You'll rarely run these yourself: the assistant uses them. Worth knowing they exist so you can ask for a health check.

---

## 5. What it's genuinely good at

**Remembering across time.** The problem it actually solves: you had a conversation three months ago and the useful part is gone. Here it's a file, linked from the people and topics it touched.

**Synthesis across sources.** Ten transcripts mentioning the same problem become one hub with an opinion about it. No chat interface does this, because no chat interface has the previous nine conversations.

**Provenance.** Every claim traces to a file. When it can't be traced, it's marked unverified. You can audit any answer back to its source, which matters more than it sounds, because it's what makes the vault trustworthy enough to act on.

**Surviving interruption.** Work items and handoffs mean a closed laptop isn't a lost thread.

**Portability.** Plain Markdown on your disk. No vendor, no export, no lock-in, no subscription that can change terms. Readable in fifteen years by anything.

**Getting better with use.** Every session that surfaces something durable updates the wiki. The system compounds; a chat history doesn't.

---

## 6. What it's bad at: read this one

Being honest about this is more useful than selling it.

**Nothing runs when you're not there.** No background jobs, no scheduled ingests, no alerts. If nobody opens a session, nothing happens. It's a filing system with a very good librarian, not an autonomous agent.

**It only knows what you feed it.** It cannot see your inbox, calendar, CRM or phone unless you put something from them in `input/`. The gap between "what I know" and "what the vault knows" is entirely on you to close.

**It costs tokens, and the cost is proportional to discipline.** Ingesting one file at a time, letting the hot cache bloat past its cap, or letting an index get read at session start will make it expensive and slow. The caps in this template exist because each of those happened somewhere.

**Search is literal, not semantic.** Retrieval is `grep` plus a hand-curated link graph. If you filed something under "pricing" and search for "cost structure," you may miss it. The hub layer is what compensates, but only for topics that have hubs.

**It can still be wrong.** The rules say cite-or-flag and never-assert-without-opening-the-file. Rules reduce hallucination; they don't eliminate it. **Spot-check citations occasionally.** If a page is cited, open it once in a while and confirm it says what the answer claimed.

**Everything is plain text on disk.** No encryption. Anything sensitive (credentials, NDA material, health or legal records) should not go in here unless the whole folder sits on an encrypted disk and a private repo. Setup asks about this; take the question seriously.

**Quality tracks the model.** A weaker model produces a weaker synthesis from the same sources. The vault is durable; the writing in it reflects whatever wrote it.

**It needs a human editor.** Hubs drift. `hot.md` goes stale. Old pages contradict new ones. Run a lint pass every month or so and actually act on it: a vault nobody maintains degrades into a folder of notes, which is exactly the thing it was built to beat.

**Merge conflicts are real** if you sync across machines. See §8.

---

## 7. The failure modes you'll actually hit

| Symptom | What's happening | Fix |
|---|---|---|
| Answers feel generic, don't cite anything | It's answering from the model, not the vault | Say *"answer from the vault and cite it, or tell me it's not there"* |
| It states something confidently that's wrong | Unverified recall presented as fact | Ask *"which file says that?"*: if there isn't one, tell it to mark it unverified. It's supposed to do this unprompted |
| Sessions feel slow and expensive | Something oversized is being read at startup | Ask *"what did you read at session start?"*: the answer should be `hot.md` and nothing else |
| It can't find something you know is there | Filed under different words than you searched | Ask *"grep the vault for X"*, and consider whether that topic needs a hub |
| `hot.md` has become a to-do list | Cap breached, detail leaked in | Ask it to compress: detail moves to linked pages, never a bigger cap |
| Same defect reported every lint pass | It's not in the "deliberately left alone" section | Tell it to record the decision in `health.md` so it stops re-proposing it |
| It re-ran the setup interview | The FIRST RUN gate wasn't removed | Check `AGENTS.md`: that section should have been deleted at setup |

---

## 8. Bonus: Obsidian, backups, sync

The vault is just Markdown files, which means a lot of things work with it for free.

### Obsidian

**Strongly recommended.** [Obsidian](https://obsidian.md) is a free Markdown editor that reads exactly the format this vault uses. Open the vault folder as an Obsidian vault and you get:

- **Clickable `[[wikilinks]]`**: the link graph becomes navigable
- **Graph view**: see how the vault actually connects. Genuinely useful for spotting orphans and clusters
- **Backlinks panel**: every page shows what links *to* it
- **Instant search** across everything
- **Tag and property browsing** from the frontmatter

Nothing about Obsidian is required (this stays plain Markdown either way) but reading the vault as a human is much better with it.

A few things to know: Obsidian resolves links **by filename across the whole vault, ignoring folders**, which is why filenames in here carry type prefixes and never collide. And clicking a broken link creates a new note wherever Obsidian's default folder points, which is how stray files end up at the root. If you see an unexpected file there, that's usually why.

### Git: the backup that also gives you history

`git init` inside the vault on day one. Not for collaboration: for the undo button.

Because everything is text, git gives you a complete history of what the assistant wrote and when, the ability to see exactly what changed in any session, and recovery from any mistake including a deletion.

```bash
git init
git add -A
git commit -m "initial vault"
```

Then commit at the end of any session that changed things. You can ask the assistant to do it.

### A private repo: cloud backup for free

Create a **private** repository on GitHub (or GitLab, or Codeberg) and push to it. Free, versioned, off-machine, and restorable to any computer with one `git clone`.

```bash
gh repo create my-vault --private --source=. --push
```

**Make it private.** This vault will accumulate everything you know about your work, your clients and your colleagues. That's not a public artifact, and it's very hard to un-publish.

If any part of the vault must never leave your machine, add that folder to `.gitignore` before the first push, not after. Git remembers.

### Working across machines

Clone the private repo on your second machine. `git pull` before you start, `git push` when you finish.

**The one real hazard:** if you work on two machines without pulling, you'll get merge conflicts. Markdown conflicts are readable and fixable by hand, and the append-only ledgers conflict most often since both sides append at the bottom. Habit that avoids nearly all of it: **pull first, push last, every session.**

### Mobile

Obsidian's mobile app opens the same vault. Getting the files onto a phone is the fiddly part: the common approaches are a git plugin for Obsidian, or syncing the folder through iCloud/Dropbox/Syncthing.

**Don't use a file-sync service and git on the same folder at the same time.** They will fight over the `.git` directory and you'll lose work. Pick one.

Realistically, mobile is good for *reading* the vault and capturing quick notes into `input/`. The assistant work happens on a computer.

### Other AI runtimes

`AGENTS.md` is deliberately model-neutral: no runtime-specific syntax anywhere in it. `CLAUDE.md` is a thin adapter that imports it and describes one runtime's tools.

To use a different agent, write a new adapter beside it that does the same thing for that runtime. **Don't fork the core.** Two divergent copies of the operating model is a problem you'll be untangling for months.

### Scaling up

Around a few hundred pages you'll want to run a lint pass regularly. Past that, watch for hubs outgrowing their cap and for `hot.md` slowly becoming a project list.

Nothing here breaks at scale, but nothing maintains itself either. **The vault degrades from neglect, not from size.**

---

## 9. Cheat sheet

```
ingest this                          file everything in input/
what do we know about X?             answer from the vault, cited
what did we decide about X?          check decisions.md
who is X?                            person page
what was I doing?                    hot cache + open work items
save the state / I'm stopping        write the checkpoint now
what's broken?                       lint the vault itself
which file says that?                demand provenance for a claim
grep the vault for X                 literal search when recall fails
write a voice guide for X            before any content for X
handoff                              compact briefing before clearing a session
change how you work with me          reconfigure without redoing setup
```

---

## 10. The three habits that decide whether this works

**Feed it.** A vault only knows what you put in it. Ten minutes of ingest a week beats a perfect system with nothing in it.

**Make it write things down.** When a conversation settles something, say so. Decisions, changed goals, new context about a person: if it only exists in the chat, it's gone when the session closes.

**Maintain it.** A lint pass every month, and a look at outcomes against decisions every quarter. Fifteen minutes each. That's the difference between a system that compounds and a folder that rots.
