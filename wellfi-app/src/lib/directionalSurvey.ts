export type TrajectoryStationKind = 'survey' | 'projection';

export interface TrajectoryPoint {
  md_m: number;
  inclination_deg: number;
  azimuth_deg: number;
  tvd_m: number;
  northing_offset_m: number;
  easting_offset_m: number;
  vertical_section_m: number;
  station_kind: TrajectoryStationKind;
  station_note: string | null;
}

export interface SurveyParseResult {
  points: TrajectoryPoint[];
  survey_header_uwi: string | null;
  vertical_section_azimuth_deg: number | null;
  last_survey_md_m: number;
  projected_td_md_m: number | null;
}

export interface InterpolatedTrajectoryPoint extends TrajectoryPoint {
  horizontal_offset_m: number;
}

const SURVEY_HEADER_PREFIX = ['MD', 'INCL', 'AZIMUTH', 'TVD', 'TVDSS', 'N(+)', 'E(+)', 'VS'];

interface HeaderColumnMap {
  md: number;
  inclination: number;
  azimuth: number;
  tvd: number;
  northing: number;
  easting: number;
  verticalSection: number;
  annotations: number | null;
}

const HEADER_ALIASES: Record<keyof Omit<HeaderColumnMap, 'annotations'>, readonly string[]> = {
  md: ['md'],
  inclination: ['incl', 'inclination'],
  azimuth: ['azimuth', 'azi'],
  tvd: ['tvd', 'true vertical depth', 'true vertical depth (tvd)'],
  northing: ['n(+)', 'n', 'north', 'northing'],
  easting: ['e(+)', 'e', 'east', 'easting'],
  verticalSection: ['vs', 'vert sect', 'vertical section', 'vert. section'],
};

const ANNOTATION_ALIASES = ['annotations', 'annotation', 'comments', 'station notes', 'notes', 'remarks'];

function normalizeHeaderToken(value: string): string {
  return value.toLowerCase().replace(/\s+/g, ' ').trim();
}

function matchColumn(normalized: string[], aliases: readonly string[]): number {
  for (let index = 0; index < normalized.length; index += 1) {
    const cell = normalized[index];
    if (!cell) continue;
    if (aliases.includes(cell)) return index;
  }
  // Fall back to prefix matching (e.g., "tvd (m)" should match "tvd").
  for (let index = 0; index < normalized.length; index += 1) {
    const cell = normalized[index];
    if (!cell) continue;
    if (aliases.some((alias) => cell.startsWith(alias))) return index;
  }
  return -1;
}

function detectHeaderMap(parts: string[]): HeaderColumnMap | null {
  const normalized = parts.map(normalizeHeaderToken);
  const map: HeaderColumnMap = {
    md: matchColumn(normalized, HEADER_ALIASES.md),
    inclination: matchColumn(normalized, HEADER_ALIASES.inclination),
    azimuth: matchColumn(normalized, HEADER_ALIASES.azimuth),
    tvd: matchColumn(normalized, HEADER_ALIASES.tvd),
    northing: matchColumn(normalized, HEADER_ALIASES.northing),
    easting: matchColumn(normalized, HEADER_ALIASES.easting),
    verticalSection: matchColumn(normalized, HEADER_ALIASES.verticalSection),
    annotations: matchColumn(normalized, ANNOTATION_ALIASES),
  };
  const required: Array<keyof Omit<HeaderColumnMap, 'annotations'>> = [
    'md', 'inclination', 'azimuth', 'tvd', 'northing', 'easting', 'verticalSection',
  ];
  for (const key of required) {
    if (map[key] < 0) return null;
  }
  if (map.annotations != null && map.annotations < 0) {
    map.annotations = null;
  }
  return map;
}

function roundTo(value: number, digits = 3): number {
  return Number(value.toFixed(digits));
}

function clampUnitInterval(value: number): number {
  return Math.min(1, Math.max(-1, value));
}

