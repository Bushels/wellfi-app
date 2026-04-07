# Petroleum Engineering Roundtable — Design Document

**Date:** 2026-04-07
**Status:** Approved
**Branch:** codex/bluesky-clearwater-import
**Approach:** Claude Code Native (Approach B)

---

## 1. Vision

Build a panel of petroleum engineering expert agents — native to Claude Code — that can be invoked individually or as a roundtable to analyze Bluesky/Clearwater/McMurray formation questions with real data, operator context, and multi-model intelligence hardening.

The system replaces the external Hermes/GPT-5.4 roundtable-bridge with a fully native Claude Code architecture that leverages built-in tools (Read, Grep, WebSearch, Bash), MCP integrations (StackDX, Gemini CLI), and the Claude Agent SDK.

## 2. Mastery Sequence

Depth before breadth. Each layer is perfected before stacking the next.

```
Phase 1: BLUESKY FORMATION MASTERY
  └─ Geoscientist agent + knowledge base + validation
  └─ Test: Can it answer any Bluesky geology question with data citations?
  └─ Iterate until perfect

Phase 2: OBSIDIAN ENERGY OPERATOR MASTERY
  └─ Obsidian Energy operator agent + business intelligence
  └─ Test: Can it explain how OBE operates, their costs, their technology?
  └─ Iterate until perfect

Phase 3: ENGINEERING PANEL ACTIVATION
  └─ Remaining 8 specialist agents built and tested individually
  └─ Test: Each agent passes domain-specific validation questions
  └─ Iterate until perfect

Phase 4: ROUNDTABLE ORCHESTRATION
  └─ /roundtable skill wires agents together with parallel execution
  └─ Gemini challenge rounds integrated
  └─ Test: Multi-agent consensus on complex cross-discipline questions
  └─ Iterate until perfect

Phase 5: STACKDX MCP + DATA LAYER
  └─ StackDX MCP server for live well data queries
  └─ Production data integration, drilling activity tracking
  └─ Test: Agents can query real well data and cite it in analysis
  └─ Iterate until perfect

Phase 6: OPERATOR EXPANSION
  └─ CNRL Peace River, Baytex, Headwater, Tamarack, Spur, etc.
  └─ Each operator rep tested against public filings and production data
  └─ Test: Operator reps provide accurate, actionable operational context
  └─ Iterate until perfect

Phase 7: FORMATION EXPANSION
  └─ Clearwater, McMurray knowledge bases
  └─ Cross-formation comparison capabilities
  └─ Iterate until perfect
```

**The rule:** No phase begins until the previous phase works synergistically — agents, skills, plugins, data, everything tuned and validated.

## 3. Architecture

```
petro-roundtable/
├── ROUNDTABLE.md                    # Master identity (replaces hermes SOUL.md)
├── CONFIG.md                        # Model config, active agents, formation focus
│
├── agents/                          # Claude Code native agent definitions
│   ├── geoscientist.md              # Geology, petrophysics, formation evaluation
│   ├── reservoir-engineer.md        # Recovery, PVT, decline curves, SAGD chamber
│   ├── drilling-engineer.md         # Well planning, casing, directional, cementing
│   ├── well-performance.md          # Completions, sand control, artificial lift
│   ├── geomechanics.md              # Stability, sand prediction, cap rock, stress
│   ├── facilities-engineer.md       # Surface facilities, steam, separation, water
│   ├── economics-reserves.md        # NPV, reserves, royalties, pricing, decisions
│   ├── simulation-engineer.md       # CFD, FEA, multiphase, thermal, erosion
│   └── production-data.md           # SCADA, analytics, dashboards, data quality
│
├── operators/                       # Operator representative agents
│   ├── _template.md                 # Template for creating new operator reps
│   ├── obsidian-energy.md           # Phase 2 — first operator, deep mastery
│   ├── cnrl-peace-river.md          # Phase 6
│   ├── baytex-energy.md             # Phase 6
│   ├── headwater-exploration.md     # Phase 6
│   ├── tamarack-valley.md           # Phase 6
│   └── spur-petroleum.md            # Phase 6
│
├── knowledge/                       # Curated formation knowledge bases
│   ├── bluesky-formation.md         # Phase 1 — curated from geology + research
│   ├── clearwater-formation.md      # Phase 7
│   └── mcmurray-formation.md        # Phase 7
│
├── skills/                          # Claude Code invokable skills
│   ├── roundtable/SKILL.md          # /roundtable — full panel discussion
│   ├── ask-engineer/SKILL.md        # /ask-engineer <specialty> — single agent
│   ├── ask-operator/SKILL.md        # /ask-operator <name> — single operator rep
│   └── bluesky-briefing/SKILL.md    # /bluesky-briefing — formation deep-dive
│
├── mcp/                             # MCP servers
│   └── stackdx-server/              # Phase 5 — StackDX data access
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
│           ├── index.ts             # MCP server entry point
│           └── tools/
│               ├── query-wells.ts   # Filter/query cached well data
│               ├── operator-stats.ts
│               ├── formation-stats.ts
│               ├── well-detail.ts
│               └── refresh-data.ts  # Trigger StackDX re-pull
│
└── calculations/                    # Python engineering calculations
    ├── decline_curves.py            # Arps decline, EUR, type curves
    ├── nodal_analysis.py            # IPR, VLP, operating point
    ├── sand_control.py              # PSD analysis, screen selection
    ├── esp_design.py                # ESP sizing, power, temperature
    └── wellbore_hydraulics.py       # Pressure drop, erosional velocity
```

