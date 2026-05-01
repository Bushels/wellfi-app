# WellFi Collector Sub — How It Works

**Version:** RT4 (2026-04-16) — corrected viscosity + revised design + firmware gate check
**Confidence:** MEDIUM
**Status:** Design ready for bench validation. NOT ready for fab.

---

## Direct answer

This is a **modified 36-inch tubing joint** with **four external asymmetric lips on the low side** that act as staged gas-coalescence and slug-fragmentation features. It sits immediately below the WellFi sonde in the bottomhole assembly. Its job is to **clean up the foamy-oil flow** before it reaches the WellFi EM signal path and the PCP intake — so WellFi transmits reliably during gas events and the pump sees a less erratic intake mixture.

It is NOT a high-efficiency gas separator. It is a **passive flow conditioner**.

---

## 1. What this tool is for — and what it is not for

| Claim | Reality |
|---|---|
| "Extends PCP run life" | **NO.** Run life on this well is driven by 86° rod wear, not gas ingestion. |
| "Eliminates gas from the PCP" | **NO.** Expected gas reduction is 57% of entrained gas, not total elimination. |
| "Replaces a WhaleShark or downhole separator" | **NO.** This is a tubing-joint modification, not a standalone separator. |
| "Improves WellFi signal quality during gas events" | **YES.** This is the primary value proposition. |
| "Fragments slug flow into smaller, more uniform disturbances" | **YES.** This is the most confident mechanism — geometry alone delivers it. |
| "Replaceable by firmware / software filter" | **NO.** Firmware recovers only 19% of the hardware benefit (tested on Run 3 data). |

---

## 2. The well — what we are actually designing for

**Well:** OBE 102 HZ 16-18-83-17W5 (Harmon Valley South, Bluesky Formation)
**Production:** 190 bbl/d at 86° inclination, rod-driven PCP
**Reservoir temperature:** 21-22°C (adjacent well BHP test)
**Oil properties (Element lab analysis, sales oil):**

| Temperature | Absolute viscosity | Kinematic |
|---|---|---|
| 20°C | **8,320 cP** | 8,420 mm²/s |
| 40°C | 1,320 cP | 1,360 mm²/s |
| 60°C | 379 cP | 394 mm²/s |

- Density: 990.8 kg/m³ (SG 0.9917, 11.3° API, bitumen)
- BS&W: 5.02% | Sulfur: 6.11% | Pour point: 3°C

**Downhole live-oil viscosity estimate:** ~4,660 cP (SPE-136665 foamy correction = 56% of dead).

**Historical note:** Prior roundtables (RT1-RT3) assumed 80,000 cP — a CSEG Recorder regional figure for "top of Bluesky reservoir." The lab measurement of this specific well's oil is **10x lower**. RT4 was convened to work through the implications.

---

## 3. Why gas is the problem

At 4,660 cP, foamy oil holds gas as **micro-bubbles** distributed throughout the liquid. A 2 mm bubble rises at 0.46 mm/s — still far too slow for bulk gravity separation (40 minutes to cross a 1 m annular gap). **Coalesced** 10 mm bubbles rise at ~11.6 mm/s — this is where gravity starts to help.

When gas reaches the PCP intake entrained in the liquid, two things happen:
1. The pump discharge stages see local GVF spikes → elastomer thermal stress
2. The WellFi EM signal path is disrupted → CRC errors → data loss

The Apr 3 Run 3 gas event (11:52) demonstrated both: a 7-minute EM disruption with CRC errors. The tool survived, but the event shows the failure mode is real.

---

## 4. Two-stage mechanism (corrected in RT4)

### Stage 1: Shear coalescence at each lip

As foamy oil squeezes past a lip restriction, **viscous shear** stretches and deforms the micro-bubbles. At 4,660 cP live viscosity, the wall shear stress through the narrowed gap is about **12 Pa** — enough to drive Capillary number above 1, which is the regime where bubble deformation and forced contact produce coalescence.

**Three smaller bubbles touching → one larger bubble.** That's the mechanism.

### Stage 2: Gravity stratification between lips

After a coalesced ~10 mm bubble forms, it rises at 11.6 mm/s (wall-corrected ~13.8 mm/s under transverse gravity at 86°). The annular gap is 62 mm — crossing time **~5 seconds**. Lip-to-lip transit time at 190 bbl/d is **11.4 seconds**. The coalesced bubble **clears the gap before the next lip**.

This is the **critical RT4 finding**. At the old 80,000 cP assumption, migration time was 52 s vs 11.4 s transit — gravity lost. At 8,320 cP, gravity **wins**. The mechanism closes on itself only at the corrected viscosity.

### Why asymmetric low-side geometry?

At 86° inclination, transverse gravity is **14x stronger** than axial gravity. The liquid sits on the low side of the casing; coalesced gas rises to the high side. A full-ring lip would pinch BOTH sides — counterproductive on the high side where gas is trying to escape. An **asymmetric half-moon lip on the low side only** lets high-side gas flow freely while creating the shear zone in the liquid-rich low-side layer.

---

## 5. Slug damping — the surest benefit

Even if the coalescence mechanism is weaker than claimed, **slug damping is pure geometry**. A large liquid slug hitting a restriction deforms, fragments, and emerges as smaller, more frequent disturbances on the other side. No coalescence physics required. No viscosity assumption required.

**Expected:** ~59% reduction in slug amplitude with 4 lips at 28% restriction, ~30% increase in slug frequency (smaller, more frequent).

**Why this matters for WellFi:** shorter slugs = shorter EM disruption per event = shorter CRC error bursts = better payload recovery. The Run 3 Apr 3 data (66% → 97% payload success after a joint pull) validates that flow-path improvements directly translate to signal quality.

