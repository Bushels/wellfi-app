export const RUN3_DURATION_FRAMES = 1500;

export const RUN3_SCENES = {
  intro: [0, 120],
  depth: [120, 390],
  interventions: [390, 600],
  pump: [600, 900],
  gas: [900, 1200],
  payoff: [1200, 1500],
} as const;

export const RUN3_SHORT_DURATION_FRAMES = 900;

export const RUN3_SHORT_SCENES = {
  intro: [0, 90],
  depthPull: [90, 330],
  pumpGas: [330, 660],
  payoff: [660, 900],
} as const;

// Hero beat frames — when the trace reaches each hero data point.
// GlowBurst components trigger relative to these.
export const HERO_BEATS = {
  peakSignal: { scene: "depth" as const, frame: 195 },
  pulledJoint: { scene: "interventions" as const, frame: 440 },
  lastPressure: { scene: "pump" as const, frame: 855 },
  crcFail: { scene: "gas" as const, frame: 1050 },
  crcRecovery: { scene: "gas" as const, frame: 1080 },
} as const;

export const RUN3_SOURCE_MANIFEST = [
  "analysis/wellfi-run3-deployment-story.png",
  "analysis/plot_run3_story.py",
  "analysis/run3-complete-timeline.md",
  "analysis/run3-narrative.md",
  "analysis/design-philosophy.md",
  "petro-roundtable/knowledge/wellfi-telemetry.md",
] as const;

export const RUN3_RAW_PACKET_SOURCE =
  "G:\\My Drive\\Belle Industries\\WellFi\\Obsidian\\102161808317W509\\Logs\\packetmessages_April2_2026.txt";

export interface SignalDepthPoint {
  label: string;
  timeLabel: string;
  md: number;
  signalDbv: number;
  pressureBar?: number;
  tempC?: number;
  note: string;
}

export const SIGNAL_DEPTH_POINTS: SignalDepthPoint[] = [
  {
    label: "First signal",
    timeLabel: "Apr 2 11:22",
    md: 113.6,
    signalDbv: -51,
    note: "Receiver first sees the tool during run-in.",
  },
  {
    label: "Peak signal",
    timeLabel: "Apr 2 11:37",
    md: 160.9,
    signalDbv: -37,
    note: "Best coupling point in the cased section.",
  },
  {
    label: "Hit fluid",
    timeLabel: "Apr 2 11:55",
    md: 482.4,
    signalDbv: -55,
    pressureBar: 1.2,
    tempC: 12.0,
    note: "Pressure jumps as the tool enters the fluid column.",
  },
  {
    label: "Deep in fluid",
    timeLabel: "Apr 2 12:10",
    md: 662.1,
    signalDbv: -88,
    pressureBar: 15.67,
    note: "Fluid attenuation drives the signal toward the floor.",
  },
  {
    label: "On bottom",
    timeLabel: "Apr 2 12:28",
    md: 832.3,
    signalDbv: -96,
    pressureBar: 20.79,
    tempC: 22.4,
    note: "Telemetry reaches the noise-floor limit on bottom.",
  },
  {
    label: "Noise floor",
    timeLabel: "Apr 2 12:37",
    md: 832.3,
    signalDbv: -100,
    note: "The link is technically alive, but barely usable.",
  },
] as const;

export interface InterventionEvent {
  title: string;
  timeLabel: string;
  metric: string;
  detail: string;
  color: "crimson" | "amber" | "cyan" | "green";
}

export const INTERVENTION_EVENTS: InterventionEvent[] = [
  {
    title: "On-lease stake move",
    timeLabel: "Apr 2 13:03-14:19",
    metric: "0 packets in 76 min",
    detail: "The on-lease location performed worse than the original off-lease stake.",
    color: "crimson",
  },
  {
    title: "Pulled 1 joint",
    timeLabel: "Apr 2 14:23",
    metric: "84 min blackout ended",
    detail: "The first packet back arrives immediately after the joint pull.",
    color: "amber",
  },
  {
    title: "20 m cable extension",
    timeLabel: "Apr 2 16:12 onward",
    metric: "12.4-26.2% RMS",
    detail: "The best Apr 2 signal window follows the cable and stake optimization.",
    color: "cyan",
  },
  {
    title: "Apr 3 operating windows",
    timeLabel: "Apr 3 AM + PM",
    metric: "94-100% CRC",
    detail: "Run 3 settles into reliable three-minute telemetry windows.",
    color: "green",
  },
] as const;

export interface ReliabilityStage {
  label: string;
  crcPassRate: number;
  meanRms: number;
  note: string;
}

export const RELIABILITY_STAGES: ReliabilityStage[] = [
  {
    label: "On bottom",
    crcPassRate: 40,
    meanRms: 43.2,
    note: "2 of 5 packets clean",
  },
  {
    label: "Post-pull",
    crcPassRate: 43,
    meanRms: 38.5,
    note: "Communication restored",
  },
  {
    label: "Best Apr 2 window",
    crcPassRate: 100,
    meanRms: 19.5,
    note: "17:17-17:32",
  },
  {
    label: "Apr 3 morning",
    crcPassRate: 94,
    meanRms: 28.3,
    note: "18 packets",
  },
  {
    label: "Apr 3 afternoon",
    crcPassRate: 100,
    meanRms: 25.8,
    note: "Late Apr 3 tail to 16:29",
  },
] as const;

export interface PressureTempPoint {
  minute: number;
  timeLabel: string;
  pressureKpa: number;
  tempC: number;
  label?: string;
  corrupted?: boolean;
}

export const TOTAL_RUN3_MINUTES = 1740;