## 4. Agent Design — Claude Code Native

### 4.1 Key Differences from Hermes Agents

| Aspect | Hermes (old) | Claude Code Native (new) |
|--------|-------------|-------------------------|
| I/O model | Text-in, text-out via CLI subprocess | Full tool access (Read, Grep, WebSearch, Bash) |
| Data access | None — had to be injected as context | Agents read files, query StackDX MCP, search web |
| Calculations | Python skill functions via import | Bash tool invokes Python scripts directly |
| Peer review | None | Gemini CLI MCP for second opinions |
| Model | GPT-5.4 (Hermes/Nous) | Claude Opus 4.6 → Claude Mythos |
| Orchestration | Lead Engineer text router | Claude Code Agent tool with parallel execution |
| Formation data | Manual context injection | Auto-loaded from knowledge/ directory |

### 4.2 Agent Definition Format

Each agent `.md` file follows this structure:

```markdown
---
agent_id: <unique-id>
model: claude-opus-4-6
tools: [Read, Grep, Glob, WebSearch, WebFetch, Bash]
mcp: [stackdx-server, gemini-cli]
knowledge: [bluesky-formation.md]
gemini_review: true
---

# <Title> — Petroleum Engineering Roundtable

<System prompt: identity, domain expertise, 25+ years experience>

## Domain
<Bullet list of specific expertise areas>

## Operational Context
<Formation-specific knowledge, operator familiarity, regulatory awareness>

## Available Data
<File paths and MCP tools this agent should use>

## Available Calculations
<Python scripts this agent can invoke via Bash>

## Response Protocol
1. State the engineering question clearly
2. Read relevant data files before answering (don't guess)
3. Show calculations with assumptions
4. Cite specific data points from files or web sources
5. State confidence level (high/medium/low) and what data would improve it
6. After significant analysis, invoke Gemini for peer review
7. Flag when another specialist should weigh in

## Gemini Peer Review Triggers
- Complex interpretations with limited data
- Recommendations that affect safety or significant capital
- When two approaches seem equally viable
- When the question crosses into another agent's domain
```

### 4.3 Core Operating Principles (from ROUNDTABLE.md)

Adapted from hermes SOUL.md for Claude Code:

1. **Show your work.** Equations, assumptions, inputs, units.
2. **Field units by default.** bbl/d, psi, ft, F, cp, mD. SI for AER submissions.
3. **Cite your sources.** SPE papers by number, API standards by designation, AER guidelines by ID. WebSearch to find them.
4. **Flag uncertainty explicitly.** State what additional data would narrow the range.
5. **Calculate, don't approximate.** Invoke Python scripts via Bash. Flag skill gaps.
6. **Think in systems.** Reservoir + wellbore + completion + facilities + economics are connected.
7. **Read the data.** Never guess when you can Read a file or query StackDX.
8. **Peace River first.** Default context is Peace River heavy oil (Bluesky/Clearwater). Ask if context is different.
9. **Regulatory awareness.** AER Directives 060, 056, 017, 086. Saskatchewan SMRID.
10. **Safety is non-negotiable.** H2S, wellbore integrity, pressure containment risks are flagged immediately.

## 5. Model Configuration

### 5.1 Claude Models

