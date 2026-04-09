import React from "react";
import { evolvePath } from "@remotion/paths";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame } from "remotion";
import { COLORS, FONTS, FPS } from "../theme";
import {
  GAS_KICK_POINTS,
  INTERVENTION_EVENTS,
  LATE_PM_AVG_RMS,
  LATE_PM_KPA,
  OVERNIGHT_AVG_KPA,
  PAYOFF_BULLETS,
  PAYOFF_METRICS,
  PRESSURE_TEMP_POINTS,
  RELIABILITY_STAGES,
  RUN3_RAW_PACKET_SOURCE,
  RUN3_SCENES,
  RUN3_SOURCE_MANIFEST,
  SIGNAL_DEPTH_POINTS,
  STEADY_STATE_KPA,
  TOTAL_RUN3_MINUTES,
  compressedTimeRatio,
  gasKickMarkerMinute,
  overnightEndMinute,
  overnightStartMinute,
  pumpMarkerMinute,
} from "./run3Data";

const HEADER_HEIGHT = 136;
const FOOTER_HEIGHT = 86;
const CONTENT_TOP = HEADER_HEIGHT + 18;
const CONTENT_LEFT = 96;
const CONTENT_WIDTH = 1728;
const CONTENT_HEIGHT = 1080 - CONTENT_TOP - FOOTER_HEIGHT - 28;

type SceneKey = keyof typeof RUN3_SCENES;
type SceneRange = (typeof RUN3_SCENES)[SceneKey];

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

const SCENE_META: Array<{ key: SceneKey; label: string; color: string }> = [
  { key: "intro", label: "Run 3", color: COLORS.cyan },
  { key: "depth", label: "Depth", color: COLORS.green },
  { key: "interventions", label: "Recovery", color: COLORS.amber },
  { key: "pump", label: "Pump", color: COLORS.cyan },
  { key: "gas", label: "Gas kick", color: COLORS.crimson },
  { key: "payoff", label: "Payoff", color: COLORS.green },
];

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

function polyline(points: XYPoint[]): string {
  return points.map((point) => `${point.x},${point.y}`).join(" ");
}

