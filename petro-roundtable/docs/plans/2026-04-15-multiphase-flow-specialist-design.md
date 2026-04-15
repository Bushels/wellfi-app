# Multiphase Flow Specialist — Agent Design Document

**Date:** 2026-04-15
**Status:** Approved
**Approach:** A — Knowledge-First Build (then Roundtable validation)

## 1. Agent Identity

- **File:** `petro-roundtable/agents/multiphase-flow.md`
- **Agent ID:** `specialist-multiphase-flow`
- **Title:** Senior Multiphase Flow Specialist
- **Model:** claude-opus-4-6
- **Tools:** Read, Grep, Glob, WebSearch, WebFetch, Bash
- **Gemini review:** true

**Persona:** 25+ years in wellbore hydraulics, downhole multiphase flow, and separation system design for heavy oil production. Deep expertise in flow regime prediction, bubble dynamics in viscous fluids, downhole separator design/selection, and tool-scale CFD. Has designed and field-tested separation systems across Western Canada heavy oil basins (Peace River, Lloydminster, Cold Lake). Published on foamy oil behavior in wellbore geometries and critical gas velocity thresholds for inclined wells.

## 2. Domain Ownership

| Domain | Scope |
|---|---|
| Multiphase flow regimes | Slug, churn, bubble, annular flow prediction in inclined/horizontal wellbores. Barnea, Taitel & Dukler correlations. Flow pattern maps per geometry. |
| Bubble dynamics | Stokes' law at high viscosity (80,000+ cP), bubble rise velocity, coalescence kinetics, dispersed vs free gas transition, foam stability |
| Downhole separator design | Poor-boy, Packer-style, WhaleShark-type. Eccentric vs centric flow paths, intake orientation, hydraulic diameter effects, turbulence minimization |
| Critical gas velocities | Liquid lifting threshold, liquid fallback rates, Nagoo equation (diameter + inclination dependent), Turner correlation adapted for heavy oil |
| Inclination effects | Separation efficiency vs angle (0-90 deg), solids angle of repose (65 deg), liquid holdup changes with deviation |
| BHA integration | Separator + WellFi sonde + PCP + tag bar + no-turn tool stack design, flow path through combined assembly, annular clearances |
| Tool-scale simulation | Analytical models for separator sizing, OpenFOAM/CFD guidance for detailed flow modeling within separator geometry |

**Defers to existing specialists:**
- Reservoir-scale foamy oil mechanism → Reservoir Engineer
- PCP rotor/stator selection → Well Performance
- Surface separation & emulsion treatment → Facilities Engineer
- CMG STARS reservoir simulation → Simulation Engineer
- Mechanical CAD of tool geometry → FreeCAD Mechanical Engineer

## 3. Knowledge Architecture

### Knowledge bases loaded by this agent:

1. `petro-roundtable/knowledge/bluesky-formation.md` (existing)
2. `petro-roundtable/knowledge/foamy-oil-dynamics.md` (enhanced — add Section 8: Wellbore-Scale Gas Behavior)
3. `petro-roundtable/knowledge/downhole-separation.md` (NEW)
4. `petro-roundtable/knowledge/multiphase-flow-regimes.md` (NEW)
5. `petro-roundtable/knowledge/pcp-operations.md` (existing)
6. `petro-roundtable/ROUNDTABLE.md` (existing)

### New KB 1: `downhole-separation.md`

Sections:
1. Separator Types — Poor-boy, Packer-style, WhaleShark. Mechanics, pros/cons, operating envelope
2. Seven Design Principles — eccentric flow (+30%), intake orientation (+50%), turbulence minimization (+25%), hydraulic diameter, side intake limits, process sequence, slug tolerance
3. Critical Velocity Thresholds — 6 ft/s side-intake limit, liquid fallback rate vs bubble rise, Nagoo equation
4. Heavy Oil / Foamy Oil Considerations — Stokes' law at 80,000+ cP, foam entrainment, dispersed gas coalescence suppression, foamy oil viscosity (SPE-136665)
5. Inclination Effects — gas: efficient to 80 deg, solids: max 65 deg, 30% improvement at 40-45 deg
6. Separator-Pump Integration — PCP intake requirements, pump fillage, gas interference, TAC annular flow-by
7. WellFi Integration — P/T signatures for separator performance monitoring
8. BHA Stack Design — Physical arrangement in 8-5/8" casing with 2-7/8" tubing
9. Case Studies — Charlie Lake foamy oil, Montney horizontal, Permian, Canadian heavy oil
10. Design Calculations — Stokes' bubble rise, critical gas velocity, residence time, cross-section requirements

