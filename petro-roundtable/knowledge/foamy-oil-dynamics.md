# Foamy Oil Dynamics — Knowledge Base

> Curated from 6 SPE papers on cold heavy oil production and foamy oil behavior in the Bluesky Formation and analogous Peace River reservoirs. All data points verified against source papers.

## Quick Reference Table

| Property | Value | Source |
|---|---|---|
| Bubble Point (Peace River) | 3,100-3,300 kPa | SPE-175390, SPE-174446 |
| Initial Solution GOR | 7-10 m3/m3 | SPE-175390, SPE-174446 |
| Dead Oil Viscosity Range | 5,000-1,000,000 cP | SPE-175390 |
| Live Oil Viscosity (Cold Lake model) | 51,314 cP | SPE-175390 |
| Dead Oil Density | 997.5 kg/m3 | SPE-175390 |
| Critical Gas Saturation | 0.5-2% (increases with depletion rate) | SPE-174431 |
| Min Mobility for CHOP Viability | >=0.05 md/cP | SPE-175390 |
| CHOPS Recovery Factor | 5-15%, average <10% | SPE-150633 |
| CSS+VSD Recovery Factor | 40-55% (PRISP/PREP analogs) | SPE-170879 |
| Dispersed Gas Viscosity | ~1,000x normal gas viscosity | SPE-174431 |
| Activation Energy (all reactions) | 59,100 J/gmol | SPE-174431 |

## 1. Foamy Oil Mechanism

Foamy oil is the dominant production mechanism in Peace River Bluesky cold production wells. When reservoir pressure drops below the bubble point (~3,100 kPa), dissolved gas exsolves but remains **trapped as dispersed microbubbles** within the viscous oil rather than forming a continuous free gas phase. This dispersed gas has apparent viscosity ~1,000x higher than free gas, which is why it flows with the oil instead of channeling separately. (SPE-174431)

### Four-Step Kinetic Process (SPE-175390, SPE-174431)

1. **Supersaturation:** Pressure drawdown drops BHP below bubble point, creating supersaturation
2. **Bubble Nucleation:** 4th-order dependence on supersaturation — small pressure drops produce few bubbles; aggressive drawdown produces many
3. **Bubble Growth:** Molecular diffusion feeds bubbles. 1st order to supersaturation + 1/3 order to dispersed gas mass
4. **Bubble Coalescence:** Film drainage between adjacent bubbles. nth order (tuned per reservoir)

### Six-Component Fluid Model (SPE-174431)

| Component | Phase | Role |
|---|---|---|
| Water | Aqueous | Connate + produced water |
| Dead Oil | Oleic | Base oil without dissolved gas |
| CH4_S (solution gas) | Oleic | Gas dissolved in oil at reservoir pressure |
| CH4_B (bubble gas) | Oleic | Nucleated bubbles smaller than pore size — flow with oil |
| CH4_D (dispersed gas) | Gaseous | Bubbles equal to or larger than pore size — may flow differently |
| CH4_F (free gas) | Gaseous | Coalesced free gas — flows independently |

**Key insight:** The apparent low gas-phase mobility in foamy-oil drive is modeled via the high dispersed-gas viscosity, NOT via rate-dependent relative permeability. This means standard relative permeability curves work across all rate conditions. (SPE-174431)

## 2. Kinetic Parameters

### Shen (2015) Model — SPE-174431

Validated against two independent lab datasets:

| Parameter | Value | Source |
|---|---|---|
| Activation energy | 59,100 J/gmol (all reactions) | SPE-174431 |
| k-value kv1 | 258,000 kPa | SPE-174431 |
| k-value kv2 | 0.004 kPa-1 | SPE-174431 |
| k-value kv4 | 880 degC | SPE-174431 |
| k-value kv5 | 266 degC | SPE-174431 |
| Nucleation order | 4 | SPE-174431 |
| Bubble growth orders | 1 + 1 + 0.33 | SPE-174431 |
| Coalescence order | n (tuned per reservoir) | SPE-174431 |

**Lab validation 1 — Kumar et al. 2002:** Sandpack 60 cm, PV 487 cm3, live oil 1,100 cP at 25 degC. Four drawdown rates: 0.08, 0.37, 3.0, 12.0 cm3/hr. (SPE-174431)

**Lab validation 2 — Ostos et al. 2004:** Sandpack 200 cm, PV 1,620 cm3, live oil 840 cP at 21 degC. Four drawdown rates: 0.041, 0.081, 0.161, 0.327 psi/min. (SPE-174431)

### Uddin (2005) Model — Alternative (SPE-150633)

| Reaction | Rate Constant | Units |
|---|---|---|
| Dissolved -> Dispersed bubbles (N1) | 0.48 | /day |
| Dissolved + Dispersed -> 2x Dispersed (N2) | 0.288 | (gmol/m3)^-2/day |
| Dispersed -> Connected gas (G1) | 0.0 | /day |
| Dissolved + Dispersed -> Dissolved + Connected (G2) | 0.48 | (gmol/m3)^-2/day |

k-values: Kv1=5.4547e5 kPa, Kv4=879.84 degC, Kv5=265.99 degC. Wormhole radius: 0.05m. (SPE-150633)

## 3. Production Implications

### Faster Drawdown = Higher Recovery

A foamy-oil dynamic model shows oil recovery **increases as well spacing decreases** because faster reservoir pressure depletion strengthens foamy-oil drive. A conventional black-oil model predicts constant ultimate recovery regardless of spacing — it only captures production acceleration, not incremental recovery. This is the fundamental difference. (SPE-175390)

### Shell Cliffdale Development (SPE-175390)

| Period | Laterals | Well Spacing | Completion |
|---|---|---|---|
| 2006-2010 | 1-2 | 75-100m | Production liner |
| 2011-2012 | 3-6 | 45-75m | Production liner |
| 2012-2013 | 5-12 | ~45m | Barefoot (open-hole) |

Barefoot laterals replaced production liners without compromising productivity. Resource scale: ~10 billion bbl bitumen in place across ~380 km2 lease. (SPE-175390)

### Reservoir Parameters — Cold Lake Typical Model (SPE-175390)

| Property | Value |
|---|---|
| Horizontal permeability | 2.5 darcy |
| Porosity | 0.32 |
| Kv/Kh | 0.2 |
| Initial reservoir pressure | 3,100 kPa |
| Dead oil density | 997.5 kg/m3 |
| Dead oil viscosity | 120,000 cP |
| Live oil viscosity | 51,314 cP |
| Connate water saturation | 0.23 |
| Solution GOR | 9.3 v/v |
| Bubble point | 3,100 kPa |

## 4. Wormholes and CHOPS

