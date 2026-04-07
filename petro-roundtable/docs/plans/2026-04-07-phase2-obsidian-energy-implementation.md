# Phase 2: Obsidian Energy Operator Mastery — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Obsidian Energy operator representative agent with a verified 13-section knowledge base, achieving mastery across business strategy, field operations, well design, financials, competitive positioning, and WellFi technology.

**Architecture:** Single knowledge base file (`knowledge/obsidian-energy.md`) + agent definition (`operators/obsidian-energy.md`) + `/ask-operator` skill. Follows Phase 1 pattern exactly — knowledge base curated from primary sources, agent loads KB + formation KB + ROUNDTABLE.md, skill routes questions to agent.

**Tech Stack:** Claude Code agent definitions (.md), knowledge base (.md), skill (SKILL.md), Gemini CLI MCP for audit, production CSV data analysis via Bash/Grep.

**Design doc:** `petro-roundtable/docs/plans/2026-04-07-obsidian-energy-operator-mastery-design.md`

---

## Task 1: Extract Data from Corporate PDFs

**Files:**
- Read: `Data/Obsidian/Corporate Presentations/Obsidian_2026-Guidance-Corporate-Presentation-FINAL.pdf`
- Read: `Data/Obsidian/Corporate Presentations/Obsidian_2026-02-05-OBE-2025-Reserves-Release-FINAL.pdf`
- Read: `Data/Obsidian/Corporate Presentations/Obsidian_OBE-2026-Capital-Program-and-Guidance-FINAL.pdf`
- Create: `petro-roundtable/docs/plans/obsidian-pdf-extraction-notes.md` (working notes)

**Step 1: Read the 2026 Corporate Presentation PDF**

```
Read Data/Obsidian/Corporate Presentations/Obsidian_2026-Guidance-Corporate-Presentation-FINAL.pdf
```

Extract and record:
- Corporate strategy slides (payout ratio, capital discipline, growth targets)
- Peace River field maps with township/range references
- Production breakdown by area (Peace River vs Willesden Green)
- Well design diagrams (fishbone/multilateral architecture)
- Waffle well design details and results
- Waterflood pilot locations and status
- Capital allocation pie chart / breakdown
- Drilling inventory slide (locations by formation)

**Step 2: Read the 2025 Reserves Release PDF**

```
Read Data/Obsidian/Corporate Presentations/Obsidian_2026-02-05-OBE-2025-Reserves-Release-FINAL.pdf
```

Extract and record:
- PDP/1P/2P reserve volumes by category (oil, gas, NGL)
- F&D costs per boe (PDP, 1P, 2P) — verify against web data ($25.70, $19.44, $20.68)
- FD&A costs (including acquisitions/dispositions)
- Recycle ratios — verify against web data (1.1x, 1.4x, 1.3x)
- Reserve replacement ratios — verify (118%, 185%, 235%)
- Reserve life index — verify (6.0, 10.1, 13.3 years)
- Drilling locations booked by area (77 Bluesky, 103 Clearwater, 130 WG, 47 Viking)
- NPV10 values (PDP $961.2M, 1P $1,446.0M, 2P $2,102.9M)
- FDC estimates
- Waterflood reserve additions (3.5 mmboe on 2P)

**Step 3: Read the 2026 Capital Program PDF**

```
Read Data/Obsidian/Corporate Presentations/Obsidian_OBE-2026-Capital-Program-and-Guidance-FINAL.pdf
```

Extract and record:
- Total capex guidance ($190-230M)
- Well count by formation and half-year (H1 vs H2)
- Peace River: 26 wells, 9 Bluesky, 8 injectors
- $80M heavy oil allocation
- $22M waterflood allocation (8 injectors: Nampa, West Dawson, Dawson)
- Production guidance (27,900-29,900 boe/d, 73% liquids)
- Rig count and drilling cadence
- Any per-well economics or type curves

**Step 4: Save extraction notes**

Write all extracted data points to `petro-roundtable/docs/plans/obsidian-pdf-extraction-notes.md` as a working reference. Include page references where possible.

