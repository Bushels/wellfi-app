# Petro-Roundtable Configuration

## Branch

- **Main:** `petro-roundtable/main`
- **Active work:** `petro-roundtable/phase-N` (branched from petro-roundtable/main)

## Model Assignments

| Model | ID | Role |
|---|---|---|
| Claude Opus 4.6 | `claude-opus-4-6` | Primary agent model (current) |
| Claude Mythos | `claude-mythos` | Primary agent model (future — per-agent rollout) |
| Gemini 3.1 Pro | `gemini-3.1-pro` | Deep peer review, knowledge audits, devil's advocate |
| Gemini 3.1 Flash | `gemini-3.1-flash` | Quick sanity checks, data validation |

## Active Phase

**Phase 3.75: Multiphase Flow Specialist** (complete)
**Phase 4: Roundtable Orchestration** (complete)

### Completed Phases
- Phase 1: Bluesky Formation Mastery — 10/10 validation, Gemini audited
- Phase 2: Obsidian Energy Operator Mastery — 10/10 validation, Gemini audited
- Phase 3: Engineering Panel Activation — 8 agents built, consistency reviewed, Gemini audited (0 critical gaps)

## Agent Roster

| Agent | Status | Phase | Model | Domain |
|---|---|---|---|---|
| Geoscientist | **Active** | 1 | claude-opus-4-6 | Formation evaluation, petrophysics, stratigraphy, facies mapping |
| Reservoir Engineer | **Active** | 3 | claude-opus-4-6 | Drainage, recovery factors, decline curves, waterflood, EOR |
| Drilling Engineer | **Active** | 3 | claude-opus-4-6 | Well design, directional, casing, cementing, mud weight |
| Well Performance | **Active** | 3 | claude-opus-4-6 | Completions, sand control, PCP/ESP lift, production optimization |
| Geomechanics | **Active** | 3 | claude-opus-4-6 | Rock mechanics, wellbore stability, cap rock, stress analysis |
| Facilities Engineer | **Active** | 3 | claude-opus-4-6 | Surface facilities, OTSG, separation, water treatment, sand handling |
| Economics & Reserves | **Active** | 3 | claude-opus-4-6 | COGEH/NI 51-101, WCS pricing, break-even, F&D, NPV |
| Simulation Engineer | **Active** | 3 | claude-opus-4-6 | CMG STARS/IMEX, thermal modeling, foamy oil, multiphase flow |
| Production Data | **Active** | 3 | claude-opus-4-6 | SCADA, analytics, dashboards, data quality, WellFi integration |
| Multiphase Flow | **Active** | 3.75 | claude-opus-4-6 | Wellbore flow regimes, bubble dynamics, downhole separator design, BHA integration |
| Lead Engineer | **Active** | 4 | claude-opus-4-6 | Roundtable moderator, relevance-weighted cascade, cross-discipline synthesis |

## Operator Representatives

| Operator | Status | Phase | Domain |
|---|---|---|---|
| Obsidian Energy | **Active** | 2 | Peace River Bluesky — cold-flow horizontal, fishbone wells, WellFi monitoring |
| CNRL | Planned | 6 | Peace River Bluesky/Clearwater — thermal CSS, Carmon Creek |
| Baytex | Planned | 6 | Peace River Bluesky — polymer flood, Seal field |
| Headwater | Planned | 6 | Clearwater — SAGD, primary cold flow |

## Skill Inventory

| Skill | Status | Purpose |
|---|---|---|
| `bluesky-briefing` | Active | Formation-level Bluesky deep-dive and context loading |
| `ask-engineer` | Active | Route questions to the correct petroleum engineering specialist |
| `ask-operator` | Active | Route questions to an operator representative |
| `wellfi-storyboard-audit` | Active | Validate customer-facing WellFi storyboard, narrative, and Remotion claims against approved evidence before animation or rendering |
| `roundtable` | Active | Multi-agent roundtable discussion with Lead Engineer moderator, relevance-weighted cascade, Gemini advisor |

**Run 3 visual-story workflow:** For Obsidian well `102161808317W509`, use `wellfi-storyboard-audit` before changing any storyboard or Remotion scene. Preserve legacy compositions and create run-scoped replacements instead of overwriting older story files.

## Gemini Integration Tiers

1. **Agent-level** (Gemini 3.1 Flash) — Quick sanity checks during individual agent responses
2. **Roundtable challenge** (Gemini 3.1 Pro) — After panel reaches consensus, Gemini reviews
3. **Devil's advocate** (Gemini 3.1 Pro) — On `--challenge` flag, Gemini actively argues against consensus

## Mastery Sequence

