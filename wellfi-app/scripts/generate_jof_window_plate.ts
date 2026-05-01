import fs from 'node:fs';
import path from 'node:path';
import {
  getSurveyedTrajectoryPoints,
  interpolateTrajectoryPoint,
  parseSurveyCsv,
  type InterpolatedTrajectoryPoint,
  type TrajectoryPoint,
} from '../src/lib/directionalSurvey.ts';

interface PlotPadding {
  left: number;
  right: number;
  top: number;
  bottom: number;
}

interface PlotTransform {
  plotLeft: number;
  plotTop: number;
  plotWidth: number;
  plotHeight: number;
  mapX: (value: number) => number;
  mapY: (value: number) => number;
}

function parseArgs(argv: string[]): Record<string, string> {
  const args: Record<string, string> = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) {
      args[key] = 'true';
      continue;
    }
    args[key] = value;
    index += 1;
  }
  return args;
}

function usage(): never {
  console.error(
    'Usage: npx tsx scripts/generate_jof_window_plate.ts --input <csv> --output <svg> --stb-top-md <md> --stb-bottom-md <md> --joint-length-m <m> --jof-min <n> --jof-max <n> --density-kgm3 <kgm3> [--port-offset-m <m>] [--well-name <name>]',
  );
  process.exit(1);
}