```yaml
# CONFIG.md model assignments
default_model: claude-opus-4-6        # Current production model
mythos_model: claude-mythos            # Update ID when Anthropic publishes it

# Per-agent overrides (optional)
agents:
  geoscientist: claude-opus-4-6       # First to test on Mythos (Phase 1)
  reservoir-engineer: claude-opus-4-6
  # ... all others default
```

**Mythos Migration Strategy:**
- When Claude Mythos model ID is published, update `CONFIG.md`
- Test geoscientist agent first (Phase 1 agent, most validated)
- Run comparison: same Bluesky question on Opus 4.6 vs Mythos
- If Mythos passes quality bar, roll forward agent-by-agent
- Support mixed panels during transition (Mythos for tested agents, Opus for untested)

### 5.2 Gemini Models

```yaml
gemini:
  deep_review: gemini-3.1-pro         # Architecture review, complex analysis
  quick_check: gemini-3.1-flash       # Factual lookups, quick second opinions
  default: gemini-3.1-flash           # Default to fast for most agent reviews
```

**Gemini Integration Tiers:**

| Tier | When | Gemini Model | Prompt Pattern |
|------|------|-------------|----------------|
| Agent-level | Individual agent wants a second opinion | 3.1 Flash | Focused question about its own analysis |
| Roundtable challenge | After all agents respond | 3.1 Pro | "The panel recommends X. What risks are underweighted?" |
| Devil's advocate | User requests `--challenge` | 3.1 Pro | Gemini argues against the consensus |
| Knowledge audit | After completing a phase | 3.1 Pro | "What are we missing about [topic]?" |

## 6. Operator Representative Design

### 6.1 Obsidian Energy — Deep Mastery (Phase 2)

The Obsidian Energy agent is the prototype operator rep. It must achieve mastery across:

**Business Intelligence:**
- Corporate strategy (capital discipline, 60-70% payout ratio, share buybacks)
- Asset portfolio (680+ net sections, Peace River focus)
- Production profile (current rates, decline, growth plans)
- Financial metrics (break-even, netback, F&D costs, recycle ratio)
- Competitive positioning vs Baytex, Headwater, CNRL in Peace River

**Operational Knowledge:**
- Cold-flow horizontal well design (multi-leg, pad drilling)
- "Waffle well" multilateral innovation (2025 pilot)
- Waterflood EOR pilots (2024-2025, which fields, results)
- No thermal — and WHY (Bluesky viscosity at 550m is low enough for primary)
- Drilling program cadence (5 rigs, 16 wells H1 2025)

**Field-Level Detail:**
- Harmon Valley South (HVS) — flagship, production history, well count
- Walrus — new discovery, exploration results, upside potential
- Township/range coverage across Peace River

**Technology:**
- WellFi deployment (first tool deployed in Bluesky — our product)
- Monitoring philosophy, pump optimization approach
- How they use data for well intervention decisions

**Data Sources:**
- StackDX MCP for well-level production data
- Public filings (TSX:OBE investor presentations, MD&A, AIF)
- AER well data and regulatory filings
- WebSearch for press releases, analyst reports

### 6.2 Operator Rep Template

```markdown
---
agent_id: operator-<slug>
model: claude-opus-4-6
type: operator-representative
operator_name: <Legal Name>
ticker: <Exchange:Symbol>
formation_focus: [Bluesky, Clearwater]
production_method: [cold-flow horizontal, CSS, SAGD, CHOPS]
headquarters: <City, Province>
tools: [Read, Grep, Glob, WebSearch, WebFetch, Bash]
mcp: [stackdx-server, gemini-cli]
---

# <Operator Name> — Operator Representative

You represent <Operator>'s operational perspective. You understand their
specific approach, their fields, their technology, and their economics.

## Operating Philosophy
<How this company approaches heavy oil development>

## Key Fields
<Major production areas with township/range references>

## Production Profile
<Current rates, well counts, growth/decline trajectory>

## Technology & Methodology
<Drilling/completion/recovery approach, innovations, monitoring>

## Financial Profile
<Break-even, netback, capital allocation philosophy>

## Competitive Position
<How they compare to peers in the same play>

## Data Sources
- StackDX: stackdx_operator_stats({ operator_name: "<Name>" })
- GeoJSON: wellfi-app/public/data/operators/<slug>/production.geojson
- Investor deck: <URL>
- AER filings: <relevant directive filings>

## When This Rep Adds Value
<Specific question types where this operator's perspective matters>
```

## 7. StackDX MCP Server Design

### 7.1 Architecture: Cache + Refresh

