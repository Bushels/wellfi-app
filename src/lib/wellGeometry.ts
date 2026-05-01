import type { Well } from '@/types';
import obe102HzFinalSurveyCsv from '@/assets/well-geometry/obe-102-hz-16-18-83-17-final-survey.csv?raw';
import obe102HzMultilateralsData from '@/assets/well-geometry/obe-102-hz-multilaterals.json';
import {
  interpolateTrajectoryPoint,
  parseSurveyCsv,
} from './directionalSurvey';
import type { InterpolatedTrajectoryPoint, TrajectoryPoint, TrajectoryStationKind } from './directionalSurvey';

export type { InterpolatedTrajectoryPoint, TrajectoryPoint } from './directionalSurvey';
export {
  getLastSurveyedTrajectoryPoint,
  getProjectedTrajectoryPoints,
  getSurveyedTrajectoryPoints,
  interpolateTrajectoryPoint,
} from './directionalSurvey';

export interface CompletionComponent {
  id: 'pump' | 'slotted_tag_bar' | 'wellfi_tool' | 'no_turn_tool' | 'collar';
  label: string;
  top_mkb: number;
  bottom_mkb: number;
  od_mm: number | null;
  note?: string;
}

export interface CompletionSnapshot {
  id: string;
  run_date: string;
  label: string;
  tubing_set_depth_mkb: number;
  source_note: string;
  components: CompletionComponent[];
}

export interface HighlightAnchor {
  snapshot_id: string;
  component_id: CompletionComponent['id'];
  edge: 'top' | 'bottom' | 'center';
  label: string;
}

export interface WellSummaryMetric {
  id: 'avg_pump_runtime_pre_wellfi';
  label: string;
  value: number;
  unit: string;
  context: string;
}

export interface TelemetryPlacementReference {
  kb_to_gl_m: number;
  conductive_casing_set_depth_mkb: number;
  guideline_percent: number;
}

export interface WellLateral {
  leg: number;
  uwi: string | null;
  label: string;
  is_parent: boolean;
  kop_md_m: number;
  kop_tvd_m: number;
  vertical_section_azimuth_deg: number | null;
  last_survey_md_m: number;
  projected_td_md_m: number | null;
  station_count: number;
  source_file: string;
  survey_points: TrajectoryPoint[];
}

/** Reservoir formation the well drains. Picks are well-specific (from LAS logs),
 * not basin-wide — every well has its own top/base TVDs. */
export interface ReservoirLayer {
  name: string;
  top_tvd_m: number;
  base_tvd_m: number;
  /** Optional display color; defaults to warm amber. Values in 0-1 range. */
  color_rgba?: [number, number, number, number];
  /** Free-form note about the pick source (e.g., "Build LAS MWD gamma at 790 m MD"). */
  pick_source?: string;
}

export interface MultilateralDataset {
  well_name: string;
  licence: string;
  source_directory: string;
  imported_at: string;
  parent_leg: number;
  laterals: WellLateral[];
}

export interface WellGeometryAsset {
  source_uwi: string;
  licence: string;
  well_name: string;
  match_tokens: string[];
  survey_name: string;
  survey_header_uwi: string | null;
  vertical_section_azimuth_deg: number | null;
  last_survey_md_m: number;
  projected_td_md_m: number | null;
  survey_points: TrajectoryPoint[];
  completion_snapshots: CompletionSnapshot[];
  current_snapshot_id: string;
  highlight_anchor: HighlightAnchor;
  telemetry_placement_reference?: TelemetryPlacementReference;
  summary_metrics?: WellSummaryMetric[];
  note?: string;
  /** Multi-lateral legs, when the well has more than just the parent bore. */
  laterals?: WellLateral[];
  /** Leg number corresponding to the currently producing / monitored bore (matches the app's well UWI suffix). */
  producing_leg?: number;
  /** Reservoir formation picked from LAS logs. Rendered as a translucent slab
   *  in 3D so laterals drilled through it are visible. */
  reservoir?: ReservoirLayer;
}

export interface HighlightAnchorPoint {
  label: string;
  anchor_md_m: number;
  component: CompletionComponent;
  snapshot: CompletionSnapshot;
  trajectory: InterpolatedTrajectoryPoint | null;
}

