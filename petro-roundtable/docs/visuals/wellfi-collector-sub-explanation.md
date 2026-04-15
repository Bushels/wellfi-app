# WellFi Collector Sub — Engineering Explanation

**Purpose:** Explain the asymmetric low-side collector concept to a downhole tool engineer.

---

## The Problem

OBE's Bluesky wells produce 8 API bitumen at 80,000 cP through rod-driven PCP at 86° inclination. Gas interference at the PCP intake causes:
- Erratic pump fillage (gas slugs displace liquid at the pump)
- Concentrated thermal stress in discharge stator stages (SPE-95272: 4x steeper pressure gradient at high GVF)
- Shortened PCP run life (5-month average at OBE, vs 12-24 month target)
- Each pump change costs $49,000

Standard downhole gas separators (Poor-boy, Packer-style) rely on gravity — gas bubbles rise upward through liquid. **At 80,000 cP, this mechanism fails catastrophically.** A 2mm gas bubble rises at 0.05 mm/s — it would take 5.7 hours to rise one meter. The standard McCoy sizing method gives 0.23 bbl/d separator capacity vs 190 bbl/d required (836x shortfall).

## The Physics Insight — Why 86° Changes Everything

At 86° from vertical, gravity decomposes into two components:

- **Transverse** (perpendicular to wellbore, toward the low side): sin(86°) × g = **0.998g** — nearly full gravity
- **Axial** (along the wellbore): cos(86°) × g = **0.07g** — only 7% of gravity

**Transverse gravity is 14x stronger than axial gravity.** This means:

1. Liquid doesn't "fall back" along the wellbore axis (the mechanism conventional separators and the WhaleShark exploit at 40-60°)
2. Instead, liquid **drains transversely to the LOW SIDE of the casing** and pools as a crescent-shaped reservoir along the bottom
3. Free gas (coalesced Taylor bubbles from slug flow) rides the **HIGH SIDE** of the casing

At near-horizontal inclination, the wellbore naturally stratifies: heavy liquid on the bottom, light gas on the top. The question is: can we exploit this stratification with a simple geometry change to the WellFi tool string?

## The Design — Asymmetric Low-Side Collector Lip

The WellFi Collector Sub is a 2-foot tubing joint with **external geometry on the low side only**:

### What it is:
- A 610mm (24") sub that replaces a standard tubing joint in the WellFi BHA
- Full 2-7/8" EUE drift bore (2.441") — rod string and couplings pass through unaffected
- A **180-degree half-moon lip** machined onto the low side of the tubing OD, projecting 23mm into the casing-tubing annulus
- The lip is angled at 15-20° (swept back) to act as a passive scoop
- The **upper 180 degrees has NO lip** — this is the gas bypass corridor
- A 1/2" bypass port with ball check valve on the high side prevents restriction during pump startup

### How it works:

1. **Slug flow delivers intermittent liquid and gas** traveling uphole from the horizontal lateral toward the PCP
2. **Between slugs**, the liquid film on the casing wall drains transversely by gravity (sin(86°) = 0.998g) to the LOW SIDE, forming a crescent pool
3. **The low-side lip intercepts this crescent pool.** Liquid flowing uphole along the bottom of the casing hits the angled lip and is deflected radially inward, toward the tubing body
4. **Liquid accumulates behind the lip**, raising the local liquid holdup immediately downstream
5. **Free gas continues unobstructed** through the upper 180° corridor — no turbulence, no foam generation, no pressure drop
6. **The WellFi sonde sits just below the collector.** The enriched-liquid zone above the collector provides a more stable P/T reading with less gas interference

### Why the rod string doesn't matter:

