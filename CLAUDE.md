# WellFi App - Claude Project Guide

## Project Summary

WellFi is now a **multi-operator Clearwater / Bluesky portal**, not an Obsidian-only app.

Current implementation state:

- Supabase tenancy and operator-scoped RLS are active
- base well dots come from live Supabase well data
- production overlay comes from monthly CSV-derived overlay GeoJSON: heatmap at basin scale, then formation/fluid production dots at close zoom using the same colors as the heatmap for easier visual handoff
- the current rollout boundary is **15 provisioned operator tenants**
- unprovisioned operators are reported and skipped during monthly syncs

## Read These First

1. `AGENTS.md`
2. `docs/current-state.md`
3. `docs/agent-workflows.md`
4. the relevant workflow `.claude/skills/*/SKILL.md`

## Workflow Discovery

Skills now live under `.claude/skills/` (auto-discovered by Claude Code's Skill tool when launched from this project).

Runbooks for documentation or workflow-oriented tasks:

- `.claude/skills/docs-maintainer/SKILL.md`
- `.claude/skills/documentation-patrol/SKILL.md`
- `.claude/skills/monthly-production-refresh/SKILL.md`
- `.claude/skills/operator-onboarding/SKILL.md`
- `.claude/skills/operator-smoke-test/SKILL.md`
- `.claude/skills/well-trajectory-visualization/SKILL.md`
- `.claude/skills/wellfi-supabase-rollout/SKILL.md`

## Related Projects

- `petro-roundtable/` — Petroleum engineering roundtable (AI specialist agents, formation knowledge bases, calculation scripts). See `petro-roundtable/CLAUDE.md` for details. Lives on `petro-roundtable/*` branches, NOT `codex/*` branches.

**Note:** The agents in `wellfi-app/agents/` are development agents that help BUILD this app (Sessions 1-8). They are completely unrelated to the petroleum engineering specialist agents in `petro-roundtable/agents/`. Do not confuse the two systems.

## Important Rules

- Treat `docs/current-state.md` as the concise implementation status summary.
- Treat `docs/agent-workflows.md` as the vendor-neutral workflow index.
- Treat each `SKILL.md` as the real workflow runbook.
- Do not rely on historical `agents/session-*` files for current architecture decisions.
- Delete stale implementation plans if they no longer reflect the live system.
- Keep docs aligned with the actual rollout boundary, not the future desired rollout.
