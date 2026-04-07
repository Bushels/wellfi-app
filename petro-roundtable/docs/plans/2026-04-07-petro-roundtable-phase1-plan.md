# Petro-Roundtable Phase 1: Bluesky Formation Mastery — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Geoscientist agent with deep Bluesky Formation expertise, curated knowledge base, and Gemini 3.1 peer review — the foundation for all subsequent roundtable phases.

**Architecture:** Claude Code native agent definition (.md) with formation knowledge base, connected to existing production data files and Gemini CLI MCP. The agent reads files directly (not injected context), uses WebSearch for SPE papers, and invokes Gemini 3.1 for peer review on significant analysis.

**Tech Stack:** Claude Code agents (.md definitions), Markdown knowledge bases, existing CSV/GeoJSON data, Gemini CLI MCP (`mcp__gemini-cli__ask-gemini`), Python calculation scripts (Bash tool).

**Design Doc:** `docs/plans/2026-04-07-petro-roundtable-design.md`

**Mastery Sequence:** This is Phase 1 of 7. Nothing else begins until this phase passes all 10 validation questions.

---

## Task 1: Create Directory Scaffold

**Files:**
- Create: `petro-roundtable/ROUNDTABLE.md`
- Create: `petro-roundtable/CONFIG.md`
- Create: `petro-roundtable/agents/` (directory)
- Create: `petro-roundtable/operators/` (directory)
- Create: `petro-roundtable/knowledge/` (directory)
- Create: `petro-roundtable/skills/` (directory)
- Create: `petro-roundtable/calculations/` (directory)
- Create: `petro-roundtable/mcp/` (directory)

**Step 1: Create the directory structure**

```bash
mkdir -p petro-roundtable/{agents,operators,knowledge,skills,calculations,mcp}
```

**Step 2: Create ROUNDTABLE.md — Master Identity**

