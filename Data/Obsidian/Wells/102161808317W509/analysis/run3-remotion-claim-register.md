# Run 3 Remotion Claim Register

## Scope

- Well: `102161808317W509`
- Customer: Obsidian Energy
- Video path: `analysis/remotion-video/src/run3/`
- Composition ID: `DeploymentStoryRun3`
- Run window presented: April 2 to April 3, 2026

## Source Manifest

- Approved storyboard:
  - `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\wellfi-run3-deployment-story.png`
- Storyboard generator:
  - `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\plot_run3_story.py`
- Narrative docs:
  - `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\run3-complete-timeline.md`
  - `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\run3-narrative.md`
- Visual direction:
  - `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\design-philosophy.md`
- Telemetry interpretation:
  - `C:\Users\kyle\MPS\Obsidian\petro-roundtable\knowledge\wellfi-telemetry.md`
- Raw packet evidence for late Apr 3 tail:
  - `G:\My Drive\Belle Industries\WellFi\Obsidian\102161808317W509\Logs\packetmessages_April2_2026.txt`

## Scene Claims

| Scene | Claim | Status | Evidence | Validation owner |
|------|-------|--------|----------|------------------|
| Intro | Run 3 can be told as an evidence-backed operations story | marketing framing | storyboard + source manifest | roundtable / operator review |
| Depth | Peak signal reached `-37 dBV` at about `161 m MD` | proven | storyboard + `run3-narrative.md` section 1 | production-data |
| Depth | Fluid contact occurred at `1.20 BAR` near `482 m MD` | proven | storyboard + `run3-narrative.md` section 1 | production-data |
| Depth | On bottom the link was below the `-95 dBV` noise floor | proven | storyboard + `run3-narrative.md` section 1 | production-data |
| Recovery | Pulling 1 joint ended an `84-minute blackout` | proven | `run3-narrative.md` section 3 | production-data |
| Recovery | On-lease stake position was worse than the off-lease stake | proven | `run3-complete-timeline.md` phase 3 | production-data |
| Recovery | Apr 3 monitoring reached `94-100% CRC` windows | proven | `run3-complete-timeline.md` sections 10-12 | production-data |
| Pump | Steady-state pressure window averaged `2069 kPa` | proven | `plot_run3_story.py` from clean packets | production-data |
| Pump | Morning Apr 3 operating window averaged `1928 kPa` | proven | `plot_run3_story.py` from clean packets | production-data |
| Pump | Late Apr 3 clean packet tail reached `1810 kPa` and was still declining | proven | raw packet at `2026-04-03 16:29:36` + storyboard generator | production-data |
| Pump | Pump start is visible in the temperature change from `24.8 C` toward the `21.6 C` band | inferred | timeline + narrative + storyboard | well-performance |
| Gas kick | Pressure at sensor depth mostly stayed in the `19.1-19.4 BAR` band | proven | `run3-narrative.md` gas-kick table | production-data |
| Gas kick | `168.65 BAR` at `11:52` was corrupted, not real pressure | proven | CRC fail + RMS 78% + recovery at `11:59` | production-data |
| Payoff | Run 3 moved from marginal telemetry to a believable operations story | marketing framing | all of the above | obsidian-energy |

## Conflict List

1. Late Apr 3 endpoint conflict
   - `run3-complete-timeline.md` and part of `run3-narrative.md` stop at `2026-04-03 14:50:34` with `18.46 BAR`.
   - `run3-narrative.md` summary table later says `2026-04-03 16:29 / 18.10 BAR`.
   - The approved storyboard image shows `1810 kPa` as the last pressure callout.
   - `plot_run3_story.py` computes that last callout from the raw clean packet tail.
   - Decision for animation: use `18.10 BAR / 1810 kPa` for the late tail because it is backed by the raw packet source and the approved storyboard visual.

2. Drawdown summary conflict
   - `2.33 BAR` is true through the `14:50` narrative cutoff.
   - The raw clean packet tail continues lower to `18.10 BAR`.
   - Decision for animation: avoid a headline claim on total drawdown and instead show the late pressure value directly.

## Beat Map

- Highest visual emphasis:
  - Peak signal
  - Pulling 1 joint after blackout
  - Pump story from pressure and temperature
  - CRC-failed gas-kick packet and recovery
- Moderate emphasis:
  - Fluid contact
  - On-bottom noise floor
  - Cable/stake tuning and CRC improvement
- Low emphasis:
  - Source manifest and validation framing

## Marketing Video Enhancement (2026-04-09)

Primary composition upgraded from dashboard slides to animated marketing video:
- `evolvePath` progressive trace drawing on all 4 SVG charts (depth, pressure, temperature, gas kick)
- `GlowBurst` radial emphasis at 4 hero moments (peak signal, pulled joint, last pressure, CRC fail + recovery)
- `NumberCounter` count-up animation on key MetricCards
- Callout temporal separation (spring in / fade out per act)
- Crimson edge flash at CRC fail moment
- Duration extended from 1200 to 1500 frames (50s)
- Short composition added: `DeploymentStoryRun3Short` (900 frames, 30s, 4 scenes)

All visual enhancements use timing and motion — no new claims were added to the story.

### Verification Pass (2026-04-09)

- [x] All dates/times match approved run window (Apr 2-3, 2026)
- [x] All unit conversions correct (BAR to kPa: x100)
- [x] Depth references use correct MD values from run3-narrative.md
- [x] Pressure callouts match: 2069, 1928, 1810 kPa
- [x] Gas kick values match: 19.1-19.4 BAR band, 168.65 BAR corrupted
- [x] No claims added that aren't in this register
- [x] Still frames rendered and visually compared at 4 hero moments
- [x] Marketing copy reviewed — all statements defensible against engineering evidence

## Validation Note

This animation is safe to iterate as a customer-facing marketing story if the final render stays inside this claim register and does not reintroduce the `14:50 vs 16:29` conflict as a casual single-number statement.