**Primary sources:** WhaleShark (Saponja 2021), McCoy (Echometer 1998), MDPI Phase Isolation (2021), SPE-215112 (2023 review, deferred), Shroud-type separator (JPT 2021, deferred)

### New KB 2: `multiphase-flow-regimes.md`

Sections:
1. Flow Regime Classification — bubble, slug, churn, annular, stratified
2. Flow Pattern Maps — superficial velocity charts for 8-5/8" casing and 8-5/8" x 2-7/8" tubing annulus at 86 deg
3. Inclination Effects on Flow Regime — stratified flow onset, slug formation at high angles
4. Liquid Holdup Correlations — Beggs & Brill, Mukherjee & Brill, drift-flux model
5. Heavy Oil Specifics — how 80,000+ cP alters flow regime boundaries, delayed coalescence, viscous slugging
6. Liquid Fallback & Flow Reversals — counter-current flow, liquid film drainage, the physics WhaleShark exploits
7. Pressure Gradient Models — mechanistic pressure drop (gravitational + frictional + accelerational)
8. CFD Methodology — OpenFOAM solver selection (interFoam/VOF, twoPhaseEulerFoam), grid requirements, validation approach
9. WellFi Observable Signatures — flow regime identification from P/T data, slug frequency from pressure oscillations

**Primary sources:** Barnea (1987), Taitel & Dukler (1976), Beggs & Brill (1973), Nagoo (2018, 2019), Gokcal/SPE-102727, high-viscosity Springer (2017)

### Enhancement: `foamy-oil-dynamics.md` — Add Section 8

**Section 8: Wellbore-Scale Gas Behavior**
- Foamy-to-free-gas transition conditions (pressure, temperature, shear)
- Shear effects on foam stability (PCP rotation, rod movement, turbulence)
- Annular gas segregation at 86 deg inclination
- Foamy oil viscosity changes with GVF (SPE-136665 data)
- Implications for separator placement (above vs below transition zone)

**Primary sources:** SPE-136665 (Alshmakhy & Maini), SPE-56541 (Maini 1999), SPE-56540 (Sheng et al. 1999), existing 6 papers

## 4. Paper Inventory

### Multiphase Flow folder (16 papers + 1 book)

| File | Paper | Priority |
|---|---|---|
| `0301-93222990002-4.pdf` | Barnea 1987 — Unified flow pattern model | T1 |
| `aic.690220105.pdf` | Taitel & Dukler 1976 — Flow pattern map | T1 |
| `190921-MS.pdf` | Nagoo 2018 — Critical gas velocity equation | T1 |
| `102727-PA.pdf` | Gokcal — High viscosity flow in horizontal pipes | T1 |
| `Improved-Downhole-Gas-Separators.pdf` | McCoy — Downhole separator sizing | T1 |
| `Bubbles, drops, and particles...pdf` | Clift, Grace, Weber — Reference book | T2 |
| `56541-ms.pdf` | Maini 1999 — Foamy oil flow review | T2 |
| `a%3A1006575510872.pdf` | Sheng et al. 1999 — Critical review foamy oil models | T2 |
| `195893-ms.pdf` | Nagoo/Kannan 2019 — Heel-dominant liquid loading | T2 |
| `applsci-11-10496.pdf` | MDPI — Phase isolation separator | T2 |
| `95272-ms.pdf` | Bratu 2005 — PCP in multiphase conditions | T2 |
| `136665-MS.pdf` | Alshmakhy & Maini — Foamy oil viscosity | T2 |
| `15094-PA.pdf` | Smith 1988 — Foundational CHOPS paper | T3 |
| `4007-pa.pdf` | Beggs & Brill 1973 — Multiphase pressure drop | T3 |
| `s00231-017-2158-5.pdf` | Springer 2017 — High viscosity multiphase flow | T3 |

### Flow Control folder (5 relevant papers)

| File | Paper | Relevance |
|---|---|---|
| `MultiphaseFlowICD(2014).pdf` | SPE-171890 — Multiphase flow through downhole devices, lab testing | Experimental methodology for downhole device characterization |
| `irani2020CFDforICD.pdf` | Irani 2020 — CFD for flow control devices, SAGD flashing | Phase change CFD methodology (nucleation modeling) |
| `CFD Flash Flow.pdf` | SPE-199929 — Flashing flow CFD in convergent-divergent nozzle | Nucleation/vaporization CFD approach transferable to foamy oil |
| `Converging Diverging Annulus CFD.pdf` | Hoo et al. — Annular flow with cavitation CFD | Annular geometry flow modeling directly applicable to separator |
| `Inflow Autonomous AICD spe-218393-pa 2023.pdf` | SPE-218393 — Autonomous ICDs, CMG STARS simulation | Fluid-discriminating device concept + simulation methodology |

