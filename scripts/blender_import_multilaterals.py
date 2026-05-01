"""Blender multi-lateral wellbore importer.

Reads the multilaterals JSON emitted by
scripts/import_multilateral_surveys.ts and builds a colored 3D Blender scene
with one beveled-curve tube per leg, per-leg materials, KOP markers, and a
glowing WellFi install-point marker.

Coordinate mapping (survey -> Blender, Z-up):
    x = easting_offset_m
    y = -northing_offset_m   (so +Y looks north-ish from Blender's default cam)
    z = -tvd_m               (Z-up, deeper = lower Z)

Usage A (interactive, from Blender's Scripting workspace):
    1. Open Blender -> Scripting workspace.
    2. Open this file via "Open" in the text editor.
    3. Adjust JSON_PATH at the top if needed.
    4. Click "Run Script".

Usage B (headless, from a shell):
    blender --background --python scripts/blender_import_multilaterals.py -- \\
        --input src/assets/well-geometry/obe-102-hz-multilaterals.json \\
        --save output/blender/obe-102-hz.blend
"""

import bpy
import mathutils
import json
import os
import sys

# --- Configuration ---------------------------------------------------------

# Default JSON path, resolved to the absolute location in the repo if possible.
DEFAULT_JSON_PATH = (
    r"C:\Users\kyle\MPS\Obsidian\wellfi-app\src\assets\well-geometry"
    r"\obe-102-hz-multilaterals.json"
)

PRODUCING_LEG = 9  # OBE 102 HZ producing lateral; matches wellGeometry.ts

# Intermediate conductive casing shoe (meters MD). Above this the parent bore
# is cased steel; below this it's open hole down to pilot TD + laterals.
CASING_SHOE_MD_M = 921.0

# Tool/tube geometry (meters). Radius is visually exaggerated for visibility.
WELLBORE_RADIUS_M = 2.2
OPEN_HOLE_RADIUS_M = 1.9  # slightly thinner than cased section
CASING_SHELL_RADIUS_M = 5.3  # casing shadow around the cased portion
LATERAL_RADIUS_M = 1.6
LATERAL_PRODUCING_RADIUS_M = 2.0
KOP_MARKER_RADIUS_M = 3.0
WELLFI_MARKER_RADIUS_M = 5.0
WELLFI_ANCHOR_MD_M = 818.41  # Run 3 post-joint-pull top-of-tool

BEVEL_RESOLUTION = 12
CURVE_RESOLUTION_U = 12

# Colour for the bare open-hole section (warm sandstone/rock tone).
OPEN_HOLE_COLOR = (0.76, 0.67, 0.49, 1.0)
# Colour for the conductive casing shell (cool steel grey).
CASING_SHELL_COLOR = (0.39, 0.45, 0.55, 1.0)

# Reservoir formation slab (LAS gamma ray picks, well-specific).
RESERVOIR_NAME = "Bluesky"
RESERVOIR_TOP_TVD_M = 660.5
RESERVOIR_BASE_TVD_M = 678.0
RESERVOIR_COLOR = (0.95, 0.70, 0.25, 1.0)  # amber
RESERVOIR_MARGIN_FRAC = 0.2  # extend slab 20% past the well footprint

# Per-leg RGBA colours (linear-ish; Blender does gamma internally).
LATERAL_COLORS = {
    0: (0.13, 0.82, 0.93, 1.0),   # cyan (parent / pilot)
    2: (0.49, 0.83, 0.98, 1.0),   # sky
    3: (0.38, 0.65, 0.98, 1.0),   # blue
    4: (0.51, 0.55, 0.97, 1.0),   # indigo
    5: (0.66, 0.55, 0.98, 1.0),   # violet
    6: (0.75, 0.52, 0.99, 1.0),   # purple
    7: (0.91, 0.48, 0.98, 1.0),   # fuchsia
    8: (0.96, 0.44, 0.71, 1.0),   # pink
    9: (0.98, 0.75, 0.14, 1.0),   # amber (PRODUCING)
    10: (0.98, 0.57, 0.24, 1.0),  # orange
    11: (0.97, 0.44, 0.44, 1.0),  # red
    12: (0.52, 0.80, 0.09, 1.0),  # lime
}

