"""Render a quick EEVEE preview of the current Blender scene to PNG.

Frames the camera based on the actual bounds of the "Laterals" collection and
extends near/far clipping so nothing is culled.
"""
import bpy
import os
import math
import mathutils

OUTPUT_PATH = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-preview.png"

coll = bpy.data.collections.get("Laterals")
if coll is None:
    raise RuntimeError("Laterals collection not found.")

pts = []
for obj in coll.objects:
    if obj.type != "CURVE":
        continue
    for spline in obj.data.splines:
        for bp in spline.bezier_points:
            pts.append(obj.matrix_world @ bp.co)

if not pts:
    raise RuntimeError("No lateral curve points found.")

xs = [p.x for p in pts]
ys = [p.y for p in pts]
zs = [p.z for p in pts] + [0.0]
cx = (min(xs) + max(xs)) / 2
cy = (min(ys) + max(ys)) / 2
cz = (min(zs) + max(zs)) / 2
span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
span = max(span, 200.0)

# 35mm lens / 36mm sensor -> horizontal FOV ~54°. Distance to frame the span
# with a small margin.
distance = (span * 0.7) / math.tan(math.radians(27))

cam = bpy.data.objects.get("Wellbore Camera")
if cam is None:
    cam_data = bpy.data.cameras.new(name="Wellbore Camera")
    cam = bpy.data.objects.new("Wellbore Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)

cam.data.lens = 35
cam.data.clip_start = 1.0
cam.data.clip_end = max(distance * 4, 20000.0)
cam.location = (cx + distance * 0.55, cy - distance * 0.75,
                cz + distance * 0.45)
direction = mathutils.Vector((cx, cy, cz)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.camera = cam

print(f"Bounds center: ({cx:.1f}, {cy:.1f}, {cz:.1f}) span={span:.1f}m")
print(f"Camera at: {tuple(round(v, 1) for v in cam.location)}")
print(f"Camera clip: {cam.data.clip_start} .. {cam.data.clip_end}")

# Pick EEVEE for fast preview. Blender 5 uses BLENDER_EEVEE_NEXT.
scene = bpy.context.scene
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE"

scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT_PATH

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
bpy.ops.render.render(write_still=True)
print(f"Rendered to {OUTPUT_PATH}")
