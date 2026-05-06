# Journal

Append-only history. Both Claude and Codex append entries here. Current-truth state lives in `../../PROJECT_STATE.md`; this directory is the record of *what was done, when, why*.

## Schema per entry

```markdown
## YYYY-MM-DD — Author (Model)
**Session:** id | **Branch:** branch | **Commit:** sha-or-uncommitted

### Intent
One sentence.

### Changes
- Bullet list of files / decisions / commits.

### Validation
- npm run build, manual smoke checks, Vercel preview, etc.

### Risks / Open
- Anything fragile, anything still pending.

### Next
- Handoff for the next session / LLM.
```

## File rotation

One file per month: `2026-05.md`, `2026-06.md`, etc. When an entry would push a monthly file beyond ~500 lines, start the next month's file early.

## Why journals here, not in AGENTS.md / CLAUDE.md

Per the design doc: AGENTS.md and CLAUDE.md are **rules-only**. Activity logs in those files become permanent standing instructions in Codex's instruction chain (per Codex's audit of the design doc). Journals keep the history visible without polluting every prompt.
