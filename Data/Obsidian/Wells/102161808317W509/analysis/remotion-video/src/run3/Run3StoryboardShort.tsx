import React from "react";
import { evolvePath } from "@remotion/paths";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame } from "remotion";
import { GlowBurst } from "../components/GlowBurst";
import { NumberCounter } from "../components/NumberCounter";
import { COLORS, FONTS, FPS } from "../theme";
import {
  GAS_KICK_POINTS,
  LATE_PM_KPA,
  OVERNIGHT_AVG_KPA,
  PAYOFF_BULLETS,
  PAYOFF_METRICS,
  PRESSURE_TEMP_POINTS,
  RUN3_SHORT_SCENES,
  SIGNAL_DEPTH_POINTS,
  STEADY_STATE_KPA,
  TOTAL_RUN3_MINUTES,
  compressedTimeRatio,
  gasKickMarkerMinute,
  overnightEndMinute,
  overnightStartMinute,
  pumpMarkerMinute,
} from "./run3Data";

/* ── Layout constants ──────────────────────────────────────────────── */

const HEADER_HEIGHT = 136;
const FOOTER_HEIGHT = 56;
const CONTENT_TOP = HEADER_HEIGHT + 18;
const CONTENT_LEFT = 96;
const CONTENT_WIDTH = 1728;
const CONTENT_HEIGHT = 1080 - CONTENT_TOP - FOOTER_HEIGHT - 28;

type ShortSceneKey = keyof typeof RUN3_SHORT_SCENES;
type ShortSceneRange = (typeof RUN3_SHORT_SCENES)[ShortSceneKey];

/* ── Hero beats for the 30-second cut ──────────────────────────────── */

const SHORT_BEATS = {
  peakSignal: 165,
  pulledJoint: 285,
  lastPressure: 510,
  crcFail: 570,
  crcRecovery: 590,
} as const;

/* ── Scene strip metadata ──────────────────────────────────────────── */

const SHORT_SCENE_META: Array<{ key: ShortSceneKey; label: string; color: string }> = [
  { key: "intro", label: "Run 3", color: COLORS.cyan },
  { key: "depthPull", label: "Depth + Pull", color: COLORS.green },
  { key: "pumpGas", label: "Pump + Gas", color: COLORS.cyan },
  { key: "payoff", label: "Payoff", color: COLORS.green },
];

/* ── Shared utilities ──────────────────────────────────────────────── */

interface XYPoint {
  x: number;
  y: number;
}