function getSceneWindow(frame: number, range: SceneRange): SceneWindowState {
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

function panelStyle(accent: string = COLORS.cyan): React.CSSProperties {
  return {
    background: `linear-gradient(180deg, ${rgba(COLORS.panel, 0.96)} 0%, ${rgba(COLORS.bg, 0.96)} 100%)`,
    border: `1px solid ${rgba(accent, 0.2)}`,
    boxShadow: `0 18px 50px ${rgba(COLORS.bg, 0.45)}, inset 0 0 0 1px ${rgba(COLORS.white, 0.03)}`,
    borderRadius: 28,
    overflow: "hidden",
  };
}

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
  value: string;
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
        <div
          style={{
            color: rgba(COLORS.cyan, 0.72),
            fontFamily: FONTS.mono,
            fontSize: 14,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            marginTop: 10,
          }}
        >
          Source-locked to approved storyboard, timeline, narrative, and raw packet tail
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

function SceneStrip(props: {
  activeKey: SceneKey;
}): React.ReactElement {
  return (
    <div
      style={{
        position: "absolute",
        left: CONTENT_LEFT,
        right: CONTENT_LEFT,
        bottom: 22,
        display: "grid",
        gridTemplateColumns: `repeat(${SCENE_META.length}, minmax(0, 1fr))`,
        gap: 14,
      }}
    >
      {SCENE_META.map((scene) => {
        const active = scene.key === props.activeKey;
        return (
          <div
            key={scene.key}
            style={{
              ...panelStyle(scene.color),
              padding: "14px 16px",
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
                fontSize: 13,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
                marginBottom: 8,
              }}
            >
              {scene.key}
            </div>
            <div
              style={{
                color: active ? scene.color : COLORS.text,
                fontFamily: FONTS.title,
                fontSize: 28,
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

function AnnotationBox(props: {
  title: string;
  body: string;
  accent: string;
  style?: React.CSSProperties;
}): React.ReactElement {
  return (
    <div
      style={{
        ...panelStyle(props.accent),
        padding: "16px 18px",
        background: `linear-gradient(180deg, ${rgba(COLORS.bgGrad, 0.94)} 0%, ${rgba(COLORS.bg, 0.96)} 100%)`,
        ...props.style,
      }}
    >
      <div
        style={{
          color: props.accent,
          fontFamily: FONTS.mono,
          fontSize: 13,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          marginBottom: 8,
        }}
      >
        {props.title}
      </div>
      <div
        style={{
          color: COLORS.text,
          fontFamily: FONTS.body,
          fontSize: 19,
          lineHeight: 1.4,
        }}
      >
        {props.body}
      </div>
    </div>
  );
}

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
            Definitive deployment story
          </div>
          <div
            style={{
              color: COLORS.white,
              fontFamily: FONTS.title,
              fontSize: 92,
              lineHeight: 0.92,
              letterSpacing: "-0.06em",
              fontWeight: 500,
              marginTop: 18,
              maxWidth: 860,
            }}
          >
            Operational proof from the first WellFi run that held up in the noise.
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
            This version stays out of the app layer and tells the customer-safe story:
            the link weakened through fluid, the field team reopened it, and the run
            still captured pump behavior plus the gas-kick disruption.
          </div>

          <svg
            width={920}
            height={420}
            viewBox="0 0 920 420"
            style={{ position: "absolute", left: -20, bottom: -10 }}
          >
            <defs>
              <linearGradient id="intro-line" x1="0" x2="1" y1="0" y2="1">
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
              stroke="url(#intro-line)"
              strokeWidth={8}
              strokeLinecap="round"
              style={{ filter: `drop-shadow(0 0 18px ${rgba(COLORS.cyan, 0.7)})` }}
            />
            {[{ x: 190, y: 338, color: COLORS.green }, { x: 514, y: 138, color: COLORS.amber }, { x: 806, y: 94, color: COLORS.cyan }].map(
              (point, index) => (
                <circle
                  key={`${point.x}-${point.y}`}
                  cx={point.x}
                  cy={point.y}
                  r={10 + Math.max(0, stepIn(props.state.localFrame, 10 + index * 10) * 10)}
                  fill={rgba(point.color, 0.2)}
                />
              ),
            )}
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
                opacity: stepIn(props.state.localFrame, 12 + index * 8),
                transform: `translateY(${(1 - stepIn(props.state.localFrame, 12 + index * 8)) * 22}px)`,
              }}
            />
          ))}
          <AnnotationBox
            title="Evidence pack"
            body={`${RUN3_SOURCE_MANIFEST.length} locked sources drive this cut. The late Apr 3 pressure tail is backed by the raw clean packet log, not just the trimmed narrative summary.`}
            accent={COLORS.amber}
          />
        </div>
      </div>
    </SceneFrame>
  );
}

function DepthScene(props: { state: SceneWindowState }): React.ReactElement {
  const chart = { x: 80, y: 110, w: 820, h: 520 };
  const maxDepth = 920;
  const xFor = (dbv: number): number => chart.x + ((dbv + 110) / 85) * chart.w;
  const yFor = (md: number): number => chart.y + (md / maxDepth) * chart.h;
  const revealCount = clamp(
    Math.ceil(interpolate(props.state.progress, [0.1, 0.82], [2, SIGNAL_DEPTH_POINTS.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })),
    2,
    SIGNAL_DEPTH_POINTS.length,
  );
  const visiblePoints = SIGNAL_DEPTH_POINTS.slice(0, revealCount).map((point) => ({
    x: xFor(point.signalDbv),
    y: yFor(point.md),
    data: point,
  }));
  // Build SVG path from visible points for evolvePath animation
  const depthPathD = visiblePoints.length >= 2
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

  const depthEvolved = depthPathD ? evolvePath(traceProgress, depthPathD) : null;

  // Each point appears when the trace reaches its normalized position
  const pointVisible = (index: number): number => {
    const pointProgress = index / Math.max(1, visiblePoints.length - 1);
    return traceProgress >= pointProgress ? 1 : 0;
  };

  const noiseX = xFor(-95);
  const pullY = yFor(822.82);
  const peakPoint = visiblePoints.find((point) => point.data.label === "Peak signal");
  const fluidPoint = visiblePoints.find((point) => point.data.label === "Hit fluid");
  const bottomPoint = visiblePoints[visiblePoints.length - 1];

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
              {fluidPoint ? (
                <g opacity={pointVisible(2)}>
                  <line x1={fluidPoint.x} x2={fluidPoint.x + 112} y1={fluidPoint.y} y2={fluidPoint.y - 16} stroke={rgba("#a78bfa", 0.7)} />
                  <text x={fluidPoint.x + 120} y={fluidPoint.y - 20} fill="#a78bfa" fontFamily={FONTS.mono} fontSize={18}>
                    HIT FLUID 1.20 BAR
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
              <text x={chart.x - 40} y={chart.y + chart.h + 8} fill={rgba(COLORS.text, 0.72)} fontFamily={FONTS.body} fontSize={19} transform={`rotate(-90 ${chart.x - 40} ${chart.y + chart.h + 8})`}>
                Depth (m MD)
              </text>
            </svg>
          </div>
        </Panel>

        <div style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <MetricCard label="Peak signal" value="-37 dBV" accent={COLORS.green} />
          <MetricCard label="Fluid contact" value="1.20 BAR" accent="#a78bfa" />
          <MetricCard label="On bottom" value="-100 dBV" accent={COLORS.crimson} />
          <AnnotationBox
            title="Why this matters"
            body="The signal was strongest near 161 m MD, then collapsed once the tool entered fluid. By bottom, the link was still alive but operating below the -95 dBV noise floor."
            accent={COLORS.green}
          />
        </div>
      </div>
    </SceneFrame>
  );
}

function InterventionScene(props: { state: SceneWindowState }): React.ReactElement {
  const accentForEvent = (color: string): string => {
    switch (color) {
      case "green":
        return COLORS.green;
      case "amber":
        return COLORS.amber;
      case "crimson":
        return COLORS.crimson;
      default:
        return COLORS.cyan;
    }
  };

  return (
    <SceneFrame state={props.state}>
      <div style={{ display: "grid", gridTemplateColumns: "1.05fr 0.95fr", gap: 24, height: CONTENT_HEIGHT }}>
        <Panel title="Small surface changes unlocked the link" eyebrow="Field interventions" accent={COLORS.amber} style={{ height: "100%" }}>
          <div style={{ padding: "22px 24px 28px", display: "grid", gap: 18 }}>
            <MetricCard label="Blackout ended" value="84 min" accent={COLORS.amber} tone={COLORS.bgGrad} />
            {INTERVENTION_EVENTS.map((event, index) => {
              const accent = accentForEvent(event.color);
              const reveal = stepIn(props.state.localFrame, 14 + index * 8);
              return (
                <div
                  key={event.title}
                  style={{
                    ...panelStyle(accent),
                    display: "grid",
                    gridTemplateColumns: "158px 1fr",
                    gap: 18,
                    padding: "18px 20px",
                    opacity: reveal,
                    transform: `translateX(${(1 - reveal) * 24}px)`,
                  }}
                >
                  <div>
                    <div
                      style={{
                        color: accent,
                        fontFamily: FONTS.mono,
                        fontSize: 13,
                        letterSpacing: "0.12em",
                        textTransform: "uppercase",
                        marginBottom: 10,
                      }}
                    >
                      {event.timeLabel}
                    </div>
                    <div
                      style={{
                        color: COLORS.white,
                        fontFamily: FONTS.title,
                        fontSize: 28,
                        lineHeight: 1,
                        fontWeight: 500,
                      }}
                    >
                      {event.metric}
                    </div>
                  </div>
                  <div>
                    <div
                      style={{
                        color: COLORS.white,
                        fontFamily: FONTS.title,
                        fontSize: 30,
                        fontWeight: 500,
                        letterSpacing: "-0.03em",
                        marginBottom: 8,
                      }}
                    >
                      {event.title}
                    </div>
                    <div
                      style={{
                        color: COLORS.text,
                        fontFamily: FONTS.body,
                        fontSize: 20,
                        lineHeight: 1.45,
                      }}
                    >
                      {event.detail}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Panel>

        <Panel title="Reliability climbed as the setup improved" eyebrow="CRC clean windows" accent={COLORS.green} style={{ height: "100%" }}>
          <div style={{ padding: "24px 26px 26px", display: "grid", gap: 18 }}>
            {RELIABILITY_STAGES.map((stage, index) => {
              const accent =
                stage.crcPassRate >= 90 ? COLORS.green : stage.crcPassRate >= 60 ? COLORS.amber : COLORS.crimson;
              const reveal = stepIn(props.state.localFrame, 10 + index * 7);
              return (
                <div
                  key={stage.label}
                  style={{
                    opacity: reveal,
                    transform: `translateY(${(1 - reveal) * 18}px)`,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: 10,
                    }}
                  >
                    <div
                      style={{
                        color: COLORS.white,
                        fontFamily: FONTS.title,
                        fontSize: 28,
                        fontWeight: 500,
                      }}
                    >
                      {stage.label}
                    </div>
                    <div
                      style={{
                        color: accent,
                        fontFamily: FONTS.mono,
                        fontSize: 22,
                        fontWeight: 600,
                      }}
                    >
                      {stage.crcPassRate}% CRC
                    </div>
                  </div>
                  <div
                    style={{
                      height: 18,
                      borderRadius: 999,
                      background: rgba(COLORS.grid, 0.9),
                      overflow: "hidden",
                      marginBottom: 8,
                    }}
                  >
                    <div
                      style={{
                        width: `${stage.crcPassRate}%`,
                        height: "100%",
                        borderRadius: 999,
                        background: `linear-gradient(90deg, ${rgba(accent, 0.8)} 0%, ${accent} 100%)`,
                        boxShadow: `0 0 20px ${rgba(accent, 0.32)}`,
                      }}
                    />
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      color: COLORS.text,
                      fontFamily: FONTS.body,
                      fontSize: 18,
                    }}
                  >
                    <span>{stage.note}</span>
                    <span>{stage.meanRms.toFixed(1)}% mean RMS</span>
                  </div>
                </div>
              );
            })}

            <AnnotationBox
              title="Customer-safe framing"
              body={`The win is operational, not theatrical: better antenna placement plus a 1-joint pull moved the run from marginal to repeatable. Late Apr 3 RMS still averaged ${LATE_PM_AVG_RMS.toFixed(1)}%.`}
              accent={COLORS.green}
            />
          </div>
        </Panel>
      </div>
    </SceneFrame>
  );
}

function PumpScene(props: { state: SceneWindowState }): React.ReactElement {
  const pressureChart = { x: 66, y: 96, w: 1060, h: 292 };
  const tempChart = { x: 66, y: 444, w: 1060, h: 196 };
  const cleanPoints = PRESSURE_TEMP_POINTS.filter((point) => !point.corrupted);
  const badPoints = PRESSURE_TEMP_POINTS.filter((point) => point.corrupted);
  const xFor = (minute: number): number => pressureChart.x + compressedTimeRatio(minute) * pressureChart.w;
  const pressureYFor = (kpa: number): number =>
    pressureChart.y + ((2200 - kpa) / (2200 - -100)) * pressureChart.h;
  const tempYFor = (temp: number): number => tempChart.y + ((28 - temp) / 30) * tempChart.h;
  const pressureLine = cleanPoints.map((point) => ({ x: xFor(point.minute), y: pressureYFor(point.pressureKpa), data: point }));
  const tempLine = cleanPoints.map((point) => ({ x: xFor(point.minute), y: tempYFor(point.tempC), data: point }));
  const lastPoint = pressureLine[pressureLine.length - 1];
  const coldSlug = tempLine.find((point) => point.data.timeLabel === "18:47");

  // Build SVG path strings for evolvePath
  const pressurePathD = pressureLine.length >= 2
    ? `M ${pressureLine[0].x} ${pressureLine[0].y} ` +
      pressureLine.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
    : "";

  const tempPathD = tempLine.length >= 2
    ? `M ${tempLine[0].x} ${tempLine[0].y} ` +
      tempLine.slice(1).map((p) => `L ${p.x} ${p.y}`).join(" ")
    : "";

  // Pressure draws left-to-right over the scene
  const pressureTrace = interpolate(
    props.state.progress,
    [0.0, 0.87],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
  );

  // Temperature follows pressure with a slight delay
  const tempTrace = interpolate(
    props.state.progress,
    [0.07, 0.87],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
  );

  const pressureEvolved = pressurePathD ? evolvePath(pressureTrace, pressurePathD) : null;
  const tempEvolved = tempPathD ? evolvePath(tempTrace, tempPathD) : null;

  // Callouts appear when the trace passes their minute position
  const pressurePointVisible = (minute: number): number => {
    const normalizedPos = compressedTimeRatio(minute);
    return pressureTrace >= normalizedPos ? 1 : 0;
  };

  return (
    <SceneFrame state={props.state}>
      <div style={{ display: "grid", gridTemplateColumns: "1.28fr 0.72fr", gap: 24, height: CONTENT_HEIGHT }}>
        <Panel title="Pressure and temperature tell the operating story" eyebrow="Compressed timeline" accent={COLORS.cyan} style={{ height: "100%" }}>
          <div style={{ padding: "18px 20px 22px" }}>
            <svg width={1160} height={660} viewBox="0 0 1160 660">
              <rect x={pressureChart.x} y={pressureChart.y} width={pressureChart.w} height={pressureChart.h} rx={28} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
              <rect x={tempChart.x} y={tempChart.y} width={tempChart.w} height={tempChart.h} rx={28} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
              <rect
                x={xFor(overnightStartMinute)}
                y={pressureChart.y}
                width={xFor(overnightEndMinute) - xFor(overnightStartMinute)}
                height={pressureChart.h + 56 + tempChart.h}
                rx={22}
                fill={rgba("#242742", 0.42)}
              />
              <line x1={xFor(pumpMarkerMinute)} x2={xFor(pumpMarkerMinute)} y1={pressureChart.y} y2={tempChart.y + tempChart.h} stroke={rgba(COLORS.amber, 0.65)} strokeDasharray="12 8" />
              {pressureEvolved ? (
                <>
                  <path
                    d={pressurePathD}
                    fill="none"
                    stroke={rgba(COLORS.cyan, 0.14)}
                    strokeWidth={18}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={pressureEvolved.strokeDasharray}
                    strokeDashoffset={pressureEvolved.strokeDashoffset}
                  />
                  <path
                    d={pressurePathD}
                    fill="none"
                    stroke={COLORS.cyan}
                    strokeWidth={5}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.7)})` }}
                    strokeDasharray={pressureEvolved.strokeDasharray}
                    strokeDashoffset={pressureEvolved.strokeDashoffset}
                  />
                </>
              ) : null}
              {tempEvolved ? (
                <>
                  <path
                    d={tempPathD}
                    fill="none"
                    stroke={rgba(COLORS.amber, 0.16)}
                    strokeWidth={16}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={tempEvolved.strokeDasharray}
                    strokeDashoffset={tempEvolved.strokeDashoffset}
                  />
                  <path
                    d={tempPathD}
                    fill="none"
                    stroke={COLORS.amber}
                    strokeWidth={4}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.amber, 0.45)})` }}
                    strokeDasharray={tempEvolved.strokeDasharray}
                    strokeDashoffset={tempEvolved.strokeDashoffset}
                  />
                </>
              ) : null}
              <text x={pressureChart.x + 18} y={pressureChart.y + 34} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={20}>
                Pressure (kPa absolute)
              </text>
              <text x={tempChart.x + 18} y={tempChart.y + 34} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={20}>
                Temperature (C)
              </text>
              <text x={xFor(overnightStartMinute) + 40} y={pressureChart.y + 44} fill={rgba(COLORS.text, 0.56)} fontFamily={FONTS.mono} fontSize={18}>
                OVERNIGHT
              </text>
              <text x={xFor(pumpMarkerMinute) + 12} y={pressureChart.y + 34} fill={rgba(COLORS.amber, 0.78)} fontFamily={FONTS.mono} fontSize={18}>
                PUMP
              </text>
              {lastPoint ? (
                <g opacity={pressurePointVisible(lastPoint.data.minute)}>
                  <circle cx={lastPoint.x} cy={lastPoint.y} r={8} fill={COLORS.white} stroke={COLORS.cyan} strokeWidth={4} />
                  <line x1={lastPoint.x} x2={lastPoint.x - 92} y1={lastPoint.y} y2={lastPoint.y - 38} stroke={rgba(COLORS.cyan, 0.72)} />
                  <text x={lastPoint.x - 268} y={lastPoint.y - 46} fill={COLORS.cyan} fontFamily={FONTS.mono} fontSize={18}>
                    LATE RAW TAIL 1810 kPa
                  </text>
                </g>
              ) : null}
              {coldSlug ? (
                <g opacity={pressurePointVisible(coldSlug.data.minute)}>
                  <circle cx={coldSlug.x} cy={coldSlug.y} r={7} fill={COLORS.white} stroke={COLORS.amber} strokeWidth={3} />
                  <line x1={coldSlug.x} x2={coldSlug.x + 90} y1={coldSlug.y} y2={coldSlug.y + 34} stroke={rgba(COLORS.amber, 0.7)} />
                  <text x={coldSlug.x + 98} y={coldSlug.y + 42} fill={COLORS.amber} fontFamily={FONTS.mono} fontSize={18}>
                    COLD SLUG 15.2 C
                  </text>
                </g>
              ) : null}
              {badPoints.map((point) => (
                <g key={point.timeLabel} opacity={pressurePointVisible(point.minute)}>
                  <line x1={xFor(point.minute) - 10} x2={xFor(point.minute) + 10} y1={pressureChart.y + 30} y2={pressureChart.y + 50} stroke={rgba(COLORS.crimson, 0.9)} strokeWidth={3} />
                  <line x1={xFor(point.minute) + 10} x2={xFor(point.minute) - 10} y1={pressureChart.y + 30} y2={pressureChart.y + 50} stroke={rgba(COLORS.crimson, 0.9)} strokeWidth={3} />
                </g>
              ))}
            </svg>
          </div>
        </Panel>

        <div style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <MetricCard label="Steady state" value={`${STEADY_STATE_KPA} kPa`} accent={COLORS.cyan} />
          <MetricCard label="Overnight avg" value={`${OVERNIGHT_AVG_KPA} kPa`} accent={COLORS.green} />
          <MetricCard label="Late Apr 3" value={`${LATE_PM_KPA} kPa`} accent={COLORS.cyan} />
          <AnnotationBox
            title="Pump readout"
            body="Temperature drops from 24.8 C into the 21.6 C operating band after pump start. The late Apr 3 clean packets keep falling, which is why the approved storyboard ends with the line still moving."
            accent={COLORS.amber}
          />
          <AnnotationBox
            title="Conflict handled"
            body={`Narrative docs stop at 14:50 and 18.46 BAR. The approved storyboard generator keeps the clean packet tail through 16:29 and reaches 18.10 BAR. This cut follows the raw packet-backed endpoint.`}
            accent={COLORS.cyan}
          />
        </div>
      </div>
    </SceneFrame>
  );
}

