# Run 3 Marketing Video Enhancement — Design Document

**Date:** 2026-04-09
**Well:** OBE 102 HZ 16-18-83-17W5 (102/16-18-083-17W5/09)
**Customer:** Obsidian Energy
**Run window:** April 2 to April 3, 2026
**Approach:** Enhance in-place (Approach A: Progressive Trace + Glow Burst)

## Deliverables

1. **Primary video:** 50s MP4 at 1920x1080 30fps (1500 frames, 6 scenes)
2. **Trimmed video:** 30s MP4 at 1920x1080 30fps (900 frames, 4 scenes)
3. **Still frames:** PNG at each hero moment for Slack/email

## Existing Assets (Preserved)

- `run3Data.ts` — Claim-register-locked data module (259 lines)
- `Run3Storyboard.tsx` — 6-scene composition (1170 lines, to be enhanced)
- `run3-remotion-claim-register.md` — Evidence gate for all on-screen claims
- `wellfi-run3-deployment-story.png` — Approved storyboard visual reference
- `run3-narrative.md` — Complete field narrative (230 lines)
- `design-philosophy.md` — Subterranean Signal visual language

## 1. Animation System — Progressive Trace Drawing

Every SVG chart uses `evolvePath` from `@remotion/paths`. The trace draws itself
over the scene's frame window, with data points (circles) appearing only when the
trace reaches them.

| Scene | Trace | Draw window (frames) | Easing |
|---|---|---|---|
| Depth | Signal vs depth polyline | 120-360 | `Easing.out(quad)` |
| Pump | Pressure line | 600-860 | `Easing.out(quad)` |
| Pump | Temperature line | 620-860 (20-frame delay) | `Easing.out(quad)` |
| Gas Kick | Good-points polyline | 900-1100 | `Easing.out(quad)` |

Implementation: convert each polyline to an SVG `<path>` with
`evolvePath(progress, pathD)` producing `strokeDasharray` + `strokeDashoffset`.
The existing 3-layer glow (fat dim + medium + sharp bright) is preserved on all
traces.

The depth chart trace draws downward (tool descending). Pump traces draw
left-to-right across compressed time. Gas kick draws left-to-right within the
zoomed 11:02-11:59 window.

## 2. Hero Moment Glow Bursts (4 beats)

Each hero beat gets a 3-part pop effect timed to when the trace reaches that
data point:

1. **Glow burst:** Radial gradient circle scales 0 -> 2.5r -> 1.2r over 18 frames
   using `spring({ damping: 12, mass: 0.6 })`. Color = scene accent at 40% opacity.
2. **Drawing pause:** Trace progress holds constant for 12 frames (0.4s) at the
   hero point, giving the eye time to lock on.
3. **Metric card bounce:** The corresponding MetricCard scales 1.0 -> 1.08 -> 1.0
   with a spring over 15 frames.

| Hero | Scene | Data point | Glow color | Metric card |
|---|---|---|---|---|
| Peak signal | Depth | -37 dBV at 161m | green | Peak signal: -37 dBV |
| Pulled 1 joint | Interventions | 84-min blackout ended | amber | Blackout ended: 84 min |
| Gas kick + recovery | Gas Kick | CRC fail 11:52 + recovery 11:59 | crimson -> green | Recovery: 11:59 clean |
| Still declining | Pump | 1810 kPa last packet | cyan | Late Apr 3: 1810 kPa |

The gas kick beat is unique: glow starts crimson (CRC fail), then a second smaller
green burst appears 15 frames later when the trace reaches the recovery point.

## 3. Number Counter Animation

All MetricCard components get an interpolated counter using
`interpolate(localFrame, [delay, delay+18], [0, targetValue])` with
`fontVariantNumeric: "tabular-nums"` to prevent layout jitter.

Special cases:
- Pressure values (1810, 2069, 1928): count from nearest round hundred
- dBV values: count from 0 toward negative
- Percentage values: count from 0%
- Duration values (84 min, 7 min): count from 0

## 4. Callout Temporal Separation

Each AnnotationBox and data label gets an `appearFrame` and `disappearFrame`.

