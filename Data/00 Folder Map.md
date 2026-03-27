# Data Folder Map

This folder holds the raw and working data inputs used by the WellFi workspace.

- Keep the root-level Clearwater and Bluesky CSVs stable.
- Keep the root-level operator inventory files stable.
- Use company folders like `Obsidian`, `Baytex`, and `CNRL` for operator-specific working material.
- Use `geological` for geology notes and reference material.

Important:

- `wellfi-app` docs and scripts already reference several files in `Data\` by their current names and paths.
- Do not move the root monthly-production CSVs or inventory files unless you update the scripts and docs in the same pass.
- Temporary Office lock files like `.~lock.*` can be ignored.