export const PRESSURE_TEMP_POINTS: PressureTempPoint[] = [
  { minute: 0, timeLabel: "Apr 2 11:29", pressureKpa: -49, tempC: 3.2, label: "Cold start" },
  { minute: 27, timeLabel: "11:56", pressureKpa: 123, tempC: 12.0, label: "Hit fluid" },
  { minute: 39, timeLabel: "12:08", pressureKpa: 1350, tempC: 16.8 },
  { minute: 51, timeLabel: "12:20", pressureKpa: 2012, tempC: 20.8 },
  { minute: 60, timeLabel: "12:29", pressureKpa: 2079, tempC: 22.4, label: "On bottom" },
  { minute: 174, timeLabel: "14:23", pressureKpa: 2075, tempC: 24.8, label: "Pulled 1 joint" },
  { minute: 354, timeLabel: "17:23", pressureKpa: 2075, tempC: 24.8, label: "Best signal window" },
  { minute: 438, timeLabel: "18:47", pressureKpa: 2051, tempC: 15.2, label: "Cold slug" },
  { minute: 465, timeLabel: "19:14", pressureKpa: 2037, tempC: 21.6, label: "Early drawdown" },
  { minute: 1407, timeLabel: "Apr 3 10:56", pressureKpa: 1951, tempC: 21.6, label: "Morning resume" },
  { minute: 1428, timeLabel: "11:17", pressureKpa: 1927, tempC: 21.6, label: "Gas kick starts" },
  { minute: 1463, timeLabel: "11:52", pressureKpa: 16865, tempC: 114.4, label: "CRC fail", corrupted: true },
  { minute: 1470, timeLabel: "11:59", pressureKpa: 1934, tempC: 21.6, label: "Recovered" },
  { minute: 1617, timeLabel: "Apr 3 14:29", pressureKpa: 1851, tempC: 20.8, label: "Afternoon return" },
  { minute: 1641, timeLabel: "14:50", pressureKpa: 1846, tempC: 20.8, label: "Early afternoon tail" },
  { minute: 1665, timeLabel: "15:14", pressureKpa: 1832, tempC: 20.8, label: "Still declining" },
  { minute: 1740, timeLabel: "16:29", pressureKpa: 1810, tempC: 20.8, label: "Last clean packet" },
] as const;

export const GAS_KICK_POINTS = [
  { minute: 0, timeLabel: "11:02", pressureBar: 19.34, good: true },
  { minute: 6, timeLabel: "11:08", pressureBar: 19.10, good: true },
  { minute: 9, timeLabel: "11:11", pressureBar: 19.15, good: true },
  { minute: 12, timeLabel: "11:14", pressureBar: 19.27, good: true },
  { minute: 15, timeLabel: "11:17", pressureBar: 19.27, good: true },
  { minute: 18, timeLabel: "11:20", pressureBar: 19.32, good: true },
  { minute: 21, timeLabel: "11:23", pressureBar: 19.25, good: true },
  { minute: 30, timeLabel: "11:32", pressureBar: 19.33, good: true },
  { minute: 33, timeLabel: "11:35", pressureBar: 19.40, good: true },
  { minute: 36, timeLabel: "11:38", pressureBar: 19.40, good: true },
  { minute: 39, timeLabel: "11:41", pressureBar: 19.25, good: true },
  { minute: 42, timeLabel: "11:44", pressureBar: 19.35, good: true },
  { minute: 45, timeLabel: "11:47", pressureBar: 19.22, good: true },
  { minute: 48, timeLabel: "11:50", pressureBar: 19.38, good: true },
  { minute: 50, timeLabel: "11:52", pressureBar: 168.65, good: false },
  { minute: 57, timeLabel: "11:59", pressureBar: 19.34, good: true },
] as const;

export const PAYOFF_BULLETS = [
  "Pulling 1 joint ended an 84-minute blackout and reopened the link.",
  "Cable and stake tuning created 94-100% CRC windows on Apr 3.",
  "Pressure kept declining to 18.10 BAR in the late Apr 3 raw packet tail.",
  "The gas-kick disruption was flagged, classified as corruption, and recovered in 7 minutes.",
] as const;

export const PAYOFF_METRICS = [
  { label: "Peak signal", value: "-37 dBV" },
  { label: "Late pressure", value: "1810 kPa" },
  { label: "Best CRC window", value: "100%" },
  { label: "Gas-kick recovery", value: "7 min" },
] as const;

export const STEADY_STATE_KPA = 2069;
export const OVERNIGHT_AVG_KPA = 1928;
export const LATE_PM_KPA = 1810;
export const LATE_PM_AVG_RMS = 25.8;

interface TimeSegment {
  sourceStart: number;
  sourceEnd: number;
  targetStart: number;
  targetEnd: number;
}

const TIME_SEGMENTS: TimeSegment[] = [
  { sourceStart: 0, sourceEnd: 480, targetStart: 0, targetEnd: 0.44 },
  { sourceStart: 480, sourceEnd: 1407, targetStart: 0.44, targetEnd: 0.60 },
  { sourceStart: 1407, sourceEnd: TOTAL_RUN3_MINUTES, targetStart: 0.60, targetEnd: 1 },
] as const;

export const overnightStartMinute = 480;
export const overnightEndMinute = 1407;
export const pumpMarkerMinute = 369;
export const gasKickMarkerMinute = 1428;

export function compressedTimeRatio(minutes: number): number {
  const bounded = Math.max(0, Math.min(minutes, TOTAL_RUN3_MINUTES));
  const segment =
    TIME_SEGMENTS.find((candidate) => bounded <= candidate.sourceEnd) ??
    TIME_SEGMENTS[TIME_SEGMENTS.length - 1];
  const localSpan = segment.sourceEnd - segment.sourceStart || 1;
  const localProgress = (bounded - segment.sourceStart) / localSpan;
  return segment.targetStart + localProgress * (segment.targetEnd - segment.targetStart);
}
