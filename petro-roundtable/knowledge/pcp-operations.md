# PCP Operations in Deviated & Horizontal Wells — Knowledge Base

> Curated from 5 SPE/technical papers on progressive cavity pump design, fatigue mechanics, and field performance in deviated and horizontal heavy oil wells. All data points cite source papers.

## Quick Reference Table

| Property | Value | Source |
|---|---|---|
| Rod-driven PCP practical max inclination | ~50 deg | SPE-192464 |
| ESPCP max demonstrated inclination | 86 deg | SPE-136816 |
| DLS failure onset (rod-driven) | 3 deg/100ft (0.98 deg/10m) | SPE-192464 |
| DLS critical threshold (rod breaks cluster) | 2 deg/10m (6.1 deg/100ft) | Energies-15-04259 |
| DLS max for ESPCP (7-inch casing) | 7 deg/30m | SPE-136816 |
| DLS max for ESPCP (tangent section) | 15 deg/100ft | SPE-93594 |
| Rod-tubing wear share of all PCP failures | 30-50% | Industry consensus |
| Rod-driven run life in deviated wells | 45-118 days | SPE-192464, SPE-93594 |
| ESPCP run life | 400-1,400 days | SPE-136816 |
| ESPCP pump efficiency | 70% (vs 30% for ESP centrifugal) | SPE-136816 |
| Rod string energy loss | ~30% of total PCP energy | SPE-136816 |
| Rod body failure share of all failures | 85.3% | Energies-15-04259 |
| Hollow rod stress reduction | ~80% in critical DLS sections | SPE-192464 |

## 1. PCP Types and Selection Criteria

### Rod-Driven PCP (Surface Drive)
- Surface drive head rotates polished rod, which turns the rod string, which turns the downhole rotor inside the stator
- Simple, low capital cost, widely available
- **Limitation:** Rod string creates friction, wear, and fatigue in deviated wells

### ESPCP (Electric Submersible PCP — Rodless)
- Downhole electric motor (ESP motor or permanent magnet motor) directly drives the PCP rotor via gear reducer
- Eliminates rod string entirely — no rod-tubing wear, no rod fatigue
- Higher capital cost but dramatically longer run life in deviated/horizontal wells

### Selection Guide

| Well Condition | Recommended System | Rationale |
|---|---|---|
| Deviation <50 deg, DLS <3 deg/100ft | Rod-driven PCP | Standard, lowest cost |
| Deviation 50-70 deg OR DLS 3-6 deg/100ft | Rod-driven with hollow rod hybrid | SPE-192464: 4x run life improvement |
| Deviation >70 deg OR DLS >6 deg/100ft | ESPCP | SPE-136816, SPE-93594 |
| Deviation >80 deg | ESPCP required | No rod-driven data above ~50 deg |

## 2. DLS Failure Thresholds

### SPE-192464 (Ecopetrol, 2018) — Field Failure Data

**Well A:** 49.39 deg deviation, pump at 3,056ft MD, max DLS 6.1 deg/100ft at 1,382ft
- All rod failures clustered at 700-1,200ft MD (DLS 4-5 deg/100ft zone)
- Conventional sucker rods AND continuous rods both failed
- **Run life with standard rods: 45 days**
- **Run life with hollow rods: 180 days** (4x improvement)
- 5 pulling jobs, all for rod string mechanical failures (broken body or coupling)
- Operating at 233 RPM

**Well B:** 44 deg deviation, max DLS 7.8 deg/100ft at 605ft
- Continuous rod failed where DLS jumped from 0 to 7.8 deg/100ft
- **Run life with hollow rods: 300+ days** (still running at publication)
- Operating at 186 RPM

### Energies-15-04259 (Sheshmaoil, 2022) — 175 Failure Cases

- DLS >= 2 deg/10m (6.1 deg/100ft) defines **"elbow" danger zones**
- 42% of rod breaks within +/-50m of elbows (JSC Kondurchaneft)
- 45% at JSC Sheshmaoil
- 76% at JSC Ideloil
- **Rod body failures: 85.3%** of all rotating string failures (not couplings, not threads)
- Longer rod strings break closer to the wellhead (upper sections carry highest tension)
- Example: Well 3633 had 12 rod breakages in 2 years, max DLS 2.39 deg/10m at 250m, average DLS at break points 1.85 deg/10m

