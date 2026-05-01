#!/usr/bin/env tsx
/**
 * Import all directional-survey CSVs in a well's "Directional Surveys and Logs"
 * folder and emit a consolidated JSON file consumable by the 3D wellbore viewer.
 *
 * Each DS_*.csv file is parsed as its own lateral. The leg-00 file is treated as
 * the parent bore; legs 2+ are laterals that branch from a kickoff-point (KOP)
 * detected by comparing stations against the parent.
 *
 * Usage:
 *   npx tsx scripts/import_multilateral_surveys.ts \
 *     --input "C:\path\to\Directional Surveys and Logs" \
 *     --output "src/assets/well-geometry/obe-102-hz-multilaterals.json" \
 *     --well-name "OBE 102 HZ 16-18-83-17" \
 *     --licence "0517936"
 */

import fs from 'node:fs';
import path from 'node:path';
import {
  parseSurveyCsv,
  type TrajectoryPoint,
} from '../src/lib/directionalSurvey.ts';

interface LegRecord {
  leg: number;
  uwi: string | null;
  source_file: string;
  label: string;
  is_parent: boolean;
  kop_md_m: number;
  kop_tvd_m: number;
  vertical_section_azimuth_deg: number | null;
  last_survey_md_m: number;
  projected_td_md_m: number | null;
  station_count: number;
  survey_points: TrajectoryPoint[];
}

interface MultilateralOutput {
  well_name: string;
  licence: string;
  source_directory: string;
  imported_at: string;
  parent_leg: number;
  laterals: LegRecord[];
}

const KOP_DISTANCE_THRESHOLD_M = 5;

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

function detectLegNumber(filename: string): number | null {
  // DS_0517936_02-16-18-083-17W5-12_33494291.csv -> 12
  // DS_0517936_02-16-18-083-17W5-00_33494132.csv -> 0
  const match = filename.match(/-(\d{2})_\d+\.csv$/i);
  if (!match) return null;
  const parsed = Number.parseInt(match[1], 10);
  return Number.isFinite(parsed) ? parsed : null;
}

function legLabel(legNumber: number, uwi: string | null, isParent: boolean): string {
  if (isParent) {
    return `Pilot / parent bore (leg ${String(legNumber).padStart(2, '0')})`;
  }
  const suffix = uwi?.match(/\/(\d{2})$/)?.[1] ?? String(legNumber).padStart(2, '0');
  return `Lateral ${legNumber} (UWI suffix /${suffix})`;
}

/**
 * Locate the kickoff point: the shallowest MD at which this lateral has
 * separated from the parent bore by more than `KOP_DISTANCE_THRESHOLD_M`
 * in 3D space.
 *
 * For a parent leg, KOP is 0 (by convention, the surface).
 */
