# Roundtable #4: WellFi Collector Sub — Viscosity Correction

**Date:** 2026-04-16
**Confidence:** MEDIUM (upgraded from LOW-MEDIUM in RT3)
**Primary Recommendation:** Design survives viscosity correction, REVISED to 4-lip / 36" / 28% restriction with scooped-underside lip profile + drain ports. Bench validation required before fab.

---

## Convening Context

All three prior roundtables (RT1, RT2, RT3) assumed dead oil viscosity of 80,000 cP. During the RT4 preparation phase, the Element lab oil analysis for OBE 102 HZ 16-18 was located and read:

- **Dead oil viscosity (absolute, ASTM D4052/D341):**
  - 8,320 cP at 20°C
  - 1,320 cP at 40°C
  - 379 cP at 60°C
- Density: 990.8 kg/m³ (SG 0.9917, 11.3° API)
- BS&W: 5.02% | Sulfur: 6.11% | Pour point: 3°C
- Sample type: sales oil (cleaned, after surface processing)

The 10x viscosity discrepancy between the lab measurement (this well's actual oil) and the CSEG Recorder regional value (80,000 cP, used in prior roundtables) triggered this roundtable.

**Three plausible downhole viscosity cases modeled:**
- **Base case:** 8,320 cP dead / 4,660 cP live (direct measurement)
- **Conservative case:** ~20,000 cP dead / ~11,200 cP live (sales-oil correction)
- **Old assumption:** 80,000 cP dead / 44,800 cP live (CSEG regional — NOT representative of this well)

---

## Discussion Summary

### Phase 2: Multiphase Flow (1st-order)

Ran `collector_sub_simulation.py` at all three viscosity cases. Key finding: the critical threshold that shifted at 8,320 cP is **gravity migration time vs. lip-to-lip transit time**.

| Parameter | 80k (RT3) | 20k | **8.3k (base)** |
|---|---|---|---|
| Reynolds number | 0.036 | 0.146 | 0.351 |
| Wall shear stress | 118 Pa | 29 Pa | 12 Pa |
| 10mm bubble rise | 1.20 mm/s | 4.82 mm/s | **11.58 mm/s** |
| Migration time (62mm gap) | 52 s | 13 s | **5 s** |
| Lip-to-lip transit | 11.4 s | 11.4 s | 11.4 s |
| Gravity vs transit | LOSES | Marginal | **WINS** |
| Simulated gas freed | 79.9% | 69.1% | 57.1% |

**Key falsifications:**
- "Gravity separation impossible" — PARTIALLY FALSIFIED. True for 2mm dispersed foam, FALSE for 10mm coalesced bubbles at 4,660 cP.
- "Stratified flow impossible" — still true (Gokcal 587 cP threshold), but margin tightened from 76x to 4.4x.

**Mechanism attribution shift:** At 80k cP, only shear coalescence mattered. At 4,660 cP, the mechanism becomes two-stage:
- **Stage 1 (at lip):** Viscous shear coalesces micro-bubbles into larger bubbles
- **Stage 2 (between lips):** Gravity stratifies coalesced bubbles to high side before re-entrainment

The asymmetric low-side lip geometry becomes MORE defensible — it now works WITH gravity instead of substituting for it.

### Phase 3: Well Performance (2nd-order)

Agreed with mechanism analysis but added two hard constraints:

**HC1 (design-changing):** Sand settling at 4,660 cP is 10x faster than at 44,800 cP (0.3 mm/s vs 0.03 mm/s). Low-side lip recirculation zones become preferential sand accumulation sites. Over 5-month run life at 190 bbl/d with 2-8% sand cut, 10-40 m³ of sand transits the sub. Lip geometry must be self-cleaning or include sand-bypass channel.

**HC2 (design-changing):** Retrievability — standard fishing neck, no wireline snag points.

**Commercial reframing (soft constraint, but material):**
- Run 1 and Run 2 WellFi failures were NOT GVF failures (clamp slide, adhesive separation)
- 5-month PCP life is driven by 86° rod wear, not gas ingestion
- Correct value prop: "WellFi signal quality + gas-kick tolerance + proactive wear detection," NOT "PCP run-life extension"
- Supporting evidence: Apr 3 Run 3 payload success improved 66%→97% after pulling one joint (shorter slugs → better CRC recovery)

### Phase 3b: Multiphase Flow Defense/Integration

Accepted HC1 and HC2. Identified that the coalescence zone (upper recirculation eddy off lip crest) and sand zone (lower stagnation corner) are NOT the same region — geometrically separable.

Proposed solution:
- **Scooped-underside lip profile** (15-20° downslope on lip underside): self-sheds sand axially while upstream face creates shear layer
- **4× ¼" drain ports per lip** at wall junction: belt-and-suspenders on sand

Revised optimum for signal-quality value prop:
- **4 lips** (not 3) — more fragmentation events per sub
- **36" sub** (not 24") — room for better lip spacing
- **28% restriction** (not 30%) — lower ΔP, more stages fit