function GasKickScene(props: { state: SceneWindowState }): React.ReactElement {
  const chart = { x: 76, y: 128, w: 900, h: 430 };
  const goodPoints = GAS_KICK_POINTS.filter((point) => point.good);
  const badPoint = GAS_KICK_POINTS.find((point) => !point.good);
  const xFor = (minute: number): number => chart.x + (minute / 57) * chart.w;
  const yFor = (pressure: number): number => chart.y + ((19.45 - pressure) / (19.45 - 19.08)) * chart.h;
  const pulse = 0.5 + 0.5 * Math.sin(props.state.localFrame / 3);
  const goodLine = goodPoints.map((point) => ({ x: xFor(point.minute), y: yFor(point.pressureBar) }));

  // Build SVG path for evolvePath animation
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

  // Points appear when trace reaches them (57 is the max minute in gas kick data)
  const gasPointVisible = (minute: number): number => {
    const normalizedPos = minute / 57;
    return gasTrace >= normalizedPos ? 1 : 0;
  };

  return (
    <SceneFrame state={props.state}>
      <div style={{ display: "grid", gridTemplateColumns: "1.08fr 0.92fr", gap: 24, height: CONTENT_HEIGHT }}>
        <Panel title="The gas kick was seen and classified correctly" eyebrow="Apr 3 zoom" accent={COLORS.crimson} style={{ height: "100%" }}>
          <div style={{ padding: "18px 20px 22px" }}>
            <svg width={1020} height={650} viewBox="0 0 1020 650">
              <rect x={chart.x} y={chart.y} width={chart.w} height={chart.h} rx={28} fill={rgba(COLORS.bg, 0.65)} stroke={rgba(COLORS.grid, 0.7)} />
              {[19.1, 19.2, 19.3, 19.4].map((value) => (
                <line
                  key={value}
                  x1={chart.x}
                  x2={chart.x + chart.w}
                  y1={yFor(value)}
                  y2={yFor(value)}
                  stroke={rgba(COLORS.grid, 0.28)}
                  strokeDasharray="4 12"
                />
              ))}
              {gasEvolved ? (
                <>
                  <path
                    d={gasPathD}
                    fill="none"
                    stroke={rgba(COLORS.cyan, 0.16)}
                    strokeWidth={18}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={gasEvolved.strokeDasharray}
                    strokeDashoffset={gasEvolved.strokeDashoffset}
                  />
                  <path
                    d={gasPathD}
                    fill="none"
                    stroke={COLORS.cyan}
                    strokeWidth={5}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ filter: `drop-shadow(0 0 14px ${rgba(COLORS.cyan, 0.7)})` }}
                    strokeDasharray={gasEvolved.strokeDasharray}
                    strokeDashoffset={gasEvolved.strokeDashoffset}
                  />
                </>
              ) : null}
              <text x={chart.x + 18} y={chart.y + 34} fill={rgba(COLORS.text, 0.74)} fontFamily={FONTS.body} fontSize={20}>
                Pressure at sensor depth stayed in-band during the kick
              </text>
              {goodPoints.map((point) => (
                <circle
                  key={point.timeLabel}
                  cx={xFor(point.minute)}
                  cy={yFor(point.pressureBar)}
                  r={6}
                  fill={COLORS.white}
                  stroke={COLORS.cyan}
                  strokeWidth={3}
                  opacity={gasPointVisible(point.minute)}
                />
              ))}
              {badPoint ? (
                <g opacity={gasPointVisible(50)}>
                  <line x1={xFor(badPoint.minute)} x2={xFor(badPoint.minute)} y1={chart.y + 28} y2={chart.y + chart.h} stroke={rgba(COLORS.crimson, 0.72)} strokeDasharray="12 10" />
                  <circle cx={xFor(badPoint.minute)} cy={chart.y + 40} r={20 + pulse * 10} fill={rgba(COLORS.crimson, 0.2 + pulse * 0.12)} />
                  <line x1={xFor(badPoint.minute) - 18} x2={xFor(badPoint.minute) + 18} y1={chart.y + 22} y2={chart.y + 58} stroke={COLORS.crimson} strokeWidth={4} />
                  <line x1={xFor(badPoint.minute) + 18} x2={xFor(badPoint.minute) - 18} y1={chart.y + 22} y2={chart.y + 58} stroke={COLORS.crimson} strokeWidth={4} />
                  <text x={xFor(badPoint.minute) - 134} y={chart.y + 84} fill={COLORS.crimson} fontFamily={FONTS.mono} fontSize={18}>
                    11:52 CRC FAIL
                  </text>
                </g>
              ) : null}
            </svg>
          </div>
        </Panel>

        <div style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <MetricCard label="Normal band" value="19.1-19.4 BAR" accent={COLORS.cyan} />
          <MetricCard label="Corrupted packet" value="168.65 BAR" accent={COLORS.crimson} />
          <MetricCard label="Recovery" value="11:59 clean" accent={COLORS.green} />
          <AnnotationBox
            title="Correct interpretation"
            body="The sensor did not record a real 168.65 BAR pressure spike. The packet failed CRC, RMS jumped to 78%, and the next clean packet returned to 19.34 BAR seven minutes later."
            accent={COLORS.crimson}
          />
          <AnnotationBox
            title="Operator context"
            body="Field notes describe a slow pump and noisy signal during the kick. That is consistent with EM path disruption above the sensor, not with a believable downhole pressure jump at tool depth."
            accent={COLORS.amber}
          />
        </div>
      </div>
    </SceneFrame>
  );
}

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
              fontSize: 78,
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
                      fontSize: 26,
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
              />
            ))}
          </div>
          <AnnotationBox
            title="Validation note"
            body={`This animation is safe to show because every hero beat is tied either to the approved storyboard image or to the raw packet log at ${RUN3_RAW_PACKET_SOURCE}.`}
            accent={COLORS.green}
          />
        </div>
      </div>
    </SceneFrame>
  );
}