function toRadians(valueDeg: number): number {
  return (valueDeg * Math.PI) / 180;
}

function normalizeAngleDeg(valueDeg: number): number {
  const normalized = ((valueDeg % 360) + 360) % 360;
  return normalized === 360 ? 0 : normalized;
}

function shortestAngleDeltaDeg(startDeg: number, endDeg: number): number {
  let delta = normalizeAngleDeg(endDeg) - normalizeAngleDeg(startDeg);
  if (delta > 180) delta -= 360;
  if (delta < -180) delta += 360;
  return delta;
}

function interpolateAngleDeg(startDeg: number, endDeg: number, ratio: number): number {
  return normalizeAngleDeg(startDeg + shortestAngleDeltaDeg(startDeg, endDeg) * ratio);
}

function detectSurveyHeaderUwi(lines: readonly string[]): string | null {
  // Match the standalone form (Vendor A) OR the embedded form (Vendor B),
  // e.g., "UWI (D59:at the time of submission) ,102/16-18-083-17W5/12,,,"
  const uwiRegex = /\b(\d{3}\/\d{2}-\d{2}-\d{3}-\d{2}W\d\/\d{2})\b/;
  for (const line of lines) {
    const match = line.match(uwiRegex);
    if (match) return match[1];
  }
  return null;
}

function detectVerticalSectionAzimuth(lines: readonly string[]): number | null {
  // Vendor A (e.g., Slot-based metadata block):
  //   "Vertical Section is from Slot and calculated along an Azimuth of 323.088°"
  // Vendor B (e.g., Altitude Energy Partners header):
  //   "Vertical Section Azimuth ,351.6"
  const patterns: RegExp[] = [
    /Vertical Section[^\n]*Azimuth of\s+([0-9]+(?:\.[0-9]+)?)/i,
    /Vertical Section Azimuth\s*[,:]\s*([0-9]+(?:\.[0-9]+)?)/i,
  ];
  for (const line of lines) {
    for (const pattern of patterns) {
      const match = line.match(pattern);
      if (match) {
        const parsed = Number(match[1]);
        if (Number.isFinite(parsed)) return roundTo(parsed, 3);
      }
    }
  }
  return null;
}

function enrichPoint(point: TrajectoryPoint): InterpolatedTrajectoryPoint {
  return {
    ...point,
    horizontal_offset_m: roundTo(Math.hypot(point.northing_offset_m, point.easting_offset_m)),
  };
}

function projectToVerticalSection(northingM: number, eastingM: number, azimuthDeg: number): number {
  const azimuthRad = toRadians(azimuthDeg);
  return northingM * Math.cos(azimuthRad) + eastingM * Math.sin(azimuthRad);
}

function minimumCurvatureDelta(
  startInclinationDeg: number,
  startAzimuthDeg: number,
  endInclinationDeg: number,
  endAzimuthDeg: number,
  courseLengthM: number,
): { northing_m: number; easting_m: number; tvd_m: number } {
  const startInclinationRad = toRadians(startInclinationDeg);
  const endInclinationRad = toRadians(endInclinationDeg);
  const startAzimuthRad = toRadians(startAzimuthDeg);
  const endAzimuthRad = toRadians(endAzimuthDeg);
  const azimuthDeltaRad = endAzimuthRad - startAzimuthRad;

  const doglegRad = Math.acos(
    clampUnitInterval(
      Math.cos(startInclinationRad) * Math.cos(endInclinationRad) +
        Math.sin(startInclinationRad) * Math.sin(endInclinationRad) * Math.cos(azimuthDeltaRad),
    ),
  );

  const ratioFactor = doglegRad === 0 ? 1 : (2 / doglegRad) * Math.tan(doglegRad / 2);

  return {
    northing_m:
      (courseLengthM / 2) *
      (Math.sin(startInclinationRad) * Math.cos(startAzimuthRad) +
        Math.sin(endInclinationRad) * Math.cos(endAzimuthRad)) *
      ratioFactor,
    easting_m:
      (courseLengthM / 2) *
      (Math.sin(startInclinationRad) * Math.sin(startAzimuthRad) +
        Math.sin(endInclinationRad) * Math.sin(endAzimuthRad)) *
      ratioFactor,
    tvd_m:
      (courseLengthM / 2) * (Math.cos(startInclinationRad) + Math.cos(endInclinationRad)) * ratioFactor,
  };
}