Validation matrix expanded to three dimensionless numbers:
- Capillary number (shear coalescence)
- Bond number (gravity vs surface tension)
- Particle Reynolds + density ratio (sand dynamics)

---

## Weight Map

| Specialist | Order | Key Contribution | Weight in Final |
|---|---|---|---|
| Multiphase Flow | 1st | Mechanism analysis across three viscosity cases; shear+gravity story; final design geometry | HIGH — anchored recommendation |
| Well Performance | 2nd | Hard constraints on sand + retrievability; commercial reframing; Run 3 data interpretation | HIGH — modified design + changed value prop |
| Multiphase Flow (defense) | 1st return | Geometry solution (scooped profile + drain ports); shifted to signal-quality optimum | HIGH — design closed |
| Geoscientist | 3rd (not dispatched) | Would have validated viscosity range | NOT NEEDED — lab data sufficient |

---

## Final Design (RT4)

| Parameter | RT3 (80k cP) | **RT4 (8.3k cP base)** |
|---|---|---|
| Sub length | 24" | **36"** |
| Number of lips | 3 | **4** |
| Lip restriction | 30% | **28%** |
| Lip geometry | Asymmetric low-side half-moon | **Asymmetric + scooped underside** |
| Sand handling | (not addressed) | **4× ¼" drain ports per lip** |
| Fishing neck | Standard | Standard (confirmed) |
| Material | Conductive steel | Conductive steel |
| Bore | Full drift | Full drift |
| Location | Below WellFi sonde | Below WellFi sonde |
| Mechanism | Shear coalescence only | **Shear coalescence + gravity stratification** |
| Value prop | Pump-life extension | **WellFi signal quality + gas-kick tolerance** |

---

## Lead Engineer Adversarial Assessment

**1. Retrievability under partial plugging:** Drain ports may plug with paraffin/asphaltene (6% sulfur oil). If scooped profile alone must clear full load, insufficient confidence without bench test. **Bench gate must include sand loading with flow cycling before fab commitment.**

**2. Scooped profile at Re = 0.35:** Creeping flow shear layer behavior not the same as high-Re NACA intuition. Removing sharp underside corner may collapse the recirculation eddy and kill coalescence. **CFD screening or bench flow visualization required before committing to scooped profile.** Square-edge lip + drain ports is the safer fallback.

**3. Software-only alternative:** Before $6+ months of hardware development, run a 2-week firmware prototype for WellFi gas-event packet filtering using Run 3 data. If firmware alone achieves >90% payload success during gas events, the sub's value prop collapses. **Cheap sanity check that could save significant development cost.**

**4. Viscosity uncertainty window:** Design must bracket 8.3k-40k cP without performance cliff. Current simulation shows monotonic degradation — need to confirm no discontinuities (e.g., eddy regime change).

**5. P.Eng stamp question:** Would NOT stamp for immediate fab. Would stamp for bench validation gate. The RT4 design is more defensible than RT3 but still untested at corrected viscosity, scooped profile, and sand dynamics.

---

## Unresolved Questions

1. **PVT sample from this well** — would collapse the 8.3k-20k-40k uncertainty window
2. **CFD screening of scooped profile** — does the shear layer survive at Re = 0.35?
3. **Coalescence kinetics at 2-5k cP** — Maini 1999 data extends to higher viscosities only
4. **Firmware alternative efficacy** — can packet filtering alone achieve the signal-quality benefit?
5. **Formation regional variation** — is 8.3k cP representative of all OBE Peace River wells, or specific to this one?

