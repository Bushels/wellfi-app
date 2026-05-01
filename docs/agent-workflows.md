# Agent Workflows

**Purpose:** one concise catalog of the repo workflows that future Codex, Claude, or Gemini sessions should use.

## Project Entrypoints

- **Codex/OpenAI:** start with `AGENTS.md`, then prefer the matching `.claude/skills/<name>/agents/openai.yaml` wrapper when one exists.
- **Claude:** start with `CLAUDE.md`, then use this file to find the right `.claude/skills/<name>/SKILL.md`.

Treat this file as the discovery index. Treat each `SKILL.md` as the portable runbook.

## Cross-Model Rule

- Keep `AGENTS.md` and `CLAUDE.md` aligned when workflow discovery changes.
- `agents/openai.yaml` is Codex/OpenAI discovery metadata only.
- `SKILL.md` must stay readable without Codex-only assumptions so Claude can use it directly.

## Current Recommended Workflows

### `docs-maintainer`

Use when a change is complete and the repo docs need to reflect reality.

Responsibilities:

- update current-source docs
- sync `AGENTS.md`, `CLAUDE.md`, and `docs/current-state.md`
- update any affected workflow docs
- update this workflow index when discovery changes
- delete stale plan docs or obsolete architecture notes
- call `documentation-patrol` logic before finishing

Files:

- `.claude/skills/docs-maintainer/SKILL.md`
- `.claude/skills/docs-maintainer/agents/openai.yaml`

### `documentation-patrol`

Use when you want a documentation drift audit without necessarily rewriting docs.

Responsibilities:

- stale-reference scan
- workflow command scan
- architecture drift detection

Files:

- `.claude/skills/documentation-patrol/SKILL.md`
- `.claude/skills/documentation-patrol/agents/openai.yaml`

### `monthly-production-refresh`

Use for the monthly Clearwater / Bluesky CSV workflow.

Responsibilities:

- validate required columns
- rebuild production overlays
- insert new provisioned-operator wells
- sync production state into Supabase for provisioned operators
- backfill missing well names when the source file includes them
- verify snapshot month, production fields, and install-linked cohort safety
- report skipped not-yet-onboarded operators

Files:

- `.claude/skills/monthly-production-refresh/SKILL.md`
- `.claude/skills/monthly-production-refresh/agents/openai.yaml`

### `operator-onboarding`

Use to provision one operator and prepare/import its wells.

Files:

- `.claude/skills/operator-onboarding/SKILL.md`
- `.claude/skills/operator-onboarding/agents/openai.yaml`

### `well-trajectory-visualization`

Use for directional survey CSV ingestion, well trajectory plates, survey-vs-projection handling, minimum-curvature anchor placement, or standalone well-path exports.

Files:

- `.claude/skills/well-trajectory-visualization/SKILL.md`
- `.claude/skills/well-trajectory-visualization/agents/openai.yaml`

### `operator-smoke-test`

Use to verify one provisioned operator login after onboarding or release work.

Files:

- `.claude/skills/operator-smoke-test/SKILL.md`
- `.claude/skills/operator-smoke-test/agents/openai.yaml`

### `wellfi-supabase-rollout`

Use for schema, RLS, and tenant rollout work in Supabase.

Files:

- `.claude/skills/wellfi-supabase-rollout/SKILL.md`
- `.claude/skills/wellfi-supabase-rollout/agents/openai.yaml`

## Current Source Of Truth

When these disagree, prefer this order:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/current-state.md`
4. workflow `SKILL.md` files
5. older historical `agents/` session artifacts
