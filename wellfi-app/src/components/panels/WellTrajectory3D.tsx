import { useMemo, useState, useCallback, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, Html } from '@react-three/drei';
import * as THREE from 'three';
import { Maximize2, RotateCcw } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  findWellGeometryAsset,
  getCurrentCompletionSnapshot,
  getHighlightAnchorPoint,
  getSurveyedTrajectoryPoints,
  getProjectedTrajectoryPoints,
  interpolateTrajectoryPoint,
  type CompletionComponent,
  type ReservoirLayer,
  type TrajectoryPoint,
} from '@/lib/wellGeometry';
import {
  buildTrajectoryCurve3D,
  buildAllLateralCurves,
  interpolatedToVec3,
  splitSurveyPointsAtMd,
  surveyPointToVec3,
  type LateralCurve3D,
  type TrajectoryBounds,
  type TrajectoryCurve3D,
} from '@/lib/trajectoryGeometry3D';
import type { Well } from '@/types';

const WELLBORE_RADIUS_M = 2.2;
const LATERAL_RADIUS_M = 1.6;
const LATERAL_PRODUCING_RADIUS_M = 2.0;
const TOOL_RADIUS_M = 4.2;
const TUBULAR_SEGMENTS = 512;
const LATERAL_TUBULAR_SEGMENTS = 192;
const RADIAL_SEGMENTS = 18;
const LATERAL_RADIAL_SEGMENTS = 12;

const COLOR_SURVEYED = '#22d3ee';
const COLOR_OPEN_HOLE = '#c2ab7d'; // warm sandstone/rock tone
const COLOR_PROJECTED = '#fbbf24';
const COLOR_TOOL = '#4ec3ff';
const COLOR_CASING = '#64748b';
const COLOR_PRODUCING_LATERAL = '#fbbf24';
const COLOR_RESERVOIR_DEFAULT = '#f59e0b';

/** Distinct, harmonious hues for each lateral leg (2-12). */
const LATERAL_COLORS: Record<number, string> = {
  2: '#7dd3fc', // sky
  3: '#60a5fa', // blue
  4: '#818cf8', // indigo
  5: '#a78bfa', // violet
  6: '#c084fc', // purple
  7: '#e879f9', // fuchsia
  8: '#f472b6', // pink
  9: COLOR_PRODUCING_LATERAL, // amber (highlighted for producing leg)
  10: '#fb923c', // orange
  11: '#f87171', // red
  12: '#84cc16', // lime
};

function colorForLateral(leg: number, isProducing: boolean): string {
  if (isProducing) return COLOR_PRODUCING_LATERAL;
  return LATERAL_COLORS[leg] ?? '#94a3b8';
}

const COMPONENT_TONE: Record<CompletionComponent['id'], { color: string; label: string }> = {
  pump: { color: '#f59e0b', label: 'Pump' },
  slotted_tag_bar: { color: '#7dd3fc', label: 'Slotted Tag Bar' },
  wellfi_tool: { color: '#22d3ee', label: 'WellFi Tool' },
  no_turn_tool: { color: '#a5b4fc', label: 'No-Turn Tool' },
  collar: { color: '#cbd5e1', label: 'Collar' },
};

interface WellTrajectory3DProps {
  well: Well;
}

interface SceneProps {
  geo: TrajectoryCurve3D;
  casedCurve: THREE.CatmullRomCurve3 | null;
  openHoleCurve: THREE.CatmullRomCurve3 | null;
  anchorWorldPos: THREE.Vector3 | null;
  anchorLabel: string | null;
  anchorDepthLabel: string | null;
  toolSegments: ToolSegmentWorld[];
  surfaceRadius: number;
  gridSize: number;
  lateralCurves: LateralCurve3D[];
  producingLeg: number | null;
  visibleLegs: ReadonlySet<number>;
  reservoir: ReservoirLayer | null;
  reservoirVisible: boolean;
  reservoirBounds: { min: THREE.Vector3; max: THREE.Vector3 } | null;
}

interface ToolSegmentWorld {
  id: CompletionComponent['id'];
  label: string;
  color: string;
  topVec: THREE.Vector3;
  bottomVec: THREE.Vector3;
  topMd: number;
  bottomMd: number;
  odMm: number | null;
}

function buildToolSegments(
  surveyPoints: readonly TrajectoryPoint[],
  components: readonly CompletionComponent[],
  verticalSectionAzimuthDeg: number | null,
): ToolSegmentWorld[] {
  return components
    .map((component) => {
      const top = interpolateTrajectoryPoint(surveyPoints, component.top_mkb, {
        verticalSectionAzimuthDeg,
      });
      const bottom = interpolateTrajectoryPoint(surveyPoints, component.bottom_mkb, {
        verticalSectionAzimuthDeg,
      });
      const topVec = interpolatedToVec3(top);
      const bottomVec = interpolatedToVec3(bottom);
      if (!topVec || !bottomVec) return null;
      const tone = COMPONENT_TONE[component.id] ?? { color: '#e2e8f0', label: component.label };
      return {
        id: component.id,
        label: component.label || tone.label,
        color: tone.color,
        topVec,
        bottomVec,
        topMd: component.top_mkb,
        bottomMd: component.bottom_mkb,
        odMm: component.od_mm,
      } satisfies ToolSegmentWorld;
    })
    .filter((value): value is ToolSegmentWorld => value != null);
}

