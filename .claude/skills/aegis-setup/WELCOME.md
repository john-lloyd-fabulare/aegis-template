# Welcome message templates

**Not read at session start. Not prose to follow.** These are the two blocks `welcome.py` fills in and prints after setup. Edit the wording here freely; the script only substitutes `{placeholders}` and never rewrites this file.

Placeholders available: `{name}` `{assistant}` `{clients}` `{blanks}` `{bluntness}` `{coaching}`

---

## BLOCK: short

Printed by `python .claude/scripts/welcome.py`. This is the default close. Paste it, then stop and wait.

```
You're set up, {name}. I'm {assistant}, and everything I learn from here lives in
files on your disk that you own outright.

Three things cover most of what we'll do:

  Remember something    Drop a file in input/ and say "ingest this"
  Recall something      Ask me in plain language. I'll cite the pages I used,
                        or tell you the vault doesn't have it
  Stop mid-task         Say "save the state" and the next session picks up
                        from where we stopped, not from scratch

Best next step: put one real file in input/ and let's file it together. A
transcript, a long email thread, a PDF you keep reopening. Until pages exist
there's nothing for me to answer from, and one pass through the loop teaches
more than any amount of me describing it.

{blanks}

Want the two-minute tour of how this actually works, or shall we just start?
```

---

## BLOCK: tour

Printed by `python .claude/scripts/welcome.py --tour`. **Only if they say yes to the offer.** Paste it, then stop. Do not continue into folder taxonomy, frontmatter, hubs, work items or the scripts.

```
The two-minute version.

1. WHAT IT IS
   A filing cabinet plus an assistant that reads it. Plain Markdown on your
   disk. No database, nothing to log into, nothing anyone can take away.

2. HOW THINGS GET IN
   You drop a file in input/ and say "ingest this". It becomes a permanent
   copy in raw/ that never gets edited again, plus pages in wiki/ that link
   to each other. The pages are what answers questions later, not the
   original file.

3. HOW THINGS COME OUT
   You ask in plain language. Answers come with citations to the pages I
   used. "The vault doesn't record this" is a real answer, and you should
   expect to hear it sometimes. That's the system working, not failing.

4. WHY IT STAYS FAST AS IT FILLS UP
   I read one small file at the start of every session and look up
   everything else on demand. That's the reason this doesn't get slower as
   it grows, and it's the one rule not worth breaking.

5. WHAT I'LL REFUSE TO DO
   Write anything published under someone else's name without their voice
   guide. State a fact I can't trace to a file. Tell you something's done
   without checking. If I ever do one of those, that's a bug and it's worth
   telling me.

6. WHAT I'LL NEVER DO
   Anything while you're away. Nothing runs on a schedule, nothing watches
   your inbox. I only know what you put in front of me.

Everything else is in GUIDE.md, and it's worth ten minutes once you've
ingested your first file.
```

---

## BLOCK: blanks

Used inside the short block when `identity.md` has unanswered fields. Omitted entirely when nothing is blank.

```
Still blank from setup: {blanks_list}. Tell me any of them whenever you like
and I'll fill them in. No need to edit files by hand.
```
