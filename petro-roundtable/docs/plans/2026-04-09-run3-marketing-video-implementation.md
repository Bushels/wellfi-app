# Run 3 Marketing Video Enhancement — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the existing Run3 Remotion composition from a dashboard slide deck into a marketing video where events pop, traces draw themselves, and hero moments demand attention.

**Architecture:** Enhance the existing `Run3Storyboard.tsx` in-place. Add 2 new reusable components (`GlowBurst.tsx`, `NumberCounter.tsx`). Create a separate 4-scene short composition (`Run3StoryboardShort.tsx`). All data stays locked to the existing claim register in `run3Data.ts`.

**Tech Stack:** Remotion 4.0.447, React 19, TypeScript 5.9, `@remotion/paths` (evolvePath), SVG

**Project root:** `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\remotion-video`

**Design doc:** `petro-roundtable/docs/plans/2026-04-09-run3-marketing-video-design.md`

**Claim register:** `analysis/run3-remotion-claim-register.md` — every number on screen must be verifiable against this.

**Approved storyboard:** `analysis/wellfi-run3-deployment-story.png` — visual reference for data accuracy.

---

## Task 1: Update Scene Timing in Data Module

**Files:**
- Modify: `src/run3/run3Data.ts`

**Step 1: Update primary composition frame ranges**

Change `RUN3_DURATION_FRAMES` from 1200 to 1500, and update `RUN3_SCENES`:

```typescript
export const RUN3_DURATION_FRAMES = 1500;

export const RUN3_SCENES = {
  intro: [0, 120],
  depth: [120, 390],
  interventions: [390, 600],
  pump: [600, 900],
  gas: [900, 1200],
  payoff: [1200, 1500],
} as const;
```

**Step 2: Add short composition constants**

Below `RUN3_SCENES`, add:

```typescript
export const RUN3_SHORT_DURATION_FRAMES = 900;

export const RUN3_SHORT_SCENES = {
  intro: [0, 90],
  depthPull: [90, 330],
  pumpGas: [330, 660],
  payoff: [660, 900],
} as const;
```

**Step 3: Add hero beat frame markers**

Below the short scenes, add:

```typescript
// Hero beat frames — when the trace reaches each hero data point.
// GlowBurst components trigger relative to these.
export const HERO_BEATS = {
  peakSignal: { scene: "depth" as const, frame: 195 },      // ~2.5s into depth scene
  pulledJoint: { scene: "interventions" as const, frame: 440 }, // ~1.7s into interventions
  lastPressure: { scene: "pump" as const, frame: 855 },     // ~8.5s into pump scene
  crcFail: { scene: "gas" as const, frame: 1050 },          // ~5s into gas scene
  crcRecovery: { scene: "gas" as const, frame: 1080 },      // 1s after CRC fail
} as const;
```

**Step 4: Verify build**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/test-timing.png --frame=750`
Expected: Renders successfully (the pump scene should be visible at frame 750).

**Step 5: Commit**

```bash
git add src/run3/run3Data.ts
git commit -m "feat(remotion): update Run3 timing to 1500 frames, add short composition constants and hero beat markers"
```

---

## Task 2: Create GlowBurst Component

**Files:**
- Create: `src/components/GlowBurst.tsx`

**Step 1: Create the component**

```tsx
import React from "react";
import { spring, useCurrentFrame, interpolate } from "remotion";
import { FPS } from "../theme";

interface GlowBurstProps {
  /** Absolute frame when the burst fires */
  triggerFrame: number;
  /** Center X in the parent SVG coordinate space */
  cx: number;
  /** Center Y in the parent SVG coordinate space */
  cy: number;
  /** Burst color (hex) */
  color: string;
  /** Resting radius after the burst settles */
  restRadius?: number;
}