The rod string is **inside the tubing**. The collector lip is **outside the tubing**, in the casing-tubing annulus. They are on opposite sides of the tubing wall (0.217" J55 steel). Rod rotation at 260 RPM creates friction on the tubing bore — it has zero effect on the external annular flow. This is the key advantage of the external-geometry design.

### Why it's asymmetric (not a full ring):

At 86°, gas and liquid are on opposite sides of the casing. A full 360° lip ring would:
- Obstruct the gas bypass path on the high side (bad — creates turbulence and foam)
- Create unnecessary flow restriction
- Add no value where there's no liquid to capture (upper 180° is gas only)

The half-moon design gives the liquid a collection surface WHERE THE LIQUID IS (low side) and gives the gas an unobstructed path WHERE THE GAS IS (high side).

## Expected Performance

**Efficiency: 5-15% gas bypass prevention** vs bare tubing.

This is an honest estimate. We are not claiming 100% separation — that's physically impossible at 80,000 cP. What we ARE claiming:

- During each slug flow reversal (momentary downflow events), the collector captures some of the liquid that would otherwise be carried uphole mixed with gas
- This enriches the liquid fraction at the PCP intake by 5-15%
- At OBE's conditions, this reduces GVF at the pump intake from (for example) 0.55 to 0.47 — crossing the critical 0.5 GVF threshold where PCP thermal stress becomes nonlinear (Bratu, SPE-95272)

**What 5-15% means operationally:**
- Reduced thermal stress on PCP discharge stages → longer elastomer life
- More consistent pump fillage → fewer pump-off events
- Cleaner WellFi P/T signal → better diagnostics for pump optimization
- Estimated value: ~$10,000/well/year in reduced pump change frequency

## What If It Doesn't Work?

**Worst case: the collector sub is a benign spacer.** It adds no flow restriction (full drift bore, bypass port for startup), no hang-up risk (bull-nose taper on leading edge), and no interference with the rod string. If the lip doesn't capture any liquid, it's just a piece of steel in the BHA that does nothing. No harm.

Over weeks, sand-laden bitumen may fill the lip recess, smoothing it back to a cylindrical profile. At that point it IS a spacer sub. But even if it works for only the first few weeks of a pump run — when GVF is highest and pump stress is greatest — the value is captured.

## What Makes This Different from a WhaleShark

| Feature | WhaleShark | WellFi Collector Sub |
|---|---|---|
| Length | 18 ft (5.5m) | 2 ft (0.6m) |
| Mechanism | Axial liquid fallback into upward-facing collector | Transverse liquid stratification capture on low side |
| Best inclination | 40-60° (tested to 80°) | 86° (exploits near-horizontal stratification) |
| Rod compatibility | Problematic (rod opposes fallback) | No issue (rod is inside tubing) |
| Separate tool? | Yes — standalone product | No — integrated into WellFi BHA |
| Trip cost | Additional trip or extended BHA | Zero — replaces a standard tubing joint |
| Cost | ~$5,000-10,000 (estimated) | ~$500-1,000 (machined tubing joint) |

## What Needs to Happen Next

1. **FreeCAD model** — Detailed CAD of the sub geometry, thread connections, casing collar clearance
2. **Flow loop test** — Even a glycerin/water analog at 1,000-10,000 cP in an inclined annular test section would validate the liquid capture mechanism
3. **Field trial** — Deploy on OBE 102 HZ 16-18 (already instrumented with WellFi). Compare pre/post WellFi P/T data to measure the effect on gas interference
4. **Patent search** — Verify no existing IP covers asymmetric annular passive separation on tubing

## Key Numbers for Quick Reference

| Parameter | Value |
|---|---|
| Oil viscosity (dead) | 80,000 cP |
| Oil viscosity (live, GVF<40%) | 44,800 cP (SPE-136665) |
| 2mm bubble rise velocity | 0.049 mm/s (Stokes' law) |
| Sand settling velocity (120μm) | 0.0003 mm/s |
| Annular flow velocity | 13.31 mm/s |
| Coalescence time | 10-20 min (Maini 1999) |
| Residence time at 15m | 19.7 min (marginal) |
| Transverse gravity at 86° | 0.998g (14x axial) |
| Collector projection | 23mm radial |
| Expected efficiency | 5-15% gas bypass prevention |
| PCP life savings | ~$10K/well/year |
| Worst case | Benign spacer sub |
