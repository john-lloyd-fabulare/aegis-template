---
name: aegis-query
description: >
  Answer a question from the vault at the shallowest reliable depth. Use when asked what the
  vault knows about a topic, a client, a person, a project or a past decision: "what do we
  know about X", "what did we decide", "who is X", "what's the status of X", "have we covered
  X", "remind me". Also use for provenance questions like "do we have the full resource" or
  "where did that come from".
---

**Retrieve by decision, not by habit.** Stop at the shallowest layer that answers reliably; descend only for a factual claim, an exact quote, a conflict, a high-stakes decision, or a missing detail.

## Read order

1. **`hot.md`**: only if the question touches active work.
2. **`priorities.md`**: only if it touches goals, income, or a trade-off.
3. **The matching Topic Hub's `## Synthesis`** if the question is topic-shaped. **This is usually the whole answer.**
4. **The `Source Details` companion file**, when the synthesis is not enough.
5. **The `wiki/sources/` page**: for one source's full treatment, its claims and provenance.
6. **`raw/`**: only for an exact quote, a disputed claim, or when the interpretation is in question.

`index.md` is a **catalogue for locating a page**, not a document to read through. Use `find` and `grep` first.

## Skip the vault entirely

Generic knowledge questions unconnected to the principal or a tracked client · pure technical questions · anything already answerable from the conversation.

## Answering

- **Cite what you drew from**, as `[[wikilinks]]`.
- **Never state an unverified claim as fact.** Every claim, number, quote or date traces to a vault file or a live check, not to recall. If it cannot be traced, **mark it unverified**.
- **Flag your own inferences** by saying so: *"my read on this is …"*. Plain synthesis of two stated facts doesn't need it; genuine speculation does.
- **Say when you don't know.** A stub, a gap, or "the vault doesn't record this" is a real answer.
- **Never silently overwrite a contradicted claim.** Note it: *"as of the 2026-08-30 update, X; the earlier note below may be stale"*, and flag it.

## Provenance questions

*"Do we have the complete resource?"* is a different question from *"what does it say?"* Answer it by checking the file, not by recalling the page:

- Does the `raw/` file exist, and is there exactly one copy?
- Does its wiki page cite it with the `.md` extension?
- Is the raw file the full source or an excerpt?
- Are there sibling files from the same batch that were never ingested?

Byte-identical copies of one recording can sit in `raw/` under several names for weeks while the distinct sources those names promised were never captured. The filenames look like coverage. **Check the disk.**

## Afterwards

If the answer is a real synthesis worth keeping, **offer to file it to `wiki/answers/`.** If the question exposed a gap or a defect, record it: business gaps on the relevant project page, vault defects in `health.md`.
