# Roundtable: Integrating Passive Gas Separation into the WellFi Tool String

**Date:** 2026-04-15
**Confidence:** MEDIUM
**Roundtable #:** 2 (first attempt reframed after product constraint correction)

## Primary Recommendation

Develop a "WellFi Collector Sub" — a 2-foot tubing joint with external annular geometry (swept-angle lip ring or baffle fins) that passively captures liquid during slug flow reversals, reducing gas entry at the PCP intake. Expected improvement: 10-25% gas bypass prevention at zero additional trip cost. Validates via WellFi P/T monitoring in-situ.

## Design Concept

The WellFi Collector Sub applies 4 WhaleShark separator principles at tubing-joint scale:
- **P1 Eccentric flow path (+30%):** Rod sag at 86 deg creates natural eccentricity
- **P3 Turbulence minimization (+25%):** Swept-angle profile, no abrupt flow changes
- **P4 Upward-facing collector (+50%):** External lip ring captures liquid falling back during slug reversals
- **P5 Round tube conduit (+50%):** Short open-tube section above collector lip

### Physical Specification
- Sub length: 24 inches (2 feet)
- Sub OD: Match tubing coupling OD or custom profile
- Bore: Full 2-7/8" EUE drift (2.441") — rod string passes through tubing unaffected
- External geometry: Swept-angle lip ring or baffle fins, 0.9" max radial projection (limited by casing collar clearance)
- Material: Conductive steel (not fiberglass) for WellFi EM compatibility
- Thread: 2-7/8" EUE pin/box connections
- Position: Immediately below WellFi sonde in BHA stack

### Why External Geometry (Not Center-Bore)
The initial design placed the collector lip inside the sub bore with the rod passing through. Well Performance Engineer identified a fatal flaw: standard rod couplings (1.75-1.875" OD) would jam in the proposed 1.25" bore. The redesign moves all separation geometry to the OUTSIDE of the tubing — the rod never touches the collector.

## Discussion Transcript Summary

### Round 1: Multiphase Flow Specialist (1st Order)
- Analyzed all 7 WhaleShark principles for scale-dependency
- 4 principles are geometry-dependent (work at any scale): P1, P3, P4, P5
- 3 principles are scale-dependent (need length): P6 (solids sequence — irrelevant at 80,000 cP), P7 (slug buffer volume — reduced proportionally)
- Initial "WellFi Collector Sub" design: 24", 3.25" OD, 1.25" bore, upward-facing annular lip
- Efficiency estimate: 10-25% gas bypass prevention (honest, not oversold)
- Scripts confirmed: bubble rise at 0.05 mm/s (impossible for gravity separation), residence time 19.7 min (marginal for coalescence)

### Round 2: Well Performance Engineer (2nd Order)
- **CAUGHT FATAL FLAW:** 1.25" bore won't clear rod couplings (1.75-1.875" OD)
- Confirmed 10-25% gas reduction IS operationally meaningful: extends PCP life, saves ~$10K/well/year
- WellFi signal becomes MORE stable with less gas (5-signal diagnostic table)
- Worst case: benign spacer sub, no harm
- Recommended swept-angle lip profile to prevent sand accumulation

### Round 3: Multiphase Flow Defense/Revision
- Conceded bore flaw immediately
- Revised to annular external-geometry design — separation features on tubing OD
- Rod stays inside tubing, full drift bore, zero coupling interference
- Efficiency estimate unchanged at 10-25%
- "The annular design is mechanically cleaner and keeps the physics identical"

## Weight Map

| Specialist | Order | Key Contribution | Weight |
|---|---|---|---|
| Multiphase Flow | 1st | WhaleShark principle analysis, design concept, annular redesign | Primary |
| Well Performance | 2nd | Coupling catch (fatal flaw), PCP benefit quantification, WellFi diagnostics | Equal to 1st |
| Lead Engineer | Moderator | Product constraint (ESPCP kills WellFi market), question reframe, adversarial assessment | Strategic |
| Gemini | Advisor | Off-topic (0/3 successful reviews). Useful EUE dimension data only. | Low |

## Unresolved Questions

1. Liquid fallback at 80,000 cP / 86 deg — unproven (the single biggest unknown)
2. External geometry profile optimization — lip ring vs fins vs swept baffles
3. Sand accumulation in collector features over time
4. Casing collar clearance — max projection ~0.9" after accounting for eccentricity
5. Retrievability — tapered lead-in required to prevent hang-up during POOH

## Action Items

- [ ] FreeCAD: Model the collector sub — external geometry on 2-7/8" EUE joint
- [ ] Flow loop: Define bench-test at 1,000-10,000 cP analog fluid
- [ ] CFD: OpenFOAM parametric study on fin angle, projection, count
- [ ] Economics: Value of 10-25% gas reduction across 210-well fleet
- [ ] Patent search: Q2 ALS and others for annular passive separation IP
- [ ] Acquire: SPE-215112, Shroud-type separator (JPT 2021)

## Lessons Learned (Post-Discussion Audit)

1. **Product constraints must be in the Lead Engineer's context.** RT1 recommended ESPCP which would kill WellFi's market. Fixed by adding WellFi product context to lead-engineer.md.
2. **The cascade catches fatal flaws that parallel dispatch misses.** The coupling clearance issue only emerged because Well Performance reacted to Multiphase Flow's specific design — this wouldn't happen if both answered independently.
3. **Gemini's adversarial capability is unreliable.** 0/3 successful challenges. It validates or hallucinates. Lead Engineer's own assessment was more valuable.
4. **Multiphase Flow Specialist keeps doing manual arithmetic.** Third occurrence. The instruction is in the agent definition but Sonnet-tier execution doesn't reliably follow it under roundtable pressure.