export function GlowBurst({
  triggerFrame,
  cx,
  cy,
  color,
  restRadius = 12,
}: GlowBurstProps): React.ReactElement | null {
  const frame = useCurrentFrame();
  const localFrame = frame - triggerFrame;
  if (localFrame < 0) return null;

  const burst = spring({
    frame: localFrame,
    fps: FPS,
    config: { damping: 12, mass: 0.6, stiffness: 180 },
  });

  // Scale: 0 -> 2.5x rest radius, then settle to 1.2x
  const radius = interpolate(burst, [0, 1], [0, restRadius * 2.5], {
    extrapolateRight: "clamp",
  });

  // After the spring settles, hold at 1.2x
  const settledRadius = localFrame > 24 ? restRadius * 1.2 : radius;
  const finalRadius = localFrame > 24 ? settledRadius : radius;

  // Opacity: fade in fast, then settle to 0.25
  const opacity = interpolate(
    localFrame,
    [0, 6, 18, 36],
    [0, 0.4, 0.35, 0.25],
    { extrapolateRight: "clamp" },
  );

  return (
    <circle
      cx={cx}
      cy={cy}
      r={finalRadius}
      fill="none"
      stroke={color}
      strokeWidth={2}
      opacity={opacity}
      style={{
        filter: `drop-shadow(0 0 ${finalRadius * 0.8}px ${color})`,
      }}
    />
  );
}
```

**Step 2: Verify build**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/test-glow.png --frame=200`
Expected: Builds successfully (component not yet used, just compiled).

**Step 3: Commit**

```bash
git add src/components/GlowBurst.tsx
git commit -m "feat(remotion): add GlowBurst reusable component for hero moment emphasis"
```

---

## Task 3: Create NumberCounter Component

**Files:**
- Create: `src/components/NumberCounter.tsx`

**Step 1: Create the component**

```tsx
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface NumberCounterProps {
  /** The target number to count to */
  target: number;
  /** Absolute frame when counting starts */
  startFrame: number;
  /** How many frames the count takes (default 18) */
  duration?: number;
  /** Number to start counting from (default: 0 or nearest round value) */
  from?: number;
  /** Prefix string (e.g. "-" for negative display) */
  prefix?: string;
  /** Suffix string (e.g. " kPa", " dBV", "%", " min") */
  suffix?: string;
  /** Decimal places (default 0) */
  decimals?: number;
  /** CSS style for the container */
  style?: React.CSSProperties;
}

export function NumberCounter({
  target,
  startFrame,
  duration = 18,
  from = 0,
  prefix = "",
  suffix = "",
  decimals = 0,
  style,
}: NumberCounterProps): React.ReactElement {
  const frame = useCurrentFrame();

  const value = interpolate(
    frame,
    [startFrame, startFrame + duration],
    [from, target],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  const display = `${prefix}${value.toFixed(decimals)}${suffix}`;

  return (
    <span
      style={{
        fontVariantNumeric: "tabular-nums",
        ...style,
      }}
    >
      {display}
    </span>
  );
}
```

**Step 2: Verify build**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/test-counter.png --frame=200`
Expected: Builds successfully.

**Step 3: Commit**

```bash
git add src/components/NumberCounter.tsx
git commit -m "feat(remotion): add NumberCounter component with interpolated count-up and tabular-nums"
```

---

## Task 4: Add evolvePath to Depth Scene

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

This is the first and most impactful trace animation. The signal-vs-depth polyline draws itself top-to-bottom as the tool descends.

**Step 1: Add imports**

At the top of `Run3Storyboard.tsx`, add:

```typescript
import { evolvePath } from "@remotion/paths";
import { Easing } from "remotion";
```

Also add to the existing `remotion` import: `Easing` (if not already there).

**Step 2: Convert Depth scene polyline to path + evolvePath**

In `DepthScene`, locate the two `<polyline>` elements (the fat dim glow and the sharp bright trace). Replace both with animated paths.

The key change is converting the `polyline` to a path string and using `evolvePath`:

Inside `DepthScene`, before the SVG, add:

```typescript
// Build the SVG path string from visible points
const pathD = visiblePoints.length >= 2
  ? `M ${visiblePoints[0].x} ${visiblePoints[0].y} ` +
    visiblePoints.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
  : "";

// Progressive reveal: trace draws top-to-bottom over the scene
const traceProgress = interpolate(
  props.state.progress,
  [0.04, 0.88],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
);

