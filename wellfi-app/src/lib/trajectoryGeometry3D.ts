import * as THREE from 'three';
import { interpolateTrajectoryPoint } from './directionalSurvey';
import type { TrajectoryPoint, InterpolatedTrajectoryPoint } from './directionalSurvey';
import type { WellLateral } from './wellGeometry';

/**
 * Axis mapping (survey → Three.js world):
 *   x = East   (+E to the right)
 *   y = -TVD   (KB at y = 0, deeper = more negative)
 *   z = -North (looking toward -Z reads as "looking north")
 */
export function surveyPointToVec3(point: {
  northing_offset_m: number;
  easting_offset_m: number;
  tvd_m: number;
}): THREE.Vector3 {
  return new THREE.Vector3(
    point.easting_offset_m,
    -point.tvd_m,
    -point.northing_offset_m,
  );
}

export interface TrajectoryBounds {
  min: THREE.Vector3;
  max: THREE.Vector3;
  center: THREE.Vector3;
  size: THREE.Vector3;
  radius: number;
}

export interface TrajectoryCurve3D {
  surveyedPoints: THREE.Vector3[];
  projectedPoints: THREE.Vector3[];
  surveyedCurve: THREE.CatmullRomCurve3 | null;
  projectedCurve: THREE.CatmullRomCurve3 | null;
  surveyedLengthM: number;
  projectedLengthM: number;
  maxTvdM: number;
  bounds: TrajectoryBounds;
}

function arcLength(points: readonly THREE.Vector3[]): number {
  let total = 0;
  for (let i = 1; i < points.length; i += 1) {
    total += points[i].distanceTo(points[i - 1]);
  }
  return total;
}

export function buildTrajectoryCurve3D(
  surveyedPoints: readonly TrajectoryPoint[],
  projectedPoints: readonly TrajectoryPoint[] = [],
): TrajectoryCurve3D {
  const surveyed = surveyedPoints.map((p) => surveyPointToVec3(p));
  const projected = projectedPoints.map((p) => surveyPointToVec3(p));

  const allPoints = surveyed.length > 0 || projected.length > 0
    ? [...surveyed, ...projected]
    : [new THREE.Vector3(0, 0, 0)];

  const box = new THREE.Box3().setFromPoints(allPoints);
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);
  const radius = size.length() / 2;

  const surveyedCurve = surveyed.length >= 2
    ? new THREE.CatmullRomCurve3(surveyed, false, 'catmullrom', 0.5)
    : null;

  // Stitch the projected tail onto the last surveyed station so the two tubes
  // meet without a visible gap.
  const projectedPathPoints = projected.length > 0 && surveyed.length > 0
    ? [surveyed[surveyed.length - 1], ...projected]
    : projected;
  const projectedCurve = projectedPathPoints.length >= 2
    ? new THREE.CatmullRomCurve3(projectedPathPoints, false, 'catmullrom', 0.5)
    : null;

  const allTvd = [...surveyed, ...projected].map((p) => -p.y);
  const maxTvdM = allTvd.length > 0 ? Math.max(...allTvd) : 0;

  return {
    surveyedPoints: surveyed,
    projectedPoints: projected,
    surveyedCurve,
    projectedCurve,
    surveyedLengthM: arcLength(surveyed),
    projectedLengthM: arcLength(projected),
    maxTvdM,
    bounds: {
      min: box.min.clone(),
      max: box.max.clone(),
      center,
      size,
      radius,
    },
  };
}

export function interpolatedToVec3(
  point: InterpolatedTrajectoryPoint | null,
): THREE.Vector3 | null {
  if (!point) return null;
  return surveyPointToVec3(point);
}

/**
 * Split a surveyed-points array at a given MD (e.g., the intermediate casing
 * shoe) so the cased section and the open-hole section can be rendered as
 * separate geometries with different styling.
 *
 * The cutoff MD is interpolated into a synthetic station at the exact boundary
 * so both resulting arrays share that point, avoiding a visual seam.
 */
