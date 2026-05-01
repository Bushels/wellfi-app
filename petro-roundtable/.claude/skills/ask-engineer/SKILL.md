---
name: ask-engineer
description: "Route a question to a specific petroleum engineering specialist agent. Usage: /ask-engineer <specialty> <question>. Available specialists are listed in petro-roundtable/CONFIG.md."
---

# Ask Engineer

Route a question to a single specialist agent from the petroleum engineering roundtable.

## Usage

```
/ask-engineer geoscientist "What are typical porosity ranges for Bluesky tidal-inlet facies?"
/ask-engineer reservoir "What recovery factor should we expect from CSS in the Bluesky?"
```

## Process

1. **Parse the request:**
   - First argument = specialty name (e.g., `geoscientist`, `reservoir`, `drilling`)
   - Remaining text = the question to ask

2. **Resolve the agent file** from the specialty name:

   The specialty short name maps to an agent file. Use the table below, or fall back to a Glob:
   ```
   Glob .claude/agents/<specialty>*.md
   ```

   | Short name | Agent file |
   |---|---|
   | `geoscientist` | `.claude/agents/geoscientist.md` |
   | `reservoir` | `.claude/agents/reservoir-engineer.md` |
   | `drilling` | `.claude/agents/drilling-engineer.md` |
   | `well-performance` | `.claude/agents/well-performance.md` |
   | `geomechanics` | `.claude/agents/geomechanics.md` |
   | `facilities` | `.claude/agents/facilities-engineer.md` |
   | `economics` | `.claude/agents/economics-reserves.md` |
   | `simulation` | `.claude/agents/simulation-engineer.md` |
   | `production-data` | `.claude/agents/production-data.md` |
   | `multiphase-flow` | `.claude/agents/multiphase-flow.md` |
   | `lead` | `.claude/agents/lead-engineer.md` |

   If the agent file does not exist, respond:
   > "The **[specialty]** agent is not yet available. Available specialists: [list agents found in .claude/agents/]."

3. **Load the specialist agent:**
   ```
   Read petro-roundtable/ROUNDTABLE.md              (master identity)
   Read .claude/agents/<resolved-file>.md   (specialist context)
   ```

4. **Spawn the agent** with the Agent tool:
   - Set the agent's system context from ROUNDTABLE.md + specialist agent file
   - Pass the user's question as the prompt
   - The agent has access to: Read, Grep, Glob, WebSearch, WebFetch, Bash
   - The agent can invoke Gemini via `mcp__gemini-cli__ask-gemini` for peer review

5. **Return the response** to the user with:
   - The specialist's answer
   - Confidence level (High/Medium/Low)
   - Data sources cited
   - Any flags for uncertainty or additional data needed

## Available Specialists

| Specialist | Agent File | Status | Domain |
|---|---|---|---|
| `geoscientist` | `.claude/agents/geoscientist.md` | **Active** | Formation evaluation, petrophysics, stratigraphy, facies |
| `reservoir` | `.claude/agents/reservoir-engineer.md` | **Active** | Drainage, recovery factors, decline curves, EOR, waterflood |
| `drilling` | `.claude/agents/drilling-engineer.md` | **Active** | Well design, directional, casing, cementing, mud weight |
| `well-performance` | `.claude/agents/well-performance.md` | **Active** | Completions, sand control, PCP/ESP lift, production optimization |
| `geomechanics` | `.claude/agents/geomechanics.md` | **Active** | Rock mechanics, wellbore stability, cap rock, stress analysis |
| `facilities` | `.claude/agents/facilities-engineer.md` | **Active** | Surface facilities, OTSG, separation, water treatment, sand handling |
| `economics` | `.claude/agents/economics-reserves.md` | **Active** | COGEH/NI 51-101, WCS pricing, break-even, F&D, NPV |
| `simulation` | `.claude/agents/simulation-engineer.md` | **Active** | CMG STARS/IMEX, thermal modeling, foamy oil, multiphase flow |
| `production-data` | `.claude/agents/production-data.md` | **Active** | SCADA, analytics, dashboards, data quality, WellFi integration |
| `multiphase-flow` | `.claude/agents/multiphase-flow.md` | **Active** | Wellbore flow regimes, separator design, bubble dynamics, BHA integration |

## Future Specialists (Phase 4)

| Specialist | Agent File | Status |
|---|---|---|
| `lead` | `.claude/agents/lead-engineer.md` | Planned (Phase 4) |

## Error Handling

- **No specialty provided:** List all available specialists
- **Invalid specialty:** Show error with list of available specialists
- **No question provided:** Ask user for their question