function Scene({
  geo,
  casedCurve,
  openHoleCurve,
  anchorWorldPos,
  anchorLabel,
  anchorDepthLabel,
  toolSegments,
  surfaceRadius,
  gridSize,
  lateralCurves,
  producingLeg,
  visibleLegs,
  reservoir,
  reservoirVisible,
  reservoirBounds,
}: SceneProps) {
  const lateralTubes = useMemo(() => {
    return lateralCurves
      .filter((l) => !l.isParent && l.curve != null)
      .map((l) => {
        const isProducing = producingLeg != null && l.leg === producingLeg;
        const radius = isProducing ? LATERAL_PRODUCING_RADIUS_M : LATERAL_RADIUS_M;
        const geometry = new THREE.TubeGeometry(
          l.curve!,
          LATERAL_TUBULAR_SEGMENTS,
          radius,
          LATERAL_RADIAL_SEGMENTS,
          false,
        );
        return {
          leg: l.leg,
          label: l.label,
          color: colorForLateral(l.leg, isProducing),
          isProducing,
          geometry,
          endVec: l.endVec,
          kopTvdM: l.kopTvdM,
          kopMdM: l.kopMdM,
          totalMdM: l.totalMdM,
          lateralLengthM: l.lateralLengthM,
        };
      });
  }, [lateralCurves, producingLeg]);
  // Cased-section tube: the portion of the parent bore inside the intermediate
  // conductive casing (0 to casing shoe MD). Rendered with a casing shadow.
  const casedGeometry = useMemo(() => {
    const curve = casedCurve ?? geo.surveyedCurve;
    if (!curve) return null;
    return new THREE.TubeGeometry(
      curve,
      TUBULAR_SEGMENTS,
      WELLBORE_RADIUS_M,
      RADIAL_SEGMENTS,
      false,
    );
  }, [casedCurve, geo.surveyedCurve]);

  // Open-hole tube: the parent bore below the casing shoe. Rendered as bare
  // drilled hole (no casing shadow, warm rock tone, slightly thinner).
  const openHoleGeometry = useMemo(() => {
    if (!openHoleCurve) return null;
    return new THREE.TubeGeometry(
      openHoleCurve,
      Math.max(32, TUBULAR_SEGMENTS / 2),
      WELLBORE_RADIUS_M * 0.88,
      RADIAL_SEGMENTS,
      false,
    );
  }, [openHoleCurve]);

  const projectedGeometry = useMemo(() => {
    if (!geo.projectedCurve) return null;
    return new THREE.TubeGeometry(
      geo.projectedCurve,
      Math.max(32, TUBULAR_SEGMENTS / 4),
      WELLBORE_RADIUS_M * 0.88,
      RADIAL_SEGMENTS,
      false,
    );
  }, [geo.projectedCurve]);

  // Casing shadow: wider translucent tube surrounding ONLY the cased section.
  // When the casing shoe hasn't been identified we fall back to the whole bore.
  const casingGeometry = useMemo(() => {
    const curve = casedCurve ?? geo.surveyedCurve;
    if (!curve) return null;
    return new THREE.TubeGeometry(
      curve,
      Math.max(32, TUBULAR_SEGMENTS / 2),
      WELLBORE_RADIUS_M * 2.4,
      RADIAL_SEGMENTS,
      false,
    );
  }, [casedCurve, geo.surveyedCurve]);

  // Tool segments rendered as their own tubes so they sit "inside" the wellbore.
  const toolTubes = useMemo(() => {
    return toolSegments.map((segment) => {
      const curve = new THREE.LineCurve3(segment.topVec, segment.bottomVec);
      const length = segment.topVec.distanceTo(segment.bottomVec);
      const geometry = new THREE.TubeGeometry(
        curve,
        4,
        // Scale tool radius by OD so pump is fatter than slim WellFi.
        segment.odMm != null ? Math.max(1.4, (segment.odMm / 203.6) * TOOL_RADIUS_M) : TOOL_RADIUS_M * 0.7,
        RADIAL_SEGMENTS,
        false,
      );
      return { segment, geometry, length };
    });
  }, [toolSegments]);

  return (
    <>
      {/* KB surface disc */}
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[surfaceRadius, 64]} />
        <meshStandardMaterial
          color="#0b1324"
          roughness={0.95}
          metalness={0.1}
          transparent
          opacity={0.85}
        />
      </mesh>

      {/* Reference grid at KB level */}
      <Grid
        args={[gridSize, gridSize]}
        position={[0, 0.1, 0]}
        cellSize={50}
        cellThickness={0.8}
        cellColor="#3b4d6b"
        sectionSize={250}
        sectionThickness={1.4}
        sectionColor="#6b84aa"
        fadeDistance={gridSize * 0.95}
        fadeStrength={0.9}
        infiniteGrid={false}
      />

      {/* Casing shadow (translucent wider tube) */}
      {casingGeometry ? (
        <mesh geometry={casingGeometry}>
          <meshStandardMaterial
            color={COLOR_CASING}
            transparent
            opacity={0.22}
            roughness={0.55}
            metalness={0.4}
            side={THREE.DoubleSide}
          />
        </mesh>
      ) : null}

      {/* Reservoir formation slab (translucent amber volume between top/base TVDs). */}
      {reservoir && reservoirVisible && reservoirBounds ? (
        <ReservoirSlab reservoir={reservoir} bounds={reservoirBounds} />
      ) : null}

      {/* Parent bore — cased section (inside intermediate conductive casing). */}
      {casedGeometry ? (
        <mesh geometry={casedGeometry} castShadow>
          <meshStandardMaterial
            color={COLOR_SURVEYED}
            emissive={COLOR_SURVEYED}
            emissiveIntensity={0.55}
            roughness={0.22}
            metalness={0.45}
            toneMapped={false}
          />
        </mesh>
      ) : null}

      {/* Parent bore — open-hole section (below the casing shoe). Bare rock,
          no casing shadow, slightly thinner tube in a warm sandstone tone. */}
      {openHoleGeometry ? (
        <mesh geometry={openHoleGeometry} castShadow>
          <meshStandardMaterial
            color={COLOR_OPEN_HOLE}
            emissive={COLOR_OPEN_HOLE}
            emissiveIntensity={0.2}
            roughness={0.75}
            metalness={0.05}
            toneMapped={false}
          />
        </mesh>
      ) : null}

      {/* Open-hole multilateral legs */}
      {lateralTubes
        .filter((t) => visibleLegs.has(t.leg))
        .map((t) => (
          <group key={`lateral-${t.leg}`}>
            <mesh geometry={t.geometry}>
              <meshStandardMaterial
                color={t.color}
                emissive={t.color}
                emissiveIntensity={t.isProducing ? 0.65 : 0.35}
                roughness={0.32}
                metalness={0.45}
                transparent={!t.isProducing}
                opacity={t.isProducing ? 1.0 : 0.78}
                toneMapped={false}
              />
            </mesh>
            {t.endVec ? (
              <Html
                position={t.endVec.toArray()}
                distanceFactor={Math.max(120, surfaceRadius / 2)}
                style={{ pointerEvents: 'none' }}
              >
                <div
                  className={`whitespace-nowrap rounded-md border px-1.5 py-0.5 text-[10px] font-semibold shadow-md ${
                    t.isProducing
                      ? 'border-amber-300/60 bg-amber-500/30 text-amber-50'
                      : 'border-slate-500/50 bg-slate-950/80 text-slate-200'
                  }`}
                  style={t.isProducing ? { boxShadow: `0 0 12px ${t.color}` } : undefined}
                >
                  L{String(t.leg).padStart(2, '0')}
                  {t.isProducing ? ' · PRODUCING' : ''}
                </div>
              </Html>
            ) : null}
          </group>
        ))}

      {/* Projected tail */}
      {projectedGeometry ? (
        <mesh geometry={projectedGeometry}>
          <meshStandardMaterial
            color={COLOR_PROJECTED}
            transparent
            opacity={0.7}
            roughness={0.4}
            metalness={0.2}
            emissive={COLOR_PROJECTED}
            emissiveIntensity={0.4}
            toneMapped={false}
          />
        </mesh>
      ) : null}

      {/* Tool stack as tubes "inside" the wellbore */}
      {toolTubes.map(({ segment, geometry }) => (
        <mesh key={segment.id} geometry={geometry}>
          <meshStandardMaterial
            color={segment.color}
            emissive={segment.color}
            emissiveIntensity={0.45}
            roughness={0.3}
            metalness={0.7}
          />
        </mesh>
      ))}

      {/* WellFi install point marker */}
      {anchorWorldPos ? (
        <group position={anchorWorldPos.toArray()}>
          <mesh>
            <sphereGeometry args={[TOOL_RADIUS_M * 1.3, 24, 24]} />
            <meshStandardMaterial
              color={COLOR_TOOL}
              emissive={COLOR_TOOL}
              emissiveIntensity={0.9}
              transparent
              opacity={0.35}
            />
          </mesh>
          <mesh>
            <sphereGeometry args={[TOOL_RADIUS_M * 0.55, 24, 24]} />
            <meshStandardMaterial
              color="#f0fbff"
              emissive={COLOR_TOOL}
              emissiveIntensity={1.2}
            />
          </mesh>
          <Html
            position={[TOOL_RADIUS_M * 2.2, TOOL_RADIUS_M * 1.5, 0]}
            distanceFactor={Math.max(80, surfaceRadius / 2)}
            style={{ pointerEvents: 'none' }}
          >
            <div className="whitespace-nowrap rounded-md border border-cyan-300/40 bg-slate-950/85 px-2 py-1 text-[11px] font-semibold text-cyan-100 shadow-lg">
              {anchorLabel ?? 'Anchor'}
              {anchorDepthLabel ? (
                <span className="ml-2 font-normal text-slate-300">{anchorDepthLabel}</span>
              ) : null}
            </div>
          </Html>
        </group>
      ) : null}

      {/* Surface marker + label */}
      <mesh position={[0, 0.2, 0]}>
        <ringGeometry args={[WELLBORE_RADIUS_M * 0.9, WELLBORE_RADIUS_M * 1.6, 32]} />
        <meshStandardMaterial color="#f1f5f9" emissive="#f1f5f9" emissiveIntensity={0.4} />
      </mesh>
      <Html position={[0, 6, 0]} distanceFactor={Math.max(80, surfaceRadius / 2)} style={{ pointerEvents: 'none' }}>
        <div className="whitespace-nowrap rounded-md border border-slate-500/60 bg-slate-900/85 px-2 py-1 text-[10px] font-semibold uppercase tracking-widest text-slate-200">
          KB / Surface
        </div>
      </Html>
    </>
  );
}