Progressive Cavity Pumps were the enabling technology for CHOPS. Removing sand-exclusion devices and switching to PCPs increased oil production up to 10x. Linear relationship between sand production rate and oil production rate. (SPE-150633)

### Wormhole Evidence

- **Burnt Lake field (Suncor):** Fluorescein dye tracer showed communication between wells 500m apart within hours (SPE-150633)
- **Elk Point (Amoco):** Dye traveled >2 km at velocities exceeding 7 m/min (420 m/hr) among 12 wells (SPE-150633)
- **Wormhole dimensions:** 5-15 cm diameter for sand-free channel, up to 1.5m for full wormhole zone (SPE-150633)
- **CHOPS recovery:** 5-15%, average <10% — approximately 90% of oil remains after CHOPS, making these fields prime EOR candidates (SPE-150633)

### CHOPS Reservoir Properties (SPE-150633)

| Property | Typical Value |
|---|---|
| Depth | 480m |
| Net pay | 5m |
| Porosity | 33% |
| Permeability | 2-4 darcy (avg 3) |
| Oil saturation | 80% |
| Initial pressure | 2,760 kPa |
| Temperature | 20 degC |
| Dead oil viscosity | 25,000 cP |
| Solution GOR | 10 m3/m3 |

### Sand-Arch Failure

Foamy oil reduces sand-arch stability, so sand failure occurs at lower pressure gradients with live oil than predicted by standard (dead-oil) criteria. Minimum fluidization velocity: 0.009-0.021 m/d. Dilation critical velocity: 2.6e-3 m/d. Sand-arch failure criterion: dP/dr > 2f*C0/R. (SPE-150633)

## 5. Gas Rate Oscillation (Geysering)

During constant-pressure depletion, gas production oscillates in a pattern similar to volcanic geysering. Gas production is limited by the rate of gas evolution from solution — when a gas slug is produced, the local pressure rises temporarily, suppressing further gas evolution until pressure drops again. (SPE-174431)

- Faster depletion = higher dispersed gas concentration = more efficient oil displacement
- This creates characteristic **pressure signatures detectable by downhole sensors** like WellFi
- The oscillation period depends on drawdown rate, oil viscosity, and pore volume

## 6. CSS Context (Thermal Alternative)

### Seal/Cadotte Properties (SPE-174446, Murphy Oil)

| Property | Value |
|---|---|
| Initial reservoir pressure | 4.5 MPa |
| Saturation pressure | 3.3 MPa |
| FVF | 1.02 m3/m3 |
| Solution GOR | 7.0 m3/m3 |
| Net pay | 19-25m |
| API gravity | 8.6 deg |
| Oil viscosity (20 degC) | 14,300-620,070 cP |
| Horizontal perm | 50-2,400 mD (avg 1,452) |
| Vertical perm | avg 726 mD |
| Porosity | 20-29% |
| Oil saturation | 52-83% |

CSS screening criteria: min 8m net pay, viscosity 5,000-100,000 cP, good Kv, transmissibility >0.01, max injection BHP 12.4 MPa (below Wilrich caprock fracture). CSS recovery potential: 15-25% OOIP from horizontal wells. (SPE-174446)

### Carmon Creek (SPE-170879, Shell Canada)

- 10 billion bbl in place, 7,000 wells over 35+ year life
- CSS followed by VSD in inverted 7-spot, 115m spacing
- SAGD failed due to shale baffles in tidal delta deposits
- Recovery: 40-55% (PRISP 1979-1994 and PREP 1996-2001 analogs)
- Pad design: 48-50 wells, 4m wellhead spacing

### Monitoring (SPE-118244, Shell)

- Seismic velocity: 2,900 m/s (virgin) -> 2,300 m/s (pressurized) -> 1,800 m/s (heated+fractured)
- Surface uplift during CSS: up to 10 cm (InSAR, 2-3 mm precision, 20-50m resolution)
- Residual gas/steam saturation after production: ~10%
- Steam preferentially moves toward pressure sinks in adjacent production units

## 7. Implications for WellFi Telemetry

| Observable | Foamy Oil Signature | Physics |
|---|---|---|
| P declining without pump speed change | Gas replacing liquid in annulus | Lower fluid density from dispersed gas |
| Overnight P drop when pump off | Gas accumulation/segregation | Buoyant gas migrates upward |
| Periodic P oscillations | Gas rate geysering | Gas evolution limited by local pressure |
| Rising GOR over months | Foamy oil transition | Pressure below pseudo-bubble-point |
| CRC error rate increase | EM signal disruption | Gas changes fluid conductivity in annulus |
| P depletion rate vs recovery | Faster drawdown = more foamy oil | Nucleation is 4th-order to supersaturation |

## Source Papers

| SPE # | Title | Authors | Year |
|---|---|---|---|
| SPE-175390 | Improving Cold Heavy Oil Development at Peace River with Foamy-Oil Dynamics | Shen, Hamm, Bdair (Shell) | 2015 |
| SPE-174431 | A Practical Approach for Modeling of Foamy Oil Drive Process | Shen (Shell) | 2015 |
| SPE-174446 | Impact of Formation Dilation-Recompaction on CSS: Seal's Cadotte | Yadali Jamaloei, Singh (Murphy) | 2015 |
| SPE-170879 | Carmon Creek Thermal Field Development Project | Vannaxay, Wasden, Howell (Shell) | 2014 |
| SPE-150633 | Well/Wormhole Model of Cold Heavy-Oil Production With Sand | Istchenko, Gates (U of Calgary) | 2014 |
| SPE-118244 | Insights from Monitoring Heavy Oil Production in Peace River | Maron, Bourne, Klemm et al. (Shell) | 2008 |

## Foamy Oil Viscosity — Wellbore-Scale Gas Behavior

*Source: Alshmakhy, A.B. and Maini, B.B. (2010), "Viscosity of Foamy Oils," CSUG/SPE 136665, Canadian Unconventional Resources & International Petroleum Conference, Calgary, Alberta, 19–21 October 2010.*

---

### Measurement Methods

Three viscometers were used in parallel to isolate instrument artifact from real fluid behavior — this methodological comparison is a central contribution of the paper.

**Cambridge Electromagnetic Viscometer (EMV)**
- Falling-piston principle: travel time of a magnetically driven piston through the fluid is proportional to absolute viscosity
- Accuracy: ±1% on absolute viscosity in centipoises
- Temperature controlled by cooling bath at 21.5 °C throughout all experiments
- Used in two modes: (1) live oil at constant pressure above bubble point, (2) foamy oil via controlled expansion — upstream BPR held at saturation pressure + 5%, downstream BPR stepped down to force expansion and gas release through the viscometer
- Flow rates tested: 2 cc/hr (low) and 10 cc/hr (high)
- (Alshmakhy & Maini 2010, SPE-136665, p. 4–6)