interface SceneWindowState {
  active: boolean;
  localFrame: number;
  opacity: number;
  progress: number;
  scale: number;
  translateY: number;
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function rgba(hex: string, alpha: number): string {
  const clean = hex.replace("#", "");
  const normalized =
    clean.length === 3
      ? clean
          .split("")
          .map((char) => `${char}${char}`)
          .join("")
      : clean;
  const r = Number.parseInt(normalized.slice(0, 2), 16);
  const g = Number.parseInt(normalized.slice(2, 4), 16);
  const b = Number.parseInt(normalized.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function getSceneWindow(frame: number, range: ShortSceneRange): SceneWindowState {
  const [start, end] = range;
  const localFrame = Math.max(0, frame - start);
  const duration = end - start;
  const enter = spring({
    frame: localFrame,
    fps: FPS,
    config: { damping: 18, stiffness: 140, mass: 0.8 },
  });
  const exit = interpolate(frame, [end - 18, end], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = clamp(enter * exit, 0, 1);
  return {
    active: frame >= start && frame < end,
    localFrame,
    opacity,
    progress: clamp((frame - start) / duration, 0, 1),
    scale: interpolate(enter, [0, 1], [0.985, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
    translateY: interpolate(enter, [0, 1], [34, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
  };
}

function stepIn(localFrame: number, delay: number, duration = 18): number {
  return clamp(
    interpolate(localFrame, [delay, delay + duration], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
    0,
    1,
  );
}

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

function panelStyle(accent: string = COLORS.cyan): React.CSSProperties {
  return {
    background: `linear-gradient(180deg, ${rgba(COLORS.panel, 0.96)} 0%, ${rgba(COLORS.bg, 0.96)} 100%)`,
    border: `1px solid ${rgba(accent, 0.2)}`,
    boxShadow: `0 18px 50px ${rgba(COLORS.bg, 0.45)}, inset 0 0 0 1px ${rgba(COLORS.white, 0.03)}`,
    borderRadius: 28,
    overflow: "hidden",
  };
}

/* ── Reusable UI components ────────────────────────────────────────── */

function Panel(props: {
  title: string;
  eyebrow?: string;
  accent?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}): React.ReactElement {
  const accent = props.accent ?? COLORS.cyan;
  return (
    <div style={{ ...panelStyle(accent), ...props.style }}>
      <div
        style={{
          padding: "22px 26px 0",
          display: "flex",
          alignItems: "baseline",
          justifyContent: "space-between",
          gap: 12,
        }}
      >
        <div>
          {props.eyebrow ? (
            <div
              style={{
                color: rgba(accent, 0.78),
                fontFamily: FONTS.mono,
                fontSize: 14,
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                marginBottom: 8,
              }}
            >
              {props.eyebrow}
            </div>
          ) : null}
          <div
            style={{
              color: COLORS.white,
              fontFamily: FONTS.title,
              fontSize: 34,
              fontWeight: 600,
              letterSpacing: "-0.03em",
            }}
          >
            {props.title}
          </div>
        </div>
      </div>
      {props.children}
    </div>
  );
}

function MetricCard(props: {
  label: string;
  value: React.ReactNode;
  accent: string;
  tone?: string;
  style?: React.CSSProperties;
}): React.ReactElement {
  return (
    <div
      style={{
        ...panelStyle(props.accent),
        padding: "18px 20px",
        background: `linear-gradient(180deg, ${rgba(props.tone ?? COLORS.panel, 0.92)} 0%, ${rgba(COLORS.bg, 0.96)} 100%)`,
        ...props.style,
      }}
    >
      <div
        style={{
          color: rgba(props.accent, 0.86),
          fontFamily: FONTS.mono,
          fontSize: 13,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          marginBottom: 10,
        }}
      >
        {props.label}
      </div>
      <div
        style={{
          color: COLORS.white,
          fontFamily: FONTS.title,
          fontSize: 34,
          fontWeight: 600,
          lineHeight: 1,
        }}
      >
        {props.value}
      </div>
    </div>
  );
}

function SceneFrame(props: {
  state: SceneWindowState;
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <div
      style={{
        position: "absolute",
        inset: `${CONTENT_TOP}px ${1920 - CONTENT_LEFT - CONTENT_WIDTH}px ${FOOTER_HEIGHT + 16}px ${CONTENT_LEFT}px`,
        opacity: props.state.opacity,
        transform: `translateY(${props.state.translateY}px) scale(${props.state.scale})`,
      }}
    >
      {props.children}
    </div>
  );
}

function HeaderBar(): React.ReactElement {
  return (
    <div
      style={{
        position: "absolute",
        top: 38,
        left: CONTENT_LEFT,
        right: CONTENT_LEFT,
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "space-between",
      }}
    >
      <div>
        <div
          style={{
            color: COLORS.white,
            fontFamily: FONTS.title,
            fontSize: 58,
            letterSpacing: "-0.04em",
            fontWeight: 500,
          }}
        >
          WellFi Run 3
        </div>
        <div
          style={{
            color: rgba(COLORS.text, 0.68),
            fontFamily: FONTS.body,
            fontSize: 23,
            marginTop: 8,
          }}
        >
          OBE 102 HZ 16-18-83-17W5 | Obsidian Energy | Apr 2 to Apr 3, 2026
        </div>
      </div>
      <div
        style={{
          color: COLORS.cyan,
          fontFamily: FONTS.title,
          fontSize: 34,
          fontWeight: 600,
          letterSpacing: "-0.04em",
          marginTop: 8,
          textShadow: `0 0 24px ${rgba(COLORS.cyan, 0.45)}`,
        }}
      >
        WellFi
      </div>
    </div>
  );
}

function SceneStrip(props: { activeKey: ShortSceneKey }): React.ReactElement {
  return (
    <div
      style={{
        position: "absolute",
        left: CONTENT_LEFT,
        right: CONTENT_LEFT,
        bottom: 12,
        display: "grid",
        gridTemplateColumns: `repeat(${SHORT_SCENE_META.length}, minmax(0, 1fr))`,
        gap: 14,
      }}
    >
      {SHORT_SCENE_META.map((scene) => {
        const active = scene.key === props.activeKey;
        return (
          <div
            key={scene.key}
            style={{
              ...panelStyle(scene.color),
              padding: "10px 14px",
              borderColor: active ? rgba(scene.color, 0.65) : rgba(scene.color, 0.12),
              boxShadow: active
                ? `0 0 32px ${rgba(scene.color, 0.22)}, inset 0 0 0 1px ${rgba(scene.color, 0.18)}`
                : `0 14px 30px ${rgba(COLORS.bg, 0.35)}`,
              background: active
                ? `linear-gradient(180deg, ${rgba(scene.color, 0.16)} 0%, ${rgba(COLORS.panel, 0.92)} 100%)`
                : `linear-gradient(180deg, ${rgba(COLORS.panel, 0.82)} 0%, ${rgba(COLORS.bg, 0.92)} 100%)`,
            }}
          >
            <div
              style={{
                color: active ? COLORS.white : rgba(COLORS.text, 0.7),
                fontFamily: FONTS.mono,
                fontSize: 12,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
                marginBottom: 4,
              }}
            >
              {scene.key}
            </div>
            <div
              style={{
                color: active ? scene.color : COLORS.text,
                fontFamily: FONTS.title,
                fontSize: 24,
                fontWeight: 500,
                lineHeight: 1,
              }}
            >
              {scene.label}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ── Scene 1: Intro (0-90, 3s) ─────────────────────────────────────── */

function IntroScene(props: { state: SceneWindowState }): React.ReactElement {
  const glow = 0.35 + Math.sin(props.state.localFrame / 7) * 0.05;
  const stats = [
    { label: "Peak signal", value: "-37 dBV", accent: COLORS.green },
    { label: "Late pressure", value: "1810 kPa", accent: COLORS.cyan },
    { label: "Recovery", value: "7 min", accent: COLORS.crimson },
  ];

  return (
    <SceneFrame state={props.state}>
      <div
        style={{
          ...panelStyle(COLORS.cyan),
          width: "100%",
          height: CONTENT_HEIGHT,
          padding: "42px 46px",
          display: "grid",
          gridTemplateColumns: "1.2fr 0.8fr",
          gap: 28,
          background: `radial-gradient(circle at 22% 16%, ${rgba(COLORS.cyan, glow)} 0%, ${rgba(COLORS.bgGrad, 0.96)} 26%, ${rgba(COLORS.bg, 0.98)} 70%)`,
        }}
      >
        <div style={{ position: "relative" }}>
          <div
            style={{
              color: rgba(COLORS.cyan, 0.86),
              fontFamily: FONTS.mono,
              fontSize: 15,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
            }}
          >
            30-second highlight reel
          </div>
          <div
            style={{
              color: COLORS.white,
              fontFamily: FONTS.title,
              fontSize: 86,
              lineHeight: 0.92,
              letterSpacing: "-0.06em",
              fontWeight: 500,
              marginTop: 18,
              maxWidth: 860,
            }}
          >
            The first WellFi run that held up in the noise.
          </div>
          <div
            style={{
              color: rgba(COLORS.text, 0.78),
              fontFamily: FONTS.body,
              fontSize: 28,
              lineHeight: 1.45,
              marginTop: 24,
              maxWidth: 860,
            }}
          >
            Signal weakened through fluid. The field team reopened the link. The run captured pump behavior and the gas-kick disruption.
          </div>

          <svg
            width={920}
            height={420}
            viewBox="0 0 920 420"
            style={{ position: "absolute", left: -20, bottom: -10 }}
          >
            <defs>
              <linearGradient id="short-intro-line" x1="0" x2="1" y1="0" y2="1">
                <stop offset="0%" stopColor={COLORS.cyan} />
                <stop offset="55%" stopColor={rgba(COLORS.cyan, 0.8)} />
                <stop offset="100%" stopColor={COLORS.amber} />
              </linearGradient>
            </defs>
            <path
              d="M70 356 L190 338 L310 266 L420 258 L514 138 L658 106 L806 94"
              fill="none"
              stroke={rgba(COLORS.cyan, 0.12)}
              strokeWidth={24}
              strokeLinecap="round"
            />
            <path
              d="M70 356 L190 338 L310 266 L420 258 L514 138 L658 106 L806 94"
              fill="none"
              stroke="url(#short-intro-line)"
              strokeWidth={8}
              strokeLinecap="round"
              style={{ filter: `drop-shadow(0 0 18px ${rgba(COLORS.cyan, 0.7)})` }}
            />
            {[
              { x: 190, y: 338, color: COLORS.green },
              { x: 514, y: 138, color: COLORS.amber },
              { x: 806, y: 94, color: COLORS.cyan },
            ].map((point, index) => (
              <circle
                key={`${point.x}-${point.y}`}
                cx={point.x}
                cy={point.y}
                r={10 + Math.max(0, stepIn(props.state.localFrame, 10 + index * 10) * 10)}
                fill={rgba(point.color, 0.2)}
              />
            ))}
          </svg>
        </div>

        <div style={{ display: "grid", gap: 16, alignContent: "start" }}>
          {stats.map((stat, index) => (
            <MetricCard
              key={stat.label}
              label={stat.label}
              value={stat.value}
              accent={stat.accent}
              style={{
                opacity: stepIn(props.state.localFrame, 10 + index * 6),
                transform: `translateY(${(1 - stepIn(props.state.localFrame, 10 + index * 6)) * 22}px)`,
              }}
            />
          ))}
        </div>
      </div>
    </SceneFrame>
  );
}

/* ── Scene 2: DepthPull (90-330, 8s) ───────────────────────────────── */
/*
 *  First 5s: signal-vs-depth chart with evolvePath.
 *  Last 3s:  "PULLED 1 JOINT" hero callout with GlowBurst climax.
 */

function DepthPullScene(props: { state: SceneWindowState }): React.ReactElement {
  const frame = useCurrentFrame();
  const chart = { x: 80, y: 110, w: 820, h: 520 };
  const maxDepth = 920;
  const xFor = (dbv: number): number => chart.x + ((dbv + 110) / 85) * chart.w;
  const yFor = (md: number): number => chart.y + (md / maxDepth) * chart.h;

  const revealCount = clamp(
    Math.ceil(
      interpolate(props.state.progress, [0.06, 0.62], [2, SIGNAL_DEPTH_POINTS.length], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      }),
    ),
    2,
    SIGNAL_DEPTH_POINTS.length,
  );

  const visiblePoints = SIGNAL_DEPTH_POINTS.slice(0, revealCount).map((point) => ({
    x: xFor(point.signalDbv),
    y: yFor(point.md),
    data: point,
  }));

  const depthPathD =
    visiblePoints.length >= 2
      ? `M ${visiblePoints[0].x} ${visiblePoints[0].y} ` +
        visiblePoints
          .slice(1)
          .map((p) => `L ${p.x} ${p.y}`)
          .join(" ")
      : "";

  const traceProgress = interpolate(props.state.progress, [0.02, 0.60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

  const depthEvolved = depthPathD ? evolvePath(traceProgress, depthPathD) : null;

  const pointVisible = (index: number): number => {
    const pointProgress = index / Math.max(1, visiblePoints.length - 1);
    return traceProgress >= pointProgress ? 1 : 0;
  };

  const noiseX = xFor(-95);
  const pullY = yFor(822.82);
  const peakPoint = visiblePoints.find((point) => point.data.label === "Peak signal");
  const bottomPoint = visiblePoints[visiblePoints.length - 1];

  // "Pulled 1 joint" callout — appears in the last 3s of this scene
  const pullCalloutOpacity = interpolate(
    props.state.progress,
    [0.68, 0.76, 0.92, 1.0],
    [0, 1, 1, 0.85],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Amber flash behind the pulled-joint callout
  const pullFlash = interpolate(
    frame,
    [SHORT_BEATS.pulledJoint, SHORT_BEATS.pulledJoint + 10, SHORT_BEATS.pulledJoint + 28],
    [0, 0.35, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <SceneFrame state={props.state}>
      <div style={{ display: "grid", gridTemplateColumns: "1.25fr 0.75fr", gap: 24, height: CONTENT_HEIGHT }}>
        <Panel title="Signal through depth" eyebrow="RIH field notes" accent={COLORS.green} style={{ height: "100%" }}>
          <div style={{ padding: "18px 24px 24px", height: "100%" }}>
            <svg width={940} height={640} viewBox="0 0 940 640">
              <rect x={chart.x} y={chart.y} width={chart.w} height={chart.h} rx={24} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.65)} />
              {[-110, -95, -80, -65, -50, -35].map((value) => (
                <line
                  key={`x-${value}`}
                  x1={xFor(value)}
                  x2={xFor(value)}
                  y1={chart.y}
                  y2={chart.y + chart.h}
                  stroke={rgba(COLORS.grid, value === -95 ? 0 : 0.32)}
                  strokeDasharray={value === -95 ? "10 8" : "4 12"}
                />
              ))}
              {[0, 200, 400, 600, 800].map((value) => (
                <line
                  key={`y-${value}`}
                  x1={chart.x}
                  x2={chart.x + chart.w}
                  y1={yFor(value)}
                  y2={yFor(value)}
                  stroke={rgba(COLORS.grid, 0.28)}
                  strokeDasharray="4 12"
                />
              ))}
              <line x1={noiseX} x2={noiseX} y1={chart.y} y2={chart.y + chart.h} stroke={rgba(COLORS.crimson, 0.72)} strokeDasharray="14 10" />
              <line x1={chart.x} x2={chart.x + chart.w} y1={pullY} y2={pullY} stroke={rgba(COLORS.amber, 0.62)} strokeDasharray="16 10" />

              {depthEvolved ? (
                <>
                  <path
                    d={depthPathD}
                    fill="none"
                    stroke={rgba(COLORS.cyan, 0.16)}
                    strokeWidth={22}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={depthEvolved.strokeDasharray}
                    strokeDashoffset={depthEvolved.strokeDashoffset}
                  />
                  <path
                    d={depthPathD}
                    fill="none"
                    stroke={COLORS.cyan}
                    strokeWidth={6}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.8)})` }}
                    strokeDasharray={depthEvolved.strokeDasharray}
                    strokeDashoffset={depthEvolved.strokeDashoffset}
                  />
                </>
              ) : null}

              {visiblePoints.map((point, index) => (
                <circle
                  key={point.data.label}
                  cx={point.x}
                  cy={point.y}
                  r={point.data.label === "Peak signal" ? 9 : 6}
                  fill={point.data.label === "Peak signal" ? COLORS.green : COLORS.white}
                  stroke={COLORS.cyan}
                  strokeWidth={point.data.label === "Peak signal" ? 4 : 3}
                  opacity={pointVisible(index)}
                />
              ))}

              {peakPoint ? (
                <g opacity={pointVisible(1)}>
                  <line x1={peakPoint.x} x2={peakPoint.x - 130} y1={peakPoint.y} y2={peakPoint.y + 32} stroke={rgba(COLORS.green, 0.7)} />
                  <text x={peakPoint.x - 140} y={peakPoint.y + 26} fill={COLORS.green} fontFamily={FONTS.mono} fontSize={18}>
                    PEAK -37 dBV
                  </text>
                </g>
              ) : null}

              {bottomPoint ? (
                <g opacity={pointVisible(visiblePoints.length - 1)}>
                  <line x1={bottomPoint.x} x2={bottomPoint.x + 112} y1={bottomPoint.y} y2={bottomPoint.y - 34} stroke={rgba(COLORS.crimson, 0.7)} />
                  <text x={bottomPoint.x + 120} y={bottomPoint.y - 40} fill={COLORS.crimson} fontFamily={FONTS.mono} fontSize={18}>
                    ON BOTTOM -100 dBV
                  </text>
                </g>
              ) : null}

              <text x={noiseX + 12} y={chart.y + 34} fill={rgba(COLORS.crimson, 0.75)} fontFamily={FONTS.mono} fontSize={18}>
                NOISE FLOOR
              </text>
              <text x={chart.x + 18} y={pullY - 10} fill={rgba(COLORS.amber, 0.75)} fontFamily={FONTS.mono} fontSize={18}>
                PULLED 1 JOINT 823 m MD
              </text>
              <text x={chart.x} y={chart.y + chart.h + 42} fill={rgba(COLORS.text, 0.72)} fontFamily={FONTS.body} fontSize={19}>
                Signal (dBV)
              </text>
              <text
                x={chart.x - 40}
                y={chart.y + chart.h + 8}
                fill={rgba(COLORS.text, 0.72)}
                fontFamily={FONTS.body}
                fontSize={19}
                transform={`rotate(-90 ${chart.x - 40} ${chart.y + chart.h + 8})`}
              >
                Depth (m MD)
              </text>

              {peakPoint ? (
                <GlowBurst
                  triggerFrame={SHORT_BEATS.peakSignal}
                  cx={peakPoint.x}
                  cy={peakPoint.y}
                  color={COLORS.green}
                  restRadius={18}
                />
              ) : null}
            </svg>
          </div>
        </Panel>

        <div style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <MetricCard
            label="Peak signal"
            value={<NumberCounter target={37} from={0} prefix="-" suffix=" dBV" startFrame={SHORT_BEATS.peakSignal} />}
            accent={COLORS.green}
          />
          <MetricCard
            label="On bottom"
            value={<NumberCounter target={100} from={0} prefix="-" suffix=" dBV" startFrame={220} />}
            accent={COLORS.crimson}
          />

          {/* Pulled 1 joint hero callout — climax of this scene */}
          <div
            style={{
              position: "relative",
              opacity: pullCalloutOpacity,
              transform: `translateY(${(1 - pullCalloutOpacity) * 18}px)`,
            }}
          >
            <MetricCard label="Blackout ended" value="84 min" accent={COLORS.amber} tone={COLORS.bgGrad} />
            <div
              style={{
                position: "absolute",
                inset: 0,
                borderRadius: 28,
                opacity: pullFlash,
                boxShadow: `0 0 40px ${rgba(COLORS.amber, 0.6)}, inset 0 0 20px ${rgba(COLORS.amber, 0.15)}`,
                pointerEvents: "none" as const,
              }}
            />
          </div>

          <div
            style={{
              ...panelStyle(COLORS.amber),
              padding: "16px 18px",
              background: `linear-gradient(180deg, ${rgba(COLORS.bgGrad, 0.94)} 0%, ${rgba(COLORS.bg, 0.96)} 100%)`,
              opacity: pullCalloutOpacity,
              transform: `translateY(${(1 - pullCalloutOpacity) * 14}px)`,
            }}
          >
            <div
              style={{
                color: COLORS.amber,
                fontFamily: FONTS.mono,
                fontSize: 13,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
                marginBottom: 8,
              }}
            >
              Field intervention
            </div>
            <div
              style={{
                color: COLORS.white,
                fontFamily: FONTS.title,
                fontSize: 28,
                fontWeight: 500,
                letterSpacing: "-0.03em",
                marginBottom: 6,
              }}
            >
              Pulled 1 joint
            </div>
            <div
              style={{
                color: COLORS.text,
                fontFamily: FONTS.body,
                fontSize: 19,
                lineHeight: 1.4,
              }}
            >
              84-minute blackout ended. First packet arrived immediately after the pull.
            </div>
          </div>
        </div>
      </div>

      {/* GlowBurst for the pulled joint hero moment — overlaid on chart area */}
      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: "absolute", inset: 0, pointerEvents: "none" as const }}
      >
        <GlowBurst
          triggerFrame={SHORT_BEATS.pulledJoint}
          cx={CONTENT_LEFT + 470}
          cy={CONTENT_TOP + 530}
          color={COLORS.amber}
          restRadius={28}
        />
      </svg>
    </SceneFrame>
  );
}

/* ── Scene 3: PumpGas (330-660, 11s) ───────────────────────────────── */
/*
 *  First ~6s: compressed P/T timeline.
 *  Last ~5s:  gas kick zoom takes over the right panel.
 */

function PumpGasScene(props: { state: SceneWindowState }): React.ReactElement {
  const frame = useCurrentFrame();

  /* ── Pressure + Temperature chart ── */
  const pressureChart = { x: 56, y: 86, w: 740, h: 250 };
  const tempChart = { x: 56, y: 388, w: 740, h: 168 };
  const cleanPoints = PRESSURE_TEMP_POINTS.filter((point) => !point.corrupted);
  const badPoints = PRESSURE_TEMP_POINTS.filter((point) => point.corrupted);
  const pxFor = (minute: number): number => pressureChart.x + compressedTimeRatio(minute) * pressureChart.w;
  const pressureYFor = (kpa: number): number =>
    pressureChart.y + ((2200 - kpa) / (2200 - -100)) * pressureChart.h;
  const tempYFor = (temp: number): number => tempChart.y + ((28 - temp) / 30) * tempChart.h;

  const pressureLine = cleanPoints.map((point) => ({ x: pxFor(point.minute), y: pressureYFor(point.pressureKpa), data: point }));
  const tempLine = cleanPoints.map((point) => ({ x: pxFor(point.minute), y: tempYFor(point.tempC), data: point }));
  const lastPressurePoint = pressureLine[pressureLine.length - 1];

  const pressurePathD =
    pressureLine.length >= 2
      ? `M ${pressureLine[0].x} ${pressureLine[0].y} ` +
        pressureLine
          .slice(1)
          .map((p) => `L ${p.x} ${p.y}`)
          .join(" ")
      : "";
  const tempPathD =
    tempLine.length >= 2
      ? `M ${tempLine[0].x} ${tempLine[0].y} ` +
        tempLine
          .slice(1)
          .map((p) => `L ${p.x} ${p.y}`)
          .join(" ")
      : "";

  const pressureTrace = interpolate(props.state.progress, [0.0, 0.52], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const tempTrace = interpolate(props.state.progress, [0.04, 0.52], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

  const pressureEvolved = pressurePathD ? evolvePath(pressureTrace, pressurePathD) : null;
  const tempEvolved = tempPathD ? evolvePath(tempTrace, tempPathD) : null;

  const pressurePointVisible = (minute: number): number => {
    const normalizedPos = compressedTimeRatio(minute);
    return pressureTrace >= normalizedPos ? 1 : 0;
  };

  /* ── Gas kick zoom chart ── */
  const gasChart = { x: 56, y: 86, w: 600, h: 360 };
  const goodGasPoints = GAS_KICK_POINTS.filter((point) => point.good);
  const badGasPoint = GAS_KICK_POINTS.find((point) => !point.good);
  const gasXFor = (minute: number): number => gasChart.x + (minute / 57) * gasChart.w;
  const gasYFor = (pressure: number): number => gasChart.y + ((19.45 - pressure) / (19.45 - 19.08)) * gasChart.h;
  const pulse = 0.5 + 0.5 * Math.sin(props.state.localFrame / 3);
  const goodGasLine = goodGasPoints.map((point) => ({ x: gasXFor(point.minute), y: gasYFor(point.pressureBar) }));

  const gasPathD =
    goodGasLine.length >= 2
      ? `M ${goodGasLine[0].x} ${goodGasLine[0].y} ` +
        goodGasLine
          .slice(1)
          .map((p) => `L ${p.x} ${p.y}`)
          .join(" ")
      : "";

  // Gas trace starts drawing at ~50% scene progress (when the right panel switches)
  const gasTrace = interpolate(props.state.progress, [0.50, 0.85], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const gasEvolved = gasPathD ? evolvePath(gasTrace, gasPathD) : null;

  const gasPointVisible = (minute: number): number => {
    const normalizedPos = minute / 57;
    return gasTrace >= normalizedPos ? 1 : 0;
  };

  // Right panel crossfade: metrics in first half, gas kick chart in second half
  const gasPhaseOpacity = interpolate(props.state.progress, [0.46, 0.54], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const metricsPhaseOpacity = interpolate(props.state.progress, [0.46, 0.54], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <SceneFrame state={props.state}>
      <div style={{ display: "grid", gridTemplateColumns: "1.15fr 0.85fr", gap: 24, height: CONTENT_HEIGHT }}>
        {/* Left panel: P/T compressed timeline (always shown) */}
        <Panel title="Pressure and temperature" eyebrow="Compressed timeline" accent={COLORS.cyan} style={{ height: "100%" }}>
          <div style={{ padding: "14px 16px 18px" }}>
            <svg width={830} height={580} viewBox="0 0 830 580">
              <rect x={pressureChart.x} y={pressureChart.y} width={pressureChart.w} height={pressureChart.h} rx={22} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
              <rect x={tempChart.x} y={tempChart.y} width={tempChart.w} height={tempChart.h} rx={22} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
              <rect
                x={pxFor(overnightStartMinute)}
                y={pressureChart.y}
                width={pxFor(overnightEndMinute) - pxFor(overnightStartMinute)}
                height={pressureChart.h + 52 + tempChart.h}
                rx={18}
                fill={rgba("#242742", 0.42)}
              />
              <line x1={pxFor(pumpMarkerMinute)} x2={pxFor(pumpMarkerMinute)} y1={pressureChart.y} y2={tempChart.y + tempChart.h} stroke={rgba(COLORS.amber, 0.65)} strokeDasharray="12 8" />

              {pressureEvolved ? (
                <>
                  <path d={pressurePathD} fill="none" stroke={rgba(COLORS.cyan, 0.14)} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={pressureEvolved.strokeDasharray} strokeDashoffset={pressureEvolved.strokeDashoffset} />
                  <path d={pressurePathD} fill="none" stroke={COLORS.cyan} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.7)})` }} strokeDasharray={pressureEvolved.strokeDasharray} strokeDashoffset={pressureEvolved.strokeDashoffset} />
                </>
              ) : null}

              {tempEvolved ? (
                <>
                  <path d={tempPathD} fill="none" stroke={rgba(COLORS.amber, 0.16)} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={tempEvolved.strokeDasharray} strokeDashoffset={tempEvolved.strokeDashoffset} />
                  <path d={tempPathD} fill="none" stroke={COLORS.amber} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.amber, 0.45)})` }} strokeDasharray={tempEvolved.strokeDasharray} strokeDashoffset={tempEvolved.strokeDashoffset} />
                </>
              ) : null}

              <text x={pressureChart.x + 14} y={pressureChart.y + 28} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={17}>
                Pressure (kPa)
              </text>
              <text x={tempChart.x + 14} y={tempChart.y + 28} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={17}>
                Temperature (C)
              </text>
              <text x={pxFor(overnightStartMinute) + 30} y={pressureChart.y + 38} fill={rgba(COLORS.text, 0.56)} fontFamily={FONTS.mono} fontSize={15}>
                OVERNIGHT
              </text>
              <text x={pxFor(pumpMarkerMinute) + 10} y={pressureChart.y + 28} fill={rgba(COLORS.amber, 0.78)} fontFamily={FONTS.mono} fontSize={15}>
                PUMP
              </text>

              {lastPressurePoint ? (
                <g opacity={pressurePointVisible(lastPressurePoint.data.minute)}>
                  <circle cx={lastPressurePoint.x} cy={lastPressurePoint.y} r={7} fill={COLORS.white} stroke={COLORS.cyan} strokeWidth={3} />
                  <line x1={lastPressurePoint.x} x2={lastPressurePoint.x - 80} y1={lastPressurePoint.y} y2={lastPressurePoint.y - 30} stroke={rgba(COLORS.cyan, 0.72)} />
                  <text x={lastPressurePoint.x - 220} y={lastPressurePoint.y - 38} fill={COLORS.cyan} fontFamily={FONTS.mono} fontSize={16}>
                    LATE TAIL 1810 kPa
                  </text>
                </g>
              ) : null}

              {lastPressurePoint ? (
                <GlowBurst
                  triggerFrame={SHORT_BEATS.lastPressure}
                  cx={lastPressurePoint.x}
                  cy={lastPressurePoint.y}
                  color={COLORS.cyan}
                  restRadius={14}
                />
              ) : null}

              {badPoints.map((point) => (
                <g key={point.timeLabel} opacity={pressurePointVisible(point.minute)}>
                  <line x1={pxFor(point.minute) - 8} x2={pxFor(point.minute) + 8} y1={pressureChart.y + 26} y2={pressureChart.y + 42} stroke={rgba(COLORS.crimson, 0.9)} strokeWidth={3} />
                  <line x1={pxFor(point.minute) + 8} x2={pxFor(point.minute) - 8} y1={pressureChart.y + 26} y2={pressureChart.y + 42} stroke={rgba(COLORS.crimson, 0.9)} strokeWidth={3} />
                </g>
              ))}
            </svg>
          </div>
        </Panel>

        {/* Right panel: crossfade from metric cards to gas kick chart */}
        <div style={{ position: "relative", height: "100%" }}>
          {/* First half: metric cards */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "grid",
              gap: 16,
              alignContent: "start",
              opacity: metricsPhaseOpacity,
            }}
          >
            <MetricCard label="Steady state" value={<NumberCounter target={STEADY_STATE_KPA} from={2000} suffix=" kPa" startFrame={360} />} accent={COLORS.cyan} />
            <MetricCard label="Overnight avg" value={<NumberCounter target={OVERNIGHT_AVG_KPA} from={1900} suffix=" kPa" startFrame={420} />} accent={COLORS.green} />
            <MetricCard label="Late Apr 3" value={<NumberCounter target={LATE_PM_KPA} from={1800} suffix=" kPa" startFrame={SHORT_BEATS.lastPressure} />} accent={COLORS.cyan} />
          </div>

          {/* Second half: gas kick zoom */}
          <div style={{ position: "absolute", inset: 0, opacity: gasPhaseOpacity }}>
            <Panel title="Gas kick zoom" eyebrow="Apr 3 11:02-11:59" accent={COLORS.crimson} style={{ height: "100%" }}>
              <div style={{ padding: "14px 16px 18px" }}>
                <svg width={680} height={480} viewBox="0 0 680 480">
                  <rect x={gasChart.x} y={gasChart.y} width={gasChart.w} height={gasChart.h} rx={22} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
                  {[19.1, 19.2, 19.3, 19.4].map((value) => (
                    <line
                      key={value}
                      x1={gasChart.x}
                      x2={gasChart.x + gasChart.w}
                      y1={gasYFor(value)}
                      y2={gasYFor(value)}
                      stroke={rgba(COLORS.grid, 0.28)}
                      strokeDasharray="4 12"
                    />
                  ))}

                  {gasEvolved ? (
                    <>
                      <path d={gasPathD} fill="none" stroke={rgba(COLORS.cyan, 0.16)} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={gasEvolved.strokeDasharray} strokeDashoffset={gasEvolved.strokeDashoffset} />
                      <path d={gasPathD} fill="none" stroke={COLORS.cyan} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.7)})` }} strokeDasharray={gasEvolved.strokeDasharray} strokeDashoffset={gasEvolved.strokeDashoffset} />
                    </>
                  ) : null}

                  <text x={gasChart.x + 14} y={gasChart.y + 28} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={16}>
                    In-band pressure (BAR)
                  </text>

                  {goodGasPoints.map((point) => (
                    <circle
                      key={point.timeLabel}
                      cx={gasXFor(point.minute)}
                      cy={gasYFor(point.pressureBar)}
                      r={5}
                      fill={COLORS.white}
                      stroke={COLORS.cyan}
                      strokeWidth={2}
                      opacity={gasPointVisible(point.minute)}
                    />
                  ))}

                  {badGasPoint ? (
                    <g opacity={gasPointVisible(50)}>
                      <line x1={gasXFor(badGasPoint.minute)} x2={gasXFor(badGasPoint.minute)} y1={gasChart.y + 24} y2={gasChart.y + gasChart.h} stroke={rgba(COLORS.crimson, 0.72)} strokeDasharray="12 10" />
                      <circle cx={gasXFor(badGasPoint.minute)} cy={gasChart.y + 36} r={16 + pulse * 8} fill={rgba(COLORS.crimson, 0.2 + pulse * 0.12)} />
                      <line x1={gasXFor(badGasPoint.minute) - 14} x2={gasXFor(badGasPoint.minute) + 14} y1={gasChart.y + 20} y2={gasChart.y + 52} stroke={COLORS.crimson} strokeWidth={3} />
                      <line x1={gasXFor(badGasPoint.minute) + 14} x2={gasXFor(badGasPoint.minute) - 14} y1={gasChart.y + 20} y2={gasChart.y + 52} stroke={COLORS.crimson} strokeWidth={3} />
                      <text x={gasXFor(badGasPoint.minute) - 110} y={gasChart.y + 72} fill={COLORS.crimson} fontFamily={FONTS.mono} fontSize={16}>
                        11:52 CRC FAIL
                      </text>
                    </g>
                  ) : null}

                  {badGasPoint ? (
                    <>
                      <GlowBurst
                        triggerFrame={SHORT_BEATS.crcFail}
                        cx={gasXFor(badGasPoint.minute)}
                        cy={gasChart.y + 36}
                        color={COLORS.crimson}
                        restRadius={20}
                      />
                      <GlowBurst
                        triggerFrame={SHORT_BEATS.crcRecovery}
                        cx={gasXFor(57)}
                        cy={gasYFor(19.34)}
                        color={COLORS.green}
                        restRadius={14}
                      />
                    </>
                  ) : null}
                </svg>

                {/* Recovery metric below the gas chart */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 8, padding: "0 4px" }}>
                  <MetricCard
                    label="Corrupted"
                    value={<NumberCounter target={168.65} from={19} suffix=" BAR" decimals={2} startFrame={SHORT_BEATS.crcFail} duration={12} />}
                    accent={COLORS.crimson}
                  />
                  <MetricCard
                    label="Recovery"
                    value={<NumberCounter target={7} from={0} suffix=" min" startFrame={SHORT_BEATS.crcRecovery} />}
                    accent={COLORS.green}
                  />
                </div>
              </div>
            </Panel>
          </div>
        </div>
      </div>
    </SceneFrame>
  );
}

/* ── Scene 4: Payoff (660-900, 8s) ─────────────────────────────────── */

function PayoffScene(props: { state: SceneWindowState }): React.ReactElement {
  return (
    <SceneFrame state={props.state}>
      <div
        style={{
          ...panelStyle(COLORS.green),
          width: "100%",
          height: CONTENT_HEIGHT,
          padding: "40px 42px",
          display: "grid",
          gridTemplateColumns: "1.06fr 0.94fr",
          gap: 28,
          background: `radial-gradient(circle at 78% 18%, ${rgba(COLORS.green, 0.16)} 0%, ${rgba(COLORS.panel, 0.96)} 28%, ${rgba(COLORS.bg, 0.98)} 70%)`,
        }}
      >
        <div>
          <div
            style={{
              color: rgba(COLORS.green, 0.86),
              fontFamily: FONTS.mono,
              fontSize: 15,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              marginBottom: 14,
            }}
          >
            Customer-facing close
          </div>
          <div
            style={{
              color: COLORS.white,
              fontFamily: FONTS.title,
              fontSize: 72,
              lineHeight: 0.94,
              letterSpacing: "-0.06em",
              fontWeight: 500,
              maxWidth: 820,
            }}
          >
            Run 3 turned marginal signal into a believable operations story.
          </div>
          <div style={{ display: "grid", gap: 14, marginTop: 28 }}>
            {PAYOFF_BULLETS.map((bullet, index) => {
              const reveal = stepIn(props.state.localFrame, 8 + index * 6);
              return (
                <div
                  key={bullet}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "14px 1fr",
                    gap: 14,
                    alignItems: "start",
                    opacity: reveal,
                    transform: `translateY(${(1 - reveal) * 14}px)`,
                  }}
                >
                  <div
                    style={{
                      width: 14,
                      height: 14,
                      borderRadius: 999,
                      marginTop: 8,
                      background: COLORS.green,
                      boxShadow: `0 0 18px ${rgba(COLORS.green, 0.5)}`,
                    }}
                  />
                  <div
                    style={{
                      color: COLORS.text,
                      fontFamily: FONTS.body,
                      fontSize: 24,
                      lineHeight: 1.4,
                    }}
                  >
                    {bullet}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div style={{ display: "grid", gap: 14, alignContent: "start" }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 14 }}>
            {PAYOFF_METRICS.map((metric, index) => (
              <MetricCard
                key={metric.label}
                label={metric.label}
                value={metric.value}
                accent={index === 2 ? COLORS.green : index === 3 ? COLORS.crimson : COLORS.cyan}
                style={{
                  opacity: stepIn(props.state.localFrame, 4 + index * 5),
                  transform: `translateY(${(1 - stepIn(props.state.localFrame, 4 + index * 5)) * 16}px)`,
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </SceneFrame>
  );
}

/* ── Root composition ──────────────────────────────────────────────── */

export const Run3StoryboardShort: React.FC = () => {
  const frame = useCurrentFrame();

  const sceneStates = {
    intro: getSceneWindow(frame, RUN3_SHORT_SCENES.intro),
    depthPull: getSceneWindow(frame, RUN3_SHORT_SCENES.depthPull),
    pumpGas: getSceneWindow(frame, RUN3_SHORT_SCENES.pumpGas),
    payoff: getSceneWindow(frame, RUN3_SHORT_SCENES.payoff),
  };

  const activeKey =
    SHORT_SCENE_META.find(
      (scene) => frame >= RUN3_SHORT_SCENES[scene.key][0] && frame < RUN3_SHORT_SCENES[scene.key][1],
    )?.key ?? "intro";

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 18% 10%, ${rgba(COLORS.bgGrad, 0.95)} 0%, ${COLORS.bg} 58%)`,
        fontFamily: FONTS.body,
      }}
    >
      {/* Subtle grid overlay */}
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${rgba(COLORS.grid, 0.14)} 1px, transparent 1px), linear-gradient(90deg, ${rgba(COLORS.grid, 0.14)} 1px, transparent 1px)`,
          backgroundSize: "120px 120px",
          opacity: 0.28,
        }}
      />

      <HeaderBar />
      <IntroScene state={sceneStates.intro} />
      <DepthPullScene state={sceneStates.depthPull} />
      <PumpGasScene state={sceneStates.pumpGas} />

      {/* Crimson edge flash at CRC fail moment */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% 50%, transparent 55%, ${rgba(COLORS.crimson, 0.12)} 100%)`,
          opacity: interpolate(
            frame,
            [SHORT_BEATS.crcFail - 2, SHORT_BEATS.crcFail + 4, SHORT_BEATS.crcFail + 14],
            [0, 0.08, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
          ),
          pointerEvents: "none" as const,
        }}
      />

      <PayoffScene state={sceneStates.payoff} />
      <SceneStrip activeKey={activeKey} />
    </AbsoluteFill>
  );
};
