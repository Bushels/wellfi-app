"""Re-import the multi-laterals (now with casing/open-hole split) and render a
Cycles hi-res hero image with DOF focused on the WellFi install point.
"""
import bpy
import os
import math
import runpy
import mathutils

# Re-import the scene (clears any previous state).
IMPORT_PATH = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\scripts\blender_import_multilaterals.py"
runpy.run_path(IMPORT_PATH, run_name="__main__")

# --- Re-frame the camera using actual bounds -------------------------------
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
span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
span = max(span, 200.0)
lens_mm = 28
distance = (span * 0.7) / math.tan(math.radians(30))

cam = bpy.data.objects.get("Wellbore Camera")
cam.data.lens = lens_mm
cam.data.clip_start = 1.0
cam.data.clip_end = max(distance * 4, 20000.0)
cam.location = (cx + distance * 0.55, cy - distance * 0.75,
                cz + distance * 0.5)
target = mathutils.Vector((cx, cy, cz))
direction = target - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

# DOF focused on the WellFi install marker, aperture shallow enough to pop it.
wellfi = None
for obj in bpy.data.objects:
    if obj.name.startswith("WellFi Install Point"):
        wellfi = obj
        break
if wellfi is not None:
    dof = cam.data.dof
    dof.use_dof = True
    dof.focus_distance = (wellfi.location - cam.location).length
    dof.aperture_fstop = 3.2

# --- Hi-res Cycles settings ------------------------------------------------
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 256
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception:
    pass

scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_depth = "16"

# Slightly brighter world so the open-hole sandstone reads well.
world = scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.04, 0.06, 0.11, 1.0)
        bg.inputs["Strength"].default_value = 1.2

OUT = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-casing-split-hires.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print(f"Hi-res render saved: {OUT}")

# Save the .blend alongside.
blend_out = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-casing-split.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_out)
print(f"Scene saved: {blend_out}")
