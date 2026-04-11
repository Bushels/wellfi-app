# WellFi Telemetry Interpretation — Knowledge Base

> Curated from OBE 102 HZ field data (Run 3, April 2026), Gemini diagnostic analysis, and SPE paper insights on downhole monitoring. All field data from EMGRx SN 2602315 event log.

## Quick Reference Table

| Property | Value | Source |
|---|---|---|
| Sensor Type | Wireless EM pressure + temperature | WellFi spec |
| Measurement Interval (first 48 hrs) | 3 minutes (when locked) | WellFi spec |
| Measurement Interval (after 48 hrs) | 6 hours | WellFi spec — battery conservation mode |
| Receiver Gain Range | 0-32,767 (max = weak but decodable) | OBE Run 3 field data |
| Pressure Type | Absolute (BAR absolute) | WellFi spec |
| Pressure Resolution | ~0.01 BAR | OBE Run 3 field data |
| Temperature Resolution | ~0.8 degC | OBE Run 3 field data |
| Communication | EM signal through conductive casing | WellFi spec |
| Signal Attenuation | Exponential with distance to casing boundary | EM telemetry physics |
| Activation | Pressure threshold (configurable, 0 kPa = immediate) | OBE Run 3 config |

## 1. Diagnostic Signatures

Seven key signatures for automated well monitoring. Each signature describes the physics, the observable pattern in WellFi P/T data, and the recommended agent response.

### Signature 1: Normal Baseline

**Pattern:** Stable P within +/-1-2% of mean, stable T at or slightly above reservoir temperature.
**Physics:** Pump running at steady speed, fluid influx balanced with displacement, thermal equilibrium reached.
**Long-term trend:** Very slow linear P decline over weeks/months = gradual reservoir depletion.
**T note:** Temperature typically 2-3 degC above reservoir temp due to viscous pump heating in heavy oil (8,320 cP).
**Field reference:** OBE Run 3 steady state: P=20.7 BAR +/-0.3, T=24.3 degC (reservoir is 21.5 degC). (EMGRx SN 2602315)

### Signature 2: Pump ON/OFF Cycle

**Startup pattern:**
- Sharp non-linear P drop over 5-15 minutes, stabilizing at flowing BHP (FBHP)
- T ramp of 2-5 degC over 30-60 minutes as warm reservoir fluid displaces cold standing fluid

**Shutdown pattern:**
- Sharp P rise (build-up curve) asymptotically approaching static reservoir pressure
- T exponential decay toward geothermal gradient as heat source (pump friction) is removed

**Field reference — Cold start (April 2, 2026):**
- 11:29 AM: P=-0.5 kPa, T=3.2 degC (Alberta April ambient, pump off overnight)
- 11:56 AM: P=1.2 kPa, T=12.0 degC (pump started, warm fluid arriving)
- 12:29 PM: P=20.7 BAR, T=24.8 degC (steady state reached in 60 min)

**Field reference — Warm restart (April 3, 2026):**
- 11:02 AM: P=19.3 BAR, T=21.6 degC from first reading (no cold ramp — wellbore retained heat)

**Diagnostic value:** Shape of the P build-up curve contains reservoir information (permeability, skin). The T ramp rate indicates fluid velocity past the sensor. Absence of a cold ramp on restart means wellbore insulation is effective.

### Signature 3: Pump Stall / Tag

**Pattern:** Immediate, near-instantaneous P spike toward static column pressure PLUS T spike >10 degC in <10 minutes.
**Physics:** Rotor seizes against stator (sand, debris, thermal expansion). Fluid movement stops abruptly. Intense localized friction from mechanical seizure generates rapid heat.
**Key differentiator:** Standard shutdown shows P rise but T DECREASE. Stall shows both P AND T rise simultaneously and rapidly.
**Agent rule:** IF (dP/dt > 5 kPa/min) AND (dT/dt > 1 degC/min) THEN pump_stall BECAUSE mechanical seizure.

### Signature 4: Gas Interference / Gas Lock

**Pattern:** Erratic, high-frequency, "spiky" P readings with high variance. Average flowing P may drift upward as pump loses displacement efficiency.
**Physics:** BHP drops below bubble point (~3,100 kPa for Bluesky), dissolved gas breaks out. PCP, designed for incompressible liquid, loses efficiency as it fills with compressible gas.
**T note:** Slight cooling possible from gas expansion (Joule-Thomson effect), but may be masked by chaotic heating from inefficient pump operation.
**Key differentiator:** High-variance CHAOTIC noise, not periodic. Distinct from the regular sawtooth of pump starvation.
**Field reference:** OBE Run 3 April 3, 11:52 AM — CRC error spike to 168.6 BAR during suspected gas event. Recovered to normal (19.3 kPa) within 7 minutes. CRC errors also increased during this period, suggesting gas disrupted the EM signal path. (EMGRx SN 2602315)

