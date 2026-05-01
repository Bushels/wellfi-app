import fs from 'node:fs';
import path from 'node:path';
import {
  interpolateTrajectoryPoint,
  parseSurveyCsv,
  type InterpolatedTrajectoryPoint,
} from '../src/lib/directionalSurvey.ts';

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
    'Usage: npx tsx scripts/generate_pressure_concept_plate.ts --input <csv> --output <svg> --stb-top-md <md> --stb-bottom-md <md> --joint-length-m <m> --jof-min <n> --jof-max <n> --design-density-kgm3 <kgm3> --analog-density-kgm3 <kgm3> --analog-bhp-kpaa <kpaa> --analog-bhp-tvd-m <m> [--port-offset-m <m>] [--atmosphere-kpa <kpa>] [--analog-atmosphere-kpa <kpa>] [--well-name <name>] [--analog-well-name <name>]',
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

function formatFixed(value: number, digits: number): string {
  return value.toFixed(digits);
}

function hydrostaticPressureKPa(deltaTvdM: number, densityKgM3: number): number {
  return (densityKgM3 * 9.81 * deltaTvdM) / 1000;
}

function requirePoint(point: InterpolatedTrajectoryPoint | null, label: string): InterpolatedTrajectoryPoint {
  if (!point) {
    throw new Error(`Unable to interpolate ${label}.`);
  }
  return point;
}

