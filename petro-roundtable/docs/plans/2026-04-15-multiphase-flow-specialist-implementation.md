# Multiphase Flow Specialist — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the 10th petro-roundtable specialist agent with expert knowledge in downhole multiphase flow, gas-liquid separation, and bubble dynamics in heavy oil — distilled from 22 papers + 1 book.

**Architecture:** Knowledge-first build. Sonnet 4.6 subagents read papers and draft KB sections (token-efficient). Opus 4.6 reviews each KB for accuracy, completeness, and citation quality. After KBs are complete, build the agent definition, calculation scripts, and skills. Finally, validate with 5 questions + Gemini audit.

**Tech Stack:** Claude Code agents (Sonnet 4.6 for distillation, Opus 4.6 for review), Python (calculation scripts), petro-roundtable agent framework (markdown agent definitions + knowledge bases)

**Model Strategy:**
- Subagent work (paper reading, KB drafting): `model: "sonnet"` parameter on Agent tool
- Quality review + agent definition writing: Opus (main session)
- Peer review: Gemini 3.1 Pro via `mcp__gemini-cli__ask-gemini`

**Paper Library Root:** `C:\Users\kyle\OneDrive - MPS Welding Inc\White Papers\Multiphase Flow\`
**Flow Control Papers:** `C:\Users\kyle\OneDrive - MPS Welding Inc\White Papers\Flow Control\`
**Existing KB Location:** `C:\Users\kyle\MPS\Obsidian\petro-roundtable\knowledge\`
**Agent Location:** `C:\Users\kyle\MPS\Obsidian\petro-roundtable\agents\`
**Calculation Scripts:** `C:\Users\kyle\MPS\Obsidian\petro-roundtable\calculations\`
**Design Doc:** `petro-roundtable/docs/plans/2026-04-15-multiphase-flow-specialist-design.md`

---

## Task 1: Distill KB Group A — Downhole Separation (4 papers → `downhole-separation.md`)

**Papers to read:**
- `Data/Obsidian/2021031 - ENHANCING DOWNHOLE GAS AND SOLIDS SEPARATION...pdf` (WhaleShark, Saponja 2021) — 20 pages
- `White Papers/Multiphase Flow/Improved-Downhole-Gas-Separators.pdf` (McCoy 1998) — ~15 pages
- `White Papers/Multiphase Flow/applsci-11-10496.pdf` (MDPI Phase Isolation 2021) — ~20 pages
- `White Papers/Flow Control/ICD/MultiphaseFlowICD(2014).pdf` (SPE-171890, lab testing methodology) — ~20 pages

**Output file:** `petro-roundtable/knowledge/downhole-separation.md`

**Step 1: Dispatch Sonnet subagent to read WhaleShark paper and draft Sections 1-3**

Launch Agent with `model: "sonnet"`:
- Read the WhaleShark PDF (all 20 pages)
- Extract: separator types (Poor-boy, Packer, WhaleShark), 7 design principles with quantified improvements, critical velocity thresholds (6 ft/s side-intake limit)
- Format as KB sections 1-3 with citation format: `(Saponja et al. 2021 SWPSC, p.X)` or `(Saponja et al. 2021, Figure X)`
- Include all numerical data in tables (velocities, efficiency improvements, dimensions)
- Write to `petro-roundtable/knowledge/downhole-separation-draft-a1.md`

**Step 2: Dispatch Sonnet subagent to read McCoy + MDPI papers and draft Sections 4-6**

Launch Agent with `model: "sonnet"`:
- Read McCoy PDF (~15 pages) — focus on: separator sizing calculations, dip tube friction loss, gas separator placement rules (above vs below formation)
- Read MDPI Phase Isolation PDF (~20 pages) — focus on: phase isolation concept, experimental validation, novel design principles
- Extract and merge into KB sections covering: separator sizing methodology, pump integration requirements, placement guidelines
- Write to `petro-roundtable/knowledge/downhole-separation-draft-a2.md`

**Step 3: Dispatch Sonnet subagent to read SPE-171890 and draft Section 9 (lab methodology)**

Launch Agent with `model: "sonnet"`:
- Read SPE-171890 (MultiphaseFlowICD 2014) — focus on: experimental setup, two-phase flow testing protocol, viscosity effects on device performance (2-60 cP data), standardized testing methodology
- Extract: test parameters, measurement techniques, how to characterize downhole device performance
- Write to `petro-roundtable/knowledge/downhole-separation-draft-a3.md`

**Step 4: Opus reviews and assembles `downhole-separation.md`**

Main session (Opus):
- Read all three draft files
- Check: are all numerical values correct against source papers? Are citations complete? Did Sonnet miss critical insights?
- Assemble into final `petro-roundtable/knowledge/downhole-separation.md` with all 10 sections from the design doc
- Add Quick Reference Table at top (matching existing KB format)
- Add Source Papers table at bottom
- Sections 7 (WellFi Integration), 8 (BHA Stack), 10 (Design Calculations) — Opus drafts these from first principles + existing WellFi telemetry KB + OBE deployment data

**Step 5: Commit**

```bash
git add petro-roundtable/knowledge/downhole-separation.md
git commit -m "feat(kb): add downhole-separation.md — 4 papers distilled, 10 sections"
```

Clean up draft files:
```bash
rm petro-roundtable/knowledge/downhole-separation-draft-*.md
```

---

## Task 2: Distill KB Group B — Multiphase Flow Regimes (7 papers → `multiphase-flow-regimes.md`)

**Papers to read:**
- `White Papers/Multiphase Flow/0301-93222990002-4.pdf` (Barnea 1987) — ~12 pages
- `White Papers/Multiphase Flow/aic.690220105.pdf` (Taitel & Dukler 1976) — ~12 pages
- `White Papers/Multiphase Flow/4007-pa.pdf` (Beggs & Brill 1973) — ~15 pages
- `White Papers/Multiphase Flow/190921-MS.pdf` (Nagoo 2018 — critical gas velocity) — ~20 pages
- `White Papers/Multiphase Flow/195893-ms.pdf` (Nagoo/Kannan 2019 — heel-dominant loading) — ~20 pages
- `White Papers/Multiphase Flow/102727-PA.pdf` (Gokcal — high viscosity flow) — ~15 pages
- `White Papers/Multiphase Flow/s00231-017-2158-5.pdf` (Springer 2017 — high viscosity multiphase) — ~15 pages

**Output file:** `petro-roundtable/knowledge/multiphase-flow-regimes.md`

**Step 1: Dispatch Sonnet subagent — Foundational models (Barnea + Taitel-Dukler + Beggs-Brill)**

Launch Agent with `model: "sonnet"`:
- Read Barnea 1987: extract transition mechanisms for each flow pattern boundary, the unified model logic, inclination dependence
- Read Taitel & Dukler 1976: extract the original flow pattern map construction, superficial velocity definitions, transition criteria for horizontal/near-horizontal
- Read Beggs & Brill 1973: extract pressure gradient correlation (gravitational + frictional + accelerational), liquid holdup correlation, flow pattern map
- Format as KB sections 1-3 (Flow Regime Classification, Flow Pattern Maps, Inclination Effects)
- Include key equations in LaTeX-free plaintext (e.g., `v_sg = Q_g / A` not `$v_{sg} = \frac{Q_g}{A}$`)
- Write to `petro-roundtable/knowledge/flow-regimes-draft-b1.md`

**Step 2: Dispatch Sonnet subagent — Nagoo critical velocity papers**

Launch Agent with `model: "sonnet"`:
- Read SPE-190921 (Nagoo 2018): extract the critical gas velocity equation as explicit function of diameter and inclination, the Taylor instability derivation, field validation database (which plays, how many wells, accuracy)
- Read SPE-195893 (Nagoo/Kannan 2019): extract heel-dominant loading phenomenon, how liquid loading starts at the heel in horizontal wells, high-frequency BHP data analysis, implications for separator placement
- Format as KB sections 5 (Liquid Fallback & Flow Reversals) and part of section 3
- Write to `petro-roundtable/knowledge/flow-regimes-draft-b2.md`

**Step 3: Dispatch Sonnet subagent — Heavy oil specific flow behavior**

Launch Agent with `model: "sonnet"`:
- Read SPE-102727 (Gokcal): extract how oil viscosity >1,000 cP changes flow pattern boundaries, slug characteristics, liquid holdup. Key data: at what viscosity do standard correlations break down?
- Read Springer 2017 (high viscosity multiphase): extract lab data on flow patterns at high viscosity, any new correlations proposed
- Format as KB section 4 (Heavy Oil Specifics) — this is the KEY section that none of the existing literature reviews cover well
- Write to `petro-roundtable/knowledge/flow-regimes-draft-b3.md`

**Step 4: Opus reviews and assembles `multiphase-flow-regimes.md`**

Main session (Opus):
- Read all three draft files
- Verify equations and numerical values against source papers
- Assemble into final KB with all 9 sections from design doc
- Add section 6 (Pressure Gradient Models) — Opus derives from Beggs-Brill data
- Add section 7 (CFD Methodology) — from design doc + OpenFOAM tutorial knowledge
- Add section 8 (WellFi Observable Signatures) — derive from physics + existing wellfi-telemetry.md
- Add Quick Reference Table + Source Papers table

**Step 5: Commit**

```bash
git add petro-roundtable/knowledge/multiphase-flow-regimes.md
git commit -m "feat(kb): add multiphase-flow-regimes.md — 7 papers distilled, 9 sections"
```

Clean up draft files.

---

## Task 3: Distill KB Group C — Enhance `foamy-oil-dynamics.md` Section 8 (4 papers)

**Papers to read:**
- `White Papers/Multiphase Flow/136665-MS.pdf` (Alshmakhy & Maini — foamy oil viscosity)
- `White Papers/Multiphase Flow/56541-ms.pdf` (Maini 1999 — foamy oil flow review)
- `White Papers/Multiphase Flow/a%3A1006575510872.pdf` (Sheng et al. 1999 — critical review)
- `White Papers/Multiphase Flow/15094-PA.pdf` (Smith 1988 — CHOPS foundational)

**Output:** Add Section 8 to existing `petro-roundtable/knowledge/foamy-oil-dynamics.md`

**Step 1: Dispatch Sonnet subagent — Read SPE-136665 (foamy oil viscosity)**

Launch Agent with `model: "sonnet"`:
- Read full paper — this is the CRITICAL paper for wellbore-scale gas behavior
- Extract: how foamy oil viscosity changes with gas volume fraction (GVF), shear rate dependence, measurement techniques (Cambridge viscometer, capillary tube, falling needle), key finding that foamy oil viscosity is flow-rate dependent
- Extract any data tables of viscosity vs GVF at different shear rates
- Note: the finding that "viscosity of foamy oil was found to be similar to live oil viscosity for a large range of gas volume fraction" — this is counterintuitive and critical for Stokes' law calculations
- Write to `petro-roundtable/knowledge/foamy-oil-section8-draft-c1.md`

**Step 2: Dispatch Sonnet subagent — Read Maini 1999 + Sheng 1999 for wellbore-scale insights**

Launch Agent with `model: "sonnet"`:
- Read SPE-56541 (Maini 1999): focus on sections about gas disengagement from oil, bubble coalescence conditions, what triggers the transition from foamy to conventional flow
- Read Sheng et al. 1999: focus on the comparison of foamy oil models, which models handle wellbore-scale transitions, pore-scale vs macro-scale behavior differences
- Extract: conditions that cause foamy-to-free-gas transition (pressure, temperature, shear), timescales of coalescence, implications for separator design
- Write to `petro-roundtable/knowledge/foamy-oil-section8-draft-c2.md`

**Step 3: Opus reviews and writes Section 8**

Main session (Opus):
- Read both draft files + existing `foamy-oil-dynamics.md`
- Write Section 8: Wellbore-Scale Gas Behavior with subsections:
  - 8.1 Foamy-to-Free-Gas Transition Conditions
  - 8.2 Foamy Oil Viscosity vs GVF (SPE-136665 data)
  - 8.3 Shear Effects on Foam Stability
  - 8.4 Annular Gas Segregation at High Inclination
  - 8.5 Implications for Separator Placement
- Append Section 8 to existing KB file
- Update Source Papers table with new papers

**Step 4: Commit**

```bash
git add petro-roundtable/knowledge/foamy-oil-dynamics.md
git commit -m "feat(kb): add Section 8 (wellbore-scale gas behavior) to foamy-oil-dynamics.md"
```

---

## Task 4: Extract CFD Methodology Notes (Group D — 4 papers, reference only)

**Papers:**
- `White Papers/Flow Control/ICD/irani2020CFDforICD.pdf` (Irani — SAGD flashing CFD)
- `White Papers/Flow Control/CFD Flash Flow.pdf` (Le et al. — convergent-divergent nozzle CFD)
- `White Papers/Flow Control/Converging Diverging Annulus CFD.pdf` (Hoo et al. — annular flow)
- `White Papers/Flow Control/ICD/Inflow Autonomous AICD spe-218393-pa 2023.pdf` (AICD + CMG STARS)

**Output:** These are NOT distilled into a separate KB. Instead, extract key CFD methodology notes that get incorporated into `multiphase-flow-regimes.md` Section 7 (CFD Methodology) and the agent definition's simulation guidance.

**Step 1: Dispatch Sonnet subagent to scan all 4 papers**

Launch Agent with `model: "sonnet"`:
- Read first 5 pages + conclusions of each paper
- Extract ONLY: solver names, mesh strategies, turbulence models, multiphase approaches (VOF vs Eulerian vs mixture), validation methodology, grid independence findings
- For Irani: nucleation model details (how phase change is modeled)
- For AICD paper: CMG STARS simulation setup for fluid-discriminating devices
- Write a concise (max 100 lines) methodology summary to `petro-roundtable/knowledge/cfd-methodology-notes.md`

**Step 2: Opus incorporates into flow-regimes KB Section 7**

Merge relevant CFD notes into `multiphase-flow-regimes.md` Section 7. Delete the standalone notes file — it's a working document only.

**Step 3: Commit**

```bash
git add petro-roundtable/knowledge/multiphase-flow-regimes.md
git commit -m "feat(kb): add CFD methodology section from 4 flow control papers"
```

---

## Task 5: Enhance `pcp-operations.md` (Group E — 1 paper)

**Paper:** `White Papers/Multiphase Flow/95272-ms.pdf` (Bratu 2005 — PCP in multiphase conditions)

**Step 1: Dispatch Sonnet subagent to read SPE-95272**

Launch Agent with `model: "sonnet"`:
- Read full paper
- Extract: how PCPs handle gas-liquid mixtures, gas interference effects on PCP performance, foam handling, volumetric efficiency vs GVF, what happens when free gas enters the PCP
- Format as a new section for the existing `pcp-operations.md`
- Write to `petro-roundtable/knowledge/pcp-multiphase-draft.md`

**Step 2: Opus reviews and appends to `pcp-operations.md`**

Add as new Section (after existing content): "PCP Performance in Multiphase/Gas-Interfered Conditions"

**Step 3: Commit**

```bash
git add petro-roundtable/knowledge/pcp-operations.md
git commit -m "feat(kb): add multiphase PCP performance section from SPE-95272"
```

---

## Task 6: Read Clift, Grace, Weber Book — Extract Bubble Dynamics Reference Data

**Source:** `White Papers/Multiphase Flow/Bubbles, drops, and particles...pdf`

This is a 380-page reference book. We do NOT distill the whole thing. We extract the specific data needed for `bubble_dynamics.py` and the separator design calculations.

**Step 1: Dispatch Sonnet subagent to extract key chapters**

Launch Agent with `model: "sonnet"`:
- Read Chapter 2 (Shapes of Rigid and Fluid Particles) — extract shape regimes, Re/Eo/Mo diagram
- Read Chapter 5 (Spherical Fluid Particles at Low Re — Stokes regime) — extract: exact Stokes' law conditions, corrections for non-dilute systems, wall effects
- Read Chapter 7 (Ellipsoidal Fluid Particles) — extract: Grace correlation for terminal velocity, drag coefficient chart
- Read any chapter on bubbles in viscous media — extract: how viscosity affects bubble shape, rise velocity, and coalescence
- Produce a data extract (max 80 lines) with: key equations, validity ranges, correction factors
- Write to `petro-roundtable/knowledge/bubble-dynamics-reference.md`

**Step 2: Opus reviews accuracy of extracted equations**

Verify Stokes' law form, Grace correlation, Re/Eo/Mo boundaries. This reference data feeds directly into `bubble_dynamics.py`.

**Step 3: Commit**

```bash
git add petro-roundtable/knowledge/bubble-dynamics-reference.md
git commit -m "feat(kb): add bubble dynamics reference from Clift, Grace, Weber"
```

---

## Task 7: Build Calculation Scripts

**Files to create:**
- `petro-roundtable/calculations/bubble_dynamics.py`
- `petro-roundtable/calculations/critical_velocity.py`
- `petro-roundtable/calculations/separator_sizing.py`
- `petro-roundtable/calculations/flow_regime.py`

**Step 1: Write `bubble_dynamics.py`**

Opus writes this script using data from:
- `bubble-dynamics-reference.md` (Clift, Grace, Weber equations)
- `foamy-oil-dynamics.md` Section 8 (foamy oil viscosity data)
- `downhole-separation.md` (Stokes' law application context)

Requirements:
- CLI interface: `python bubble_dynamics.py --viscosity 80000 --density_oil 997 --density_gas 0.8 --bubble_diameter 2.0 --temperature 24`
- Outputs: bubble rise velocity (m/s), Stokes vs Grace regime indicator, Reynolds number, time to rise 1m
- Include foamy oil viscosity correction (if GVF provided)
- Print human-readable text (agents read stdout)

**Step 2: Write `critical_velocity.py`**

Based on Nagoo SPE-190921 equation:
- CLI: `python critical_velocity.py --casing_id 196.9 --tubing_od 73.0 --inclination 86 --oil_sg 0.99 --gas_sg 0.65 --water_cut 0.4`
- Outputs: critical gas velocity (m/s and ft/s), liquid loading risk (yes/no at given gas rate), recommended separator placement zone

**Step 3: Write `separator_sizing.py`**

Based on WhaleShark + McCoy design principles:
- CLI: `python separator_sizing.py --casing_id 196.9 --liquid_rate 190 --gor 10 --oil_viscosity 80000 --inclination 86 --separator_type whaleshark`
- Outputs: required cross-sectional area, minimum separator length, residence time, expected separation efficiency, recommended separator type comparison table

**Step 4: Write `flow_regime.py`**

Based on Barnea (1987) + Taitel-Dukler (1976):
- CLI: `python flow_regime.py --casing_id 196.9 --tubing_od 73.0 --liquid_rate 190 --gas_rate 1.9 --oil_viscosity 80000 --inclination 86`
- Outputs: predicted flow regime, superficial gas velocity, superficial liquid velocity, liquid holdup, whether slug/churn flow reversals are expected

**Step 5: Run all 4 scripts with OBE reference well parameters to verify**

```bash
python calculations/bubble_dynamics.py --viscosity 80000 --density_oil 997 --density_gas 0.8 --bubble_diameter 2.0 --temperature 24
python calculations/critical_velocity.py --casing_id 196.9 --tubing_od 73.0 --inclination 86 --oil_sg 0.99 --gas_sg 0.65 --water_cut 0.4
python calculations/separator_sizing.py --casing_id 196.9 --liquid_rate 190 --gor 10 --oil_viscosity 80000 --inclination 86
python calculations/flow_regime.py --casing_id 196.9 --tubing_od 73.0 --liquid_rate 190 --gas_rate 1.9 --oil_viscosity 80000 --inclination 86
```

Verify outputs are physically reasonable. Bubble rise velocity in 80,000 cP oil should be VERY slow (order of mm/s for small bubbles).

**Step 6: Commit**

```bash
git add petro-roundtable/calculations/bubble_dynamics.py petro-roundtable/calculations/critical_velocity.py petro-roundtable/calculations/separator_sizing.py petro-roundtable/calculations/flow_regime.py
git commit -m "feat(calc): add 4 multiphase flow calculation scripts"
```

---

## Task 8: Build the Agent Definition (`multiphase-flow.md`)

**File:** `petro-roundtable/agents/multiphase-flow.md`

**Step 1: Opus writes the agent definition**

Follow the template pattern from `geoscientist.md`:
- Frontmatter: name, agent_id, description, model, tools, knowledge (6 KBs), gemini_review
- Identity paragraph (from design doc Section 1)
- Domain sections with specific data tables (populated from the KBs we just built)
- Bluesky-specific application context
- Response protocol (7-step, matching other agents)
- Gemini peer review triggers
- Available data section (file paths)
- Available calculations (4 new scripts + existing 3)
- Calculation gaps (flagged for future)
- 5 validation questions

**Step 2: Write 5 validation questions**

1. "What flow regime would you predict at 86 deg inclination with 190 bbl/d liquid and 10 scf/bbl GOR in 8-5/8 inch casing?"
2. "Calculate the bubble rise velocity in 80,000 cP Bluesky bitumen for a 2mm diameter gas bubble."
3. "Compare Poor-boy, Packer-style, and WhaleShark separators for OBE's 86 deg horizontal wells — which do you recommend and why?"
4. "Where should the separator be placed relative to the foamy-oil to free-gas transition zone? Above or below?"
5. "Design the BHA stack for an OBE Bluesky well with WellFi sonde + downhole separator + PCP — specify the physical arrangement and annular clearances."

**Step 3: Commit**

```bash
git add petro-roundtable/agents/multiphase-flow.md
git commit -m "feat(agent): add multiphase-flow specialist — 10th petro-roundtable agent"
```

---

## Task 9: Update System Files

**Step 1: Update `petro-roundtable/CONFIG.md`**

- Add Multiphase Flow to Agent Roster table
- Add to Knowledge Base Inventory table (3 new KBs + 1 reference)
- Add to Calculation Script Inventory (4 new scripts)
- Update phase status: Phase 3.75 in progress

**Step 2: Update `petro-roundtable/CLAUDE.md`**

- Add agent to directory structure
- Add new KBs to directory listing
- Add new calculation scripts

**Step 3: Update `ask-engineer` skill routing**

- Add multiphase-flow to the specialist routing table
- Route keywords: "flow regime", "separator", "bubble", "multiphase", "slug flow", "liquid loading", "gas separation", "BHA stack", "annular flow"

**Step 4: Commit**

```bash
git add petro-roundtable/CONFIG.md petro-roundtable/CLAUDE.md petro-roundtable/skills/ask-engineer/
git commit -m "feat(system): register multiphase-flow specialist in CONFIG, CLAUDE.md, ask-engineer"
```

---

## Task 10: Validate Agent — 5 Questions + Gemini Audit

**Step 1: Run all 5 validation questions through the agent**

Invoke the agent definition and ask each question. Verify:
- Answers cite specific KB sections and paper numbers
- Calculations are physically reasonable
- Agent correctly defers to other specialists when appropriate
- Response protocol is followed (7 steps)

**Step 2: Gemini 3.1 Pro audit**

```
Ask Gemini: "Review this new Multiphase Flow Specialist agent for a petroleum engineering roundtable focused on Peace River Bluesky heavy oil. The agent specializes in downhole gas-liquid separation, wellbore flow regimes, and bubble dynamics at 80,000+ cP viscosity. Here are its 5 validation Q&A pairs: [paste]. What gaps do you see? What would a real multiphase flow engineer challenge in these answers?"
```

**Step 3: Fix any gaps identified by validation or Gemini**

**Step 4: Final commit**

```bash
git add -A petro-roundtable/
git commit -m "feat(roundtable): Phase 3.75 complete — multiphase flow specialist validated"
```

---

## Task 11: Create `separator-design` Skill (Optional — after validation)

**File:** `petro-roundtable/skills/separator-design/SKILL.md`

Guided workflow skill:
1. Input: well conditions (casing size, inclination, production rate, GOR, oil viscosity)
2. Run `flow_regime.py` → identify flow regime
3. Run `bubble_dynamics.py` → calculate bubble rise velocity
4. Run `critical_velocity.py` → determine liquid loading risk
5. Run `separator_sizing.py` → size the separator
6. Present recommendation with comparison table
7. Generate BHA stack diagram description

**Step 1: Write the skill definition**
**Step 2: Test with OBE reference well parameters**
**Step 3: Commit**

---

## Execution Notes

**Parallelism opportunities:**
- Task 1 Steps 1-3 can run in parallel (3 Sonnet subagents reading different papers)
- Task 2 Steps 1-3 can run in parallel (3 Sonnet subagents)
- Task 3 Steps 1-2 can run in parallel (2 Sonnet subagents)
- Task 4 Step 1 can run in parallel with Tasks 1-3
- Task 5 Step 1 can run in parallel with Tasks 1-3
- Task 6 Step 1 can run in parallel with Tasks 1-3
- Tasks 7-11 are sequential (depend on KB completion)

**Maximum parallelism:** Tasks 1-6 (KB distillation) can all start simultaneously with up to 11 Sonnet subagents. Opus review gates (Step 4 in each task) are sequential checkpoints.

**Estimated token usage:**
- Each paper read by Sonnet: ~20K input tokens + ~5K output tokens
- 22 papers total: ~550K tokens for Sonnet subagents
- Opus review passes: ~100K tokens
- Agent definition + scripts: ~50K tokens
- **Total estimate: ~700K tokens** (mostly Sonnet-tier pricing)

**Deferred papers reminder:**
- [ ] SPE-215112 (2023 separator review) — incorporate into downhole-separation.md when acquired
- [ ] Shroud-type separator (JPT 2021) — incorporate into downhole-separation.md Section 5 when acquired
