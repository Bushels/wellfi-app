---
name: well-trajectory-visualization
description: Directional-survey workflow for 2D plates, 3D Three.js wellbores (single + multi-lateral engineering digital twins), and Blender marketing-quality photoreal renders.
---

# Well Trajectory Visualization

Use this workflow when directional-survey CSVs need to become accurate well views —
2D section/plan plates inside WellFi, interactive 3D scenes in the right panel, or
photoreal Blender renders for marketing and investor-facing materials.

## Use When

- a vendor survey CSV needs to drive a deviated-well visualization
- a right-panel popout should show the actual well path (2D plate or interactive 3D)
- a completion anchor must be positioned along the real survey
- a multi-lateral well needs every leg rendered, with the producing leg highlighted
- a standalone SVG or PNG artifact is needed for engineering review
- a photorealistic still or animation is needed for marketing / investor decks
- Gemini should do a second-pass visual audit on the generated plate

## Tool Choice: Three.js vs Blender (VERIFIED by experience on OBE 102 HZ)

**Default to Three.js for engineering-overview visualization.** This was proven
empirically in April 2026 — we built the identical multi-lateral scene in both
Three.js and Blender, and Three.js consistently looked cleaner, clearer, and
more useful for quick comprehension. Blender renders felt soft and unpunchy no
matter how we tuned them.

**The technical reason Three.js wins for this use case:** engineering digital-
twin visualization rewards *additive emission on dark backgrounds* — saturated
colors that look "lit from within." Three.js's `MeshStandardMaterial` with
`emissiveIntensity: 0.55+` and `toneMapped={false}`, on a near-black world, is
native to this aesthetic. Blender's physically-based renderers (Cycles + EEVEE)
actively *fight* it: the HDRI environment light desaturates emission, and there
is no equivalent of "unlit glow" without compositor Glare nodes that we never
wired up. It's not that Blender can't match the look — it's that Blender gets
there the hard way, against the grain of what its materials want to do.

**Where Three.js loses**: any time you need photorealism, animation, export to
other 3D formats, or physical simulation. For those, Blender is the right tool
and the only tool.

| Need | Tool | Why |
|------|------|-----|
| Quick overview of open-hole multi-lateral | **Three.js** | Schematic emission aesthetic, interactive, no round-trip |
| Engineer reviewing well trajectory vs plan | **Three.js** in right panel + 2D plates | Truth views + interactive exploration |
| Marketing hero still for investor deck / website | **Blender (Cycles)** | Photoreal materials, DOF, physical lighting — plus worth the extra time |
| Fly-through animation for conference talk | **Blender** | Three.js can't export MP4 without a lot of custom work |
| AR / VR / 3D viewer embed on a marketing site | **Blender → glTF** | Industry-standard export path |
| Physical simulation (fluid in lateral, collapse) | **Blender** | Cycles + physics sim; Three.js is not a simulator |
| "I want to see where the lateral is right now" (dashboard) | **Three.js** | Already in the app, lazy-loaded |

Do not try to use Blender to replicate the Three.js look. It is the wrong tool
for that goal. If a Blender render is the deliverable, commit to photorealism
and spend the time on materials, lighting, and post-processing — or hand the
job back to Three.js.

## Core Rules

