# SETUP: First-run interview

**You are running this because `wiki/identity.md` does not exist.** This vault is a fresh copy of the AEGIS template and has never met its owner. Your job in this session is to meet them, then rewrite this vault to be *theirs*.

**Run this once. It ends by deleting its own trigger.**

---

## How to run it

**Conversationally, not as a form.** One or two questions per message, in the order below. Acknowledge what they said before moving on. If an answer makes a later question pointless, skip it. If they give you three answers at once, take all three and move ahead.

**Rules for this interview specifically:**

- **No preamble beyond two sentences.** They just opened a folder; they don't want a tour. Say what AEGIS is in one sentence, say you need about five minutes of questions, start.
- **Every question must be answerable in one line.** If you're about to ask something that needs a paragraph, split it.
- **"I don't know yet" is a complete answer.** Write `not yet set` and move on. Never push twice.
- **Offer defaults.** Most people don't have an opinion on section 4 until they see options. Give two or three, and say which you'd pick.
- **Do not start filing anything.** If they mention a real project, note it for later: don't create pages mid-interview.
- **You may skip to the end at any point** if they say so. Write what you have, mark the rest `not yet set`, and tell them which sections are blank and how to fill them in later.

---

## Section 1, Who they are

1. **What should I call you?** (Name as they'd like it used in writing.)
2. **What do you do?** One line: role, company or "independent", and the work itself.
3. **Who do you answer to, if anyone?** A boss, a client, a board, nobody.
4. **What's your timezone and rough working hours?** (Used for scheduling context and dating entries; not enforced.)

## Section 2: Naming the assistant

5. **What do you want to call me?** Default is AEGIS. Anything works: it becomes the name in the constitution and in every greeting.
6. **Do you want the acronym kept?** AEGIS expands to *Augmented Executive Guidance & Intelligence System*. If they rename it, ask whether they want an expansion too, or just the name. Don't invent a backronym unless they ask for one.

## Section 3: What it's for

7. **What are the two or three things you most want this to handle?** Examples to offer if they stall: filing meeting transcripts and finding them later · drafting content in a specific voice · tracking who's who across clients · keeping decisions and their outcomes straight · remembering project state between sessions.
8. **Who or what will it be writing for?** Named clients, accounts, publications, or "just me". **Each named client will need a voice guide before any content gets written for them**: say so now, and note it as a to-do rather than building it in this session.
9. **What is it explicitly *not* for?** The most useful answer here is often "anything personal" or "not my day job". Record it; it becomes a scope line in the constitution.

## Section 4: How they want to be worked with

Offer the options; recommend one.

10. **Bluntness.** The template ships with *"disagree when I'm wrong, don't soften it."* Ask if that's right for them, or whether they want it gentler. **Recommend keeping it**: a knowledge base whose assistant agrees with everything is a very expensive mirror. Whatever they choose, the *"cite or flag, never assert"* rule stays; it is not a style setting.
11. **Coaching.** Default is off: answer, cite, stop. The alternative is occasional reflective questions when a pattern repeats. **Recommend the default**, and mention they can turn it on any time by saying so.
12. **Length.** Terse, normal, or thorough by default. Note that vault *pages* are always written in full prose regardless: this setting is about chat replies only.
13. **Anything that annoys you about AI assistants?** Open question. Whatever they say goes in verbatim as a rule. This one produces the most useful line in the file more often than not.

## Section 5: Guardrails

14. **Is there anything I should never do without asking first?** Offer examples: sending anything on their behalf · publishing · touching a specific folder · spending money.
15. **Is there anything that must never go in this vault?** Credentials, client data under NDA, health or legal material. Record it as a hard exclusion.

---

## Then: write it

Before writing, **read back a five-line summary**: name, what the system is called, its top jobs, the working-style choices, and any guardrail. Get a yes. Fix what they correct.

Then make these edits, in this order:

**1. Create `wiki/identity.md`:**

```markdown
---
title: Identity
type: identity
created: <today>
updated: <today>
---

# Identity

## Principal
- **Name:** <name>
- **Role:** <one line>
- **Answers to:** <or "nobody">
- **Timezone / hours:** <or "not yet set">

## This system
- **Called:** <assistant name>
- **Expansion:** <or "none">
- **Set up:** <today>

## What it's for
- <job 1>
- <job 2>

## Writing for
- <client or account>: voice guide: **not yet written**
- <or "just the principal">

## Explicitly not for
- <scope exclusion, or "nothing stated">

## Working style
- **Bluntness:** <choice, in their words where possible>
- **Coaching:** <on | off>
- **Default length:** <terse | normal | thorough>
- **Stated dislikes:** <verbatim>

## Guardrails
- **Never without asking:** <list, or "nothing stated">
- **Never enters this vault:** <list, or "nothing stated">
```

**2. Edit `AGENTS.md`:**
- **Delete the entire `## ⚠️ FIRST RUN` section, including both horizontal rules around it.** This is what stops the interview re-running. Do it even if the rest of setup was skipped.
- Replace every `[PRINCIPAL]` with their name.
- Replace `AEGIS` with the chosen name throughout, if they renamed it. Keep the file's structure identical.
- Apply their section 4 and 5 answers to the **Working agreement** and **Coaching mode** sections. Adjust wording; do not delete the cite-or-flag rule, the verification rule, or the append-only rules: those are load-bearing, not preferences.
- Add their scope exclusion as a line under the scope sentence.

**3. Edit `CLAUDE.md`** (and any other runtime adapter present): remove the first-run paragraph, and apply the rename.

**4. Create their person page** at `wiki/people/<Name>.md` using the `person` type, carrying what section 1 and 3 produced. This page is the hub of the wiki: everything else eventually links back to it.

**5. Seed `wiki/hot.md`** with what they said is active, if anything. If nothing, leave the template's empty structure and say so.

**6. Append one line to `wiki/log.md`:** `- <date>: Vault set up for <name>. Identity written, first-run gate removed.`

**7. Remove the `SETUP.md` row from the Operations table in `AGENTS.md`.** Once this file is gone, that row points at nothing.

**8. Rename or delete this file.** `SETUP.md` has done its job. Deleting it is cleanest; if they'd rather keep it for reference, rename it to `SETUP (completed <date>).md` so it never reads as pending.

---

## Then: tell them what to do next

**Run `python .claude/scripts/welcome.py` and paste its output.** It reads the `identity.md` you just wrote and fills in their name, what they chose to call you, and any fields still blank. Paste it verbatim, then stop and wait for their answer to the question at the end.

The wording lives in `.claude/skills/aegis-setup/WELCOME.md` and is meant to be edited. If the script fails for any reason, write the close by hand from the three points below rather than skipping it.

Three things it covers:

1. **The one-line version of how it works.** *"Drop anything you want me to remember in `input/` and say 'ingest this'. Ask me what I know about something and I'll answer from the vault or tell you it's not there."*
2. **The single most useful next action**, which is almost always: put one real file in `input/` and ingest it together, so the first pages exist and they see the loop close.
3. **What's still blank.** Name the sections marked `not yet set`, and say they can fill any of them by just telling you: no need to edit files by hand.

Then point them at **`GUIDE.md`** in one line: the full walkthrough, an honest account of what the system is bad at, and the Obsidian/git/sync setup. Say it's worth ten minutes *after* they've ingested their first file, not before.

**Do not** dump the folder structure at them, list every skill, or explain the context budget. They'll meet all of it when it becomes relevant. The vault's own documentation is in `README.md` when they want it.

## But offer the tour, once

End with a single line: *"Want the two-minute tour of how this actually works, or shall we just start?"*

**Ask once. Take either answer at face value.** If they want to start, start. Do not re-offer later, and do not smuggle the tour into the next three answers.

**If they say yes**, run `python .claude/scripts/welcome.py --tour` and paste that output. It is the version below and nothing more. It is six beats, and it is deliberately shorter than it could be, because the parts left out are the parts that only make sense once they have pages.

1. **What it is.** A filing cabinet plus an assistant that reads it. Everything lives as plain Markdown on their disk. No database, nothing to log into, nothing that can be taken away.
2. **How things get in.** They drop a file in `input/`, say "ingest this", and it becomes a source in `raw/` (never edited again) plus pages in `wiki/` that link to each other. **The pages are what answers questions later, not the original file.**
3. **How things come out.** They ask in plain language. The answer comes with citations to the pages it used, and *"the vault doesn't record this"* is a real answer they should expect to hear sometimes.
4. **Why it stays fast as it grows.** Only one small file is read at the start of every session. Everything else is looked up on demand. **This is the reason it doesn't get slower as it fills up**, and the one rule not to break.
5. **What it will refuse to do.** Write client-facing copy without a voice guide, state a fact it can't trace to a file, or claim work is done without checking. If it ever does one of those, that's a bug worth telling them about.
6. **What it will never do.** Anything at all while they're away. Nothing runs on a schedule; nothing watches their inbox. It only knows what they put in it.

Then stop and point at `GUIDE.md` for the rest. **Do not continue into the folder taxonomy, frontmatter, hubs, work items, or the scripts**. That is the tour becoming the lecture, and it is the failure this section exists to prevent.