export interface TelemetryPlacementMetric {
  kb_to_gl_m: number;
  conductive_casing_set_depth_mkb: number;
  conductive_casing_length_gl_m: number;
  install_point_distance_from_casing_bottom_m: number;
  install_point_percent_from_casing_bottom: number;
  tool_bottom_mkb: number;
  tool_bottom_distance_from_casing_bottom_m: number;
  tool_bottom_percent_from_casing_bottom: number;
  guideline_percent: number;
  status: 'meets_guideline' | 'borderline' | 'below_guideline';
}

function roundTo(value: number, digits = 3): number {
  return Number(value.toFixed(digits));
}

function normalizeToken(value: string | null | undefined): string | null {
  if (!value) return null;
  const normalized = value.toUpperCase().replace(/[^A-Z0-9]/g, '');
  return normalized.length > 0 ? normalized : null;
}

function tokenStem(value: string): string {
  return value.replace(/(W[0-9])(?:[0-9]{2,3})$/, '$1');
}

export function componentLengthM(component: CompletionComponent): number {
  return Math.max(0, component.bottom_mkb - component.top_mkb);
}

export function componentCenterM(component: CompletionComponent): number {
  return component.top_mkb + componentLengthM(component) / 2;
}

const obe102HzSurvey = parseSurveyCsv(obe102HzFinalSurveyCsv);

function coerceStationKind(value: string): TrajectoryStationKind {
  return value === 'projection' ? 'projection' : 'survey';
}

function coerceLaterals(data: MultilateralDataset): WellLateral[] {
  // The JSON import infers station_kind as `string`; coerce it back to the union type.
  return data.laterals.map((raw) => ({
    ...raw,
    survey_points: raw.survey_points.map((p) => ({
      ...p,
      station_kind: coerceStationKind(p.station_kind as unknown as string),
    })),
  }));
}

const obe102HzLaterals = coerceLaterals(obe102HzMultilateralsData as unknown as MultilateralDataset);

