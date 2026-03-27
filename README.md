## WellFi Workspace

Canonical app:

- `C:\Users\kyle\MPS\Obsidian\wellfi-app`

Use `wellfi-app\` for:

- frontend code
- Supabase migrations
- scripts
- Vercel deployment

Use `Data\` for:

- monthly production inputs
- operator inventory outputs
- company-specific working files
- geology and reference data

Keep these root-level files stable unless you update references in the same pass:

- `obsidian_bluesky_clearwater_last2years.json`
- `obsidian_ab_mineral_rights_all_zones.json`
- `100141808317W5 DH Schematic.pdf`

Use `_local\` for:

- scratch files
- diff output
- local draft plans
- packaged skill exports

Rule:

- if you are changing product code, start in `wellfi-app\`
- if you are changing production inputs, start in `Data\`
- do not reorganize `Data\` root files casually because scripts and docs already point at them
