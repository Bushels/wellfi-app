import type { Well } from '@/types';
import {
  componentLengthM,
  getCurrentCompletionSnapshot,
  getHighlightAnchorPoint,
  getLastSurveyedTrajectoryPoint,
  getProjectedTrajectoryPoints,
  getSurveyedTrajectoryPoints,
  getTelemetryPlacementMetric,
  type CompletionComponent,
  type TrajectoryPoint,
  type WellGeometryAsset,
} from '@/lib/wellGeometry';

interface WellTrajectoryPlateProps {
  well: Well;
  asset: WellGeometryAsset;
  heightClassName: string;
}

interface PlotPadding {
  left: number;
  right: number;
  top: number;
  bottom: number;
}

interface PlotTransform {
  scale: number;
  plotLeft: number;
  plotTop: number;
  plotWidth: number;
  plotHeight: number;
  mapX: (value: number) => number;
  mapY: (value: number) => number;
}

const SECTION_WIDTH = 760;
const SECTION_HEIGHT = 420;
const PLAN_WIDTH = 320;
const PLAN_HEIGHT = 240;
const STRIP_WIDTH = 920;
const STRIP_HEIGHT = 150;

function accentColor(componentId: CompletionComponent['id']): string {
  switch (componentId) {
    case 'pump':
      return '#d4a017';
    case 'slotted_tag_bar':
      return '#4ec3ff';
    case 'wellfi_tool':
      return '#1ecad3';
    case 'no_turn_tool':
      return '#5b7fff';
    case 'collar':
      return '#d7dde8';
    default:
      return '#d7dde8';
  }
}

function badgeClassName(componentId: CompletionComponent['id']): string {
  switch (componentId) {
    case 'pump':
      return 'border-amber-300/35 bg-amber-300/12 text-amber-100';
    case 'slotted_tag_bar':
      return 'border-sky-300/35 bg-sky-300/12 text-sky-100';
    case 'wellfi_tool':
      return 'border-cyan-300/35 bg-cyan-300/12 text-cyan-100';
    case 'no_turn_tool':
      return 'border-indigo-300/35 bg-indigo-300/12 text-indigo-100';
    case 'collar':
      return 'border-slate-200/25 bg-slate-200/10 text-slate-100';
    default:
      return 'border-slate-200/25 bg-slate-200/10 text-slate-100';
  }
}

function formatSignedDepth(value: number): string {
  const sign = value >= 0 ? '+' : '-';
  return `${sign}${Math.abs(value).toFixed(2)} m`;
}

function formatAngle(value: number): string {
  return `${value.toFixed(2)}\u00B0`;
}

function formatDate(date: string): string {
  return date;
}

function telemetryStatusLabel(status: 'meets_guideline' | 'borderline' | 'below_guideline'): string {
  switch (status) {
    case 'meets_guideline':
      return 'Meets 10% target';
    case 'borderline':
      return 'Borderline vs 10%';
    default:
      return 'Below 10% target';
  }
}

function telemetryTone(status: 'meets_guideline' | 'borderline' | 'below_guideline'): 'cyan' | 'amber' {
  return status === 'meets_guideline' ? 'cyan' : 'amber';
}

function formatTick(value: number): string {
  if (Math.abs(value) >= 100) return `${Math.round(value)}`;
  if (Math.abs(value) >= 10) return value.toFixed(1);
  return value.toFixed(2);
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
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

  if (ticks.length === 0) {
    ticks.push(Number(minValue.toFixed(3)), Number(maxValue.toFixed(3)));
  }

  return Array.from(new Set(ticks));
}

function createPlotTransform(
  xDomain: [number, number],
  yDomain: [number, number],
  width: number,
  height: number,
  padding: PlotPadding,
  options: { invertY: boolean },
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
    scale,
    plotLeft,
    plotTop,
    plotWidth,
    plotHeight,
    mapX: (value) => plotLeft + (value - xDomain[0]) * scale,
    mapY: (value) =>
      options.invertY
        ? plotTop + (yDomain[1] - value) * scale
        : plotTop + (value - yDomain[0]) * scale,
  };
}