### Signature 5: Pump Starvation (Fluid Pounding)

**Pattern:** Deep periodic P drops followed by sharp recovery = **sawtooth pattern**. Frequency relates to time for fluid slug to accumulate at intake.
**Physics:** Q_pump exceeds reservoir inflow rate (IPR). Fluid level drawn down to pump intake. Pump runs partially empty, then catches fluid slug.
**Agent rule:** IF P shows periodic drops >5 kPa with regular interval THEN pump_starvation BECAUSE Q_pump > IPR. Recommend reducing pump speed.

### Signature 6: Gradual Pump Wear

**Pattern:** Long-term trend (weeks/months) — for given pump speed, FBHP gradually increases (less drawdown achieved). Baseline T gradually increases.
**Physics:** Stator elastomer wears, increasing internal "slippage" (fluid leaking from high to low pressure stages). Slippage is inefficiency that converts mechanical energy to heat.
**Agent rule:** IF P increasing >0.5 kPa/month at constant RPM AND T increasing >0.5 degC/month THEN pump_wear BECAUSE elastomer degradation. Plan workover.
**OBE context:** $49,000 per pump change. Proactive scheduling from WellFi wear detection avoids emergency pulls.

### Signature 7: Water Influx (Changing Fluid Properties)

**Pattern:** Rising P + falling T.
**Physics:** Increasing water cut lowers bulk fluid viscosity. Lower viscosity = (a) less frictional heating at pump (T drops), (b) less tubing friction losses (P at sensor rises because less drawdown is consumed by friction).
**Key differentiator:** Counter-intuitive — rising P normally suggests less drawdown or pump wear, but combined with FALLING T, the cause is viscosity reduction from water, not pump degradation.
**Agent rule:** IF P rising AND T falling at same rate THEN water_influx BECAUSE lower viscosity reduces both friction heat and tubing losses.

## 2. Foamy Oil Detection via WellFi

Combines insights from SPE-175390, SPE-174431, and OBE Run 3 field data.

| Observable | Interpretation | Physics | Source |
|---|---|---|---|
| P declining >0.5 kPa/day without pump speed change | Gas replacing liquid in annulus | Lower fluid density from dispersed gas bubbles | SPE-174431 |
| Overnight P drop >1 kPa when pump off | Gas accumulation/segregation | Buoyant gas migrates upward, reduces column weight | OBE Run 3 |
| Rising GOR correlation over months | Foamy oil transition in progress | Pressure below pseudo-bubble-point, gas breakout | SPE-175390 |
| Periodic P oscillations (not sawtooth) | Gas rate geysering | Gas evolution limited by local pressure recovery | SPE-174431 |
| CRC error rate increase | EM signal disruption by gas | Gas bubbles change fluid conductivity in annulus | OBE Run 3 |
| P decline rate accelerating | Foamy drive strengthening | Nucleation is 4th-order to supersaturation | SPE-174431 |

**OBE field evidence:**
- GOR rose from 66 to 477 scf/bbl over 10 months (30x above Bluesky solution GOR of 5-15 scf/bbl)
- Run 3 pressure: 20.7 BAR (Apr 2 PM) -> 19.3 BAR (Apr 3 AM) -> 18.4 BAR (Apr 3 PM) = -2.3 BAR over 2 days
- Overnight drop of -1.4 BAR — pump drawdown + possible gas segregation in annulus

## 3. Hydrostatic Head in Deviated Wells

### Formula

P_hydrostatic = SG * 9.81 * TVD_head (kPa)

Where TVD_head = TVD_sensor - TVD_fluid_level

**CRITICAL:** In deviated wells, MD and TVD are NOT proportional. Each joint's contribution to hydrostatic head depends on the inclination WHERE the fluid level sits in the build curve.

| Inclination | cos(inc) | TVD per 9.456m joint |
|---|---|---|
| 60 deg | 0.500 | 4.73m |
| 70 deg | 0.342 | 3.23m |
| 80 deg | 0.174 | 1.64m |
| 86 deg | 0.070 | 0.66m |
| 90 deg | 0.000 | 0.00m |

### OBE 102 HZ Reference (SG=1.01, joint=9.456m, port at 819.9m MD / 663.1m TVD)

