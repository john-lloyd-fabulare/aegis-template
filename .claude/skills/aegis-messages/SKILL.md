---
name: aegis-messages
description: >
  Voice gate for any message AEGIS drafts for a person to send under their own name: email,
  DM, WhatsApp, Slack, LinkedIn message, text, reply or follow-up. Use whenever the owner asks to
  draft, write, rewrite or reply to a message as the vault owner or as anyone else in the voice
  registry below, including personal admin (cancellations, complaints, requests).
  Not for published content such as posts, newsletters or campaign copy: that is aegis-content.
---

# AEGIS Messages

A message goes to one person or a small group, under someone's own name. It is not published content. **Published posts, captions, newsletters and campaign copy use `aegis-content`.** Everything a person sends as themselves uses this skill.

## 1. Pick the voice

Find the sender in the registry. Read their voice page in full, every time, before drafting a word.

| Sender | Voice page | Signs as |
|---|---|---|
| **The owner** (named in `wiki/identity.md`) | `wiki/concepts/<Owner> Message Voice.md` | Their usual sign-off |

*Add one row per person you draft messages for. The table starts with the owner only.*

**Sender not in the registry:** do not improvise a voice. Derive one from that person's own sent messages (ask the owner for them), file it as `wiki/concepts/<Name> Message Voice.md`, add a row to the table above, and tell the owner. Ask the owner to confirm it before the first message ships.

**Registry change rule:** when a voice page is added, renamed or superseded, update this table in the same edit.

## 2. Read the real thread

Before drafting, look for the sender's past messages **to this recipient** (Gmail exports, ingested threads, `wiki/communications/`). Match their greeting, length, warmth and sign-off. Real messages outrank the voice guide on register for personal messages. If none exist, say so in the reply.

## 3. Facts and recipients

- **No invented facts, policies, offers or positions.** Every claim about the sender, the recipient or their organization traces to a vault file, an export the owner supplied, or a cited web source. Missing: leave it out or ask the owner.
- **Check the recipient's role** before choosing who to write to. A role or title comes from a source (staff page, signature, LinkedIn), cited in the draft notes. Never guess an email address: if the address is not in a source, say so.
- **Unverified details in the message** (dates, amounts, "this spring") are named in the reply as things to confirm.

## 4. Deliver

1. Save the draft to `wiki/content-drafts/<Sender or Client>/` with frontmatter: `type: content-draft`, `client:`, `status: draft`, `voice:` (the page used) and `parent:` when a work item exists. Put the sources and open questions above the draft, and next actions under `## Tasks`.
2. Run the dash check on the file: `python -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();assert chr(8212) not in t and chr(8211) not in t" FILE` must pass.
3. Show the **full text in chat** (From, To, CC, Subject, body) as a `>` quote block, ready to copy.
4. AEGIS never sends. The owner sends, or the sender does.

## Before delivering

- [ ] Voice page read in full this session
- [ ] Sender's past messages to this recipient checked, or their absence stated
- [ ] Recipient role and address from a source, or flagged
- [ ] No invented fact, policy or offer
- [ ] No em or en dashes (search, not read)
- [ ] Saved in the vault and shown in full in chat