export function WellTrajectory3D({ well }: WellTrajectory3DProps) {
  const asset = useMemo(() => findWellGeometryAsset(well), [well]);

  const geo = useMemo(() => {
    if (!asset) return null;
    return buildTrajectoryCurve3D(
      getSurveyedTrajectoryPoints(asset.survey_points),
      getProjectedTrajectoryPoints(asset.survey_points),
    );
  }, [asset]);

  // Split the parent bore at the intermediate casing shoe. Cased above the
  // shoe (inside steel), open-hole below (pilot extension into reservoir).
  const { casedCurve, openHoleCurve, casingShoeMd } = useMemo(() => {
    if (!asset) return { casedCurve: null, openHoleCurve: null, casingShoeMd: null };
    const shoeMd = asset.telemetry_placement_reference?.conductive_casing_set_depth_mkb ?? null;
    if (shoeMd == null) {
      return { casedCurve: null, openHoleCurve: null, casingShoeMd: null };
    }
    const surveyed = getSurveyedTrajectoryPoints(asset.survey_points);
    const { casedPoints, openHolePoints } = splitSurveyPointsAtMd(
      surveyed,
      shoeMd,
      asset.vertical_section_azimuth_deg,
    );
    const casedVecs = casedPoints.map((p) => surveyPointToVec3(p));
    const openHoleVecs = openHolePoints.map((p) => surveyPointToVec3(p));
    return {
      casedCurve: casedVecs.length >= 2
        ? new THREE.CatmullRomCurve3(casedVecs, false, 'catmullrom', 0.5)
        : null,
      openHoleCurve: openHoleVecs.length >= 2
        ? new THREE.CatmullRomCurve3(openHoleVecs, false, 'catmullrom', 0.5)
        : null,
      casingShoeMd: shoeMd,
    };
  }, [asset]);

  const highlight = useMemo(() => (asset ? getHighlightAnchorPoint(asset) : null), [asset]);
  const snapshot = useMemo(() => (asset ? getCurrentCompletionSnapshot(asset) : null), [asset]);

  const toolSegments = useMemo(() => {
    if (!asset || !snapshot) return [];
    return buildToolSegments(
      getSurveyedTrajectoryPoints(asset.survey_points),
      snapshot.components,
      asset.vertical_section_azimuth_deg,
    );
  }, [asset, snapshot]);

  const anchorWorldPos = useMemo(() => {
    if (!highlight?.trajectory) return null;
    return interpolatedToVec3(highlight.trajectory);
  }, [highlight]);

  const lateralCurvesResult = useMemo(() => {
    if (!asset?.laterals || asset.laterals.length === 0) return null;
    return buildAllLateralCurves(asset.laterals);
  }, [asset]);

  const producingLeg = asset?.producing_leg ?? null;

  const lateralCurves = lateralCurvesResult?.curves ?? [];
  const nonParentLaterals = lateralCurves.filter((l) => !l.isParent);

  const [visibleLegs, setVisibleLegs] = useState<Set<number>>(() => {
    return new Set(nonParentLaterals.map((l) => l.leg));
  });

  // Reset visibility set when the well changes.
  useEffect(() => {
    setVisibleLegs(new Set(nonParentLaterals.map((l) => l.leg)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [asset?.source_uwi]);

  // Production diagnostics — visible in browser DevTools if the 3D scene
  // doesn't render as expected on a deployed build. Tagged with [WellFi/3D]
  // so it's easy to grep alongside other module logs.
  useEffect(() => {
    if (!asset || !geo || !geo.surveyedCurve) {
      console.warn('[WellFi/3D] no 3D asset for well', { wellId: well.id, name: well.name, hasAsset: !!asset, hasGeo: !!geo });
      return;
    }
    console.info('[WellFi/3D] state', {
      wellId: well.id,
      name: well.name,
      sourceUwi: asset.source_uwi,
      surveyName: asset.survey_name,
      surveyedPoints: geo.surveyedPoints.length,
      lateralCount: lateralCurvesResult?.curves.length ?? 0,
      producingLeg,
    });
  }, [well.id, well.name, asset, geo, lateralCurvesResult, producingLeg]);

  const toggleLeg = useCallback((leg: number) => {
    setVisibleLegs((prev) => {
      const next = new Set(prev);
      if (next.has(leg)) next.delete(leg);
      else next.add(leg);
      return next;
    });
  }, []);

  const showAllLegs = useCallback(() => {
    setVisibleLegs(new Set(nonParentLaterals.map((l) => l.leg)));
  }, [nonParentLaterals]);

  const hideAllLegs = useCallback(() => {
    setVisibleLegs(new Set());
  }, []);

  const [reservoirVisible, setReservoirVisible] = useState(true);
  const toggleReservoir = useCallback(() => setReservoirVisible((v) => !v), []);

  const [fullscreenOpen, setFullscreenOpen] = useState(false);
  const [resetKey, setResetKey] = useState(0);
  const handleResetView = useCallback(() => setResetKey((k) => k + 1), []);

  // Combine the parent bore's bounds with lateral bounds so the camera can
  // frame everything that's visible.
  const combinedBounds: TrajectoryBounds = useMemo(() => {
    if (!geo) {
      return lateralCurvesResult?.bounds ?? {
        min: new THREE.Vector3(), max: new THREE.Vector3(),
        center: new THREE.Vector3(), size: new THREE.Vector3(), radius: 0,
      };
    }
    if (!lateralCurvesResult || visibleLegs.size === 0) return geo.bounds;
    const box = new THREE.Box3();
    box.expandByPoint(geo.bounds.min);
    box.expandByPoint(geo.bounds.max);
    for (const lc of lateralCurvesResult.curves) {
      if (!lc.isParent && !visibleLegs.has(lc.leg)) continue;
      for (const p of lc.points) box.expandByPoint(p);
    }
    const size = new THREE.Vector3();
    const center = new THREE.Vector3();
    box.getSize(size);
    box.getCenter(center);
    return { min: box.min.clone(), max: box.max.clone(), center, size, radius: size.length() / 2 };
  }, [geo, lateralCurvesResult, visibleLegs]);

  if (!asset || !geo || !geo.surveyedCurve) {
    return (
      <Card className="border-slate-700/70 bg-slate-950/45">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-semibold text-slate-200">3D Wellbore</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-400">
            3D trajectory is not available for this well yet. Add a directional survey to
            <code className="mx-1 rounded bg-slate-800/70 px-1 py-0.5 text-[11px] text-slate-200">
              src/lib/wellGeometry.ts
            </code>
            to enable this view.
          </p>
        </CardContent>
      </Card>
    );
  }

  const surveyedLengthM = geo.surveyedLengthM;
  const maxTvdM = geo.maxTvdM;
  const horizontalReach = Math.hypot(
    geo.bounds.size.x,
    geo.bounds.size.z,
  );

  const anchorDepthLabel = highlight
    ? `MD ${highlight.anchor_md_m.toFixed(1)} m · TVD ${highlight.trajectory?.tvd_m.toFixed(1) ?? '—'} m`
    : null;

  return (
    <Card className="border-slate-700/70 bg-slate-950/45">
      <CardHeader className="pb-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <CardTitle className="text-sm font-semibold text-slate-200">
              3D Wellbore · Navigate
            </CardTitle>
            <p className="mt-1 text-[11px] text-slate-400">
              Drag to rotate · scroll to zoom · right-drag to pan. Trajectory is to
              scale; tube radius is visually exaggerated.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="h-7 border-slate-600/70 bg-slate-900/70 text-slate-200 hover:bg-slate-800"
              onClick={handleResetView}
            >
              <RotateCcw className="mr-1 h-3 w-3" /> Reset view
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="h-7 border-slate-600/70 bg-slate-900/70 text-slate-200 hover:bg-slate-800"
              onClick={() => setFullscreenOpen(true)}
            >
              <Maximize2 className="mr-1 h-3 w-3" /> Fullscreen
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <Trajectory3DViewport
          key={resetKey}
          geo={geo}
          casedCurve={casedCurve}
          openHoleCurve={openHoleCurve}
          toolSegments={toolSegments}
          anchorWorldPos={anchorWorldPos}
          anchorLabel={highlight?.label ?? null}
          anchorDepthLabel={anchorDepthLabel}
          surveyedPoints={asset.survey_points}
          heightClassName="h-[520px]"
          lateralCurves={lateralCurves}
          producingLeg={producingLeg}
          visibleLegs={visibleLegs}
          combinedBounds={combinedBounds}
          reservoir={asset.reservoir ?? null}
          reservoirVisible={reservoirVisible}
        />

        <div className="mt-3 grid grid-cols-2 gap-2 text-[11px] text-slate-400 sm:grid-cols-4">
          <Metric label="Parent bore" value={`${surveyedLengthM.toFixed(1)} m MD`} />
          <Metric label="Max TVD" value={`${maxTvdM.toFixed(1)} m`} />
          <Metric label="Horizontal reach" value={`${horizontalReach.toFixed(1)} m`} />
          <Metric
            label={nonParentLaterals.length > 0 ? 'Laterals' : 'VS azimuth'}
            value={
              nonParentLaterals.length > 0
                ? `${nonParentLaterals.length} legs / ${Math.round(
                    nonParentLaterals.reduce((sum, l) => sum + l.lateralLengthM, 0),
                  )} m total`
                : asset.vertical_section_azimuth_deg != null
                  ? `${asset.vertical_section_azimuth_deg.toFixed(1)}° T`
                  : '—'
            }
          />
        </div>

        {nonParentLaterals.length > 0 ? (
          <LateralLegend
            laterals={nonParentLaterals}
            producingLeg={producingLeg}
            visibleLegs={visibleLegs}
            onToggle={toggleLeg}
            onShowAll={showAllLegs}
            onHideAll={hideAllLegs}
          />
        ) : null}

        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-slate-400">
          <LegendSwatch color={COLOR_SURVEYED} label="Cased bore" />
          {openHoleCurve ? (
            <LegendSwatch color={COLOR_OPEN_HOLE} label="Open hole" />
          ) : null}
          {geo.projectedCurve ? (
            <LegendSwatch color={COLOR_PROJECTED} label="Projected to TD" />
          ) : null}
          <LegendSwatch color={COLOR_TOOL} label="WellFi install point" />
          {asset.reservoir ? (
            <button
              type="button"
              onClick={toggleReservoir}
              className={`flex items-center gap-1.5 rounded border px-1.5 py-0.5 text-[11px] transition-colors ${
                reservoirVisible
                  ? 'border-amber-400/60 bg-amber-500/15 text-amber-100'
                  : 'border-slate-600/60 bg-slate-900/60 text-slate-400 hover:bg-slate-800/60'
              }`}
            >
              <span
                className="inline-block h-2 w-4 rounded-sm"
                style={{
                  backgroundColor: reservoirVisible ? COLOR_RESERVOIR_DEFAULT : `${COLOR_RESERVOIR_DEFAULT}33`,
                  boxShadow: reservoirVisible ? `0 0 6px ${COLOR_RESERVOIR_DEFAULT}aa` : undefined,
                }}
              />
              <span>
                {asset.reservoir.name} ({asset.reservoir.top_tvd_m.toFixed(0)}-
                {asset.reservoir.base_tvd_m.toFixed(0)} m TVD)
              </span>
            </button>
          ) : null}
          {casingShoeMd != null ? (
            <span className="text-slate-500">Casing shoe {casingShoeMd.toFixed(0)} m MD</span>
          ) : null}
          <span className="text-slate-500">Tube radius ≈ {WELLBORE_RADIUS_M.toFixed(1)} m (not to scale)</span>
        </div>
      </CardContent>

      <Dialog open={fullscreenOpen} onOpenChange={setFullscreenOpen}>
        <DialogContent className="max-w-[96vw] border-slate-700 bg-slate-950 p-0 sm:rounded-xl">
          <DialogHeader className="border-b border-slate-800 px-4 py-3">
            <DialogTitle className="text-sm font-semibold text-slate-200">
              3D Wellbore · {asset.well_name}
            </DialogTitle>
          </DialogHeader>
          <div className="p-3">
            <Trajectory3DViewport
              geo={geo}
              casedCurve={casedCurve}
              openHoleCurve={openHoleCurve}
              toolSegments={toolSegments}
              anchorWorldPos={anchorWorldPos}
              anchorLabel={highlight?.label ?? null}
              anchorDepthLabel={anchorDepthLabel}
              surveyedPoints={asset.survey_points}
              heightClassName="h-[80vh]"
              lateralCurves={lateralCurves}
              producingLeg={producingLeg}
              visibleLegs={visibleLegs}
              combinedBounds={combinedBounds}
              reservoir={asset.reservoir ?? null}
              reservoirVisible={reservoirVisible}
            />
          </div>
        </DialogContent>
      </Dialog>
    </Card>
  );
}

interface ViewportProps {
  geo: TrajectoryCurve3D;
  casedCurve: THREE.CatmullRomCurve3 | null;
  openHoleCurve: THREE.CatmullRomCurve3 | null;
  toolSegments: ToolSegmentWorld[];
  anchorWorldPos: THREE.Vector3 | null;
  anchorLabel: string | null;
  anchorDepthLabel: string | null;
  surveyedPoints: readonly TrajectoryPoint[];
  heightClassName: string;
  lateralCurves: LateralCurve3D[];
  producingLeg: number | null;
  visibleLegs: ReadonlySet<number>;
  combinedBounds: TrajectoryBounds;
  reservoir: ReservoirLayer | null;
  reservoirVisible: boolean;
}

function Trajectory3DViewport({
  geo,
  casedCurve,
  openHoleCurve,
  toolSegments,
  anchorWorldPos,
  anchorLabel,
  anchorDepthLabel,
  surveyedPoints,
  heightClassName,
  lateralCurves,
  producingLeg,
  visibleLegs,
  combinedBounds,
  reservoir,
  reservoirVisible,
}: ViewportProps) {
  const target = combinedBounds.center;
  const size = Math.max(combinedBounds.size.x, combinedBounds.size.y, combinedBounds.size.z);
  const distance = Math.max(size * 1.6, 220);
  const cameraPosition: [number, number, number] = [
    target.x + distance * 0.55,
    target.y + distance * 0.75,
    target.z + distance * 0.55,
  ];
  const gridSize = Math.max(size * 2.2, 600);
  const surfaceRadius = Math.max(size * 1.2, 300);

  // Early-calculated first surveyed vector, useful for the surface connector line.
  const firstSurveyVec = useMemo(() => {
    if (surveyedPoints.length === 0) return null;
    return surveyPointToVec3(surveyedPoints[0]);
  }, [surveyedPoints]);

  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // R3F's internal ResizeObserver occasionally misses the initial measurement
    // when mounted inside a Suspense boundary (lazy-loaded chunk). Nudging with
    // a synthetic resize on mount makes the Canvas pick up its parent size.
    const id = window.setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 16);
    return () => window.clearTimeout(id);
  }, []);

  return (
    <div
      ref={containerRef}
      className={`relative w-full overflow-hidden rounded-xl border border-slate-700/80 bg-[#0b1426] ${heightClassName}`}
    >
      <Canvas
        shadows
        // frameloop="always" is intentional here — OrbitControls below uses
        // enableDamping, and frameloop="demand" makes damping animation choppy.
        // See .claude/skills/well-trajectory-visualization/SKILL.md for the
        // empirical reasoning.
        frameloop="always"
        camera={{ position: cameraPosition, fov: 42, near: 0.5, far: Math.max(size * 12, 4000) }}
        gl={{ antialias: true, alpha: false, preserveDrawingBuffer: true }}
        onCreated={() => console.info('[WellFi/3D] canvas ready')}
      >
        <color attach="background" args={[0x0b1426]} />
        <fog attach="fog" args={[0x0b1426, distance * 2.5, distance * 8]} />

        <ambientLight intensity={0.85} />
        <hemisphereLight args={['#9fc4ff', '#1a2a44', 0.5]} />
        <directionalLight
          position={[size, size * 1.8, size]}
          intensity={1.35}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <directionalLight position={[-size, size * 0.4, -size]} intensity={0.65} color="#6ea8ff" />
        <directionalLight position={[0, size * 0.6, -size * 1.5]} intensity={0.35} color="#ffd28a" />

        <Scene
          geo={geo}
          casedCurve={casedCurve}
          openHoleCurve={openHoleCurve}
          anchorWorldPos={anchorWorldPos}
          anchorLabel={anchorLabel}
          anchorDepthLabel={anchorDepthLabel}
          toolSegments={toolSegments}
          surfaceRadius={surfaceRadius}
          gridSize={gridSize}
          lateralCurves={lateralCurves}
          producingLeg={producingLeg}
          visibleLegs={visibleLegs}
          reservoir={reservoir}
          reservoirVisible={reservoirVisible}
          reservoirBounds={{ min: combinedBounds.min, max: combinedBounds.max }}
        />

        {/* Surface connector: short line from KB (origin) straight down to the first surveyed station. */}
        {firstSurveyVec ? (
          <CylinderBetween
            from={new THREE.Vector3(0, 0, 0)}
            to={firstSurveyVec}
            radius={WELLBORE_RADIUS_M}
            color={COLOR_SURVEYED}
          />
        ) : null}

        <OrbitControls
          target={[target.x, target.y, target.z]}
          enablePan
          enableDamping
          dampingFactor={0.08}
          minDistance={size * 0.15}
          maxDistance={size * 6}
          makeDefault
        />
      </Canvas>
    </div>
  );
}