export function parseSurveyCsv(rawCsv: string): SurveyParseResult {
  const lines = rawCsv.split(/\r?\n/);

  let headerIndex = -1;
  let headerMap: HeaderColumnMap | null = null;
  for (let index = 0; index < lines.length; index += 1) {
    const parts = lines[index].split(',').map((part) => part.trim());
    const map = detectHeaderMap(parts);
    if (map != null) {
      headerIndex = index;
      headerMap = map;
      break;
    }
  }

  if (headerIndex === -1 || !headerMap) {
    throw new Error('Survey CSV header not found.');
  }

  // Some vendors place units on the line immediately after the header, e.g. "(m),(deg),..."
  // Skip it if present.
  let firstDataIndex = headerIndex + 1;
  const firstCandidate = lines[firstDataIndex];
  if (firstCandidate) {
    const firstParts = firstCandidate.split(',').map((p) => p.trim());
    const mdCell = firstParts[headerMap.md] ?? '';
    if (!Number.isFinite(Number(mdCell))) {
      firstDataIndex += 1;
    }
  }

  const points: TrajectoryPoint[] = [];
  for (let index = firstDataIndex; index < lines.length; index += 1) {
    const rawLine = lines[index].trim();
    if (!rawLine) continue;

    const parts = lines[index].split(',').map((part) => part.trim());
    if (parts.length < headerMap.verticalSection + 1) continue;

    const md = Number(parts[headerMap.md]);
    if (!Number.isFinite(md)) continue;

    const inclination = Number(parts[headerMap.inclination]);
    const azimuth = Number(parts[headerMap.azimuth]);
    const tvd = Number(parts[headerMap.tvd]);
    const northing = Number(parts[headerMap.northing]);
    const easting = Number(parts[headerMap.easting]);
    const verticalSection = Number(parts[headerMap.verticalSection]);

    if (
      !Number.isFinite(inclination) ||
      !Number.isFinite(azimuth) ||
      !Number.isFinite(tvd) ||
      !Number.isFinite(northing) ||
      !Number.isFinite(easting) ||
      !Number.isFinite(verticalSection)
    ) {
      continue;
    }

    // Annotations: prefer the mapped column, but fall back to everything after
    // the vertical-section column so we still catch trailing notes in the old
    // embedded-CSV format.
    const annotationIndex = headerMap.annotations;
    let stationNote: string | null;
    if (annotationIndex != null) {
      stationNote = parts.slice(annotationIndex).join(',').trim() || null;
    } else {
      stationNote = parts.slice(headerMap.verticalSection + 1).join(',').trim() || null;
    }
    const stationKind: TrajectoryStationKind = stationNote && /projection/i.test(stationNote) ? 'projection' : 'survey';

    points.push({
      md_m: roundTo(md),
      inclination_deg: roundTo(inclination),
      azimuth_deg: roundTo(normalizeAngleDeg(azimuth)),
      tvd_m: roundTo(tvd),
      northing_offset_m: roundTo(northing),
      easting_offset_m: roundTo(easting),
      vertical_section_m: roundTo(verticalSection),
      station_kind: stationKind,
      station_note: stationNote,
    });
  }

  if (points.length === 0) {
    throw new Error('Survey CSV contained no trajectory rows.');
  }

  const surveyedPoints = getSurveyedTrajectoryPoints(points);
  const lastSurveyPoint = surveyedPoints.at(-1) ?? points[points.length - 1];
  const projectedTdPoint = getProjectedTrajectoryPoints(points).at(-1) ?? null;

  return {
    points,
    survey_header_uwi: detectSurveyHeaderUwi(lines),
    vertical_section_azimuth_deg: detectVerticalSectionAzimuth(lines),
    last_survey_md_m: lastSurveyPoint.md_m,
    projected_td_md_m: projectedTdPoint?.md_m ?? null,
  };
}