**Step 5: Commit**

```bash
git add petro-roundtable/docs/plans/obsidian-pdf-extraction-notes.md
git commit -m "docs: extract Obsidian Energy data from corporate PDFs for Phase 2 KB"
```

---

## Task 2: Analyze Production CSV Data

**Files:**
- Read: `Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv` (178 OBE rows)
- Read: `Data/clearwater_bluesky_2026_drilling_chart_full.csv` (OBE drilling data)

**Step 1: Analyze OBE well distribution by field**

```bash
grep -i "obsidian" Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv | \
  awk -F',' '{print $5}' | sort | uniq -c | sort -rn
```

This extracts the `field_name` column for all 178 OBE wells. Record distribution (expect mostly SEAL, some HVS, Walrus).

**Step 2: Analyze production rates**

```bash
grep -i "obsidian" Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv | \
  awk -F',' '{sum+=$10; count++} END {print "Avg oil rate:", sum/count, "bbl/d across", count, "wells"}'
```

Calculate:
- Average oil production rate per well
- Total OBE oil production from CSV
- Top 10 producing wells (sort by `last_oil_production_rate`)
- Wells with zero production (suspended/shut-in)
- Well status distribution (Active, Suspended, etc.)

**Step 3: Analyze well vintage and spud dates**

```bash
grep -i "obsidian" Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv | \
  awk -F',' '{print $16}' | awk -F'/' '{print $3}' | sort | uniq -c | sort -k2 -n
```

Build a spud-year histogram showing OBE's drilling cadence over time.

**Step 4: Check fluid types**

```bash
grep -i "obsidian" Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv | \
  awk -F',' '{print $7}' | sort | uniq -c
```

Verify all wells are Crude Bitumen (expect 100% for Bluesky).

**Step 5: Record all statistics**

Add production statistics to the extraction notes file.

---

## Task 3: Write the Knowledge Base

**Files:**
- Create: `petro-roundtable/knowledge/obsidian-energy.md`

**Step 1: Write the knowledge base**

Create the 13-section knowledge base following the exact pattern of `petro-roundtable/knowledge/bluesky-formation.md`. Use the design doc Section 3 as the section outline. Populate every data point from:
- PDF extraction notes (Task 1)
- CSV analysis results (Task 2)
- Web research data from design doc Section 10

**Section checklist — every section MUST have:**
- [ ] Specific numbers, not vague statements
- [ ] Source citation (PDF name, press release, CSV file)
- [ ] Cross-references to `bluesky-formation.md` where relevant (Sections 8, 11)

**Key data points that MUST appear (verification checklist):**

| Data Point | Value | Source |
|---|---|---|
| FY2025 production | 30,624 boe/d | Q4/FY2025 Results |
| Heavy oil component | 12,080 bbl/d | Q4/FY2025 Results |
| 2P reserves | 158.4 mmboe | 2025 Reserves Release |
| NPV10 2P BT | $2,102.9M | 2025 Reserves Release |
| Bluesky locations | 77 (2P undeveloped) | 2025 Reserves Release |
| Clearwater locations | 103 (2P undeveloped) | 2025 Reserves Release |
| PDP F&D | $25.70/boe | 2025 Reserves Release |
| Operating netback | $27.48/boe | Q4/FY2025 Results |
| Net debt | $268.2M | Q4/FY2025 Results |
| FFO | $272.1M | Q4/FY2025 Results |
| 2026 capex | $190-230M | 2026 Guidance |
| Peace River wells 2026 | 26 (9 Bluesky) | 2026 Capital Program |
| Waterflood injectors 2026 | 8 ($22M) | 2026 Capital Program |
| Walrus wells drilled | 14 | H1 2025 Update |
| Walrus best IP30 | 361 boe/d | H1 2025 Update |
| Waffle wells tested | 2 of 5 HVS, >170 boe/d | H1 2025 Update |
| Share buybacks 2025 | 7.6M shares, $54.9M | Q4/FY2025 Results |
| Pembina sale proceeds | ~$325M | Q4/FY2025 Results |
| Waterflood 2P addition | 3.5 mmboe | 2025 Reserves Release |

