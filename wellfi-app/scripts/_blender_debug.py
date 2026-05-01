"""Print diagnostic info about the wellbore scene: bounds, camera, object list."""
import bpy

coll = bpy.data.collections.get("Laterals")
print("=== Scene Debug ===")
print(f"Total curves: {len(bpy.data.curves)}")
print(f"Total objects: {len(bpy.data.objects)}")

if coll:
    pts = []
    for obj in coll.objects:
        if obj.type != "CURVE":
            continue
        spline = obj.data.splines[0] if obj.data.splines else None
        if spline is None:
            continue
        for bp in spline.bezier_points:
            pts.append(obj.matrix_world @ bp.co)
    if pts:
        xs = [p.x for p in pts]
        ys = [p.y for p in pts]
        zs = [p.z for p in pts]
        print(f"Points: {len(pts)}")
        print(f"  X: {min(xs):.1f} .. {max(xs):.1f}  (span {max(xs)-min(xs):.1f})")
        print(f"  Y: {min(ys):.1f} .. {max(ys):.1f}  (span {max(ys)-min(ys):.1f})")
        print(f"  Z: {min(zs):.1f} .. {max(zs):.1f}  (span {max(zs)-min(zs):.1f})")

cam = bpy.data.objects.get("Wellbore Camera")
if cam:
    print(f"Camera location: {cam.location}")
    print(f"Camera rotation: {cam.rotation_euler}")
    print(f"Camera lens: {cam.data.lens}mm")
    print(f"Camera clip start: {cam.data.clip_start}  end: {cam.data.clip_end}")

for obj in bpy.data.objects:
    if obj.type in ("CURVE", "MESH"):
        bb = obj.bound_box
        print(f"  {obj.name}: location {obj.location}, visible={obj.visible_get()}")