- Treat surveyed stations and projected tail rows as different things.
- Use minimum curvature for anchor interpolation.
- Keep section view plus plan view as the primary 2D truth view; 3D is exploratory.
- Label schematic cutaways as schematic, not realistic.
- Call out the TVD reference explicitly, especially when the source uses `Actual KB`.
- For multi-laterals, render each lateral's **post-KOP segment only** — do not duplicate the shared cased section.
- Producing-leg highlight is load-bearing: different color, larger radius, brighter emissive, labeled in-scene.
- **Split the parent bore at the intermediate casing shoe MD.** Cased section (0 to shoe) gets a casing shadow/shell and metallic-looking material; open-hole section (shoe to TD, plus all laterals) gets a warm rock tone, thinner tube, no casing shadow. The casing shoe MD lives on `asset.telemetry_placement_reference.conductive_casing_set_depth_mkb`.
- **Reservoir formation picks are well-specific** (from the well's LAS gamma-ray logs), not basin-wide. Put them on `asset.reservoir` as `{ name, top_tvd_m, base_tvd_m, color_rgba, pick_source }`. Render as a translucent amber box volume spanning the horizontal well extent — laterals weaving through it should stay visible at ~20% opacity.

## Parser: Flexible Vendor-CSV Support

`src/lib/directionalSurvey.ts` uses **header-name to column-index mapping** with aliases,
not fixed positions. This handles both column-name variants (`Inclination`/`INCL`,
`North`/`N(+)`, `Vert Sect`/`VS`) and column-order variants (some vendors emit VS
before N/E, others after). Both of these parse identically:

```text
MD,INCL,AZIMUTH,TVD,TVDSS,N(+),E(+),VS,...         (Vendor A)
MD,Inclination,Azimuth,True Vertical Depth (TVD),TVDSS,Vert Sect,North,East,...   (Vendor B)
```

UWI detection also supports both the standalone-line form and the inline form
(`UWI (D59:...) ,102/16-18-083-17W5/12,,,`).

VS-azimuth detection matches both "Azimuth of 323.088" (metadata block) and
"Vertical Section Azimuth ,351.6" (CSV header row).

## Workflow

### 1. Validate the survey input

- Prefer vendor CSV with `MD`, `INCL`/`Inclination`, `AZIMUTH`, `TVD`, `N`/`North`,
  `E`/`East`, and `VS`/`Vert Sect`.
- Capture the survey header UWI, vertical-section azimuth, last surveyed MD, and
  any projected TD row.
- Do not silently merge `Projection to Final TD` into the surveyed path.

### 2. Build geometry from the survey

- Use `src/lib/directionalSurvey.ts` for parsing and MD-interpolation.
- Use `src/lib/wellGeometry.ts` for WellFi asset matching and completion anchoring.
- Treat solid path = surveyed stations and dashed/translucent path = projected tail.

### 3. Render the 2D truth view

- Use `src/components/panels/WellTrajectoryPlate.tsx` for the in-app truth view.
- Keep equal scale in plan and section views unless you explicitly disclose exaggeration.
- Show surface, last survey, projected TD, and anchor marker when relevant.

### 4. Render the 3D navigator (Three.js / React Three Fiber)

- Entry point: `src/components/panels/WellTrajectory3D.tsx`
- Geometry helpers: `src/lib/trajectoryGeometry3D.ts`
- **Axis mapping (survey to Three.js Y-up):** `x = East, y = -TVD, z = -North`
- Tube radius is **visually exaggerated** (~2m) — note in legend.
- Surveyed bore = `CatmullRomCurve3` + `TubeGeometry`, tension 0.5.
- **Casing vs open-hole split (parent bore only):** use `splitSurveyPointsAtMd(points, shoeMd, vsAz)` to get two point arrays sharing a synthetic boundary station. Build one `CatmullRomCurve3` per array. Cased tube uses cyan metallic material wrapped in a translucent casing shell (2.4× radius). Open-hole tube uses a warm sandstone color (`#c2ab7d`), thinner radius (0.88×), and **no** casing shell — this is the single most effective engineering signal in the 3D view.
- **Reservoir slab:** `BoxGeometry` sized to the combined bounds + 20% margin, centered at the TVD midpoint of the formation. Use `transparent, opacity ~0.22, side: DoubleSide, depthWrite: false` — the `depthWrite: false` is critical so the tubes behind the slab still z-sort correctly. Add top/base plane overlays at slightly higher opacity to make the bounding surfaces readable. Keep the slab render **before** the tubes in JSX so alpha ordering is predictable.
- R3F `<Canvas>` must use `frameloop="always"` when `<OrbitControls enableDamping>` is used — demand mode makes damping choppy.
- Dispatch one synthetic resize after mount: lazy-loaded Canvases sometimes miss the initial ResizeObserver measurement. A `setTimeout(() => dispatchEvent(new Event('resize')), 16)` in a mount effect fixes it.

### 5. Render multi-lateral wells

- Import vendor CSVs with `scripts/import_multilateral_surveys.ts`. Output: one consolidated JSON per well with per-leg `survey_points`, auto-detected `kop_md_m` / `kop_tvd_m`, and source-file metadata.
- **KOP detection algorithm:** for each lateral station, find the closest-MD parent station; if 3D distance > 5 m, that's the KOP. Robust to survey noise.
- Type model in `wellGeometry.ts`:
  ```ts
  WellGeometryAsset {
    // existing fields...
    laterals?: WellLateral[];        // leg 0 = parent, rest = laterals
    producing_leg?: number;           // matches app's UWI suffix
  }
  ```
- **Rendering:** for each non-parent lateral, filter `survey_points` to `md_m >= kop_md_m` and sweep a tube only over that segment. This avoids duplicating the shared cased section.
- **Producing-leg visual signals (all of these together):** distinct amber color, larger radius (2.0 m vs 1.6 m), brighter emissive (0.65 vs 0.35), glowing HTML label "L0X · PRODUCING", and a ● marker on its legend chip.
- **Combined bounds** drive camera framing: when a user toggles legs on/off, re-compute bounds from visible legs only; camera refocuses automatically.

### 6. Render in Blender (photoreal / animation / export)

Use this path when you want Cycles/EEVEE render quality, fly-throughs, or a .blend file for engineering reviewers.

- Script: `scripts/blender_import_multilaterals.py`
- **Interactive run** (Blender already open): open the Scripting workspace, click in the Python console, paste an `open(...).read()` execution call (see the script docstring), press Return.
- **Headless run**: `blender --background --python scripts/blender_import_multilaterals.py -- --input <json> --save <out.blend>`
- **Axis mapping (survey to Blender Z-up):** `x = East, y = -North, z = -TVD`
- The script creates one `CURVE` object per leg with `bevel_depth = radius`, a dedicated Principled-BSDF material per leg (with emission for glow), KOP sphere markers, and a glowing WellFi install-point sphere. The parent bore is split at `CASING_SHOE_MD_M` into two curves: "Leg-00 (PARENT · CASED)" + an "Intermediate Casing Shell" wrapping it, plus "Leg-00 (PARENT · OPEN HOLE)" below the shoe.
- **Reservoir slab** is a scaled cube in a `Reservoir` collection, sized from the lateral bounds. The translucent amber material uses `Principled BSDF` with Alpha = 0.2; set the material's `surface_render_method` (Blender 5) or `blend_method` (Blender 4.x) to `BLEND` so transparency renders correctly. Update `RESERVOIR_TOP_TVD_M` / `RESERVOIR_BASE_TVD_M` constants for each new well.
- **Two non-obvious Blender gotchas:**
  1. **Viewport clip distance.** Default `clip_end` on a 3D viewport is 1000 m. Multi-lateral wells extend 2500+ m — the far laterals get culled. Set `space.clip_end = 20000` (and do the same on `camera.data.clip_end`) before framing.
  2. **Frame-all from Python requires a context override.** `bpy.ops.view3d.view_all()` needs an area + region override from the Python console, otherwise it throws. Use `bpy.context.temp_override(area=a, region=a.regions[-1])`.
- Switch shading to `space.shading.type = "MATERIAL"` to see per-leg colors without rendering.
- Use `BLENDER_EEVEE_NEXT` (Blender 5.x) for fast previews; switch to `CYCLES` for final publication renders.

#### Hi-res publication render

For a publication-quality hero render, after the scene is imported:

- Set `scene.render.engine = "CYCLES"` and `scene.cycles.samples = 512` (or 256 if time is short).
- Boost resolution: `scene.render.resolution_x = 3840` (4K) or 7680 (8K) with `resolution_percentage = 100`.
- Add an HDRI world map via `Environment Texture` node in the world shader (studio or outdoor-overcast HDRIs read well for dark subsurface scenes).
- Enable `scene.cycles.use_denoising = True` with `scene.cycles.denoiser = "OPENIMAGEDENOISE"` — removes fireflies without softening edges.
- Camera DOF: `cam.data.dof.use_dof = True`, set focus distance to the WellFi marker, aperture `f_stop = 2.8`. Makes the producing-leg anchor pop.
- A 4K / 512-sample Cycles render of a multi-lateral with DOF + HDRI takes ~3-8 min on a mid-range GPU; plan accordingly.

### 7. Export standalone 2D artifact

- Use `scripts/generate_well_trajectory_plate.ts`.
- Example:

```bash
npx tsx scripts/generate_well_trajectory_plate.ts \
  --input "C:\path\to\survey.csv" \
  --output "C:\path\to\trajectory-plate.svg" \
  --well-name "OBE 102 HZ 16-18-83-17" \
  --anchor-md 818.41
```

### 8. Verify before shipping

- Run `npm run build`.
- Compare `last_survey_md_m` versus `projected_td_md_m`.
- Confirm the UWI/event mapping is intentional if the survey header uses `/00` (pilot) and the app well uses `/09` (producing lateral).
- When updating a completion snapshot, also update `highlight_anchor.snapshot_id` — these are independent references.
- If you need a raster artifact, place screenshots under `output/playwright/`; .blend files go under `output/blender/`.

## Gemini Review Prompt

Use this prompt when asking Gemini for a second opinion:

```text
Read GEMINI.md first, then review this directional well visualization workflow.
Check for two things only:
1. visual honesty: surveyed path vs projected tail, equal-scale geometry in 2D,
   per-lateral colors distinguishable in 3D, readable labels
2. engineering trust: anchor placement (shifted with joint-pulls?), last-survey
   vs projected-TD handling, TVD reference clarity, KOP detection, producing-leg
   identification

Files:
- src/lib/directionalSurvey.ts
- src/lib/wellGeometry.ts
- src/lib/trajectoryGeometry3D.ts
- src/components/panels/WellTrajectoryPlate.tsx
- src/components/panels/WellTrajectory3D.tsx
- scripts/import_multilateral_surveys.ts
- scripts/blender_import_multilaterals.py
- output/blender/<well>.blend (if present)

Tell me the remaining risks, not a rewrite.
```

## Complexity Warning

Do not make a decorative 3D scene the primary source of truth for directional geometry.
The fastest clean workflow is:

- survey parser (`parseSurveyCsv` — flexible headers)
- section view (2D SVG plate) **← authoritative**
- plan view (2D SVG plate) **← authoritative**
- optional completion strip
- **then** Three.js 3D navigator as the interactive engineering view
- **only when photorealism is the actual deliverable** — Blender

2D stays authoritative. Three.js 3D is for exploration and engineering handoff.
Blender is *not* a better 3D view — it's a fundamentally different output
(photoreal marketing stills + animations) that requires a different investment
of time and craft to land.

## Lessons Learned (April 2026 session, verified)

What we got right:

- Flexible vendor-CSV parser (column-name mapping, not positions) — parses every vendor we tried.
- Multi-lateral data model with auto-detected KOPs via 3D-distance divergence.
- Producing-leg highlight as a load-bearing visual signal across tube color, radius, emission, and HTML label.
- Casing/open-hole split in both Three.js and Blender — the single most useful engineering signal.
- Two reservoir planes beat a volumetric box (cleaner, no alpha-sort issues).
- BlenderMCP setup as a reusable runbook.

What didn't work as hoped:

- **Trying to use Blender for quick-overview engineering visualization.** Multiple iterations (Cycles + HDRI, EEVEE + camera-ray mask, tuned emission strengths) all underperformed the Three.js view. Lesson: tool selection matters more than tool-tuning.
- **First-pass fly-through MP4** — technically correct but aesthetically unremarkable. Lesson: motion alone is not narrative; animation needs shot design.
- **Volumetric reservoir slab in Blender (initial attempt)** — rendered opaque in Cycles because Principled BSDF Alpha and `blend_method` aren't cross-engine reliable. Replacing with two thin horizontal planes + Mix Shader pattern fixed it.
- **One-big-MCP-call for complex bpy operations** caused TCP keepalive timeouts and crashed Blender once. Lesson: break MCP calls small, save `.blend` often.

The skill keeps the failed approaches documented, not to shame them, but because future-you might consider them again and deserves to know why they don't work.

## Camera Fly-Through Animation (verified recipe)

To ride along any lateral curve as a first-person / chase-cam clip:

1. **Duplicate the render curve as a dedicated flight path** — set `bevel_depth = 0` so it's invisible, and `use_path = True` / `use_path_follow = True` so Follow Path works:

   ```python
   src = bpy.data.objects["Leg-09 (PRODUCING)"]
   flight_data = src.data.copy()
   flight_data.name = "Leg-09 Flight Path"
   flight_data.bevel_depth = 0.0
   flight_data.use_path = True
   flight_data.use_path_follow = True
   flight_data.path_duration = 240
   flight_obj = bpy.data.objects.new("Leg-09 Flight Path", flight_data)
   bpy.context.scene.collection.objects.link(flight_obj)
   ```

2. **Keyframe `eval_time` across the frame range using `keyframe_insert`** (NOT `action.fcurves.new` — Blender 5's slotted Action API breaks that):

   ```python
   scene.frame_set(1);   flight_data.eval_time = 0;    flight_data.keyframe_insert("eval_time", frame=1)
   scene.frame_set(240); flight_data.eval_time = 240;  flight_data.keyframe_insert("eval_time", frame=240)
   ```

3. **Camera with a Follow Path constraint**. Critical settings:
   - `forward_axis = "TRACK_NEGATIVE_Z"` (camera view direction = curve tangent)
   - `up_axis = "UP_Y"`
   - `use_curve_follow = True`
   - Camera local position `(0, 35, 25)` = 35m up in curve frame, 25m behind the riding point (chase-cam offset)
   - `camera.rotation_euler = (0, 0, 0)` — let the constraint drive rotation

4. **Render PNG sequence, stitch externally**. Blender 5.1 removed `FFMPEG` from `image_settings.file_format`. Don't fight it:

   ```python
   scene.render.image_settings.file_format = "PNG"
   scene.render.filepath = "<dir>/frame_"  # writes frame_0001.png, frame_0002.png, ...
   bpy.ops.render.render(animation=True)
   ```

   Then from a shell:

   ```bash
   ffmpeg -framerate 24 -i "<dir>/frame_%04d.png" \
     -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium -movflags +faststart \
     <output>.mp4
   ```

5. **The animation-render TCP timeout is normal.** `bpy.ops.render.render(animation=True)` blocks Blender's main thread, so the BlenderMCP TCP socket can't service the keepalive and Claude Code sees `No data received`. This isn't a failure — the render continues. Watchdog pattern: poll the frames directory from a Bash monitor and emit one event when the target count is reached, rather than holding an open MCP call.

## BlenderMCP Setup (verified on Blender 5.1 + Claude Code 2.1.74)

Install once, works from any project that has the MCP registered. Setup is
~3 minutes and Blender must be open each time you want to use it.

**One-time install:**

```bash
# 1. Grab the addon (111 KB, single Python file from the official repo)
mkdir -p ~/Downloads/blender-mcp
curl -sSL -o ~/Downloads/blender-mcp/addon.py \
  https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py

# 2. Register the MCP server in Claude Code (user scope = works across all projects)
claude mcp add blender --scope user -- uvx blender-mcp
```

**Inside Blender (every session you want to use MCP):**

Open the Scripting workspace -> Python console -> run:

```python
import bpy
bpy.ops.preferences.addon_install(filepath=r"C:\Users\<you>\Downloads\blender-mcp\addon.py", overwrite=True)
bpy.ops.preferences.addon_enable(module="addon")
bpy.ops.wm.save_userpref()
bpy.ops.blendermcp.start_server()
# Expect: "BlenderMCP server started on localhost:9876"
```

After first install you only need the last line (`start_server()`) on subsequent
Blender sessions — the addon stays installed + enabled until you explicitly
disable it.

**Verify the connection:**

```bash
claude mcp list | grep blender
# blender: uvx blender-mcp - ✓ Connected
```

The `✓ Connected` status means the external `uvx blender-mcp` process is talking
successfully to the Blender addon on 9876.

**Architecture (so the pieces make sense):**

```
Claude Code ← stdio → uvx blender-mcp ← TCP:9876 → Blender addon (Python in Blender)
    (MCP tools)         (MCP server)                 (bpy operations)
```

Claude Code sees tools like `mcp__blender__execute_python`,
`mcp__blender__view_control`, `mcp__blender__test_echo`. You only get these
tools in a *new* Claude Code session after registering — running sessions
started before registration will not have them.

**When Blender is closed or the server was never started**, MCP calls hang
waiting for the TCP connection. Always verify `localhost:9876` is listening:

```powershell
Test-NetConnection -ComputerName localhost -Port 9876
# TcpTestSucceeded should be True
```

## HDRI Lighting via BlenderMCP + PolyHaven

Quickest way to upgrade the look of any wellbore scene:

1. **Enable PolyHaven in the BlenderMCP N-panel sidebar** — required one-time checkbox, then the `download_polyhaven_asset` MCP tool works.
2. **Search + pick an HDRI** (`mcp__blender__search_polyhaven_assets` with `asset_type=hdris`, category `studio` or `outdoor`). For engineering scenes, high-contrast studio HDRIs like `cyclorama_hard_light` work well — they produce crisp directional shadows on the tubes.
3. **Download at 1k** for previews, 2k-4k for publication. 1k is usually enough for our subsurface scenes since we rarely show the sky.
4. **Mask the HDRI from camera rays** so you get clean lighting without the studio walls/lightstands showing up in the render:

   ```python
   # World shader: Mix between HDRI (for lighting) and flat color (visible to camera)
   lp = nodes.new("ShaderNodeLightPath")
   mix = nodes.new("ShaderNodeMixShader")
   bg_light = nodes.new("ShaderNodeBackground")   # HDRI-driven, lights geometry
   bg_camera = nodes.new("ShaderNodeBackground")  # solid dark color, seen by camera
   links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
   links.new(bg_light.outputs["Background"], mix.inputs[1])   # non-camera rays
   links.new(bg_camera.outputs["Background"], mix.inputs[2])  # camera rays
   ```

5. **Tune `bg_light.inputs["Strength"]` to 0.6-1.1**. Above 1.1 the HDRI washes out the tube emission colors; below 0.6 you lose directional shadow definition.

## MCP Stability Notes (learned the hard way)

- **Avoid one huge `execute_blender_code` call with many node-tree operations.** Long bpy ops starve the TCP keepalive and trigger `[WinError 10054] forcibly closed by remote host`. Break work into smaller calls — each returns quickly, Blender services the socket between them.
- **Cycles renders with HDRI at 192 samples + 2560x1440 crashed Blender** on CPU — memory spike. Use EEVEE_NEXT for iteration, drop Cycles samples to 96 or below, and keep final publication renders at 1920x1080 unless you have GPU acceleration.
- **Save the `.blend` after every meaningful change** (`bpy.ops.wm.save_as_mainfile(filepath=...)`) so a crash doesn't cost the scene. Re-running the import script also rebuilds everything in ~2 seconds but you lose session-specific tweaks (materials, cameras, lights).

## Three.js Aesthetic Principles (what makes our 3D view work)

The Three.js wellbore view is the *hero* visualization for this project. The
aesthetic was arrived at empirically; these principles are what make it read
well and why it beats photoreal approaches for this subject:

1. **Dark, uniform background.** `bg-[#0b1426]` or similar deep navy. No HDRI,
   no sky, no ground. The subject (glowing wellbore) has nothing to compete with.
2. **Additive emission dominates, physical light supplements.** Every tube has
   `emissive` equal to its base `color` with `emissiveIntensity: 0.4-0.65`, and
   `toneMapped={false}` on the material so the color doesn't get crushed by the
   renderer's tone mapping. This is the single most important technique.
3. **Hemisphere + 2-3 directional lights** with modest intensity (0.3-1.4) for
   subtle specular highlights. Not physically accurate — tuned for shape-reading.
4. **Per-leg saturated hues.** 11 distinguishable colors across the hue wheel
   (sky, blue, indigo, violet, purple, fuchsia, pink, amber, orange, red, lime).
   The producing leg gets the most attention-grabbing hue (amber) *and* a
   radius/emission boost.
5. **Translucent volumes use `depthWrite: false`.** Reservoir planes, casing
   shell — anything alpha-blended. The opaque tubes keep default `depthWrite:
   true`. This prevents the sort-order flicker that kills typical R3F scenes.
6. **Labels via drei `<Html>` portals** (not in-scene 3D text). They stay
   readable at any camera distance, support markdown-like styling, and don't
   require a text-geometry asset.
7. **No bloom / post-processing.** The emission + dark background gives enough
   punch without post-fx complexity. Can add `@react-three/postprocessing` +
   Bloom later if we want more drama, but the skill warning is *don't reach for
   bloom to fix lighting you haven't tuned yet*.

## Blender: Marketing-Quality Photoreal Only

Blender is the right tool for *photorealistic* wellbore visualization — hero
stills for pitch decks, marketing collateral, conference posters, glossy
website visuals. It is the WRONG tool for quick-overview engineering
schematics. Attempts to replicate the Three.js "digital twin" aesthetic in
Blender consistently underwhelm (verified April 2026) and aren't worth the
iteration time.

**When to reach for Blender:**

- Investor / board deck hero still, 4K, photorealistic
- Marketing website "see how our tech works" video (with professional motion-graphics polish)
- Conference poster or technical-paper figure that needs physically-accurate lighting
- AR/VR/glTF export of the wellbore for embeddable 3D viewers
- Physical simulation (fluid flow in lateral, formation damage visualization)

**What that actually requires** (which is more work than we did in the April '26 session):

1. **Photoreal materials**, not emission-driven schematics:
   - Brushed steel casing with subtle anisotropic specular + roughness map
   - Open-hole rock with procedural noise + displacement for surface roughness
   - Translucent reservoir with volumetric scattering, not just alpha-blended planes
2. **Three-point lighting**, not HDRI-only. HDRIs are easy but they're isotropic
   studio light — a product-rendering setup with a strong key, a colored rim,
   and a subtle fill reads dramatically better.
3. **High Cycles sample counts** (512–1024) with OpenImageDenoise. EEVEE is
   for previews, not finals.
4. **Compositor work after render**: Glare node (for bloom), Lens Distortion
   (for subtle chromatic aberration on metallic surfaces), Color Balance (for
   grade).
5. **Carefully-tuned DOF**: f/2.8–f/4.0, focus on the WellFi install point.
   Makes the hero element pop against a softly-blurred reservoir.
6. **Shrink the reservoir slab footprint dramatically.** Our "combined bounds +
   20% margin" made the reservoir 5000m × 2000m — bigger than the subject. For
   a marketing still, 1.2× the lateral fan width is enough; anything more steals
   focus.

**What we built that IS re-usable for marketing:**

- `scripts/blender_import_multilaterals.py` — deterministic scene builder.
  Bring the geometry in, then tune from there.
- `scripts/_blender_hires_render.py` — Cycles hero render pattern with DOF on
  the WellFi anchor.
- `scripts/_blender_closeup_render.py` — close-up at the casing shoe with
  spotlight + rim light. This one actually looked good; it's the template for
  marketing shots.

**The MP4 fly-through deliverable is honest about being OK-not-great.** The
April '26 version had flat lighting, no motion blur, no narrative beats
(fade-in, annotations, tempo changes), and a steady camera that felt robotic.
For marketing use it would need: motion blur enabled, per-shot lighting
changes, On-screen titles via compositor, music/sfx, fade-in/fade-out,
cuts between multiple angles rather than one continuous chase-cam.

## BlenderMCP as Creative-Iteration Tool

BlenderMCP shines for *creative* iteration — "try a warmer HDRI", "add a
translucent Bluesky formation layer", "move the camera closer". The
conversational loop is genuinely faster than file-edit-then-exec for tuning
lighting and composition.

For building the deterministic scene from survey data, keep using
`scripts/blender_import_multilaterals.py` — it's fast, reproducible, and
doesn't require Blender to be running.

## Alpha Sorting in Three.js (reservoir slab + tubes)

When a translucent object (reservoir slab) contains opaque objects (lateral tubes),
Three.js's default back-to-front sort can flicker or hide geometry. Use these
rules, which have been verified in `WellTrajectory3D.tsx`:

1. **Render the translucent slab FIRST in JSX** — earlier mesh = drawn first.
2. Slab material: `transparent`, `opacity ~0.2`, `depthWrite: false`, `side: DoubleSide`.
3. Tubes inside the slab: fully opaque (no `transparent`), default `depthWrite: true`.
4. Keep slab `opacity` at 0.2-0.25. Lower → hard to see; higher → tubes get washed out.
5. Don't add `renderOrder` unless you see actual bugs — the default order works when the slab renders with `depthWrite: false`.

## Known Data Oddities (OBE 102 HZ reference case)

- Embedded final-survey CSV is leg 00 (pilot); app well event UWI is `/09` (producing lateral). Survey and app-well UWI do not match — this is intentional.
- Two different VS-azimuths exist across vendor files: 323.088 deg (embedded, Slot origin) and 351.6 deg (DS_* final, different reference). Document whichever you show.
- Run 3 snapshot (`2026-04-02-run-3-operating`) shifts every BHA component up 9.456 m (one joint pull) from the pre-Run 3 schematic. Three independent snapshot references in `wellGeometry.ts` — make sure to update all of them when revving a snapshot: `current_snapshot_id`, `highlight_anchor.snapshot_id`, and any DB columns on the `wells` row.
