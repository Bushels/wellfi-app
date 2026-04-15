# Downhole Gas-Liquid-Solids Separation — Knowledge Base

> Curated from 4 technical papers on downhole separator design, sizing, and field performance. Includes heavy oil corrections derived from cross-referencing with foamy-oil-dynamics.md and bubble-dynamics-reference.md. All data points cite source papers.

## Quick Reference Table

| Property | Value | Source |
|---|---|---|
| Side intake velocity ceiling | 6 ft/s (1.8 m/s) onset, 10 ft/s (3.0 m/s) starvation | Saponja 2021, p.4 |
| Eccentric flow path improvement | +30% separation efficiency | Saponja 2021, Figure 2 |
| Upward-facing intake improvement | +50% separation efficiency | Saponja 2021, Figure 5 |
| Turbulence minimization improvement | +25% separation efficiency | Saponja 2021, Figure 4 |
| Round tube vs annulus improvement | +50% (hydraulic diameter effect) | Saponja 2021, Figure 8 |
| Sizing rule (low-viscosity oil) | 50 BPD per sq-in of annular area | McCoy 1998, p.2 |
| Sizing rule basis | 6 in/s gas bubble rise velocity in <10 cP oil | McCoy 1998, p.2 |
| Max inclination for gas separation | 80 deg from vertical | Saponja 2021, p.11 |
| Max inclination for solids separation | 65 deg (angle of repose) | Saponja 2021, p.11 |
| Optimal inclination for gas separation | 40-45 deg (+30% vs vertical) | Saponja 2021, p.11 |
| WhaleShark length | 18 ft (5.5 m) | Saponja 2021, p.9 |
| WhaleShark tensile rating | Equivalent to 2-3/8" EUE coupling | Saponja 2021, p.9 |
| Flow loop separation efficiency | 100% (WhaleShark) | Saponja 2021, p.10 |
| HEAVY OIL CORRECTION: bubble rise at 80,000 cP | 0.022 mm/s for 2mm bubble (vs 150 mm/s in water) | CGW 1978 + Stokes' law |
| HEAVY OIL CORRECTION: correct viscosity for Stokes | Use LIVE oil viscosity, not dead oil (1.6-1.8x difference) | SPE-136665 |
| HEAVY OIL IMPLICATION: separation mechanism | Liquid fallback, NOT bubble rise (bubbles non-rising at 80,000 cP) | Cross-reference synthesis |


---

# Downhole Gas and Solids Separation — WhaleShark Design

**Source:** Saponja, J., Hari, R., David, S., Brignac, J., Jaszan, D. (Oilify); Coyes, C., VanHuss, B. (Q2 Artificial Lift Services); Nagoo, A. (Nagoo & Associates LLC); Penner, B. (Calyx Energy III LLC). "Enhancing Downhole Gas and Solids Separation and Lowering Operational Risk by Taking Advantage of Multi-Phase Flow Reversals." 2021 Southwestern Petroleum Short Course (SWPSC), Paper 2021031.

**Cited as:** Saponja et al. 2021 SWPSC

---

## 1. Separator Types

### Overview

There are three separator types relevant to sucker rod pumping: Poor-Boy (packerless), Packer-Style, and the WhaleShark. All rely on the fundamental principle of counter-current gas bubble rise versus downward liquid velocity — but the WhaleShark breaks this constraint by exploiting liquid fallback instead. (Saponja et al. 2021 SWPSC, p.2)

---

### 1A. Poor-Boy (Packerless) Style

| Attribute | Detail |
|---|---|
| Seal mechanism | None — packerless |
| Separation annulus | Inner annular cross-sectional area (A1, per Figure 1) — the region inside the separator body |
| Fluid entry | Side intakes / slots/ports on separator body |
| Gas venting | Back to casing annulus |
| Solids | Settled into mud joints at base of separator |
| Cost | Generally lower than packer-style |

**How it works:** A concentric pump intake dip tube is placed inside a tubular body mandrel. Side entry slots or ports draw annular fluids into the inner annular separation region (A1). Gas separates in the inner annulus and vents back out through the same side ports to the casing. Separated liquid travels up through the dip tube to the pump intake. Some variants include a vortex flow accessory to assist gas or solids separation. (Saponja et al. 2021 SWPSC, p.2)

**Pros:**
- Packerless — no packer or cup seal risk
- Lower cost
- Solids separation occurs after gas separation (correct process sequence)
- No risk of solids packing above a packer/seal

**Cons:**
- Cross-sectional area A1 is smaller than packer-style A2, reducing separation capacity
- Side intakes create a hard velocity ceiling: separation diminishes above 6 ft/s (1.8 m/s) gas velocity, separator becomes fully liquid-starved at 10 ft/s (3.0 m/s) (Saponja et al. 2021 SWPSC, p.4; Figure 3, Figure 9)
- Separator OD must be larger to maximize A1, which reduces outer annulus cross-section to casing — a physical trade-off
- Concentric (non-eccentric) dip tube positioning limits eccentric flow path benefits (Saponja et al. 2021 SWPSC, p.4)
- Performance governed and limited by gas bubble rise velocity, not liquid fallback

**Operating envelope:** Effective at low-to-moderate gas rates where casing annulus gas velocity adjacent to intake ports remains below 6 ft/s. Performance degrades sharply in slug/churn flow regimes with high GVF. Best suited for low-inclination wells (vertical to moderate deviated). (Saponja et al. 2021 SWPSC, p.4, p.8)

---

### 1B. Packer-Style

| Attribute | Detail |
|---|---|
| Seal mechanism | Packer or cup-type seal (with Tubing Anchor Catcher) |
| Separation annulus | Casing annulus above packer/seal (A2, per Figure 1) — larger cross-sectional area than A1 |
| Fluid entry | Pump intake dip tube positioned just above packer/seal draws degassed liquid from casing annulus |
| Gas venting | Upward through casing annulus to wellhead |
| Solids | Require separate solids separation accessory BELOW packer/seal and upstream of gas separator |
| Cost | Higher than poor-boy |

**How it works:** A packer or cup seal forces all multiphase flow through the separator and discharges it at the top of the separator into the casing annulus above the packer. The large casing annulus (A2) provides higher residence time (liquid travels downward slowly) and greater cross-sectional area than poor-boy A1. The pump intake dip tube draws degassed liquid from the large annulus. (Saponja et al. 2021 SWPSC, p.2–3)

**Pros:**
- Larger separation annulus A2 > A1 — higher separation capacity at equivalent velocity
- Higher liquid residence time in annulus (beneficial for gas bubble rise)

**Cons:**
- Packer/cup seal creates significant workover risk — retrieval is operationally complex and costly
- Solids settle on top of packer/seal, creating stuck-in-hole risk and potential workovers
- Flow path through packer-style is more tortuous than poor-boy, generating turbulence, smaller gas bubbles, foam, and reduced separation (Saponja et al. 2021 SWPSC, p.5)
- Side discharge into casing annulus is a region of significant turbulence and fluid agitation — generates smaller bubbles that rise slower (Saponja et al. 2021 SWPSC, p.5)
- Annular packer can become the smallest cross-sectional area and highest critical liquid lifting gas velocity risk point in the system (TAC restriction problem) (Saponja et al. 2021 SWPSC, p.12)
- Gas entrainment risk (gas entrained in liquid cannot be separated downhole) due to foaming from turbulence

**Operating envelope:** Better than poor-boy at moderate gas rates due to A2 > A1, but turbulence-driven performance degradation limits practical efficiency. Problematic in high-GVF wells and foam-generating fluids. Solids in the produced stream require mandatory pre-separation accessory. (Saponja et al. 2021 SWPSC, p.3, p.5)

---

### 1C. WhaleShark

| Attribute | Detail |
|---|---|
| Seal mechanism | None — packerless |
| Separation region | "No annulus" — fully eccentric open tube above collector (A3, per Figure 11) — A3 > A2 > A1 |
| Fluid entry | Large diameter **upward-facing** collector intake (open top "bucket") |
| Gas venting | Radially upward and circumferentially around collector, then up casing annulus |
| Solids | Gravity + momentum separation system (angled weir + velocity acceleration dip tube on opposite side) into mud joints |
| Length | 18 feet (Saponja et al. 2021 SWPSC, p.9) |
| Tensile rating | Equivalent to 2-3/8" EUE tubing coupling (Saponja et al. 2021 SWPSC, p.9) |
| Structural | Two spiral half-gussets connect rigid bar to oval pump intake tube for torsional strength and guiding |
| Available size example | 35 series: 3.5" OD collector intake inside 5.5" (139.7mm) casing (Saponja et al. 2021 SWPSC, Case Study 6) |

**How it works:** The WhaleShark intentionally takes advantage of transient, ongoing multiphase flow reversals (liquid fallback) in slug and churn flow regimes. The upward-facing collector "bucket" acts as a passive liquid trap — liquid falling backward gravitationally falls into the collector. The eccentric oval pump intake tube is positioned to maximize its distance from the casing center line, maximizing liquid fallback into the collector and creating the "no annulus" separation region (A3) above the collector. Multiphase flow arriving at the collector top enters radially and circumferentially, with the radially inward moving flow creating a funnel shape that guides separated liquid counter-currently down into the upward-facing shroud intake. (Saponja et al. 2021 SWPSC, p.8–10; Figures 11, 12, 13, 14)

**Separation is governed by how fast liquid falls, not how fast gas bubbles rise.** This is the fundamental paradigm shift. (Saponja et al. 2021 SWPSC, p.7)

**Key engineered features:**
1. Large diameter upward-facing collector intake
2. Separation region immediately above collector: "no annulus" using eccentric placement of oval pump intake dip tube
3. Oval pump intake tube — maximizes distance from casing center line, maximizing liquid fallback rate into collector
4. Highly efficient gravity + momentum solids separation (not cyclonic) — separates solids from 0%–200% of flow rate
5. Annular clearance adjacent to collector is reduced to increase multiphase fluid velocity, increasing GVF, forcing bubble coalescence to larger bubbles, and maximizing collector mouth-size intake (Saponja et al. 2021 SWPSC, p.9)
6. Abrupt flow path changes eliminated — minimizes turbulence
7. Packerless — eliminates packer/seal retrieval risk