export const Run3Storyboard: React.FC = () => {
  const frame = useCurrentFrame();
  const sceneStates = {
    intro: getSceneWindow(frame, RUN3_SCENES.intro),
    depth: getSceneWindow(frame, RUN3_SCENES.depth),
    interventions: getSceneWindow(frame, RUN3_SCENES.interventions),
    pump: getSceneWindow(frame, RUN3_SCENES.pump),
    gas: getSceneWindow(frame, RUN3_SCENES.gas),
    payoff: getSceneWindow(frame, RUN3_SCENES.payoff),
  };
  const activeKey =
    SCENE_META.find((scene) => frame >= RUN3_SCENES[scene.key][0] && frame < RUN3_SCENES[scene.key][1])?.key ?? "intro";

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 18% 10%, ${rgba(COLORS.bgGrad, 0.95)} 0%, ${COLORS.bg} 58%)`,
        fontFamily: FONTS.body,
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${rgba(COLORS.grid, 0.14)} 1px, transparent 1px), linear-gradient(90deg, ${rgba(COLORS.grid, 0.14)} 1px, transparent 1px)`,
          backgroundSize: "120px 120px",
          opacity: 0.28,
        }}
      />
      <HeaderBar />
      <IntroScene state={sceneStates.intro} />
      <DepthScene state={sceneStates.depth} />
      <InterventionScene state={sceneStates.interventions} />
      <PumpScene state={sceneStates.pump} />
      <GasKickScene state={sceneStates.gas} />
      <PayoffScene state={sceneStates.payoff} />
      <SceneStrip activeKey={activeKey} />
    </AbsoluteFill>
  );
};
