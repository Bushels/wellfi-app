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

**Phase 4: Roundtable Orchestration** (next)

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
| Lead Engineer | Planned | 4 | claude-opus-4-6 | Orchestration, routing, synthesis, arbitration, regulatory integration |

## Operator Representatives

| Operator | Status | Phase | Domain |
|---|---|---|---|
| Obsidian Energy | **Active** | 2 | Peace River Bluesky — cold-flow horizontal, fishbone wells, WellFi monitoring |
| CNRL | Planned | 6 | Peace River Bluesky/Clearwater — thermal CSS, Carmon Creek |
| Baytex | Planned | 6 | Peace River Bluesky — polymer flood, Seal field |
| Headwater | Planned | 6 | Clearwater — SAGD, primary cold flow |

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

## Calculation Script Inventory

| Script | Status | Agents Using |
|---|---|---|
| `decline_curves.py` | **Built** | Reservoir, Economics, Production Data, Simulation |
| `nodal_analysis.py` | **Built** | Reservoir, Well Performance, Simulation |
| `sand_control.py` | **Built** | Well Performance, Drilling, Geomechanics, Facilities |
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
