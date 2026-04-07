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

2. **Validate the specialist exists:**
   ```
   Glob petro-roundtable/agents/<specialty>.md
   ```
   If the agent file does not exist, respond:
   > "The **[specialty]** agent is not yet available. Available specialists: [list agents found in petro-roundtable/agents/]."

3. **Load the specialist agent:**
   ```
   Read petro-roundtable/ROUNDTABLE.md    (master identity)
   Read petro-roundtable/agents/<specialty>.md  (specialist context)
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

## Available Specialists (Phase 1)

| Specialist | Agent File | Status |
|---|---|---|
| `geoscientist` | `agents/geoscientist.md` | Active |

## Future Specialists (Phase 3+)

| Specialist | Agent File | Status |
|---|---|---|
| `reservoir` | `agents/reservoir-engineer.md` | Planned |
| `drilling` | `agents/drilling-engineer.md` | Planned |
| `well-performance` | `agents/well-performance.md` | Planned |
| `geomechanics` | `agents/geomechanics.md` | Planned |
| `facilities` | `agents/facilities-engineer.md` | Planned |
| `economics` | `agents/economics-reserves.md` | Planned |
| `simulation` | `agents/simulation-engineer.md` | Planned |
| `lead` | `agents/lead-engineer.md` | Planned |

## Error Handling

- **No specialty provided:** List all available specialists
- **Invalid specialty:** Show error with list of available specialists
- **No question provided:** Ask user for their question