| Joints Above Tag Bar | Fluid Level MD | Inclination | TVD Head | Liquid P (BAR) | Liquid P (kPa) |
|---|---|---|---|---|---|
| 4 (OBE min target) | 780.6m | 81 deg | 3.9m | 0.38 | 38 |
| 5 | 771.1m | 79 deg | 5.5m | 0.54 | 54 |
| 6 | 761.7m | 77 deg | 7.4m | 0.73 | 73 |
| 7 | 752.2m | 75 deg | 9.7m | 0.96 | 96 |
| 8 | 742.8m | 73 deg | 12.2m | 1.21 | 121 |
| 9 | 733.3m | 72 deg | 15.0m | 1.48 | 148 |
| 10 | 723.9m | 70 deg | 18.1m | 1.79 | 179 |
| 11 (OBE max target) | 714.4m | 69 deg | 21.4m | 2.12 | 212 |

**OBE annulus is ALWAYS OPEN to atmosphere** (gas routed to flare stack, tubing to tanks).
This means WellFi reads PURE liquid hydrostatic — no casing gas component.
The raw sensor has a -0.49 BAR offset (reads -0.49 in air). Corrected gauge = raw + 0.49.

At 4 joints submergence, the corrected reading would be 0.38 BAR (raw display: -0.11 BAR).
At 11 joints, corrected 2.12 BAR (raw display: 1.63 BAR).

**OBE Run 3 readings:** 18-21 BAR raw (18.5-21.3 BAR corrected) = 188-215m TVD of liquid column.
The fluid level is at ~449-476m TVD — a FULL column, hundreds of joints above the tag bar.
The pump ran only 12 hours; it would take weeks/months to draw down to the 4-11 joint operating range.
The 2.69 BAR decline over 12 hours = 27m TVD of fluid level drop (early-phase drawdown).

## 4. Signal Quality Interpretation

| Event Type | Meaning | Action |
|---|---|---|
| PayloadRecoveredEvent (CRC=00) | Clean data — use for analysis | Include in trend |
| PayloadRecoveredEvent (CRC=01) | Data corruption — values unreliable | EXCLUDE from trend analysis |
| PotentialSyncLostEvent (sig_err >50%) | Marginal link — tool transmitting but receiver struggling | Monitor — may indicate gas or position issue |
| RecoverPayloadLost | Signal detected but payload incomplete | Normal for marginal link |
| PowerUp | Receiver restarted | Check for data gap |
| Gain at 32,767 | Maximum amplification — signal is weak | System is compensating successfully |

**Signal improves with:**
- Shallower tool position (shorter EM path to surface antenna)
- Greater distance from casing shoe (less signal leakage into formation)
- Higher fluid conductivity (better EM transmission medium)
- Absence of gas in annulus (gas reduces EM path conductivity)

## 5. Field Reference — OBE 102 HZ Run 3

**Well:** OBE 102 HZ Cadotte 16-18-83-17W5 (102/16-18-083-17W5/09)
**Receiver:** EMGRx SN 2602315
**Dates:** April 1-4, 2026 (3-min data); receiver alive to April 9+
**Position:** 819.9m MD, 663.1m TVD, 86.3 deg (pulled 1 joint from 829.4m original)

### Data Summary

| Phase | Date/Time | P (BAR) | T (degC) | Notes |
|---|---|---|---|---|
| First data | Apr 1, 18:52 | 3.15 | 14.4 | Tool just landed |
| Cold start | Apr 2, 11:29 | -0.49 | 3.2 | Pump off overnight, ambient |
| Hit fluid (RIH) | Apr 2, 11:55 | 1.20 | 12.0 | Pressure jumps at fluid contact |
| Steady state | Apr 2, 12:29+ | 20.7 avg | 24.3 avg | 22 clean readings |
| Morning resume | Apr 3, 11:02 | 19.34 | 21.6 | 1.4 BAR overnight drop |
| Gas kick event | Apr 3, 11:52 | 168.65 (CRC) | 114.4 (CRC) | EM disruption, garbled |
| Post-kick | Apr 3, 11:59 | 19.34 | 21.6 | Recovered in 7 min |
| Final reading | Apr 3, 16:29 | 18.10 | 20.8 | Continued decline |

**Totals:** 80 clean payloads + 22 CRC errors over ~44 hours (from packet messages)
**Pressure unit:** BAR (as labeled in packet messages). Multiply by 100 for kPa.

### Key Observations

