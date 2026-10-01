---
name: aegis-content
description: >
  Mandatory voice gate for any content written for a client or on someone else's behalf: 
  posts, captions, newsletters, campaign copy, scripts, calendars, landing-page text. Use
  whenever a request names a client or account listed in wiki/identity.md and asks to write,
  draft, rewrite, or schedule anything published under their name. Loads the voice guide
  before drafting a word.
---

**Before writing anything, and before asking the principal anything, read the voice guide for that client, in full, every time. Silently, without offering to.** If a guide exists, do not ask whether you should read it.

**If the client has no voice guide, build it before drafting a word, but do not stall on it.** In order:

1. **Ask the principal for samples**: three to five pieces that sound right, one that sounds wrong. The wrong one is usually more informative than the right ones.
2. **If they don't have samples to hand, or tell you to proceed, derive the guide from the client's own published material** (site copy, published bios, recorded talks) and say plainly that it was derived rather than confirmed.
3. **File it as `wiki/concepts/Voice Guide — <Client>.md`**, register it in the table below, and tell the principal it now exists and on what basis.

**Never write client-facing copy off improvised voice.** A voice set by accident gets defended for a year.

⚠️ **A standing instruction from the principal overrides a client's own house style**, including the client's own published usage. Record the conflict in the guide rather than silently resolving it either way.

## Which guide

Voice guides live in `wiki/concepts/` as `Voice Guide — <Client>.md`. `wiki/identity.md` lists every client the vault writes for and whether their guide exists yet.

| For | Read |
|---|---|
| A client organisation | `Voice Guide — <Client>` |
| A person, in their personal channels | `Voice Guide — <Person> (Social)` |
| A person, in formal or campaign copy | `Voice Guide (<Person> (Formal)`) a different document, deliberately |
| The principal themselves | `Voice Guide — <Principal>`, never a client guide |

**A guide missing from this table means it has not been built.** Build it by the three steps at the top of this file, then write the content.

## Output rules

- **Follow the guide's exact output format.** If the guide is followed correctly there is **one** correct output: produce that single package, **not a menu of options**.
- **Hard character limits are verified programmatically, never estimated.** Count them in code and show the count.
- **Real links only.** Never a `[Link]` placeholder. If you do not have the URL, retrieve it or ask.
- **Formatting conventions (hashtags, emoji, casing, sign-offs) come from the guide**, not from general practice.
- **File the draft** to `wiki/content-drafts/<Client>/` with a dated filename, **before it is shown to the principal**. No index pages inside that folder; drafts are found by folder and linked from the client's project page.
- **Built files (`.docx`, `.pdf`, images) go to `wiki/content-drafts/<Client>/assets/`, together with the script that generated them.** The markdown is the source of truth and the binary is a build artifact; keeping both means an edit never has to start over. **A deliverable left in a session scratch directory is not filed**: that location is machine-local, outside version control, and temporary.
- **Frontmatter carries** `client:`, `status:`, `parent:` (the work item) and `voice:` (the guide used).

## When a deliverable recurs, give it its own procedure

A weekly or monthly package earns a dedicated skill. The pattern that works:

1. **Named inputs, asked for upfront**: the source document, the period, the optional secondary feeds.
2. **A pre-verified links table, consulted before any fetch.** Known-dead URLs listed with their approved substitute, so the same broken link is never rediscovered.
3. **Strict extraction rules**: an explicit include list *and* an explicit skip list for the repetitive or evergreen sections.
4. **Programmatic verification** of anything checkable: dates, days of the week, character counts.
5. **Crossover flags** where one client's material serves another.
6. **A fixed output path and filename pattern**, so the deliverable is findable without an index.
