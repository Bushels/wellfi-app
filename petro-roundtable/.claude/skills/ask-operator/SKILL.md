---
name: ask-operator
description: "Route a question to a specific operator representative agent. Usage: /ask-operator <operator> <question>. Available operators are listed in petro-roundtable/CONFIG.md."
---

# Ask Operator

Route a question to an operator representative from the petroleum engineering roundtable.

## Usage

```
/ask-operator obsidian "What's your 2026 drilling program in the Bluesky?"
/ask-operator obsidian "Why don't you use thermal recovery?"
/ask-operator obsidian "How does your F&D cost compare to Baytex?"
```

## Process

1. **Parse the request:**
   - First argument = operator name (e.g., `obsidian`, `cnrl`, `baytex`)
   - Remaining text = the question to ask

2. **Validate the operator agent exists:**
   ```
   Glob petro-roundtable/operators/<name>*.md
   ```
   If the agent file does not exist, respond:
   > "The **[operator]** operator agent is not yet available. Available operators: [list agents found in petro-roundtable/operators/]."

3. **Load the operator agent:**
   ```
   Read petro-roundtable/ROUNDTABLE.md    (master identity)
   Read petro-roundtable/operators/<matched-file>.md  (operator context)
   ```

4. **Spawn the agent** with the Agent tool:
   - Set the agent's system context from ROUNDTABLE.md + operator agent file
   - Pass the user's question as the prompt
   - The agent has access to: Read, Grep, Glob, WebSearch, WebFetch, Bash
   - The agent can invoke Gemini via `mcp__gemini-cli__ask-gemini` for peer review

5. **Return the response** to the user with:
   - The operator's answer
   - Data sources cited
   - Confidence level (High/Medium/Low)
   - Flags for when a specialist engineer should weigh in

## Available Operators (Phase 2)

| Operator | Agent File | Status |
|---|---|---|
| `obsidian` | `operators/obsidian-energy.md` | Active |

## Future Operators (Phase 6)

| Operator | Agent File | Status |
|---|---|---|
| `cnrl` | `operators/cnrl-peace-river.md` | Planned |
| `baytex` | `operators/baytex-energy.md` | Planned |
| `headwater` | `operators/headwater-exploration.md` | Planned |

## Error Handling

- **No operator provided:** List all available operators
- **Invalid operator:** Show error with list of available operators
- **No question provided:** Ask user for their question