1. **Cold start ramp** (Apr 2): Beautiful 60-min P/T ramp from ambient to reservoir conditions — textbook Signature #2
2. **No cold ramp on Apr 3:** Wellbore retained heat overnight — T started at 21.6 degC, not 3.2 degC
3. **Declining pressure trend:** 20.7 -> 19.3 -> 18.4 BAR over 2 days — pump drawdown + possible gas accumulation
4. **Gas kick CRC event:** 168.6 BAR / 114.4 degC are garbled values (T physically impossible), but the EM disruption is significant
5. **Cannot determine JOF from WellFi alone:** 18-21 BAR total reading includes casing gas + liquid column. Need casing head pressure to isolate submergence.

## 6. Agent Decision Rules

Format: IF [condition] THEN [interpretation] BECAUSE [physics]

| # | Condition | Interpretation | Physics |
|---|---|---|---|
| 1 | P declining >0.5 BAR/day AND GOR rising | Foamy oil transition likely | Gas breakout reduces fluid density |
| 2 | P shows periodic sawtooth (drops >0.5 BAR) | Pump starvation | Q_pump exceeds reservoir IPR |
| 3 | P stable BUT T rising >1 degC/month | Pump wear progressing | Elastomer slippage generates heat |
| 4 | P spike >3x baseline with CRC error | EM signal disruption (not real P) | Gas slug changes fluid conductivity |
| 5 | Cold start T ramp <30 min to reservoir T | High fluid velocity past sensor | Pump displacing standing fluid quickly |
| 6 | Overnight P drop >2 kPa | Gas segregation in annulus | Buoyant gas migrates upward when pump off |
| 7 | P declining >1 BAR/day during pumping | Accelerated drawdown warning | Pump may be drawing fluid level too low — verify with casing head pressure |
| 8 | P rise + T drop simultaneously | Water cut increasing | Lower viscosity reduces friction heat |
| 9 | dP/dt >5 kPa/min AND dT/dt >1 degC/min | Pump stall / mechanical seizure | Rotor seized, intense friction |
| 10 | High-variance chaotic P noise (not periodic) | Gas interference / gas lock | Free gas in pump reduces efficiency |

## 11. Extended Monitoring — Apr 3 PM to Apr 9 (from Apr 9 event log export)

**Data window:** Apr 3 15:11 to Apr 4 0:32 (3-min clean packets), then 6-hour sync attempts through Apr 9.

| Phase | Timespan | P range (BAR) | T (degC) | Packets | Note |
|---|---|---|---|---|---|
| Late Apr 3 PM | 15:11-16:50 | 18.09-18.35 | 20.8 | 13 clean | Continued drawdown, P bottoming |
| Apr 3 evening ramp | 17:02-19:14 | 18.10-18.73 | 20.8-21.6 | 38 clean | P begins RISING — well re-equilibrating |
| Apr 3 late evening | 20:08-23:59 | 18.84-19.85 | 21.6-23.2 | 62 clean | Steady P recovery to ~1955 kPa |
| Apr 4 early AM | 0:02-0:32 | 19.52-19.64 | 23.2 | 11 clean | Last 3-min window, P stable |
| Apr 4 0:32 | - | 19.64 | 23.2 | CRC fail | Last decode attempt; 48-hr battery switch imminent |
| Apr 4-9 | every 6 hrs | - | - | PotentialSyncLost | Tool transmitting, signal too weak for decode |

**Key findings:**
1. The pressure RECOVERED after the gas kick — it was not a monotonic decline. The well reached a new equilibrium at ~1955 kPa by midnight.
2. Temperature rose from 20.8 to 23.2 degC through the evening — consistent with the pump running and viscous heating stabilizing.
3. The tool transitioned to 6-hour intervals after 48 hours (battery conservation) and continued transmitting PotentialSyncLost events through Apr 9 — the tool is STILL ALIVE 8+ days post-deployment.
4. Total clean packets: 102 (Apr 2-3 3-min window) + ~120 (Apr 3 PM-Apr 4 0:32) = ~222 clean payloads from the pulled position.

**Source:** EMGRx SN 2602315 EventLog CSV exported 2026-04-09 21:04:13, from `G:\My Drive\Belle Industries\WellFi\Obsidian\102161808317W509\Logs\`

## Source Data

| Source | Description |
|---|---|
| EMGRx SN 2602315 | OBE 102 HZ Run 3 event log, April 1-9, 2026 (extended export) |
| SPE-175390 | Foamy oil dynamics, Shell Cliffdale (2015) |
| SPE-174431 | Foamy oil kinetic model, Shen (2015) |
| Gemini 3.1 Pro | Diagnostic signature framework (April 2026 session) |
| BHP test 26021001 | Adjacent well P/T data, SG=1.01 confirmation |
| Directional survey DS_0517936 | Trajectory for hydrostatic calculations |