function detectKickoff(
  parentPoints: readonly TrajectoryPoint[],
  lateralPoints: readonly TrajectoryPoint[],
): { md: number; tvd: number } {
  if (parentPoints.length === 0 || lateralPoints.length === 0) {
    return { md: 0, tvd: 0 };
  }

  const parentLastMd = parentPoints[parentPoints.length - 1].md_m;

  for (const lp of lateralPoints) {
    // Past the end of the parent bore, everything is by definition divergent.
    if (lp.md_m > parentLastMd) {
      return { md: parentLastMd, tvd: parentPoints[parentPoints.length - 1].tvd_m };
    }

    // Find the parent station closest to this lateral MD.
    let best = parentPoints[0];
    let bestDelta = Math.abs(best.md_m - lp.md_m);
    for (const pp of parentPoints) {
      const delta = Math.abs(pp.md_m - lp.md_m);
      if (delta < bestDelta) {
        best = pp;
        bestDelta = delta;
      }
    }

    // If no station is within 2 m, skip — too sparse to compare.
    if (bestDelta > 2) continue;

    const dx = lp.easting_offset_m - best.easting_offset_m;
    const dy = lp.northing_offset_m - best.northing_offset_m;
    const dz = lp.tvd_m - best.tvd_m;
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

    if (dist > KOP_DISTANCE_THRESHOLD_M) {
      return { md: lp.md_m, tvd: lp.tvd_m };
    }
  }

  // Paths never diverged meaningfully — fall through to final surveyed station.
  const last = lateralPoints[lateralPoints.length - 1];
  return { md: last.md_m, tvd: last.tvd_m };
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));

  const input = args.input;
  const output = args.output;
  const wellName = args['well-name'] ?? 'Unknown Well';
  const licence = args.licence ?? '';

  if (!input || !output) {
    console.error('Usage: --input <dir> --output <json> [--well-name "..."] [--licence "..."]');
    process.exit(1);
  }

  const inputDir = path.resolve(input);
  const outputPath = path.resolve(output);

  if (!fs.existsSync(inputDir) || !fs.statSync(inputDir).isDirectory()) {
    console.error(`Input directory not found: ${inputDir}`);
    process.exit(1);
  }

  const allFiles = fs.readdirSync(inputDir);
  const csvFiles = allFiles
    .filter((f) => /^DS_.+\.csv$/i.test(f))
    .sort();

  if (csvFiles.length === 0) {
    console.error(`No DS_*.csv files found in ${inputDir}`);
    process.exit(1);
  }

  console.log(`Found ${csvFiles.length} DS_*.csv files in ${inputDir}`);

  // Parse every file.
  type Parsed = {
    leg: number;
    file: string;
    parsed: ReturnType<typeof parseSurveyCsv>;
  };

  const parsedLegs: Parsed[] = [];
  for (const file of csvFiles) {
    const leg = detectLegNumber(file);
    if (leg == null) {
      console.warn(`  skipping ${file} - could not detect leg number`);
      continue;
    }
    try {
      const raw = fs.readFileSync(path.join(inputDir, file), 'utf-8');
      const parsed = parseSurveyCsv(raw);
      parsedLegs.push({ leg, file, parsed });
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      console.warn(`  skipping ${file} - parse error: ${message}`);
    }
  }

  if (parsedLegs.length === 0) {
    console.error('No DS_*.csv files parsed successfully.');
    process.exit(1);
  }

  parsedLegs.sort((a, b) => a.leg - b.leg);

  // Leg 0 (pilot hole) is the parent when present; otherwise use the lowest-numbered leg.
  const parent = parsedLegs.find((l) => l.leg === 0) ?? parsedLegs[0];
  const parentPoints = parent.parsed.points;

  const laterals: LegRecord[] = parsedLegs.map(({ leg, file, parsed }) => {
    const isParent = leg === parent.leg;
    const { md: kopMd, tvd: kopTvd } = isParent
      ? { md: 0, tvd: 0 }
      : detectKickoff(parentPoints, parsed.points);

    return {
      leg,
      uwi: parsed.survey_header_uwi,
      source_file: file,
      label: legLabel(leg, parsed.survey_header_uwi, isParent),
      is_parent: isParent,
      kop_md_m: Number(kopMd.toFixed(3)),
      kop_tvd_m: Number(kopTvd.toFixed(3)),
      vertical_section_azimuth_deg: parsed.vertical_section_azimuth_deg,
      last_survey_md_m: parsed.last_survey_md_m,
      projected_td_md_m: parsed.projected_td_md_m,
      station_count: parsed.points.length,
      survey_points: parsed.points,
    };
  });

  const output_json: MultilateralOutput = {
    well_name: wellName,
    licence,
    source_directory: inputDir,
    imported_at: new Date().toISOString(),
    parent_leg: parent.leg,
    laterals,
  };

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(output_json, null, 2), 'utf-8');

  console.log(`\nWrote ${laterals.length} laterals to ${outputPath}`);
  console.log(`  Parent leg: ${parent.leg} (${parent.file})`);
  console.log('  Leg breakdown:');
  for (const l of laterals) {
    const parentTag = l.is_parent ? ' [PARENT]' : '';
    console.log(
      `    leg ${String(l.leg).padStart(2, '0')}: ${String(l.station_count).padStart(3)} stations, ` +
        `KOP ${l.kop_md_m.toFixed(1).padStart(7)} m MD / ${l.kop_tvd_m.toFixed(1).padStart(6)} m TVD, ` +
        `TD ${l.last_survey_md_m.toFixed(1).padStart(7)} m MD` +
        parentTag,
    );
  }
}

main();
