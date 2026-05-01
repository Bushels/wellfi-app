---
name: bluesky-briefing
description: "Deep-dive Bluesky Formation briefing for petroleum engineering training and onboarding. Use when the user wants to understand the Bluesky Formation, asks about Peace River geology, or needs formation context for engineering decisions."
---

# Bluesky Formation Briefing

Produce a comprehensive Bluesky Formation briefing by reading the knowledge base and delivering a structured deep-dive.

## Process

1. **Read the knowledge base:**
   ```
   Read petro-roundtable/knowledge/bluesky-formation.md
   ```

2. **Read the geoscientist agent context** for additional interpretation guidance:
   ```
   Read .claude/agents/geoscientist.md
   ```

3. **Deliver the briefing** covering the knowledge base (13 headers: Quick Reference + Sections 1-10 + Subsections 4b, 4c):

   ### Section Structure
   For each section, provide:
   - **Key data points** with specific numbers (not vague statements)
   - **Engineering implications** — why this matters for production decisions
   - **Data sources** — cite the knowledge base section and original reference

   ### Required Sections
   1. **Stratigraphic Position** — Where the Bluesky sits, what's above/below, correlatives
   2. **Depositional Environment** — Boreal Sea transgression, estuarine complex, paleotopography
   3. **Reservoir Properties by Facies** — Full facies hierarchy table with porosity and BIP estimates
   4. **Fluid Properties** — API gravity range, vertical viscosity gradient (80,000→1,750,000 cP), oil mobility
   5. **Trapping Mechanism** — Wilrich cap rock, lateral pinchout, bottom water absence
   6. **Production Methods** — CHOPS, fishbone multilateral, CSS, SAGD limitations, ASP/polymer
   7. **Key Operators** — Obsidian Energy, CNRL, Baytex with fields and methods
   8. **Challenges** — Water coning, sand production, foamy oil, shale baffles, emulsification
   9. **Key Calculation Data** — OOIP formula, recovery factors, petrophysical cutoffs, SOR ranges
   10. **Data File Locations** — Where to find production, drilling, and geological data

4. **Optionally invoke Gemini for audit** (if user requests or if `--audit` flag passed):
   ```
   Ask Gemini 3.1 Pro: "We built an AI geoscientist agent specialized in the Bluesky Formation
   at Peace River, Alberta. Here are the sections of our knowledge base: [list sections].
   What critical aspects of Bluesky Formation geology and petrophysics are we likely missing?
   List 5-7 items ranked by importance for petroleum engineering decisions."
   ```

## Quality Checks

The briefing MUST:
- [ ] Include specific numbers, not generic statements (e.g., "28.0% porosity for tidal-inlet" not "high porosity")
- [ ] Reference the viscosity gradient data (80,000→1,750,000 cP over 32m, 22x increase)
- [ ] Include oil mobility data (0.017 mD/cP top → 0.000030 mD/cP base)
- [ ] Present the facies hierarchy table with all 6 facies ranked
- [ ] Cite data file paths for further exploration
- [ ] Flag what additional data would strengthen the analysis