---

## Action Items

### Immediate (before any fab)
- [ ] **Build `signal_quality_vs_gvf.py`** — quantify CRC rate vs intake GVF, iterate on lip count/spacing (CALCULATION GAP)
- [ ] **Build `sand_transport_in_sub.py`** — settling velocity + recirculation residence time (CALCULATION GAP)
- [ ] **Build `stratified_migration.py`** — gravity-assisted bubble stratification with axial advection (CALCULATION GAP)
- [ ] **2-week firmware prototype**: WellFi gas-event packet filtering using Run 3 Apr 3 data. If >90% payload success achievable in software, reassess hardware business case.
- [ ] **CFD screening of scooped lip profile** at Re = 0.35 (OpenFOAM or commercial)

### Bench validation gate (6-8 weeks, REQUIRED before fab)
- [ ] Flow loop test at matched Ca + Bo + Re_p + density ratio (glycerin/water + glass beads + air)
- [ ] Sand loading with flow cycling (simulate PCP restart events)
- [ ] Flow visualization (dye tracers) to confirm shear layer survival behind scooped lip
- [ ] Sensitivity at 8.3k, 20k, 40k cP-equivalent conditions

### If bench validates
- [ ] Prototype fab (ONE unit)
- [ ] Single-well field trial on next OBE deployment
- [ ] 6-month field data collection before fleet expansion

### Data / field gaps
- [ ] Request PVT sample from OBE for next Bluesky well (viscosity + GOR at reservoir conditions)
- [ ] Request viscosity-vs-depth profile (account for 22x formation gradient)

### Documentation
- [ ] Update `bluesky-formation.md` KB with "Obsidian-specific viscosity" note (8.3k cP measured, vs 80k cP regional average)
- [ ] Update `wellfi-collector-sub-explanation.md` with corrected mechanism story (shear + gravity, 4-lip / 36" / 28%)
- [ ] Regenerate `wellfi-collector-sub-mechanism.png` visual with revised physics and design

---

## Gemini Advisor Review

**Not invoked for this roundtable.** Per roundtable skill guidance and the Lead Engineer's own policy (Gemini adversarial review failed 0/3 in prior roundtables), the Lead Engineer's adversarial assessment above is the primary quality gate. Gemini was rate-limited at time of roundtable — would have been limited to factual lookups only per protocol.

---

## Post-Discussion Audit

**Knowledge gaps identified:**
- `bluesky-formation.md` listed 80,000 cP as Bluesky "top of reservoir" viscosity without disambiguating measured vs regional-average data. Will add caveat.
- `wellfi-telemetry.md` §1 lacks tabulated noise signatures vs viscosity/GVF — need characterization from Run 3 data.
- No calculation script exists for gravity-assisted stratification with axial advection (central to RT4 mechanism story).

**Agent improvements:**
- Multiphase Flow agent definition could add HARD RULE: "Always verify lab-measured oil properties for the specific well before extrapolating from formation averages."
- Lead Engineer should consider adding a pre-roundtable checklist: "Verify data inputs are well-specific, not regional averages."

**Relevance ordering feedback:**
- 1st order (Multiphase Flow) + 2nd order (Well Performance) was sufficient. Geoscientist not needed once lab data was located.
- Defense round (Phase 3b) was necessary — caught the sand/coalescence zone interaction that would have been missed in pure cascade.
- Total: 3 dispatches, converged cleanly. No wasted specialists.

**Cascade quality:** Cascade caught two design-changing constraints (HC1 sand, HC2 retrievability) that would have been missed in parallel dispatch. This validates the sequential-reactive protocol.

---

## Branch Context

- Prior roundtables: `2026-04-15-wellfi-separator-integration.md` (RT2), RT3 presented in-conversation but not committed
- This roundtable reflects: `8,320 cP` correction from Element lab report discovered 2026-04-16
- Design changes: 3-lip → 4-lip, 24" → 36", 30% → 28%, added scooped profile + drain ports
- Mechanism changes: shear-only → shear + gravity stratification
- Value prop changes: pump-life extension → signal quality + gas-kick tolerance