**Step 2: Self-review the knowledge base**

Read the completed file back. Check:
- Every section has data citations
- No "approximately" or "around" where exact numbers are available
- Cross-references to bluesky-formation.md use correct section numbers
- File paths in Section 13 are correct and exist

**Step 3: Commit**

```bash
git add petro-roundtable/knowledge/obsidian-energy.md
git commit -m "feat: add Obsidian Energy knowledge base — 13 sections with verified data"
```

---

## Task 4: Write the Agent Definition

**Files:**
- Create: `petro-roundtable/operators/obsidian-energy.md`
- Reference: `petro-roundtable/agents/geoscientist.md` (pattern to follow)

**Step 1: Write the agent definition**

Follow the operator template from the design doc (Section 6.2) and the geoscientist pattern. The file must include:

**Frontmatter:**
```yaml
---
agent_id: operator-obsidian-energy
model: claude-opus-4-6
type: operator-representative
operator_name: Obsidian Energy Ltd.
ticker: TSX:OBE
formation_focus: [Bluesky]
production_method: [cold-flow horizontal, multilateral fishbone, waterflood EOR]
headquarters: Calgary, Alberta
tools: [Read, Grep, Glob, WebSearch, WebFetch, Bash]
knowledge:
  - petro-roundtable/knowledge/obsidian-energy.md
  - petro-roundtable/knowledge/bluesky-formation.md
  - petro-roundtable/ROUNDTABLE.md
gemini_review: true
---
```

**Body sections (following geoscientist.md structure):**

1. **Title + identity paragraph** — "You represent Obsidian Energy's operational perspective..."
2. **Operating Philosophy** — Capital discipline, cold-flow horizontal focus, waterflood EOR path, no thermal
3. **Key Fields** — HVS, Walrus, Cadotte, Dawson, Seal (with township/range)
4. **Production Profile** — FY2025 rates, growth trajectory, well count
5. **Well Design & Technology** — Fishbone multilateral, waffle well, WellFi monitoring
6. **Financial Profile** — Netback, F&D, recycle ratio, break-even, capital allocation
7. **Competitive Position** — vs CNRL (thermal), Baytex (polymer), Headwater (Clearwater)
8. **Response Protocol** — 6-step protocol adapted for operator context
9. **Gemini Peer Review Triggers** — Financial accuracy, competitive comparisons, tech claims
10. **Available Data** — File paths to knowledge base, production CSVs, well data, corporate PDFs
11. **When This Rep Adds Value** — Specific question types where OBE perspective matters

**Key design decisions embedded in the prompt:**
- Agent must read `knowledge/obsidian-energy.md` AND `knowledge/bluesky-formation.md` before answering
- Agent uses first-person OBE perspective ("we operate...", "our approach...")
- Agent must cite data vintage (e.g., "FY2025 netback of $27.48/boe per Q4 2025 results")
- Agent must compare to peers when relevant, distinguishing OBE's approach
- Agent must flag when a specialist engineer should weigh in

**Step 2: Verify agent file references are correct**

```
Glob petro-roundtable/knowledge/obsidian-energy.md
Glob petro-roundtable/knowledge/bluesky-formation.md
Glob petro-roundtable/ROUNDTABLE.md
```

All three files must exist.

**Step 3: Commit**

```bash
git add petro-roundtable/operators/obsidian-energy.md
git commit -m "feat: add Obsidian Energy operator agent definition"
```

---

## Task 5: Write the /ask-operator Skill

**Files:**
- Create: `petro-roundtable/skills/ask-operator/SKILL.md`
- Reference: `petro-roundtable/skills/ask-engineer/SKILL.md` (pattern to follow)

**Step 1: Write the skill definition**

Mirror `/ask-engineer` pattern exactly. Key differences:
- Looks in `petro-roundtable/operators/` instead of `petro-roundtable/agents/`
- Operator name is the first argument (e.g., `obsidian`, `cnrl`, `baytex`)
- Matches operator name to file: `operators/<name>*.md` (fuzzy match for convenience)

