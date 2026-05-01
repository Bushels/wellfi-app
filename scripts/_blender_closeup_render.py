"""Close-up hero render at the casing shoe — where cased bore transitions to
open hole — with dramatic lighting and a ground-truth overlay showing where
the steel ends and rock begins.
"""
import bpy
import os
import math
import mathutils

SHOE_MD_M = 921.0

# Find the casing-shoe world position by grabbing the last point of the cased
# bore curve.
cased_obj = bpy.data.objects.get("Leg-00 (PARENT · CASED)")
openhole_obj = bpy.data.objects.get("Leg-00 (PARENT · OPEN HOLE)")
wellfi_obj = next((o for o in bpy.data.objects if o.name.startswith("WellFi Install Point")), None)

if cased_obj is None or openhole_obj is None:
    raise RuntimeError("Run blender_import_multilaterals.py first.")

last_cased_co = cased_obj.matrix_world @ cased_obj.data.splines[0].bezier_points[-1].co
first_open_co = openhole_obj.matrix_world @ openhole_obj.data.splines[0].bezier_points[0].co
shoe_world = (last_cased_co + first_open_co) * 0.5

# Camera: position close to the shoe, slightly offset so both cased and
# open-hole are visible.
cam = bpy.data.objects.get("Wellbore Camera")
if cam is None:
    cam_data = bpy.data.cameras.new(name="Wellbore Camera")
    cam = bpy.data.objects.new("Wellbore Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)

cam.data.lens = 50
cam.data.clip_start = 0.5
cam.data.clip_end = 20000.0

# Look at the shoe from a 45-degree angle, ~80m away.
offset = mathutils.Vector((60.0, -55.0, 35.0))
cam.location = shoe_world + offset
direction = shoe_world - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

# DOF on the shoe.
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = offset.length
cam.data.dof.aperture_fstop = 3.5

bpy.context.scene.camera = cam

# Spotlight on the casing shoe transition to punch up the geometry.
spot_data = bpy.data.lights.new(name="Shoe Spot", type="SPOT")
spot_data.energy = 500000.0
spot_data.spot_size = math.radians(55)
spot_data.spot_blend = 0.35
spot_data.color = (1.0, 0.96, 0.85)
spot = bpy.data.objects.new("Shoe Spot", spot_data)
spot.location = shoe_world + mathutils.Vector((20.0, -30.0, 60.0))
sd = shoe_world - spot.location
spot.rotation_euler = sd.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(spot)

# Cool rim light from the open-hole side.
rim_data = bpy.data.lights.new(name="Rim Light", type="AREA")
rim_data.energy = 80000.0
rim_data.size = 40.0
rim_data.color = (0.45, 0.7, 1.0)
rim = bpy.data.objects.new("Rim Light", rim_data)
rim.location = shoe_world + mathutils.Vector((-40.0, 50.0, -20.0))
rd = shoe_world - rim.location
rim.rotation_euler = rd.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(rim)

# Cycles hi-quality
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 384
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

# Dim the background so the lights sculpt the form.
world = scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.015, 0.025, 0.045, 1.0)
        bg.inputs["Strength"].default_value = 0.45

OUT = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-shoe-closeup.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)

# Save blend so the user can tweak.
blend_out = r"C:\Users\kyle\MPS\Obsidian\wellfi-app\output\blender\obe-102-hz-shoe-closeup.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_out)

print(f"Close-up saved: {OUT}")
print(f"Scene saved: {blend_out}")