export function getSurveyedTrajectoryPoints(points: readonly TrajectoryPoint[]): TrajectoryPoint[] {
  return points.filter((point) => point.station_kind === 'survey');
}

export function getProjectedTrajectoryPoints(points: readonly TrajectoryPoint[]): TrajectoryPoint[] {
  return points.filter((point) => point.station_kind === 'projection');
}

export function getLastSurveyedTrajectoryPoint(points: readonly TrajectoryPoint[]): TrajectoryPoint | null {
  const surveyedPoints = getSurveyedTrajectoryPoints(points);
  return surveyedPoints.at(-1) ?? null;
}

export function interpolateTrajectoryPoint(
  points: readonly TrajectoryPoint[],
  targetMdM: number,
  options?: {
    includeProjectedStations?: boolean;
    verticalSectionAzimuthDeg?: number | null;
  },
): InterpolatedTrajectoryPoint | null {
  const eligiblePoints = options?.includeProjectedStations ? points : getSurveyedTrajectoryPoints(points);
  if (eligiblePoints.length === 0) return null;

  if (targetMdM <= eligiblePoints[0].md_m) {
    return enrichPoint(eligiblePoints[0]);
  }

  const lastPoint = eligiblePoints[eligiblePoints.length - 1];
  if (targetMdM >= lastPoint.md_m) {
    return enrichPoint(lastPoint);
  }

  for (let index = 0; index < eligiblePoints.length - 1; index += 1) {
    const left = eligiblePoints[index];
    const right = eligiblePoints[index + 1];

    if (targetMdM < left.md_m || targetMdM > right.md_m) continue;
    if (targetMdM === left.md_m) return enrichPoint(left);
    if (targetMdM === right.md_m) return enrichPoint(right);

    const spanM = right.md_m - left.md_m;
    const ratio = spanM === 0 ? 0 : (targetMdM - left.md_m) / spanM;
    const targetInclinationDeg = roundTo(
      left.inclination_deg + (right.inclination_deg - left.inclination_deg) * ratio,
    );
    const targetAzimuthDeg = roundTo(interpolateAngleDeg(left.azimuth_deg, right.azimuth_deg, ratio));
    const partialDelta = minimumCurvatureDelta(
      left.inclination_deg,
      left.azimuth_deg,
      targetInclinationDeg,
      targetAzimuthDeg,
      targetMdM - left.md_m,
    );
    const northingM = roundTo(left.northing_offset_m + partialDelta.northing_m);
    const eastingM = roundTo(left.easting_offset_m + partialDelta.easting_m);
    const tvdM = roundTo(left.tvd_m + partialDelta.tvd_m);
    const verticalSectionM =
      options?.verticalSectionAzimuthDeg != null
        ? roundTo(projectToVerticalSection(northingM, eastingM, options.verticalSectionAzimuthDeg))
        : roundTo(left.vertical_section_m + (right.vertical_section_m - left.vertical_section_m) * ratio);

    return {
      md_m: roundTo(targetMdM),
      inclination_deg: targetInclinationDeg,
      azimuth_deg: targetAzimuthDeg,
      tvd_m: tvdM,
      northing_offset_m: northingM,
      easting_offset_m: eastingM,
      vertical_section_m: verticalSectionM,
      station_kind: right.station_kind,
      station_note: right.station_note,
      horizontal_offset_m: roundTo(Math.hypot(northingM, eastingM)),
    };
  }

  return null;
}