### DLS Summary

| DLS Range | Risk Level | Expected Outcome | Source |
|---|---|---|---|
| <2 deg/100ft | Low | Standard rod string survives | SPE-192464 |
| 2-3 deg/100ft | Moderate | Monitor rod condition closely | SPE-192464 |
| 3-5 deg/100ft | High | Fatigue failures likely within months | SPE-192464 |
| 5-6 deg/100ft | Very High | Rod breaks in <45 days | SPE-192464 |
| >6 deg/100ft | Critical | Rod-driven PCP not viable — use ESPCP or hollow rods | Energies-15-04259 |
| >7.8 deg/100ft | Extreme | Rapid failure even with continuous rod | SPE-192464 |

## 3. Fatigue Mechanics — C-FER Method (SPE-171352)

The definitive fatigue calculation method for PCP rod strings, by Paul Skoczylas of C-FER Technologies (2014).

### Key Equations

**Wellbore radius of curvature:**
R0 = (360 * 30) / (2 * pi * DLS) where DLS is in deg/30m

**Bending stress:**
sigma_bend = (E * D) / (2 * R_rod) where R_rod is effective radius at the coupling

**Von Mises effective mean stress:**
sigma_eff = sqrt(sigma_axial^2 + 3 * tau_torque^2)

**Goodman effective stress (conservative):**
S_eff = sigma_bend / (1 - sigma_eff / Su)

**Gerber effective stress (less conservative):**
S_eff = sigma_bend / (1 - (sigma_eff / Su)^2)

**Cycles to failure:**
N = (S_eff / S_f-eff)^(1/B_eff)

**Time to failure (days):**
t = N / (RPM * 60 * 24)

### S-N Curve Correction Factors

All factors multiply together to give combined Ceff:

| Factor | Symbol | Values | Source |
|---|---|---|---|
| Surface finish | Csurf | ~0.5 for hot-rolled rods | SPE-171352 |
| Environment | Cenv | 1.0 non-corrosive, 0.75 mild, 0.50 moderate, 0.40 severe | SPE-171352 |
| Size | Csize | 0.90 for 10-50mm rods | SPE-171352 |
| Combined (typical field) | Ceff | 0.3-0.4 | SPE-171352 |

**CRITICAL:** No endurance limit should be assumed in PCP applications. Corrosive environments, multiaxial stresses, and higher-strength steels all invalidate the traditional infinite-life assumption. The S-N curve should be extended at the same slope, not assumed flat below any threshold. (SPE-171352)

### Curvature Magnification at Couplings

Coupled rod strings do NOT follow tubing curvature smoothly. The coupling holds the rod body away from the tubing wall, creating **magnified curvature** (and therefore magnified bending stress) in the rod body near the coupling. This is the primary fatigue driver — not the nominal wellbore DLS. (SPE-171352)

**Mitigations:**
- Reduce distance between upsets (add rod guides) — significantly reduces effective curvature
- Use slimhole couplings — reduces standoff distance
- Both dramatically improve fatigue life

**Note:** Larger pump at lower speed is NOT always better for fatigue. Higher mean loads from the larger pump can negate the benefit of fewer cycles. Each case must be calculated individually. (SPE-171352)

### Size Correction Factors by Rod Diameter

| Rod Diameter | Csize |
|---|---|
| 22.2 mm | 0.88 |
| 25.4 mm | 0.87 |
| 31.8 mm | 0.85 |
| 38.1 mm | 0.84 |

## 4. ESPCP Operating Envelope

### SPE-136816 (CNOOC, 150+ Installations)

| Parameter | Limit |
|---|---|
| Viscosity | 100-8,000 mPa.s |
| Temperature at pump | <120 degC |
| GOR | <20% |
| Sand content | <15% vol |
| Min submergence | 100m |
| Max DLS (7-inch casing) | 7 deg/30m |
| Inclination range (demonstrated) | 20-86 deg |
| Average run life | 400+ days |
| Max run life | 1,400 days (Bohai Bay) |

PCP flow rate formula: **Q = 4 * E * D * Ps * n** where E=eccentricity, D=rotor diameter, Ps=stator pitch, n=RPM. (SPE-136816)

Primary ESPCP failure modes:
- Elastomer failure: 43% (dry running + debonding at high speed)
- Motor overheat: 37% (insufficient flow rate for cooling)
- Mechanical transfer: 11.4%
- Cable connection: 8.6%

