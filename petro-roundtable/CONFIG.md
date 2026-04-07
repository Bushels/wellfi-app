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

**Phase 1: Bluesky Formation Mastery**

## Agent Roster

| Agent | Status | Phase | Model | Domain |
|---|---|---|---|---|
| Geoscientist | **Active** | 1 | claude-opus-4-6 | Formation evaluation, petrophysics, stratigraphy, facies mapping |
| Reservoir Engineer | Planned | 3 | claude-opus-4-6 | Drainage, recovery factors, simulation, EOR |
| Drilling Engineer | Planned | 3 | claude-opus-4-6 | Well design, directional, casing, cementing |
| Well Performance | Planned | 3 | claude-opus-4-6 | Completions, sand control, artificial lift, production optimization |
| Geomechanics | Planned | 3 | claude-opus-4-6 | Rock mechanics, wellbore stability, cap rock integrity |
| Facilities Engineer | Planned | 3 | claude-opus-4-6 | Surface facilities, OTSG, separation, water treatment |
| Economics & Reserves | Planned | 3 | claude-opus-4-6 | COGEH/NI 51-101, WCS pricing, break-even analysis |
| Simulation Engineer | Planned | 3 | claude-opus-4-6 | CFD, FEA, thermal modeling, multiphase flow |
| Lead Engineer | Planned | 4 | claude-opus-4-6 | Orchestration, routing, synthesis, arbitration |

## Operator Representatives

| Operator | Status | Phase | Domain |
|---|---|---|---|
| Obsidian Energy | Planned | 2 | Peace River Bluesky — cold-flow horizontal, fishbone wells, WellFi monitoring |
| CNRL | Planned | 6 | Peace River Bluesky/Clearwater — thermal CSS, Carmon Creek |
| Baytex | Planned | 6 | Peace River Bluesky — polymer flood, Seal field |
| Headwater | Planned | 6 | Clearwater — SAGD, primary cold flow |

## Gemini Integration Tiers

1. **Agent-level** (Gemini 3.1 Flash) — Quick sanity checks during individual agent responses
2. **Roundtable challenge** (Gemini 3.1 Pro) — After panel reaches consensus, Gemini reviews
3. **Devil's advocate** (Gemini 3.1 Pro) — On `--challenge` flag, Gemini actively argues against consensus

## Mastery Sequence

1. Bluesky Formation Mastery (current)
2. Obsidian Energy Operator Mastery
3. Engineering Panel (all 9 agents)
4. Roundtable Orchestration (Lead Engineer + /roundtable skill)
5. StackDX MCP Server
6. Operator Expansion (CNRL, Baytex, Headwater)
7. Formation Expansion (Clearwater, McMurray)
