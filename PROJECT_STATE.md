# Project State — wellfi-app

**Last verified commit:** `21fe2451` (Phase 2 E4 path-fix + force-push to main; Vercel deployed)
**Last updated:** 2026-05-06
**Production URL:** https://wellfi-app-kyles-projects-d3ab6818.vercel.app

## Active task

Phase 3 standardization — adding `PROJECT_STATE.md` + `docs/journal/` to complete the standard MPS portfolio layout. Most of the layout (`AGENTS.md`, `CLAUDE.md`, `.claude/skills/`, `.codex/config.toml`) already exists from earlier work; this commit fills the remaining gaps.

## Known blockers

None.

## Current state

- Multi-operator Clearwater / Bluesky portal — 15 provisioned operator tenants
- Production deploy: ✓ Ready, 51s build, all env vars set (VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, VITE_MAPBOX_TOKEN)
- 3D Wellbore Navigator (Three.js + @react-three/fiber/drei, pinned versions): live on production
- Diagnostic logging tagged `[WellFi/3D]` for browser DevTools
- Vercel auto-detects Vite from package.json at repo root (vercel.json no longer needed post-extraction)

## Backup safety

- Tag `pre-restructure-c822306` exists on origin (rollback marker before Phase 2 extraction)
- Branch `backup/pre-restructure-main` on origin (rollback path: `git push --force-with-lease origin backup/pre-restructure-main:main`)

## Pending follow-ups

1. **Untracked Blender scripts** in `scripts/` from the well-trajectory-visualization workflow — already committed (efe8661). No action needed.
2. **Local working tree** has petro-roundtable + Data references in some doc plans — those refs are now cross-repo. Active docs already fixed; archive plans intentionally left.
3. **Untracked operator data** (was in old Obsidian/Data/) lives in sibling `operator-data` repo — if any production code path references `Data/...` it needs updating to `../operator-data/...` or a runtime config. Need to grep src/ to verify.

## Next action

After Phase 3 commit lands:
1. Grep `src/` for any remaining `Data/` path literals that might be hardcoded data references — fix to point at sibling operator-data or move to runtime config.
2. Verify a fresh clone of wellfi-app builds and deploys cleanly (regression check).
3. Decide on the WellFi/ marketing folder fate (sibling MPS/WellFi/) — absorb into wellfi-app/marketing/ or keep separate.

## How to update this file

Update **Last verified commit** every meaningful commit (`git log -1 --format='%H' | cut -c1-8`).
Update **Active task** when starting new work.
Update **Known blockers** when something prevents progress.
Update **Next action** at session end.

History of what was done lives in `docs/journal/YYYY-MM.md`.
