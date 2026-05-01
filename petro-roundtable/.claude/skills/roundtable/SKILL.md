---
name: roundtable
description: "Run a multi-agent roundtable discussion on a petroleum engineering question. The Lead Engineer moderates, specialists debate in relevance-weighted order, Gemini reviews at the end. Usage: /roundtable <question>"
---

# Petroleum Engineering Roundtable

Run a moderated multi-agent discussion on a complex cross-discipline question.

## Usage

```
/roundtable "Can we integrate a downhole gas separator with the WellFi device?"
/roundtable "Should OBE switch from rod-driven PCP to ESPCP at 86 degrees?"
```

## Process

### Step 0: Load the Lead Engineer

```
Read petro-roundtable/ROUNDTABLE.md        (master identity)
Read .claude/agents/lead-engineer.md  (moderator persona + protocol)
Read petro-roundtable/CONFIG.md            (agent roster)
```

Become the Lead Engineer for this discussion. Follow the Relevance-Weighted Cascade protocol exactly.

### Step 1: FRAMING (Phase 1)

As the Lead Engineer:
1. Restate the question clearly
2. Determine the **1st-order specialist** — who owns this domain?
3. Rank the remaining specialists by relevance (2nd, 3rd, 4th order)
4. Identify any **hard-constraint specialists** that carry override weight
5. Present the speaking order to the user:
   ```
   ROUNDTABLE FRAMING
   Question: [restated clearly]
   Speaking Order:
     1st Order: [Specialist] — [why they're primary]
     2nd Order: [Specialist] — [what they add]
     3rd Order: [Specialist] — [if needed, why]
     Hard Constraints: [any override specialists]
   ```
6. Dispatch the 1st-order specialist

### Step 2: PRIMARY RESPONSE (Phase 2)

Dispatch the 1st-order specialist using the Agent tool:
- `model: "opus"` for ALL specialist agents in the roundtable — no exceptions. RT2 vs RT3 comparison proved that Sonnet produces calculation errors (600x velocity mistake), shallow physics (symmetric lip when asymmetric was required), and optimistic estimates (10-25% when 5-15% was honest). Opus costs more tokens but produces engineering-grade analysis. All specialists must operate at the same level of rigor to maintain discussion quality.
- Include their agent definition as context
- Include ROUNDTABLE.md as shared identity
- The question should be the original roundtable question
- Instruct them to: read KBs, run calculations, cite sources, flag extrapolations

Read the response. Identify:
- What is their position?
- What assumptions did they make?
- What tensions or unknowns exist?
- What adjacent domains are affected?

Present the primary response to the user with your commentary:
```
[1ST ORDER: Specialist Name]
[Their response]

LEAD ENGINEER NOTES:
- Key position: [summary]
- Assumptions made: [list]
- Tensions identified: [what needs challenge or additional perspective]
- Dispatching 2nd order: [Specialist] to address [specific aspect]
```

### Step 3: CASCADE (Phase 3)

Dispatch the 2nd-order specialist:
- Include the FULL transcript so far (Lead Engineer framing + primary response)
- Frame a SPECIFIC follow-up question — don't just repeat the original question
- Example: "Multiphase Flow has recommended X. From your perspective as Well Performance, how does this affect [specific concern]? Do you agree with their assumption about [Y]?"

Read the 2nd-order response. Then:
- Give the 1st-order specialist a chance to **defend or incorporate** the 2nd-order feedback
  (dispatch them again with the 2nd-order response as context)
- Decide: does a 3rd or 4th order perspective add value?
- If yes: dispatch with full accumulated transcript
- If no: move to synthesis

**Cascade continues** until:
- All relevant perspectives have been heard
- Discussion is producing diminishing returns
- A hard constraint has been raised that changes the direction
- Typically 2-4 specialists total (not all 10)

### Step 4: SYNTHESIS (Phase 4)

As the Lead Engineer, draft the synthesis:

```
SYNTHESIS DRAFT
Primary conclusion: [weighted by relevance order]
Key constraints: [from each specialist]
Unresolved tensions: [where specialists disagree]
Confidence: High / Medium / Low
```

The Lead Engineer performs their OWN adversarial assessment:
- What did the panel miss?
- What are the deployment/retrievability/manufacturing risks?
- What is the single biggest risk to this design succeeding?
- What alternative approaches were not considered?

Document this as "Lead Engineer Adversarial Assessment" in the deliverable.

**Gemini review is OPTIONAL.** If invoked, use adversarial framing ("stop validating, challenge this"). Gemini has proven unreliable for adversarial review (0/3 in roundtables 1-2) — the Lead Engineer's own critical assessment is the primary quality gate.

### Step 5: DELIVERABLE (Phase 5)

Present the final roundtable output:

```
## Roundtable: [Question]
**Date:** YYYY-MM-DD
**Confidence:** [High/Medium/Low]
**Primary Recommendation:** [1-2 sentences]

### Discussion Summary
[Weighted synthesis of all specialist contributions]

### Weight Map
| Specialist | Order | Key Contribution | Weight in Final |
|---|---|---|---|

### Unresolved Questions
- [What couldn't be resolved — needs data, research, field validation]

### Action Items
- [ ] [Specific next step with owner]

### Gemini Advisor Review
[What Gemini flagged, what was incorporated, what was noted]

### Post-Discussion Audit
- Knowledge gaps identified: [any KB enhancements needed]
- Agent improvements: [any agent definitions that should be updated]
- Relevance ordering feedback: [was the speaking order right?]
```

## Rules

1. **One specialist at a time.** Don't dispatch multiple specialists in parallel during the cascade — each must react to what came before.
2. **Context accumulates.** Each subsequent specialist gets the FULL transcript so far.
3. **The primary expert speaks first.** Not the most senior, not the most vocal — the most relevant.
4. **Defend or incorporate.** When challenged, the primary expert must respond — they can't just be overruled silently.
5. **Gemini comes LAST.** Not during the discussion. After the synthesis is drafted.
6. **The Lead Engineer decides.** Specialists advise, Gemini advises, but the Lead Engineer makes the call.
7. **Flag knowledge gaps.** If a specialist says "I don't have data for this," that's an ACTION ITEM, not a dead end.
8. **No more than 4 specialists per discussion** unless a hard constraint demands another voice.

## Specialist Dispatch Template

When dispatching a specialist via the Agent tool, use this prompt structure:

```
You are the [Specialist Name] for the petro-roundtable.
Read your agent definition at: .claude/agents/[file].md
Read the shared identity at: petro-roundtable/ROUNDTABLE.md

ROUNDTABLE CONTEXT:
Question: [original question]
Your role: [Nth order] specialist
Discussion so far:
[full transcript]

SPECIFIC QUESTION FOR YOU:
[Tailored follow-up from Lead Engineer — not just the original question]

Instructions:
- Read your knowledge bases before answering
- Run calculation scripts where applicable
- Cite sources (KB sections, SPE papers)
- Flag extrapolation uncertainties
- Respond to the prior specialist's position — agree, challenge, or add constraints
- Keep your response under [word limit] words
```