```markdown
---
name: ask-operator
description: "Route a question to a specific operator representative agent. Usage: /ask-operator <operator> <question>. Available operators are listed in petro-roundtable/CONFIG.md."
---

# Ask Operator

Route a question to an operator representative from the petroleum engineering roundtable.

## Usage

/ask-operator obsidian "What's your 2026 drilling program in the Bluesky?"
/ask-operator obsidian "Why don't you use thermal recovery?"
/ask-operator obsidian "How does your F&D cost compare to Baytex?"

## Process

1. Parse the request:
   - First argument = operator name (e.g., obsidian, cnrl, baytex)
   - Remaining text = the question to ask

2. Validate the operator agent exists:
   Glob petro-roundtable/operators/<name>*.md
   If not found, list available operators from petro-roundtable/operators/

3. Load the operator agent:
   Read petro-roundtable/ROUNDTABLE.md
   Read petro-roundtable/operators/<matched-file>.md

4. Spawn the agent with the Agent tool:
   - Set system context from ROUNDTABLE.md + operator agent file
   - Pass the user's question as the prompt
   - Agent has access to: Read, Grep, Glob, WebSearch, WebFetch, Bash
   - Agent can invoke Gemini for peer review

5. Return the response with:
   - The operator's answer
   - Data sources cited
   - Confidence level
   - Flags for when a specialist engineer should weigh in

## Available Operators (Phase 2)

| Operator | Agent File | Status |
|---|---|---|
| obsidian | operators/obsidian-energy.md | Active |

## Future Operators (Phase 6)

| Operator | Agent File | Status |
|---|---|---|
| cnrl | operators/cnrl-peace-river.md | Planned |
| baytex | operators/baytex-energy.md | Planned |
| headwater | operators/headwater-exploration.md | Planned |

## Error Handling

- No operator provided: List all available operators
- Invalid operator: Show error with list of available operators
- No question provided: Ask user for their question
```

**Step 2: Verify skill directory structure**

```bash
ls petro-roundtable/skills/ask-operator/
```

Ensure SKILL.md is the only file in the directory.

**Step 3: Commit**

```bash
git add petro-roundtable/skills/ask-operator/SKILL.md
git commit -m "feat: add /ask-operator skill for operator representative queries"
```

---

## Task 6: Update CONFIG.md and CLAUDE.md

**Files:**
- Modify: `petro-roundtable/CONFIG.md`
- Modify: `petro-roundtable/CLAUDE.md`

**Step 1: Update CONFIG.md**

Change Active Phase from "Phase 1: Bluesky Formation Mastery" to "Phase 2: Obsidian Energy Operator Mastery".

In the Operator Representatives table, change Obsidian Energy status from "Planned" to "**Active**".

**Step 2: Update CLAUDE.md**

Add to Directory Structure:
- `operators/obsidian-energy.md` under operators/ (with description)
- `knowledge/obsidian-energy.md` under knowledge/ (with description)
- `skills/ask-operator/` under skills/ (with description)

Update Current Phase section:
- Phase 1: mark as COMPLETE
- Phase 2: mark as ACTIVE

Update Mastery Sequence:
- Phase 1: add checkmark
- Phase 2: mark as "(current)"

**Step 3: Commit**

```bash
git add petro-roundtable/CONFIG.md petro-roundtable/CLAUDE.md
git commit -m "docs: update CONFIG.md and CLAUDE.md for Phase 2 active status"
```

---

## Task 7: Run Validation Questions (10)

**Files:**
- Read: `petro-roundtable/operators/obsidian-energy.md` (agent to test)
- Read: `petro-roundtable/knowledge/obsidian-energy.md` (knowledge base)
- Read: `petro-roundtable/knowledge/bluesky-formation.md` (cross-reference)
- Create: `petro-roundtable/docs/plans/phase2-validation-results.md`

**Step 1: Test questions 1-5 (basic → moderate)**

For each question, spawn the Obsidian Energy agent via Agent tool with:
- System context: ROUNDTABLE.md + operators/obsidian-energy.md
- The validation question as the prompt
- Record: answer quality, data citations present, factual accuracy