**Pros:**
- 100% separation efficiency achieved in flow loop testing (Saponja et al. 2021 SWPSC, p.10; Figure 16)
- Not governed by gas bubble rise velocity — can sustain separation through slug and surging conditions where side-intake separators fail
- No packer — lower operational risk, lower workover cost
- Separation capacity A3 > A2 > A1 — largest possible for given casing
- Handles highly variable, sluggy, inconsistent flow from horizontal wellbores
- Gas separation to 80° inclination, solids to 65° inclination (Saponja et al. 2021 SWPSC, p.11)
- At inclinations 40°–45°, 30% more efficient because liquid more easily collects at low side and gas escapes high side (Saponja et al. 2021 SWPSC, p.11)
- Handles high-rate flumping conditions: critical liquid lifting gas velocity in Separation Region requires 48 ft/s in 5.5" casing — liquid continues to fall back even at very high gas velocities (Saponja et al. 2021 SWPSC, p.10)
- Collector remains full with little-to-no gas separation inside the collector during flow loop shutdown (Saponja et al. 2021 SWPSC, p.10; Figure 16)

**Cons:**
- Not suited beyond 65° inclination for solids (angle of repose limit)
- At low GVF bubble flow (<25% gas volume fraction), performance is governed by gas bubble rise velocity like conventional separators (Saponja et al. 2021 SWPSC, p.10)
- Larger physical footprint (18 ft long) requires consideration during installation and retrieval

**Operating envelope:** Slug and churn flow regimes (the dominant regimes for sucker rod and ESP pumping at 30–600 bbl/day liquid, 30–1,000 Mscf/day gas, 150 psi pump intake pressure per Figure 7). Effective from vertical to 80° inclination for gas separation, vertical to 65° for solids. Optimal efficiency window at 40°–45° inclination. (Saponja et al. 2021 SWPSC, p.7, p.11)

---

### Comparative Summary Table

| Feature | Poor-Boy | Packer-Style | WhaleShark |
|---|---|---|---|
| Seal required | No | Yes (packer/cup) | No |
| Separation annulus area | A1 (smallest) | A2 (medium) | A3 (largest, "no annulus") |
| Separation governed by | Gas bubble rise velocity | Gas bubble rise velocity | Liquid fallback rate |
| Side intakes | Yes — limiting above 6 ft/s | Side discharge — turbulence risk | No — upward-facing collector |
| Flow turbulence | Low-moderate | High (tortuous path, side discharge) | Minimized (no abrupt flow changes) |
| Solids process sequence | Gas first, solids second (correct) | Solids must be separated first below packer (adds complexity) | Gas first, solids second (correct) |
| Slug/churn flow tolerance | Poor — pump fillage erratic | Poor-moderate | High — designed for it |
| Gas separation limit | ~80° (side-intake geometry limits lower) | N/A | 80° inclination |
| Solids separation limit | ~65° | ~65° | 65° inclination |
| Retrieval risk | Low | High (packer) | Low |
| Flow loop separation efficiency | Not reported at 100% | Not reported at 100% | 100% (Saponja et al. 2021 SWPSC, p.10) |

---

## 2. Seven Design Improvement Principles

The authors compiled and extensively studied seven mutually exclusive downhole separation improvement opportunity categories. Each was analyzed for the physics mechanism and quantified improvement potential. (Saponja et al. 2021 SWPSC, p.4)

---

### Principle 1: Separation in an Eccentric Flow Path

**The principle:** An annular flow path where the pump intake dip tube is positioned eccentrically (to the side) rather than concentrically allows gas to escape more easily.

**Quantified improvement:** +30% improvement in separation efficiency (Saponja et al. 2021 SWPSC, Figure 2 caption)

**Physics:** Caetano's research found that in annular shaped conduits with upward-flowing co-current and partially counter-current multiphase flow (slug and churn regimes), liquid slippage or liquid hold-up increases with eccentricity of the annular conduit. Gas can escape up a fully eccentric annulus more easily. Rowlan, McCoy, and others confirmed that an eccentric annular flow path allows gas to escape more easily and is more efficient for gas separation. (Saponja et al. 2021 SWPSC, p.4)

**Design implication:** Any annular flow path used for gas separation should be eccentrically shaped. The entire tubing string to surface should ideally be eccentrically positioned inside the casing. For the WhaleShark, the oval pump intake dip tube is intentionally positioned eccentrically to create the "no annulus" eccentric separation region (A3).

---

### Principle 2: Limitations of Side Intakes on Separators

**The principle:** Side intakes/ports create a hard velocity ceiling on separator performance because liquid cannot turn 90° into the intake when annular gas velocity is too high.

**Quantified improvement:** +30% improvement by positioning the side-intake's slots/ports at the largest cross-sectional area on the casing annulus (most likely at the top of the separator, above the inner annulus) (Saponja et al. 2021 SWPSC, p.4–5; Figure 3 caption)

**Critical velocity thresholds (see also Section 3):**
- At 6 ft/s (1.8 m/s): separation capacity begins to diminish — liquid cannot effectively "turn sideways 90°" into intake (Saponja et al. 2021 SWPSC, p.4; Figure 9)
- At 10 ft/s (3.0 m/s): separator becomes fully starved of liquid (Saponja et al. 2021 SWPSC, p.4)
- Note: 6 ft/s is only approximately half of the critical liquid lifting gas velocity — meaning side-intake separators are limited at velocities well below those needed to lift all liquid (Saponja et al. 2021 SWPSC, Figure 3 caption)

**Physics:** Liquid's momentum travelling axially and vertically along the side of the separator cannot effectively turn sideways 90° into the separator's intake at high gas velocities. The higher the annular gas velocity adjacent to the separator OD, the less liquid can enter the side intake slots/ports. The consequence is inconsistent and erratic pump fillage, leading to compressional rod loading events and excessive tubing wear. (Saponja et al. 2021 SWPSC, p.4)

**Design implication:** Eliminate side intakes entirely (WhaleShark solution) or place side intakes at the highest possible cross-sectional area point on the casing annulus. Poor-boy separator intakes should be at the top of the separator, above the inner annulus.

---

### Principle 3: Flow Turbulence Minimization

**The principle:** Minimizing fluid agitation and turbulence during separation maximizes separation efficiency by preserving large bubble sizes.

**Quantified improvement:** +25% improvement in separation efficiency by minimizing fluid agitation and turbulence (Saponja et al. 2021 SWPSC, Figure 4 caption)

**Physics — Stokes' Law bubble rise velocity:**

$$v_{bubble} = \frac{2}{9} \frac{(\rho_{fluid} - \rho_{bubble})}{\mu_{fluid}} g \cdot R^2_{bubble}$$

Bubble rise velocity scales with the square of bubble radius. A 1/8" diameter air bubble in water rises at 1 inch per second; a 1/2" diameter bubble rises at 6 inches per second. The commonly accepted 6 inches per second gas bubble rise velocity for sizing downhole separators is therefore accurate only for large bubbles. Turbulence generates smaller bubbles (by breaking up large bubbles), which rise much more slowly and are much harder to separate. The commonly accepted 6 in/s figure can be misleading if turbulence is generating small bubbles. (Saponja et al. 2021 SWPSC, p.5; Figure 4)

Packer-style separators are particularly prone to turbulence because:
- Flow path from packer base through to side discharge slot is narrow and highly tortuous
- Side discharge into casing annulus causes high-velocity multiphase impingement on casing wall
- Both mechanisms generate smaller bubbles and foam

**Design implication:** Be as gentle as possible with fluids. Eliminate abrupt flow path changes. Avoid side discharges into the annulus. For the WhaleShark: abrupt flow path changes are eliminated to effectively minimize turbulence. (Saponja et al. 2021 SWPSC, p.5, p.9)

---

### Principle 4: Separator Intake Orientation — Taking Advantage of Multiphase Flow Reversals

**The principle:** Re-orienting the separator intake from side-facing to upward-facing allows it to take advantage of transient, ongoing, partial liquid phase flow reversals (liquid fallback).

**Quantified improvement:** +50% improvement in separation efficiency by re-orienting separator intake from side to upward-facing (Saponja et al. 2021 SWPSC, Figure 5 caption)

**Physics:** In inclined-upward and vertical flow in slug and churn flow regimes, multiphase flow reversals are frequent and occur at high frequency. Parts of the liquid phase regularly reverse direction — falling gravitationally backward (downward) while gas continues upward. An upward-facing collector "bucket" passively captures this falling liquid. Liquid falling backwards simply falls into the upward-facing collector. An open top bucket fills faster than a closed top bucket with side slots/ports — the open top captures both upward-moving liquid AND downward-falling liquid (fallback). (Saponja et al. 2021 SWPSC, p.6–7; Figure 5, Figure 6)

Flow reversals progress as gas rate decreases: partially concurrent/partially counter-current → liquid's hydrostatic pressure gradient becomes zero (hanging liquid film field) → fully counter-current liquid flow (maximum liquid accumulation downhole). (Saponja et al. 2021 SWPSC, p.6)

The researched concluded that separation capacity can be preferentially governed by liquid fallback rate rather than gas bubble rise velocity — liquid can fall back faster than gas bubbles rise, enabling much greater handling of slug and inconsistent flow conditions. (Saponja et al. 2021 SWPSC, p.7)

**Operating flow regime context:** At 150 psi pump intake pressure, typical sucker rod and ESP casing flows (30–600 bbl/day liquid, 30–1,000 Mscf/day gas) are predominantly in slug and churn flow regimes — exactly the regimes where flow reversals are most active. (Saponja et al. 2021 SWPSC, p.7; Figure 7)

**Design implication:** Orient separator collector intake upward. This is the single largest improvement opportunity (+50%) identified in the study. WhaleShark collector is explicitly designed as an upward-facing "bucket."

---

### Principle 5: Hydraulic Diameter (Conduit Shape) in the Separation Region

**The principle:** A round tube-shaped separation conduit has a larger hydraulic diameter than an annular conduit of equivalent cross-sectional area, resulting in greater liquid fallback and more separation capacity.

**Quantified improvement:** +50% improvement in separation efficiency with a tube-shaped conduit versus an annulus-shaped conduit (Saponja et al. 2021 SWPSC, p.8)

**Physics:** In a round tube conduit, gas can more easily escape because there is no obstruction along the center line — gas bubbles can form larger Taylor bubbles (elongated bullets) unobstructed. In an annulus, the inner tube wall provides additional contact surface area that can bridge across the annulus and allow liquid to bridge, reducing the rate at which gas can escape. (Saponja et al. 2021 SWPSC, p.7; Figure 8)

