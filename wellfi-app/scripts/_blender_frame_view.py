"""Viewport helper: clip distances, material preview, frame, and switch to camera view."""
import bpy

for area in bpy.context.screen.areas:
    if area.type != "VIEW_3D":
        continue
    space = area.spaces[0]
    space.clip_start = 0.01
    space.clip_end = 20000.0
    space.shading.type = "MATERIAL"
    region = next((r for r in area.regions if r.type == "WINDOW"), area.regions[-1])
    with bpy.context.temp_override(area=area, region=region):
        # Deselect everything so material colors display without selection outlines.
        bpy.ops.object.select_all(action="DESELECT")
        # View through the "Wellbore Camera" object the import script placed.
        cam = bpy.data.objects.get("Wellbore Camera")
        if cam is not None:
            bpy.context.scene.camera = cam
            bpy.ops.view3d.view_camera()
        else:
            bpy.ops.view3d.view_all()
    break

# Switch to EEVEE for a fast viewport preview; keep Cycles as scene engine.
# (Viewport shading mode is separate from final-render engine.)
print("View configured: material shading, camera view, select cleared.")
