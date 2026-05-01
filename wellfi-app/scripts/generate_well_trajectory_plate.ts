import fs from 'node:fs';
import path from 'node:path';
import {
  getLastSurveyedTrajectoryPoint,
  getProjectedTrajectoryPoints,
  getSurveyedTrajectoryPoints,
  interpolateTrajectoryPoint,
  parseSurveyCsv,
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
  invertY: boolean,
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
    mapY: (value) => (invertY ? plotTop + (yDomain[1] - value) * scale : plotTop + (value - yDomain[0]) * scale),
  };
}

function buildPath(
  points: readonly TrajectoryPoint[],
  transform: PlotTransform,
  selectors: { x: (point: TrajectoryPoint) => number; y: (point: TrajectoryPoint) => number },
): string {
  return points
    .map((point, index) => {
      const x = transform.mapX(selectors.x(point));
      const y = transform.mapY(selectors.y(point));
      return `${index === 0 ? 'M' : 'L'}${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(' ');
}

function formatTick(value: number): string {
  if (Math.abs(value) >= 100) return `${Math.round(value)}`;
  if (Math.abs(value) >= 10) return value.toFixed(1);
  return value.toFixed(2);
}

function usage(): never {
  console.error('Usage: npx tsx scripts/generate_well_trajectory_plate.ts --input <csv> --output <svg> [--well-name <name>] [--anchor-md <md>] [--anchor-label <label>] [--tool-bottom-mkb <m>] [--conductive-casing-set-depth-mkb <m>] [--kb-to-gl-m <m>] [--guideline-percent <pct>]');
  process.exit(1);
}

const args = parseArgs(process.argv.slice(2));
const inputPath = args.input;
const outputPath = args.output;
const wellName = args['well-name'] ?? 'Directional Well Plate';
const anchorMd = args['anchor-md'] ? Number(args['anchor-md']) : null;
const anchorLabel = args['anchor-label'] ?? 'Anchor point';
const toolBottomMkb = args['tool-bottom-mkb'] ? Number(args['tool-bottom-mkb']) : null;
const conductiveCasingSetDepthMkb = args['conductive-casing-set-depth-mkb'] ? Number(args['conductive-casing-set-depth-mkb']) : null;
const kbToGlM = args['kb-to-gl-m'] ? Number(args['kb-to-gl-m']) : null;
const guidelinePercent = args['guideline-percent'] ? Number(args['guideline-percent']) : 10;

if (!inputPath || !outputPath) usage();

const rawCsv = fs.readFileSync(inputPath, 'utf8');
const survey = parseSurveyCsv(rawCsv);
const surveyedPoints = getSurveyedTrajectoryPoints(survey.points);
const projectedPoints = getProjectedTrajectoryPoints(survey.points);
const lastSurveyPoint = getLastSurveyedTrajectoryPoint(survey.points);
const projectedTailPoints = projectedPoints.length > 0 && lastSurveyPoint ? [lastSurveyPoint, ...projectedPoints] : [];
const anchorPoint =
  anchorMd != null
    ? interpolateTrajectoryPoint(survey.points, anchorMd, {
        verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
      })
    : null;

const width = 1600;
const height = 980;
const sectionRect = { x: 40, y: 190, width: 930, height: 560 };
const planRect = { x: 1000, y: 190, width: 560, height: 420 };

const sectionPadding = { left: 88, right: 26, top: 28, bottom: 62 };
const planPadding = { left: 64, right: 24, top: 24, bottom: 52 };

const sectionXDomain = extent([...survey.points.map((point) => point.vertical_section_m), anchorPoint?.vertical_section_m ?? 0], 24, 80);
const sectionYDomain = extent([...survey.points.map((point) => point.tvd_m), anchorPoint?.tvd_m ?? 0], 22, 80);
const planXDomain = extent([...survey.points.map((point) => point.easting_offset_m), anchorPoint?.easting_offset_m ?? 0, 0], 28, 80);
const planYDomain = extent([...survey.points.map((point) => point.northing_offset_m), anchorPoint?.northing_offset_m ?? 0, 0], 28, 80);

const sectionTransform = createPlotTransform(sectionXDomain, sectionYDomain, sectionRect.width, sectionRect.height, sectionPadding, false);
const planTransform = createPlotTransform(planXDomain, planYDomain, planRect.width, planRect.height, planPadding, true);

const sectionPath = buildPath(surveyedPoints, sectionTransform, {
  x: (point) => point.vertical_section_m,
  y: (point) => point.tvd_m,
});
const sectionProjectionPath =
  projectedTailPoints.length > 1
    ? buildPath(projectedTailPoints, sectionTransform, {
        x: (point) => point.vertical_section_m,
        y: (point) => point.tvd_m,
      })
    : '';
const planPath = buildPath(surveyedPoints, planTransform, {
  x: (point) => point.easting_offset_m,
  y: (point) => point.northing_offset_m,
});
const planProjectionPath =
  projectedTailPoints.length > 1
    ? buildPath(projectedTailPoints, planTransform, {
        x: (point) => point.easting_offset_m,
        y: (point) => point.northing_offset_m,
      })
    : '';

const sectionXTicks = buildTicks(sectionXDomain[0], sectionXDomain[1], 4);
const sectionYTicks = buildTicks(sectionYDomain[0], sectionYDomain[1], 4);
const planXTicks = buildTicks(planXDomain[0], planXDomain[1], 3);
const planYTicks = buildTicks(planYDomain[0], planYDomain[1], 3);

const anchorSectionX = anchorPoint ? sectionTransform.mapX(anchorPoint.vertical_section_m) : null;
const anchorSectionY = anchorPoint ? sectionTransform.mapY(anchorPoint.tvd_m) : null;
const anchorPlanX = anchorPoint ? planTransform.mapX(anchorPoint.easting_offset_m) : null;
const anchorPlanY = anchorPoint ? planTransform.mapY(anchorPoint.northing_offset_m) : null;
const originPlanX = planTransform.mapX(0);
const originPlanY = planTransform.mapY(0);
const telemetryPlacement =
  anchorMd != null &&
  toolBottomMkb != null &&
  conductiveCasingSetDepthMkb != null &&
  kbToGlM != null &&
  Number.isFinite(toolBottomMkb) &&
  Number.isFinite(conductiveCasingSetDepthMkb) &&
  Number.isFinite(kbToGlM) &&
  conductiveCasingSetDepthMkb > kbToGlM
    ? {
        conductiveCasingSetDepthMkb,
        conductiveCasingLengthGlM: conductiveCasingSetDepthMkb - kbToGlM,
        installPointDistanceFromBottomM: Math.max(0, conductiveCasingSetDepthMkb - anchorMd),
        installPointPercentFromBottom:
          (Math.max(0, conductiveCasingSetDepthMkb - anchorMd) / (conductiveCasingSetDepthMkb - kbToGlM)) * 100,
        toolBottomMkb,
        toolBottomDistanceFromBottomM: Math.max(0, conductiveCasingSetDepthMkb - toolBottomMkb),
        toolBottomPercentFromBottom:
          (Math.max(0, conductiveCasingSetDepthMkb - toolBottomMkb) / (conductiveCasingSetDepthMkb - kbToGlM)) * 100,
        status:
          (Math.max(0, conductiveCasingSetDepthMkb - toolBottomMkb) / (conductiveCasingSetDepthMkb - kbToGlM)) * 100 >= guidelinePercent
            ? 'meets target'
            : (Math.max(0, conductiveCasingSetDepthMkb - anchorMd) / (conductiveCasingSetDepthMkb - kbToGlM)) * 100 >= guidelinePercent
              ? 'borderline'
              : 'below target',
      }
    : null;

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
  <defs>
    <linearGradient id="surveyLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7dd3fc" />
      <stop offset="100%" stop-color="#facc15" />
    </linearGradient>
    <linearGradient id="pageBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#08111f" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#pageBg)" />
  <rect x="18" y="18" width="${width - 36}" height="${height - 36}" rx="22" fill="none" stroke="rgba(148,163,184,0.18)" />

  <text x="40" y="62" fill="#f8fafc" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="700">${escapeXml(wellName)}</text>
  <text x="40" y="94" fill="#94a3b8" font-size="16" font-family="Segoe UI, Arial, sans-serif">Directional survey plate generated from CSV. Solid = surveyed, dashed = projected.</text>

  <rect x="40" y="112" width="320" height="34" rx="17" fill="rgba(15,23,42,0.72)" stroke="rgba(148,163,184,0.18)" />
  <text x="58" y="134" fill="#e2e8f0" font-size="13" font-family="Segoe UI, Arial, sans-serif">Survey header: ${escapeXml(survey.survey_header_uwi ?? 'not found')}</text>
  <rect x="378" y="112" width="260" height="34" rx="17" fill="rgba(15,23,42,0.72)" stroke="rgba(148,163,184,0.18)" />
  <text x="396" y="134" fill="#e2e8f0" font-size="13" font-family="Segoe UI, Arial, sans-serif">Last survey MD: ${survey.last_survey_md_m.toFixed(2)} m</text>
  <rect x="654" y="112" width="320" height="34" rx="17" fill="rgba(15,23,42,0.72)" stroke="rgba(148,163,184,0.18)" />
  <text x="672" y="134" fill="#e2e8f0" font-size="13" font-family="Segoe UI, Arial, sans-serif">Projected TD: ${survey.projected_td_md_m ? `${survey.projected_td_md_m.toFixed(2)} m` : 'none'}</text>

  <g transform="translate(${sectionRect.x} ${sectionRect.y})">
    <text x="0" y="-20" fill="#cbd5e1" font-size="18" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Section View</text>
    <rect x="0" y="0" width="${sectionRect.width}" height="${sectionRect.height}" rx="22" fill="rgba(15,23,42,0.58)" stroke="rgba(148,163,184,0.18)" />
    ${sectionYTicks.map((tick) => {
      const y = sectionTransform.mapY(tick);
      return `<line x1="${sectionTransform.plotLeft}" x2="${sectionTransform.plotLeft + sectionTransform.plotWidth}" y1="${y}" y2="${y}" stroke="rgba(148,163,184,0.12)" stroke-dasharray="4 8" />
      <text x="16" y="${y + 4}" fill="#94a3b8" font-size="11" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    }).join('\n')}
    ${sectionXTicks.map((tick) => {
      const x = sectionTransform.mapX(tick);
      return `<line x1="${x}" x2="${x}" y1="${sectionTransform.plotTop}" y2="${sectionTransform.plotTop + sectionTransform.plotHeight}" stroke="rgba(148,163,184,0.10)" stroke-dasharray="4 8" />
      <text x="${x}" y="${sectionRect.height - 16}" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    }).join('\n')}
    <path d="${sectionPath}" fill="none" stroke="url(#surveyLine)" stroke-width="6" opacity="0.16" stroke-linecap="round" stroke-linejoin="round" />
    <path d="${sectionPath}" fill="none" stroke="url(#surveyLine)" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" />
    ${sectionProjectionPath ? `<path d="${sectionProjectionPath}" fill="none" stroke="#fbbf24" stroke-width="2.2" stroke-dasharray="7 7" stroke-linecap="round" stroke-linejoin="round" />` : ''}
    ${anchorSectionX != null && anchorSectionY != null ? `<line x1="${anchorSectionX}" x2="${anchorSectionX}" y1="${sectionTransform.plotTop}" y2="${sectionTransform.plotTop + sectionTransform.plotHeight}" stroke="rgba(78,195,255,0.7)" stroke-dasharray="6 8" />
    <line x1="${sectionTransform.plotLeft}" x2="${anchorSectionX}" y1="${anchorSectionY}" y2="${anchorSectionY}" stroke="rgba(78,195,255,0.7)" stroke-dasharray="6 8" />
    <circle cx="${anchorSectionX}" cy="${anchorSectionY}" r="10" fill="rgba(78,195,255,0.18)" />
    <circle cx="${anchorSectionX}" cy="${anchorSectionY}" r="4.5" fill="#4ec3ff" />
    <g transform="translate(${Math.min(Math.max(anchorSectionX + 16, 110), sectionRect.width - 288)} ${Math.min(Math.max(anchorSectionY - 92, 36), sectionRect.height - 138)})">
      <rect width="262" height="86" rx="14" fill="rgba(2,6,23,0.88)" stroke="rgba(78,195,255,0.35)" />
      <text x="14" y="23" fill="#f8fafc" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">${escapeXml(anchorLabel)}</text>
      <text x="14" y="42" fill="#94a3b8" font-size="11" font-family="Segoe UI, Arial, sans-serif">${anchorMd?.toFixed(2)} mKB</text>
      <text x="14" y="58" fill="#94a3b8" font-size="11" font-family="Segoe UI, Arial, sans-serif">TVD ${anchorPoint.tvd_m.toFixed(2)} m from KB</text>
      <text x="14" y="74" fill="#7dd3fc" font-size="11" font-family="Segoe UI, Arial, sans-serif">Incl ${anchorPoint.inclination_deg.toFixed(2)}&#176;${telemetryPlacement ? ` | QA ${telemetryPlacement.toolBottomPercentFromBottom.toFixed(2)}% tool` : ''}</text>
    </g>` : ''}
    <text x="${sectionRect.width / 2}" y="${sectionRect.height - 6}" text-anchor="middle" fill="#cbd5e1" font-size="12" font-family="Segoe UI, Arial, sans-serif" letter-spacing="2">VERTICAL SECTION (m)</text>
  </g>

  <g transform="translate(${planRect.x} ${planRect.y})">
    <text x="0" y="-20" fill="#cbd5e1" font-size="18" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Plan View</text>
    <rect x="0" y="0" width="${planRect.width}" height="${planRect.height}" rx="22" fill="rgba(15,23,42,0.58)" stroke="rgba(148,163,184,0.18)" />
    ${planYTicks.map((tick) => {
      const y = planTransform.mapY(tick);
      return `<line x1="${planTransform.plotLeft}" x2="${planTransform.plotLeft + planTransform.plotWidth}" y1="${y}" y2="${y}" stroke="rgba(148,163,184,0.12)" stroke-dasharray="4 7" />
      <text x="10" y="${y + 4}" fill="#94a3b8" font-size="10" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    }).join('\n')}
    ${planXTicks.map((tick) => {
      const x = planTransform.mapX(tick);
      return `<line x1="${x}" x2="${x}" y1="${planTransform.plotTop}" y2="${planTransform.plotTop + planTransform.plotHeight}" stroke="rgba(148,163,184,0.12)" stroke-dasharray="4 7" />
      <text x="${x}" y="${planRect.height - 14}" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="Segoe UI, Arial, sans-serif">${formatTick(tick)}</text>`;
    }).join('\n')}
    <line x1="${originPlanX}" x2="${originPlanX}" y1="${planTransform.plotTop}" y2="${planTransform.plotTop + planTransform.plotHeight}" stroke="rgba(248,250,252,0.18)" stroke-dasharray="3 5" />
    <line x1="${planTransform.plotLeft}" x2="${planTransform.plotLeft + planTransform.plotWidth}" y1="${originPlanY}" y2="${originPlanY}" stroke="rgba(248,250,252,0.18)" stroke-dasharray="3 5" />
    <path d="${planPath}" fill="none" stroke="#4ec3ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    ${planProjectionPath ? `<path d="${planProjectionPath}" fill="none" stroke="#fbbf24" stroke-width="2.2" stroke-dasharray="6 6" stroke-linecap="round" stroke-linejoin="round" />` : ''}
    <circle cx="${originPlanX}" cy="${originPlanY}" r="4" fill="#f8fafc" />
    ${anchorPlanX != null && anchorPlanY != null ? `<circle cx="${anchorPlanX}" cy="${anchorPlanY}" r="7" fill="rgba(78,195,255,0.18)" /><circle cx="${anchorPlanX}" cy="${anchorPlanY}" r="4" fill="#4ec3ff" />` : ''}
    <text x="${planRect.width / 2}" y="${planRect.height - 4}" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="Segoe UI, Arial, sans-serif" letter-spacing="1.5">EASTING OFFSET (m)</text>
  </g>

  <rect x="1000" y="600" width="560" height="300" rx="20" fill="rgba(15,23,42,0.58)" stroke="rgba(148,163,184,0.18)" />
  <text x="1026" y="636" fill="#cbd5e1" font-size="18" font-family="Segoe UI, Arial, sans-serif" font-weight="700">QA Summary</text>
  <text x="1026" y="668" fill="#e2e8f0" font-size="15" font-family="Segoe UI, Arial, sans-serif">Vertical section azimuth: ${survey.vertical_section_azimuth_deg?.toFixed(3) ?? 'not found'}&#176; True</text>
  <text x="1026" y="698" fill="#e2e8f0" font-size="15" font-family="Segoe UI, Arial, sans-serif">Last survey station: ${lastSurveyPoint?.md_m.toFixed(2) ?? 'n/a'} m MD</text>
  <text x="1026" y="728" fill="#e2e8f0" font-size="15" font-family="Segoe UI, Arial, sans-serif">Projected tail rows: ${projectedPoints.length}</text>
  ${anchorPoint ? `<text x="1026" y="758" fill="#7dd3fc" font-size="15" font-family="Segoe UI, Arial, sans-serif">${escapeXml(anchorLabel)}: ${anchorMd?.toFixed(2)} m | TVD: ${anchorPoint.tvd_m.toFixed(2)} m | Incl: ${anchorPoint.inclination_deg.toFixed(2)}&#176;</text>` : ''}
  ${telemetryPlacement ? `<text x="1026" y="790" fill="${telemetryPlacement.status === 'meets target' ? '#7dd3fc' : '#fbbf24'}" font-size="15" font-family="Segoe UI, Arial, sans-serif">Telemetry QA: ${telemetryPlacement.toolBottomPercentFromBottom.toFixed(2)}% tool bottom | ${telemetryPlacement.installPointPercentFromBottom.toFixed(2)}% top install</text>` : ''}
  ${telemetryPlacement ? `<text x="1026" y="816" fill="#cbd5e1" font-size="14" font-family="Segoe UI, Arial, sans-serif">Conductive casing basis: ${telemetryPlacement.conductiveCasingSetDepthMkb.toFixed(2)} mKB set depth (${telemetryPlacement.conductiveCasingLengthGlM.toFixed(2)} mGL)</text>` : ''}
  ${telemetryPlacement ? `<text x="1026" y="844" fill="#cbd5e1" font-size="14" font-family="Segoe UI, Arial, sans-serif">Lower casing below install: ${telemetryPlacement.installPointDistanceFromBottomM.toFixed(2)} m | below tool: ${telemetryPlacement.toolBottomDistanceFromBottomM.toFixed(2)} m</text>` : ''}
  ${telemetryPlacement ? `<text x="1026" y="870" fill="${telemetryPlacement.status === 'meets target' ? '#7dd3fc' : '#fde68a'}" font-size="14" font-family="Segoe UI, Arial, sans-serif">Guideline: target >= ${guidelinePercent.toFixed(0)}% lower conductive casing section | Status: ${telemetryPlacement.status}</text>` : ''}
</svg>`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, svg, 'utf8');
console.log(`Wrote ${outputPath}`);