Nagoo's critical gas velocity equation for liquids shows that rate of liquid fallback is diameter-dependent. Applying Nagoo's MAPe superficial gas phase velocity model for critical liquid lifting:

**Example calculation at 250 psi pump intake pressure, 200°F, 0.8 gas gravity, 65% water cut, 1.07 water SG, 35° API oil:**
- 5.5" casing (round tube approximation): critical liquid lifting gas velocity = **43 ft/s (13 m/s)**
- 5.5" casing × 2-7/8" tubing annulus: critical liquid lifting gas velocity = **12 ft/s (3.3 m/s)**

The critical velocity is 3.6× higher in the round tube. Liquid can much more easily fall back in a round tube. (Saponja et al. 2021 SWPSC, p.8)

**Hydraulic diameter examples:**
| Conduit | Inner Diameter | Cross-Sectional Area | Hydraulic Diameter |
|---|---|---|---|
| Round tube (4.0" ID) | 4.0" | 12.56 in² | 4.0" |
| Annulus (outer circle minus 1.9" OD inner tube) | equivalent area | equivalent | 2.5" |

Fluid velocities and Reynolds numbers are much lower in round tube of equivalent cross-sectional area versus annulus — greater amounts of flow reversals and liquid fallback occur in a round tube shaped conduit. (Saponja et al. 2021 SWPSC, p.8)

**Design implication:** Use a tube-shaped (non-annular) separation region above the collector. WhaleShark's "no annulus" separation region (A3) achieves this by placing the oval pump intake dip tube eccentrically to one side — the dominant cross-section of the separation region is functionally a tube with an open center line.

---

### Principle 6: Process Sequence for Solids Separation

**The principle:** Separate gas first, then separate solids from the degassed liquid. This is the correct and more efficient process sequence.

**Quantified improvement:** Not quantified as a standalone percentage — described as "far more effective and efficient" (Saponja et al. 2021 SWPSC, p.8)

**Physics:**
- If gas is not removed first, the fluid will have high velocities due to the gas phase, challenging solids separation through erosion and carry-over of solids risk
- Gas bubbles in the fluid increase effective viscosity, particularly in foamy fluids, slowing settling velocity per Stokes' Law — gas presence makes solids harder to settle
- With gas removed and lower liquid velocities, solids can be more efficiently separated by gravity
- Poor-boy separators naturally achieve this correct sequence (gas separation, then solids into mud joints below)
- Packer-style separators require a solids accessory BELOW the packer/seal and UPSTREAM of the gas separator — this is the wrong sequence, or requires additional complexity (Saponja et al. 2021 SWPSC, p.8)

**Design implication:** Install solids separation system below or downstream of the gas separator, not upstream. WhaleShark: angled weir guides liquids/solids to velocity acceleration dip tube (intentionally on the opposite side of the pump intake tube). Pump intake tube is positioned vertically shallower than the lowermost edge of the weir's velocity dip tube — liquid must always move upward against gravity to reach the pump intake tube, which assists solids separation. Degassed, solids-free liquid must travel upward and across to the pump intake tube, gravitationally settling solids into the sump/mud joints. (Saponja et al. 2021 SWPSC, p.11)

---

### Principle 7: Slug Flow Tolerance

**The principle:** Downhole separators must tolerate highly inconsistent, sluggy flow from horizontal wellbores without causing pump shutdown or erratic pump fillage.

**Quantified improvement:** Not quantified as a standalone percentage — framed as a design requirement for horizontal wells (Saponja et al. 2021 SWPSC, p.8–9)

**Physics:** Flow emanating from a horizontal wellbore is commonly inconsistent and sluggy. Slug flows are characterized by:
- Larger amplitude, lower frequency slug flow from toe-up trajectories (fluid pools in wellbore toe, then unloads)
- Smaller amplitude, higher frequency slug flow from near-heel near the separator
- Slug flow is particularly severe at inclinations between 20°–60° (highest multiphase fluid level slippage)
- A wellbore's directional survey primarily in toe-up orientation greatly increases slug flow (Saponja et al. 2021 SWPSC, p.9; Figure 10)

Casing gas velocity fluctuation above 140 Mscf/day (4 × 10³ m³/day) in 5.5" casing can exceed the 6 ft/s limit for side intake separators, causing immediate liquid starvation of the pump. (Saponja et al. 2021 SWPSC, p.9; Figure 9)

The annular fluid level pump-down mechanism during high gas surges can create a vicious on/off pumping cycle: gas velocity lifts all liquid above TAC → liquid column builds above TAC as pressure builds → gas velocities subside → fillage returns → cycle repeats multiple times per day. (Saponja et al. 2021 SWPSC, p.12)

HEAL System® and small internal diameter tailpipe in the well's bend section have been tried to stabilize slug flow but have had operational risk challenges (talipes can damage). (Saponja et al. 2021 SWPSC, p.9)

**Design implication:** WhaleShark: governed by liquid fallback rate (not gas bubble rise), which means high pump fillage is sustained through slug/surge events as long as gas velocities in the Separation Region do not reach the critical liquid lifting gas velocity (48 ft/s in 5.5" casing). Consistent pump fillage during flumping is now achievable. (Saponja et al. 2021 SWPSC, p.10)

---

### Seven Principles Summary Table

| # | Principle | Improvement | Key Physics |
|---|---|---|---|
| 1 | Eccentric flow path | +30% | Higher liquid hold-up + easier gas escape in eccentric annulus (Caetano research) |
| 2 | Side intake placement at largest CSA | +30% | Reduces annular gas velocity adjacent to ports; liquid turns 90° more easily |
| 3 | Turbulence minimization | +25% | Stokes Law: bubble rise ∝ R². Small bubbles rise much slower; turbulence creates small bubbles |
| 4 | Upward-facing intake (flow reversals) | +50% | Liquid fallback rate > gas bubble rise rate in slug/churn; open bucket fills faster |
| 5 | Round tube separation conduit | +50% | Hydraulic diameter 4.0" (tube) vs 2.5" (annulus): critical liquid lifting velocity 43 vs 12 ft/s |
| 6 | Gas-first solids process sequence | Qualitative | Lower velocity + lower viscosity after degassing improves solids settling per Stokes Law |
| 7 | Slug flow tolerance | Design req. | Horizontal wellbores generate highly variable sluggy flow; separator must operate 0%–200% of pump rate |

*All citations: Saponja et al. 2021 SWPSC, pp.4–9 and corresponding Figures 2–10*

---

## 3. Critical Velocity Thresholds

### 3A. Side-Intake Separator Velocity Limits

| Threshold | Velocity | Effect | Citation |
|---|---|---|---|
| Side intake limitation onset | 6 ft/s (1.8 m/s) superficial gas phase velocity in casing annulus adjacent to ports/slots | Liquid's ability to enter separator begins to diminish; separator becomes starved of liquid; pump fillage becomes inconsistent and erratic | Saponja et al. 2021 SWPSC, p.4; Figure 3, Figure 9 |
| Full liquid starvation | 10 ft/s (3.0 m/s) superficial gas phase velocity | Separator becomes fully starved of liquid; pump fillage collapses | Saponja et al. 2021 SWPSC, p.4 |
| Casing gas rate trigger (~5.5" casing) | ~140 Mscf/day (4 × 10³ m³/day) | At this gas rate in 5.5" 20# casing, annular velocities can exceed 6 ft/s limit | Saponja et al. 2021 SWPSC, p.9; Figure 9 |

**Why it matters:** The 6 ft/s limit is only approximately **half** of the critical liquid lifting gas velocity. This means side-intake separators become limited at flow rates far below those where gas would actually lift all liquid out of the wellbore — an enormous lost opportunity in separation capacity. (Saponja et al. 2021 SWPSC, Figure 3 caption)

**Physics:** At high annular gas velocities, liquid's momentum travelling axially and vertically along the separator body cannot effectively turn sideways 90° into the separator's intake. The higher the velocity, the less liquid can enter through side intake slots/ports. (Saponja et al. 2021 SWPSC, p.4)

---

### 3B. Critical Liquid Lifting Gas Velocity — By Conduit Shape

This is the gas velocity at which all liquid is lifted upward and liquid fallback ceases. Below this velocity, liquid fallback can occur and be captured by an upward-facing collector.

**Parameters for example calculation:** 250 psi pump intake pressure, 200°F, 0.8 gas gravity, 65% water cut, 1.07 water SG, 35° API oil (Nagoo MAPe model) (Saponja et al. 2021 SWPSC, p.8)

| Conduit Configuration | Critical Liquid Lifting Gas Velocity | Notes |
|---|---|---|
| 5.5" casing (round tube) | **43 ft/s (13 m/s)** | High — liquid falls back easily |
| 5.5" × 2-7/8" tubing annulus | **12 ft/s (3.3 m/s)** | Much lower — annulus bridges liquid easily |
| WhaleShark Separation Region (5.5" casing) | **48 ft/s** | Requires extremely high gas velocity to prevent liquid fallback; sustains pump fillage through flumping (Saponja et al. 2021 SWPSC, p.10) |

**Key insight:** Liquid can fall back in a round tube (43 ft/s critical velocity) far more easily than in an annulus (12 ft/s). The WhaleShark's "no annulus" eccentric separation region exploits this — separation is governed by liquid fallback rate, not gas bubble rise. (Saponja et al. 2021 SWPSC, p.7–8)

---

### 3C. Gas Bubble Rise Velocity (Stokes' Law Relationship)

These are the velocities that govern conventional (poor-boy and packer-style) separator performance.

**Stokes' equation:**
$$v_{bubble} = \frac{2}{9} \frac{(\rho_{fluid} - \rho_{bubble})}{\mu_{fluid}} g \cdot R^2_{bubble}$$

| Bubble Diameter | Rise Velocity (in water) | Notes |
|---|---|---|
| 1/8" (3.2 mm) | ~1 inch/second (~2.5 cm/s) | Small bubbles from turbulence — very slow |
| 1/2" (12.7 mm) | ~6 inches/second (~15 cm/s) | "Commonly accepted" industry design value |

**Critical notes:**
- The commonly accepted 6 in/s design velocity is accurate only for 1/2" diameter bubbles in water — it can be misleading if turbulence is generating smaller bubbles (Saponja et al. 2021 SWPSC, p.5)
- Turbulence and fluid agitation generate smaller bubbles that rise much slower — a Packer-Style separator's turbulent flow path can significantly reduce actual bubble sizes below the design assumption
- Separation efficiency can be improved by 25% or more by minimizing turbulence and preserving larger bubble sizes (Saponja et al. 2021 SWPSC, p.5; Figure 4)

---

### 3D. Inclination Limits for Separation

| Separation Type | Maximum Inclination | Physics Basis | Citation |
|---|---|---|---|
| Gas separation (WhaleShark) | **80°** | WhaleShark designed to efficiently separate gas from liquid up to 80° inclination | Saponja et al. 2021 SWPSC, p.11 |
| Solids separation (WhaleShark) | **65°** | 65° = angle of repose — solids do not settle downward at higher inclinations; solids "stack out" and do not settle to higher inclinations | Saponja et al. 2021 SWPSC, p.11 |
| Optimal gas separation efficiency | **40°–45°** | At 40°–45°, liquid more easily collects at low side of casing; gas can escape more easily on high side; increases liquid fallback rate into collector by ~30% | Saponja et al. 2021 SWPSC, p.11 |

**Inclination physics note:** At 40°–45° inclination, there is no stratified flow in slug and churn regimes — this eliminates separator design constraints related to liquids falling to the low side. The large open mouth of the WhaleShark collector covers most of the casing internal diameter, so orientation of the separator at inclination does not matter for collection. (Saponja et al. 2021 SWPSC, p.11)

**Solids angle of repose:** At 65°, solids stack out and do not settle downward to higher inclinations. The design of the vertical spacing between the Velocity Acceleration Tube and the Pump Intake Tube maintains vertical distance when the separator is placed at 65°, so gravity separation of solids still occurs. It is not recommended to place the separator beyond 65° inclination for solids. (Saponja et al. 2021 SWPSC, p.11)

---

### 3E. Tubing Anchor Catcher (TAC) Velocity Risk

The TAC annular flow-by cross-sectional area is a critical system constraint that acts as a separate critical velocity choke point above the separator.

| Condition | Velocity | Effect |
|---|---|---|
| TAC annular flow-by velocity below critical | < 6 ft/s | Liquid can fall back past TAC; system functions normally |
| TAC annular flow-by velocity at/above critical | ~6 ft/s (1.8 m/s) superficial gas velocity | Liquid column builds above TAC; pump shows poor and erratic fillage; high annular fluid level with excessive pump gas interference |
| Full liquid lift at TAC | Gas velocity sufficient to lift all liquid past TAC | Separation of gas from liquid will not occur at pump level; undesirable cycle can repeat multiple times per day |

**Recommended practice:** Always use slimhole or slimline high annular flow-by TACs. Never use an annular restrictive packer as a TAC. Use a critical liquid lifting gas velocity/rate calculator to check TAC restriction risks. Calculate minimum required Tubing Hanger Tension considering: reservoir fluid temperature heating tubing, tapping pump, filling tubing after start, annular fluid level dropping, and thermal expansion coefficients. Results are commonly higher than the standard practice of 10,000 lbs tubing hanger tension. (Saponja et al. 2021 SWPSC, p.12; Figure 20, Figure 21)

---

## 4. WhaleShark Design — Detailed Specifications

### Physical Construction

| Parameter | Specification | Citation |
|---|---|---|
| Length | 18 feet | Saponja et al. 2021 SWPSC, p.9 |
| Tensile strength | Equivalent to 2-3/8" EUE tubing coupling | Saponja et al. 2021 SWPSC, p.9 |
| Structural elements | Two spiral half-gussets connecting rigid bar to oval pump intake tube | Saponja et al. 2021 SWPSC, p.9 |
| Collector intake | Large diameter, upward-facing, open | Saponja et al. 2021 SWPSC, p.9 |
| Pump intake tube shape | Oval — maximizes eccentricity from casing center line | Saponja et al. 2021 SWPSC, p.9 |
| Separation region | "No annulus" — eccentric open tube (A3) above collector; A3 > A2 > A1 | Saponja et al. 2021 SWPSC, p.9; Figure 11 |
| Solids system | Angled weir + gravity/momentum separation (not cyclonic); separates 0%–200% of flow rate | Saponja et al. 2021 SWPSC, p.10–11 |
| Mud joints | Standard tubing joints (retrievable, adjustable length) | Saponja et al. 2021 SWPSC, p.11 |
| Example field size (Case Study 6) | 35 series: 3.5" OD collector inside 5.5" (139.7mm) 23#/ft (34.2 kg/m) heavy wall casing, 4.7" (118.6mm) ID | Saponja et al. 2021 SWPSC, Case Study 6 |

---

## 5. Flow Loop Testing Results

Flow loop testing confirmed the WhaleShark concept with a physical near-scale prototype. (Saponja et al. 2021 SWPSC, p.10; Figures 15, 16)

**Key finding:** The collector remains full with little-to-no gas separation occurring inside the collector — visual proof that the separator is governed by how fast liquid can fall (not gas bubble rise velocity). This was described as "probably the most exciting moment in the design of the WhaleShark." (Saponja et al. 2021 SWPSC, p.10; Figure 16)

**Flow loop confirmed:**
1. **100% separation efficiency** achieved
2. Separation region above the collector effectively has "no annulus" — eccentric oval pump intake tube significantly improves separator performance
3. Taking advantage of multiphase flow reversals with upward-facing intake significantly enhances separation
4. More efficient and greater capacity than packer-style separators
5. Ability to handle sluggy and inconsistent flows

---

## 6. Case Studies

### Case Study 1 — Mississippian Lime, Oklahoma (Figure 22)

| Parameter | Result |
|---|---|
| Formation | Mississippian Lime horizontal wells, Oklahoma |
| Casing | 5.5" |
| Liquid rate | 500–600 bbl/day |
| Gas rate | 1.3–1.8 MMscf/day |
| GLR | High (2,000–3,600 scf/bbl implied) |
| Pump | Tubing pump |
| Result | Complete and consistent high pump fillage in 5.5" casing at high gas liquid ratios |

**Significance:** Demonstrated that full consistent pump fillage is achievable with a packerless separator not governed and limited by gas bubble rise velocity. (Saponja et al. 2021 SWPSC, p.12; Figure 22)

---

### Case Study 2 — DJ Basin Niobrara, Colorado (Figure 23)

| Parameter | Result |
|---|---|
| Formation | DJ Basin Niobrara |
| Fluid characteristics | Gassy light oil with high foaming tendency |
| Replaced | Poor-boy separator (showing very inconsistent pump fillage, ~85% average) |
| WhaleShark result | Stable and consistent high pump fillage, averaging over 95% |

**Significance:** Replaced a poorly performing poor-boy separator with "fairly decent average pump fillage (around 85%)" and achieved >95% consistent fillage in a high-foaming-tendency environment. (Saponja et al. 2021 SWPSC, p.12; Figure 23)

---

### Case Study 3 — Texas Permian Basin (Figure 24)

| Parameter | WhaleShark Well | Poor-Boy Well |
|---|---|---|
| Formation | Permian (foamy tendency) | Same formation |
| GLR | ~2,000 scf/bbl (same for both) | ~2,000 scf/bbl |
| Days from initial rod up | Same | Same |
| Fluid rate | ~450 bbl/day | <225 bbl/day (less than half) |
| Pump fillage | 75%+ smooth consistent | 40%–80% erratic, "rough" |
| Pump load (hydrostatic) | ~10,000 lbs | ~5,000 lbs |
| Pump card appearance | Smooth — minimal free gas entering pump | Rough — free gas entering pump/tubing |
| Pump card zero crossing | Card reaches zero line (adequate fluid) | Card does not reach zero line (excessive gas in pump) |

**Significance:** WhaleShark well removing majority of free gas from liquid; consistent 75% fillage = compression of entrained gas only. Poor-boy not separating free gas → free gas entering tubing → rough cards, excessive rod friction, high pressure loss. (Saponja et al. 2021 SWPSC, p.13; Figure 24)

---

### Case Study 4 — Charlie Lake, BC — 60° Inclination Test (Figure 25)

| Parameter | Result |
|---|---|
| Formation | Canadian Charlie Lake |
| Inclination | 60° (high inclination) |
| Fluid | Gassy/foamy water and oil |
| Replaced | Weighted intake poor-boy separator |
| Result | Improved separation, reduced gas slugging, increased production at same pump strokes per minute |

**Significance:** Validated WhaleShark performance at 60° well inclination — a high-inclination deployment scenario. (Saponja et al. 2021 SWPSC, p.13; Figure 25)

---

### Case Study 5 — Montney, BC — Foamy Oil/Water (Figure 26)

| Parameter | Result |
|---|---|
| Formation | Canadian Montney play horizontal well |
| Fluid | Gassy foamy oil/water production |
| Previous separator | Low reliability poor-boy |
| Issue before WhaleShark | Rod failures occurring every couple months |
| WhaleShark result | Improved production and rod lifting reliability since early April 2021 install; well still operating |
| Operator decision | Chose to rod lift the NEXT well instead of gas lift — directly attributable to WhaleShark result |

**Significance:** Demonstrates reliability improvement in a challenging gassy foamy fluid environment, and influenced operator's artificial lift selection for next well. (Saponja et al. 2021 SWPSC, p.13; Figure 26)

---

### Case Study 6 — Charlie Lake, BC — 35 Series WhaleShark, Record Performance (Figure 27)

| Parameter | Specification |
|---|---|
| Formation | Canadian Charlie Lake |
| Separator | 35 series WhaleShark (3.5" OD collector intake) |
| Casing | 5.5" (139.7mm) heavy wall 23 #/ft (34.2 kg/m), ID 4.7" (118.6mm) |
| Gas handled | 2.7 MMscf/day (75 E³m³/day) |
| Liquid handled | 2,000 bbl/day (320 m³/day) |
| Result | Successfully handling both rates simultaneously; demonstrated flumping out the annulus while sustaining nearly full and consistent pump cards |

**Significance:** Likely a downhole separation record for inside 5.5" casing. Demonstrated full flumping condition management while sustaining high pump fillage. (Saponja et al. 2021 SWPSC, p.13; Figure 27)

---

### Case Study 7 — North Dakota Bakken (Figure 28)

| Parameter | Result |
|---|---|
| Formation | North Dakota Bakken play |
| Replaced | Packer-style and poor-boy separators |
| Timing | Pro-active pulls (not wait-for-failure) |
| Result | Significant improvements in pump fillage consistency and average pump fillage |

**Significance:** Pro-active replacement program improving production performance across both packer-style and poor-boy wells. (Saponja et al. 2021 SWPSC, p.13; Figure 28)

---

## 7. Industry Context and Problem Framing

### Why Downhole Separation Matters

Sucker rod pumping is industry-proven as the most cost-effective artificial lift for achieving maximum production drawdown and low bottomhole producing pressure per unit cost. A consistent gas-free and solids-free liquid supply to the pump (full pump fillage) is critical for long-term reliability and high production rate. (Saponja et al. 2021 SWPSC, p.1)

### Technical Limitations That Drove WhaleShark Development

| Limitation | Physics Constraint |
|---|---|
| Casing size cross-sectional area | 5.5" × 20# casing physically limits maximum separator cross-section |
| Horizontal wellbore slug/churn flow | Flow is not steady-state — highly transient and sluggy |
| Fluid gas entrainment and foaming | Entrained gas passes through pump; foam suspends solids and slows bubble rise |
| High gas velocities entraining solids | Gas phase carries solids, causing erosion; cyclonic separation too narrow operating range for 0%–200% pump rate |
| Cyclonic separation narrow envelope | Rod pumping varies 0%–200% each pump stroke; turbulence suspends solids; foamy fluids suspend solids |

(Saponja et al. 2021 SWPSC, p.3–4)

### Operator Improvement Wish List

The artificial lift community identified these requirements for improved separators:
1. Lower operational risk — avoid packers/cup seals; avoid scaling-in-hole risks; want packerless
2. Higher average pump fillage — for production maximization
3. More consistent pump fillage — for pump and rod protection and reliability
4. Broader operating window — minimize pump/separator reconfiguration over well life
5. More solids separation capacity — handle broad flow rate conditions, broad solids concentrations, low-risk sump retention and retrievability (mud joints at base of separator)

(Saponja et al. 2021 SWPSC, p.3)

---

*Knowledge base compiled from: Saponja et al. 2021 SWPSC Paper 2021031, 20 pages, all figures. Draft A1 — 2026-04-14.*

---

# Downhole Gas Separation — Knowledge Base (Draft A2)

**Sources:**
- McCoy, J.N. & Podio, A.L. (Echometer Company / University of Texas at Austin). "Improved Downhole Gas Separators." Presented at the Southwestern Petroleum Short Course, April 7–8, 1998, Texas Tech University, Lubbock, TX. [Cited as: McCoy & Podio 1998]
- Yang, Y. et al. "Feasibility Study on Downhole Gas–Liquid Separator Design and Experiment Based on the Phase Isolation Method." *Applied Sciences*, 2021, 11, 10496. https://doi.org/10.3390/app11210496. [Cited as: MDPI 2021]

---

## 4. Separator Sizing Methodology

### 4.1 Fundamental Sizing Principle

The governing constraint in all downhole gas separator sizing is the **liquid capacity of the annular chamber** — specifically the cross-sectional area available between the dip tube (or outer barrel) and the casing ID. Gas bubbles rise through produced liquid in most wells at approximately **6 inches (15 cm) per second** in low-viscosity fluids (<10 cp), so each square inch of annular cross-sectional area allows approximately **50 barrels per day (BPD) of liquid** to fall free-fall downward to the pump inlet without entraining gas (McCoy & Podio 1998, p.2).

> **Core sizing rule:** Liquid capacity (BPD) ≈ Annular area (sq in) × 50

This factor derives directly from the gas bubble rise velocity and represents the downward liquid velocity at which gas can still escape upward. If the downward liquid velocity exceeds the gas rise velocity, free gas will be drawn into the pump.

### 4.2 Gas Separator Placement: Below vs. Above Fluid Entry Zone

McCoy & Podio describe two fundamentally different separator architectures depending on pump depth relative to the perforations:

| Placement | Separator Type | Outer Barrel | Mechanism |
|---|---|---|---|
| Pump **below** fluid entry zone (preferred) | Single dip tube / perforated sub | Casing itself acts as outer barrel | Natural gravity separation in open casing annulus |
| Pump **at or above** fluid entry zone | Outer-barrel assembly (gas anchor/mud anchor) | Separate outer barrel with ports | Forced separation in enclosed chamber |

**Rule 1 — Always prefer below-formation placement.** Setting the pump at least 5 feet below the perforations allows the casing to act as the outer barrel. This produces the highest liquid capacity and the most efficient separation because the downward liquid velocity will be lower in the full casing cross-section than in any enclosed separator (McCoy & Podio 1998, p.1).

**Rule 2 — Dip tube must extend at least 5 feet below the fluid entry zone.** When the pump is below formation, the dip tube should extend at least 5 feet below the perforations. This ensures that gas bubbles entering with the produced liquid have adequate distance to migrate upward and escape into the casing annulus before reaching the pump inlet (McCoy & Podio 1998, p.2).

**Rule 3 — Do not run a dip tube below the pump.** Running a dip tube below the pump on the inside of a perforated sub increases friction losses and results in less efficient operation. Additional friction losses reduce liquid inflow to the pump (McCoy & Podio 1998, p.2).

### 4.3 Dip Tube Friction Loss Criteria

The pressure drop across the dip tube is a critical sizing constraint. McCoy & Podio state that friction loss in the dip tube should be kept to a **minimum — preferably less than 0.5 PSI** and the design target is **less than 1/2 PSI** across the dip tube (McCoy & Podio 1998, p.3, Table 3 footnote; p.4).

Thin-wall dip tubes are specifically recommended to achieve this:

- **Recommended material:** Smooth, thin-wall, 316 stainless steel, Schedule 10, seamless tubing (McCoy & Podio 1998, p.4).
- The differential pressure across the dip tube being less than 1 PSI enables the dip tube to add liquid capacity compared to standard-wall tubing.
- The dip tube liquid capacity table (Table 3) shows that a **0.5 PSI pressure drop** limit governs the capacities for thin-wall dip tubes or 7 feet of thin-wall pipe. See table below.

**Table 4-A: Dip Tube Liquid Capacity (below formation, pump below fluid entry zone)**
*(Reproduced from McCoy & Podio 1998, Table 3 — capacities based on 0.5 PSI friction drop in 7 ft of Schedule 10 thin-wall or standard line pipe)*

| Dip Tube Size (in) | Description | Liquid Capacity (BPD) |
|---|---|---|
| 3/4 × 0.824 SCH 40 | Standard | 315 |
| 1 × 1.050 SCH 40 | Standard | 630 |
| 1-1/4 × 1.315 SCH 40 | Standard | 740 |
| 1 × 1.315 SCH 316 SS | Thin-wall | 1,350 |
| 1-1/4 × 1.380 SCH 316 SS | Thin-wall | 1,570 |
| 1-1/4 × 1.440 SCH 316 SS | Thin-wall | 1,930 |
| 1-1/2 × 1.610 SCH 40 | Standard | — |
| 2 × 2.067 SCH 40 | Standard | 3,700 |

*(McCoy & Podio 1998, Table 3)*

### 4.4 Natural Gas Separator Sizing: Below-Formation Configuration (Table 1)

When the pump is set below the fluid entry zone, the casing itself is the outer barrel and the entire casing-dip tube annular area is available for gas-liquid separation. McCoy & Podio provide capacity data for common casing/tubing combinations:

**Table 4-B: Natural Gas Separator Capacity — Pump Below Fluid Entry Zone**

| Casing Size (in) | Dip Tube Size (in) | Description | Annulus Area (sq in) | Liquid Capacity (BPD) |
|---|---|---|---|---|
| 7 | 3-1/2 | Perforated tubing sub | 23.1 | 1,150 |
| 7 | 2-7/8 | Perforated tubing sub | 26.7 | 1,335 |
| 7 | 2-3/8 | Perforated tubing sub | 28.8 | 1,440 |
| 5-1/2 | 2-7/8 | Perforated tubing sub | 12.7 | 635 |
| 5-1/2 | 2-3/8 | Perforated tubing sub | 14.8 | 740 |
| 4-1/2 | 2-7/8 | Perforated tubing sub | 6.1 | 305 |
| 4-1/2 | 2-3/8 | Perforated tubing sub | 8.2 | 410 |
| **Higher capacity options** | | | | |
| 5-1/2 | 1-1/2 | Perforated line pipe | 16.4 | 820 |
| 4-1/2 | 1-1/4 | Perforated line pipe | 10.4 | 520 |

*(McCoy & Podio 1998, Table 1)*

Key note: A 2-3/8" perforated tubing sub below the formation inside 4-1/2" casing has a capacity of **410 BPD**. A 1-1/4" dip tube below the seating nipple increases the capacity to **520 BPD** (McCoy & Podio 1998, p.2).

### 4.5 Conventional Gas Separator Sizing: Above-Formation Configuration (Table 2)

When the pump must be set above or at the fluid entry zone, a separate outer barrel is required. McCoy & Podio document the significant capacity penalty imposed by conventional perforated-sub outer barrels:

**Table 4-C: Gas Separator Capacity — Separator Above Fluid Entry Zone**

| Outer Barrel Description | Dip Tube Size (in) | Annulus Area* (sq in) | Liquid Capacity (BPD) |
|---|---|---|---|
| 3-1/2 perforated tubing sub | 1-1/4 | 4.9 | 240 |
| 2-7/8 perforated tubing sub | 1-1/4 | 2.7 | 135 |
| 2-3/8 perforated tubing sub | 1-1/4 | 3.9 | 195 |
| 2-7/8 perforated tubing sub | 1 | 1.0 | 50 |
| 2-3/8 perforated tubing sub | 1 | 2.1 | 105 |
| 2-7/8 perforated tubing sub | 3/4 | 2.3 | 115 |
| **Higher capacity (collar-size)** | | | |
| 3-1/2 collar-size gas separator | 1-1/4 | 12.0 | 600 |
| 2-7/8 collar-size gas separator | 1-1/4 | 8.3 | 415 |
| 2-3/8 collar-size gas separator | 1 | 4.6 | 230 |

*Annulus area between gas separator outer barrel and dip tube (McCoy & Podio 1998, Table 2)*

**Critical finding:** Conventional 2-3/8" perforated-sub separators above the formation have a liquid capacity of only **50 BPD** with a 1" dip tube — compared to 410 BPD for the same tubing below formation. The conventional "Poor-Boy" separator loses ~87% of available capacity by using a sub smaller than the collar diameter (McCoy & Podio 1998, p.3).

**Why conventional separators above the formation fail:**
1. Thick-wall tubing/perforated sub OD is smaller than the collar diameter — reduces annular area by approximately **50 BPD** vs. collar-size design (McCoy & Podio 1998, p.3).
2. Most use small 1/4" or 3/8" holes for fluid entry — liquid can only enter on the upstroke when pump creates a differential pressure. On the downstroke, very little liquid and significant gas flows inward. Conventional perforated sub separators "operate at low efficiency — this fact has been verified by hundreds of tests" (McCoy & Podio 1998, p.3).
3. Liquid entry area of the conventional dip tube is only **50 BPD** (McCoy & Podio 1998, p.3).

### 4.6 Collar-Size Gas Separator Design

The collar-size separator addresses all three conventional separator deficiencies. Its key design features:

**Outer barrel diameter:** Equal to the tubing collar OD. This maximizes the annular area between the outer barrel and the casing, providing liquid capacity equivalent to or greater than the pump capacity (McCoy & Podio 1998, p.3–4).

**Large ports:** Four ports, each 4" high, with total port area approximately equal to four times the area between the outer barrel and dip tube. Two upper ports are immediately below the collar; two lower ports at right angles, 2" below the upper ports. This allows liquid to enter 100% of the time on both upstroke and downstroke — gravity driven from the casing annulus (McCoy & Podio 1998, p.4).

**Collar-size gas separator selection rules:**
- Select a separator the same size as the tubing unless pump capacity exceeds separator capacity
- If pump capacity exceeds 415 BPD in 5-1/2" casing, use a collar-size separator with capacity ≥ pump capacity
- A 2-7/8" collar-size separator should not be used on the inside of 5-1/2" casing if maximum casing annulus gas flow rate exceeds **51 MCF/d at 1 ATM** (McCoy & Podio 1998, p.6)

**Table 4-D: Collar-Size Gas Separator — Liquid and Gas Capacity**

| Collar Size (in OD) | Liquid Capacity, 4-1/2" Casing (BPD) | Liquid Capacity, 5-1/2" Casing (BPD) | Gas Capacity, 4-1/2" Casing (MCF/D) | Gas Capacity, 5-1/2" Casing (MCF/D) | Gas Capacity, 7" Casing (MCF/D) |
|---|---|---|---|---|---|
| 2-3/8 (3.0" OD) | 230 | — | 27 | — | — |
| 2-7/8 (3.75" OD) | 415 | — | 9 | 51 | 127 |
| 3-1/2 (4.5" OD) | 600 | — | — | 5 | 98 |

*Gas capacity at 1 ATM. Multiply by casing pressure in atmospheres for actual capacity (McCoy & Podio 1998, Table 5)*

**Gas capacity scaling with casing pressure:** The gas capacities in Table 5 assume liquid exists above the pump (well produced with casing valves open). Most wells produce with casing pressures of 30–125 PSI, giving a multiplier of **3× (at 30 PSI)** to **10× (at 125 PSI)** on the 1 ATM gas capacities (McCoy & Podio 1998, p.6).

### 4.7 Gas Separator Length and Dip Tube Depth

**Dip tube minimum extension below ports:**
The rate at which gas bubbles migrate upward in the liquid column is the controlling factor for dip tube length, not pump volume. Gas bubbles rise at approximately 6 inches/second in the liquid (McCoy & Podio 1998, p.5):

- At 10 strokes/min: pumping cycle = 6 seconds (3 sec upstroke, 3 sec downstroke)
- On the downstroke, gas bubbles drawn into the annulus will migrate upward at 6 in/sec × 3 sec = **18 inches**
- Therefore, the dip tube should extend at least **18 inches below the gas separator inlet perforations** for a well pumping 10 strokes/min (McCoy & Podio 1998, p.5)
- Longer distance increases friction losses and causes free gas release from oil flowing up the dip tube

**Specific examples:**
- Rotoflex unit at 4 strokes/min → pumping cycle = 7-1/2 sec → dip tube length should be **45 inches** (McCoy & Podio 1998, p.5)
- The collar-size gas separator dip tube extends approximately **70 inches below the bottom of the outer barrel ports** (McCoy & Podio 1998, p.5)

### 4.8 Separator Type Selection Matrix

| Condition | Recommended Separator | Rationale |
|---|---|---|
| Pump can be set ≥5 ft below perforations | Single dip tube / perforated sub (natural separator) | Casing = outer barrel; maximum capacity |
| Pump must be set above formation; production >100 BPD with free gas | Collar-size gas separator | Liquid capacity ≥ pump capacity; 100% liquid entry on both strokes |
| Pump above formation; production <100 BPD | Collar-size (preferred) or top-holddown with joint of tubing | Poor-Boy inadequate; top-holddown pump has <50 BPD capacity |
| Well produces sand into separator | Add collection chamber below collar-size separator | Remove bull plug, install nipple + debris chamber (McCoy & Podio 1998, p.5) |
| Larger capacity needed than casing size allows | Upsize outer barrel with 2-7/8" separator on 2-3/8" seating nipple via swedge | Increases annular area within the casing constraint (McCoy & Podio 1998, p.5) |
| Gas separator ports laid against casing wall due to tubing anchor | Run ≥2 joints of tubing between TAC and separator | Liquid concentrates where tubing contacts casing wall; ports must be away from that zone (McCoy & Podio 1998, p.4) |

---

## 5. Phase Isolation Separator Concept

### 5.1 Design Motivation and Differentiation from Conventional Separators

The Downhole Gas–Liquid Separator (DGLS) described in Yang et al. (MDPI 2021) is designed for a fundamentally different application than the pump-protection separators of McCoy & Podio: **production profile logging accuracy**, specifically eliminating gas-phase interference with electromagnetic flowmeters (spinners/turbines) used in production logging tools.

During the high water-cut development stage of oilfields, formation pressure drops and crude oil degasses, creating oil–gas–water three-phase flow in the wellbore. This gas phase causes significant errors in oil–water two-phase flowmeter measurements because:
- Electromagnetic flowmeters (conductance sensors) treat the water phase as conductive and the oil phase as non-conductive — the gas phase also behaves as non-conductive, inflating the apparent oil volume holdup (MDPI 2021, p.1–2)
- The gas phase changes the flowmeter's response characteristics

The DGLS **places the oil–water flowmeter inside a liquid channel** from which gas has been actively excluded, allowing accurate two-phase measurement in the presence of free gas. This is the "phase isolation method" — physically separating gas from the liquid before it reaches the measurement instrument, rather than correcting the measurement post-hoc (MDPI 2021, p.2–3).

### 5.2 DGLS Architecture and Operating Principle

The DGLS consists of three main components:
1. **Collection umbrella** — an inverted conical deflector deployed in the wellbore annulus that directs upward-flowing multiphase fluid toward the instrument
2. **Gas–liquid separating valve** — a float-actuated valve that routes gas to an exhaust channel and liquid to the central pipe
3. **Central pipe with oil–water flowmeter** — the measurement zone fed only with gas-free liquid

**Operating sequence (MDPI 2021, p.3):**
1. Logging tool is lowered and collection umbrella is opened to fix the tool in the wellbore
2. Upward-flowing multiphase fluid (oil + gas + water) enters from below the umbrella
3. The umbrella increases local flow velocity (orifice effect — flow area reduction multiplies velocity)
4. Inside the DGLS, density stratification separates phases: low-density gas rises to the top of the umbrella, forming a gas cap; oil accumulates under the gas cap; water accumulates below
5. When gas accumulates sufficiently, the float valve opens the gas inlet (3 mm diameter), venting gas into the exhaust channel along the outer wall
6. When oil/water reaches the top of the umbrella, the float valve closes the gas inlet and opens the liquid inlet (21 mm diameter) to the central pipe
7. Liquid enters the central pipe where the oil–water flowmeter makes an accurate measurement

**Key structural parameters of the gas-liquid separating valve (MDPI 2021, Fig. 3):**
- Casing (experimental): 20 mm
- Gas inlet port diameter: 3 mm
- Liquid inlet diameter: 21 mm
- Central pipe (flow measurement zone): 10 mm inner diameter
- Float: stainless steel, spring-actuated (one spring above floater, one below)
- Outer diameter of instrument prototype: 28 mm (MDPI 2021, p.14)

### 5.3 Mathematical Model of Separation Efficiency

The DGLS separation efficiency is calculated using the volume-fraction method (MDPI 2021, p.6):

**Gas separation efficiency:**
$$\eta_g = \left(1 - \frac{(1 - Y_w) \cdot M_a}{Y_{sg}}\right) \times 100\%$$

where $\eta_g$ is the gas collection rate, $Y_w$ is the central pipe water holdup, $M_a$ is the central pipe total flow fraction, and $Y_{sg}$ is the wellbore total gas flow fraction.

**Oil separation (collection) efficiency:**
$$\eta_{oil} = \frac{(1 - Y_w)M_a}{Y_{so}} \times 100\%$$

where $Y_{so}$ is the wellbore total oil fraction.

**Engineering acceptance criterion:** Both $\eta_g \geq 90\%$ and $\eta_{oil} \geq 90\%$ must be satisfied (MDPI 2021, p.6).

The bubble rise velocity (Wallis model) in two-phase gas–water flow:
$$v_t = 1.53\left[\frac{\delta_{gw}(\rho_w - \rho_g)g}{\rho_w^2}\right]^{0.25}$$

where $\delta_{gw}$ is the gas–water interfacial tension, $\rho_w$ and $\rho_g$ are water and gas densities, and $g$ is gravitational acceleration (MDPI 2021, Eq. 4).

**Gas superficial velocity:**
$$v_{sg} = v_m - v_{sw}$$

where $v_m$ is the gas–water mixture average velocity and $v_{sw}$ is the water boundary velocity (MDPI 2021, Eq. 2).

### 5.4 Numerical Simulation Results: Gas–Water Two-Phase Flow

Simulations were run in ANSYS Fluent 16.0 using the VOF (Volume of Fluid) model for stratified/free-surface flow. Flow conditions: gas holdup 5% or 10%; total flow rates 20–60 m³/d; temperature 20°C; inlet pressure at standard atmospheric pressure (MDPI 2021, p.8).

**Table 5-A: Gas–Water Separation Efficiency at 5% Gas Holdup**
*(MDPI 2021, Table 2)*

| Total Flow (m³/d) | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|
| $\eta_g$ (%) | 90.5 | 84.4 | 79.5 | 75.1 | 66.1 |

**Table 5-B: Gas–Water Separation Efficiency at 10% Gas Holdup**
*(MDPI 2021, Table 3)*

| Total Flow (m³/d) | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|
| $\eta_g$ (%) | 91.2 | 80.9 | 75.2 | 69.1 | 51.5 |

**Key finding:** The DGLS meets the $\eta_g \geq 90\%$ criterion **only at total flow rates ≤ 20 m³/d** in gas–water two-phase flow, regardless of whether gas holdup is 5% or 10% (MDPI 2021, p.9–10). The applicable operating range for gas–water two-phase flow is **0–20 m³/d total** (MDPI 2021, p.10).

Flow regime transitions observed in simulation (MDPI 2021, p.9):
- 20 m³/d: Dispersed gas in water bubble flow (D G/W) + VFD G/W bubble flow
- 30–40 m³/d: D G/W supplemented by VFD G/W bubble flow
- 50–60 m³/d: Dominated by D G/W bubble flow (more complex mixing)

### 5.5 Numerical Simulation Results: Oil–Gas–Water Multiphase Flow

Simulation conditions: gas holdup 5%, oil holdup 10%, water holdup 85%; total flow 20–60 m³/d (MDPI 2021, Table 4, p.11). The oil phase has higher viscosity than water and gas, acting as a seal around the gas exhaust hole — this improves gas–liquid separation compared to two-phase flow.

**Table 5-C: Gas–Liquid Separation Efficiency at Oil–Gas–Water Multiphase Flow**
*(MDPI 2021, Table 5)*

| Total Flow (m³/d) | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|
| $\eta_g$ (%) | 92.4 | 90.9 | 90.5 | 90.4 | 86.5 |
| $\eta_{oil}$ (%) | 91.9 | 95.3 | 93.2 | 99.3 | 99.1 |

**Key finding:** In oil–gas–water three-phase flow, both gas and oil collection efficiencies exceed 90% at total flows of **20–50 m³/d** (MDPI 2021, Table 5). The applicable range extends to **20–50 m³/d** for multiphase flow — significantly wider than for two-phase flow. The oil phase's higher viscosity acts as a barrier around the gas exhaust port, reducing gas leakage into the liquid channel (MDPI 2021, p.12).

The oil–gas–water simulation results should not be replaced by gas–water two-phase simulation when total flow exceeds 30 m³/d, because oil's viscosity and slippage effects change separation behavior substantially at higher flows (MDPI 2021, p.14).

### 5.6 Dynamic Experimental Validation

Experiments were conducted at the Daqing Oilfield multiphase flow experimental device — a closed-loop system with a simulated wellbore, pressure stabilizer, turbine transmitter, and separate oil/gas/water feed controls (MDPI 2021, p.14, Fig. 12).

**Experimental prototype specifications (MDPI 2021, p.14):**
- Outer diameter: 28 mm
- Inner diameter of central flow channel: 10 mm
- Central pipe material: plexiglass (non-conductive, compatible with impedance sensors)

**Experimental conditions tested (MDPI 2021, p.16):**
- Gas mass flow: 0–15 m³/d (in three steps: 5, 10, 15 m³/d)
- Liquid flow range: 1–60 m³/d
- Water holdup range: 50%–100%

**Results summary (MDPI 2021, p.16–20):**

| Gas Flow (m³/d) | Turbine Response | Separation Performance |
|---|---|---|
| 5 m³/d | Linear, independent of water holdup 60–100%; closely tracks pure water curve | Good isolation — gas effectively excluded from central pipe |
| 10 m³/d | Still approximately linear; small offset from pure water curve at different holdups | Acceptable — some gas enters central pipe but within ±10% error tolerance |
| 15 m³/d | Nonlinear at liquid flow < 10 m³/d; large deviation from pure water curve | DGLS separation insufficient — gas enters central pipe and accelerates turbine |

**Verified operating envelope (MDPI 2021, p.20):**
- Gas mass flow: **0–15 m³/d** (upper limit for adequate separation)
- Liquid flow: **1–60 m³/d**
- Water holdup: **50%–100%**

The experimental research demonstrated that when gas flow is below 15 m³/d, the turbine response increases linearly with liquid flow and the DGLS can effectively isolate the gas and liquid phases. When gas flow reaches 15 m³/d, the DGLS gas–liquid separation effect becomes minimal (MDPI 2021, p.18–19, Fig. 16).

---

## 6. Separator-Pump Integration

### 6.1 What the Pump Requires

Both papers converge on the same fundamental requirement: **the pump must receive gas-free (or nearly gas-free) liquid at the inlet** to operate efficiently and reliably.

**From McCoy & Podio (sucker rod pump context):**
- Pumps operating with incomplete liquid fillage are identified by dynagraph analysis showing gas-pound signatures
- Acoustic liquid level tests showing a high gaseous liquid column above the pump indicate incomplete pump fillage
- Operating the pump at excessive speed, rimming the pump (tapping bottom), or increasing tubing/casing pressure are *not* valid corrective actions for gas interference — they mask the symptom without addressing the root cause (McCoy & Podio 1998, p.1)
- The correct diagnostic sequence: (1) acoustic liquid level test, (2) dynamometer measurement, (3) separator evaluation

**From MDPI 2021 (production logging context):**
- Gas-phase interference reduces measurement accuracy of oil–water electromagnetic flowmeters (MDPI 2021, p.1)
- Engineering acceptance criterion: $\eta_g \geq 90\%$ and $\eta_{oil} \geq 90\%$ (MDPI 2021, p.6)
- Both criteria must be met simultaneously for the instrument measurement to be valid

### 6.2 Progressive Cavity Pump (PCP) Specific Considerations

McCoy & Podio devote a dedicated section to PCP requirements, which are more stringent than rod pump requirements:

**Temperature risk of gas compression in PCPs (McCoy & Podio 1998, p.6, Table 4):**

| Pump Inlet Pressure (PSI) | Inlet Temp (°F) | Outlet Temp at 3,000 ft depth — Adiabatic Compression (°F) |
|---|---|---|
| | | 2,000 ft | 3,000 ft | 4,000 ft | 5,000 ft |
| 15 | 100 | 600 | 650 | 700 | 750 |
| 50 | 100 | 440 | 490 | 530 | 570 |
| 100 | 100 | 360 | 420 | 475 | 530 |
| 500 | 100 | 190 | 235 | 280 | 310 |
| 1,000 | 100 | 100 | 150 | 190 | 225 |

*(McCoy & Podio 1998, Table 4 — pump outlet pressure assumed at one-half of well depth in feet)*

**Critical implication:** At a pump inlet pressure of 15 PSI (near-zero back-pressure) and a well depth of 3,000 ft, outlet temperature rises to **650°F** from adiabatic gas compression. Most PCP elastomers (nitrile, hydrogenated nitrile) fail above approximately 300°F sustained temperature. Exposure to gas without liquid cooling causes rapid polymer destruction (McCoy & Podio 1998, p.6).

"Separation of free gas from the liquid entering the PC pumps will greatly increase the efficiency and prolong the life of progressive cavity pumps... the collar-size gas separator improves the separation of gas from liquid and results in additional production and longer life than when a progressive cavity pump is used above the formation without an efficient gas separator" (McCoy & Podio 1998, p.6).

**PCP placement rule:** Preferably, the progressive cavity pump inlet should be run **below the formation** (McCoy & Podio 1998, p.6).

### 6.3 Separator-to-Pump Distance and Placement Rules

**TAC (Tubing Anchor Catcher) considerations (McCoy & Podio 1998, p.4):**
- Liquid concentrates on the side of the casing where the tubing contacts the wall
- Studies at the University of Texas clear casing/tubing facilities and downhole video camera studies confirm that gas concentrates on the high side of the casing annulus (McCoy & Podio 1998, p.4, refs 12, 15)
- The collar-size separator always lays against the **low side of the casing** (by gravity), which is the side of higher liquid concentration — this is an advantage over decentralized gas separators that may be held against the high side by a spring (McCoy & Podio 1998, p.4)
- **Rule:** The collar-size gas separator should **not be run immediately below a tubing anchor** — the tubing anchor causes liquid to concentrate against the casing wall where the tubing rests, creating a zone of gas concentration at the separator inlet
- **Minimum spacing:** At least **two joints of tubing** (approximately 40–50 ft) should be run between the tubing anchor and the collar-size gas separator. This spacing allows the tubing to lay against the casing wall by gravity, reducing gas concentration at the separator ports (McCoy & Podio 1998, p.4)

**Top-holddown pump limitations (McCoy & Podio 1998, p.5):**
- Top-holddown pumps used above the formation with conventional perforated sub gas separators are inefficient
- The area between the inside of the perforated sub and the OD of the pump is less than **one square inch**
- Liquid capacity with a top-holddown pump is less than **50 BPD** — far below most production rates
- Solution: Use a joint of tubing slightly longer than the top-holddown pump, with the seating nipple and collar-size gas separator attached to the joint bottom. This converts the pump body into the dip tube (McCoy & Podio 1998, p.5)

### 6.4 Summary: Separator Performance vs. Pump Reliability

| Separator Condition | Pump Impact | Corrective Action |
|---|---|---|
| Separator liquid capacity < pump rate | Gas drawn into pump; gas pound, incomplete fillage, low efficiency | Upsize separator or set pump below formation |
| Dip tube friction > 0.5 PSI | Reduced inflow; pump starved | Use thin-wall Schedule 10 dip tube |
| Separator set within 1–2 joints of TAC | Gas concentration at separator ports; reduced liquid inflow | Run ≥2 joints between TAC and separator |
| Gas entering PCP without liquid cooling | Adiabatic compression → elastomer destruction | Run PCP below formation; use collar-size separator |
| Conventional "Poor-Boy" above formation | 50–195 BPD liquid cap; most production exceeds this | Replace with collar-size separator |
| DGLS gas flow > 15 m³/d (logging context) | Turbine flowmeter over-reads; oil–water split inaccurate | Reduce total flow or accept reduced measurement accuracy (MDPI 2021, p.18) |
| DGLS total flow > 20 m³/d (two-phase) | Gas separation efficiency drops below 90% | Switch to multiphase flow regime analysis or accept degraded accuracy (MDPI 2021, p.9–10) |

### 6.5 Diagnostic Indicators of Separator Failure

**McCoy & Podio indicators (McCoy & Podio 1998, p.1):**
- Acoustic liquid level test: high gaseous liquid column above pump → indicates incomplete pump fillage → separator may be inefficient or inadequate
- Dynamometer (dynagraph): gas-pound signature on the downstroke card → free gas is entering the pump
- Field check: view the gas separator above-ground — whether the pump is above or below the formation should be determinable by visual inspection; separators should be built differently for each case

**MDPI 2021 indicators (flowmeter context):**
- Turbine flowmeter output frequency diverges from linear relationship with total liquid flow at different water holdups → gas entering central pipe
- Turbine response at low liquid flow (<10 m³/d) becomes nonlinear when gas flow ≥15 m³/d → DGLS separation failing (MDPI 2021, p.18, Fig. 16)
- Output frequency at a given liquid flow rate higher than pure-water baseline → gas contamination in measurement zone


---

## 7. Heavy Oil Corrections — Why Standard Separator Design Fails at 80,000 cP

> This section synthesizes findings from SPE-136665, Clift/Grace/Weber, Gokcal SPE-102727, and the WhaleShark paper to explain why conventional separator sizing is fundamentally wrong for Bluesky heavy oil.

### 7.1 The Bubble Rise Problem

McCoy's 50 BPD/sq-in sizing rule (Section 4.1) assumes gas bubbles rise at 6 in/s (15 cm/s) in low-viscosity oil (<10 cP). Stokes' law shows bubble rise velocity is inversely proportional to viscosity:

v_rise = (2/9) * (rho_l - rho_g) * g * R^2 / mu

At 80,000 cP (Bluesky upper zone), a 2mm gas bubble rises at 0.022 mm/s — roughly 7,000x slower than the 15 cm/s assumed by McCoy. (Clift, Grace & Weber 1978, Ch.3; worked example in bubble-dynamics-reference.md)

This means: The standard 50 BPD/sq-in sizing rule OVERESTIMATES separator capacity by approximately 3 orders of magnitude for Bluesky heavy oil if applied to dispersed gas bubbles. Conventional gravity separation of micro-bubbles is physically impossible at this viscosity.

### 7.2 The Viscosity Correction

SPE-136665 (Alshmakhy & Maini 2010) shows that for foamy oil at GVF <40%, the correct viscosity to use is LIVE oil viscosity, not dead oil viscosity:
- Dead oil at atmospheric: ~3,050 cP (for 2,700 cP @ 30C test oil)
- Live oil at saturation: ~1,700 cP
- Ratio: dead/live = ~1.8x

Using dead oil viscosity underestimates bubble rise velocity by ~1.8x for this class of oil. However, even with this correction, the rise velocity in heavy oil remains negligible compared to flow velocities in a wellbore.

### 7.3 The WhaleShark Solution — Liquid Fallback, Not Bubble Rise

The WhaleShark (Section 1C) resolves this by inverting the separation mechanism:
- Conventional separators: Wait for gas to rise UP through liquid (bubble rise velocity governs) — FAILS in heavy oil
- WhaleShark: Let liquid fall DOWN past gas (liquid fallback velocity governs) — WORKS in heavy oil

Liquid fallback is driven by gravity acting on the dense liquid phase. The fallback rate depends on liquid density and geometry, NOT on oil viscosity in the same way bubble rise does. In slug and churn flow regimes (which dominate at high viscosity per Gokcal SPE-102727), liquid is frequently falling backward — the WhaleShark's upward-facing collector captures this naturally occurring phenomenon.

### 7.4 The Coalescence Prerequisite

Maini (1999, SPE-56541) and Sheng et al. (1999) show that dispersed micro-bubbles in foamy oil coalesce into free gas within 10-20 minutes after exiting the porous media. This means:
- IN the foamy zone (first 10-15m above intake): gas is dispersed, non-separable by ANY mechanism
- ABOVE the foamy zone: gas has coalesced into large bubbles or slugs, separable by liquid fallback
- Separator placement must be ABOVE the coalescence transition zone

### 7.5 Extrapolation Warning

No validated multiphase flow correlations exist above 6,000 cP (Gokcal SPE-102727 tested to 587 cP; Springer 2017 tested to 6,000 cP). At 80,000 cP:
- Standard flow pattern maps (Barnea 1987) are unreliable
- Slug flow dominates the entire production velocity envelope
- Dispersed bubble flow is impossible above ~600 cP
- All calculations in this section are first-principles extrapolations that should be validated with field data

## 8. BHA Stack Design — Separator + WellFi + PCP Integration

### 8.1 Physical Arrangement (for 8-5/8 inch Casing, OBE Reference Geometry)

Stacking order from bottom to top of the BHA:

1. Mud Joints (sump) — 2-3 joints standard tubing, sand/solids settle here
2. Solids Separation Section — Gravity + momentum weir system (WhaleShark-type)
3. Gas Separation Section (WhaleShark-type) — 18 ft, upward-facing collector, eccentric A3 region
4. WellFi Sonde — Clamped to tubing, wireless EM, reads liquid hydrostatic head
5. No-Turn Tool — Prevents rod string from backing off tubing connections
6. Tag Bar — Controlled stop when RIH
7. PCP (Progressing Cavity Pump) — Rotor + stator, rod-driven, intake from separator dip tube
8. Tubing String to Surface

### 8.2 Annular Clearances

| Component | OD (in) | 8-5/8 inch Casing ID (in) | Annular Gap (in) |
|---|---|---|---|
| 2-7/8 inch EUE Tubing | 2.875 | 7.921 | 2.52 per side |
| WhaleShark separator body | ~3.5 (35 series) | 7.921 | 2.21 per side |
| WellFi sonde (on tubing) | ~3.0 (estimated) | 7.921 | 2.46 per side |
| PCP stator | ~3.75 (typical) | 7.921 | 2.09 per side |

### 8.3 Separator Placement Relative to WellFi

- WellFi position: Near the pump intake, ~820m MD (OBE Run 3 reference)
- Separator position: Below the WellFi sonde in the BHA stack
- Physics basis: Separator collects fluid from below (mud joints > solids > gas separation > liquid to pump). WellFi sits above separator and reads hydrostatic head of degassed liquid column.
- Monitoring integration: WellFi P/T indicates separator performance:
  - Stable P with smooth decline = good separation, consistent pump fillage
  - Erratic P oscillations = poor separation, gas interference at pump
  - Sudden P drops = gas slug bypassing separator
  - Temperature anomalies = PCP thermal stress from gas compression (per Bratu SPE-95272)

## 9. Design Calculations — Worked Examples for OBE Reference Well

### 9.1 Stokes Law Bubble Rise (80,000 cP Bluesky Bitumen)

Given:
  rho_l = 997 kg/m3 (Bluesky oil at reservoir conditions)
  rho_g = 0.8 kg/m3 (methane at wellbore pressure)
  mu = 80,000 cP = 80 Pa.s (dead oil) or ~40,000 cP (live oil per SPE-136665 ratio)
  d = 2 mm = 0.002 m (typical dispersed bubble)
  g = 9.81 m/s2

Stokes rise velocity (dead oil):
  v = (1/18) * (997 - 0.8) * 9.81 * (0.002)^2 / 80
  v = 2.72e-5 m/s = 0.027 mm/s

Stokes rise velocity (live oil, corrected per SPE-136665):
  v = 0.027 * (80,000 / 40,000) = 0.054 mm/s

Time to rise 1 m (dead oil): 1 / 2.72e-5 = 36,800 s = 10.2 hours
Time to rise 1 m (live oil): 1 / 5.44e-5 = 18,400 s = 5.1 hours

CONCLUSION: Micro-bubbles are NON-RISING in heavy oil. Gravity separation of dispersed foamy oil is physically impossible. Only works on FREE GAS (coalesced bubbles > 10mm) or via liquid fallback mechanism.

### 9.2 Nagoo Critical Gas Velocity (OBE 8-5/8 inch Casing at 86 deg)

Given (OBE 102 HZ 16-18 reference):
  D_casing_ID = 7.921 in = 0.2012 m (8-5/8 inch casing)
  D_tubing_OD = 2.875 in = 0.0730 m (2-7/8 inch EUE)
  D_H = D_casing - D_tubing = 0.2012 - 0.0730 = 0.1282 m (hydraulic diameter)
  theta = 86 deg from vertical
  cos(86 deg) = 0.0698
  rho_l = 997 kg/m3
  rho_g = 0.8 kg/m3
  sigma_gl = 0.025 N/m (estimated for heavy oil/methane)

At 86 deg inclination, cos(theta) is very small (0.07), making the critical velocity very high. This means liquid loading is VERY UNLIKELY in the near-horizontal section. BUT this also means liquid cannot fall back easily either — it tends to accumulate. This is the heel-loading phenomenon described by Nagoo/Kannan (SPE-195893).

For the build section (~60 deg): cos(60) = 0.5, critical velocity drops substantially — this is where liquid loading and flow reversals are most active, and where the separator is most effective.

## Source Papers

| Ref | Title | Authors | Year |
|---|---|---|---|
| Saponja 2021 SWPSC | Enhancing Downhole Gas and Solids Separation (WhaleShark) | Saponja, Hari, David, Brignac, Jaszan, Coyes, VanHuss, Nagoo, Penner | 2021 |
| McCoy and Podio 1998 | Improved Downhole Gas Separators | McCoy, Podio | 1998 |
| MDPI 2021 | Phase Isolation Method for Downhole Separator | Yang et al. | 2021 |
| SPE-171890 | Multiphase Flow Performance of ICDs (lab methodology) | Mayer, Spiecker, Shuchart, Burkey, Ufford, Brysch | 2014 |
| SPE-136665 | Viscosity of Foamy Oils (cross-reference) | Alshmakhy, Maini | 2010 |
| CGW 1978 | Bubbles, Drops and Particles (cross-reference) | Clift, Grace, Weber | 1978 |
| SPE-102727 | Effects of High Oil Viscosity on Flow Behavior (cross-reference) | Gokcal et al. | 2007 |
| SPE-56541 | Foamy Oil Flow (cross-reference) | Maini | 1999 |
| SPE-95272 | PCP in Multiphase Conditions (cross-reference) | Bratu | 2005 |
| SPE-190921 | Critical Gas Velocity Equation (cross-reference) | Nagoo et al. | 2018 |
| SPE-195893 | Heel Dominant Liquid Loading (cross-reference) | Kannan, Nagoo | 2019 |