**Questions 1-5:**

| # | Question | Pass Criteria |
|---|---|---|
| 1 | What is Obsidian Energy's primary production method in the Bluesky? | Mentions cold-flow multilateral horizontal / fishbone, cites KB |
| 2 | How many wells does OBE operate in Peace River and what's the current production rate? | Cites 178 wells from CSV or well count from corporate data, cites FY2025 production |
| 3 | What is OBE's 2026 capital program — how many wells, which formations, what cadence? | 38 total, 26 Peace River, 9 Bluesky, H1 Clearwater injectors / H2 Bluesky drilling |
| 4 | Describe the Harmon Valley South field. | Location (township/range), flagship status, waterflood pilot at 9-25 pad, waffle well tests |
| 5 | What is OBE's 'waffle well' innovation and what were the pilot results? | 2 of 5 HVS wells, >170 boe/d, better than linear offsets, early interventions needed |

**Step 2: Test questions 6-10 (hard — cross-reference, competitive, synthesis)**

| # | Question | Pass Criteria |
|---|---|---|
| 6 | Why doesn't Obsidian use thermal recovery when CNRL does at Carmon Creek? | Cross-refs viscosity gradient from bluesky-formation.md, explains cold-flow economics |
| 7 | What are OBE's key financial metrics? | Cites F&D ($25.70 PDP), netback ($27.48), recycle ratio (1.1x), FFO ($272.1M) with sources |
| 8 | Compare OBE's cold-flow to Baytex's polymer flood in the Seal area. | Capex intensity, RF targets, water breakthrough risk, break-even comparison |
| 9 | How does WellFi fit into OBE's operations? | PCP optimization, data-driven interventions, dual P/T sensors, references well data |
| 10 | What is OBE's waterflood pilot program? | HVS 9-25 (Bluesky, 2 wells Q3 2025), Dawson 4-24 (CW, 2+2), 2026 expansion (8 injectors, $22M) |

**Step 3: Record results**

Write pass/fail for each question to `petro-roundtable/docs/plans/phase2-validation-results.md` with notes on gaps found.

**Step 4: Fix any gaps**

If a question fails:
- Factually wrong → fix knowledge base data point
- Missing data → add to knowledge base section
- Not citing sources → fix agent response protocol
- Not reading files → fix agent Available Data section

**Step 5: Retest failed questions**

Re-run any failed questions after fixes. All 10 must pass.

**Step 6: Commit fixes**

```bash
git add petro-roundtable/knowledge/obsidian-energy.md petro-roundtable/operators/obsidian-energy.md
git add petro-roundtable/docs/plans/phase2-validation-results.md
git commit -m "feat: Phase 2 validation — 10/10 questions passing with gap fixes"
```

---

## Task 8: Gemini 3.1 Pro Audit

**Step 1: Send knowledge base to Gemini for audit**

Use `mcp__gemini-cli__ask-gemini` with this prompt:

```
We built an AI operator representative agent for Obsidian Energy Ltd. (TSX:OBE), a Peace River heavy oil producer focused on Bluesky Formation cold-flow horizontal wells.

Our knowledge base covers 13 sections:
1. Quick Reference (production, reserves, locations)
2. Corporate Strategy (capital discipline, payout, buybacks)
3. Asset Portfolio (680+ net sections, 357 drilling locations)
4. Key Fields (HVS, Walrus, Cadotte, Dawson, Seal)
5. Production Profile (30,624 boe/d FY2025)
6. Well Design (fishbone multilateral, waffle well pilot)
7. EOR & Waterflooding (Bluesky + Clearwater pilots, 8 injectors 2026)
8. Why No Thermal (viscosity allows cold flow, capex advantage)
9. Financial Metrics (F&D $25.70 PDP, netback $27.48, FFO $272.1M)
10. Technology (WellFi downhole monitoring, PCP optimization)
11. Competitive Position (vs CNRL CSS, Baytex polymer, Headwater CW)
12. 2026 Capital Program (26 Peace River wells, $80M heavy oil)
13. Data Sources (file paths)

What critical aspects of Obsidian Energy's operations, strategy, or competitive position are we likely missing? List 5-7 items ranked by importance for petroleum engineering decisions. Be specific to Peace River Bluesky operations.
```