const OBE_102_HZ_GEOMETRY: WellGeometryAsset = {
  source_uwi: '102/16-18-083-17W5/09',
  licence: '0517936',
  well_name: 'OBE 102 HZ 16-18-83-17',
  match_tokens: [
    '102161808317W509',
    '102161808317W5',
    '102/16-18-083-17W5/09',
    '102/16-18-083-17W5/00',
    '102/16-18-083-17W5',
    'OBE 102 HZ 16-18-83-17',
  ],
  survey_name: 'OBE 102 Hz Cadotte (13-8) 16-18-83-17 Final Survey L01.csv',
  survey_header_uwi: obe102HzSurvey.survey_header_uwi,
  vertical_section_azimuth_deg: obe102HzSurvey.vertical_section_azimuth_deg,
  last_survey_md_m: obe102HzSurvey.last_survey_md_m,
  projected_td_md_m: obe102HzSurvey.projected_td_md_m,
  survey_points: obe102HzSurvey.points,
  completion_snapshots: [
    {
      id: '2025-09-01-production-string',
      run_date: '2025-09-01',
      label: 'Pre-WellFi production string',
      tubing_set_depth_mkb: 832.28,
      source_note: 'Historical schematic prior to WellFi deployment. Retained for comparison against the current Run 3 operating state.',
      components: [
        {
          id: 'pump',
          label: 'Stator / Pump',
          top_mkb: 818.69,
          bottom_mkb: 826.83,
          od_mm: 88.9,
          note: 'LSI 54-1500 stator',
        },
        {
          id: 'slotted_tag_bar',
          label: 'Slotted Tag Bar',
          top_mkb: 826.83,
          bottom_mkb: 827.87,
          od_mm: 88.9,
          note: '88.9 mm OD tag bar; deviation anchor at the bottom',
        },
        {
          id: 'wellfi_tool',
          label: 'WellFi (60.3 mm / 12 ft)',
          top_mkb: 827.87,
          bottom_mkb: 831.53,
          od_mm: 60.3,
          note: '12 ft WellFi body installed directly below the slotted tag bar',
        },
        {
          id: 'no_turn_tool',
          label: 'No-Turn Tool',
          top_mkb: 831.53,
          bottom_mkb: 832.13,
          od_mm: 203.6,
          note: 'DTA XB 8 5/8"',
        },
        {
          id: 'collar',
          label: 'Collar',
          top_mkb: 832.13,
          bottom_mkb: 832.28,
          od_mm: 88.9,
        },
      ],
    },
    {
      id: '2026-04-02-run-3-operating',
      run_date: '2026-04-02',
      label: 'Run 3 operating (post joint-pull)',
      tubing_set_depth_mkb: 822.82,
      source_note: 'Run 3 re-ran Tool 1 after pulling one joint (9.456 m) to move the tool into a lower-dogleg section. Operating from 2026-04-02 onward: JOF 4-11, payload success 97%, sensor position ≈819.9 m MD.',
      components: [
        {
          id: 'pump',
          label: 'Stator / Pump',
          top_mkb: 809.23,
          bottom_mkb: 817.37,
          od_mm: 88.9,
          note: 'LSI 54-1500 stator (shifted up 9.456 m from Run 2)',
        },
        {
          id: 'slotted_tag_bar',
          label: 'Slotted Tag Bar',
          top_mkb: 817.37,
          bottom_mkb: 818.41,
          od_mm: 88.9,
          note: '88.9 mm OD tag bar; deviation anchor at the bottom',
        },
        {
          id: 'wellfi_tool',
          label: 'WellFi (60.3 mm / 12 ft)',
          top_mkb: 818.41,
          bottom_mkb: 822.07,
          od_mm: 60.3,
          note: 'Operating position after one-joint pull; centerline ≈820.2 m (sensor ≈819.9 m MD)',
        },
        {
          id: 'no_turn_tool',
          label: 'No-Turn Tool',
          top_mkb: 822.07,
          bottom_mkb: 822.67,
          od_mm: 203.6,
          note: 'DTA XB 8 5/8"',
        },
        {
          id: 'collar',
          label: 'Collar',
          top_mkb: 822.67,
          bottom_mkb: 822.82,
          od_mm: 88.9,
        },
      ],
    },
  ],
  current_snapshot_id: '2026-04-02-run-3-operating',
  highlight_anchor: {
    snapshot_id: '2026-04-02-run-3-operating',
    component_id: 'wellfi_tool',
    edge: 'top',
    label: 'WellFi install point (Run 3)',
  },
  telemetry_placement_reference: {
    kb_to_gl_m: 4.52,
    conductive_casing_set_depth_mkb: 921.0,
    guideline_percent: 10,
  },
  summary_metrics: [
    {
      id: 'avg_pump_runtime_pre_wellfi',
      label: 'Avg pump run time',
      value: 21.6,
      unit: 'months',
      context: 'Average pump run time for this well before WellFi installation.',
    },
  ],
  note: 'Uses the final survey CSV for trajectory, keeps the projected TD separate from the last surveyed station, places the completion anchor with minimum-curvature interpolation, and evaluates telemetry placement against the intermediate conductive casing denominator.',
  laterals: obe102HzLaterals,
  producing_leg: 9,
  reservoir: {
    name: 'Bluesky',
    top_tvd_m: 660.5,
    base_tvd_m: 678.0,
    color_rgba: [0.95, 0.7, 0.25, 1.0],
    pick_source: 'Build LAS MWD gamma ray drop 139 -> 92 API at ~790 m MD',
  },
};

export const WELL_GEOMETRY_ASSETS: WellGeometryAsset[] = [OBE_102_HZ_GEOMETRY];

export function findWellGeometryAsset(well: Pick<Well, 'well_id' | 'formatted_id' | 'name'>): WellGeometryAsset | null {
  const rawCandidates = [well.well_id, well.formatted_id ?? null, well.name ?? null];
  const normalizedCandidates = rawCandidates
    .map((value) => normalizeToken(value))
    .filter((value): value is string => !!value);

  if (normalizedCandidates.length === 0) return null;

  const candidateStems = new Set(normalizedCandidates.map(tokenStem));
  let fallbackMatch: WellGeometryAsset | null = null;

  for (const asset of WELL_GEOMETRY_ASSETS) {
    const normalizedTokens = asset.match_tokens
      .map((value) => normalizeToken(value))
      .filter((value): value is string => !!value);

    if (normalizedTokens.length === 0) continue;

    const tokenSet = new Set(normalizedTokens);
    const tokenStems = new Set(normalizedTokens.map(tokenStem));

    for (const candidate of normalizedCandidates) {
      if (tokenSet.has(candidate)) return asset;
    }

    for (const stem of candidateStems) {
      if (tokenStems.has(stem)) {
        fallbackMatch = asset;
      }
    }
  }

  return fallbackMatch;
}