export function splitSurveyPointsAtMd(
  points: readonly TrajectoryPoint[],
  cutoffMdM: number,
  verticalSectionAzimuthDeg: number | null,
): { casedPoints: TrajectoryPoint[]; openHolePoints: TrajectoryPoint[] } {
  if (points.length === 0) {
    return { casedPoints: [], openHolePoints: [] };
  }

  const minMd = points[0].md_m;
  const maxMd = points[points.length - 1].md_m;

  // Cutoff outside the surveyed range — no split needed.
  if (cutoffMdM <= minMd) return { casedPoints: [], openHolePoints: [...points] };
  if (cutoffMdM >= maxMd) return { casedPoints: [...points], openHolePoints: [] };

  const interp = interpolateTrajectoryPoint(points, cutoffMdM, {
    verticalSectionAzimuthDeg,
  });

  const boundary: TrajectoryPoint = interp
    ? {
        md_m: interp.md_m,
        inclination_deg: interp.inclination_deg,
        azimuth_deg: interp.azimuth_deg,
        tvd_m: interp.tvd_m,
        northing_offset_m: interp.northing_offset_m,
        easting_offset_m: interp.easting_offset_m,
        vertical_section_m: interp.vertical_section_m,
        station_kind: 'survey',
        station_note: 'Casing shoe (synthetic)',
      }
    : points.reduce((closest, p) =>
        Math.abs(p.md_m - cutoffMdM) < Math.abs(closest.md_m - cutoffMdM) ? p : closest,
      );

  const casedPoints: TrajectoryPoint[] = points.filter((p) => p.md_m < boundary.md_m);
  const openHolePoints: TrajectoryPoint[] = points.filter((p) => p.md_m > boundary.md_m);
  casedPoints.push(boundary);
  openHolePoints.unshift(boundary);

  return { casedPoints, openHolePoints };
}

export interface LateralCurve3D {
  leg: number;
  label: string;
  uwi: string | null;
  isParent: boolean;
  kopMdM: number;
  kopTvdM: number;
  totalMdM: number;
  lateralLengthM: number;
  /** The 3D curve for this lateral's *unique* segment.
   *  For the parent bore, this is the full path. For laterals, only the post-KOP divergent portion. */
  curve: THREE.CatmullRomCurve3 | null;
  /** Start point in world coordinates (at KOP for laterals, origin for parent). */
  startVec: THREE.Vector3 | null;
  /** End point in world coordinates (TD). */
  endVec: THREE.Vector3 | null;
  points: THREE.Vector3[];
}

/**
 * Build a 3D curve for a single lateral.
 *
 * For the parent bore, uses every station in the survey.
 *
 * For laterals, keeps only stations at or after the kickoff MD so the rendered
 * tube starts at the branch point instead of doubling the shared cased section.
 */
export function buildLateralCurve3D(lateral: WellLateral): LateralCurve3D {
  const relevantPoints = lateral.is_parent
    ? lateral.survey_points
    : lateral.survey_points.filter((p) => p.md_m >= lateral.kop_md_m);

  const vecs = relevantPoints.map((p) => surveyPointToVec3(p));
  const curve = vecs.length >= 2
    ? new THREE.CatmullRomCurve3(vecs, false, 'catmullrom', 0.5)
    : null;

  let arcLenM = 0;
  for (let i = 1; i < vecs.length; i += 1) {
    arcLenM += vecs[i].distanceTo(vecs[i - 1]);
  }

  return {
    leg: lateral.leg,
    label: lateral.label,
    uwi: lateral.uwi,
    isParent: lateral.is_parent,
    kopMdM: lateral.kop_md_m,
    kopTvdM: lateral.kop_tvd_m,
    totalMdM: lateral.last_survey_md_m,
    lateralLengthM: arcLenM,
    curve,
    startVec: vecs[0] ?? null,
    endVec: vecs[vecs.length - 1] ?? null,
    points: vecs,
  };
}

/**
 * Build 3D curves for every lateral + aggregate bounds across all of them.
 */
export function buildAllLateralCurves(laterals: readonly WellLateral[]): {
  curves: LateralCurve3D[];
  bounds: TrajectoryBounds;
} {
  const curves = laterals.map(buildLateralCurve3D);
  const allPoints = curves.flatMap((c) => c.points);
  const box = new THREE.Box3().setFromPoints(
    allPoints.length > 0 ? allPoints : [new THREE.Vector3(0, 0, 0)],
  );
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);
  return {
    curves,
    bounds: {
      min: box.min.clone(),
      max: box.max.clone(),
      center,
      size,
      radius: size.length() / 2,
    },
  };
}
