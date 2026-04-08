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
- Originally on `codex/bluesky-clearwater-import`, now merged to `petro-roundtable/main`

**Phase 2: Obsidian Energy Operator Mastery — COMPLETE**
- 10/10 validation questions passed with data citations
- Gemini 3.1 Pro audit completed — 0 critical gaps (5 suggestions were Phase 5 data system scope)
- Knowledge base: 13 sections, 649 lines, all data verified against 3 corporate PDFs + CSV analysis
- KB hardening: added no-frac clarification and PCP lift details per Gemini review

**Phase 3: Engineering Panel Activation — COMPLETE**
- 8 specialist agents built (reservoir, drilling, well-performance, geomechanics, facilities, economics, simulation, production-data)
- All agents follow geoscientist.md template pattern (frontmatter + identity + domain + operational context + response protocol + Gemini triggers + data + calculations + 5 validation questions)
- Consistency review: all pass (1 fix applied to geoscientist.md — added `gemini_review: true`)
- Gemini 3.1 Pro panel audit: 0 critical gaps. Noted regulatory integration for Phase 4 Lead Engineer.
- ask-engineer skill updated with all 9 active specialists + production-data
- 2 design-doc calculation scripts still missing: `esp_design.py`, `wellbore_hydraulics.py`
- 18 additional calculation gaps flagged across 8 agents (see CONFIG.md)
- Knowledge loading: all load bluesky-formation.md + ROUNDTABLE.md; 6 of 8 also load obsidian-energy.md (geomechanics and simulation exempt — pure physics agents)

**Next: Phase 4 — Roundtable Orchestration**

## Directory Structure

```
petro-roundtable/
  CLAUDE.md              ← You are here
  ROUNDTABLE.md          ← Master identity (all agents load this)
  CONFIG.md              ← Model config, agent roster, phase status
  agents/                ← Agent definitions (.md files)
    geoscientist.md      ← Phase 1: Bluesky Formation specialist
    reservoir-engineer.md ← Phase 3: Recovery, decline, waterflood, EOR
    drilling-engineer.md  ← Phase 3: Well design, directional, casing
    well-performance.md   ← Phase 3: Completions, sand control, PCP lift
    geomechanics.md       ← Phase 3: Rock mechanics, stability, cap rock
    facilities-engineer.md ← Phase 3: Surface facilities, separation, water
    economics-reserves.md ← Phase 3: COGEH, pricing, break-even, NPV
    simulation-engineer.md ← Phase 3: CMG STARS, thermal, foamy oil
    production-data.md    ← Phase 3: SCADA, analytics, dashboards
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
- **Gemini strength:** Review, challenge, gap identification ("What are we missing?")
- **Gemini weakness:** Code generation with specific data — it ignores provided numbers and generates from training. Never trust Gemini-generated scripts without verifying every data point.

## Engineering Gotchas (Learned from Sessions)

- **WellFi is wireless EM telemetry** — There is no cable. The sonde is clamped to the tubing and transmits wirelessly. When clamps slide, the sonde shifts position and the signal grounds out. Never say "cable short" — say "signal loss" or "sonde shifted."
- **WellFi event log pressure is in BAR** — Always convert to kPa (×100) for engineering use. Temperature is in °C.
- **WellFi activation threshold varies per tool** — Check the deployment config for each tool. The first deployment used 50 kPa.
- **Tubing ≠ casing depths** — Downhole tools on tubing sit INSIDE casing, not at the casing shoe. Always ask: "Is this on tubing or casing?" before placing a tool depth.
- **Joint length is 9.456m for OBE HVS 16-18** — Do not assume 9.14m (30ft generic). Always verify from the Downhole Well Profile PDF.
- **Check LAS logs before offset extrapolation** — If Build/geosteering LAS files exist for a well, use the gamma ray to pick formation tops directly. Don't extrapolate from offset wells when you have the actual log.
- **Structural extrapolation uncertainty** — Bluesky structure varies 30+ meters across one township. Never present a formation boundary with false confidence from offsets alone.
- **Gemini fails at data-driven generation** — Gemini discards provided data and generates from training. Use Gemini for review/challenge ONLY, never for code that must use specific numbers.
- **Sales oil ≠ downhole oil** — Lab oil analysis labeled "Sales Oil" has been treated/heated. Viscosity will be lower than in-situ reservoir conditions.

## Visualization

Use the `engineering-visual` skill for well schematics, deployment diagrams, and subsurface cross-sections. Design philosophy: "Subterranean Signal" — dark theme, dual-purpose for marketing + engineering audiences. Key rules:
- Every number on the canvas must be verifiable against a source file
- If formation boundary is uncertain, don't show it — note the uncertainty
- Cyan=data, Amber=tools, Green=geology, Red=alerts
- Use the `remotion-data-video` skill for animated data stories (Remotion → MP4 video)
- Remotion `npx create-video` has interactive prompts that fail in Claude Code — scaffold manually
- For animated callouts, use temporal separation (appear/disappear per act), not spatial stacking

## Mastery Sequence (7 Phases)

1. **Bluesky Formation Mastery** — COMPLETE
2. **Obsidian Energy Operator Mastery** — COMPLETE
3. **Engineering Panel** (9 specialists + 1 operator rep) — COMPLETE
4. Roundtable Orchestration (Lead Engineer + /roundtable skill) — NEXT
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