function ReservoirSlab({
  reservoir,
  bounds,
}: {
  reservoir: ReservoirLayer;
  bounds: { min: THREE.Vector3; max: THREE.Vector3 };
}) {
  // Horizontal extent = combined well bounds + a ~20% margin so laterals always
  // sit inside the reservoir footprint visually, even with a few legs visible.
  const topY = -reservoir.top_tvd_m;
  const baseY = -reservoir.base_tvd_m;

  const marginX = Math.max((bounds.max.x - bounds.min.x) * 0.1, 80);
  const marginZ = Math.max((bounds.max.z - bounds.min.z) * 0.1, 80);
  const sizeX = bounds.max.x - bounds.min.x + marginX * 2;
  const sizeZ = bounds.max.z - bounds.min.z + marginZ * 2;
  const centerX = (bounds.min.x + bounds.max.x) / 2;
  const centerZ = (bounds.min.z + bounds.max.z) / 2;

  const color = reservoir.color_rgba
    ? new THREE.Color(...reservoir.color_rgba.slice(0, 3))
    : new THREE.Color(COLOR_RESERVOIR_DEFAULT);

  return (
    <group>
      {/* Two horizontal planes at the reservoir top + base. No volumetric box —
          laterals between the planes are fully visible. */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[centerX, topY, centerZ]}>
        <planeGeometry args={[sizeX, sizeZ]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.32}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[centerX, baseY, centerZ]}>
        <planeGeometry args={[sizeX, sizeZ]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
      <Html
        position={[bounds.min.x - marginX * 0.3, topY + 2, centerZ]}
        distanceFactor={Math.max(120, sizeX / 3)}
        style={{ pointerEvents: 'none' }}
      >
        <div className="whitespace-nowrap rounded border border-amber-400/50 bg-slate-950/85 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-amber-200 shadow-md">
          {reservoir.name} top · {reservoir.top_tvd_m.toFixed(1)} m TVD
        </div>
      </Html>
      <Html
        position={[bounds.min.x - marginX * 0.3, baseY - 2, centerZ]}
        distanceFactor={Math.max(120, sizeX / 3)}
        style={{ pointerEvents: 'none' }}
      >
        <div className="whitespace-nowrap rounded border border-amber-400/40 bg-slate-950/80 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-amber-200/80 shadow-md">
          {reservoir.name} base · {reservoir.base_tvd_m.toFixed(1)} m TVD
        </div>
      </Html>
    </group>
  );
}

