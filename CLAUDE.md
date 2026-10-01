@AGENTS.md

## Claude Code

The operating model is in `AGENTS.md`, imported above. This file adds only what is specific to this runtime.

**If `wiki/identity.md` does not exist, the FIRST RUN section at the top of `AGENTS.md` applies. Read `SETUP.md` and run the interview before doing anything else**: including before answering whatever the user opened with.

- **The procedures in the Operations table are installed as skills** in `.claude/skills/` and load automatically when a prompt matches their description. Do not read them by hand.
- **Use plan mode** for schema changes and multi-file mutations, per the dry-run rule.
- **Scripts live in `.claude/scripts/`** and are run with `python`. They exist so you don't have to read a file to change one line of it: check there before opening a large page.
- Anything you learn about how this user wants to be worked with goes in `wiki/identity.md`, not in a runtime-local memory store. Machine-local memory is invisible to every other runtime, to a second machine, and to the git history: it is a staging area, never a second constitution.