This replaces hermes `SOUL.md`. It is the system prompt backbone loaded by all agents. Contains the 10 core operating principles adapted for Claude Code (show your work, field units, cite sources, flag uncertainty, calculate don't approximate, think in systems, read the data, Peace River first, regulatory awareness, safety non-negotiable).

Key differences from SOUL.md:
- References Claude Code tools (Read, Grep, WebSearch, Bash) not hermes skill functions
- Includes Gemini peer review protocol
- References formation knowledge base paths
- Includes model configuration reference

**Step 3: Create CONFIG.md — Model & Agent Configuration**

```markdown
---
default_model: claude-opus-4-6
mythos_model: claude-mythos
gemini_deep: gemini-3.1-pro
gemini_fast: gemini-3.1-flash
formation_focus: Bluesky
active_phase: 1
---
```

Lists all agents with their model assignments, active/inactive status, and phase.

**Step 4: Commit**

```bash
git add petro-roundtable/
git commit -m "feat: scaffold petro-roundtable directory structure"
```

---

## Task 2: Curate Bluesky Formation Knowledge Base

**Files:**
- Read: `Data/geological/Bluesky Geology.md` (13,000+ token source)
- Read: web research results (from brainstorming session)
- Create: `petro-roundtable/knowledge/bluesky-formation.md`

**Step 1: Read the existing Bluesky Geology.md**

This is the primary source. It contains 11+ sections covering stratigraphy, depositional environment, lithology, facies hierarchy, petrophysics, fluid properties, volumetrics, production methods, challenges, and future EOR.

**Step 2: Curate into structured knowledge base**

The knowledge base must be structured for agent consumption — not a research paper but a quick-reference that an agent can scan to find specific data points. Organize into these sections:

```markdown
# Bluesky Formation — Knowledge Base
## Quick Reference Table
(API gravity, porosity, permeability, depth, thickness, OOIP, trap type — one table)

## 1. Stratigraphic Position
(Fort St. John Group, overlain by Wilrich/Spirit River, underlain by Gething/Ostracode)

## 2. Depositional Environment
(Transgressive estuarine complex, Boreal Sea, facies hierarchy)

## 3. Reservoir Properties by Facies
(Table: Tidal-Inlet 28%, Barrier-Bar 26.6%, Flood-Tidal Delta 27%, etc.)

## 4. Fluid Properties
(API 8-16°, viscosity gradient 80,000 cP top → 1,750,000 cP base, mobility)

## 5. Trapping Mechanism
(Stratigraphic: Wilrich cap rock, estuarine pinchout, bottom water)

## 6. Production Methods
(Primary cold-flow, CHOPS, CSS, SAGD limited, VSD pilot, waterflood EOR)

## 7. Key Operators
(Obsidian, CNRL, Baytex, Headwater — with field names and production methods)

## 8. Challenges
(Sand production, foamy oil, bottom water, shale baffles, wellbore integrity)

## 9. Key Data Points for Calculations
(OOIP formula inputs, recovery factors by method, SOR ranges, break-even prices)

## 10. Data File Locations
(CSV paths, GeoJSON paths, where to find production data)
```

Include the vertical viscosity gradient data (80,000 cP top → 1,750,000 cP base over 32m), the oil mobility calculation (0.017 → 0.000030 mD/cP), and the facies porosity table — these are the unique data points that differentiate a knowledgeable agent from a generic one.

**Step 3: Verify all data points against source**

Cross-check every number in the knowledge base against `Bluesky Geology.md` and the web research. Flag any conflicts.

**Step 4: Commit**

```bash
git add petro-roundtable/knowledge/bluesky-formation.md
git commit -m "feat: curate Bluesky formation knowledge base from geology reference"
```

---

## Task 3: Build the Geoscientist Agent

**Files:**
- Read: `hermes-petro-agents/agents/geoscientist.md` (source to adapt)
- Read: `hermes-petro-agents/SOUL.md` (operating principles)
- Create: `petro-roundtable/agents/geoscientist.md`

**Step 1: Read the hermes geoscientist agent and SOUL.md**

Understand the domain, operational context, and response protocol.

**Step 2: Write the Claude Code native geoscientist agent**

Key adaptations from hermes:
- Add `tools: [Read, Grep, Glob, WebSearch, WebFetch, Bash]` — the agent can read files
- Add `mcp: [gemini-cli]` — the agent can invoke Gemini for peer review
- Add `knowledge: [bluesky-formation.md]` — explicit knowledge base reference
- Add `model: claude-opus-4-6` — explicit model for Mythos migration
- Expand Bluesky Formation expertise (hermes version was Clearwater-heavy, thin on Bluesky)
- Add `Available Data` section listing exact file paths to CSVs and GeoJSON
- Add `Gemini Peer Review Triggers` section
- Add Peace River specific context (depths, temperatures, operators, fields)
- Include the facies hierarchy, viscosity gradient, and oil mobility data
- Reference Bluesky-specific log signatures (different from Clearwater)

The agent identity: "Senior Geoscientist (geologist + petrophysicist) with 25+ years in Western Canada heavy oil and oil sands, with deep specialization in the Bluesky Formation at Peace River."

**Step 3: Verify agent references valid file paths**

Ensure every file path in the "Available Data" section actually exists.

**Step 4: Commit**

```bash
git add petro-roundtable/agents/geoscientist.md
git commit -m "feat: create Claude Code native geoscientist agent with Bluesky expertise"
```

---

## Task 4: Build the /bluesky-briefing Skill

**Files:**
- Create: `petro-roundtable/skills/bluesky-briefing/SKILL.md`

**Step 1: Write the skill definition**

This skill is the first test of the knowledge base + agent combination. When invoked, it:
1. Loads the Bluesky knowledge base
2. Spawns the geoscientist agent
3. Produces a structured formation briefing covering all 10 sections
4. Optionally invokes Gemini for a "what are we missing?" audit

```markdown
---
name: bluesky-briefing
description: "Deep-dive Bluesky Formation briefing for petroleum engineering training and onboarding. Use when the user wants to understand the Bluesky Formation, asks about Peace River geology, or needs formation context for engineering decisions."
---
```

**Step 2: Test the skill manually**

Invoke the skill and verify it produces a comprehensive briefing that:
- Covers all 10 knowledge base sections
- Cites specific data points (not generic statements)
- References file paths where agents can find more data
- Includes the viscosity gradient, facies hierarchy, and oil mobility data

**Step 3: Commit**

```bash
git add petro-roundtable/skills/bluesky-briefing/
git commit -m "feat: create /bluesky-briefing skill for formation deep-dive"
```

---

## Task 5: Build the /ask-engineer Skill

**Files:**
- Create: `petro-roundtable/skills/ask-engineer/SKILL.md`

**Step 1: Write the skill definition**

This skill routes a question to a single specialist agent:

```
/ask-engineer geoscientist "What are typical porosity ranges for Bluesky tidal-inlet facies?"
```

The skill:
1. Parses the specialty name from the first argument
2. Finds the matching agent in `petro-roundtable/agents/`
3. Spawns the agent with the question as prompt
4. Returns the agent's response

For Phase 1, only `geoscientist` is available. The skill should gracefully handle requests for agents that don't exist yet: "The [specialty] agent is not yet available. Available specialists: geoscientist."

**Step 2: Commit**

```bash
git add petro-roundtable/skills/ask-engineer/
git commit -m "feat: create /ask-engineer skill for single-agent queries"
```

---

## Task 6: Migrate Python Calculation Scripts

**Files:**
- Read: `hermes-petro-agents/skills/decline_curves/decline_curves.py`
- Read: `hermes-petro-agents/skills/nodal_analysis/nodal_analysis.py`
- Read: `hermes-petro-agents/skills/sand_control/sand_control.py`
- Create: `petro-roundtable/calculations/decline_curves.py`
- Create: `petro-roundtable/calculations/nodal_analysis.py`
- Create: `petro-roundtable/calculations/sand_control.py`

**Step 1: Read the hermes Python scripts**

Understand the function signatures, inputs, outputs, and engineering logic.

**Step 2: Copy and adapt for standalone execution**

The hermes scripts were designed to be imported as modules. For Claude Code, they need to work as standalone CLI scripts invokable via Bash:

```bash
python petro-roundtable/calculations/decline_curves.py \
  --mode arps_fit \
  --qi 100 --di 0.15 --b 1.2 --time_months 60
```

Each script should:
- Accept command-line arguments (argparse)
- Print results as formatted text (not JSON — agents read text)
- Include usage help (`--help`)
- Handle missing dependencies gracefully (numpy, scipy)

**Step 3: Test each script runs**

```bash
python petro-roundtable/calculations/decline_curves.py --help
python petro-roundtable/calculations/nodal_analysis.py --help
python petro-roundtable/calculations/sand_control.py --help
```

**Step 4: Commit**

```bash
git add petro-roundtable/calculations/
git commit -m "feat: migrate petroleum engineering calculation scripts from hermes"
```

---

## Task 7: Validation — 10 Bluesky Questions

**Files:**
- Read: All files created in Tasks 1-6
- No files created — this is a validation step

**Step 1: Run through all 10 validation questions**

Using `/ask-engineer geoscientist`, test each question:

1. "What is the depositional environment of the Bluesky Formation?"
   - Expected: transgressive estuarine complex, Boreal Sea, incised valley fill, tidal channels
   - Must cite: knowledge base section 2

2. "What are typical porosity and permeability ranges for Bluesky reservoir sands?"
   - Expected: 20-30% porosity (avg 26%), up to Darcy-scale in clean channels
   - Must cite: facies table from knowledge base section 3

3. "Why is SAGD less common than CSS in the Bluesky?"
   - Expected: shale baffles limit vertical steam rise, bottom water, CSS better suited
   - Must reference: knowledge base sections 6 and 8

4. "Explain the foamy oil mechanism in Peace River CHOPS wells."
   - Expected: dissolved gas exsolves below bubble point, metastable foam, wormholes
   - Must reference: knowledge base section 6 (CHOPS) and section 8 (foamy oil)

5. "What is the vertical viscosity gradient in the Bluesky and why does it matter?"
   - Expected: 80,000 cP top → 1,750,000 cP base (22x over ~32m), mobility 0.017 → 0.000030 mD/cP
   - Must cite: exact numbers from knowledge base section 4

6. "How does bottom water affect Bluesky production?"
   - Expected: mobile below 65% So, high water cuts, steam invasion, handling costs
   - Must reference: knowledge base section 8

7. "Compare Bluesky tidal-inlet facies vs bayhead delta facies for reservoir quality."
   - Expected: tidal-inlet 28% porosity (highest quality), bayhead delta 26.5% (moderate)
   - Must cite: facies table with BIP estimates

8. "What is the cap rock for the Bluesky and how competent is it?"
   - Expected: Wilrich Member of Spirit River Formation, marine shale, high quality seal
   - Must reference: knowledge base section 5

9. "Calculate OOIP for a 160-acre Bluesky section at 15m pay, 26% porosity, 65% So."
   - Expected: agent uses volumetric formula, shows work, gives answer in barrels
   - Should invoke calculation or do it inline with units

10. "What SPE papers are most relevant to Bluesky formation evaluation?"
    - Expected: agent uses WebSearch to find relevant SPE papers, cites by number
    - Must include at least 3 specific SPE paper references

**Step 2: Score each response**

For each question, evaluate:
- [ ] Factually correct (matches knowledge base and web research)
- [ ] Cites data sources (file paths, knowledge base sections, or web results)
- [ ] Shows confidence level (high/medium/low)
- [ ] Identifies what additional data would improve the answer
- [ ] No hallucinated numbers or references

**Step 3: Identify gaps and fix**

For any question that fails:
1. Identify whether the gap is in the knowledge base, agent prompt, or tool usage
2. Fix the specific issue
3. Retest that question
4. Verify fix didn't break other questions

**Step 4: Gemini knowledge audit**

After all 10 questions pass, invoke Gemini 3.1 Pro:

```
We built an AI geoscientist agent specialized in the Bluesky Formation
at Peace River, Alberta. It passed these 10 validation questions:
[list questions]

What critical aspects of Bluesky Formation geology and petrophysics
are we likely missing? What would a real geoscientist working Peace
River want the agent to know that isn't covered? List 5-7 items
ranked by importance for petroleum engineering decisions.
```

**Step 5: Incorporate valid Gemini feedback**

Update knowledge base and/or agent prompt with any valid gaps Gemini identifies. Retest affected questions.

**Step 6: Commit final validated state**

```bash
git add petro-roundtable/
git commit -m "feat: Phase 1 complete — Bluesky formation mastery validated"
```

---

## Task 8: Phase 1 Completion Gate

**Checklist — Phase 1 is COMPLETE when:**

- [ ] `petro-roundtable/` directory structure exists with all required subdirectories
- [ ] `ROUNDTABLE.md` contains adapted operating principles for Claude Code
- [ ] `CONFIG.md` contains model assignments with Mythos placeholder
- [ ] `knowledge/bluesky-formation.md` covers all 10 sections with cited data points
- [ ] `agents/geoscientist.md` is Claude Code native with tools, MCP, and knowledge refs
- [ ] `skills/bluesky-briefing/SKILL.md` produces comprehensive formation briefing
- [ ] `skills/ask-engineer/SKILL.md` routes to geoscientist correctly
- [ ] `calculations/` has at least decline_curves.py, nodal_analysis.py, sand_control.py
- [ ] All 10 validation questions pass with data citations
- [ ] Gemini 3.1 Pro knowledge audit finds no critical gaps
- [ ] All files committed to `codex/bluesky-clearwater-import` branch

**Next Phase:** Phase 2 — Obsidian Energy Operator Mastery
