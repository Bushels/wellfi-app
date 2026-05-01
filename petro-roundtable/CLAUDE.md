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

**Phase 3.75: Multiphase Flow Specialist — COMPLETE (2026-04-15)**
- 10th specialist agent: downhole multiphase flow, gas-liquid separation, bubble dynamics
- 22 papers + 1 book distilled via 9 parallel Sonnet subagents into 4 new KBs + 2 enhanced KBs (~4,000 lines)
- 4 new calculation scripts (bubble_dynamics, critical_velocity, flow_regime, separator_sizing)
- Gemini 3.1 Pro adversarial audit: 5 engineering challenges documented
- Key finding: gravity-based gas separation is physically impossible at 80,000 cP. Liquid fallback (WhaleShark-type) is the only viable mechanism.
- Design doc: `docs/plans/2026-04-15-multiphase-flow-specialist-design.md`

**Phase 3.5: SPE Paper Knowledge Enrichment — COMPLETE (2026-04-08)**
- 11 SPE papers distilled into 3 new knowledge bases (~680 lines total)
- `foamy-oil-dynamics.md`: 6 Bluesky papers — kinetic model, wormholes, CSS context
- `pcp-operations.md`: 5 PCP papers — DLS thresholds, ESPCP vs rod-driven, C-FER fatigue method
- `wellfi-telemetry.md`: Field data + Gemini — 7 diagnostic signatures, 10 decision rules
- Agent KB assignments updated: well-performance loads all 3, reservoir/simulation load foamy-oil, production-data loads wellfi-telemetry
- Gemini 3.1 Pro peer review: 0 corrections needed
- Source papers: `C:\Users\kyle\OneDrive - MPS Welding Inc\White Papers\Bluesky\` and `\PCP Pump\`

**Next: Phase 4 — Roundtable Orchestration**

## Directory Structure

```
petro-roundtable/
  CLAUDE.md              ← You are here
  ROUNDTABLE.md          ← Master identity (all agents load this)
  CONFIG.md              ← Model config, agent roster, phase status
  .claude/agents/        ← Agent definitions (.md files, auto-loaded by Claude Code)
    geoscientist.md      ← Phase 1: Bluesky Formation specialist
    reservoir-engineer.md ← Phase 3: Recovery, decline, waterflood, EOR
    drilling-engineer.md  ← Phase 3: Well design, directional, casing
    well-performance.md   ← Phase 3: Completions, sand control, PCP lift
    geomechanics.md       ← Phase 3: Rock mechanics, stability, cap rock
    facilities-engineer.md ← Phase 3: Surface facilities, separation, water
    economics-reserves.md ← Phase 3: COGEH, pricing, break-even, NPV
    simulation-engineer.md ← Phase 3: CMG STARS, thermal, foamy oil
    production-data.md    ← Phase 3: SCADA, analytics, dashboards
    multiphase-flow.md   ← Phase 3.75: Wellbore flow, separator design, bubble dynamics
    lead-engineer.md     ← Phase 4: Roundtable moderator, relevance-weighted cascade
  agents/console/        ← Console-mode prompts (sub-agent prompt resources)
  operators/             ← Operator representative agents (Phase 2+)
    obsidian-energy.md   ← Phase 2: Obsidian Energy operator rep
  knowledge/             ← Curated knowledge bases (verified, cited)
    bluesky-formation.md ← 13-section Bluesky reference (Phase 1)
    obsidian-energy.md   ← 13-section Obsidian Energy operator reference (Phase 2)
    foamy-oil-dynamics.md ← SPE paper KB: kinetic model, CHOPS, wormholes, CSS (6+3 papers) + Section 8: wellbore-scale gas behavior
    pcp-operations.md    ← SPE paper KB: DLS limits, ESPCP, fatigue, rod failure (5+1 papers) + multiphase gas handling
    wellfi-telemetry.md  ← Field data KB: 7 diagnostic signatures, decision rules, hydrostatic tables
    downhole-separation.md ← Separator design KB: WhaleShark, McCoy, MDPI (4 papers + cross-refs)
    multiphase-flow-regimes.md ← Flow regime KB: Barnea, Taitel-Dukler, Beggs-Brill, Nagoo (7 papers)
    bubble-dynamics-reference.md ← Clift/Grace/Weber book: Stokes, H-R, Grace correlation
    gemini-audit-challenges.md ← 5 adversarial engineering challenges for separator design
  .claude/skills/        ← Skill definitions (auto-loaded by Claude Code)
    bluesky-briefing/    ← /bluesky-briefing — formation deep-dive
    ask-engineer/        ← /ask-engineer — route question to specialist
    ask-operator/        ← /ask-operator — route question to operator rep
    roundtable/          ← /roundtable — multi-agent moderated discussion
    wellfi-storyboard-audit/ ← gate before customer-facing storyboard/Remotion work
    remotion-data-video/ ← Remotion video scaffolding
  calculations/          ← Python CLI scripts (run via Bash)
    decline_curves.py    ← Arps decline fitting, EUR estimation
    nodal_analysis.py    ← Vogel/Darcy IPR, VLP, operating point
    sand_control.py      ← PSD analysis, screen selection, erosional velocity
    bubble_dynamics.py   ← Stokes' law, Grace correlation, foamy viscosity correction, sand settling
    critical_velocity.py ← Nagoo critical gas velocity, residence time vs coalescence
    flow_regime.py       ← Flow regime prediction with heavy oil corrections
    separator_sizing.py  ← Downhole separator sizing, WhaleShark assessment, Gemini challenge checks
  mcp/                   ← MCP server definitions (Phase 5: StackDX)
  docs/
    plans/               ← Design docs and implementation plans
