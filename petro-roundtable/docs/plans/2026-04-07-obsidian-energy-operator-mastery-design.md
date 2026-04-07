# Phase 2: Obsidian Energy Operator Mastery — Design Document

**Date:** 2026-04-07
**Status:** Approved
**Phase:** 2 of 7
**Branch:** petro-roundtable/main
**Predecessor:** Phase 1 — Bluesky Formation Mastery (COMPLETE, 10/10 validation, Gemini audited)

---

## 1. Objective

Build the Obsidian Energy operator representative agent — the first operator rep in the petro-roundtable system. The agent must achieve mastery across OBE's business strategy, field operations, well design, financial metrics, competitive positioning, and technology (WellFi).

**The test:** Can the agent answer any question about how Obsidian Energy operates, why they make the choices they do, and how they compare to peers — with data citations?

## 2. Available Data Sources

### 2.1 Corporate PDFs (Primary — extract with Claude)

| File | Contents |
|---|---|
| `Data/Obsidian/Corporate Presentations/Obsidian_2026-Guidance-Corporate-Presentation-FINAL.pdf` | 2026 guidance, corporate strategy, field maps, capital allocation, growth plan |
| `Data/Obsidian/Corporate Presentations/Obsidian_2026-02-05-OBE-2025-Reserves-Release-FINAL.pdf` | 2025 reserves results, F&D costs, recycle ratios, drilling locations |
| `Data/Obsidian/Corporate Presentations/Obsidian_OBE-2026-Capital-Program-and-Guidance-FINAL.pdf` | 2026 capital program, well counts by formation/half, waterflood plans |

### 2.2 Production Data (CSV — 178 OBE wells)

| File | Contents |
|---|---|
| `Data/clearwater_bluesky_feb2026_prod_imperial_canonical.csv` | 178 Obsidian wells, all Bluesky, Seal field area — monthly production rates |
| `Data/clearwater_bluesky_2026_drilling_chart_full.csv` | 2026 drilling program by operator |

### 2.3 Well-Level Data

| File | Contents |
|---|---|
| `Data/Obsidian/Obsidian_PeaceRiver_2025_v3.xlsx` | Peace River 2025 well data |
| `Data/Obsidian/Obsidian_Drill_vs_WellFi_Analysis.xlsx` | Drill vs WellFi comparison analysis |
| `Data/Obsidian/Wells/102161808317W509/` | Well 102-16-18-083-17W5: production CSV, directional survey, PCP chart, WellFi sensor data (BHP, dual sensors), pressure analysis |
| `Data/Obsidian/Wells/102130708317W51308/` | Well 102-13-07-083-17W5: Obsidian-provided sensor data |
| `Data/Obsidian/Wells/OBE Hz Walrus (8-28) 1-29-82-18W5 Final Survey L01.csv` | Walrus field directional survey |

### 2.4 Web Research (Supplementary)