# --- Helpers ---------------------------------------------------------------


def survey_point_to_blender(point):
    """Convert a survey station dict to a Blender (x, y, z) tuple."""
    return (
        point["easting_offset_m"],
        -point["northing_offset_m"],
        -point["tvd_m"],
    )


def clear_scene():
    """Remove every object, mesh, curve, and material. Fresh scene."""
    for collection in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                       bpy.data.lights, bpy.data.cameras, bpy.data.worlds):
        pass  # kept to show intent; we actually delete via operators below

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                       bpy.data.lights, bpy.data.cameras):
        for item in list(block_list):
            block_list.remove(item)


def ensure_collection(name):
    existing = bpy.data.collections.get(name)
    if existing:
        return existing
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def make_material(name, color_rgba, emission_strength=1.0, metallic=0.45,
                  roughness=0.25):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is None:
        return mat
    bsdf.inputs["Base Color"].default_value = color_rgba
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    # Blender 4.x renamed the emission socket.
    for name_candidate in ("Emission Color", "Emission"):
        if name_candidate in bsdf.inputs:
            bsdf.inputs[name_candidate].default_value = color_rgba
            break
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def create_tube_from_points(name, points_3d, radius, material, collection):
    """Create a beveled Bezier curve (tube) through points_3d."""
    if len(points_3d) < 2:
        return None

    curve_data = bpy.data.curves.new(name=name, type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = radius
    curve_data.bevel_resolution = BEVEL_RESOLUTION
    curve_data.resolution_u = CURVE_RESOLUTION_U
    curve_data.use_fill_caps = True

    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(len(points_3d) - 1)
    for i, pt in enumerate(points_3d):
        bp = spline.bezier_points[i]
        bp.co = pt
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"

    obj = bpy.data.objects.new(name=name, object_data=curve_data)
    obj.data.materials.append(material)
    collection.objects.link(obj)
    return obj


def create_sphere_marker(name, location, radius, material, collection):
    mesh = bpy.data.meshes.new(name=f"{name}-mesh")
    obj = bpy.data.objects.new(name=name, object_data=mesh)
    collection.objects.link(obj)

    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm, u_segments=24, v_segments=16, radius=radius,
    )
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    if material is not None:
        obj.data.materials.append(material)
    return obj


def interpolate_md(survey_points, target_md):
    """Return a dict-like point at target_md via linear interpolation."""
    if not survey_points:
        return None
    for i in range(len(survey_points) - 1):
        p0, p1 = survey_points[i], survey_points[i + 1]
        if p0["md_m"] <= target_md <= p1["md_m"] and p1["md_m"] != p0["md_m"]:
            t = (target_md - p0["md_m"]) / (p1["md_m"] - p0["md_m"])
            return {
                "md_m": target_md,
                "easting_offset_m": p0["easting_offset_m"]
                + t * (p1["easting_offset_m"] - p0["easting_offset_m"]),
                "northing_offset_m": p0["northing_offset_m"]
                + t * (p1["northing_offset_m"] - p0["northing_offset_m"]),
                "tvd_m": p0["tvd_m"] + t * (p1["tvd_m"] - p0["tvd_m"]),
            }
    return None


def split_points_at_md(survey_points, cutoff_md):
    """Split a survey-point list at a given MD, sharing a synthetic boundary
    station so cased and open-hole segments meet without a seam.
    """
    if not survey_points:
        return [], []
    min_md = survey_points[0]["md_m"]
    max_md = survey_points[-1]["md_m"]
    if cutoff_md <= min_md:
        return [], list(survey_points)
    if cutoff_md >= max_md:
        return list(survey_points), []

    boundary = interpolate_md(survey_points, cutoff_md)
    if boundary is None:
        return list(survey_points), []

    cased = [p for p in survey_points if p["md_m"] < boundary["md_m"]]
    open_hole = [p for p in survey_points if p["md_m"] > boundary["md_m"]]
    cased.append(boundary)
    open_hole.insert(0, boundary)
    return cased, open_hole


# --- Scene build -----------------------------------------------------------