function buildSvgPath(
  points: readonly TrajectoryPoint[],
  transform: PlotTransform,
  selectors: {
    x: (point: TrajectoryPoint) => number;
    y: (point: TrajectoryPoint) => number;
  },
): string {
  return points
    .map((point, index) => {
      const x = transform.mapX(selectors.x(point));
      const y = transform.mapY(selectors.y(point));
      return `${index === 0 ? 'M' : 'L'}${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(' ');
}

export function WellTrajectoryPlate({ well, asset, heightClassName }: WellTrajectoryPlateProps) {
  const snapshot = getCurrentCompletionSnapshot(asset);
  const highlight = getHighlightAnchorPoint(asset);
  const avgPumpRuntime = asset.summary_metrics?.find((metric) => metric.id === 'avg_pump_runtime_pre_wellfi') ?? null;
  const telemetryPlacement = highlight ? getTelemetryPlacementMetric(asset, highlight.component, highlight.anchor_md_m) : null;

  if (!snapshot || !highlight || !highlight.trajectory) {
    return (
      <div className={`flex items-center justify-center rounded-xl border border-slate-700/70 bg-slate-950/80 ${heightClassName}`}>
        <p className="px-6 text-center text-sm text-slate-400">
          Survey geometry is not available for this well yet.
        </p>
      </div>
    );
  }

  const surveyedPoints = getSurveyedTrajectoryPoints(asset.survey_points);
  const projectedPoints = getProjectedTrajectoryPoints(asset.survey_points);
  const lastSurveyPoint = getLastSurveyedTrajectoryPoint(asset.survey_points);
  const projectedTailPoints = projectedPoints.length > 0 && lastSurveyPoint ? [lastSurveyPoint, ...projectedPoints] : [];
  const projectedEndPoint = projectedPoints.at(-1) ?? null;
  const components = snapshot.components ?? [];

  const sectionPadding = { left: 80, right: 28, top: 32, bottom: 60 };
  const planPadding = { left: 58, right: 18, top: 24, bottom: 48 };
  const stripPadding = { left: 28, right: 28, top: 24, bottom: 34 };

  const sectionXDomain = extent(
    [...asset.survey_points.map((point) => point.vertical_section_m), highlight.trajectory.vertical_section_m],
    24,
    80,
  );
  const sectionYDomain = extent(
    [...asset.survey_points.map((point) => point.tvd_m), highlight.trajectory.tvd_m],
    22,
    80,
  );
  const sectionTransform = createPlotTransform(sectionXDomain, sectionYDomain, SECTION_WIDTH, SECTION_HEIGHT, sectionPadding, {
    invertY: false,
  });
  const sectionSurveyPath = buildSvgPath(surveyedPoints, sectionTransform, {
    x: (point) => point.vertical_section_m,
    y: (point) => point.tvd_m,
  });
  const sectionProjectionPath =
    projectedTailPoints.length > 1
      ? buildSvgPath(projectedTailPoints, sectionTransform, {
          x: (point) => point.vertical_section_m,
          y: (point) => point.tvd_m,
        })
      : '';

  const sectionAnchorX = sectionTransform.mapX(highlight.trajectory.vertical_section_m);
  const sectionAnchorY = sectionTransform.mapY(highlight.trajectory.tvd_m);
  const lastSurveySectionX = lastSurveyPoint ? sectionTransform.mapX(lastSurveyPoint.vertical_section_m) : null;
  const lastSurveySectionY = lastSurveyPoint ? sectionTransform.mapY(lastSurveyPoint.tvd_m) : null;
  const projectedSectionX = projectedEndPoint ? sectionTransform.mapX(projectedEndPoint.vertical_section_m) : null;
  const projectedSectionY = projectedEndPoint ? sectionTransform.mapY(projectedEndPoint.tvd_m) : null;

  const planXDomain = extent(
    [...asset.survey_points.map((point) => point.easting_offset_m), highlight.trajectory.easting_offset_m, 0],
    28,
    80,
  );
  const planYDomain = extent(
    [...asset.survey_points.map((point) => point.northing_offset_m), highlight.trajectory.northing_offset_m, 0],
    28,
    80,
  );
  const planTransform = createPlotTransform(planXDomain, planYDomain, PLAN_WIDTH, PLAN_HEIGHT, planPadding, {
    invertY: true,
  });
  const planSurveyPath = buildSvgPath(surveyedPoints, planTransform, {
    x: (point) => point.easting_offset_m,
    y: (point) => point.northing_offset_m,
  });
  const planProjectionPath =
    projectedTailPoints.length > 1
      ? buildSvgPath(projectedTailPoints, planTransform, {
          x: (point) => point.easting_offset_m,
          y: (point) => point.northing_offset_m,
        })
      : '';

  const planAnchorX = planTransform.mapX(highlight.trajectory.easting_offset_m);
  const planAnchorY = planTransform.mapY(highlight.trajectory.northing_offset_m);
  const originX = planTransform.mapX(0);
  const originY = planTransform.mapY(0);
  const sectionXTicks = buildTicks(sectionXDomain[0], sectionXDomain[1], 4);
  const sectionYTicks = buildTicks(sectionYDomain[0], sectionYDomain[1], 4);
  const planXTicks = buildTicks(planXDomain[0], planXDomain[1], 3);
  const planYTicks = buildTicks(planYDomain[0], planYDomain[1], 3);

  const stripTop = components.length > 0 ? Math.min(...components.map((component) => component.top_mkb)) : 0;
  const stripBottom = components.length > 0 ? Math.max(...components.map((component) => component.bottom_mkb)) : 1;
  const stripMetrics = {
    focusMin: Math.max(0, stripTop - 0.65),
    focusMax: stripBottom + 0.4,
  };
  const focusWidth = STRIP_WIDTH - stripPadding.left - stripPadding.right;
  const highlightStripX =
    stripPadding.left +
    ((highlight.anchor_md_m - stripMetrics.focusMin) / (stripMetrics.focusMax - stripMetrics.focusMin)) * focusWidth;
  const stripTicks = Array.from({ length: 6 }, (_, index) =>
    Number((stripMetrics.focusMin + ((stripMetrics.focusMax - stripMetrics.focusMin) * index) / 5).toFixed(2)),
  );

  return (
    <div className={`relative overflow-hidden rounded-xl border border-slate-700/70 ${heightClassName}`}>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(92,172,223,0.20),transparent_38%),radial-gradient(circle_at_bottom_right,rgba(212,160,23,0.10),transparent_32%),linear-gradient(180deg,#08111f_0%,#020617_100%)]" />
      <div className="relative flex h-full flex-col gap-4 p-4">
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full border border-slate-600/70 bg-slate-950/70 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-slate-200">
            Trajectory Plate
          </span>
          <span className="rounded-full border border-slate-600/70 bg-slate-950/70 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-slate-300">
            Event {asset.source_uwi}
          </span>
          {asset.survey_header_uwi && asset.survey_header_uwi !== asset.source_uwi ? (
            <span className="rounded-full border border-slate-600/70 bg-slate-950/70 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-slate-300">
              Survey {asset.survey_header_uwi}
            </span>
          ) : null}
          <span className={`rounded-full border px-3 py-1 text-[10px] uppercase tracking-[0.18em] ${badgeClassName(highlight.component.id)}`}>
            {highlight.label}
          </span>
          <span className="rounded-full border border-slate-600/70 bg-slate-950/70 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-slate-300">
            Snapshot {formatDate(snapshot.run_date)}
          </span>
        </div>

        <div className="grid gap-3 xl:grid-cols-4 2xl:grid-cols-5">
          {avgPumpRuntime ? (
            <SummaryCard
              label={avgPumpRuntime.label}
              value={`${avgPumpRuntime.value.toFixed(1)} ${avgPumpRuntime.unit}`}
              detail={avgPumpRuntime.context}
              tone="amber"
            />
          ) : null}
          <SummaryCard
            label="Surveyed MD"
            value={`${asset.last_survey_md_m.toFixed(2)} m`}
            detail={
              projectedEndPoint
                ? `Projection extends to ${asset.projected_td_md_m?.toFixed(2)} m MD as dashed tail.`
                : 'No projected tail in this file.'
            }
            tone="cyan"
          />
          {telemetryPlacement ? (
            <SummaryCard
              label="Telemetry Placement"
              value={`${telemetryPlacement.tool_bottom_percent_from_casing_bottom.toFixed(2)}% tool-bottom`}
              detail={`Top install point: ${telemetryPlacement.install_point_percent_from_casing_bottom.toFixed(2)}%. Basis: ${telemetryPlacement.conductive_casing_set_depth_mkb.toFixed(2)} mKB conductive casing set depth (${telemetryPlacement.conductive_casing_length_gl_m.toFixed(2)} mGL). ${telemetryStatusLabel(telemetryPlacement.status)}.`}
              tone={telemetryTone(telemetryPlacement.status)}
            />
          ) : null}
          <SummaryCard
            label="Install Inclination"
            value={formatAngle(highlight.trajectory.inclination_deg)}
            detail={`At ${highlight.anchor_md_m.toFixed(2)} mKB for the ${highlight.label.toLowerCase()}.`}
            tone="slate"
          />
          <SummaryCard
            label="Section Azimuth"
            value={
              asset.vertical_section_azimuth_deg != null
                ? `${asset.vertical_section_azimuth_deg.toFixed(3)}\u00B0T`
                : 'Not stated'
            }
            detail="TVD is referenced to Actual KB. Solid path is surveyed; dashed path is projected."
            tone="slate"
          />
        </div>

        <div className="grid min-h-0 flex-1 gap-4 xl:grid-cols-[minmax(0,1fr)_300px]">
          <div className="min-h-0 rounded-xl border border-slate-700/70 bg-slate-950/45 p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
            <div className="mb-3 flex flex-wrap items-end justify-between gap-3">
              <div>
                <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Section View</div>
                <div className="mt-1 text-sm font-semibold text-slate-100">Equal-scale deviation section from the final survey</div>
              </div>
              <div className="flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
                <LegendSwatch className="bg-gradient-to-r from-sky-300 to-amber-300" label="Surveyed" />
                {projectedTailPoints.length > 1 ? (
                  <LegendSwatch className="border-t-2 border-dashed border-amber-300" label="Projected TD" />
                ) : null}
              </div>
            </div>
            <svg viewBox={`0 0 ${SECTION_WIDTH} ${SECTION_HEIGHT}`} className="h-full min-h-[260px] w-full">
              <defs>
                <linearGradient id="trajectory-section-line" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#7dd3fc" />
                  <stop offset="100%" stopColor="#facc15" />
                </linearGradient>
              </defs>

              <rect
                x={sectionTransform.plotLeft}
                y={sectionTransform.plotTop}
                width={sectionTransform.plotWidth}
                height={sectionTransform.plotHeight}
                rx="18"
                fill="rgba(15,23,42,0.55)"
                stroke="rgba(148,163,184,0.18)"
              />

              {sectionYTicks.map((tick) => {
                const y = sectionTransform.mapY(tick);
                return (
                  <g key={`section-y-${tick}`}>
                    <line
                      x1={sectionTransform.plotLeft}
                      x2={sectionTransform.plotLeft + sectionTransform.plotWidth}
                      y1={y}
                      y2={y}
                      stroke="rgba(148,163,184,0.14)"
                      strokeDasharray="4 8"
                    />
                    <text x={18} y={y + 4} fill="#94a3b8" fontSize="10">
                      {formatTick(tick)}
                    </text>
                  </g>
                );
              })}

              {sectionXTicks.map((tick) => {
                const x = sectionTransform.mapX(tick);
                return (
                  <g key={`section-x-${tick}`}>
                    <line
                      x1={x}
                      x2={x}
                      y1={sectionTransform.plotTop}
                      y2={sectionTransform.plotTop + sectionTransform.plotHeight}
                      stroke="rgba(148,163,184,0.12)"
                      strokeDasharray="4 8"
                    />
                    <text x={x} y={SECTION_HEIGHT - 18} textAnchor="middle" fill="#94a3b8" fontSize="10">
                      {formatTick(tick)}
                    </text>
                  </g>
                );
              })}

              <path
                d={sectionSurveyPath}
                fill="none"
                stroke="url(#trajectory-section-line)"
                strokeWidth="6"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.16"
              />
              <path
                d={sectionSurveyPath}
                fill="none"
                stroke="url(#trajectory-section-line)"
                strokeWidth="3.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />

              {sectionProjectionPath ? (
                <path
                  d={sectionProjectionPath}
                  fill="none"
                  stroke="#fbbf24"
                  strokeWidth="2.4"
                  strokeDasharray="7 7"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              ) : null}

              {lastSurveySectionX != null && lastSurveySectionY != null ? (
                <>
                  <circle cx={lastSurveySectionX} cy={lastSurveySectionY} r="4.2" fill="#f8fafc" />
                  <text
                    x={clamp(lastSurveySectionX + 8, 96, SECTION_WIDTH - 84)}
                    y={clamp(lastSurveySectionY - 10, 26, SECTION_HEIGHT - 70)}
                    fill="#f8fafc"
                    fontSize="10"
                    fontWeight="700"
                  >
                    Last Survey
                  </text>
                </>
              ) : null}

              {projectedSectionX != null && projectedSectionY != null ? (
                <>
                  <circle cx={projectedSectionX} cy={projectedSectionY} r="4.2" fill="#fbbf24" />
                  <text
                    x={clamp(projectedSectionX + 8, 96, SECTION_WIDTH - 84)}
                    y={clamp(projectedSectionY - 10, 26, SECTION_HEIGHT - 70)}
                    fill="#fde68a"
                    fontSize="10"
                    fontWeight="700"
                  >
                    Projected TD
                  </text>
                </>
              ) : null}

              <line
                x1={sectionAnchorX}
                x2={sectionAnchorX}
                y1={sectionTransform.plotTop}
                y2={sectionTransform.plotTop + sectionTransform.plotHeight}
                stroke="rgba(78,195,255,0.7)"
                strokeDasharray="6 8"
              />
              <line
                x1={sectionTransform.plotLeft}
                x2={sectionAnchorX}
                y1={sectionAnchorY}
                y2={sectionAnchorY}
                stroke="rgba(78,195,255,0.7)"
                strokeDasharray="6 8"
              />
              <circle cx={sectionAnchorX} cy={sectionAnchorY} r="9" fill="rgba(78,195,255,0.16)" />
              <circle cx={sectionAnchorX} cy={sectionAnchorY} r="4.5" fill="#4ec3ff" />

              <g transform={`translate(${clamp(sectionAnchorX + 14, 96, SECTION_WIDTH - 274)} ${clamp(sectionAnchorY - 98, 44, SECTION_HEIGHT - 146)})`}>
                <rect
                  width="256"
                  height="96"
                  rx="14"
                  fill="rgba(2,6,23,0.88)"
                  stroke="rgba(78,195,255,0.35)"
                />
                <text x="14" y="22" fill="#f8fafc" fontSize="12" fontWeight="700">
                  {highlight.label}
                </text>
                <text x="14" y="40" fill="#94a3b8" fontSize="11">
                  MD {highlight.anchor_md_m.toFixed(2)} mKB
                </text>
                <text x="14" y="56" fill="#94a3b8" fontSize="11">
                  TVD {highlight.trajectory.tvd_m.toFixed(2)} m from KB
                </text>
                <text x="14" y="72" fill="#7dd3fc" fontSize="11" fontWeight="600">
                  Incl {formatAngle(highlight.trajectory.inclination_deg)}
                </text>
                {telemetryPlacement ? (
                  <text x="14" y="88" fill={telemetryPlacement.status === 'meets_guideline' ? '#7dd3fc' : '#fbbf24'} fontSize="11" fontWeight="600">
                    QA {telemetryPlacement.tool_bottom_percent_from_casing_bottom.toFixed(2)}% tool | {telemetryPlacement.install_point_percent_from_casing_bottom.toFixed(2)}% top
                  </text>
                ) : null}
                {!telemetryPlacement ? (
                  <text x="14" y="88" fill="#7dd3fc" fontSize="11" fontWeight="600">
                    Telemetry placement basis not configured
                  </text>
                ) : null}
              </g>

              <text
                x={(sectionTransform.plotLeft + sectionTransform.plotLeft + sectionTransform.plotWidth) / 2}
                y={SECTION_HEIGHT - 6}
                textAnchor="middle"
                fill="#cbd5e1"
                fontSize="11"
                letterSpacing="2"
              >
                VERTICAL SECTION (m)
              </text>
              <g transform={`translate(18 ${(sectionTransform.plotTop + sectionTransform.plotTop + sectionTransform.plotHeight) / 2}) rotate(-90)`}>
                <text textAnchor="middle" fill="#cbd5e1" fontSize="11" letterSpacing="2">
                  TVD FROM KB (m)
                </text>
              </g>
            </svg>
          </div>
          <div className="grid min-h-0 gap-4">
            <div className="rounded-xl border border-slate-700/70 bg-slate-950/45 p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
              <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Anchor Callout</div>
              <div className="mt-2 text-base font-semibold text-slate-100">{highlight.label}</div>
              <div className="mt-1 text-sm text-slate-400">{highlight.component.note ?? snapshot.label}</div>

              <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                <Metric label="OD" value={highlight.component.od_mm ? `${highlight.component.od_mm.toFixed(1)} mm` : 'N/A'} />
                <Metric label="Run Date" value={formatDate(snapshot.run_date)} />
                <Metric label="MD" value={`${highlight.anchor_md_m.toFixed(2)} mKB`} />
                <Metric label="TVD" value={`${highlight.trajectory.tvd_m.toFixed(2)} m KB`} />
                <Metric label="Install Angle" value={formatAngle(highlight.trajectory.inclination_deg)} />
                <Metric label="Azimuth" value={formatAngle(highlight.trajectory.azimuth_deg)} />
                {telemetryPlacement ? (
                  <Metric label="Top Install QA" value={`${telemetryPlacement.install_point_percent_from_casing_bottom.toFixed(2)}%`} />
                ) : null}
                {telemetryPlacement ? (
                  <Metric label="Tool Bottom QA" value={`${telemetryPlacement.tool_bottom_percent_from_casing_bottom.toFixed(2)}%`} />
                ) : null}
                {telemetryPlacement ? (
                  <Metric label="Casing Bottom" value={`${telemetryPlacement.conductive_casing_set_depth_mkb.toFixed(2)} mKB`} />
                ) : null}
                {telemetryPlacement ? (
                  <Metric label="Casing Length" value={`${telemetryPlacement.conductive_casing_length_gl_m.toFixed(2)} mGL`} />
                ) : null}
                {telemetryPlacement ? (
                  <Metric label="10% Guideline" value={telemetryStatusLabel(telemetryPlacement.status)} />
                ) : null}
                <Metric label="Northing" value={formatSignedDepth(highlight.trajectory.northing_offset_m)} />
                <Metric label="Easting" value={formatSignedDepth(highlight.trajectory.easting_offset_m)} />
              </div>

              <div className="mt-4 rounded-lg border border-slate-700/70 bg-slate-900/70 p-3 text-[11px] leading-relaxed text-slate-300">
                The marker is placed from the final survey stations using minimum-curvature interpolation at the current WellFi install point. Telemetry placement follows the lower-casing-section rule from the EM telemetry reference paper, using the intermediate conductive casing as the denominator. The tool-bottom percentage is the conservative QA check.
              </div>
            </div>

            <div className="rounded-xl border border-slate-700/70 bg-slate-950/45 p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
              <div className="mb-2 flex items-start justify-between gap-3">
                <div>
                  <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Plan View</div>
                  <div className="mt-1 text-sm font-semibold text-slate-100">Equal-scale horizontal displacement</div>
                </div>
                <div className="text-right text-[11px] text-slate-400">
                  <div>{well.name ?? asset.well_name}</div>
                  <div>Licence {asset.licence}</div>
                </div>
              </div>
              <svg viewBox={`0 0 ${PLAN_WIDTH} ${PLAN_HEIGHT}`} className="h-full min-h-[190px] w-full">
                <rect
                  x={planTransform.plotLeft}
                  y={planTransform.plotTop}
                  width={planTransform.plotWidth}
                  height={planTransform.plotHeight}
                  rx="16"
                  fill="rgba(15,23,42,0.55)"
                  stroke="rgba(148,163,184,0.18)"
                />

                {planYTicks.map((tick) => {
                  const y = planTransform.mapY(tick);
                  return (
                    <g key={`plan-y-${tick}`}>
                      <line
                        x1={planTransform.plotLeft}
                        x2={planTransform.plotLeft + planTransform.plotWidth}
                        y1={y}
                        y2={y}
                        stroke="rgba(148,163,184,0.12)"
                        strokeDasharray="4 7"
                      />
                      <text x={10} y={y + 4} fill="#94a3b8" fontSize="9">
                        {formatTick(tick)}
                      </text>
                    </g>
                  );
                })}

                {planXTicks.map((tick) => {
                  const x = planTransform.mapX(tick);
                  return (
                    <g key={`plan-x-${tick}`}>
                      <line
                        x1={x}
                        x2={x}
                        y1={planTransform.plotTop}
                        y2={planTransform.plotTop + planTransform.plotHeight}
                        stroke="rgba(148,163,184,0.12)"
                        strokeDasharray="4 7"
                      />
                      <text x={x} y={PLAN_HEIGHT - 14} textAnchor="middle" fill="#94a3b8" fontSize="9">
                        {formatTick(tick)}
                      </text>
                    </g>
                  );
                })}

                <line
                  x1={originX}
                  x2={originX}
                  y1={planTransform.plotTop}
                  y2={planTransform.plotTop + planTransform.plotHeight}
                  stroke="rgba(248,250,252,0.20)"
                  strokeDasharray="3 5"
                />
                <line
                  x1={planTransform.plotLeft}
                  x2={planTransform.plotLeft + planTransform.plotWidth}
                  y1={originY}
                  y2={originY}
                  stroke="rgba(248,250,252,0.20)"
                  strokeDasharray="3 5"
                />

                <path
                  d={planSurveyPath}
                  fill="none"
                  stroke="rgba(78,195,255,0.95)"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />

                {planProjectionPath ? (
                  <path
                    d={planProjectionPath}
                    fill="none"
                    stroke="#fbbf24"
                    strokeWidth="2.2"
                    strokeDasharray="6 6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                ) : null}

                <circle cx={originX} cy={originY} r="4" fill="#f8fafc" />
                <circle cx={planAnchorX} cy={planAnchorY} r="7" fill="rgba(78,195,255,0.18)" />
                <circle cx={planAnchorX} cy={planAnchorY} r="3.8" fill="#4ec3ff" />
                <text x={originX + 8} y={originY - 8} fill="#e2e8f0" fontSize="10" fontWeight="700">Surface</text>

                <text
                  x={(planTransform.plotLeft + planTransform.plotLeft + planTransform.plotWidth) / 2}
                  y={PLAN_HEIGHT - 2}
                  textAnchor="middle"
                  fill="#cbd5e1"
                  fontSize="10"
                  letterSpacing="1.6"
                >
                  EASTING OFFSET (m)
                </text>
                <g transform={`translate(14 ${(planTransform.plotTop + planTransform.plotTop + planTransform.plotHeight) / 2}) rotate(-90)`}>
                  <text textAnchor="middle" fill="#cbd5e1" fontSize="10" letterSpacing="1.6">
                    NORTHING OFFSET (m)
                  </text>
                </g>
              </svg>
            </div>

            <div className="rounded-xl border border-slate-700/70 bg-slate-950/45 p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
              <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Survey Context</div>
              <div className="mt-3 grid gap-2 text-sm text-slate-300">
                <ContextRow label="Well event" value={asset.source_uwi} />
                <ContextRow label="Survey header" value={asset.survey_header_uwi ?? 'Not found'} />
                <ContextRow label="Last surveyed MD" value={`${asset.last_survey_md_m.toFixed(2)} m`} />
                <ContextRow label="Projected TD" value={asset.projected_td_md_m ? `${asset.projected_td_md_m.toFixed(2)} m` : 'None'} />
                <ContextRow
                  label="VS azimuth"
                  value={asset.vertical_section_azimuth_deg != null ? `${asset.vertical_section_azimuth_deg.toFixed(3)}\u00B0 True` : 'Not found'}
                />
                {telemetryPlacement ? (
                  <ContextRow
                    label="Conductive Casing"
                    value={`${telemetryPlacement.conductive_casing_set_depth_mkb.toFixed(2)} mKB set depth`}
                  />
                ) : null}
                {telemetryPlacement ? (
                  <ContextRow
                    label="Telemetry QA"
                    value={
                      `${telemetryPlacement.tool_bottom_percent_from_casing_bottom.toFixed(2)}% tool | ${telemetryPlacement.install_point_percent_from_casing_bottom.toFixed(2)}% top`
                    }
                  />
                ) : null}
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-700/70 bg-slate-950/45 p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
          <div className="mb-3 flex flex-wrap items-end justify-between gap-3">
            <div>
              <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Current Completion Strip</div>
              <div className="mt-1 text-sm font-semibold text-slate-100">Focused interval around the current tool stack</div>
            </div>
            <div className="text-right text-[11px] text-slate-400">
              <div>{stripMetrics.focusMin.toFixed(2)} - {stripMetrics.focusMax.toFixed(2)} mKB</div>
            </div>
          </div>

          <svg viewBox={`0 0 ${STRIP_WIDTH} ${STRIP_HEIGHT}`} className="w-full">
            <line
              x1={stripPadding.left}
              x2={STRIP_WIDTH - stripPadding.right}
              y1={STRIP_HEIGHT - stripPadding.bottom}
              y2={STRIP_HEIGHT - stripPadding.bottom}
              stroke="rgba(148,163,184,0.35)"
            />
            {stripTicks.map((tick) => {
              const x =
                stripPadding.left +
                ((tick - stripMetrics.focusMin) / (stripMetrics.focusMax - stripMetrics.focusMin)) * focusWidth;
              return (
                <g key={`strip-tick-${tick}`}>
                  <line
                    x1={x}
                    x2={x}
                    y1={STRIP_HEIGHT - stripPadding.bottom}
                    y2={stripPadding.top}
                    stroke="rgba(148,163,184,0.12)"
                    strokeDasharray="4 6"
                  />
                  <text x={x} y={STRIP_HEIGHT - 10} textAnchor="middle" fill="#94a3b8" fontSize="10">
                    {tick.toFixed(2)}
                  </text>
                </g>
              );
            })}

            {snapshot.components.map((component, index) => {
              const x =
                stripPadding.left +
                ((component.top_mkb - stripMetrics.focusMin) / (stripMetrics.focusMax - stripMetrics.focusMin)) * focusWidth;
              const width = (componentLengthM(component) / (stripMetrics.focusMax - stripMetrics.focusMin)) * focusWidth;
              const y = 42 + index * 18;
              return (
                <g key={component.id}>
                  <rect
                    x={x}
                    y={y}
                    width={Math.max(width, 10)}
                    height="14"
                    rx="7"
                    fill={accentColor(component.id)}
                    opacity="0.82"
                  />
                  <text x={x + 8} y={y - 6} fill="#e2e8f0" fontSize="11" fontWeight="600">
                    {component.label}
                  </text>
                </g>
              );
            })}

            <line
              x1={highlightStripX}
              x2={highlightStripX}
              y1={stripPadding.top}
              y2={STRIP_HEIGHT - stripPadding.bottom}
              stroke="rgba(78,195,255,0.85)"
              strokeDasharray="6 6"
            />
            <circle cx={highlightStripX} cy={36} r="5" fill="#4ec3ff" />
            <text x={highlightStripX} y={22} textAnchor="middle" fill="#7dd3fc" fontSize="11" fontWeight="700">
              {highlight.anchor_md_m.toFixed(2)} mKB
            </text>
          </svg>
          <div className="mt-3 text-[11px] text-slate-400">{snapshot.source_note}</div>
        </div>
      </div>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  detail,
  tone,
}: {
  label: string;
  value: string;
  detail: string;
  tone: 'amber' | 'cyan' | 'slate';
}) {
  const toneClassName =
    tone === 'amber'
      ? 'border-amber-300/20 bg-amber-300/8 text-amber-100'
      : tone === 'cyan'
        ? 'border-cyan-300/20 bg-cyan-300/8 text-cyan-100'
        : 'border-slate-300/15 bg-slate-300/8 text-slate-100';

  return (
    <div className={`rounded-xl border p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] ${toneClassName}`}>
      <div className="text-[10px] font-semibold uppercase tracking-[0.22em] opacity-80">{label}</div>
      <div className="mt-1 text-xl font-semibold">{value}</div>
      <div className="mt-2 text-sm text-slate-300">{detail}</div>
    </div>
  );
}

function LegendSwatch({ className, label }: { className: string; label: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`block h-0 w-7 ${className}`} />
      <span>{label}</span>
    </div>
  );
}

function ContextRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-lg border border-slate-700/70 bg-slate-900/70 px-3 py-2">
      <span className="text-slate-400">{label}</span>
      <span className="text-right font-medium text-slate-100">{value}</span>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-700/70 bg-slate-900/70 p-2">
      <div className="text-[10px] uppercase tracking-[0.18em] text-slate-400">{label}</div>
      <div className="mt-1 text-sm font-medium text-slate-100">{value}</div>
    </div>
  );
}

export default WellTrajectoryPlate;