The MCP server manages local CSV data and provides structured query tools.

```
CSV Files (Data/*.csv)
    ↓ parse on startup
In-Memory Queryable Store
    ↓ exposed via
MCP Tools → Agents query structured data
    ↓ when stale
Chrome MCP refresh trigger → new CSV → reload
```

### 7.2 MCP Tools

| Tool | Input Schema | Returns |
|------|-------------|---------|
| `stackdx_query_wells` | `{ operator?, formation?, fluid_type?, min_oil?, province?, bbox?, spud_after?, limit? }` | Array of well records matching filters |
| `stackdx_operator_stats` | `{ operator_name }` | Well count, avg production, formation breakdown, drilling activity |
| `stackdx_formation_stats` | `{ formation }` | Total wells, avg porosity/production, operator breakdown, trend |
| `stackdx_well_detail` | `{ uwi }` | Full record: location, production history, operator, status, formation |
| `stackdx_top_producers` | `{ n, formation?, operator? }` | Top N wells ranked by production rate |
| `stackdx_drilling_activity` | `{ months_back?, operator?, formation? }` | Recent spuds, completion dates, rig counts |

### 7.3 Data Sources

| File | Wells | Vintage | Use |
|------|-------|---------|-----|
| `clearwater_bluesky_feb2026_prod_imperial_canonical.csv` | ~9,189 | Feb 2026 | Primary production data |
| `clearwater_bluesky_2026_drilling_chart_full.csv` | varies | 2026 | Drilling activity |
| `operator_inventory_clearwater_bluesky.csv` | varies | varies | Operator well counts |
| Per-operator GeoJSON in `public/data/operators/` | varies | varies | Spatial data |

### 7.4 Future: Direct StackDX API

If StackDX exposes a programmatic API (the `/sql` command suggests backend capabilities), the MCP tools stay the same — only the data source changes from local CSV to API calls. Agents never know the difference.

## 8. Skill Definitions

### 8.1 /roundtable

```
Orchestrates a full panel discussion:
1. Parse question, identify relevant specialists + operator reps
2. Spawn agents in parallel via Agent tool (run_in_background)
3. Collect responses
4. Send consensus to Gemini 3.1 Pro for challenge round
5. Synthesize final recommendation with:
   - Consensus view
   - Dissenting opinions
   - Gemini challenge points
   - Data gaps flagged
   - Recommended next steps

Flags:
  --challenge    Aggressive Gemini devil's advocate
  --operators    Include relevant operator reps
  --formation X  Override default formation focus
  --model X      Override default model for all agents
```

### 8.2 /ask-engineer

```
Quick single-agent query:
  /ask-engineer reservoir "What's the expected RF for Bluesky CHOPS?"
  /ask-engineer geoscientist "Describe the Bluesky depositional environment"
  /ask-engineer economics "Break-even for cold-flow horizontal at WCS $55?"
```

### 8.3 /ask-operator

```
Quick single-operator query:
  /ask-operator obsidian "What's your waffle well IP-30 performance?"
  /ask-operator cnrl "How does Carmon Creek CSS SOR compare to target?"
```

### 8.4 /bluesky-briefing

```
Deep-dive formation briefing for training/onboarding:
  - Loads full knowledge base
  - Presents structured geological overview
  - Key reservoir properties with data citations
  - Production method comparison
  - Active operators and their approaches
  - Open questions and data gaps
```

## 9. Gemini CLI Integration

### 9.1 Model Versions

- **gemini-3.1-pro** — Deep analysis, architecture review, roundtable challenges
- **gemini-3.1-flash** — Quick factual checks, agent-level peer reviews

### 9.2 Petroleum Engineering Prompt Templates

**Agent-level peer review:**
```
I'm a [specialty] analyzing [topic] in the Bluesky Formation, Peace River.
My conclusion: [X] based on [data].
What geological/engineering factors would challenge this?
Be specific to Peace River Bluesky at ~550m depth, 8 API bitumen.
```

**Roundtable challenge:**
```
A panel of petroleum engineers analyzed: "[question]"

Their consensus: [summary of recommendations]

Argue AGAINST this consensus. What are the top 3 risks they're
underweighting? What data would change their recommendation?
Focus on Peace River Bluesky operational reality.
```

**Knowledge gap audit:**
```
We just completed a deep analysis of [topic] for Bluesky heavy oil.
What common operational challenges in Peace River are we likely missing?
List 5-7 items ranked by production impact. Be specific — cite field
names, operators, or SPE papers where possible.
```