**Step 2: Evaluate Gemini's response**

For each gap Gemini identifies:
1. Is it factual? → Verify against PDFs, CSVs, or web search
2. Is it relevant to OBE specifically? → Some may be generic heavy oil, not OBE-specific
3. Is it already covered? → Check if KB already addresses it under a different section
4. Is it critical? → Would an engineer make a worse decision without this information?

**Step 3: Incorporate valid gaps**

Add verified, relevant, critical gaps to the knowledge base. Do NOT add:
- Generic petroleum engineering knowledge (already in ROUNDTABLE.md or bluesky-formation.md)
- Speculative or unverifiable claims
- Items already covered in different wording

**Step 4: Retest affected validation questions**

If any incorporated gaps affect the 10 validation questions, retest those questions.

**Step 5: Commit**

```bash
git add petro-roundtable/knowledge/obsidian-energy.md
git add petro-roundtable/docs/plans/phase2-validation-results.md
git commit -m "feat: incorporate Gemini audit feedback — Phase 2 knowledge base hardened"
```

---

## Task 9: Final Commit and Phase Update

**Step 1: Final self-review**

Read all Phase 2 files end-to-end:
```
Read petro-roundtable/knowledge/obsidian-energy.md
Read petro-roundtable/operators/obsidian-energy.md
Read petro-roundtable/skills/ask-operator/SKILL.md
Read petro-roundtable/CONFIG.md
Read petro-roundtable/CLAUDE.md
```

Verify:
- [ ] Knowledge base has all 13 sections with data citations
- [ ] Agent definition loads correct knowledge files
- [ ] Skill matches /ask-engineer pattern
- [ ] CONFIG.md shows Phase 2 active, OBE agent active
- [ ] CLAUDE.md directory listing includes all new files
- [ ] No broken file path references

**Step 2: Update CLAUDE.md Phase status to COMPLETE**

```markdown
**Phase 2: Obsidian Energy Operator Mastery — COMPLETE**
- 10/10 validation questions passed with data citations
- Gemini 3.1 Pro audit completed — N gaps incorporated
- Knowledge base: 13 sections, all data verified against source
```

**Step 3: Final commit**

```bash
git add -A petro-roundtable/
git commit -m "feat: Phase 2 complete — Obsidian Energy operator mastery, 10/10 validation, Gemini audited"
```

**Step 4: Verify success criteria**

Check all boxes from design doc Section 8:
- [ ] Agent can explain OBE's operating philosophy with specifics
- [ ] Agent cites current production data from CSVs
- [ ] Agent knows waffle well design, waterflood pilots, HVS field details
- [ ] Financial metrics are current and sourced
- [ ] Agent correctly distinguishes OBE's cold-flow approach from CNRL's thermal
- [ ] Gemini 3.1 Pro finds no critical gaps in an operator knowledge audit

---

## Summary

| Task | Deliverable | Commit Message |
|---|---|---|
| 1 | PDF extraction notes | `docs: extract Obsidian Energy data from corporate PDFs` |
| 2 | CSV production analysis | (rolled into Task 3) |
| 3 | `knowledge/obsidian-energy.md` | `feat: add Obsidian Energy knowledge base — 13 sections` |
| 4 | `operators/obsidian-energy.md` | `feat: add Obsidian Energy operator agent definition` |
| 5 | `skills/ask-operator/SKILL.md` | `feat: add /ask-operator skill` |
| 6 | CONFIG.md + CLAUDE.md updates | `docs: update CONFIG.md and CLAUDE.md for Phase 2` |
| 7 | Validation results (10/10) | `feat: Phase 2 validation — 10/10 questions passing` |
| 8 | Gemini audit + gap fixes | `feat: incorporate Gemini audit feedback` |
| 9 | Final phase completion | `feat: Phase 2 complete — Obsidian Energy operator mastery` |
