---
title: Health
type: health
updated: not yet set
---

# Health

Open defects in the vault's own machinery, not business problems. **~40-line cap.** Hitting the cap schedules a pass; it does not justify a bigger file.

**Read this before any lint pass.** Without it you will re-derive the same findings every time.

## Open

<!-- - [ ] <defect> (<how it was found>) <date> -->

## Examined and deliberately left alone

Things that look like defects but are not. This section is what stops a lint pass from
proposing the same rejected fix every month. Include the reason.

- **Orphan pages on a fresh vault.** A newly cloned template reports every scaffolding file as
  an orphan, because nothing links to anything yet. This is expected and resolves itself as
  real pages get written. It is not a defect until the vault has content and orphans persist.