function escapeXml(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function extent(values: readonly number[], padding = 0, minimumSpan = 1): [number, number] {
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  if (!Number.isFinite(minValue) || !Number.isFinite(maxValue)) {
    return [0, minimumSpan];
  }

  if (maxValue - minValue < minimumSpan) {
    const midpoint = (minValue + maxValue) / 2;
    const halfSpan = minimumSpan / 2;
    return [midpoint - halfSpan - padding, midpoint + halfSpan + padding];
  }

  return [minValue - padding, maxValue + padding];
}

function niceStep(span: number, targetTickCount: number): number {
  if (span <= 0) return 1;
  const roughStep = span / Math.max(1, targetTickCount);
  const magnitude = 10 ** Math.floor(Math.log10(roughStep));
  const residual = roughStep / magnitude;

  if (residual >= 5) return 5 * magnitude;
  if (residual >= 2) return 2 * magnitude;
  return magnitude;
}

function buildTicks(minValue: number, maxValue: number, targetTickCount: number): number[] {
  const step = niceStep(maxValue - minValue, targetTickCount);
  const start = Math.ceil(minValue / step) * step;
  const ticks: number[] = [];

  for (let value = start; value <= maxValue + step * 0.5; value += step) {
    ticks.push(Number(value.toFixed(3)));
  }

  return ticks.length > 0 ? ticks : [Number(minValue.toFixed(2)), Number(maxValue.toFixed(2))];
}

function createPlotTransform(
  xDomain: [number, number],
  yDomain: [number, number],
  width: number,
  height: number,
  padding: PlotPadding,
): PlotTransform {
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;
  const dataWidth = Math.max(xDomain[1] - xDomain[0], 1);
  const dataHeight = Math.max(yDomain[1] - yDomain[0], 1);
  const scale = Math.min(innerWidth / dataWidth, innerHeight / dataHeight);
  const plotWidth = dataWidth * scale;
  const plotHeight = dataHeight * scale;
  const plotLeft = padding.left + (innerWidth - plotWidth) / 2;
  const plotTop = padding.top + (innerHeight - plotHeight) / 2;

  return {
    plotLeft,
    plotTop,
    plotWidth,
    plotHeight,
    mapX: (value) => plotLeft + (value - xDomain[0]) * scale,
    mapY: (value) => plotTop + (value - yDomain[0]) * scale,
  };
}

function buildPath(
  points: readonly Pick<TrajectoryPoint, 'vertical_section_m' | 'tvd_m'>[],
  transform: PlotTransform,
  offsetX = 0,
  offsetY = 0,
): string {
  return points
    .map((point, index) => {
      const x = offsetX + transform.mapX(point.vertical_section_m);
      const y = offsetY + transform.mapY(point.tvd_m);
      return `${index === 0 ? 'M' : 'L'}${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(' ');
}

function formatTick(value: number): string {
  if (Math.abs(value) >= 100) return `${Math.round(value)}`;
  if (Math.abs(value) >= 10) return value.toFixed(1);
  return value.toFixed(2);
}

function hydrostaticPressureKPa(deltaTvdM: number, densityKgM3: number): number {
  return (densityKgM3 * 9.81 * deltaTvdM) / 1000;
}

function roundTo(value: number, digits: number): number {
  return Number(value.toFixed(digits));
}

function formatFixed(value: number, digits: number): string {
  return value.toFixed(digits);
}

function requirePoint(point: InterpolatedTrajectoryPoint | null, label: string): InterpolatedTrajectoryPoint {
  if (!point) {
    throw new Error(`Unable to interpolate ${label}.`);
  }
  return point;
}

function sampleSegment(
  points: readonly TrajectoryPoint[],
  startMdM: number,
  endMdM: number,
  verticalSectionAzimuthDeg: number | null,
  samples = 24,
): InterpolatedTrajectoryPoint[] {
  const leftMd = Math.min(startMdM, endMdM);
  const rightMd = Math.max(startMdM, endMdM);
  const segmentPoints: InterpolatedTrajectoryPoint[] = [];

  for (let index = 0; index <= samples; index += 1) {
    const md = leftMd + ((rightMd - leftMd) * index) / samples;
    const point = interpolateTrajectoryPoint(points, md, {
      verticalSectionAzimuthDeg,
    });
    if (point) segmentPoints.push(point);
  }

  return segmentPoints;
}

function textLine(
  x: number,
  y: number,
  text: string,
  options?: {
    fill?: string;
    size?: number;
    weight?: number | string;
  },
): string {
  const fill = options?.fill ?? '#cbd5e1';
  const size = options?.size ?? 20;
  const weight = options?.weight ?? 500;
  return `<text x="${x}" y="${y}" fill="${fill}" font-size="${size}" font-family="Segoe UI, Arial, sans-serif" font-weight="${weight}">${escapeXml(text)}</text>`;
}

function estimateTextWidth(text: string, size: number): number {
  return text.length * size * 0.56;
}

function wrapText(text: string, maxWidth: number, size: number): string[] {
  const words = text.split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let currentLine = '';

  for (const word of words) {
    const candidate = currentLine ? `${currentLine} ${word}` : word;
    if (!currentLine || estimateTextWidth(candidate, size) <= maxWidth) {
      currentLine = candidate;
      continue;
    }
    lines.push(currentLine);
    currentLine = word;
  }

  if (currentLine) lines.push(currentLine);
  return lines.length > 0 ? lines : [''];
}

function textBlock(
  x: number,
  y: number,
  text: string,
  options?: {
    fill?: string;
    size?: number;
    weight?: number | string;
    maxWidth?: number;
    lineHeight?: number;
  },
): { svg: string; height: number } {
  const fill = options?.fill ?? '#cbd5e1';
  const size = options?.size ?? 20;
  const weight = options?.weight ?? 500;
  const maxWidth = options?.maxWidth ?? Number.POSITIVE_INFINITY;
  const lineHeight = options?.lineHeight ?? size * 1.25;
  const lines = Number.isFinite(maxWidth) ? wrapText(text, maxWidth, size) : [text];
  const tspans = lines
    .map((line, index) => {
      const dy = index === 0 ? 0 : lineHeight;
      return `<tspan x="${x}" dy="${dy}">${escapeXml(line)}</tspan>`;
    })
    .join('');

  return {
    svg: `<text x="${x}" y="${y}" fill="${fill}" font-size="${size}" font-family="Segoe UI, Arial, sans-serif" font-weight="${weight}">${tspans}</text>`,
    height: size + Math.max(0, lines.length - 1) * lineHeight,
  };
}

const args = parseArgs(process.argv.slice(2));
const inputPath = args.input;
const outputPath = args.output;
const wellName = args['well-name'] ?? 'WellFi JOF Window';
const stbTopMd = Number(args['stb-top-md']);
const stbBottomMd = Number(args['stb-bottom-md']);
const portOffsetM = Number(args['port-offset-m'] ?? '1.524');
const jointLengthM = Number(args['joint-length-m']);
const jofMin = Number(args['jof-min']);
const jofMax = Number(args['jof-max']);
const densityKgM3 = Number(args['density-kgm3']);
const atmosphereKPa = Number(args['atmosphere-kpa'] ?? '101.325');

if (
  !inputPath ||
  !outputPath ||
  !Number.isFinite(stbTopMd) ||
  !Number.isFinite(stbBottomMd) ||
  !Number.isFinite(jointLengthM) ||
  !Number.isFinite(jofMin) ||
  !Number.isFinite(jofMax) ||
  !Number.isFinite(densityKgM3)
) {
  usage();
}

if (jofMin <= 0 || jofMax <= 0 || jofMax < jofMin) {
  throw new Error('Invalid JOF range.');
}

const portMd = Number.isFinite(Number(args['port-md'])) ? Number(args['port-md']) : stbBottomMd + portOffsetM;
const survey = parseSurveyCsv(fs.readFileSync(inputPath, 'utf8'));
const surveyedPoints = getSurveyedTrajectoryPoints(survey.points);

const stbTopPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, stbTopMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  'slotted tag bar top',
);
const portPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, portMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  'WellFi pressure port',
);

const shallowFluidMd = stbTopMd - jofMax * jointLengthM;
const deepFluidMd = stbTopMd - jofMin * jointLengthM;
const shallowFluidPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, shallowFluidMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  `${jofMax} JOF fluid top`,
);
const deepFluidPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, deepFluidMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  `${jofMin} JOF fluid top`,
);

const windowSegment = sampleSegment(
  survey.points,
  shallowFluidMd,
  deepFluidMd,
  survey.vertical_section_azimuth_deg,
  30,
);

const pressureLowKPag = hydrostaticPressureKPa(portPoint.tvd_m - deepFluidPoint.tvd_m, densityKgM3);
const pressureHighKPag = hydrostaticPressureKPa(portPoint.tvd_m - shallowFluidPoint.tvd_m, densityKgM3);
const pressureLowKPaA = pressureLowKPag + atmosphereKPa;
const pressureHighKPaA = pressureHighKPag + atmosphereKPa;
const headAtFiveJofTvdM = portPoint.tvd_m - deepFluidPoint.tvd_m;
const headAtTwelveJofTvdM = portPoint.tvd_m - shallowFluidPoint.tvd_m;

const width = 1600;
const height = 980;
const sectionRect = { x: 40, y: 150, width: 980, height: 720 };
const panelRect = { x: 1060, y: 150, width: 500, height: 720 };
const sectionPadding = { left: 86, right: 32, top: 30, bottom: 72 };

const sectionXDomain = extent(
  [
    ...surveyedPoints.map((point) => point.vertical_section_m),
    shallowFluidPoint.vertical_section_m,
    deepFluidPoint.vertical_section_m,
    portPoint.vertical_section_m,
    0,
  ],
  24,
  80,
);
const sectionYDomain = extent(
  [
    0,
    ...surveyedPoints.map((point) => point.tvd_m),
    shallowFluidPoint.tvd_m,
    deepFluidPoint.tvd_m,
    portPoint.tvd_m,
  ],
  18,
  100,
);

const sectionTransform = createPlotTransform(
  sectionXDomain,
  sectionYDomain,
  sectionRect.width,
  sectionRect.height,
  sectionPadding,
);
const sectionPath = buildPath(surveyedPoints, sectionTransform, sectionRect.x, sectionRect.y);
const windowPath = buildPath(windowSegment, sectionTransform, sectionRect.x, sectionRect.y);

const xTicks = buildTicks(sectionXDomain[0], sectionXDomain[1], 5);
const yTicks = buildTicks(sectionYDomain[0], sectionYDomain[1], 7);

const shallowX = sectionTransform.mapX(shallowFluidPoint.vertical_section_m);
const shallowY = sectionTransform.mapY(shallowFluidPoint.tvd_m);
const deepX = sectionTransform.mapX(deepFluidPoint.vertical_section_m);
const deepY = sectionTransform.mapY(deepFluidPoint.tvd_m);
const portX = sectionTransform.mapX(portPoint.vertical_section_m);
const portY = sectionTransform.mapY(portPoint.tvd_m);
const stbX = sectionTransform.mapX(stbTopPoint.vertical_section_m);
const stbY = sectionTransform.mapY(stbTopPoint.tvd_m);

const calloutX = Math.min(portX + 86, sectionRect.width - 300);
const calloutY = Math.max(portY - 146, 88);

const summaryLines = [
  { text: 'Expected kPaa', fill: '#e2e8f0', size: 20, weight: 600, gapAfter: 6 },
  {
    text: `${formatFixed(pressureLowKPaA, 1)} to ${formatFixed(pressureHighKPaA, 1)} kPaa`,
    fill: '#7dd3fc',
    size: 29,
    weight: 700,
    gapAfter: 6,
  },
  { text: 'Gauge equivalent', fill: '#e2e8f0', size: 18, weight: 700, gapAfter: 8 },
  {
    text: `${formatFixed(pressureLowKPag, 1)} to ${formatFixed(pressureHighKPag, 1)} kPag`,
    fill: '#cbd5e1',
    size: 15,
    weight: 500,
    gapAfter: 20,
  },
  { text: 'Head at WellFi port (TVD)', fill: '#e2e8f0', size: 18, weight: 700, gapAfter: 8 },
  { text: `${jofMin} JOF: ${formatFixed(headAtFiveJofTvdM, 2)} m TVD`, fill: '#cbd5e1', size: 15, gapAfter: 6 },
  { text: `${jofMax} JOF: ${formatFixed(headAtTwelveJofTvdM, 2)} m TVD`, fill: '#cbd5e1', size: 15, gapAfter: 16 },
  { text: 'WellFi port', fill: '#e2e8f0', size: 18, weight: 700, gapAfter: 8 },
  { text: `${roundTo(portMd, 2)} mKB | ${roundTo(portPoint.tvd_m, 2)} mTVD`, fill: '#7dd3fc', size: 15, weight: 600, gapAfter: 16 },
  { text: 'Assumptions', fill: '#e2e8f0', size: 18, weight: 700, gapAfter: 8 },
  { text: `JOF from top of slotted tag bar at ${stbTopMd.toFixed(2)} mKB`, fill: '#94a3b8', size: 14, gapAfter: 6 },
  { text: `Joint length: ${jointLengthM.toFixed(3)} m per joint`, fill: '#94a3b8', size: 14, gapAfter: 6 },
  { text: `Fluid density: ${roundTo(densityKgM3, 0)} kg/m^3`, fill: '#94a3b8', size: 14, gapAfter: 6 },
];

let summaryY = 192;
const summarySvg = summaryLines
  .map((line) => {
    const block = textBlock(panelRect.x + 28, summaryY, line.text, {
      fill: line.fill,
      size: line.size,
      weight: line.weight,
      maxWidth: panelRect.width - 56,
      lineHeight: line.size * 1.22,
    });
    summaryY += block.height + (line.gapAfter ?? 8);
    return block.svg;
  })
  .join('\n');

const portCalloutTitle = textBlock(sectionRect.x + calloutX + 14, sectionRect.y + calloutY + 22, 'WellFi pressure port', {
  fill: '#f8fafc',
  size: 15,
  weight: 700,
  maxWidth: 252,
});
const portCalloutDepth = textBlock(
  sectionRect.x + calloutX + 14,
  sectionRect.y + calloutY + 46,
  `${roundTo(portMd, 2)} mKB | TVD ${roundTo(portPoint.tvd_m, 2)} m from KB`,
  {
    fill: '#94a3b8',
    size: 13,
    weight: 500,
    maxWidth: 252,
  },
);

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
  <defs>
    <linearGradient id="pageBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#08111f" />
      <stop offset="100%" stop-color="#030712" />
    </linearGradient>
    <linearGradient id="wellPath" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7dd3fc" />
      <stop offset="100%" stop-color="#facc15" />
    </linearGradient>
    <linearGradient id="windowPath" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22c55e" />
      <stop offset="100%" stop-color="#4ade80" />
    </linearGradient>
    <clipPath id="sectionClip">
      <rect x="${sectionRect.x}" y="${sectionRect.y}" width="${sectionRect.width}" height="${sectionRect.height}" rx="24" />
    </clipPath>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#pageBg)" />
  <rect x="20" y="20" width="${width - 40}" height="${height - 40}" rx="24" fill="none" stroke="rgba(148,163,184,0.14)" />

  ${textLine(40, 62, `${wellName} | WellFi JOF Window`, { fill: '#f8fafc', size: 38, weight: 700 })}
  ${textLine(
    40,
    96,
    'Hydrostatic operating window built from the final survey and the WellFi pressure-port depth.',
    { fill: '#94a3b8', size: 17, weight: 500 },
  )}

  ${textLine(sectionRect.x, 132, 'Section View', { fill: '#e2e8f0', size: 19, weight: 700 })}
  <rect x="${sectionRect.x}" y="${sectionRect.y}" width="${sectionRect.width}" height="${sectionRect.height}" rx="24" fill="rgba(15,23,42,0.44)" stroke="rgba(148,163,184,0.14)" />
  <rect x="${panelRect.x}" y="${panelRect.y}" width="${panelRect.width}" height="${panelRect.height}" rx="24" fill="rgba(15,23,42,0.56)" stroke="rgba(148,163,184,0.14)" />

  ${yTicks
    .map((tick) => {
      const y = sectionRect.y + sectionTransform.mapY(tick);
      return `<line x1="${sectionRect.x + sectionTransform.plotLeft}" x2="${sectionRect.x + sectionTransform.plotLeft + sectionTransform.plotWidth}" y1="${y}" y2="${y}" stroke="rgba(148,163,184,0.08)" stroke-dasharray="4 10" />
      <text x="${sectionRect.x + 14}" y="${y + 4}" fill="#64748b" font-size="11" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    })
    .join('\n')}
  ${xTicks
    .map((tick) => {
      const x = sectionRect.x + sectionTransform.mapX(tick);
      return `<line x1="${x}" x2="${x}" y1="${sectionRect.y + sectionTransform.plotTop}" y2="${sectionRect.y + sectionTransform.plotTop + sectionTransform.plotHeight}" stroke="rgba(148,163,184,0.08)" stroke-dasharray="4 10" />
      <text x="${x}" y="${sectionRect.y + sectionRect.height - 18}" text-anchor="middle" fill="#64748b" font-size="11" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    })
    .join('\n')}
  ${textLine(sectionRect.x + sectionRect.width / 2 - 110, sectionRect.y + sectionRect.height - 6, 'VERTICAL SECTION (m)', {
    fill: '#94a3b8',
    size: 14,
    weight: 600,
  })}
  <text transform="translate(${sectionRect.x + 18} ${sectionRect.y + sectionRect.height / 2 + 70}) rotate(-90)" fill="#94a3b8" font-size="14" font-family="Segoe UI, Arial, sans-serif" font-weight="600">TVD FROM KB (m)</text>

  <g clip-path="url(#sectionClip)">
    <path d="${sectionPath}" fill="none" stroke="url(#wellPath)" stroke-width="6" opacity="0.12" stroke-linecap="round" stroke-linejoin="round" />
    <path d="${sectionPath}" fill="none" stroke="url(#wellPath)" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" />
    <path d="${windowPath}" fill="none" stroke="url(#windowPath)" stroke-width="6.4" stroke-linecap="round" stroke-linejoin="round" />
  </g>

  <circle cx="${sectionRect.x + shallowX}" cy="${sectionRect.y + shallowY}" r="6" fill="#22c55e" />
  <circle cx="${sectionRect.x + deepX}" cy="${sectionRect.y + deepY}" r="6" fill="#4ade80" />
  <circle cx="${sectionRect.x + stbX}" cy="${sectionRect.y + stbY}" r="5" fill="#f59e0b" />
  <circle cx="${sectionRect.x + portX}" cy="${sectionRect.y + portY}" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2" />

  ${textLine(sectionRect.x + shallowX + 10, sectionRect.y + shallowY - 18, `${jofMax} JOF top: ${roundTo(shallowFluidMd, 2)} mKB`, {
    fill: '#bbf7d0',
    size: 14,
    weight: 600,
  })}
  ${textLine(sectionRect.x + deepX - 42, sectionRect.y + deepY - 10, `${jofMin} JOF top: ${roundTo(deepFluidMd, 2)} mKB`, {
    fill: '#dcfce7',
    size: 14,
    weight: 600,
  })}
  ${textLine(sectionRect.x + stbX - 18, sectionRect.y + stbY + 24, `STB top: ${stbTopMd.toFixed(2)} mKB`, {
    fill: '#fed7aa',
    size: 14,
    weight: 600,
  })}

  <rect x="${sectionRect.x + calloutX}" y="${sectionRect.y + calloutY}" width="272" height="66" rx="16" fill="rgba(2,6,23,0.86)" stroke="rgba(56,189,248,0.44)" />
  ${portCalloutTitle.svg}
  ${portCalloutDepth.svg}
  <line x1="${sectionRect.x + portX}" y1="${sectionRect.y + portY}" x2="${sectionRect.x + calloutX}" y2="${sectionRect.y + calloutY + 34}" stroke="rgba(56,189,248,0.55)" stroke-width="1.5" />

  ${summarySvg}

  ${textLine(
    40,
    930,
    'Adjacent-well BHP helps with shut-in / reservoir context. It is not needed to estimate the normal 5 to 12 JOF operating band.',
    { fill: '#64748b', size: 14, weight: 500 },
  )}
</svg>`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, svg, 'utf8');
console.log(outputPath);