export function getCompletionSnapshot(asset: WellGeometryAsset, snapshotId: string): CompletionSnapshot | null {
  return asset.completion_snapshots.find((snapshot) => snapshot.id === snapshotId) ?? null;
}

export function getCurrentCompletionSnapshot(asset: WellGeometryAsset): CompletionSnapshot | null {
  return getCompletionSnapshot(asset, asset.current_snapshot_id);
}

export function findCompletionComponent(
  snapshot: CompletionSnapshot | null,
  componentId: CompletionComponent['id'],
): CompletionComponent | null {
  if (!snapshot) return null;
  return snapshot.components.find((component) => component.id === componentId) ?? null;
}

export function getHighlightAnchorPoint(asset: WellGeometryAsset): HighlightAnchorPoint | null {
  const snapshot = getCompletionSnapshot(asset, asset.highlight_anchor.snapshot_id);
  const component = findCompletionComponent(snapshot, asset.highlight_anchor.component_id);
  if (!snapshot || !component) return null;

  const anchorMdM =
    asset.highlight_anchor.edge === 'top'
      ? component.top_mkb
      : asset.highlight_anchor.edge === 'center'
        ? componentCenterM(component)
        : component.bottom_mkb;

  return {
    label: asset.highlight_anchor.label,
    anchor_md_m: roundTo(anchorMdM),
    component,
    snapshot,
    trajectory: interpolateTrajectoryPoint(asset.survey_points, anchorMdM, {
      verticalSectionAzimuthDeg: asset.vertical_section_azimuth_deg,
    }),
  };
}

export function getTelemetryPlacementMetric(
  asset: WellGeometryAsset,
  component: CompletionComponent | null,
  anchorMdM: number,
): TelemetryPlacementMetric | null {
  const reference = asset.telemetry_placement_reference;
  if (
    !reference ||
    !component ||
    !Number.isFinite(reference.kb_to_gl_m) ||
    !Number.isFinite(reference.conductive_casing_set_depth_mkb) ||
    reference.conductive_casing_set_depth_mkb <= reference.kb_to_gl_m
  ) {
    return null;
  }

  const conductiveCasingLengthGlM = roundTo(reference.conductive_casing_set_depth_mkb - reference.kb_to_gl_m, 3);
  const installPointDistanceFromBottomM = roundTo(Math.max(0, reference.conductive_casing_set_depth_mkb - anchorMdM), 3);
  const installPointPercentFromBottom = roundTo((installPointDistanceFromBottomM / conductiveCasingLengthGlM) * 100, 3);
  const toolBottomMkb = roundTo(component.bottom_mkb, 3);
  const toolBottomDistanceFromBottomM = roundTo(Math.max(0, reference.conductive_casing_set_depth_mkb - toolBottomMkb), 3);
  const toolBottomPercentFromBottom = roundTo((toolBottomDistanceFromBottomM / conductiveCasingLengthGlM) * 100, 3);
  const guidelinePercent = roundTo(reference.guideline_percent, 3);
  const status =
    toolBottomPercentFromBottom >= guidelinePercent
      ? 'meets_guideline'
      : installPointPercentFromBottom >= guidelinePercent
        ? 'borderline'
        : 'below_guideline';

  return {
    kb_to_gl_m: roundTo(reference.kb_to_gl_m, 3),
    conductive_casing_set_depth_mkb: roundTo(reference.conductive_casing_set_depth_mkb, 3),
    conductive_casing_length_gl_m: conductiveCasingLengthGlM,
    install_point_distance_from_casing_bottom_m: installPointDistanceFromBottomM,
    install_point_percent_from_casing_bottom: installPointPercentFromBottom,
    tool_bottom_mkb: toolBottomMkb,
    tool_bottom_distance_from_casing_bottom_m: toolBottomDistanceFromBottomM,
    tool_bottom_percent_from_casing_bottom: toolBottomPercentFromBottom,
    guideline_percent: guidelinePercent,
    status,
  };
}