- Spring in at `appearFrame` (same spring config as scene enter)
- Fade out at `disappearFrame` over 12 frames
- At most 2 callouts visible simultaneously per scene
- Hero-beat callouts appear AFTER the glow burst settles (6-frame delay)

## 5. Gas Kick Crimson Edge Flash

At the CRC fail marker (frame ~960), a subtle full-screen crimson vignette:
- Opacity: 0 -> 0.08 -> 0 over 12 frames
- Implemented as AbsoluteFill with radial-gradient(transparent 60%, crimson 100%)
- Brief enough to feel like an alert, not a strobe

## 6. Scene Timing

### Primary (50s, 1500 frames at 30fps)

| Scene | Frames | Duration | Hero beat |
|---|---|---|---|
| Intro | 0-120 | 4.0s | - |
| Depth | 120-390 | 9.0s | Peak signal |
| Interventions | 390-600 | 7.0s | Pulled 1 joint |
| Pump | 600-900 | 10.0s | Still declining |
| Gas Kick | 900-1200 | 10.0s | Gas kick + recovery |
| Payoff | 1200-1500 | 10.0s | - |

### Trimmed (30s, 900 frames at 30fps)

| Scene | Frames | Duration | Notes |
|---|---|---|---|
| Intro | 0-90 | 3.0s | Condensed hero stats |
| Depth + Pull | 90-330 | 8.0s | Depth chart, then pulled-joint burst as climax |
| Pump + Gas | 330-660 | 11.0s | Compressed P/T then gas kick zoom |
| Payoff | 660-900 | 8.0s | Summary bullets + metrics |

The trimmed cut drops the Interventions scene. The pulled-1-joint hero moment
moves into the Depth scene as its climax: the trace reaches bottom, glow burst,
then the amber PULLED 1 JOINT line + burst.

## 7. Files Changed

| File | Change type | Description |
|---|---|---|
| `run3Data.ts` | MODIFY | Update frame ranges for 1500-frame primary, add RUN3_SHORT_SCENES and RUN3_SHORT_DURATION_FRAMES |
| `Run3Storyboard.tsx` | MODIFY | Add evolvePath to 4 charts, add GlowBurst usage, add NumberCounter usage, add callout temporal windows, add crimson edge flash, update frame ranges |
| `Run3StoryboardShort.tsx` | NEW | 4-scene trimmed composition |
| `Root.tsx` | MODIFY | Register DeploymentStoryRun3Short composition |
| `package.json` | MODIFY | Add render-run3-short and still-run3-short scripts |
| `components/GlowBurst.tsx` | NEW | Reusable radial glow burst with spring animation |
| `components/NumberCounter.tsx` | NEW | Interpolated numeric display with tabular-nums |

## 8. Verification Plan

1. **Storyboard audit skill** — Run wellfi-storyboard-audit pre-render checklist
   against the claim register before any render
2. **Still frame comparison** — Render stills at each hero moment frame and compare
   against the approved wellfi-run3-deployment-story.png
3. **Data accuracy check** — Every number on screen traced back to run3Data.ts ->
   run3-narrative.md -> raw packet source
4. **Gemini peer review** — Review marketing copy/framing for claims that outrun
   the evidence

## 9. Constraints

- **Data module accuracy** — run3Data.ts values are locked to the claim register.
  No new data points, no rounding, no re-interpretation.
- **Design philosophy** — Subterranean Signal palette, dark canvas, sparse labels.
  Pop comes from timing and motion, not clutter.
- **Claim register** — run3-remotion-claim-register.md stays as-is. New claims for
  the short cut must go through the audit process.
- **No new dependencies** — evolvePath is already in @remotion/paths (installed).
  No additional npm packages needed.

## 10. Skills and Agents Used

- **remotion-data-video** — Primary skill for Remotion patterns (evolvePath, callouts, spring)
- **wellfi-storyboard-audit** — Pre-render evidence gate
- **engineering-visual** — Still frame generation for comparison
- **Gemini CLI** — Peer review of marketing claims (review only, no code gen)
- **production-data agent** — Verify timestamps and packet quality if questions arise