function textLine(
  x: number,
  y: number,
  text: string,
  options?: {
    fill?: string;
    size?: number;
    weight?: number | string;
    anchor?: 'start' | 'middle' | 'end';
  },
): string {
  const fill = options?.fill ?? '#cbd5e1';
  const size = options?.size ?? 20;
  const weight = options?.weight ?? 500;
  const anchor = options?.anchor ?? 'start';
  return `<text x="${x}" y="${y}" fill="${fill}" font-size="${size}" font-family="Segoe UI, Arial, sans-serif" font-weight="${weight}" text-anchor="${anchor}">${escapeXml(text)}</text>`;
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
const wellName = args['well-name'] ?? 'WellFi Pressure Concept';
const analogWellName = args['analog-well-name'] ?? 'Adjacent Well Analog';
const stbTopMd = Number(args['stb-top-md']);
const stbBottomMd = Number(args['stb-bottom-md']);
const portOffsetM = Number(args['port-offset-m'] ?? '1.524');
const jointLengthM = Number(args['joint-length-m']);
const jofMin = Number(args['jof-min']);
const jofMax = Number(args['jof-max']);
const designDensityKgM3 = Number(args['design-density-kgm3']);
const atmosphereKPa = Number(args['atmosphere-kpa'] ?? '101.325');
const analogDensityKgM3 = Number(args['analog-density-kgm3']);
const analogAtmosphereKPa = Number(args['analog-atmosphere-kpa'] ?? '93');
const analogBhpKPaA = Number(args['analog-bhp-kpaa']);
const analogBhpTvdM = Number(args['analog-bhp-tvd-m']);

if (
  !inputPath ||
  !outputPath ||
  !Number.isFinite(stbTopMd) ||
  !Number.isFinite(stbBottomMd) ||
  !Number.isFinite(jointLengthM) ||
  !Number.isFinite(jofMin) ||
  !Number.isFinite(jofMax) ||
  !Number.isFinite(designDensityKgM3) ||
  !Number.isFinite(analogDensityKgM3) ||
  !Number.isFinite(analogBhpKPaA) ||
  !Number.isFinite(analogBhpTvdM)
) {
  usage();
}

const portMd = Number.isFinite(Number(args['port-md'])) ? Number(args['port-md']) : stbBottomMd + portOffsetM;
const survey = parseSurveyCsv(fs.readFileSync(inputPath, 'utf8'));

const stbTopPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, stbTopMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  'slotted tag bar top',
);
const stbBottomPoint = requirePoint(
  interpolateTrajectoryPoint(survey.points, stbBottomMd, {
    verticalSectionAzimuthDeg: survey.vertical_section_azimuth_deg,
  }),
  'slotted tag bar bottom',
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

const headAtFiveJofTvdM = portPoint.tvd_m - deepFluidPoint.tvd_m;
const headAtTwelveJofTvdM = portPoint.tvd_m - shallowFluidPoint.tvd_m;
const pressureLowKPagDesign = hydrostaticPressureKPa(headAtFiveJofTvdM, designDensityKgM3);
const pressureHighKPagDesign = hydrostaticPressureKPa(headAtTwelveJofTvdM, designDensityKgM3);
const pressureLowKPaADesign = pressureLowKPagDesign + atmosphereKPa;
const pressureHighKPaADesign = pressureHighKPagDesign + atmosphereKPa;
const analogEquivalentFluidHeightM = (analogBhpKPaA - analogAtmosphereKPa) / ((analogDensityKgM3 * 9.81) / 1000);
const analogFuturePortStaticKPaA = analogAtmosphereKPa + hydrostaticPressureKPa(portPoint.tvd_m, analogDensityKgM3);
const windowSpanTvdM = deepFluidPoint.tvd_m - shallowFluidPoint.tvd_m;

const width = 1800;
const height = 1180;
const compareBand = { x: 40, y: 104, width: 1720, height: 92 };
const leftCard = { x: 40, y: 220, width: 332, height: 500 };
const centerCard = { x: 402, y: 220, width: 842, height: 500 };
const rightCard = { x: 1274, y: 220, width: 486, height: 500 };
const assumptionsPanel = { x: 40, y: 748, width: 1720, height: 392 };

const analogColumn = { x: leftCard.x + 26, y: leftCard.y + 104, width: 82, height: 228 };
const centerPlot = { x: centerCard.x + 84, y: centerCard.y + 118, width: 260, height: 360 };
const centerInfo = { x: centerCard.x + 400, y: centerCard.y + 118, width: 402, height: 360 };

const localTopTvdM = Math.floor((shallowFluidPoint.tvd_m - 2) * 2) / 2;
const localBottomTvdM = Math.ceil((portPoint.tvd_m + 1.5) * 2) / 2;
const localSpanTvdM = localBottomTvdM - localTopTvdM;

function mapLocalY(tvdM: number): number {
  const ratio = (tvdM - localTopTvdM) / localSpanTvdM;
  return centerPlot.y + ratio * centerPlot.height;
}

const fluidTwelveY = mapLocalY(shallowFluidPoint.tvd_m);
const fluidFiveY = mapLocalY(deepFluidPoint.tvd_m);
const stbTopY = mapLocalY(stbTopPoint.tvd_m);
const stbBottomY = mapLocalY(stbBottomPoint.tvd_m);
const portY = mapLocalY(portPoint.tvd_m);
const stbVisualY = (stbTopY + stbBottomY) / 2;
const stbVisualHeight = Math.max(10, Math.abs(stbBottomY - stbTopY));
const wellCenterX = centerPlot.x + 162;
const wellOuterWidth = 108;
const wellInnerWidth = 52;
const localTicks = [640, 645, 650, 655, 660, 665].filter((tick) => tick >= localTopTvdM && tick <= localBottomTvdM);

const assumptionTiles = [
  { title: 'JOF Datum', body: `Top of STB = ${formatFixed(stbTopMd, 2)} mKB`, tone: '#fbbf24' },
  { title: '1 JOF', body: `${formatFixed(jointLengthM, 3)} m measured joint length`, tone: '#c4b5fd' },
  { title: 'Port Location', body: `${formatFixed(portOffsetM, 3)} m below STB bottom = ${formatFixed(portMd, 2)} mKB`, tone: '#67e8f9' },
  { title: 'Fluid Basis', body: `${formatFixed(designDensityKgM3, 0)} kg/m^3 design fluid | annulus vented`, tone: '#86efac' },
];

const assumptionTileWidth = 400;
const assumptionTileHeight = 92;
const assumptionTilesSvg = assumptionTiles
  .map((tile, index) => {
    const x = assumptionsPanel.x + 24 + index * 418;
    const y = assumptionsPanel.y + 108;
    const body = textBlock(x + 18, y + 52, tile.body, {
      fill: '#cbd5e1',
      size: 15,
      weight: 500,
      maxWidth: assumptionTileWidth - 36,
      lineHeight: 18,
    });
    return `
      <rect x="${x}" y="${y}" width="${assumptionTileWidth}" height="${assumptionTileHeight}" rx="18" fill="rgba(15,23,42,0.54)" stroke="rgba(148,163,184,0.12)" />
      <rect x="${x + 16}" y="${y + 16}" width="10" height="10" rx="5" fill="${tile.tone}" />
      ${textLine(x + 34, y + 29, tile.title, { fill: '#f8fafc', size: 17, weight: 700 })}
      ${body.svg}
    `;
  })
  .join('\n');

const centerInfoBlocks = [
  {
    title: 'Operating Fluid-Top Window',
    lines: [
      `12 JOF top  ${formatFixed(shallowFluidPoint.tvd_m, 2)} mTVD`,
      `5 JOF top   ${formatFixed(deepFluidPoint.tvd_m, 2)} mTVD`,
      `Window  ${formatFixed(windowSpanTvdM, 2)} m TVD`,
    ],
    fill: 'rgba(21,128,61,0.18)',
    stroke: 'rgba(74,222,128,0.28)',
    tone: '#86efac',
    y: centerInfo.y,
    lineGap: 22,
  },
  {
    title: 'Static Analog',
    lines: [
      `Future port could load to ${formatFixed(analogFuturePortStaticKPaA / 1000, 2)} MPaa abs`,
      `${formatFixed(analogBhpKPaA, 1)} kPaa analog BHP @ ${formatFixed(analogBhpTvdM, 1)} mTVD`,
      `Near-full static column is a shut-in case`,
    ],
    fill: 'rgba(14,116,144,0.16)',
    stroke: 'rgba(56,189,248,0.26)',
    tone: '#7dd3fc',
    y: centerInfo.y + 126,
    lineGap: 20,
  },
  {
    title: 'Datum And Tool',
    lines: [
      `STB top ${formatFixed(stbTopPoint.tvd_m, 2)} mTVD | bottom ${formatFixed(stbBottomPoint.tvd_m, 2)} mTVD`,
      `WellFi port ${formatFixed(portPoint.tvd_m, 2)} mTVD`,
      `${formatFixed(portOffsetM, 3)} m below STB bottom`,
    ],
    fill: 'rgba(245,158,11,0.12)',
    stroke: 'rgba(251,191,36,0.22)',
    tone: '#fed7aa',
    y: centerInfo.y + 252,
    lineGap: 20,
  },
];

const centerInfoSvg = centerInfoBlocks
  .map((block) => {
    const heightBlock = block === centerInfoBlocks[0] ? 110 : 98;
    const linesSvg = block.lines
      .map((line, index) =>
        textLine(centerInfo.x + 24, block.y + 54 + index * block.lineGap, line, {
          fill: index === 0 ? block.tone : '#cbd5e1',
          size: index === 0 ? 15 : 14,
          weight: index === 0 ? 700 : 500,
        }),
      )
      .join('\n');
    return `
      <rect x="${centerInfo.x}" y="${block.y}" width="${centerInfo.width}" height="${heightBlock}" rx="18" fill="${block.fill}" stroke="${block.stroke}" />
      ${textLine(centerInfo.x + 24, block.y + 30, block.title, { fill: '#f8fafc', size: 17, weight: 700 })}
      ${linesSvg}
    `;
  })
  .join('\n');

const outputCards = [
  {
    title: '12 JOF',
    value: `${formatFixed(pressureHighKPaADesign, 1)} kPaa`,
    detail: `${formatFixed(headAtTwelveJofTvdM, 2)} m TVD head`,
    fill: 'rgba(21,128,61,0.18)',
    stroke: 'rgba(74,222,128,0.28)',
    tone: '#86efac',
    y: rightCard.y + 258,
  },
  {
    title: '5 JOF',
    value: `${formatFixed(pressureLowKPaADesign, 1)} kPaa`,
    detail: `${formatFixed(headAtFiveJofTvdM, 2)} m TVD head`,
    fill: 'rgba(20,83,45,0.18)',
    stroke: 'rgba(34,197,94,0.28)',
    tone: '#bbf7d0',
    y: rightCard.y + 368,
  },
];

const outputCardsSvg = outputCards
  .map(
    (card) => `
      <rect x="${rightCard.x + 24}" y="${card.y}" width="${rightCard.width - 48}" height="96" rx="18" fill="${card.fill}" stroke="${card.stroke}" />
      ${textLine(rightCard.x + 42, card.y + 30, card.title, { fill: '#f8fafc', size: 16, weight: 700 })}
      ${textLine(rightCard.x + 42, card.y + 62, card.value, { fill: card.tone, size: 28, weight: 700 })}
      ${textLine(rightCard.x + 42, card.y + 84, card.detail, { fill: '#cbd5e1', size: 14, weight: 500 })}
    `,
  )
  .join('\n');

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
  <defs>
    <linearGradient id="pageBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#08111f" />
      <stop offset="55%" stop-color="#081425" />
      <stop offset="100%" stop-color="#030712" />
    </linearGradient>
    <linearGradient id="staticBand" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="rgba(56,189,248,0.22)" />
      <stop offset="100%" stop-color="rgba(125,211,252,0.08)" />
    </linearGradient>
    <linearGradient id="flowBand" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="rgba(34,197,94,0.22)" />
      <stop offset="100%" stop-color="rgba(74,222,128,0.08)" />
    </linearGradient>
    <linearGradient id="analogFill" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7dd3fc" stop-opacity="0.62" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.18" />
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#pageBg)" />
  <rect x="16" y="16" width="${width - 32}" height="${height - 32}" rx="26" fill="none" stroke="rgba(148,163,184,0.14)" />

  ${textLine(40, 62, `${wellName} | WellFi Pressure Concept`, { fill: '#f8fafc', size: 40, weight: 700 })}
  ${textLine(
    40,
    92,
    'Shut-in pressure can be MPa while pump-on WellFi pressure stays in the kPa range because the tool reads the local TVD head above the port.',
    { fill: '#94a3b8', size: 17, weight: 500 },
  )}

  <rect x="${compareBand.x}" y="${compareBand.y}" width="${compareBand.width}" height="${compareBand.height}" rx="22" fill="rgba(8,15,27,0.66)" stroke="rgba(148,163,184,0.12)" />
  <rect x="${compareBand.x + 18}" y="${compareBand.y + 14}" width="790" height="64" rx="19" fill="url(#staticBand)" stroke="rgba(56,189,248,0.18)" />
  <rect x="${compareBand.x + 912}" y="${compareBand.y + 14}" width="790" height="64" rx="19" fill="url(#flowBand)" stroke="rgba(74,222,128,0.18)" />
  ${textLine(compareBand.x + 36, compareBand.y + 41, 'Static analog at future port', { fill: '#bae6fd', size: 15, weight: 700 })}
  ${textLine(compareBand.x + 36, compareBand.y + 79, `~${formatFixed(analogFuturePortStaticKPaA / 1000, 2)} MPaa abs`, { fill: '#7dd3fc', size: 28, weight: 700 })}
  ${textLine(compareBand.x + 930, compareBand.y + 41, 'Pump-on target at WellFi', { fill: '#bbf7d0', size: 15, weight: 700 })}
  ${textLine(compareBand.x + 930, compareBand.y + 79, `${formatFixed(pressureLowKPaADesign, 1)} to ${formatFixed(pressureHighKPaADesign, 1)} kPaa`, { fill: '#86efac', size: 28, weight: 700 })}
  ${textLine(compareBand.x + compareBand.width / 2, compareBand.y + 56, 'same reservoir / different operating state', {
    fill: '#cbd5e1',
    size: 13,
    weight: 600,
    anchor: 'middle',
  })}

  <rect x="${leftCard.x}" y="${leftCard.y}" width="${leftCard.width}" height="${leftCard.height}" rx="24" fill="rgba(15,23,42,0.54)" stroke="rgba(148,163,184,0.14)" />
  <rect x="${centerCard.x}" y="${centerCard.y}" width="${centerCard.width}" height="${centerCard.height}" rx="24" fill="rgba(15,23,42,0.54)" stroke="rgba(148,163,184,0.14)" />
  <rect x="${rightCard.x}" y="${rightCard.y}" width="${rightCard.width}" height="${rightCard.height}" rx="24" fill="rgba(15,23,42,0.54)" stroke="rgba(148,163,184,0.14)" />
  <rect x="${assumptionsPanel.x}" y="${assumptionsPanel.y}" width="${assumptionsPanel.width}" height="${assumptionsPanel.height}" rx="24" fill="rgba(8,15,27,0.66)" stroke="rgba(148,163,184,0.12)" />

  ${textLine(leftCard.x + 24, leftCard.y + 38, 'Adjacent-Well Static Analog', { fill: '#f8fafc', size: 25, weight: 700 })}
  ${textLine(leftCard.x + 24, leftCard.y + 62, analogWellName, { fill: '#94a3b8', size: 14, weight: 600 })}
  <rect x="${analogColumn.x}" y="${analogColumn.y}" width="${analogColumn.width}" height="${analogColumn.height}" rx="32" fill="rgba(15,23,42,0.94)" stroke="rgba(148,163,184,0.18)" />
  <rect x="${analogColumn.x + 18}" y="${analogColumn.y + 12}" width="${analogColumn.width - 36}" height="${analogColumn.height - 24}" rx="20" fill="url(#analogFill)" />
  ${textLine(analogColumn.x + analogColumn.width / 2, analogColumn.y - 8, 'near-full static column', { fill: '#7dd3fc', size: 13, weight: 700, anchor: 'middle' })}
  ${textLine(leftCard.x + 132, leftCard.y + 122, 'BHP', { fill: '#94a3b8', size: 13, weight: 700 })}
  ${textLine(leftCard.x + 132, leftCard.y + 152, `${formatFixed(analogBhpKPaA, 1)} kPaa`, { fill: '#f8fafc', size: 28, weight: 700 })}
  ${textLine(leftCard.x + 132, leftCard.y + 176, `@ ${formatFixed(analogBhpTvdM, 1)} mTVD`, { fill: '#cbd5e1', size: 14, weight: 500 })}
  ${textLine(leftCard.x + 132, leftCard.y + 228, 'Fluid Density', { fill: '#94a3b8', size: 13, weight: 700 })}
  ${textLine(leftCard.x + 132, leftCard.y + 258, `${formatFixed(analogDensityKgM3, 1)} kg/m^3`, { fill: '#f8fafc', size: 24, weight: 700 })}
  ${textLine(leftCard.x + 132, leftCard.y + 306, 'Equivalent Fluid Height', { fill: '#94a3b8', size: 13, weight: 700 })}
  ${textLine(leftCard.x + 132, leftCard.y + 336, `${formatFixed(analogEquivalentFluidHeightM, 1)} m`, { fill: '#f8fafc', size: 24, weight: 700 })}
  ${textBlock(leftCard.x + 24, leftCard.y + 394, 'Use this only as the shut-in analog. It is not the pump-on pressure that the WellFi port should normally see.', {
    fill: '#cbd5e1',
    size: 16,
    weight: 500,
    maxWidth: leftCard.width - 48,
    lineHeight: 20,
  }).svg}

  ${textLine(centerCard.x + 24, centerCard.y + 38, 'Zoomed Operating Window', { fill: '#f8fafc', size: 25, weight: 700 })}
  ${textLine(centerCard.x + 24, centerCard.y + 62, 'Local interval only. This is the part of the wellbore that matters to the tool.', { fill: '#94a3b8', size: 14, weight: 500 })}
  <rect x="${centerPlot.x - 18}" y="${centerPlot.y - 18}" width="${centerPlot.width + 54}" height="${centerPlot.height + 36}" rx="22" fill="rgba(2,6,23,0.32)" stroke="rgba(148,163,184,0.10)" />
  ${localTicks
    .map((tick) => {
      const y = mapLocalY(tick);
      return `
        <line x1="${centerPlot.x + 22}" x2="${centerPlot.x + centerPlot.width}" y1="${y}" y2="${y}" stroke="rgba(148,163,184,0.09)" stroke-dasharray="4 10" />
        ${textLine(centerPlot.x - 18, y + 4, `${tick}`, { fill: '#64748b', size: 12, weight: 500, anchor: 'end' })}
      `;
    })
    .join('\n')}
  <text transform="translate(${centerPlot.x - 54} ${centerPlot.y + centerPlot.height / 2 + 36}) rotate(-90)" fill="#94a3b8" font-size="14" font-family="Segoe UI, Arial, sans-serif" font-weight="600">TVD FROM KB (m)</text>

  <rect x="${centerPlot.x + 22}" y="${fluidTwelveY}" width="146" height="${fluidFiveY - fluidTwelveY}" rx="18" fill="url(#flowBand)" stroke="rgba(74,222,128,0.24)" />
  <line x1="${centerPlot.x + 10}" x2="${centerPlot.x + centerPlot.width}" y1="${fluidTwelveY}" y2="${fluidTwelveY}" stroke="rgba(34,197,94,0.60)" stroke-width="2" />
  <line x1="${centerPlot.x + 10}" x2="${centerPlot.x + centerPlot.width}" y1="${fluidFiveY}" y2="${fluidFiveY}" stroke="rgba(74,222,128,0.60)" stroke-width="2" />
  <line x1="${centerPlot.x + 2}" x2="${centerPlot.x + 2}" y1="${fluidTwelveY}" y2="${fluidFiveY}" stroke="rgba(74,222,128,0.66)" stroke-width="3" />
  <line x1="${centerPlot.x - 8}" x2="${centerPlot.x + 2}" y1="${fluidTwelveY}" y2="${fluidTwelveY}" stroke="rgba(74,222,128,0.66)" stroke-width="3" />
  <line x1="${centerPlot.x - 8}" x2="${centerPlot.x + 2}" y1="${fluidFiveY}" y2="${fluidFiveY}" stroke="rgba(74,222,128,0.66)" stroke-width="3" />
  ${textLine(centerPlot.x + 20, (fluidTwelveY + fluidFiveY) / 2 - 12, '5-12 JOF', { fill: '#86efac', size: 20, weight: 700 })}
  ${textLine(centerPlot.x + 20, (fluidTwelveY + fluidFiveY) / 2 + 14, `${formatFixed(windowSpanTvdM, 2)} m TVD window`, { fill: '#bbf7d0', size: 14, weight: 600 })}

  <rect x="${wellCenterX - wellOuterWidth / 2}" y="${centerPlot.y + 4}" width="${wellOuterWidth}" height="${centerPlot.height - 8}" rx="38" fill="rgba(15,23,42,0.96)" stroke="rgba(148,163,184,0.20)" />
  <rect x="${wellCenterX - wellInnerWidth / 2}" y="${centerPlot.y + 12}" width="${wellInnerWidth}" height="${centerPlot.height - 24}" rx="20" fill="rgba(56,189,248,0.12)" />
  <rect x="${wellCenterX - wellOuterWidth / 2 + 8}" y="${fluidTwelveY}" width="${wellOuterWidth - 16}" height="${fluidFiveY - fluidTwelveY}" rx="18" fill="rgba(34,197,94,0.12)" />
  <rect x="${wellCenterX - wellOuterWidth / 2 + 8}" y="${stbVisualY - stbVisualHeight / 2}" width="${wellOuterWidth - 16}" height="${stbVisualHeight}" rx="8" fill="rgba(245,158,11,0.40)" stroke="rgba(251,191,36,0.60)" />
  <circle cx="${wellCenterX}" cy="${portY}" r="8" fill="#f8fafc" stroke="#38bdf8" stroke-width="3" />
  <line x1="${wellCenterX + 46}" x2="${centerInfo.x - 18}" y1="${portY}" y2="${portY}" stroke="rgba(56,189,248,0.42)" stroke-width="2" />
  ${textLine(centerPlot.x - 18, fluidTwelveY - 8, '12 JOF top', { fill: '#86efac', size: 13, weight: 700, anchor: 'end' })}
  ${textLine(centerPlot.x - 18, fluidFiveY - 8, '5 JOF top', { fill: '#bbf7d0', size: 13, weight: 700, anchor: 'end' })}
  ${textLine(centerPlot.x - 18, stbVisualY - 8, 'STB datum', { fill: '#fed7aa', size: 13, weight: 700, anchor: 'end' })}
  ${textLine(centerPlot.x - 18, portY + 18, 'WellFi port', { fill: '#7dd3fc', size: 13, weight: 700, anchor: 'end' })}
  ${centerInfoSvg}

  ${textLine(rightCard.x + 24, rightCard.y + 38, 'What WellFi Sees', { fill: '#f8fafc', size: 25, weight: 700 })}
  ${textLine(rightCard.x + 24, rightCard.y + 62, 'Absolute pressure at the WellFi port while the pump holds the target JOF window.', { fill: '#94a3b8', size: 14, weight: 500 })}
  ${textLine(rightCard.x + 24, rightCard.y + 126, `${formatFixed(pressureLowKPaADesign, 1)} to ${formatFixed(pressureHighKPaADesign, 1)} kPaa`, { fill: '#7dd3fc', size: 36, weight: 700 })}
  ${textLine(rightCard.x + 24, rightCard.y + 154, `${formatFixed(pressureLowKPagDesign, 1)} to ${formatFixed(pressureHighKPagDesign, 1)} kPag gauge equivalent`, { fill: '#cbd5e1', size: 15, weight: 500 })}
  <rect x="${rightCard.x + 24}" y="${rightCard.y + 176}" width="${rightCard.width - 48}" height="50" rx="16" fill="rgba(14,116,144,0.16)" stroke="rgba(56,189,248,0.20)" />
  ${textBlock(rightCard.x + 42, rightCard.y + 198, 'Tool pressure is set by local TVD head above the port, not by full measured joint length.', {
    fill: '#bae6fd',
    size: 14,
    weight: 700,
    maxWidth: rightCard.width - 84,
    lineHeight: 17,
  }).svg}
  ${outputCardsSvg}
  ${textLine(rightCard.x + 24, rightCard.y + 484, `Port reference: ${formatFixed(portMd, 2)} mKB | ${formatFixed(portPoint.tvd_m, 2)} mTVD`, { fill: '#7dd3fc', size: 15, weight: 600 })}

  ${textLine(assumptionsPanel.x + 24, assumptionsPanel.y + 38, 'Assumptions Used On This Infographic', { fill: '#f8fafc', size: 24, weight: 700 })}
  ${textLine(assumptionsPanel.x + 24, assumptionsPanel.y + 66, 'Pressure uses TVD head from fluid top to port. The annulus is treated as vented to atmosphere.', {
    fill: '#94a3b8',
    size: 15,
    weight: 500,
  })}
  ${assumptionTilesSvg}
</svg>`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, svg, 'utf8');
console.log(outputPath);