### SPE-93594 (CPI Kulin Horizontal Wells)

| Parameter | Value |
|---|---|
| Max build rate design limit | 15 deg/100ft in tangent section |
| Installed inclination | 58-64 deg |
| Run life | 450-800+ days (zero pump failures) |
| Pump efficiency | 56-66% (vs 30% for tubing pumps) |
| Production | 2.5-3.5x vertical well equivalent |
| Motor | 2-pole, 562 series, 38 HP, 453V, 53A |
| Gear ratio | 9:1 (2,333 RPM motor -> 259 RPM pump) |
| Elastomer temp grades | 95, 105, 135, 150 degC |

**Backflush capability** by reversing motor rotation = critical maintenance feature for clearing intake plugging without pulling. (SPE-93594)

## 5. Resonant Torsional Oscillations (Energies-15-04259)

Curved well sections ("elbows") lower the natural torsional oscillation frequency of the rod string. When the rod's natural frequency matches the operating RPM, **resonant vibration** causes rod-tubing shock impacts, accelerating fatigue and wear.

### Resonant RPM by Rod Diameter (Well 3633 example)

| Rod Diameter | Resonant RPM |
|---|---|
| 19 mm | 4.41 |
| 22 mm | 5.91 |
| 25 mm | 7.63 |

**Circular frequency:** omega = sqrt(C / (J_D + K * J_r)) where K = 1/3 (mass reduction factor)
**Rod string stiffness:** C = G * J_p / (section length), where G = shear modulus, J_p = pi * d^4 / 32

**Mitigation:** Calculate natural frequency for the specific well trajectory and rod string, then operate at an RPM that avoids resonance. (Energies-15-04259)

## 6. Rod-Driven vs ESPCP Comparison

| Parameter | Rod-Driven PCP | ESPCP |
|---|---|---|
| Max inclination | ~50 deg practical | 86 deg demonstrated |
| Max DLS tolerance | 3 deg/100ft onset of failure | 7-15 deg/100ft design limit |
| Pump efficiency | Same pump, but ~30% energy lost to rod string | 70% pump efficiency |
| Run life (deviated) | 45-118 days typical | 400-1,400 days |
| Rod-tubing wear | Primary failure mode (30-50% of failures) | Eliminated (rodless) |
| Backflush | Not available | Motor reversal clears plugging |
| Capital cost | Lower | Higher (motor + cable + gear reducer) |
| Operating cost | Higher (frequent pulling, rod replacement) | Lower (extended run life) |
| Sand tolerance | Good (PCP inherent) | Good (same PCP) |
| Gas tolerance | Good (<20% GOR) | Good (<20% GOR) |

## 7. Mitigation Strategies for Rod-Driven PCP

For wells where ESPCP is not available or economically justified:

1. **Hollow rods at critical DLS sections** — 80% stress reduction, 4x run life. Polar moment of inertia ~10x standard rods. Use hybrid string: hollow rods only in DLS sections, standard rods elsewhere. (SPE-192464)
2. **Rod guides/centralizers at high-DLS points** — TsNShP design with sliding bearings achieves 67% centering. Maintain coaxiality to reduce vibration-induced breakage. (Energies-15-04259)
3. **Slimhole couplings** — Reduce coupling-to-tubing standoff, lower curvature magnification at connections. (SPE-171352)
4. **Corrosion inhibitor programs** — Environment factor from 0.4 (severe) to 1.0 (non-corrosive) roughly doubles fatigue life. (SPE-171352)
5. **Avoid resonant RPM** — Calculate natural torsional frequency, operate away from it. (Energies-15-04259)
6. **Convert to ESPCP** when deviation >50 deg or DLS persistently >6 deg/100ft. (All papers)

## 8. Application to OBE 102 HZ 16-18-83-17W5

| Parameter | OBE Well Value | Literature Guidance |
|---|---|---|
| Inclination at pump | 86.3 deg | Well above ~50 deg rod-driven limit |
| DLS at pump (1.85 deg/30m) | Below critical threshold | DLS alone is acceptable |
| Avg pump run time | 5 months (~150 days) | Aligns with 45-118 day range for rod-driven in deviated wells |
| Rod string condition | Continuous side-loading at 86 deg | Rod lying on bottom of tubing = constant wear |
| Recommended system | ESPCP | SPE-136816 demonstrated 86 deg with ESPCP |
| Expected ESPCP run life | 400-1,400 days | 3-10x current run life |