**Capillary Tube Viscometer**
- High-pressure capillary tube ~5 m length, 0.3175 cm outer diameter
- 1300 cc upstream transfer vessel, 1000 cc downstream blind vessel
- Pressure drop measured by Rosemount differential pressure transducer
- Viscosity calculated from Poiseuille's law: μ = ΔP/Q × (πr⁴/8L) = k × ΔP/Q
- Instrument constant k calibrated with oil of known viscosity at multiple flow rates
- Key limitation: flow rate at downstream end is difficult to determine precisely during foam expansion due to transient gas evolution — uncertainty in GVF calculation
- Workaround: constant injection upstream + constant withdrawal downstream (water) to define both ends of the mass balance
- Results consistently LOWER than EMV — capillary tube always underestimates foamy oil viscosity relative to EMV
- (Alshmakhy & Maini 2010, SPE-136665, p. 6–7)

**Slim Tube Viscometer (Sand-Packed)**
- 19 mm outer diameter tube, 30 cm length, packed with silica sand (100–140 mesh)
- Measures effective viscosity in porous media via Darcy's law
- Designed to represent reservoir-scale two-phase flow behavior — most relevant for porous media applications
- Showed results generally similar to EMV at low foam qualities (<40%)
- At foam quality >40%, stable differential pressures could not be achieved (unstable flow)
- (Alshmakhy & Maini 2010, SPE-136665, p. 7, 11)

**Oil Sample**
- Single crude oil from an unnamed Canadian heavy oil reservoir
- Dead oil viscosity: **2,700 cP at 30 °C** (measured by Anton-Paar)
- Dead oil density: **0.9297 g/cc at 30 °C**
- Basic sediment and water (BSW): 1%
- Live oil prepared by recombining crude with methane at 500 psi and 21.5 °C
- Live oil gas-oil ratio: **9.7 m³/m³** at 500 psi saturation
- All experiments at room temperature **21.5 °C** (not reservoir temperature)
- Composition: predominantly C₁₂+ heavy fractions; C₃₀+ fraction = 31.78 mole fraction, density 0.9985 g/cc
- Molecular weight of dead oil: 393 g/mol; C₃₀+ fraction MW: 722.73 g/mol
- (Alshmakhy & Maini 2010, SPE-136665, p. 2–3, Table 1)

---

### Key Findings

**1. Dead Oil Viscosity vs. Pressure (Figure 5)**

Dead oil viscosity was measured by EMV at 21.5 °C from 0 to 500 psi in 50 psi increments. Key data points read from Figure 5:

| Pressure (psi) | Dead Oil Viscosity (mPa·s = cP) |
|---|---|
| 0 (atmospheric) | ~3,050 |
| 50 | ~3,060 |
| 100 | ~3,080 |
| 150 | ~3,100 |
| 200 | ~3,130 |
| 250 | ~3,140 |
| 300 | ~3,150 |
| 350 | ~3,240 |
| 400 | ~3,260 |
| 450 | ~3,295 |
| 500 | ~3,310 |

Key finding: **dead oil viscosity increases only ~8% from atmospheric to 500 psi** — a moderate pressure effect. Variation is less than 10% across the full pressure range tested.
(Alshmakhy & Maini 2010, SPE-136665, p. 8, Figure 5)

**2. Live Oil Viscosity (Figure 6)**

Live oil viscosity measured at 500 psi saturation pressure, 21.5 °C, across flow rates 1–10 cc/hr:

| Flow Rate (cc/hr) | Live Oil Viscosity (cP) |
|---|---|
| 1 | ~1,700 |
| 2 | ~1,700 |
| 4 | ~1,680 |
| 6 | ~1,680 |
| 10 | ~1,700 |

Key finding: **live oil viscosity is completely independent of flow rate (shear rate)** — live oil is a Newtonian fluid. Capillary and slim tube viscometers confirmed the same result.

Live oil viscosity at 500 psi (~1,700 cP) is **substantially lower than dead oil viscosity at atmospheric pressure (~3,050 cP)**. Dissolved methane reduces viscosity by approximately **44%** at 500 psi saturation relative to dead oil at atmospheric. This dissolved-gas viscosity reduction is the baseline against which foamy oil behavior must be compared.
(Alshmakhy & Maini 2010, SPE-136665, p. 8–9, Figure 6)

**3. Foamy Oil Viscosity vs. Foam Quality — The Core Finding (Figures 4, 7, 8, 9)**

This is the central and most counterintuitive result of the paper. Multiple measurement approaches are presented:

**Capillary Tube — Figure 4 (pressure reduction from above bubble point):**

| Foam Quality / GVF (%) | Apparent Viscosity (cP) |
|---|---|
| 0 (live oil at bubble point) | ~1,750 |
| 30 | ~1,050 |
| 40 | ~940 |
| 50 | ~920 |
| 55 | ~880 |
| 60 | ~860 |
| 65 | ~855 |
| 80 | ~855 |
| 88 | ~855 |

The capillary viscometer shows viscosity DECREASING with increasing foam quality, from ~1,750 cP at the bubble point down to ~855 cP at 88% foam quality — approaching and then staying near a floor value. The authors note this is likely an artifact: the capillary viscometer allows gas to partially segregate from the oil, so it is measuring something between live oil and dead oil viscosity rather than the true dispersion viscosity.

**EMV + Slim Tube — Figure 8 and Figure 9 (controlled expansion approach):**

EMV data (Figure 8):
| Foam Quality / GVF (%) | Apparent Viscosity (cP) |
|---|---|
| 0 (live oil) | ~1,700 |
| 10 | ~1,700 |
| 20 | ~1,700 |
| 30 | ~1,700 |
| 40 | ~1,700 |
| 55 | ~2,300 |
| 60 | ~2,300 |
| 75 | ~2,500 |

Slim tube data (Figure 9):
| Foam Quality / GVF (%) | Apparent Viscosity (cP) |
|---|---|
| 20 | ~1,850 |
| 30 | ~1,750 |
| 40 | ~1,730 |
| 45 | ~1,720 |
| 55 | ~2,200 |

**Critical interpretation:** EMV and slim tube both show foamy oil viscosity staying near live oil viscosity (~1,700 cP) for GVF 0–40%, then increasing at higher GVF. This is the opposite of what capillary tube shows and the opposite of what classical dispersion theory predicts. A gas-in-liquid dispersion should increase viscosity above the continuous phase viscosity as GVF increases, but the measured apparent viscosity stays flat at ~live oil viscosity until ~40–50% GVF.

(Alshmakhy & Maini 2010, SPE-136665, p. 10–11, Figures 4, 8, 9)

**4. Effect of Flow Rate on Foamy Oil Viscosity — Figure 7**