### Already in Bluesky folder (6 papers, already distilled into foamy-oil-dynamics.md)

SPE-175390, SPE-174431, SPE-174446, SPE-170879, SPE-150633, SPE-118244

### WhaleShark paper (already have)

`Data/Obsidian/2021031 - ENHANCING DOWNHOLE GAS AND SOLIDS SEPARATION...pdf`

### Deferred (user to acquire later)

- SPE-215112 — 2023 comprehensive separator review (OnePetro paywall)
- Shroud-type separator at high deviation (JPT 2021, publication access)

**Total: 22 papers + 1 book in hand, 2 deferred**

## 5. Calculation Scripts

| Script | Purpose | Key Equations |
|---|---|---|
| `bubble_dynamics.py` | Stokes' law bubble rise in heavy oil, Grace correlation | v = (2/9)(rho_l - rho_g)gR^2/mu + Grace for non-Stokes |
| `critical_velocity.py` | Nagoo equation — liquid loading onset per geometry | v_crit = f(diameter, inclination, fluid properties) |
| `separator_sizing.py` | Downhole separator sizing | Stokes + fallback velocity + cross-section geometry + residence time |
| `flow_regime.py` | Flow regime prediction (Barnea/Taitel-Dukler) | Superficial velocities to regime map lookup |

Location: `petro-roundtable/calculations/`

## 6. Simulation Approach

- **Tier 1 (daily use):** Analytical Python models (calculation scripts above)
- **Tier 2 (geometry validation):** OpenFOAM — interFoam (VOF) for slug flow, twoPhaseEulerFoam for bubbly flow. Agent generates case files, user runs externally.
- **Not building:** Custom simulator (analytical + OpenFOAM cover the full range)

## 7. Skills

| Skill | Purpose |
|---|---|
| Update `ask-engineer` | Add multiphase-flow to routing table |
| New: `separator-design` | Guided workflow: well conditions → flow regime → size separator → recommend type → BHA stack |

## 8. Operating Envelope (Reference Geometry)

| Parameter | Value | Source |
|---|---|---|
| Casing | 8-5/8" intermediate | OBE 102 HZ 16-18 |
| Tubing | 2-7/8" EUE | OBE standard |
| Inclination at tool depth | 86 deg | Directional survey |
| Artificial lift | PCP (rod-driven, 260 RPM) | OBE operations |
| Liquid rate | ~190 bbl/d | Production data |
| Solution GOR | 5-15 scf/bbl | Bluesky typical |
| Oil viscosity | 80,000+ cP at reservoir temp | Bluesky upper zone |
| Annulus | Open to atmosphere (gas vents to flare) | OBE completion |
| WellFi position | ~820 m MD, inside 8-5/8" casing on tubing | Run 3 deployment |

## 9. Distillation Workflow

**Model strategy:** Sonnet 4.6 subagents for paper reading and KB drafting (token efficiency). Opus 4.6 for quality review.

**Per-paper workflow:**
1. Sonnet subagent reads PDF
2. Extracts: key data tables, equations, design rules, field results
3. Drafts KB section with citations (SPE #, page/figure)
4. Opus reviews for accuracy, completeness, citation quality
5. Iterate if needed, finalize KB section

**Distillation grouping:**
- Group A (downhole-separation.md): WhaleShark, McCoy, MDPI Phase Isolation, SPE-171890
- Group B (multiphase-flow-regimes.md): Barnea, Taitel & Dukler, Beggs & Brill, Nagoo x2, Gokcal, Springer 2017
- Group C (foamy-oil-dynamics.md Section 8): SPE-136665, SPE-56541, SPE-56540, SPE-15094
- Group D (CFD methodology reference): Irani 2020, Flash Flow CFD, Converging Annulus CFD, SPE-218393
- Group E (PCP multiphase): SPE-95272 (enhances pcp-operations.md)

## 10. Integration with Existing System

- Adds as 10th specialist in petro-roundtable CONFIG.md
- Routes via updated `ask-engineer` skill
- Cross-consults: reservoir (foamy oil), well-performance (PCP), facilities (surface), simulation (CMG), FreeCAD (tool CAD)
- Gemini peer review on sizing/selection recommendations
- First real roundtable question after agent is built: "Design a downhole gas-oil separator for OBE's 86 deg Bluesky wells with PCP lift"

## 11. Reminders

- [ ] Acquire SPE-215112 (2023 separator review) — user could not access OnePetro
- [ ] Acquire Shroud-type separator study (JPT 2021) — user could not access
- [ ] When acquired, distill into downhole-separation.md Sections 1 and 5