**Interpretation:** The 5-month average pump run time at OBE is consistent with rod-driven PCP operating at the extreme of its capability. The DLS is manageable (1.85 deg/30m < critical thresholds), but the **continuous 86-deg inclination** means the rod rests on the low side of the tubing for the entire string length, creating persistent side-loading wear. ESPCP would eliminate this failure mode entirely.

**WellFi value proposition:** Real-time pressure and temperature trending via WellFi can detect gradual pump wear (Signature #6 in wellfi-telemetry.md) — enabling proactive workover scheduling and avoiding unexpected failures.

## Source Papers

| ID | Title | Authors | Year |
|---|---|---|---|
| SPE-136816 | Application of ESPCP in China Offshore Oilfield | Feng, Meng, Li et al. (CNOOC/PCM) | 2010 |
| SPE-93594 | ESPCP Application in Kulin Horizontal Wells | Taufan, Adriansyah, Satriana (CPI) | 2005 |
| SPE-171352 | Drive String Fatigue in PCP Applications | Skoczylas (C-FER Technologies) | 2014 |
| SPE-192464 | Improvement of PCP Run Life in Highly Deviated Wells | Castillo, Valderrama, Godoy (Ecopetrol/Tenaris) | 2018 |
| Energies-15-04259 | Improving Efficiency of Curved Wells by Means of PCPs | Isaev et al. (Sheshmaoil/SPb Mining) | 2022 |

---

# PCP Performance in Multiphase/Gas-Interfered Conditions

> Distilled from SPE-95272-MS: "Progressing Cavity Pump (PCP) Behavior in Multiphase Conditions," C. Bratu, PCM Pompes (2005). Presented at the 2005 SPE Annual Technical Conference, Dallas TX. Experimental data from PCM's CREMHyG/Turbomachinery Laboratory, Grenoble, France.

---

## Quick Reference — Multiphase Performance Numbers

| Parameter | Value | Source |
|---|---|---|
| Max GVF tested experimentally | 90% (GVF = 0.9) | Bratu 2005, Table 1 |
| Pump tested | PCM Oilfield 100 TP 600, 13 stages | Bratu 2005, Table 1 |
| Flow rate range tested | 10–60 m³/d (63–377 bpd) | Bratu 2005, Table 1 |
| Head tested | 600 m (2,000 ft); discharge P = 40 bar | Bratu 2005, Table 1 |
| Rotational speeds tested | 100 and 300 RPM | Bratu 2005, Table 1 |
| Fluids | Water, oil (1200 cP at 20°C, 600 cP at 30°C), air | Bratu 2005, Table 1 |
| Pressure gradient ratio (GVF=0.9 vs liquid) | ~4× steeper in discharge stages | Bratu 2005, p.3, Fig. 3 |
| Temperature ratio at discharge (GVF=0.9) | T13/T10 = 2.9 (20°C/7°C) | Bratu 2005, p.5 |
| Temperature ratio at discharge (GVF=0.5) | T13/T10 = 2.5 (10°C/4°C) | Bratu 2005, p.6 |
| Pressure distribution extent at GVF=0.9, high RPM | Concentrated in stages 10–13 (final ~25% of pump) | Bratu 2005, p.5 |
| Pressure distribution extent at GVF=0.9, low RPM | Extended to stages 8–13 (final ~46% of pump) | Bratu 2005, Fig. 8 |

---

## Gas Handling Capability

### Mechanism: Slippage as Gas Compensation

A PCP handles free gas through an internal slippage mechanism. As gas enters the pump cavities, it occupies volume. The PCP compensates by routing a portion of its slippage flow (internal backflow from discharge toward intake, across the rotor-stator contact seal) back into the cavity to replace the volume that gas compression "consumed." This is the **slippage-compensation** process. (Bratu 2005, SPE-95272, Appendix)

This is fundamentally different from a centrifugal pump's gas-lock failure: the PCP's positive-displacement geometry creates a closed cavity that physically compresses gas from intake pressure to discharge pressure, cavity by cavity. The pump does not stall; it compresses. (Bratu 2005, SPE-95272, p.1)

### Pressure Distribution vs GVF

In liquid flow (GVF = 0), pressure builds **linearly** across all 13 stages. This is described by:

`Px/Pd = 1 - x/L`  (Eq. 18)

where Px is section pressure, Pd is discharge pressure, x is position from discharge, L is total pump length. (Bratu 2005, SPE-95272, p.8)

In multiphase flow (GVF > 0), this becomes nonlinear:

`Px/Pd = 1 - F(α, x/L)`  (Eq. 4/17)

where F is a polynomial function of GVF (α) and position. At GVF = 0.9, the pressure curve is **~4 times steeper in the discharge stages** compared to liquid flow, and the inlet stages (1–9) carry almost no pressure differential. The discharge stages (10–13) absorb the entire pressure build-up. (Bratu 2005, SPE-95272, p.3, Fig. 3)

### Effect of Pump Speed on Pressure Distribution

Pump speed (RPM) interacts with GVF to shift where pressure is concentrated:

- **High RPM (300 RPM) + high GVF (0.9):** Slippage compensates compressed gas volume, limiting pressure to stages 10–13 only (final 3-4 stages of 13)
- **Low RPM (100 RPM) + high GVF (0.9):** Pressure distribution extends to stages 8–13 — gas is less concentrated because lower speed allows more slippage-compensation per stage (Bratu 2005, SPE-95272, p.5, Fig. 8)
- **Low RPM + low GVF (0.1):** Pressure distributed across all 13 stages — behaves near-liquid

**Practical implication:** Operating at lower RPM with high-GVF fluid gives more uniform pressure loading across the stator, reducing the peak stress concentration in discharge stages. Higher RPM concentrates the thermal and mechanical load. (Bratu 2005, SPE-95272, p.5)

### GVF Limit — What the Data Shows

The paper does not state a hard GVF failure threshold. The PCM test pump operated successfully at GVF = 0.9 (90%) at both 100 and 300 RPM with P = 40 bar discharge pressure. The **failure risk at high GVF is thermal and mechanical** (stator degradation from concentrated pressure), not an immediate hydraulic lockout. The existing ESPCP GOR limit of "< 20%" (SPE-136816, in pcp-operations.md) refers to a conservative design guideline for long-term reliability, not hydraulic capability. (Bratu 2005, SPE-95272, p.4–6)

---

## Foam Effects

### How Foam Differs from Free Gas

The paper does not treat foam (stable gas-in-oil emulsion) separately from free gas as a distinct fluid state. However, the thermal analysis provides indirect insight:

When oil is the liquid phase (1200 cP at 20°C), the rotor-stator interface is **oil-lubricated** regardless of GVF, because the centrifugal acceleration of the rotor throws liquid to the outer radius, maintaining an oil film at the rotor-stator contact even at GVF = 0.9. This is described as: "the interference fit is oil lubricated and the friction coefficients are equivalent." (Bratu 2005, SPE-95272, p.6)

**Implication for foam:** A stable foam (gas dispersed as fine bubbles in oil) would behave similarly to the oil-continuous phase in the tests — the liquid film would be maintained at the contact, and the pump would handle the mixture without a step-change in friction coefficient. The gas fraction still compresses, but the lubrication mechanism is preserved. This is effectively more favorable than large slugs of free gas entering a cavity. (Bratu 2005, SPE-95272, p.6 — inferred from oil-lubrication discussion)

### No Foam-Specific Efficiency Curve Provided

The paper does not present a volumetric efficiency vs GVF curve. The experimental program measured pressure distribution and temperature as functions of GVF and RPM, not volumetric efficiency directly. The slippage-compensation model (Appendix) implies volumetric efficiency degrades with GVF because more slippage flow is consumed compensating compressed gas volume — but no numerical efficiency table is provided. (Bratu 2005, SPE-95272, Appendix)

---

## Gas Interference Symptoms

### Temperature as the Primary Diagnostic

The most actionable finding of the paper: **temperature rise is the measurable proxy for gas interference and stator failure risk.**

There are two distinct temperature sources in a PCP handling gas:

1. **Thermo-hydraulic process (discharge stages):** Gas compression by the polytropic process generates heat in stages 10–13. This is proportional to the pressure gradient — higher GVF = steeper gradient = more compression heat in fewer stages.
2. **Thermo-mechanical process (inlet stages 1–9):** Viscous friction between the rotor and the strained stator generates heat throughout the pump. This is proportional to pressure gradient × friction coefficient × pump velocity (Eq. 3: T ∝ P × f × N).

The two mechanisms are distinguishable by location: discharge stages (10–13) show the thermal signature of gas compression; inlet stages (1–9) show the signature of viscous friction lubrication. (Bratu 2005, SPE-95272, p.2, p.5)

### Quantified Temperature Signatures

| Condition | Location | Temperature Rise | Ratio |
|---|---|---|---|
| GVF=0.9, N=300 rpm, P=40 bar | Discharge stages 10–13 | T13/T10 = 20°C/7°C | 2.9 |
| GVF=0.5, N=300 rpm, P=40 bar | Discharge stages 10–13 | T13/T10 = 10°C/4°C | 2.5 |
| Low GVF, N=100 vs 300 rpm | Inlet stages 1–9 | Te/Th = 2.4 (friction model) | — |

(Bratu 2005, SPE-95272, p.5–6, Figs. 9, 10)

### Observable Symptoms vs Other Failure Modes

| Symptom | Gas Interference | Sand Plugging | Rod/Stator Wear |
|---|---|---|---|
| Temperature concentrated in discharge stages | Yes — primary signature | No | No — uniform or inlet-biased |
| Temperature at inlet stages elevated | Secondary (friction) | No | Yes — primary |
| Pressure gradient nonlinear (steep at discharge) | Yes | No — pressure drop at intake | Gradual across all stages |
| Erratic torque / power spikes | Yes — cavity pressure surges during slug entry | Less likely | Progressive increase |
| Reduced flow rate | Progressive as GVF rises | Sudden blockage | Progressive |

**Critical point:** Temperature at the **discharge end** of the pump is the diagnostic for gas-interference-induced stator failure risk. Temperature at the **inlet end** reflects friction (wear) conditions. These two signals should be monitored independently. (Bratu 2005, SPE-95272, Conclusions p.6–7)

### Stator Deformation Mechanism

The concentrated pressure gradient in discharge stages causes **stator radial deformation** (Bowden's model, Fig. 2B in paper). The strained stator increases viscous friction torque on the rotor, which further increases temperature — a positive feedback loop. Temperature rise at discharge stages is therefore both a symptom AND an accelerating cause of stator failure. (Bratu 2005, SPE-95272, p.2–3)

---

## Separator Quality Impact

### Separator Is Not the Primary Variable in This Paper

SPE-95272 is a laboratory pump-performance study, not a field separator study. The GVF at the pump intake was a controlled test parameter (0 to 0.9), not derived from separator efficiency. Therefore, the paper does not quantify separator efficiency vs pump life directly.

### What the Data Implies for Separator Requirements

The thermo-hydraulic model is clear: **pressure distribution severity is directly proportional to GVF at pump intake.** From the nonlinear pressure formula (Eq. 4), a step increase in intake GVF produces a disproportionate increase in discharge-stage pressure gradient and temperature. Specifically:

- GVF = 0.1 → pressure nearly linear (minimal gas concentration effect)
- GVF = 0.5 → discharge stages carry ~33% more pressure gradient than liquid case
- GVF = 0.9 → discharge stages carry ~4× the pressure gradient of liquid case (Bratu 2005, SPE-95272, p.3, Fig. 3, Fig. 8)

**Practical implication:** Any separator malfunction that allows GVF at the pump intake to rise from, say, 0.3 to 0.8 does not linearly increase stator thermal stress — it increases it disproportionately, because the pressure distribution function F(α, x/L) is nonlinear in α. Separator efficiency therefore has a nonlinear effect on pump thermal reliability.

### Operating Guideline Derived from Paper

The paper confirms the pump can handle GVF up to 0.9 without hydraulic failure. However, the thermal data shows that GVF above ~0.5 begins to shift significant heat load into 3–4 discharge stages. For elastomer stator longevity, keeping intake GVF below 0.5 is conservative. The CNOOC ESPCP operating limit of GOR < 20% (SPE-136816) reflects a much more conservative elastomer-protection criterion than this paper's hydraulic capability data suggests is necessary. (Bratu 2005, SPE-95272, p.5; cross-reference: SPE-136816 in pcp-operations.md)

---

## Design Recommendations

### Speed Management Under High GVF

Lower pump speed (100 RPM vs 300 RPM) at high GVF distributes the pressure gradient more evenly across pump stages — extending the pressure build-up zone from 3–4 stages to 5–6 stages and reducing peak thermal stress in any single stator section. (Bratu 2005, SPE-95272, p.5, Fig. 8)

**Recommendation:** When operating with known high GVF (>0.5), reduce pump RPM to spread the pressure load. This is the opposite of a common field instinct to "speed up to maintain rate."

### Temperature Monitoring — Where to Place Sensors

If downhole temperature sensors are available:
- **Discharge-end sensor (stages 10–13 equivalent):** Monitors gas compression thermal load. Rising T here with stable intake T = increasing GVF
- **Intake-end sensor (stages 1–5 equivalent):** Monitors rotor-stator friction wear. Rising T here with stable discharge T = stator deformation or dry-running

Two-point temperature monitoring enables separation of gas-interference symptoms from wear symptoms — they are otherwise indistinguishable from surface torque/power data alone. (Bratu 2005, SPE-95272, Conclusions)

### Stator Elastomer Grade Selection

Higher GVF → higher discharge-stage temperatures from gas compression. The polytropic temperature ratio at GVF=0.9 is T13/T10 = 2.9 (approximately 20°C rise in final 3 stages at P=40 bar). At field conditions with higher pressures, this temperature rise will be greater. Elastomer temperature grade must account for ambient well temperature plus the compression-heating increment, not just the reservoir temperature. (Bratu 2005, SPE-95272, p.5; cross-reference: SPE-93594 elastomer grades 95–150°C in pcp-operations.md)

### Intake Depth / Submergence

The paper does not address intake depth directly. However, the slippage-compensation model (Appendix) shows that the pump's ability to handle high GVF depends on having adequate differential pressure across each cavity. Setting the pump deeper (higher submergence, higher intake pressure) increases the fluid density and reduces GVF at the intake by compressing the gas into solution — directly reducing the free gas fraction entering the pump. This is consistent with general ESP/PCP intake design practice. (Bratu 2005, SPE-95272, Appendix, Eq. 9)

---

## Integration with OBE 102 HZ 16-18-83-17W5

| Parameter | OBE Well Context | Bratu 2005 Guidance |
|---|---|---|
| Foamy oil production | Clearwater bitumen with dissolved gas, foam documented | Oil-lubricated rotor-stator contact maintained even at GVF=0.9 — favorable for stator |
| Gas kicks (WellFi Run 3) | CRC error spike Apr 3, hypothesized gas slug | Temperature spike at discharge stages would be the confirmation signal |
| PCP operating at 260 RPM | Higher speed = more concentrated pressure in discharge stages | If GVF is high during gas kick, discharge elastomer is the thermal hot spot |
| 5-month average run life | Consistent with high-inclination rod wear (pcp-operations.md) | Gas compression stress adds to thermal load — both degrade elastomer |
| WellFi temperature sensor | Reads downhole T at ~820m MD (tool position) | At 820m MD tool is near intake of pump — captures Thermo-mechanical (friction) signature, not discharge gas-compression signature |

**Key insight for WellFi interpretation:** The WellFi sensor at 820m MD is positioned near the pump intake, not the discharge. Per Bratu 2005, the **intake stages (1–9) reflect friction/wear temperature**, while the **discharge stages (10–13) reflect gas compression temperature**. A rising temperature trend at the WellFi position is therefore more likely to indicate rotor-stator wear (friction) than gas interference — unless a gas slug causes an immediate pressure/temperature transient. Gas interference would be better captured by a sensor at the pump discharge (above the pump). (Bratu 2005, SPE-95272, p.5–6; cross-reference: wellfi-telemetry.md Signature #6)

---

## Source Paper

| ID | Title | Author | Year | Conference |
|---|---|---|---|---|
| SPE-95272 | Progressing Cavity Pump (PCP) Behavior in Multiphase Conditions | C. Bratu, PCM Pompes | 2005 | SPE Annual Technical Conference, Dallas TX |

**Test pump:** PCM Oilfield 100 TP 600 (680 bpd nominal, 2,000 ft head, 13 stages, 500 RPM max)
**Test facility:** CREMHyG Turbomachinery and Cavitation Research Laboratory, Grenoble, France
**Instrumentation:** 21 pressure sensors, 10 temperature sensors, gas/liquid flow meters, speed/torque