Figure 7 plots viscosity vs. pressure during depletion for dead oil, live oil, foamy oil at 10 cc/hr, and foamy oil at 2 cc/hr, all measured by EMV:

| Pressure (psi) | Dead Oil (cP) | Live Oil (cP) | Foamy 10 cc/hr (cP) | Foamy 2 cc/hr (cP) |
|---|---|---|---|---|
| 100 | ~3,100 | ~2,800 | ~2,900 | ~2,700 |
| 200 | ~3,110 | ~2,460 | ~2,370 | ~2,330 |
| 300 | ~3,120 | ~2,130 | ~2,100 | ~2,100 |
| 400 | ~3,130 | ~1,790 | ~1,770 | ~1,760 |
| 500 | ~3,310 | ~1,700 | — | — |

Key finding: **foamy oil and live oil viscosities are nearly identical** at any given pressure during depletion. The two foamy oil flow rates (2 cc/hr and 10 cc/hr) produce slightly different results — 10 cc/hr gives marginally higher viscosity than 2 cc/hr, indicating a **mild shear-thinning (non-Newtonian) tendency** at higher foam qualities. However, the effect is small.

The authors explain this flow-rate sensitivity: at low flow rates, gas has more time to separate from oil, so the viscometer reads closer to live oil (supersaturated single-phase oil). At high flow rates, gas has less time to separate, so a true dispersion flows through — yet the viscosity barely differs.
(Alshmakhy & Maini 2010, SPE-136665, p. 9–10, Figure 7)

**5. Newtonian vs. Non-Newtonian Behavior**

- **Live oil: purely Newtonian** — viscosity independent of flow rate across the full 1–10 cc/hr range tested (Figure 6)
- **Foamy oil: mildly non-Newtonian** — viscosity shows slight shear-thinning at higher GVF (higher foam quality), but the effect is small relative to the absolute viscosity level
- Previous investigators (Marsden and Khan, 1966) found foam to be strongly non-Newtonian at GVF 70–96%, but those foams had much higher effective viscosity than the continuous phase. The Alshmakhy & Maini result — where foamy oil viscosity stays near live oil viscosity — suggests gas is either not forming a stable dispersion in the EMV or that the dispersion viscosity genuinely tracks live oil viscosity
- The authors explicitly state: "It strongly suggests that the flow-through electromagnetic viscometer is allowing gas to fully separate from the oil, especially at small flow rates. Therefore, these measurements may not be representative of the dispersion viscosity."
- The slim tube result is considered more physically representative for porous media/reservoir engineering applications
(Alshmakhy & Maini 2010, SPE-136665, p. 9, 12)

**6. What "Similar to Live Oil Viscosity for a Large Range of GVF" Means**

The paper's headline conclusion (Conclusion #3, p. 12) states: *"Viscosity of foamy oil, using Cambridge EMV and slim tube, was found to be similar to live oil viscosity for a large range of gas volume fractions."*

This means specifically:
- At foam quality 0–40% GVF, foamy oil viscosity measured by EMV = approximately **1,700 cP**, identical to live oil viscosity at 500 psi
- At foam quality 0–40% GVF, foamy oil viscosity measured by slim tube = approximately **1,700–1,850 cP**, also close to live oil
- This is substantially LOWER than dead oil viscosity (~3,050 cP at atmospheric)
- The range where this holds is GVF up to approximately **40–50%**

Above ~50% GVF, the EMV shows viscosity rising to ~2,300–2,500 cP — still well below dead oil viscosity but notably above live oil viscosity. The slim tube could not sustain stable pressure differentials above ~55% GVF.

**7. Temperature Effects**

The paper does not investigate temperature systematically. All experiments were conducted at **21.5 °C** (room temperature), which is **not representative of subsurface reservoir conditions** (typically 35–55 °C for shallow Bluesky/Clearwater). The Anton-Paar dead oil measurement was taken at **30 °C** (2,700 cP). The authors note the oil viscosity (dead oil) varied less than 10% across the 0–500 psi pressure range tested at constant temperature.

Limitation: the 21.5 °C test condition means all viscosity values in this paper are significantly higher than in-situ reservoir viscosities. For Obsidian/Bluesky application at ~35 °C, the foamy oil viscosity would be lower than reported here, but the *ratio* of foamy-to-live-oil viscosity should remain approximately valid.
(Alshmakhy & Maini 2010, SPE-136665, p. 2, 5–6)

---

### Data Tables — Extracted Values for Calculation Use

**Table A: Oil Properties (SPE-136665, Table 1 and p. 2)**
| Property | Value | Condition |
|---|---|---|
| Dead oil viscosity (Anton-Paar) | 2,700 cP | 30 °C |
| Dead oil density | 0.9297 g/cc | 30 °C |
| Dead oil viscosity (EMV, atmospheric) | ~3,050 cP | 21.5 °C |
| Live oil saturation pressure | 500 psi | 21.5 °C |
| Live oil GOR | 9.7 m³/m³ | 500 psi, 21.5 °C |
| Live oil viscosity | ~1,700 cP | 500 psi, 21.5 °C |
| BSW | 1% | — |
| Molecular weight (dead oil) | 393 g/mol | — |
| C₃₀+ mole fraction | 0.3178 | — |
| C₃₀+ density | 0.9985 g/cc | — |

**Table B: Dead Oil Viscosity vs. Pressure at 21.5 °C (read from Figure 5)**
| Pressure (psi) | Viscosity (mPa·s) |
|---|---|
| 0 | 3,050 |
| 100 | 3,080 |
| 200 | 3,130 |
| 300 | 3,150 |
| 400 | 3,260 |
| 500 | 3,310 |

**Table C: Foamy Oil Viscosity vs. GVF — EMV (read from Figure 8)**
| GVF (%) | Viscosity (cP) | Notes |
|---|---|---|
| 0 | 1,700 | Live oil baseline at 500 psi |
| 10 | 1,700 | Stable, near live oil |
| 20 | 1,700 | Stable, near live oil |
| 30 | 1,700 | Stable, near live oil |
| 40 | 1,700 | Stable, near live oil |
| 55 | 2,300 | Rising — regime change |
| 60 | 2,300 | Rising |
| 75 | 2,500 | Rising |

**Table D: Foamy Oil Viscosity vs. GVF — Slim Tube (read from Figure 9)**
| GVF (%) | Viscosity (cP) | Notes |
|---|---|---|
| 20 | 1,850 | Near live oil |
| 30 | 1,750 | Near live oil |
| 40 | 1,730 | Near live oil |
| 45 | 1,720 | Near live oil |
| 55 | 2,200 | Rising, unstable above this |