function CylinderBetween({
  from,
  to,
  radius,
  color,
}: {
  from: THREE.Vector3;
  to: THREE.Vector3;
  radius: number;
  color: string;
}) {
  const { position, quaternion, length } = useMemo(() => {
    const dir = new THREE.Vector3().subVectors(to, from);
    const len = dir.length();
    const mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);
    const up = new THREE.Vector3(0, 1, 0);
    const axis = dir.clone().normalize();
    const quat = new THREE.Quaternion().setFromUnitVectors(up, axis);
    return { position: mid.toArray() as [number, number, number], quaternion: quat, length: len };
  }, [from, to]);

  if (length < 0.001) return null;

  return (
    <mesh position={position} quaternion={quaternion}>
      <cylinderGeometry args={[radius, radius, length, 18]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.15}
        roughness={0.35}
        metalness={0.55}
      />
    </mesh>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-700/70 bg-slate-900/60 px-2 py-1.5">
      <div className="text-[10px] uppercase tracking-[0.18em] text-slate-500">{label}</div>
      <div className="mt-0.5 text-[12px] font-semibold text-slate-200">{value}</div>
    </div>
  );
}

interface LateralLegendProps {
  laterals: LateralCurve3D[];
  producingLeg: number | null;
  visibleLegs: ReadonlySet<number>;
  onToggle: (leg: number) => void;
  onShowAll: () => void;
  onHideAll: () => void;
}

