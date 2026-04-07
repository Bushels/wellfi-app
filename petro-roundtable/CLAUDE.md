# Petro-Roundtable — Claude Project Guide

## What This Is

A Claude Code native petroleum engineering roundtable — a panel of AI specialist agents with deep formation knowledge, operator intelligence, and multi-model hardening (Gemini 3.1 peer review). Replaces the external Hermes/GPT-5.4 system (`hermes-petro-agents/` + `roundtable-bridge/`).

## Read These First

1. `ROUNDTABLE.md` — Master identity and operating principles (loaded by all agents)
2. `CONFIG.md` — Model assignments, agent roster, mastery sequence, phase status
3. `docs/plans/2026-04-07-petro-roundtable-design.md` — Full design document (approved)

## Current Phase

**Phase 1: Bluesky Formation Mastery — COMPLETE**
- All 10 validation questions passed with data citations
- Gemini 3.1 Pro audit completed — 3 gaps incorporated
- Committed: `546a395` on `codex/bluesky-clearwater-import`

**Phase 2: Obsidian Energy Operator Mastery — ACTIVE**
- Operator agent: `operators/obsidian-energy.md`
- Knowledge base: `knowledge/obsidian-energy.md` (13 sections, verified data)
- Skill: `/ask-operator` routes questions to operator representatives

## Directory Structure

```
petro-roundtable/
  CLAUDE.md              ← You are here
  ROUNDTABLE.md          ← Master identity (all agents load this)
  CONFIG.md              ← Model config, agent roster, phase status
  agents/                ← Agent definitions (.md files)
    geoscientist.md      ← Phase 1: Bluesky Formation specialist
  operators/             ← Operator representative agents (Phase 2+)
    obsidian-energy.md   ← Phase 2: Obsidian Energy operator rep
  knowledge/             ← Curated formation knowledge bases
    bluesky-formation.md ← 13-section Bluesky reference (verified)
    obsidian-energy.md   ← 13-section Obsidian Energy operator reference
  skills/                ← Skill definitions
    bluesky-briefing/    ← /bluesky-briefing — formation deep-dive
    ask-engineer/        ← /ask-engineer — route question to specialist
    ask-operator/        ← /ask-operator — route question to operator rep
  calculations/          ← Python CLI scripts (run via Bash)
    decline_curves.py    ← Arps decline fitting, EUR estimation
    nodal_analysis.py    ← Vogel/Darcy IPR, VLP, operating point
    sand_control.py      ← PSD analysis, screen selection, erosional velocity
  mcp/                   ← MCP server definitions (Phase 5: StackDX)
  docs/
    plans/               ← Design docs and implementation plans
```

## Data Files (External to This Directory)

Production and drilling data live in the parent repo's `Data/` directory:

| File | Contents |
|---|---|
| `Data/clearwater_bluesky_feb2026_prod_imperial.csv` | Monthly production (imperial) |
| `Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv` | Canonical format |
| `Data/clearwater_bluesky_2026_drilling_chart.csv` | 2026 drilling activity |
| `Data/clearwater_bluesky_2026_drilling_chart_full.csv` | Full drilling chart |
| `Data/clearwater_bluesky_company_summary.xlsx` | Operator summary |
| `Data/geological/Bluesky Geology.md` | Primary geological source (38 citations) |
| `Data/Obsidian/` | Obsidian Energy data |
| `Data/CNRL/` | CNRL data |
| `Data/Baytex/` | Baytex data |

## Models

| Model | ID | Role |
|---|---|---|
| Claude Opus 4.6 | `claude-opus-4-6` | Primary agent model (current) |
| Claude Mythos | `claude-mythos` | Primary agent model (future) |
| Gemini 3.1 Pro | `gemini-3.1-pro` | Deep peer review, knowledge audits |
| Gemini 3.1 Flash | `gemini-3.1-flash` | Quick sanity checks |

## Gemini Integration

Use `mcp__gemini-cli__ask-gemini` for peer review. Rules:
- Direct, specific questions — no preamble
- Gemini's claims are hypotheses — verify against data before accepting
- Claude makes the final decision — Gemini advises

## Mastery Sequence (7 Phases)

1. **Bluesky Formation Mastery** — COMPLETE
2. **Obsidian Energy Operator Mastery** — (current)
3. Engineering Panel (all 9 specialist agents)
4. Roundtable Orchestration (Lead Engineer + /roundtable skill)
5. StackDX MCP Server (well data queries)
6. Operator Expansion (CNRL, Baytex, Headwater)
7. Formation Expansion (Clearwater, McMurray)

Each phase must be perfected before advancing. Iterate: BUILD > TEST > IDENTIFY GAPS > FIX > RETEST > VALIDATE WITH GEMINI > SHIP.

## Important Rules

- **All paths in agent files and knowledge bases are relative to the repo root** (`C:\Users\kyle\MPS\Obsidian\`)
- **Never modify `ROUNDTABLE.md` without updating all agents** — they all load it
- **Knowledge base data points must be verified against source** — cite the section
- **Calculation scripts must accept CLI args and print text** — agents read stdout, not JSON
- **Update `CONFIG.md` phase status** when advancing phases
- **Update this file** when adding agents, skills, or knowledge bases

## Branch Strategy

- **This project:** `petro-roundtable/main` branch (and `petro-roundtable/phase-N` for active work)
- **WellFi app:** `codex/*` branches (separate git history)
- Do NOT mix petro-roundtable commits with wellfi-app feature branches

## Two Agent Systems — Do Not Confuse

This repo contains two completely unrelated agent systems:

| | Petro-Roundtable Agents (THIS PROJECT) | WellFi Development Agents |
|---|---|---|
| **Purpose** | Domain experts that ARE the product | Development agents that help BUILD the wellfi-app |
| **Location** | `petro-roundtable/agents/` | `wellfi-app/agents/session-{N}/` |
| **Examples** | Geoscientist, reservoir engineer | UI agent, data-integrity agent |
| **Invoked by** | Users via `/ask-engineer`, `/roundtable` | Claude Code during dev sessions |
| **Identity** | `ROUNDTABLE.md` | `wellfi-app/agents/COORDINATOR.md` |

These systems share no code, no identity, and no coordination. If you are working on petro-roundtable, ignore `wellfi-app/agents/` entirely.

## Related Projects

- `wellfi-app/` — WellFi multi-operator monitoring app (sibling project, same repo)
- `hermes-petro-agents/` — Legacy Hermes agent definitions (being replaced by this)
- `roundtable-bridge/` — Legacy FastAPI bridge server (being replaced by this)