**Table E: Foamy Oil Viscosity vs. GVF — Capillary Tube (read from Figure 4)**
| GVF (%) | Viscosity (cP) | Notes |
|---|---|---|
| 0 | 1,750 | Live oil at bubble point |
| 30 | 1,050 | Declining (gas segregation artifact) |
| 40 | 940 | Declining |
| 55 | 880 | Near floor |
| 65 | 855 | Floor value |
| 80 | 855 | Floor value |
| 88 | 855 | Floor value |

Note: capillary tube values are considered unreliable for dispersion viscosity by the authors — gas segregates in the large-diameter tube.

**Table F: Live and Foamy Oil Viscosity vs. Pressure During Depletion — EMV (read from Figure 7)**
| Pressure (psi) | Dead Oil (cP) | Live Oil (cP) | Foamy @ 10 cc/hr (cP) | Foamy @ 2 cc/hr (cP) |
|---|---|---|---|---|
| 100 | 3,100 | 2,800 | 2,900 | 2,700 |
| 200 | 3,110 | 2,460 | 2,370 | 2,330 |
| 300 | 3,120 | 2,130 | 2,100 | 2,100 |
| 400 | 3,130 | 1,790 | 1,770 | 1,760 |
| 500 | 3,310 | 1,700 | — | — |

---

### Implications for Separator Design

**The Stokes' Law Problem**

Stokes' law governs bubble rise velocity in a gravity separator:

```
v_rise = (2/9) × (ρ_liquid - ρ_gas) × g × R² / μ
```

The viscosity term μ is typically taken as **dead oil viscosity** in standard separator design. Alshmakhy & Maini (2010) show this assumption is wrong for foamy heavy oil systems in two distinct ways:

**Implication 1: Live oil viscosity, not dead oil viscosity, is the correct baseline**

At any pressure above the bubble point, the relevant viscosity is live oil viscosity, not dead oil. For the Alshmakhy & Maini oil at 500 psi:
- Dead oil viscosity: ~3,310 cP
- Live oil viscosity: ~1,700 cP
- **Ratio: dead/live = ~1.95x**

Using dead oil viscosity in Stokes' law underestimates bubble rise velocity by a factor of ~2 for this oil. Since bubble rise velocity is inversely proportional to μ, a designer using dead oil viscosity would predict bubbles rising at roughly half the actual rate — an overly pessimistic (conservative) separator sizing error. The separator would be oversized for bubble separation.

**Implication 2: Foamy oil viscosity tracks live oil viscosity across a wide GVF range**

Within the wellbore and in the separator inlet at GVF < 40–50%, the foamy oil viscosity is approximately equal to live oil viscosity (~1,700 cP for this oil), not to some higher dispersion viscosity. This is the key counterintuitive finding:

- Classical dispersion theory predicts viscosity **increases** above the continuous phase as GVF increases
- Alshmakhy & Maini (2010) find viscosity **stays constant** near live oil viscosity for GVF 0–40%
- Therefore, using Stokes' law with μ = live oil viscosity is a reasonable approximation across the low-to-moderate GVF range typical of producing wellbores

**Quantitative impact on bubble rise velocity:**

If the continuous phase viscosity is correctly taken as live oil (~1,700 cP) rather than dead oil (~3,050 cP at 21.5 °C or 2,700 cP at 30 °C), then:

- v_rise_correct / v_rise_dead_oil = μ_dead / μ_live = 3,050 / 1,700 ≈ **1.79x** (at 21.5 °C)
- Or using the 30 °C Anton-Paar value: 2,700 / 1,700 ≈ **1.59x**

Bubble rise velocity is approximately **1.6–1.8× faster** than dead oil viscosity calculations would predict for this class of heavy oil at GVF < 40%.

At GVF > 50%, viscosity rises above live oil (to ~2,300–2,500 cP per EMV), meaning bubble rise velocity slows relative to the live oil baseline but is still faster than dead oil predictions would suggest.

**Implication 3: Instrument selection matters — field application should use porous media analog**