function LateralLegend({
  laterals,
  producingLeg,
  visibleLegs,
  onToggle,
  onShowAll,
  onHideAll,
}: LateralLegendProps) {
  return (
    <div className="mt-3 rounded-lg border border-slate-700/70 bg-slate-900/50 p-2">
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">
          Laterals · toggle to compare
        </span>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={onShowAll}
            className="rounded border border-slate-600/70 bg-slate-800/70 px-1.5 py-0.5 text-[10px] font-medium text-slate-200 hover:bg-slate-700"
          >
            All
          </button>
          <button
            type="button"
            onClick={onHideAll}
            className="rounded border border-slate-600/70 bg-slate-800/70 px-1.5 py-0.5 text-[10px] font-medium text-slate-200 hover:bg-slate-700"
          >
            None
          </button>
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {laterals.map((l) => {
          const isProducing = producingLeg != null && l.leg === producingLeg;
          const color = colorForLateral(l.leg, isProducing);
          const active = visibleLegs.has(l.leg);
          return (
            <button
              key={l.leg}
              type="button"
              onClick={() => onToggle(l.leg)}
              className={`group flex items-center gap-1.5 rounded-md border px-1.5 py-1 text-[10px] font-medium transition-colors ${
                active
                  ? 'border-slate-500/70 bg-slate-800/80 text-slate-100'
                  : 'border-slate-700/50 bg-slate-900/60 text-slate-500 hover:bg-slate-800/60'
              }`}
              title={`Leg ${l.leg} · KOP ${l.kopMdM.toFixed(0)} m · ${Math.round(l.lateralLengthM)} m lateral${isProducing ? ' · PRODUCING' : ''}`}
            >
              <span
                className="inline-block h-2 w-4 rounded-sm"
                style={{
                  backgroundColor: active ? color : `${color}33`,
                  boxShadow: active ? `0 0 6px ${color}aa` : undefined,
                }}
              />
              <span>L{String(l.leg).padStart(2, '0')}</span>
              {isProducing ? <span className="text-amber-300">●</span> : null}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function LegendSwatch({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span
        className="inline-block h-1.5 w-5 rounded-full"
        style={{ backgroundColor: color, boxShadow: `0 0 8px ${color}66` }}
      />
      <span>{label}</span>
    </div>
  );
}

export default WellTrajectory3D;