1. ~~Bluesky Formation Mastery~~ (complete)
2. ~~Obsidian Energy Operator Mastery~~ (complete)
3. ~~Engineering Panel — 9 specialists + 1 operator rep~~ (complete)
4. Roundtable Orchestration (Lead Engineer + /roundtable skill) — next
5. StackDX MCP Server
6. Operator Expansion (CNRL, Baytex, Headwater)
7. Formation Expansion (Clearwater, McMurray)

## Phase 3 Gemini Audit Notes

Gemini 3.1 Pro panel audit (2026-04-07): **0 critical gaps found.**

**Noted for future phases:**
- Regulatory/AER Compliance integration → Phase 4 Lead Engineer will serve as regulatory checkpoint
- Geophysicist (3D/4D seismic interpretation) → Phase 7 when seismic data becomes relevant

**Top 3 cross-agent interaction scenarios identified:**
1. End-to-end sand management: Geomechanics → Well Performance → Facilities
2. Foamy oil drawdown optimization: Simulation/Reservoir → Well Performance → Production Data
3. Caprock integrity & EOR injection: Geomechanics → Reservoir → Drilling

## Knowledge Base Inventory

| File | Lines | Source | Loaded By |
|---|---|---|---|
| `bluesky-formation.md` | ~300 | Geological source + web research (Phase 1) | All 9 agents + operator |
| `obsidian-energy.md` | ~650 | 3 corporate PDFs + CSV analysis (Phase 2) | 7 agents + operator |
| `foamy-oil-dynamics.md` | ~210 | 6 SPE papers (175390, 174431, 174446, 170879, 150633, 118244) | well-performance, reservoir-engineer, simulation-engineer |
| `pcp-operations.md` | ~250 | 5 SPE papers (136816, 93594, 171352, 192464, Energies-15-04259) | well-performance |
| `wellfi-telemetry.md` | ~220 | OBE Run 3 field data + Gemini diagnostic analysis | well-performance, production-data |
| `downhole-separation.md` | ~1090 | 4 papers (WhaleShark, McCoy, MDPI, SPE-171890) + cross-reference synthesis | multiphase-flow |
| `multiphase-flow-regimes.md` | ~1317 | 7 papers (Barnea, Taitel-Dukler, Beggs-Brill, Nagoo x2, Gokcal, Springer) | multiphase-flow |
| `bubble-dynamics-reference.md` | ~358 | Clift, Grace & Weber (1978) book extract | multiphase-flow |
| `gemini-audit-challenges.md` | ~100 | 5 adversarial engineering challenges from Gemini 3.1 Pro | multiphase-flow |

Added 2026-04-08: Three KBs distilled from 11 SPE papers on foamy oil dynamics, PCP pump placement/fatigue, and WellFi telemetry interpretation. Gemini 3.1 Pro peer review: 0 corrections needed.

Added 2026-04-15: Four KBs + 1 reference for Multiphase Flow Specialist (Phase 3.75). Distilled from 22 papers + 1 book via 9 parallel Sonnet subagents. Enhanced foamy-oil-dynamics.md (Section 8: wellbore-scale gas behavior) and pcp-operations.md (multiphase gas handling). Gemini 3.1 Pro adversarial audit: 5 challenges identified and documented.

## Calculation Script Inventory

| Script | Status | Agents Using |
|---|---|---|
| `decline_curves.py` | **Built** | Reservoir, Economics, Production Data, Simulation |
| `nodal_analysis.py` | **Built** | Reservoir, Well Performance, Simulation |
| `sand_control.py` | **Built** | Well Performance, Drilling, Geomechanics, Facilities |
| `bubble_dynamics.py` | **Built** | Multiphase Flow |
| `critical_velocity.py` | **Built** | Multiphase Flow |
| `flow_regime.py` | **Built** | Multiphase Flow |
| `separator_sizing.py` | **Built** | Multiphase Flow |
| `esp_design.py` | **Missing** (in design doc) | Well Performance |
| `wellbore_hydraulics.py` | **Missing** (in design doc) | Drilling |

**Additional gaps flagged by Phase 3 agents:**
- `material_balance.py`, `waterflood_prediction.py`, `thermal_design.py` (Reservoir)
- `casing_design.py`, `directional_planning.py` (Drilling)
- `pcp_design.py`, `pump_optimization.py` (Well Performance)
- `wellbore_stability.py`, `stress_analysis.py`, `cap_rock_integrity.py` (Geomechanics)
- `separator_sizing.py`, `heater_treater_design.py`, `pipeline_hydraulics.py`, `otsg_design.py` (Facilities)
- `economic_analysis.py`, `npv_calculator.py`, `reserves_classification.py` (Economics)
- `simulation_preprocessor.py`, `history_match_qc.py` (Simulation)
- `data_quality.py`, `production_allocation.py`, `rate_transient_analysis.py` (Production Data)