The slim tube (sand-packed) viscometer is identified as the best choice for reservoir/wellbore engineering (Conclusion #6, p. 12). The EMV and slim tube agree at low GVF. The capillary tube systematically underestimates due to gas segregation — it produces values between live oil and dead oil viscosity, which could tempt an engineer toward an intermediate assumption that is also wrong.

**Limitations of applying this paper to Obsidian/Bluesky conditions:**
1. Single oil sample — composition differs from Bluesky bitumen (different asphaltene content, GOR, density)
2. Test temperature 21.5 °C — Bluesky reservoir is warmer (~35–45 °C), so absolute viscosities will be lower but the foamy/live oil ratio relationship should be qualitatively preserved
3. GOR of 9.7 m³/m³ at 500 psi — Bluesky solution GOR and saturation pressure differ; live oil viscosity reduction will scale differently
4. Methane only as dissolved gas — actual solution gas includes heavier components which dissolve differently
5. The paper notes EMV measurements may show gas fully separating from oil at low flow rates, meaning even the "foamy oil" measurements may be measuring near-equilibrium supersaturated oil rather than true dispersion

(Alshmakhy & Maini 2010, SPE-136665, p. 9, 11–12, Conclusions)

---

### Conclusions (verbatim from paper, p. 11–12)

1. The type of measuring device used has a significant effect on foamy oil viscosity measurements.
2. With live oil samples, viscosity was independent of flow rate (i.e. shear rate) with all three viscometers.
3. Viscosity of foamy oil, using Cambridge EMV and slim tube, was found to be similar to live oil viscosity for a large range of gas volume fractions.
4. The capillary viscometer results were different from the other two viscometers.
5. Measurements with the capillary tube viscometer show a decreasing viscosity trend as foam quality increases.
6. Slim tube appears to be the best option for measuring the apparent viscosity for reservoir engineering applications.

---

## Foamy-to-Free-Gas Transition Conditions

*Source papers: Maini 1999 (SPE-56541-MS) and Sheng, Hayes, Maini, Tortike 1999 (Transport in Porous Media 35: 157-187)*

---

### From Maini 1999 (SPE-56541)

#### Gas Disengagement from Oil: What Conditions Cause Bubbles to Separate from the Oil Phase

Maini's central argument is that foamy oil flow is **two-phase gas-oil flow at high capillary number**, in which dispersed flow is maintained by a dynamic balance between bubble break-up and coalescence. Gas remains dispersed as long as viscous mobilizing forces exceed capillary trapping forces. When this balance tips — i.e., when pressure gradient drops below a threshold — bubbles stop migrating and instead coalesce into a continuous gas phase, triggering disengagement.

The paper does not describe a wellbore-scale disengagement event directly. It frames disengagement as a reservoir-scale process that happens when the local pressure gradient falls below the critical value for ganglion mobilization. The calculated threshold is **approximately 25 kPa/m (≈1.0 psi/ft)** based on Chatzis and Morrow (1981) correlations, assuming 3,000 mD permeability and 25 mN/m interfacial tension (Maini 1999, SPE-56541, p. 5).

Key condition for maintaining dispersed flow — all three must hold simultaneously:
1. Viscous forces acting on growing bubbles must exceed capillary trapping forces.
2. Gravitational forces must not be sufficient to induce gravity segregation of the two phases.
3. Interfacial chemistry effects that hinder coalescence may also be needed.

When condition (2) is violated (i.e., buoyancy can overcome viscous drag), bubbles preferentially rise and coalesce. This is far more likely to occur in a **near-vertical wellbore** than in a near-horizontal reservoir pore network — a critical wellbore implication.

#### Pseudo-Bubble-Point Behavior: How Foamy Oil Differs from Conventional Oil at Bubble Point

Maini does not use the term "pseudo-bubble-point" in SPE-56541, but the behavior it describes is equivalent. In conventional solution gas drive, the bubble point is a sharp thermodynamic event at which gas phase becomes continuous and GOR rises sharply. In foamy solution gas drive:

- Gas nucleates and bubbles begin to migrate, but break-up of migrating bubbles maintains a **dispersed, discontinuous gas phase**.
- The producing GOR therefore remains low even though reservoir pressure has fallen well below the thermodynamic bubble point (Maini 1999, SPE-56541, p. 3).
- This means the "apparent" bubble point — the pressure at which GOR rises sharply at surface — is **artificially suppressed**. The oil arrives at surface still carrying entrained gas that has not yet disengaged.

The lab evidence for this: in fast depletion tests, even at 25% gas saturation, the gas mobility was so low that a substantial pressure gradient (~50 psi / 345 kPa) could be maintained over extended periods in a 200 cm sand-pack. This is only consistent with non-continuous (dispersed) gas (Maini 1999, SPE-56541, p. 3-4).

#### Role of Viscosity in Trapping Gas: At What Viscosity Range Does Gas Remain Dispersed

This is one of the most quantitatively useful sections of the paper:

> "When the depletion tests conducted with different oils were compared to evaluate the effect of oil viscosity, it was found that the depletion rate needed to obtain the high recovery factor became slower with increasing oil viscosity. With a **50,000 mPa.s oil**, high pressure gradients and high recovery factors could be obtained even in **seven days** decline test. On the other hand with a **200 mPa.s viscosity oil**, the depletion time had to be **shorter than a few hours** to obtain the high performance behaviour."
> (Maini 1999, SPE-56541, p. 4)

Interpretation: High viscosity mechanically impedes bubble coalescence and slows bubble rise by buoyancy. At 50,000 mPa.s (typical Clearwater/Bluesky in-situ bitumen), dispersed flow can persist for days under very low driving gradients. At 200 mPa.s (lighter heavy oil), the dispersed state is much more fragile — hours only.

Obsidian Energy context: Bluesky in-situ viscosity is in the 1,000–10,000 mPa.s range (Table 1 of SPE-56541 lists 1,000–100,000 mPa.s for cold production candidates). This places Bluesky firmly in the regime where dispersed flow should persist for many hours to days under reservoir conditions.

#### Timescales: How Long Do Bubbles Remain Trapped

The paper does not provide direct bubble lifetime data in porous media. However, it implies the timescale is set by the viscosity regime:
- 50,000 mPa.s oil: dispersed state persists for days even at very low flow rates (Maini 1999, SPE-56541, p. 4).
- 200 mPa.s oil: dispersed state collapses within hours.

The micro-model observations show that **coalescence is more likely when liquid velocity is low and bubbles remain in contact for a longer period** (Maini 1999, SPE-56541, p. 4, observation #8). This is directly relevant to the wellbore: as fluid velocity slows in a standing column above a stopped pump, coalescence conditions are met.

#### Lab Data on Coalescence Rates or Conditions

Micro-model observations yielded the following mechanistic conclusions (Maini 1999, SPE-56541, p. 4):
- Dispersed flow is generated not by explosive nucleation but by **bubble break-up** of a small number of mobilized bubbles (typically 5-20 nucleated bubbles → orders of magnitude more dispersed bubbles via break-up).
- Coalescence is **counteracted by high flow rates** (observation #10: bubble break-up likely at high flow rates).
- Coalescence is **promoted by low flow rates** (observation #8).
- High oil viscosity coupled with high flow velocity leads to dispersed flow (observation #11).
- Asphaltenes appeared to hinder coalescence (observation #9) — suggesting Bluesky oil with natural asphaltene content has better dispersion stability than lighter crudes.

No quantitative coalescence rate data (e.g., k_coalescence in s⁻¹) are reported in SPE-56541.

---

### From Sheng et al. 1999 (Transport in Porous Media 35: 157-187)

#### Comparison of Foamy Oil Models: Which Handle the Transition from Foamy to Conventional Flow

Sheng et al. review five modelling approaches, evaluating each for its ability to capture the foamy-to-free-gas transition:

**1. Conventional models (Section 6.1):** History match conventional simulators by adjusting critical gas saturation, relative permeability, compressibility, and permeability. Cannot capture dynamic dispersion generation or collapse. "Obviously, conventional models cannot be expected to capture important features of dispersed flow, especially the dynamic processes involved in generation and collapse of the dispersion." (Sheng et al. 1999, p. 180)

**2. Dispersed microbubble model — Smith (1988) (Section 6.2):** Assumes a pseudo-single-phase fluid with enhanced compressibility c_fo = κ/p, where κ ≈ 0.25–0.4 for Lloydminster oil. Treats gas fraction as independent of time and flow conditions — an acknowledged fault, since it cannot capture dispersion collapse. The postulation of large microbubble populations was not experimentally validated (Sheng et al. 1999, p. 180).

**3. Pseudo-bubble-point model — Kraus et al. (1993) (Section 6.3):** All solution gas remains dispersed until pressure drops to the "pseudo-bubble-point pressure" (an adjustable parameter). Below this pressure, dispersed fraction decreases linearly to zero. This is the only model that explicitly codes a **transition from foamy to conventional flow**. It uses conventional PVT data with enhanced compressibility for the dispersed phase. Limitation: does not simulate time-dependent or pressure-gradient-dependent changes — the transition is pressure-only, not kinetic (Sheng et al. 1999, p. 180).

**4. Modified fractional flow model — Lebel (1994) (Section 6.4):** Gas saturation below a limiting dispersed gas fraction flows with oil; above that limit, excess gas is free. Captures partial entrainment but not dynamic changes or pressure-gradient dependence (Sheng et al. 1999, p. 181).

**5. Dynamic flow models — Sheng et al. (1996, 1997) (Section 6.6):** Two rate processes: (i) transfer from solution gas to evolved (dispersed) gas, and (ii) transfer from dispersed gas to free gas. Both transfers modelled as kinetic rate processes. Disengagement of dispersed gas bubbles from oil is assumed to be **exponential decay**: u(t) = u(0)·e^(-λt), where λ is the decay coefficient (Sheng et al. 1999, p. 179, 182). This is the only model with an explicit kinetic rate for the foamy-to-free-gas transition. Limitation: model parameters vary with pressure decline rate, and the local pressure gradient plays no role — making field prediction unreliable (Sheng et al. 1999, p. 182).

**Critical finding from model comparison:** None of the existing models (as of 1999) can simultaneously capture (a) the kinetics of dispersion generation, (b) the role of local pressure gradient (not just pressure decline rate) in maintaining dispersion, and (c) the collapse of dispersion as conditions change. This remains an unresolved gap.

#### Foamy Oil Stability: Bulk Phase vs. Porous Media

This is among the most wellbore-relevant data in the paper:

> "gas bubbles remain dispersed in the oil for only a short time, **with the lifetime being of the order of tens of minutes**" (in bulk phase, outside porous media). (Sheng et al. 1999, p. 164)

However, the authors explicitly caution:

> "The foam stability measured in bulk phase (outside porous media) does not tell how fast the gas will separate from the oil within a porous medium. Our own tests in etched glass micromodels and sand-packs suggest that **such dispersions are considerably more stable in porous media**." (Sheng et al. 1999, p. 164)

This is a critical distinction for wellbore interpretation: once the foamy oil exits the pore network and enters the open bore of a wellbore (above perforations), the porous-media stabilizing constraint is removed. The dispersion lifetime measured in bulk (tens of minutes) becomes the operative timescale. At pump-intake velocities, this residence time budget determines how much gas arrives as dispersed bubbles vs. free gas.

Additional stability factors observed (Sheng et al. 1999, p. 163-164):
- Stability increases with higher oil viscosity.
- Stability increases with higher dissolved gas content.
- Stability increases with higher pressure decline rate.
- Foam quality (gas volume fraction) was very low — less than 20%.
- **Asphaltene content was not observed to increase stability significantly** in their bulk-phase tests (contradicting some earlier literature).

#### Bubble Disengagement: The Key Transition Mechanism

Section 5.4 of Sheng et al. (p. 179) addresses bubble disengagement directly:

> "The gas-in-oil dispersion, irrespective of how it is formed, is thermodynamically unstable. The dispersed gas bubbles eventually separate from the oil to form a free gas phase. This separation is controlled by the flow conditions and the surface chemistry of the system. A dynamic equilibrium between the break-up of bubbles and coalescence of interacting bubbles would be involved."

Factors that increase foam stability (slow disengagement), from the literature review:
- Higher liquid oil viscosity (Brady and Ross, 1944; McBain and Robinson, 1949; Callaghan and Neustadter, 1981; Sheng et al., 1995c). This is the strongest factor.
- Higher interfacial area per unit volume (finer bubble size).

The exponential decay model (Equation 8-9 in the paper) is the only quantitative kinetic formulation reviewed:

  du/dt = -λu

where u is a foam parameter (interfacial area, foam volume, or number of flowing bubbles) and λ is the decay coefficient. No numerical value for λ is provided for Bluesky or Clearwater-type crudes in the paper — it remains a fitting parameter dependent on fluid system, temperature, and pressure.

#### Pore-Scale vs. Pipe-Scale Behavior: Does the Mechanism Change at Wellbore Scale

The paper does not directly model or discuss pipe-scale wellbore flow. This is an explicit knowledge gap. However, the following statements have clear pipe-scale implications:

1. The local pore-scale capillary number is "the key consideration" for maintaining dispersed flow (Sheng et al. 1999, p. 178). In a wellbore pipe, there are no pore throats — capillary trapping is absent. The only mechanism maintaining dispersion is fluid inertia (viscosity × velocity preventing buoyant rise).

2. The dispersion is described as being generated by break-up of bubbles "in the shear field generated by high flow velocity" (Sheng et al. 1999, p. 182). In a wellbore, flow velocity depends on pump rate and tubing diameter. A running PCP at 190 bbl/d through 2-7/8" tubing generates substantial shear that will maintain break-up. A stopped pump or low RPM will allow coalescence.

3. Internal vs. external gas drive distinction (Section 3.7, p. 169): The authors note that in an internal gas drive process (solution gas nucleating in situ), "it is easier for the gas phase to become discontinuous in the internal process, as compared to the external process." This suggests that in the wellbore, where gas is arriving already partially nucleated from the reservoir, conditions for continuous gas formation are *more* favorable than in the reservoir.

#### Critical Review Findings: Biggest Gaps

From Section 7 Summary (Sheng et al. 1999, p. 183):

1. **Reservoir-scale existence unconfirmed:** "Although the occurrence of foamy oil flow has been verified in laboratory experiments, its existence at the reservoir scale has not been confirmed."

2. **Viscosity controversy:** "It is not even certain that the [foamy oil] viscosity is higher or lower than that of a single oil phase." This means apparent viscosity changes through the pump are unknown and may be non-monotonic.

3. **Pressure gradient vs. pressure decline rate:** "It appears that the pressure gradient (and not the pressure decline rate) is a more relevant parameter in controlling the generation of gas-in-oil dispersion." Field implications are large — what matters is the local gradient across the wellbore/near-wellbore zone, not the field-average depletion rate.

4. **Surface chemistry gap:** "The role of surface chemistry in controlling the in situ generation of gas-in-oil dispersion and its eventual collapse into segregated flow is another area that remains unexplored."

5. **Modelling inadequacy:** "An accurate modelling of the physics of foamy oil flow appears to be impossible to achieve with the existing knowledge base."

---

### Implications for Separator Placement

*Synthesized from both papers — wellbore-specific interpretation of reservoir-scale findings*

#### What the Papers Actually Say About the Wellbore

Neither paper directly addresses downhole separator design or wellbore-scale phase segregation. This is an **explicit knowledge gap** — both papers treat foamy oil as a reservoir phenomenon and stop their analysis at the wellbore face (perforations). The following implications are therefore inferences from first principles applied to the published physics.

#### The Phase State of Fluid Entering the Wellbore

Based on Maini 1999 and Sheng et al. 1999, the fluid arriving at the pump intake in a CHOPS/Bluesky well is likely to be:

- **Still partially dispersed (foamy)** if:
  - Drawdown across the perforation zone is high (>25 kPa/m in near-wellbore region).
  - Oil viscosity is high (>1,000 mPa.s in situ).
  - Pump is running and generating fluid velocity (maintaining shear break-up).
  - Residence time in the sump/below perforations is short (minutes, not hours).

- **Transitioning to free gas** if:
  - The pump has been stopped or slowed (low velocity, low shear — coalescence favored).
  - Fluid has been resident in an open wellbore column for tens of minutes or more (bulk-phase stability is "order of tens of minutes," Sheng et al. 1999, p. 164).
  - Temperature has increased (wellbore is warmer than reservoir in some cases, reducing viscosity and thus dispersion stability).
  - Gas saturation has exceeded the limiting dispersed fraction in the pseudo-bubble-point or fractional flow models.

#### Should a Downhole Separator Be Placed Above or Below the Transition Zone

The question is whether to intercept the fluid while gas is still dispersed (below the transition, harder to separate) or after it has coalesced into free gas (above the transition, easier to separate).

**Argument for placing the separator BELOW the natural transition zone (intercept dispersed flow):**

This would defeat the purpose. A downhole gas-liquid separator (DGLS) works by exploiting density difference between free gas and liquid. If gas is still dispersed as sub-pore-size bubbles, the density contrast is insufficient to drive gravitational separation at the residence times available downhole. The separator would pass dispersed gas upward with the liquid, providing no benefit.

**Argument for placing the separator ABOVE the natural transition zone (intercept free gas after coalescence):**

Once bubbles have coalesced into continuous free gas, the gas-liquid density contrast (~800 kg/m³) drives rapid gravitational separation. This is what conventional annular DGLS designs exploit. The practical question is: where in the wellbore does this transition occur?

**Estimating the transition depth:**

Using the bulk-phase stability data from Sheng et al. (1999, p. 164) — lifetime on the order of tens of minutes — and a typical upflow velocity in a 5" casing annulus at 190 bbl/d production:

  Flow rate: 190 bbl/d = 0.00035 m³/s
  Annular cross-section (8-5/8" casing, 2-7/8" tubing): ~0.030 m²
  Upflow velocity: ~0.012 m/s = 0.72 m/min

At this velocity, fluid travels ~7–14 m in 10–20 minutes. This suggests the foamy-to-free-gas transition would largely complete **within 10–15 m above the pump intake** under normal pumping conditions.

**However**, this calculation assumes the bulk-phase stability timescale applies. Sheng et al. explicitly warn that stability is considerably greater in porous media — and the sub-perforation sump (unperforated casing section, 10–20 m deep) represents a transition zone between porous-media-stabilized flow and open-bore-destabilized flow. The effective transition is likely to be **in or immediately above the sump**, and complete within the first 20–30 m of the tubing string above the pump.

**Practical placement recommendation (inference from the physics):**

Place the downhole separator at or slightly above the perforations/pump intake — i.e., within the sump zone or at the base of the producing interval. The goal is to allow the brief (tens-of-minutes) natural coalescence to occur in the sump while the fluid is still moving slowly, then separate before the combined gas-liquid mixture accelerates up the tubing. Placing a separator at mid-tubing depth would miss the early coalescence window and encounter an already-mixed column.

**Counterargument — preserve foamy oil production benefit:**

Maini (1999) and Sheng et al. (1999) both emphasize that maintaining the dispersed state in the reservoir is what produces the anomalously high recovery factors. Any mechanical disruption at the wellbore that promotes coalescence (e.g., turbulence from perforation chokes, pump shear) could theoretically destroy the near-wellbore dispersed flow and reduce inflow performance. A downhole separator that actively promotes early gas separation might increase the near-wellbore gas mobility, reducing foamy oil benefit. This is speculative but physically grounded — neither paper discusses the feedback effect of wellbore gas management on near-wellbore foamy flow continuity.

---

### Key Quantitative Data Points for Engineering Use

| Parameter | Value | Source |
|---|---|---|
| Critical pressure gradient for ganglion mobilization (3,000 mD, σ=25 mN/m) | ~25 kPa/m (~1.0 psi/ft) | Maini 1999, p. 5 |
| Foamy dispersion lifetime in bulk phase (outside porous media) | Order of tens of minutes | Sheng et al. 1999, p. 164 |
| Foamy dispersion stability in porous media | Considerably longer than bulk | Sheng et al. 1999, p. 164 |
| Viscosity range for cold production (in-situ) | 1,000–100,000 mPa.s | Maini 1999, Table 1 |
| Oil at 200 mPa.s: foamy flow requires depletion time | Shorter than a few hours | Maini 1999, p. 4 |
| Oil at 50,000 mPa.s: foamy flow maintained even in | Seven-day decline tests | Maini 1999, p. 4 |
| Foam quality (gas volume fraction) | Less than 20% | Sheng et al. 1999, p. 164 |
| Lloydminster oil compressibility coefficient κ | 0.25–0.4 | Sheng et al. 1999, p. 161 |
| Kinetic disengagement model form | u(t) = u(0)·e^(-λt) | Sheng et al. 1999, p. 179 |
| Numerical value of λ for Bluesky/Clearwater crudes | Not reported — fitting parameter | Sheng et al. 1999, p. 182 |

---

### Explicit Knowledge Gaps (Both Papers Combined)

1. **No wellbore-scale data or models exist in either paper.** Both papers treat the wellbore as a boundary condition, not as a flow domain. The transition from porous-media-stabilized dispersed flow to open-bore-destabilized free gas is not modeled by anyone reviewed.

2. **No quantitative coalescence rate (λ) for Bluesky or Clearwater crude.** The exponential decay model exists but the rate constant is purely empirical and has not been measured for Alberta Bluesky or Clearwater crudes at in-situ conditions.

3. **Temperature effects on the transition are not addressed.** Both papers are isothermal or near-isothermal. Wellbore temperature gradients (reservoir temperature at bottom, lower temperature uphole) will affect both viscosity (and thus dispersion stability) and gas solubility in unpredictable ways.

4. **Shear environment of a PCP is not addressed.** A progressive cavity pump creates a specific shear history for the fluids passing through it. Whether PCP shear promotes break-up (maintaining dispersed flow) or promotes coalescence (by repeated bubble-wall collisions) is not discussed.

5. **Feedback of wellbore gas management on near-wellbore foamy flow is unknown.** If a DGLS captures free gas at the pump, does this change the near-wellbore pressure gradient enough to affect foamy flow generation? Neither paper provides a basis for answering this.

## Updated Source Papers (Section 8 additions)

| SPE # | Title | Authors | Year |
|---|---|---|---|
| SPE-136665 | Viscosity of Foamy Oils | Alshmakhy, Maini (U of Calgary/Weatherford) | 2010 |
| SPE-56541 | Foamy Oil Flow in Primary Production | Maini (U of Alberta) | 1999 |
| Sheng et al. 1999 | Critical Review of Foamy Oil Flow | Sheng, Hayes, Maini, Tortike | 1999 |