def _make_reservoir_material(name, color_rgba, alpha):
    """Simple translucent Principled BSDF with explicit Alpha + blend mode."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color_rgba
        bsdf.inputs["Roughness"].default_value = 0.9
        bsdf.inputs["Metallic"].default_value = 0.0
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        for emission_key in ("Emission Color", "Emission"):
            if emission_key in bsdf.inputs:
                bsdf.inputs[emission_key].default_value = color_rgba
                break
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 0.6
    # Both EEVEE (blend_method) and EEVEE_NEXT (surface_render_method) need
    # BLEND mode to respect alpha. Try both attribute names.
    for attr in ("blend_method", "surface_render_method"):
        if hasattr(mat, attr):
            try:
                setattr(mat, attr, "BLEND")
            except (TypeError, ValueError):
                # Blender 5 accepts "BLENDED" on surface_render_method
                try:
                    setattr(mat, attr, "BLENDED")
                except Exception:
                    try:
                        setattr(mat, attr, "HASHED")
                    except Exception:
                        pass
    if hasattr(mat, "show_transparent_back"):
        mat.show_transparent_back = False
    return mat


def create_reservoir_planes(name, top_tvd_m, base_tvd_m, color_rgba, bounds_min,
                            bounds_max, collection):
    """Add two horizontal planes marking the reservoir top + base.

    Two planes read cleaner than a volumetric slab — laterals drilled between
    them remain fully visible, and the planes themselves define the formation
    boundary surfaces which is the geological truth anyway.
    """
    import bmesh

    cx = (bounds_min[0] + bounds_max[0]) / 2
    cy = (bounds_min[1] + bounds_max[1]) / 2
    size_x = max(bounds_max[0] - bounds_min[0], 200.0) * (1.0 + RESERVOIR_MARGIN_FRAC * 2)
    size_y = max(bounds_max[1] - bounds_min[1], 200.0) * (1.0 + RESERVOIR_MARGIN_FRAC * 2)

    # Two materials: top slightly more opaque than base so they read distinctly.
    top_mat = _make_reservoir_material(f"{name} Top-mat", color_rgba, 0.3)
    base_mat = _make_reservoir_material(f"{name} Base-mat", color_rgba, 0.18)

    objs = []
    for label, tvd, mat in (("Top", top_tvd_m, top_mat),
                            ("Base", base_tvd_m, base_mat)):
        mesh = bpy.data.meshes.new(name=f"{name} {label}-mesh")
        obj = bpy.data.objects.new(name=f"{name} {label}", object_data=mesh)
        collection.objects.link(obj)
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5,
                              calc_uvs=False)
        bm.to_mesh(mesh)
        bm.free()
        obj.scale = (size_x, size_y, 1.0)
        obj.location = (cx, cy, -tvd)
        mesh.materials.append(mat)
        objs.append(obj)
    return objs


def setup_world():
    world = bpy.data.worlds.new(name="Wellbore World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.02, 0.04, 0.08, 1.0)
        bg.inputs["Strength"].default_value = 0.8


def setup_camera_and_lights(bounds_min, bounds_max, collection):
    cx = (bounds_min[0] + bounds_max[0]) / 2
    cy = (bounds_min[1] + bounds_max[1]) / 2
    cz = (bounds_min[2] + bounds_max[2]) / 2
    span = max(
        bounds_max[0] - bounds_min[0],
        bounds_max[1] - bounds_min[1],
        bounds_max[2] - bounds_min[2],
        100.0,
    )
    distance = span * 1.5

    cam_loc = (cx + distance * 0.6, cy - distance * 0.8, cz + distance * 0.4)
    cam_data = bpy.data.cameras.new(name="Wellbore Camera")
    cam_data.lens = 35
    cam = bpy.data.objects.new("Wellbore Camera", cam_data)
    cam.location = cam_loc
    direction = mathutils.Vector((cx, cy, cz)) - mathutils.Vector(cam_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    collection.objects.link(cam)
    bpy.context.scene.camera = cam

    # Key sun
    sun_data = bpy.data.lights.new(name="Key Sun", type="SUN")
    sun_data.energy = 3.0
    sun = bpy.data.objects.new("Key Sun", sun_data)
    sun.location = (span, span, span)
    sun.rotation_euler = (0.9, 0.0, -0.7)
    collection.objects.link(sun)

    # Fill area light
    fill_data = bpy.data.lights.new(name="Fill Area", type="AREA")
    fill_data.energy = span * span * 0.2
    fill_data.size = span
    fill_data.color = (0.43, 0.65, 1.0)
    fill = bpy.data.objects.new("Fill Area", fill_data)
    fill.location = (-span, -span, span * 0.6)
    fill.rotation_euler = (-0.6, 0.0, 2.4)
    collection.objects.link(fill)


def build_scene(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    clear_scene()
    setup_world()

    laterals_coll = ensure_collection("Laterals")
    markers_coll = ensure_collection("Markers")
    scene_coll = ensure_collection("Scene Setup")

    all_points_3d = []

    for lateral in data["laterals"]:
        leg = lateral["leg"]
        is_parent = lateral["is_parent"]
        is_producing = (leg == PRODUCING_LEG)

        if is_parent:
            # Split the parent bore at the intermediate casing shoe. Render the
            # cased section and open-hole section as distinct geometries with
            # different materials + wrap the cased section in a casing shell.
            cased_pts, openhole_pts = split_points_at_md(
                lateral["survey_points"], CASING_SHOE_MD_M,
            )

            cased_3d = [survey_point_to_blender(p) for p in cased_pts]
            openhole_3d = [survey_point_to_blender(p) for p in openhole_pts]
            all_points_3d.extend(cased_3d)
            all_points_3d.extend(openhole_3d)

            color = LATERAL_COLORS.get(leg, (0.5, 0.5, 0.5, 1.0))

            # Cased bore (inside steel casing).
            if len(cased_3d) >= 2:
                mat_cased = make_material(
                    "Parent-Cased-mat", color, emission_strength=1.8,
                    metallic=0.4, roughness=0.25,
                )
                create_tube_from_points(
                    "Leg-00 (PARENT · CASED)", cased_3d, WELLBORE_RADIUS_M,
                    mat_cased, laterals_coll,
                )
                # Casing shell: translucent steel shadow around the cased bore.
                mat_casing = make_material(
                    "Intermediate Casing-mat", CASING_SHELL_COLOR,
                    emission_strength=0.15, metallic=0.75, roughness=0.35,
                )
                # Alpha-blend the casing material so the bore shows through.
                if mat_casing.node_tree:
                    bsdf = mat_casing.node_tree.nodes.get("Principled BSDF")
                    if bsdf and "Alpha" in bsdf.inputs:
                        bsdf.inputs["Alpha"].default_value = 0.32
                    mat_casing.blend_method = "BLEND" if hasattr(
                        mat_casing, "blend_method") else mat_casing.blend_method
                create_tube_from_points(
                    "Intermediate Casing Shell", cased_3d,
                    CASING_SHELL_RADIUS_M, mat_casing, laterals_coll,
                )

            # Open-hole parent bore (pilot extension below the shoe).
            if len(openhole_3d) >= 2:
                mat_open = make_material(
                    "Parent-OpenHole-mat", OPEN_HOLE_COLOR,
                    emission_strength=0.3, metallic=0.05, roughness=0.8,
                )
                create_tube_from_points(
                    "Leg-00 (PARENT · OPEN HOLE)", openhole_3d,
                    OPEN_HOLE_RADIUS_M, mat_open, laterals_coll,
                )
            continue

        # Non-parent: render only the post-KOP branch.
        kop = lateral["kop_md_m"]
        pts = [p for p in lateral["survey_points"] if p["md_m"] >= kop]
        if len(pts) < 2:
            continue

        points_3d = [survey_point_to_blender(p) for p in pts]
        all_points_3d.extend(points_3d)

        radius = LATERAL_PRODUCING_RADIUS_M if is_producing else LATERAL_RADIUS_M
        color = LATERAL_COLORS.get(leg, (0.5, 0.5, 0.5, 1.0))
        emission = 3.5 if is_producing else 0.8

        tag = " (PRODUCING)" if is_producing else ""
        mat = make_material(
            f"Leg-{leg:02d}-mat{tag}",
            color,
            emission_strength=emission,
            metallic=0.5 if is_producing else 0.4,
            roughness=0.22 if is_producing else 0.3,
        )

        tube_name = f"Leg-{leg:02d}{tag}"
        create_tube_from_points(tube_name, points_3d, radius, mat,
                                laterals_coll)

        # KOP marker for non-parent legs
        if points_3d:
            kop_mat = make_material(
                f"KOP-Leg-{leg:02d}-mat",
                color,
                emission_strength=4.0,
                metallic=0.2,
                roughness=0.4,
            )
            create_sphere_marker(
                f"KOP-Leg-{leg:02d}",
                points_3d[0],
                KOP_MARKER_RADIUS_M,
                kop_mat,
                markers_coll,
            )

    # WellFi install point — interpolate on the PARENT bore at anchor MD.
    parent = next((l for l in data["laterals"] if l["is_parent"]), None)
    if parent is not None:
        anchor_pt = interpolate_md(parent["survey_points"], WELLFI_ANCHOR_MD_M)
        if anchor_pt is not None:
            anchor_mat = make_material(
                "WellFi Install Point mat",
                (0.94, 0.99, 1.0, 1.0),
                emission_strength=8.0,
                metallic=0.1,
                roughness=0.2,
            )
            create_sphere_marker(
                f"WellFi Install Point (Run 3 @ {WELLFI_ANCHOR_MD_M:.2f} m MD)",
                survey_point_to_blender(anchor_pt),
                WELLFI_MARKER_RADIUS_M,
                anchor_mat,
                markers_coll,
            )

    # KB surface marker (small ring at origin)
    origin_mat = make_material(
        "KB Surface mat", (0.95, 0.95, 0.95, 1.0),
        emission_strength=1.0, metallic=0.2, roughness=0.4,
    )
    create_sphere_marker("KB Surface", (0.0, 0.0, 0.0), WELLBORE_RADIUS_M * 1.2,
                         origin_mat, markers_coll)

    # Frame the camera around every visible point
    bounds_min = bounds_max = None
    if all_points_3d:
        xs = [p[0] for p in all_points_3d]
        ys = [p[1] for p in all_points_3d]
        zs = [p[2] for p in all_points_3d] + [0.0]  # include surface
        bounds_min = (min(xs), min(ys), min(zs))
        bounds_max = (max(xs), max(ys), max(zs))
        setup_camera_and_lights(bounds_min, bounds_max, scene_coll)

    # Reservoir top + base planes — translucent amber horizons the laterals drain.
    if bounds_min is not None and bounds_max is not None:
        reservoir_coll = ensure_collection("Reservoir")
        create_reservoir_planes(
            f"{RESERVOIR_NAME} Reservoir",
            RESERVOIR_TOP_TVD_M,
            RESERVOIR_BASE_TVD_M,
            RESERVOIR_COLOR,
            bounds_min,
            bounds_max,
            reservoir_coll,
        )

    # Render settings tuned for reasonable preview speed; user can up samples.
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 64
    scene.cycles.preview_samples = 16
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Frame viewport on the new geometry (if a 3D viewport exists).
    try:
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = {"area": area, "region": area.regions[-1]}
                with bpy.context.temp_override(**override):
                    bpy.ops.view3d.view_all()
                break
    except Exception as exc:  # pragma: no cover - defensive
        print(f"Could not auto-frame viewport: {exc}")

    leg_count = sum(1 for l in data["laterals"] if not l["is_parent"])
    print(f"Imported {len(data['laterals'])} legs "
          f"({leg_count} laterals + 1 parent) from {json_path}")


def parse_cli_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    args = {}
    i = 0
    while i < len(argv):
        token = argv[i]
        if token.startswith("--") and i + 1 < len(argv):
            args[token[2:]] = argv[i + 1]
            i += 2
        elif token.startswith("--"):
            args[token[2:]] = True
            i += 1
        else:
            i += 1
    return args


def main():
    args = parse_cli_args()
    json_path = args.get("input", DEFAULT_JSON_PATH)
    if not os.path.isabs(json_path):
        json_path = os.path.abspath(json_path)

    if not os.path.exists(json_path):
        print(f"ERROR: JSON not found at {json_path}")
        return

    build_scene(json_path)

    save = args.get("save")
    if save:
        save = os.path.abspath(save)
        os.makedirs(os.path.dirname(save), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=save)
        print(f"Saved .blend to {save}")


if __name__ == "__main__":
    main()