```

## Additional Skill

- `wellfi-storyboard-audit` - Use before customer-facing WellFi storyboard, marketing video, roundtable visual story, or Remotion edits. It locks claims to approved evidence, separates proven vs inferred statements, and forces a final validation pass before render.
- Skill path: `petro-roundtable/.claude/skills/wellfi-storyboard-audit/SKILL.md`
- Default evidence pack for the current Obsidian run: `Data/Obsidian/Wells/102161808317W509/analysis/wellfi-run3-deployment-story.png`, `run3-complete-timeline.md`, `run3-narrative.md`, `design-philosophy.md`

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
- **WellFi pressure is in BAR ABSOLUTE** — The sensor reads absolute pressure. Packet messages label it as BAR. For hydrostatic calculations, subtract the air reference reading (-0.49 BAR for this deployment) to get the liquid head. Temperature is in °C.
- **WellFi activation threshold varies per tool** — Check the deployment config for each tool. The first deployment used 50 kPa.
- **Tubing ≠ casing depths** — Downhole tools on tubing sit INSIDE casing, not at the casing shoe. Always ask: "Is this on tubing or casing?" before placing a tool depth.
- **Joint length is 9.456m for OBE HVS 16-18** — Do not assume 9.14m (30ft generic). Always verify from the Downhole Well Profile PDF.
- **Check LAS logs before offset extrapolation** — If Build/geosteering LAS files exist for a well, use the gamma ray to pick formation tops directly. Don't extrapolate from offset wells when you have the actual log.
- **Structural extrapolation uncertainty** — Bluesky structure varies 30+ meters across one township. Never present a formation boundary with false confidence from offsets alone.
- **Gemini fails at data-driven generation** — Gemini discards provided data and generates from training. Use Gemini for review/challenge ONLY, never for code that must use specific numbers.
- **Sales oil ≠ downhole oil** — Lab oil analysis labeled "Sales Oil" has been treated/heated. Viscosity will be lower than in-situ reservoir conditions.
- **WellFi CRC errors are NOT real pressure readings** — When isCRCError=01, the P and T values are garbled EM data. Exclude from trend analysis. The event itself is significant (indicates signal disruption, possibly from gas in annulus).
- **Hydrostatic head in deviated wells is non-linear** — At 86 deg inclination, a 9.5m joint adds only 0.66m TVD. At 69 deg, the same joint adds 3.4m TVD. Always interpolate TVD from the directional survey, never assume linear MD-to-TVD conversion.
- **Rod-driven PCP at >50 deg inclination = short run life** — SPE literature shows rod-driven PCP practical limit is ~50 deg deviation. At 86 deg (OBE 102 HZ), the 5-month average run time aligns with published 45-118 day range. ESPCP (rodless) is the literature recommendation for >70 deg.
- **Gemini cannot write files** — Gemini CLI MCP is read-only. Do not attempt to delegate file creation to Gemini. It will enter an infinite retry loop attempting write_file, run_shell_command, and generalist delegation — all fail. Use Gemini for review and questions only.
- **Tubing joints x joint length ≠ tool MD** — 86 joints × 9.456m = 813.2m is the tubing PIPE length. The tool's actual MD is the tubing set depth (832.28m) because the BHA (pump + tag bar + WellFi + no-turn + collar = ~19m) sits below the last tubing joint. Always use `tubing_set_depth_mkb` from wellGeometry.ts as the reference, then calculate positions as `set_depth - (joints_from_bottom × joint_length)`. Never multiply total joints × joint length and call it a depth.
- **OBE annulus is ALWAYS open to atmosphere** — Gas goes to flare stack, tubing to tanks. This means WellFi reads PURE liquid hydrostatic with no casing gas component. The 4-11 joint target corresponds to 0.38-2.12 BAR corrected (or -0.11 to 1.63 BAR raw display, accounting for the -0.49 BAR sensor offset). Run 3 readings of 18-21 BAR = full liquid column (~200m TVD), hundreds of joints above tag bar. The pump had only run 12 hours — would take weeks to reach the 4-11 joint operating range.
- **WellFi reads ABSOLUTE pressure in BAR** — The sensor outputs BAR absolute. In air it displayed -0.49 BAR (sensor zero drift; true atmospheric at Peace River elevation is ~0.93 BAR abs). For hydrostatic head calculations, use the differential: P_downhole - P_air_reference = liquid head. The -0.49 air reading is the zero reference for this deployment.
- **WellFi measurement interval changes after 48 hours** — First 48 hours: transmits every 3 minutes. After 48 hours: switches to every 6 hours (battery conservation). Plan field monitoring accordingly.

## Visualization

Use the `engineering-visual` skill for well schematics, deployment diagrams, and subsurface cross-sections. Design philosophy: "Subterranean Signal" — dark theme, dual-purpose for marketing + engineering audiences. Key rules:
- Every number on the canvas must be verifiable against a source file
- If formation boundary is uncertain, don't show it — note the uncertainty
- Cyan=data, Amber=tools, Green=geology, Red=alerts
- Use the `remotion-data-video` skill for animated data stories (Remotion → MP4 video)
- Remotion `npx create-video` has interactive prompts that fail in Claude Code — scaffold manually
- For animated callouts, use temporal separation (appear/disappear per act), not spatial stacking

For customer-facing WellFi storyboard and Remotion work, use `wellfi-storyboard-audit` first. It locks scenes to approved evidence, separates proven vs inferred claims, and is the required gate before animation or render changes.

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

For WellFi marketing / Remotion work, preserve legacy story compositions. Build new run-scoped files and data modules instead of overwriting older storyboard code until the replacement is reviewed and approved.

## Branch Strategy

- **This project:** `petro-roundtable/main` branch (and `petro-roundtable/phase-N` for active work)
- **WellFi app:** `codex/*` branches (separate git history)
- Do NOT mix petro-roundtable commits with wellfi-app feature branches

## Two Agent Systems — Do Not Confuse

This repo contains two completely unrelated agent systems:

| | Petro-Roundtable Agents (THIS PROJECT) | WellFi Development Agents |
|---|---|---|
| **Purpose** | Domain experts that ARE the product | Development agents that help BUILD the wellfi-app |
| **Location** | `petro-roundtable/.claude/agents/` | `wellfi-app/agents/session-{N}/` |
| **Examples** | Geoscientist, reservoir engineer | UI agent, data-integrity agent |
| **Invoked by** | Users via `/ask-engineer`, `/roundtable` | Claude Code during dev sessions |
| **Identity** | `ROUNDTABLE.md` | `wellfi-app/agents/COORDINATOR.md` |

These systems share no code, no identity, and no coordination. If you are working on petro-roundtable, ignore `wellfi-app/agents/` entirely.

## Related Projects

- `wellfi-app/` — WellFi multi-operator monitoring app (sibling project, same repo)
- `hermes-petro-agents/` — Legacy Hermes agent definitions (being replaced by this)
- `roundtable-bridge/` — Legacy FastAPI bridge server (being replaced by this)