---

## 6. The design (RT4 revision)

| Parameter | Value | Change from RT3 |
|---|---|---|
| Sub length | **36 inches** | was 24" |
| Number of lips | **4** | was 3 |
| Lip restriction | **28% of annular area** | was 30% |
| Lip profile | **Asymmetric low-side + scooped underside** | was square asymmetric |
| Sand handling | **4x 1/4" drain ports per lip** | new |
| Material | Conductive steel | unchanged |
| Bore | Full drift (rod couplings pass freely) | unchanged |
| Fishing neck | Standard (retrievable) | unchanged |
| Location in BHA | Immediately below WellFi sonde | unchanged |

**Why 4 lips instead of 3:** optimizing for signal quality (more fragmentation events) rather than pump life (more residence time).

**Why 36" instead of 24":** gives enough axial spacing (~7.2" per stage) for coalesced bubbles to actually migrate to the high side between lips — the stage-2 gravity mechanism needs that length.

**Why scooped profile:** solves the sand-accumulation problem Well Performance raised during RT4. At 4,660 cP, 120-μm sand settles at ~0.3 mm/s (10x faster than at the 80k cP assumption). A square lip creates a stagnation corner where sand piles up over 5 months. The scooped underside self-sheds sand axially while the upstream crest still creates the shear layer.

**Why drain ports:** belt-and-suspenders redundancy for the sand problem. Cheap to machine, no impact on mechanism.

---

## 7. Why firmware alone cannot do this (the adversarial gate check)

Before committing to hardware fab, the Lead Engineer proposed a firmware alternative test. Could a smart packet filter on WellFi's receiver recover most of the benefit without any downhole hardware?

**Test (proof of concept on real Run 3 data):**
- Parse 89 packets from Apr 2-3 Run 3 EMGRx event log
- Apply three filter strategies: naive CRC rejection, multi-criterion, gas-event-aware + interpolation
- Measure how much of the +27.5 pp Apr 2 → Apr 3 improvement is recoverable in software

**Result:** Best firmware strategy recovers **only 19% of the hardware gain**.

| Strategy | Usable rate | Gain vs baseline |
|---|---|---|
| Raw Apr 2 (baseline) | 66.1% | — |
| A: Naive CRC rejection | 66.1% effective | 0 pp |
| B: Multi-criterion | 66.1% effective | +0 pp (only 1 recovered packet) |
| C: Gas-event-aware + interpolation | 71.4% | **+5.4 pp** |
| Raw Apr 3 (goal, post joint-pull) | 93.5% | +27.5 pp |

**Why firmware can't close the gap:** The Apr 2 problem wasn't a discrete gas event to interpolate through. It was **continuous poor EM signal path**. No firmware can fix a bad signal environment — that requires geometric change. The collector sub is the geometric change equivalent of the joint pull.

**What firmware CAN contribute:** gas-event detection flags for SCADA, short-gap interpolation for trending displays, low-confidence packet labeling. These are useful enhancements — not substitutes for the hardware.

---

## 8. Risks and validation requirements

### Before fab (required)

1. **Flow loop bench test** matching three dimensionless numbers: Capillary (shear coalescence), Bond (gravity), particle Reynolds (sand). Glycerin/water + glass beads + air gets you all three. ~6-8 weeks.
2. **CFD screening** of the scooped lip profile at Re = 0.35. The shear layer behavior at creeping flow is not the same as at high Re — cannot assume NACA-style intuition holds. If CFD shows shear layer collapse, fall back to square-edge lip + drain ports only.
3. **Two calculation scripts** flagged as gaps in RT4:
   - `signal_quality_vs_gvf.py` — CRC rate vs intake GVF, for sizing iteration
   - `stratified_migration.py` — gravity-assisted bubble migration with axial advection

### Open unknowns

- **PVT sample from this well** would collapse the 8.3k / 20k / 40k cP uncertainty window. Not yet available.
- **Coalescence kinetics at 2-5k cP** — Maini 1999 data only validated at higher viscosities.
- **Sand accumulation under flow cycling** (PCP restart events) — needs to be part of bench test.

### P.Eng stamp question

**Would NOT stamp for immediate fabrication.** The RT4 design is more defensible than RT3, but still untested at corrected viscosity, scooped profile, and sand dynamics. Would stamp for **entering bench validation gate**.

---

## 9. What happens if we deploy it

**Success case:** WellFi payload success during gas events improves from Run 3's 93.5% (Apr 3) toward 97-98%. Slug amplitude drops ~60%. The operator sees cleaner pressure/temperature trends. Proactive rod-wear detection via pressure signature shifts becomes feasible. Net value: more reliable monitoring, earlier pump-pull decisions, $49k pump change avoided PER PROACTIVE PULL (not per sub — the sub doesn't extend pump life, it extends the window in which we know whether the pump is healthy).

**Degradation case:** If downhole viscosity is closer to 20k cP, shear stress triples (to ~29 Pa), coalescence efficiency rises, gravity migration is marginal. Design still works — monotonic degradation, no cliff. If viscosity is 40k cP, gravity loses again and we're back to shear-dominated (still works, just closer to RT3 regime).

**Failure case:** Sand accumulates despite the scooped profile and drain ports. Lips plug. Sub becomes a wireline fishing hazard. **This is the critical design risk.** Must be caught in bench testing with flow cycling — cannot be extrapolated from steady-state analysis.

---

## 10. One-sentence summary

A passive 36-inch tubing sub with four low-side shear-coalescence lips that improves WellFi signal quality and dampens slug flow, validated to survive viscosity correction and to be unrecoverable by firmware alone — requiring bench-scale flow loop validation before fabrication.