**Cross-model validation:**
```
Claude's reservoir engineer calculated [result] using [method] with
these assumptions: [list].
Verify: Are the assumptions reasonable for Bluesky Formation at
Peace River? What would you calculate differently?
```

### 9.3 Cross-Verification Rule

Gemini's claims are hypotheses, not facts. After receiving Gemini's response:
1. Factual claims → verify against data files, StackDX, or web sources
2. Engineering opinions → evaluate critically, Claude makes the decision
3. "Missing factor" suggestions → check if actually relevant to Peace River context
4. Conflicting calculations → rerun with explicit assumptions, identify the divergence

## 10. Iterative Perfection Protocol

Each phase follows the same validation loop:

```
BUILD → TEST → IDENTIFY GAPS → FIX → RETEST → VALIDATE WITH GEMINI → SHIP

Specifically:
1. Build the agent/skill/MCP component
2. Test with 5-10 domain-specific questions (easy → hard)
3. Identify where the response is:
   - Factually wrong (fix knowledge base)
   - Missing data (add data sources, fix MCP tools)
   - Poorly reasoned (fix system prompt, add examples)
   - Not citing sources (fix response protocol)
   - Inconsistent with other agents (fix cross-agent context)
4. Fix and retest
5. Send to Gemini 3.1 Pro: "What are we missing about [topic]?"
6. Incorporate valid Gemini feedback
7. Ship only when all tests pass and Gemini finds no critical gaps
```

**Phase 1 validation questions (Bluesky Formation):**
1. "What is the depositional environment of the Bluesky Formation?"
2. "What are typical porosity and permeability ranges for Bluesky reservoir sands?"
3. "Why is SAGD less common than CSS in the Bluesky?"
4. "Explain the foamy oil mechanism in Peace River CHOPS wells."
5. "What is the vertical viscosity gradient in the Bluesky and why does it matter?"
6. "How does bottom water affect Bluesky production?"
7. "Compare Bluesky tidal-inlet facies vs bayhead delta facies for reservoir quality."
8. "What is the cap rock for the Bluesky and how competent is it?"
9. "Calculate OOIP for a 160-acre Bluesky section at 15m pay, 26% porosity, 65% So."
10. "What SPE papers are most relevant to Bluesky formation evaluation?"

## 11. Migration from Hermes

### 11.1 What We Keep
- Agent domain expertise and response protocols (adapted for Claude Code tools)
- Python calculation scripts (decline_curves, nodal_analysis, sand_control, esp_design, wellbore_hydraulics)
- Bluesky Geology.md knowledge base (curated into knowledge/ format)
- Roundtable concept (parallel specialist consultation)

### 11.2 What We Replace
- Hermes CLI subprocess routing → Claude Code Agent tool
- GPT-5.4 model → Claude Opus 4.6 → Claude Mythos
- Text-only I/O → Full tool access (Read, Grep, WebSearch, Bash, MCP)
- roundtable-bridge FastAPI server → /roundtable Claude Code skill
- Lead Engineer text router → Claude Code orchestrator with parallel Agent spawning
- No peer review → Gemini 3.1 challenge rounds

### 11.3 What We Add
- Formation knowledge bases (curated, structured)
- Operator representative agents
- StackDX MCP for live well data
- Gemini multi-tier peer review
- Model migration path (Opus 4.6 → Mythos)
- Iterative perfection protocol with validation questions

## 12. Success Criteria

**Phase 1 (Bluesky Mastery) is complete when:**
- [ ] Geoscientist agent passes all 10 validation questions with data citations
- [ ] Knowledge base covers all sections from Bluesky Geology.md + web research
- [ ] Agent reads production data files when answering (not just from training)
- [ ] Gemini 3.1 Pro finds no critical gaps in a knowledge audit
- [ ] Agent correctly handles edge cases (gas wells in Deep Basin Bluesky, bitumen vs oil classification)

**Phase 2 (Obsidian Energy Mastery) is complete when:**
- [ ] Operator agent can explain OBE's operating philosophy with specifics
- [ ] Agent cites current production data from StackDX/CSVs
- [ ] Agent knows waffle well design, waterflood pilots, HVS field details
- [ ] Financial metrics are current and sourced
- [ ] Agent correctly distinguishes OBE's cold-flow approach from CNRL's thermal approach
- [ ] Gemini 3.1 Pro finds no critical gaps in an operator knowledge audit