Key URLs confirmed by search:
- [OBE Q4/FY2025 Results](https://obsidianenergy.com/press-releases/obsidian-energy-announces-fourth-quarter-and-full-year-2025-results/)
- [OBE 2025 Reserves Results](https://obsidianenergy.com/press-releases/obsidian-energy-announces-strong-2025-reserves-results/)
- [OBE 2026 Guidance](https://obsidianenergy.com/press-releases/obsidian-energy-announces-2026-guidance-and-provides-an-operational-update/)
- [OBE Peace River Operations](https://obsidianenergy.com/operations/peace-river/)
- [OBE H1 2025 Capital Program Update](https://obsidianenergy.com/press-releases/obsidian-energy-announces-first-half-capital-program-update/)

## 3. Knowledge Base Design — `knowledge/obsidian-energy.md`

Single monolithic file following the Phase 1 pattern (bluesky-formation.md). Approximately 12 sections:

### Section 1: Quick Reference Table

| Property | Value | Source |
|---|---|---|
| Legal Name | Obsidian Energy Ltd. | — |
| Ticker | TSX:OBE | — |
| Headquarters | Calgary, Alberta | — |
| FY2025 Production | 30,624 boe/d (12,080 heavy oil, 7,340 light oil, 2,308 NGL, 53 mmcf/d gas) | Q4/FY2025 Results |
| Peace River Focus | Heavy oil — Bluesky + Clearwater formations | — |
| Primary Method | Cold-flow multilateral horizontal ("fishbone") | — |
| 2P Reserves | 158.4 mmboe | 2025 Reserves Release |
| NPV10 (2P, BT) | $2,102.9 million | 2025 Reserves Release |
| 2026 Capex Guidance | $190-230 million, 38 total wells (26 Peace River) | 2026 Guidance |
| Peace River Locations | 180 (77 Bluesky + 103 Clearwater, 2P undeveloped) | 2025 Reserves Release |

### Section 2: Corporate Strategy

Capital discipline philosophy, 60-70% payout ratio, share buybacks ($54.9M in 2025, 7.6M shares), Pembina asset sale ($325M proceeds applied to debt), focus on Peace River heavy oil + Willesden Green light oil, three-year growth plan to 50,000 boe/d.

### Section 3: Asset Portfolio

680+ net sections at Peace River, Willesden Green/PCU#11 light oil assets, 357 total 2P undeveloped locations (130 Willesden Green, 180 Peace River, 47 Viking). Land position map references.

### Section 4: Key Fields

**Harmon Valley South (HVS):** Flagship Bluesky development, multi-pad multilateral horizontals, waterflood injector pilot at 9-25 pad (2 wells, started Q3 2025).

**Walrus:** New Bluesky discovery (Q1 2023), 14 wells drilled to date, best pad (7-21) produced highest initial rates — one well IP30 of 361 boe/d, another 170 boe/d. Key growth area.

**Cadotte:** Bluesky development area, 2026 drilling planned.

**Dawson:** Clearwater waterflood pilot at 4-24 pad (2 single-leg injectors + 2 additional planned Q4 2025).

**Nampa, West Dawson:** Clearwater waterflood expansion areas (8 injectors planned in H1 2026).

**Seal Area:** Legacy Bluesky production area (Penn West heritage), 178 wells in production CSV.

### Section 5: Production Profile

FY2025 total 30,624 boe/d, Q4 2025 27,971 boe/d (post-Pembina sale). Heavy oil component: ~12,000 bbl/d. Peace River vs Willesden Green production split. Decline trajectory and growth outlook from 2026 guidance.

### Section 6: Well Design & Completions

Cold-flow multilateral horizontal ("fishbone") architecture. Single motherbore with multiple open-hole laterals. Laterals steered to upper Bluesky pay (lower-viscosity oil zone, 500x mobility advantage over base). No slotted liners needed for primary production. Pad drilling with 2-4 wells per pad typical.

**Waffle Well Innovation:** Tested on 2 of 5 HVS wells in 2025. Both produced >170 boe/d (100% oil). Better performance than standard linear offset wells, though 2 required early interventions. Design increases contact area on existing pads. Ongoing evaluation.

### Section 7: EOR & Waterflooding

**Bluesky waterflood:** HVS 9-25 pad — 2 existing wells converted to water injection (started Q3 2025). First Bluesky waterflood pilot.

**Clearwater waterflood:** Dawson 4-24 pad — 2 single-leg injectors (Q3 2025), 2 additional planned Q4 2025.

**2026 waterflood plans:** $22M allocated, 8 net injection wells (Nampa, West Dawson, Dawson), strategically prioritized in H1 2026 while Bluesky development drilling targets H2 when commodity prices anticipated to improve.

**Reserves impact:** 3.5 mmboe added on 2P basis across Peace River waterflood projects.

### Section 8: Why No Thermal

OBE operates exclusively cold-flow in the Bluesky — no CSS, no SAGD. This is deliberate:
- Bluesky dead oil viscosity at Peace River (~550m depth, ~25 degC reservoir temp) is ~80,000 cP at top of pay — low enough for primary production with multilateral horizontals
- Horizontal laterals target upper pay where oil mobility is 500x higher than base
- Capital intensity of thermal (OTSG, water treatment, steam distribution) is 3-5x higher per flowing barrel
- OBE's cold-flow break-even is WCS $35-50/bbl vs CSS break-even WCS $45-60/bbl
- Waterflood EOR is the chosen secondary recovery path — lower capex, leverages existing infrastructure
- CNRL uses CSS at Carmon Creek because their wells target deeper, thicker pay in the deltaic lower sand where viscosity is higher

Cross-reference: `knowledge/bluesky-formation.md` Section 4 (Vertical Viscosity Gradient).

### Section 9: Financial Metrics

| Metric | Value | Period |
|---|---|---|
| FFO | $272.1M ($3.92/share) | FY2025 |
| Net Income | $35.2M ($0.51/share) | FY2025 |
| Operating Netback | $27.48/boe | FY2025 |
| Capex | $298.9M | FY2025 |
| Net Debt | $268.2M | Dec 31, 2025 |
| Share Buybacks | 7.6M shares, $54.9M | FY2025 |
| PDP F&D Cost | $25.70/boe | 2025 |
| 1P F&D Cost | $19.44/boe | 2025 |
| 2P F&D Cost | $20.68/boe | 2025 |
| PDP Recycle Ratio | 1.1x | 2025 |
| 1P Recycle Ratio | 1.4x | 2025 |
| PDP Reserve Replacement | 118% | 2025 |
| 1P Reserve Replacement | 185% | 2025 |
| 2P Reserve Replacement | 235% | 2025 |
| PDP RLI | 6.0 years | 2025 |
| 2P RLI | 13.3 years | 2025 |

### Section 10: Technology & Monitoring (WellFi)

WellFi deployment as first downhole monitoring tool in Bluesky. Dual pressure/temperature sensors providing real-time BHP data. Used for:
- Pump optimization (PCP systems)
- Intervention timing decisions (data-driven vs scheduled)
- Production decline diagnosis
- Waterflood response monitoring

Reference: `Data/Obsidian/Wells/102161808317W509/WellFi_Pressure_Analysis_Complete.md`

### Section 11: Competitive Position

| Aspect | Obsidian (OBE) | CNRL (Carmon Creek) | Baytex (Seal) |
|---|---|---|---|
| Primary Method | Cold-flow horizontal | CSS thermal | Multilateral + polymer flood |
| Formation Target | Bluesky upper pay | Bluesky lower+upper sand | Bluesky |
| Capex Intensity | Low | Very High | Medium |
| Break-Even | WCS $35-50/bbl | WCS $45-60/bbl | WCS $40-55/bbl |
| Innovation | Waffle well, waterflood | Horizontal CSS 1,400m TD | Polymer flood pilot |
| RF Target | 10-20% (primary) + waterflood | 20-30% (CSS) | 8-15% incremental (polymer) |

### Section 12: 2026 Capital Program

Total: $190-230M guidance, 38 operated wells company-wide.
Peace River: 26 wells ($80M capex), split:
- H1: Clearwater injectors prioritized (waterflood buildout)
- H2: Bluesky development drilling (9 wells including 1 appraisal)
- 8 net injection wells across Nampa, West Dawson, Dawson ($22M)

### Section 13: Data Sources

File paths to all production CSVs, well data, corporate PDFs, WellFi sensor data, directional surveys.

## 4. Agent Definition — `operators/obsidian-energy.md`

Follows the operator template from the main design doc (Section 6.2). Key attributes:

```yaml
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
```

**Dual knowledge base loading:** The operator rep loads both `obsidian-energy.md` (operator-specific) AND `bluesky-formation.md` (formation reference). This enables cross-referencing — e.g., "Why no thermal?" → agent pulls viscosity gradient from formation KB to explain OBE's cold-flow rationale.

**Response protocol (adapted for operator context):**
1. State the operator question clearly
2. Read knowledge base AND relevant data files before answering
3. Cite financial metrics with source and vintage
4. Compare to peers when relevant (CNRL, Baytex, Headwater)
5. Distinguish operator-specific practices from formation-wide norms
6. Flag when a specialist engineer should weigh in (e.g., reservoir, completions)

**Gemini peer review triggers:**
- Financial accuracy claims (F&D, netback, recycle ratio)
- Competitive comparisons between operators
- Claims about technology advantages or innovation results
- Strategic recommendations based on operator data

## 5. Skill — `skills/ask-operator/SKILL.md`

Mirrors the `/ask-engineer` pattern:

```
/ask-operator obsidian "What's your 2026 drilling program in the Bluesky?"
/ask-operator obsidian "Why don't you use thermal recovery?"
/ask-operator obsidian "How does your F&D cost compare to Baytex?"
```

Process:
1. Parse operator name (first argument)
2. Validate agent exists: `Glob petro-roundtable/operators/<name>*.md`
3. Load ROUNDTABLE.md + operator agent file
4. Spawn agent via Agent tool
5. Return response with data citations

## 6. Validation Questions (10)

Ordered easy → hard, covering all mastery domains:

| # | Question | Tests |
|---|---|---|
| 1 | What is Obsidian Energy's primary production method in the Bluesky? | Basic operational knowledge |
| 2 | How many wells does OBE operate in Peace River and what's the current production rate? | Production data access |
| 3 | What is OBE's 2026 capital program — how many wells, which formations, what cadence? | Capital program mastery |
| 4 | Describe the Harmon Valley South field — location, well count, production history. | Field-level detail |
| 5 | What is OBE's 'waffle well' innovation and what were the pilot results? | Technology knowledge |
| 6 | Why doesn't Obsidian use thermal recovery (CSS/SAGD) when CNRL does at Carmon Creek? | Cross-reference formation KB + competitive reasoning |
| 7 | What are OBE's key financial metrics — F&D cost, recycle ratio, netback, break-even? | Financial data accuracy |
| 8 | Compare OBE's cold-flow approach to Baytex's polymer flood in the Seal area. | Competitive analysis |
| 9 | How does WellFi monitoring fit into OBE's pump optimization and intervention strategy? | Technology + operational integration |
| 10 | What is OBE's waterflood pilot program — which fields, how many injectors, early results? | EOR knowledge depth |

## 7. Build Sequence

Same iterative perfection loop as Phase 1:

```
Step 1: Extract data from 3 corporate PDFs → build knowledge base draft
Step 2: Analyze 178 OBE wells in production CSV → add production statistics
Step 3: Web research → fill competitive positioning, recent news, gaps
Step 4: Write knowledge base (knowledge/obsidian-energy.md)
Step 5: Write agent definition (operators/obsidian-energy.md)
Step 6: Write /ask-operator skill (skills/ask-operator/SKILL.md)
Step 7: Run 10 validation questions, fix gaps
Step 8: Gemini 3.1 Pro audit — "What are we missing about Obsidian Energy?"
Step 9: Incorporate valid Gemini feedback, retest
Step 10: Update CONFIG.md, CLAUDE.md, commit
```

## 8. Success Criteria

From main design doc Section 12:

- [ ] Agent can explain OBE's operating philosophy with specifics
- [ ] Agent cites current production data from CSVs
- [ ] Agent knows waffle well design, waterflood pilots, HVS field details
- [ ] Financial metrics are current and sourced
- [ ] Agent correctly distinguishes OBE's cold-flow approach from CNRL's thermal
- [ ] Gemini 3.1 Pro finds no critical gaps in an operator knowledge audit

## 9. Files Created/Modified

| Action | File | Description |
|---|---|---|
| CREATE | `petro-roundtable/knowledge/obsidian-energy.md` | 13-section operator knowledge base |
| CREATE | `petro-roundtable/operators/obsidian-energy.md` | Agent definition |
| CREATE | `petro-roundtable/skills/ask-operator/SKILL.md` | /ask-operator skill |
| UPDATE | `petro-roundtable/CONFIG.md` | Phase status → Phase 2 active, OBE agent active |
| UPDATE | `petro-roundtable/CLAUDE.md` | Add operator agent, skill, knowledge base to directory listing |

## 10. Web Research Data (Verified 2026-04-07)

Key metrics confirmed via web search for knowledge base population:

**Production:** FY2025 30,624 boe/d, Q4 2025 27,971 boe/d
**FFO:** $272.1M (FY2025)
**Netback:** $27.48/boe (FY2025), Q4 $25.64/boe
**Net Debt:** $268.2M (post-Pembina sale)
**F&D (PDP):** $25.70/boe (2025)
**Recycle Ratio (PDP):** 1.1x (2025)
**Reserve Replacement:** PDP 118%, 1P 185%, 2P 235%
**2P Reserves:** 158.4 mmboe, NPV10 $2,102.9M
**Drilling Locations:** 357 total (77 Bluesky, 103 Clearwater, 130 WG, 47 Viking)
**Walrus:** 14 wells, best IP30 361 boe/d
**Waffle Wells:** 2 tested, both >170 boe/d (100% oil), better than linear offsets
**Waterflood:** HVS 9-25 (Bluesky, 2 wells Q3 2025), Dawson 4-24 (Clearwater, 2+2 wells)
**2026 Program:** 26 Peace River wells, 9 Bluesky, 8 injectors, $80M heavy oil capex
