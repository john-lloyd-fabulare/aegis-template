---
title: Vault Failure Modes (Recurring Defects)
type: concept
tags: [meta, quality]
created: not yet set
updated: not yet set
---

# Vault Failure Modes (Recurring Defects)

**The catalogue of mistakes this vault has actually made, and how to catch each one.** Distinct from [[health]], which lists what is broken *right now*. This page lists defect *classes* that recur.

**Add an entry when a mistake is made a second time, or when a single mistake was bad enough that repeating it would be costly.** Each entry names the defect, why the existing rule failed to catch it, and the check that would.

**Read before a lint pass**, and when a piece of work feels finished but unverified.

---

## Work delivered but never filed

**The shape.** Something is produced for the principal (a document, a draft, an email, a script) handed over in conversation, and left in a session scratch directory. It never reaches the vault. It looks complete to everyone in the conversation.

**Why a "file your output" rule does not catch it on its own.** Delivering *feels* like finishing. The rule is read as a follow-up step rather than part of the deliverable, and rules that mention markdown pages leave **built binaries** (`.docx`, `.pdf`, images) with no stated home even when read carefully.

**Why it is costly.** A scratch directory is machine-local, outside version control, invisible to every other runtime, and impermanent. Work that lives only there is **lost at the end of the session and unfindable by any other model**, while appearing done.

**The check.** Before reporting a deliverable complete: *"if this session ended right now, would the vault contain it?"* See the scratchpad rule in `AGENTS.md` § Working agreement.

---

## Claiming a source corroborates itself

**The shape.** An automated artifact (a transcript, an export, an auto-summary) is checked against **another artifact produced by the same pipeline**, and the agreement is read as confirmation. Both carry the same error.

**Why it is costly.** It produces confident, wrong statements about things the principal will act on. Two outputs of one tool are one source wearing two hats.

**The check.** Corroboration only counts across **independent** pipelines. When attribution or accuracy is known to be unreliable, get a second independent capture (the original recording, a different tool's export) before writing anything load-bearing as fact, and ask the principal for it early, since they usually have it.

---

## Assuming content is safe somewhere it is not

**The shape.** Content is compressed, merged or deleted on the belief that a full copy exists elsewhere. The belief is not checked first.

**The check.** Verify the destination actually holds the content **before** removing the source. Verification is a precondition, not a follow-up.

---

## Stating a vault fact without opening the file

**The shape.** Counts, emptiness, gaps and "this page does not exist" asserted from memory or inference rather than a check. Also: trusting a checker that does not handle aliases, code fences, escaped pipes or non-markdown targets.

**The check.** Open the file. Then confirm the tool itself is sound before reporting a number.

---

## Redesigning the architecture when the problem was one expensive read

**The shape.** Session cost climbs. The response is a structural redesign (a router, a tiered loader, a classifier) built and trialled at real cost. The actual cause turns out to be **a single large file being read every session for no retrieval benefit.**

**Why it is costly.** The redesign is unpaid overhead that never runs, while the fix was a one-line deletion. Worse, the redesign then gets credited with the improvement the deletion produced, which makes the wrong lesson durable.

**The check.** Before redesigning retrieval, **measure what is actually being read at session start and what each read returns.** Delete the expensive read that earns nothing, then see whether a problem remains.

---

## An always-on obligation is dropped exactly when it matters

**The shape.** A rule fires after *every* task: log this, append that, update the tracker. It is honoured in quiet sessions and silently skipped in busy ones, **which is the inverse of when its data would be useful.**

**Why a written rule does not fix it.** Prose in a schema file is the weakest possible enforcement: it competes with the task in front of it and loses.

**The check.** Give a recurring obligation either **a mechanical trigger** (a hook, or a checklist item *inside* the skill that does the work) or **a bounded lifetime with a review date**. If it is neither, expect it to be skipped and do not build on its data.

## Related

- [[health]]: what is broken right now
- `AGENTS.md` § Working agreement
