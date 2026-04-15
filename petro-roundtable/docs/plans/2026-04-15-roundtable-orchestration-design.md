# Roundtable Orchestration — Phase 4 Design Document

**Date:** 2026-04-15
**Status:** Approved
**Phase:** 4 — Roundtable Orchestration

## 1. Vision

Build a reusable multi-agent discussion system where petroleum engineering specialists debate complex cross-discipline questions under the guidance of a Lead Engineer moderator. The system uses a Relevance-Weighted Cascade protocol where the most qualified specialist speaks first, subsequent specialists react to what came before (not in isolation), and opinions are weighted by their proximity to the core question. Gemini 3.1 Pro serves as the Lead Engineer's advisor — reviewing the final consensus for blind spots after the discussion concludes.

## 2. Components

### Lead Engineer Agent (`agents/lead-engineer.md`)

A senior technical leader who:
- Understands all 10 specialist domains well enough to determine speaking order
- Ranks specialists by relevance order (1st through 4th) per question
- Recognizes when lower-order perspectives carry critical-constraint weight
- Synthesizes weighted opinions into actionable conclusions
- Identifies knowledge gaps that need research
- Decides when to cut off diminishing-return discussion
- Consults Gemini as a post-discussion advisor

Loads: `ROUNDTABLE.md` + `CONFIG.md` (roster awareness). Does NOT load domain KBs — relies on specialists for domain knowledge.

### `/roundtable` Skill (`skills/roundtable/SKILL.md`)

The discussion protocol invoked by the user. Defines:
- How to frame a question
- The 5-phase discussion process
- How to dispatch specialists (as Agent subagents)
- How to pass context between rounds (each specialist sees prior responses)
- When and how to invoke Gemini
- The output format (answer, weight map, unresolved items, action items)

## 3. Discussion Protocol — 5 Phases

### Phase 1: FRAMING

Lead Engineer receives the question and determines:
- **Primary expert (1st order):** Who owns this domain?
- **Relevance ranking:** Which other specialists are 2nd, 3rd, 4th order?
- **Hard-constraint specialists:** Any domains that carry override weight (safety, mechanical feasibility, regulatory)?

Dispatches ONLY the primary expert first. Others wait.

### Phase 2: PRIMARY RESPONSE

1st-order specialist gives their full analysis (reading KBs, running scripts, citing sources). Lead Engineer reads the response and identifies:
- What tensions exist?
- What assumptions were made?
- What adjacent domains are affected?

Dispatches 2nd-order specialist WITH the primary response as context.

### Phase 3: CASCADE

Sequential-reactive discussion:
1. 2nd-order specialist responds — reacting to the primary response
2. They may: agree + add constraints, challenge assumptions, raise concerns
3. Primary expert gets a chance to DEFEND or INCORPORATE the feedback
4. Lead Engineer decides: does a 3rd or 4th order perspective add value?
5. If yes: dispatch next specialist with full transcript so far
6. If no: move to synthesis
7. Repeat until diminishing returns (typically 2-4 specialists total)

**Override rule:** If any specialist raises a hard constraint (safety, physical impossibility, regulatory violation), it overrides relevance ordering and must be addressed before synthesis.

### Phase 4: SYNTHESIS + GEMINI REVIEW

Lead Engineer drafts the consensus summary:
- Primary conclusion (weighted by relevance order)
- Key constraints identified by each specialist
- Unresolved tensions (where specialists disagree)
- Confidence level (High/Medium/Low)

Sends the FULL synthesis to Gemini 3.1 Pro:
- "Here is the panel's conclusion on [question]. What did we miss? What would you challenge? Any blind spots?"
- Lead Engineer incorporates Gemini's feedback into the final output
- Gemini is an advisor — the Lead Engineer decides what to accept

### Phase 5: DELIVERABLE

The roundtable output includes:
1. **ANSWER** — The engineering recommendation with confidence level
2. **WEIGHT MAP** — Which specialist contributed what, at what relevance order, and how heavily it was weighted
3. **UNRESOLVED** — Open questions that need field data or more research
4. **ACTION ITEMS** — Specific next steps: calculations to run, papers to acquire, agent improvements needed, knowledge gaps to fill
5. **TRANSCRIPT** — Full discussion record for audit

## 4. Relevance Ordering Logic

The Lead Engineer determines order based on the QUESTION DOMAIN, not a fixed roster. The mapping is dynamic:

| Question Type | Typical 1st Order | Typical 2nd Order |
|---|---|---|
| Separator/flow physics | Multiphase Flow | Well Performance |
| Completion/lift design | Well Performance | Multiphase Flow or Drilling |
| EOR/recovery strategy | Reservoir Engineer | Simulation |
| Facility sizing | Facilities Engineer | Production Data |
| Cap rock/stability | Geomechanics | Reservoir |
| Economics/investment | Economics & Reserves | Reservoir or Facilities |
| Formation properties | Geoscientist | Reservoir |
| Data/monitoring | Production Data | Well Performance |

**Override triggers:**
- Safety concern → immediate escalation regardless of order
- Mechanical infeasibility → blocks the recommendation
- Regulatory non-compliance → must be resolved before proceeding
- Cost showstopper → flags the economic constraint

## 5. Gemini's Role

Gemini 3.1 Pro acts as the Lead Engineer's advisor:
- NOT a discussion participant
- NOT a judge
- Receives the complete synthesis AFTER the panel concludes
- Reviews for: missed considerations, logical contradictions, literature the panel didn't cite, alternative approaches not discussed
- Lead Engineer decides what to incorporate from Gemini's review
- Gemini's input is labeled as "Advisor Review" in the deliverable

## 6. Implementation

### Agent dispatch pattern

Each specialist is spawned as a Claude Agent subagent (via the Agent tool) with:
- The specialist's agent definition as context
- ROUNDTABLE.md as shared identity
- The discussion transcript so far (accumulated through phases)
- The specific question or follow-up from the Lead Engineer

The main Claude session acts as the execution environment. The Lead Engineer's logic is encoded in the `/roundtable` skill and the `lead-engineer.md` agent definition.

### Context accumulation

Each round of discussion adds to a running transcript:
```
[Lead Engineer] Framing: ...
[1st Order: Multiphase Flow] Response: ...
[Lead Engineer] Follow-up to 2nd Order: ...
[2nd Order: Well Performance] Response: ...
[1st Order: Multiphase Flow] Defense/Incorporation: ...
[Lead Engineer] Synthesis draft: ...
[Gemini Advisor] Review: ...
[Lead Engineer] Final deliverable: ...
```

This transcript is passed to each subsequent specialist so they have full context.

### Post-discussion audit

After each roundtable, the Lead Engineer assesses:
- Were there knowledge gaps that limited the discussion?
- Should any agent's KB be enhanced?
- Were any specialists unable to answer because they lacked data?
- Should the relevance ordering be adjusted for future similar questions?

These findings go into the ACTION ITEMS section of the deliverable.