const evolved = pathD ? evolvePath(traceProgress, pathD) : null;
```

Then replace the two polyline elements with:

```tsx
{evolved ? (
  <>
    <path
      d={pathD}
      fill="none"
      stroke={rgba(COLORS.cyan, 0.16)}
      strokeWidth={22}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={evolved.strokeDasharray}
      strokeDashoffset={evolved.strokeDashoffset}
    />
    <path
      d={pathD}
      fill="none"
      stroke={COLORS.cyan}
      strokeWidth={6}
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.8)})` }}
      strokeDasharray={evolved.strokeDasharray}
      strokeDashoffset={evolved.strokeDashoffset}
    />
  </>
) : null}
```

**Step 3: Make data point circles appear progressively**

Update the circle rendering to only show points that the trace has passed. After `evolved`, add:

```typescript
// Each point appears when the trace progress passes its normalized position
const pointVisibility = (index: number): number => {
  const pointProgress = index / Math.max(1, visiblePoints.length - 1);
  return traceProgress >= pointProgress ? 1 : 0;
};
```

Then in the circles map, wrap each circle with `opacity={pointVisibility(index)}`.

**Step 4: Make callout labels appear with their point**

The peak, fluid, and bottom callout blocks should each get an opacity controlled by `pointVisibility` for their respective index.

Find `peakPoint`, `fluidPoint`, `bottomPoint` — each already checks for null. Add opacity:

```tsx
{peakPoint ? (
  <g opacity={pointVisibility(1)}> {/* index 1 = peak signal */}
    {/* existing line + text */}
  </g>
) : null}
```

Repeat for `fluidPoint` (index 2) and `bottomPoint` (last index).

**Step 5: Verify with still frames**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/depth-start.png --frame=140`
Expected: Only the first 1-2 points of the trace visible (tool just entering).

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/depth-mid.png --frame=250`
Expected: Trace drawn partway, peak signal and fluid contact visible.

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/depth-end.png --frame=380`
Expected: Full trace with all points and annotations visible.

**Step 6: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add evolvePath progressive trace drawing to Depth scene"
```

---

## Task 5: Add evolvePath to Pump Scene

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Convert pressure polyline to path + evolvePath**

In `PumpScene`, before the SVG, add trace progress for pressure and temperature:

```typescript
const pressurePathD = pressureLine.length >= 2
  ? `M ${pressureLine[0].x} ${pressureLine[0].y} ` +
    pressureLine.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
  : "";

const tempPathD = tempLine.length >= 2
  ? `M ${tempLine[0].x} ${tempLine[0].y} ` +
    tempLine.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
  : "";

const pressureTrace = interpolate(
  props.state.progress,
  [0.0, 0.87],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
);

// Temperature trace follows pressure with a slight delay
const tempTrace = interpolate(
  props.state.progress,
  [0.07, 0.87],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
);

const pressureEvolved = pressurePathD ? evolvePath(pressureTrace, pressurePathD) : null;
const tempEvolved = tempPathD ? evolvePath(tempTrace, tempPathD) : null;
```

**Step 2: Replace both polylines**

Replace the pressure polylines (fat + bright) with `<path>` using `pressureEvolved.strokeDasharray/strokeDashoffset`.

Replace the temperature polylines with `<path>` using `tempEvolved.strokeDasharray/strokeDashoffset`.

Same pattern as Task 4: keep the 2-layer glow, apply dash props to both layers.

**Step 3: Progressive point visibility for callouts**

The `lastPoint` callout (LATE RAW TAIL 1810 kPa) and `coldSlug` callout should appear only when the trace reaches them:

```typescript
const pressurePointVisible = (minute: number): number => {
  const normalizedPos = compressedTimeRatio(minute);
  return pressureTrace >= normalizedPos ? 1 : 0;
};
```

Wrap `lastPoint` and `coldSlug` SVG groups with `opacity={pressurePointVisible(point.data.minute)}`.

**Step 4: Verify with still frames**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/pump-start.png --frame=620`
Expected: Pressure trace just starting to draw, temperature not yet visible.

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/pump-mid.png --frame=750`
Expected: Both traces drawn through overnight, approaching morning readings.

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/pump-end.png --frame=890`
Expected: Full traces with LATE RAW TAIL 1810 kPa callout visible.

**Step 5: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add evolvePath progressive traces to Pump scene (pressure + temperature)"
```

---

## Task 6: Add evolvePath to Gas Kick Scene

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Convert gas kick polyline to path + evolvePath**

In `GasKickScene`, add:

```typescript
const gasPathD = goodLine.length >= 2
  ? `M ${goodLine[0].x} ${goodLine[0].y} ` +
    goodLine.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
  : "";

const gasTrace = interpolate(
  props.state.progress,
  [0.0, 0.7],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
);

const gasEvolved = gasPathD ? evolvePath(gasTrace, gasPathD) : null;
```

**Step 2: Replace the polylines**

Same 2-layer pattern. Replace polyline with `<path d={gasPathD}>` using evolved dash props.

**Step 3: Progressive circles**

Data point circles appear as the trace passes them:

```typescript
const gasPointVisible = (minute: number): number => {
  const normalizedPos = minute / 57;
  return gasTrace >= normalizedPos ? 1 : 0;
};
```

Wrap each `goodPoints.map` circle with `opacity={gasPointVisible(point.minute)}`.

**Step 4: Make CRC fail marker appear at the right moment**

The CRC fail X marker and label should appear when `gasTrace >= 50/57` (~0.877). Use the existing `pulse` animation but gate it behind the trace progress.

**Step 5: Verify**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/gas-mid.png --frame=1000`
Expected: Trace drawn partway, pre-kick points visible.

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/gas-kick.png --frame=1100`
Expected: CRC fail marker visible with pulse, recovery point drawn.

