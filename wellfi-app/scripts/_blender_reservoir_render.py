"""Re-import the multi-laterals (now with reservoir slab) and render a wide hero
shot that shows the Bluesky formation with every lateral weaving through it.
"""
import bpy
import os
import math
import runpy
import mathutils

IMPORT_PATH = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\scripts\blender_import_multilaterals.py"
runpy.run_path(IMPORT_PATH, run_name="__main__")

# Frame the camera looking down the fan of laterals, slightly elevated so the
# reservoir slab reads as a thin amber horizon.
coll = bpy.data.collections.get("Laterals")
pts = []
for obj in coll.objects:
    if obj.type != "CURVE":
        continue
    for spline in obj.data.splines:
        for bp in spline.bezier_points:
            pts.append(obj.matrix_world @ bp.co)

xs = [p.x for p in pts]
ys = [p.y for p in pts]
zs = [p.z for p in pts] + [0.0]
cx = (min(xs) + max(xs)) / 2
cy = (min(ys) + max(ys)) / 2
cz = (min(zs) + max(zs)) / 2
span_x = max(xs) - min(xs)
span_y = max(ys) - min(ys)
span_z = max(zs) - min(zs)
span = max(span_x, span_y, span_z, 200.0)

lens_mm = 32
distance = (span * 0.72) / math.tan(math.radians(28))

cam = bpy.data.objects.get("Wellbore Camera")
cam.data.lens = lens_mm
cam.data.clip_start = 1.0
cam.data.clip_end = max(distance * 4, 20000.0)
# Slightly lower elevation so the reservoir slab reads edge-on as a horizon.
cam.location = (cx + distance * 0.4, cy - distance * 0.85, cz + distance * 0.32)
direction = mathutils.Vector((cx, cy, cz)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

# DOF on the WellFi install point.
wellfi = next((o for o in bpy.data.objects if o.name.startswith("WellFi Install Point")), None)
if wellfi is not None:
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (wellfi.location - cam.location).length
    cam.data.dof.aperture_fstop = 4.5

scene = bpy.context.scene
# EEVEE_NEXT gives reliable alpha blending for the reservoir slab in seconds;
# Cycles' alpha handling on solid meshes is finicky without volume shaders.
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE"
# Bump sampling for a clean EEVEE render.
try:
    scene.eevee.taa_render_samples = 128
except Exception:
    pass
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_depth = "16"

# Import script already builds proper translucent materials for the reservoir
# planes; no material overrides needed here.

world = scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.03, 0.05, 0.10, 1.0)
        bg.inputs["Strength"].default_value = 0.8

OUT = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-reservoir-hero.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)

blend_out = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-reservoir.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_out)

print(f"Reservoir hero saved: {OUT}")
print(f"Scene saved: {blend_out}")