**Step 6: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add evolvePath progressive trace to Gas Kick scene"
```

---

## Task 7: Integrate GlowBurst at Hero Moments

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Import GlowBurst**

```typescript
import { GlowBurst } from "../components/GlowBurst";
import { HERO_BEATS } from "./run3Data";
```

**Step 2: Add GlowBurst to Depth scene (peak signal)**

Inside the DepthScene SVG, after the circles, add:

```tsx
{peakPoint ? (
  <GlowBurst
    triggerFrame={HERO_BEATS.peakSignal.frame}
    cx={peakPoint.x}
    cy={peakPoint.y}
    color={COLORS.green}
    restRadius={18}
  />
) : null}
```

**Step 3: Add GlowBurst to Interventions scene (pulled 1 joint)**

In `InterventionScene`, add a GlowBurst next to the "Blackout ended" MetricCard. Since this scene doesn't have an SVG chart, wrap the MetricCard in a `<div style={{ position: "relative" }}>` and add an absolutely positioned glow div:

```tsx
<div style={{ position: "relative" }}>
  <MetricCard label="Blackout ended" value="84 min" accent={COLORS.amber} tone={COLORS.bgGrad} />
  <div
    style={{
      position: "absolute",
      inset: 0,
      borderRadius: 28,
      opacity: interpolate(
        frame,
        [HERO_BEATS.pulledJoint.frame, HERO_BEATS.pulledJoint.frame + 12, HERO_BEATS.pulledJoint.frame + 30],
        [0, 0.35, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
      ),
      boxShadow: `0 0 40px ${rgba(COLORS.amber, 0.6)}, inset 0 0 20px ${rgba(COLORS.amber, 0.15)}`,
      pointerEvents: "none" as const,
    }}
  />
</div>
```

Note: `InterventionScene` will need access to `frame` — add `const frame = useCurrentFrame();` at the top of the component (or pass it through props).

**Step 4: Add GlowBurst to Gas Kick scene (CRC fail + recovery)**

Inside the GasKickScene SVG, after the bad point marker:

```tsx
{badPoint ? (
  <>
    <GlowBurst
      triggerFrame={HERO_BEATS.crcFail.frame}
      cx={xFor(badPoint.minute)}
      cy={chart.y + 40}
      color={COLORS.crimson}
      restRadius={24}
    />
    {/* Recovery burst — green, 30 frames later */}
    <GlowBurst
      triggerFrame={HERO_BEATS.crcRecovery.frame}
      cx={xFor(57)}
      cy={yFor(19.34)}
      color={COLORS.green}
      restRadius={16}
    />
  </>
) : null}
```

**Step 5: Add GlowBurst to Pump scene (last pressure point)**

Inside the PumpScene SVG, near the `lastPoint` circle:

```tsx
{lastPoint ? (
  <GlowBurst
    triggerFrame={HERO_BEATS.lastPressure.frame}
    cx={lastPoint.x}
    cy={lastPoint.y}
    color={COLORS.cyan}
    restRadius={14}
  />
) : null}
```

**Step 6: Verify all 4 hero moments**

Run still frames at each hero beat:
- `--frame=195` (peak signal in depth)
- `--frame=440` (pulled joint in interventions)
- `--frame=855` (last pressure in pump)
- `--frame=1050` (CRC fail in gas kick)

Expected: Each shows a visible glow burst at the hero data point.

**Step 7: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add GlowBurst hero emphasis to all 4 hero moments"
```

---

## Task 8: Integrate NumberCounter into MetricCards

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Import NumberCounter**

```typescript
import { NumberCounter } from "../components/NumberCounter";
```

**Step 2: Update key MetricCard values to use NumberCounter**

Replace the static `value` strings in the hero metric cards with `NumberCounter`:

In **DepthScene**:
```tsx
<MetricCard label="Peak signal" value={<NumberCounter target={37} from={0} prefix="-" suffix=" dBV" startFrame={HERO_BEATS.peakSignal.frame} />} accent={COLORS.green} />
```

In **PumpScene**:
```tsx
<MetricCard label="Late Apr 3" value={<NumberCounter target={1810} from={1800} suffix=" kPa" startFrame={HERO_BEATS.lastPressure.frame} />} accent={COLORS.cyan} />
<MetricCard label="Steady state" value={<NumberCounter target={2069} from={2000} suffix=" kPa" startFrame={600 + 12} />} accent={COLORS.cyan} />
```

In **GasKickScene**:
```tsx
<MetricCard label="Recovery" value={<NumberCounter target={7} from={0} suffix=" min" startFrame={HERO_BEATS.crcRecovery.frame} />} accent={COLORS.green} />
```

Note: `MetricCard` currently accepts `value: string`. Update the prop type to `value: React.ReactNode` to accept JSX.

**Step 3: Update MetricCard props type**

Change the MetricCard component's `value` prop from `string` to `React.ReactNode`.

**Step 4: Verify**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/counter-before.png --frame=192`
Expected: Peak signal counter shows a partial value (mid-count).

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/counter-after.png --frame=220`
Expected: Peak signal counter shows -37 dBV (fully counted).

**Step 5: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): integrate NumberCounter into hero MetricCards for count-up animation"
```

---

## Task 9: Add Crimson Edge Flash to Gas Kick

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Add the vignette flash**

In the main `Run3Storyboard` component, after the `<GasKickScene>` element, add an `AbsoluteFill` that flashes when the CRC fail fires:

```tsx
<AbsoluteFill
  style={{
    background: `radial-gradient(circle at 50% 50%, transparent 55%, ${rgba(COLORS.crimson, 0.12)} 100%)`,
    opacity: interpolate(
      frame,
      [HERO_BEATS.crcFail.frame - 2, HERO_BEATS.crcFail.frame + 4, HERO_BEATS.crcFail.frame + 14],
      [0, 0.08, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
    ),
    pointerEvents: "none" as const,
  }}
/>
```

This produces a brief crimson edge tint (0.08 opacity, 12 frames) that reads as an alert without being jarring.

**Step 2: Verify**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/flash-peak.png --frame=1052`
Expected: Subtle crimson vignette visible at screen edges.

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/flash-after.png --frame=1068`
Expected: Vignette fully faded.

**Step 3: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add subtle crimson edge flash at CRC fail hero moment"
```

---

## Task 10: Add Callout Temporal Separation

**Files:**
- Modify: `src/run3/Run3Storyboard.tsx`

**Step 1: Create a timed callout wrapper**

Add a helper function near the top of the file:

```typescript
function timedOpacity(
  frame: number,
  appearFrame: number,
  disappearFrame: number,
  fadeFrames = 12,
): number {
  const enter = interpolate(frame, [appearFrame, appearFrame + fadeFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exit = interpolate(frame, [disappearFrame - fadeFrames, disappearFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return clamp(Math.min(enter, exit), 0, 1);
}
```

**Step 2: Apply to AnnotationBox elements**

Wrap each AnnotationBox in each scene with a `<div style={{ opacity: timedOpacity(frame, appear, disappear) }}>`.

Timing per scene:
- **Depth scene**: "Why this matters" box appears at frame 250, disappears at frame 380
- **Interventions**: "Customer-safe framing" box appears at frame 520, disappears at frame 595
- **Pump scene**: "Pump readout" box appears at frame 650, disappears at frame 780. "Conflict handled" box appears at frame 790, disappears at frame 895
- **Gas kick**: "Correct interpretation" appears at frame 1020, disappears at frame 1120. "Operator context" appears at frame 1130, disappears at frame 1195

This ensures at most 1-2 callouts are visible per scene, preventing visual clutter.

**Step 3: Each scene needs `useCurrentFrame()` access**

Several scenes already have `frame` via props. For scenes that don't, add `const frame = useCurrentFrame();` at the top of the scene component.

**Step 4: Verify**

Render stills at transition points to confirm callouts appear/disappear:
- `--frame=240` (Depth, before callout — should not be visible)
- `--frame=300` (Depth, callout visible)
- `--frame=390` (Depth exit, callout faded)

**Step 5: Commit**

```bash
git add src/run3/Run3Storyboard.tsx
git commit -m "feat(remotion): add temporal separation to AnnotationBox callouts — spring in, fade out per act"
```

---

## Task 11: Update Root.tsx and package.json

**Files:**
- Modify: `src/Root.tsx`
- Modify: `package.json`

**Step 1: Update Root.tsx with new duration**

Change the `DeploymentStoryRun3` composition's `durationInFrames` to use the new 1500 value (it already imports `RUN3_DURATION_FRAMES`, so this should update automatically).

Add the short composition registration:

```tsx
import { Run3StoryboardShort } from "./run3/Run3StoryboardShort";
import { RUN3_SHORT_DURATION_FRAMES } from "./run3/run3Data";

// Inside RemotionRoot, add:
<Composition
  id="DeploymentStoryRun3Short"
  component={Run3StoryboardShort}
  durationInFrames={RUN3_SHORT_DURATION_FRAMES}
  fps={FPS}
  width={WIDTH}
  height={HEIGHT}
/>
```

**Step 2: Update package.json scripts**

Add to `"scripts"`:

```json
"render-run3-short": "remotion render src/index.ts DeploymentStoryRun3Short out/wellfi-run3-short.mp4",
"still-run3-short": "remotion still src/index.ts DeploymentStoryRun3Short out/wellfi-run3-short.png --frame=450"
```

Update the existing render-run3 still frame to use the new payoff scene:
```json
"still-run3": "remotion still src/index.ts DeploymentStoryRun3 out/wellfi-run3-deployment-story.png --frame=1350"
```

**Step 3: Create a placeholder Run3StoryboardShort.tsx**

Create `src/run3/Run3StoryboardShort.tsx` as a minimal placeholder that can be built out in Task 12:

```tsx
import React from "react";
import { AbsoluteFill } from "remotion";
import { COLORS, FONTS } from "../theme";

export const Run3StoryboardShort: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: COLORS.bg, fontFamily: FONTS.body }}>
      <div style={{ color: COLORS.white, fontSize: 48, padding: 96 }}>
        Run3StoryboardShort — placeholder
      </div>
    </AbsoluteFill>
  );
};
```

**Step 4: Verify both compositions build**

Run: `npx remotion still src/index.ts DeploymentStoryRun3 out/test-primary.png --frame=750`
Run: `npx remotion still src/index.ts DeploymentStoryRun3Short out/test-short.png --frame=100`
Expected: Both render successfully.

**Step 5: Commit**

```bash
git add src/Root.tsx src/run3/Run3StoryboardShort.tsx package.json
git commit -m "feat(remotion): register short composition, update scripts for 1500-frame primary"
```

---

## Task 12: Build Run3StoryboardShort (30s Trimmed Cut)

**Files:**
- Modify: `src/run3/Run3StoryboardShort.tsx`

**Step 1: Build the 4-scene short composition**

This reuses the existing scene components from `Run3Storyboard.tsx` but with different timing. The approach:

- Extract `IntroScene`, `DepthScene`, `PumpScene`, `GasKickScene`, `PayoffScene` into importable components (or duplicate with adjusted timing)
- The simplest approach: create a self-contained `Run3StoryboardShort` that references `RUN3_SHORT_SCENES` and combines:
  - Condensed Intro (3s)
  - DepthPull scene: depth chart → pulled joint hero as climax (8s)
  - PumpGas scene: compressed P/T → gas kick zoom (11s)
  - Payoff (8s)

Since the scenes are tightly coupled to their frame ranges, the cleanest approach is to build `Run3StoryboardShort` as a standalone composition that imports from `run3Data.ts` but has its own scene functions tuned for the compressed timing.

The implementation should follow the same patterns (evolvePath, GlowBurst, NumberCounter) established in Tasks 4-10.

**Step 2: Verify**

Run: `npx remotion still src/index.ts DeploymentStoryRun3Short out/short-intro.png --frame=45`
Run: `npx remotion still src/index.ts DeploymentStoryRun3Short out/short-depth.png --frame=200`
Run: `npx remotion still src/index.ts DeploymentStoryRun3Short out/short-pump.png --frame=500`
Run: `npx remotion still src/index.ts DeploymentStoryRun3Short out/short-payoff.png --frame=780`

**Step 3: Commit**

```bash
git add src/run3/Run3StoryboardShort.tsx
git commit -m "feat(remotion): build 30s trimmed composition with 4 scenes and all animation enhancements"
```

---

## Task 13: Storyboard Audit + Final Verification

**Files:**
- Read: `analysis/run3-remotion-claim-register.md`
- Read: `analysis/wellfi-run3-deployment-story.png`
- Read: `petro-roundtable/knowledge/wellfi-telemetry.md`

**Step 1: Run the wellfi-storyboard-audit skill pre-render checklist**

Verify against the claim register:
- [ ] All dates and times match the approved run window (Apr 2-3, 2026)
- [ ] All unit conversions correct (BAR to kPa: x100)
- [ ] All depth references use correct MD/TVD values
- [ ] Pressure callouts match: 2069, 1928, 1810 kPa
- [ ] Gas kick values match: 19.1-19.4 BAR normal band, 168.65 BAR corrupted
- [ ] No claims added that aren't in the claim register

**Step 2: Render hero moment stills and compare to approved storyboard**

```bash
npx remotion still src/index.ts DeploymentStoryRun3 out/hero-peak.png --frame=210
npx remotion still src/index.ts DeploymentStoryRun3 out/hero-pull.png --frame=450
npx remotion still src/index.ts DeploymentStoryRun3 out/hero-pressure.png --frame=860
npx remotion still src/index.ts DeploymentStoryRun3 out/hero-gaskick.png --frame=1060
npx remotion still src/index.ts DeploymentStoryRun3 out/hero-recovery.png --frame=1090
npx remotion still src/index.ts DeploymentStoryRun3 out/payoff.png --frame=1350
```

Visually compare each against `wellfi-run3-deployment-story.png` for data accuracy.

**Step 3: Gemini peer review of marketing copy**

Use `mcp__gemini-cli__ask-gemini` to review the on-screen text for any claims that outrun the evidence. Focus question: "Do any of these statements overstate what the WellFi tool actually demonstrated?"

**Step 4: Render final videos**

```bash
npm run render-run3
npm run render-run3-short
```

Expected output:
- `out/wellfi-run3-deployment-story.mp4` (50s primary)
- `out/wellfi-run3-short.mp4` (30s trimmed)

**Step 5: Commit**

```bash
git add -A
git commit -m "feat(remotion): Run 3 marketing video complete — progressive traces, hero glow bursts, number counters, 50s primary + 30s trimmed"
```

---

## Summary

| Task | What | Est. time |
|---|---|---|
| 1 | Update scene timing in data module | 5 min |
| 2 | Create GlowBurst component | 10 min |
| 3 | Create NumberCounter component | 10 min |
| 4 | evolvePath in Depth scene | 15 min |
| 5 | evolvePath in Pump scene | 15 min |
| 6 | evolvePath in Gas Kick scene | 10 min |
| 7 | Integrate GlowBurst at 4 hero moments | 15 min |
| 8 | Integrate NumberCounter in MetricCards | 10 min |
| 9 | Crimson edge flash | 5 min |
| 10 | Callout temporal separation | 15 min |
| 11 | Root.tsx + package.json + placeholder | 5 min |
| 12 | Build 30s short composition | 25 min |
| 13 | Storyboard audit + final verification | 15 min |
