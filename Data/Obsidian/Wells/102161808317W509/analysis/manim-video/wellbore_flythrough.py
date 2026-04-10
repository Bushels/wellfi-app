"""
wellbore_flythrough.py
3D well path flythrough for OBE 102 Hz 16-18-083-17W5/09.

Scene list:
    Scene0_WellPathTest  — proof-of-concept: colored well path + formation plane + WellFi marker
"""

import sys
import os

# Ensure well_data.py resolves regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manim import *
import numpy as np
from well_data import (
    WELL_PATH_3D, WELL_MD, md_to_3d, md_to_index,
    SURFACE_CASING_MD, BUILD_START_MD, BLUESKY_TOP_TVD,
    WELLFI_POSITION_MD, CASING_SHOE_MD,
    WELLFI_ON_BOTTOM_MD, JOINT_LENGTH, PEAK_SIGNAL_MD,
    FLUID_CONTACT_MD, NOISE_FLOOR_DBV, SIGNAL_DEPTH_POINTS,
)

# ---------------------------------------------------------------------------
# Palette — always use hex strings; Manim has conflicting named constants
# ---------------------------------------------------------------------------
BG_HEX        = "#06090f"
CYAN_HEX      = "#00D4FF"
AMBER_HEX     = "#F5A623"
GREEN_HEX     = "#2dd4a8"
WHITE_HEX     = "#f0f4f8"
DIM_HEX       = "#8b95a5"

# ---------------------------------------------------------------------------
# Well path crop parameters
# ---------------------------------------------------------------------------
CROP_MD = 1000.0   # Only visualise the interesting top section (vertical→build→landing)


def build_well_path_colored(points: np.ndarray, md_values: np.ndarray) -> VGroup:
    """
    Build a VGroup of Line3D segments, each coloured by stratigraphic section.

    Sections:
        0 – SURFACE_CASING_MD (126 m)  : white  — surface casing
        SURFACE_CASING_MD – BUILD_START_MD (370 m) : cyan  — vertical
        BUILD_START_MD – 790 m         : green  — build into formation
        790 m – CROP_MD                : amber  — horizontal Bluesky
    """
    HORIZONTAL_START_MD = 790.0   # MD where GR confirms Bluesky entry

    segments = VGroup()
    for i in range(len(points) - 1):
        md = float(md_values[i])
        p1 = points[i].tolist()
        p2 = points[i + 1].tolist()

        if md < SURFACE_CASING_MD:
            color = WHITE_HEX
        elif md < BUILD_START_MD:
            color = CYAN_HEX
        elif md < HORIZONTAL_START_MD:
            color = GREEN_HEX
        else:
            color = AMBER_HEX

        line = Line3D(
            start=p1,
            end=p2,
            color=color,
            thickness=0.03,
        )
        segments.add(line)

    return segments


def build_dotted_extension(
    start_point: np.ndarray,
    end_point: np.ndarray,
    n_dots: int = 12,
) -> VGroup:
    """
    Create a dotted / dashed hint line suggesting the horizontal continues beyond crop.
    Uses small spheres with decreasing opacity to produce a fade-out effect.
    """
    dots = VGroup()
    for i in range(n_dots):
        t = (i + 1) / n_dots
        pt = start_point + t * (end_point - start_point)
        opacity = max(0.05, 0.55 * (1 - t))
        dot = Sphere(radius=0.04, color=AMBER_HEX)
        dot.move_to(pt.tolist())
        dot.set_opacity(opacity)
        dots.add(dot)
    return dots


# ---------------------------------------------------------------------------
# Scene 0: well path test
# ---------------------------------------------------------------------------

class Scene0_WellPathTest(ThreeDScene):
    def construct(self):
        # ---------------------------------------------------------------
        # Camera & background
        # ---------------------------------------------------------------
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        # Center on the build section (mid-depth) and zoom in tight
        self.camera.frame_center = np.array([-0.5, 1.2, -3.3])
        self.camera.focal_distance = 8.0

        # ---------------------------------------------------------------
        # Crop the path to the interesting first 1000 m
        # ---------------------------------------------------------------
        crop_idx = md_to_index(CROP_MD)
        path_points = WELL_PATH_3D[:crop_idx + 1]
        path_md     = WELL_MD[:crop_idx + 1]

        # ---------------------------------------------------------------
        # Coloured well path
        # ---------------------------------------------------------------
        well_path = build_well_path_colored(path_points, path_md)

        # ---------------------------------------------------------------
        # Dotted extension beyond crop to hint at horizontal length
        # Extend roughly 3 Manim units (300 m) east along the horizontal
        # ---------------------------------------------------------------
        crop_end = path_points[-1]
        # The horizontal runs roughly due-east in this well; extend in X
        direction = np.array([1.5, 0.0, 0.0])  # approximate eastward extension
        extension_end = crop_end + direction
        dotted_ext = build_dotted_extension(crop_end, extension_end, n_dots=14)

        # ---------------------------------------------------------------
        # Bluesky formation top — translucent horizontal plane
        # Z = -TVD/100, so Bluesky top is at Z = -6.605
        # ---------------------------------------------------------------
        formation_z = -BLUESKY_TOP_TVD / 100.0   # -6.605

        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5],
            v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX,
            fill_opacity=0.12,
            stroke_width=0,
            checkerboard_colors=False,
        )

        # ---------------------------------------------------------------
        # WellFi tool marker — small glowing cyan sphere
        # ---------------------------------------------------------------
        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        tool_marker = Sphere(radius=0.12, color=CYAN_HEX)
        tool_marker.move_to(wellfi_3d.tolist())
        tool_marker.set_opacity(0.95)

        # Outer glow ring (larger, more transparent)
        tool_glow = Sphere(radius=0.22, color=CYAN_HEX)
        tool_glow.move_to(wellfi_3d.tolist())
        tool_glow.set_opacity(0.25)

        # ---------------------------------------------------------------
        # Animate
        # ---------------------------------------------------------------
        self.play(Create(well_path), run_time=4)
        self.play(
            FadeIn(formation_plane),
            FadeIn(dotted_ext),
            run_time=1.2,
        )
        self.play(
            FadeIn(tool_glow),
            FadeIn(tool_marker),
            run_time=1.0,
        )

        # Slow ambient rotation to show the 3D structure
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=0.5,
        )


# ---------------------------------------------------------------------------
# Scene 1: Title Card (5s) — 2D only
# ---------------------------------------------------------------------------

class Scene1_Title(Scene):
    """2D title card — no 3D needed."""
    def construct(self):
        self.camera.background_color = BG_HEX

        # Title
        title = Text(
            "WellFi Run 3",
            font_size=64,
            color=CYAN_HEX,
            font="Consolas",
            weight=BOLD,
        )

        # Subtitle
        sub = Text(
            "OBE 102 HZ 16-18-83-17W5  |  Bluesky Formation  |  663m TVD",
            font_size=24,
            color=DIM_HEX,
            font="Consolas",
        )
        sub.next_to(title, DOWN, buff=0.5)

        # Byline
        byline = Text(
            "3D Field Story  |  April 2\u20133, 2026",
            font_size=20,
            color="#F5A623",
            font="Consolas",
        )
        byline.next_to(sub, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(sub), run_time=0.8)
        self.play(FadeIn(byline), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ---------------------------------------------------------------------------
# Scene 2: Well Path Reveal (10s)
# ---------------------------------------------------------------------------

class Scene2_WellPathReveal(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.camera.frame_center = np.array([-0.5, 1.2, -3.3])
        self.camera.focal_distance = 8.0

        # Build the cropped well path
        crop_idx = md_to_index(CROP_MD)
        path_points = WELL_PATH_3D[:crop_idx + 1]
        path_md = WELL_MD[:crop_idx + 1]

        well_path = build_well_path_colored(path_points, path_md)

        # Dotted extension beyond crop
        crop_end = path_points[-1]
        extension_end = crop_end + np.array([1.5, 0.0, 0.0])
        dotted_ext = build_dotted_extension(crop_end, extension_end, n_dots=14)

        # Formation plane
        formation_z = -BLUESKY_TOP_TVD / 100.0
        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5],
            v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX,
            fill_opacity=0.10,
            stroke_width=0,
            checkerboard_colors=False,
        )

        # 2D labels (fixed in frame)
        label_surface = Text(
            "SURFACE CASING  126m",
            font_size=16,
            color=WHITE_HEX,
            font="Consolas",
        )
        label_surface.to_edge(UP + LEFT, buff=0.8)

        label_bluesky = Text(
            "BLUESKY FORMATION  660.5m TVD",
            font_size=16,
            color=GREEN_HEX,
            font="Consolas",
        )
        label_bluesky.to_edge(DOWN + LEFT, buff=0.8)

        self.add_fixed_in_frame_mobjects(label_surface, label_bluesky)
        label_surface.set_opacity(0)
        label_bluesky.set_opacity(0)

        # Animate: draw the well path progressively
        self.play(Create(well_path), run_time=4)
        self.play(
            FadeIn(formation_plane),
            FadeIn(dotted_ext),
            label_surface.animate.set_opacity(1),
            run_time=1.2,
        )
        self.play(label_bluesky.animate.set_opacity(1), run_time=0.8)

        # Slow rotation to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 3: Build Section Close-Up (8s)
# ---------------------------------------------------------------------------

class Scene3_BuildCloseUp(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_HEX

        # Start from the same orientation as Scene 2
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.camera.frame_center = np.array([-0.5, 1.2, -3.3])
        self.camera.focal_distance = 8.0

        # Build full cropped well path (static backdrop, dimmed)
        crop_idx = md_to_index(CROP_MD)
        path_points = WELL_PATH_3D[:crop_idx + 1]
        path_md = WELL_MD[:crop_idx + 1]
        well_path = build_well_path_colored(path_points, path_md)
        well_path.set_opacity(0.25)

        # Formation plane (dim)
        formation_z = -BLUESKY_TOP_TVD / 100.0
        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5],
            v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX,
            fill_opacity=0.08,
            stroke_width=0,
            checkerboard_colors=False,
        )

        # Build section highlight — bright green segments 370–790m MD
        build_start_idx = md_to_index(BUILD_START_MD)
        build_end_idx = md_to_index(790.0)
        build_points = WELL_PATH_3D[build_start_idx:build_end_idx + 1]
        build_md = WELL_MD[build_start_idx:build_end_idx + 1]

        build_highlight = VGroup()
        for i in range(len(build_points) - 1):
            line = Line3D(
                start=build_points[i].tolist(),
                end=build_points[i + 1].tolist(),
                color=GREEN_HEX,
                thickness=0.05,
            )
            build_highlight.add(line)

        # WellFi tool marker at 819.9m MD
        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        tool_marker = Sphere(radius=0.12, color=CYAN_HEX)
        tool_marker.move_to(wellfi_3d.tolist())

        # 2D labels
        inc_label = Text(
            "BUILD SECTION  0\u00b0 \u2192 86\u00b0",
            font_size=20,
            color=GREEN_HEX,
            font="Consolas",
        )
        inc_label.to_edge(UP, buff=0.6)

        wellfi_label = Text(
            "WellFi TOOL  819.9m MD  |  663.1m TVD",
            font_size=18,
            color=CYAN_HEX,
            font="Consolas",
        )
        wellfi_label.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(inc_label, wellfi_label)
        inc_label.set_opacity(0)
        wellfi_label.set_opacity(0)

        # Start with the full dim path visible
        self.add(well_path, formation_plane)

        # Zoom camera toward the build section center
        build_center = md_to_3d(580.0)  # Midpoint of build section

        self.play(
            Create(build_highlight),
            inc_label.animate.set_opacity(1),
            run_time=2.5,
        )

        # Move camera closer to the build section
        self.move_camera(
            phi=55 * DEGREES,
            theta=-40 * DEGREES,
            frame_center=build_center.tolist(),
            run_time=2.0,
        )

        self.play(
            FadeIn(tool_marker),
            wellfi_label.animate.set_opacity(1),
            run_time=1.0,
        )

        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 4: Tool Descent — RIH Animation (12s)
# ---------------------------------------------------------------------------

class Scene4_ToolDescent(ThreeDScene):
    """Animated tool descent along the well path with signal degradation."""
    def construct(self):
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.camera.frame_center = np.array([-0.5, 1.2, -3.3])
        self.camera.focal_distance = 8.0

        # Static well path (dim backdrop)
        crop_idx = md_to_index(CROP_MD)
        path_points = WELL_PATH_3D[:crop_idx + 1]
        path_md = WELL_MD[:crop_idx + 1]
        well_path = build_well_path_colored(path_points, path_md)
        well_path.set_opacity(0.2)

        # Formation plane (dim)
        formation_z = -BLUESKY_TOP_TVD / 100.0
        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5], v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX, fill_opacity=0.08,
            stroke_width=0, checkerboard_colors=False,
        )

        self.add(well_path, formation_plane)

        # Tool descent points — surface to on-bottom (832.3m MD)
        bottom_idx = md_to_index(WELLFI_ON_BOTTOM_MD)
        descent_points = WELL_PATH_3D[:bottom_idx + 1]

        # Build a VMobject path for MoveAlongPath
        descent_curve = VMobject()
        descent_curve.set_points_as_corners([p.tolist() for p in descent_points])
        descent_curve.set_stroke(opacity=0)  # invisible — just for MoveAlongPath

        # The tool — a glowing amber sphere
        tool = Sphere(radius=0.10, color=AMBER_HEX)
        tool.move_to(descent_points[0].tolist())

        # Trail ValueTracker + always_redraw
        progress = ValueTracker(0)

        def get_trail():
            t = progress.get_value()
            n_points = max(2, int(t * len(descent_points)))
            trail_pts = descent_points[:n_points]
            trail = VMobject()
            trail.set_points_as_corners([p.tolist() for p in trail_pts])
            trail.set_stroke(color=CYAN_HEX, width=3, opacity=0.6)
            return trail

        trail_mob = always_redraw(get_trail)

        # Signal strength label (fixed in frame)
        signal_label = Text("SIGNAL: —", font_size=18, color=CYAN_HEX, font="Consolas")
        signal_label.to_edge(UP + RIGHT, buff=0.6)
        self.add_fixed_in_frame_mobjects(signal_label)
        signal_label.set_opacity(0)

        self.add(trail_mob, tool)

        # Animate descent over 6 seconds
        self.play(
            MoveAlongPath(tool, descent_curve, rate_func=smooth),
            progress.animate.set_value(1.0),
            signal_label.animate.set_opacity(1),
            run_time=6,
        )

        # On bottom label
        bottom_label = Text(
            "ON BOTTOM  832m MD  |  -100 dBV",
            font_size=18, color="#dc2626", font="Consolas",
        )
        bottom_label.to_edge(DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(bottom_label)
        bottom_label.set_opacity(0)

        self.play(
            tool.animate.set_color("#dc2626"),
            bottom_label.animate.set_opacity(1),
            run_time=1.0,
        )

        self.wait(2)

        # Signal below noise floor — tool pulses dim
        for _ in range(3):
            self.play(tool.animate.set_opacity(0.3), run_time=0.5)
            self.play(tool.animate.set_opacity(0.8), run_time=0.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 5: Signal Failure — On Bottom (6s)
# ---------------------------------------------------------------------------

class Scene5_SignalFailure(ThreeDScene):
    """Tool sitting on bottom, signal at noise floor, 84-min blackout."""
    def construct(self):
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=55 * DEGREES, theta=-40 * DEGREES)

        # Zoom to bottom-hole area
        bottom_3d = md_to_3d(WELLFI_ON_BOTTOM_MD)
        self.camera.frame_center = bottom_3d.tolist()
        self.camera.focal_distance = 6.0

        # Local well path around bottom (last ~200m of crop)
        local_start_idx = md_to_index(700.0)
        crop_idx = md_to_index(CROP_MD)
        local_points = WELL_PATH_3D[local_start_idx:crop_idx + 1]
        local_md = WELL_MD[local_start_idx:crop_idx + 1]
        local_path = build_well_path_colored(local_points, local_md)
        local_path.set_opacity(0.3)

        # Formation plane
        formation_z = -BLUESKY_TOP_TVD / 100.0
        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5], v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX, fill_opacity=0.06,
            stroke_width=0, checkerboard_colors=False,
        )

        # Tool on bottom — red, dim, pulsing
        tool = Sphere(radius=0.14, color="#dc2626")
        tool.move_to(bottom_3d.tolist())
        tool.set_opacity(0.5)

        # Glow ring
        glow = Sphere(radius=0.28, color="#dc2626")
        glow.move_to(bottom_3d.tolist())
        glow.set_opacity(0.15)

        self.add(local_path, formation_plane, glow, tool)

        # Labels
        status_label = Text(
            "SIGNAL BELOW NOISE FLOOR",
            font_size=22, color="#dc2626", font="Consolas",
        )
        status_label.to_edge(UP, buff=0.6)

        crc_label = Text(
            "33% CRC PASS RATE  |  84-MINUTE BLACKOUT",
            font_size=18, color=DIM_HEX, font="Consolas",
        )
        crc_label.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(status_label, crc_label)
        status_label.set_opacity(0)
        crc_label.set_opacity(0)

        self.play(status_label.animate.set_opacity(1), run_time=1.0)

        # Pulsing tool — barely alive
        for _ in range(3):
            self.play(tool.animate.set_opacity(0.2), run_time=0.6)
            self.play(tool.animate.set_opacity(0.6), run_time=0.6)

        self.play(crc_label.animate.set_opacity(1), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 6: Pulled 1 Joint (8s)
# ---------------------------------------------------------------------------

class Scene6_PulledJoint(ThreeDScene):
    """Tool moves UP 9.456m — signal restored, blackout ends."""
    def construct(self):
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=55 * DEGREES, theta=-40 * DEGREES)

        bottom_3d = md_to_3d(WELLFI_ON_BOTTOM_MD)
        self.camera.frame_center = bottom_3d.tolist()
        self.camera.focal_distance = 6.0

        # Local well path
        local_start_idx = md_to_index(700.0)
        crop_idx = md_to_index(CROP_MD)
        local_points = WELL_PATH_3D[local_start_idx:crop_idx + 1]
        local_md = WELL_MD[local_start_idx:crop_idx + 1]
        local_path = build_well_path_colored(local_points, local_md)
        local_path.set_opacity(0.3)

        # Formation plane
        formation_z = -BLUESKY_TOP_TVD / 100.0
        formation_plane = Surface(
            lambda u, v: np.array([u, v, formation_z]),
            u_range=[-3.5, 2.5], v_range=[-0.5, 5.5],
            fill_color=GREEN_HEX, fill_opacity=0.06,
            stroke_width=0, checkerboard_colors=False,
        )

        # Tool starts on bottom (red)
        tool = Sphere(radius=0.14, color="#dc2626")
        tool.move_to(bottom_3d.tolist())
        tool.set_opacity(0.5)

        self.add(local_path, formation_plane, tool)

        # Labels
        action_label = Text(
            "PULLING 1 JOINT  —  9.456m",
            font_size=22, color=AMBER_HEX, font="Consolas",
        )
        action_label.to_edge(UP, buff=0.6)

        result_label = Text(
            "84-MIN BLACKOUT ENDED  |  SIGNAL RESTORED",
            font_size=20, color=CYAN_HEX, font="Consolas",
        )
        result_label.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(action_label, result_label)
        action_label.set_opacity(0)
        result_label.set_opacity(0)

        self.play(action_label.animate.set_opacity(1), run_time=0.8)

        # Move tool UP to new position (819.9m MD)
        new_pos = md_to_3d(WELLFI_POSITION_MD)

        self.play(
            tool.animate.move_to(new_pos.tolist()).set_color(AMBER_HEX).set_opacity(0.9),
            run_time=2.0,
            rate_func=smooth,
        )

        self.wait(0.5)

        # Signal restored — tool turns cyan
        self.play(
            tool.animate.set_color(CYAN_HEX),
            result_label.animate.set_opacity(1),
            run_time=1.2,
        )

        # New position label
        pos_label = Text(
            "NEW POSITION  819.9m MD  |  663.1m TVD",
            font_size=16, color=DIM_HEX, font="Consolas",
        )
        pos_label.next_to(result_label, UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(pos_label)
        pos_label.set_opacity(0)
        self.play(pos_label.animate.set_opacity(1), run_time=0.8)

        # Camera slowly pulls back
        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            run_time=2.0,
        )

        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 7: Pump Start Visualization (8s)
# ---------------------------------------------------------------------------

class Scene7_PumpStart(ThreeDScene):
    """Pump starts — fluid flow, temperature drop, pressure readout."""
    def construct(self):
        self.camera.background_color = BG_HEX
        self.set_camera_orientation(phi=55*DEGREES, theta=-40*DEGREES)

        # Position camera near the tool
        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        self.camera.frame_center = wellfi_3d.tolist()
        self.camera.focal_distance = 6.0

        # Local well path (dim)
        local_start_idx = md_to_index(700.0)
        crop_idx = md_to_index(CROP_MD)
        local_points = WELL_PATH_3D[local_start_idx:crop_idx + 1]
        local_md = WELL_MD[local_start_idx:crop_idx + 1]
        local_path = build_well_path_colored(local_points, local_md)
        local_path.set_opacity(0.2)

        # WellFi tool (cyan, at 819.9m MD)
        tool = Sphere(radius=0.12, color=CYAN_HEX)
        tool.move_to(wellfi_3d.tolist())

        self.add(local_path, tool)

        # 2D overlay labels (fixed in frame)
        pump_label = Text(
            "PUMP START  |  Apr 2, 17:38",
            font_size=22, color=AMBER_HEX, font="Consolas",
        )
        pump_label.to_edge(UP, buff=0.5)

        # Pressure readout — will update
        pressure_text = Text(
            "P: 2075 kPa  |  T: 24.8\u00b0C",
            font_size=20, color=CYAN_HEX, font="Consolas",
        )
        pressure_text.to_edge(DOWN + LEFT, buff=0.6)

        self.add_fixed_in_frame_mobjects(pump_label, pressure_text)
        pump_label.set_opacity(0)
        pressure_text.set_opacity(0)

        self.play(pump_label.animate.set_opacity(1), run_time=0.8)
        self.wait(0.5)

        # Show pressure readout
        self.play(pressure_text.animate.set_opacity(1), run_time=0.8)
        self.wait(1.0)

        # Cold slug — temperature drops, tool pulses amber
        cold_slug_text = Text(
            "COLD SLUG  |  T: 15.2\u00b0C",
            font_size=20, color=AMBER_HEX, font="Consolas",
        )
        cold_slug_text.to_edge(DOWN + LEFT, buff=0.6)
        self.add_fixed_in_frame_mobjects(cold_slug_text)
        cold_slug_text.set_opacity(0)

        self.play(
            pressure_text.animate.set_opacity(0),
            cold_slug_text.animate.set_opacity(1),
            tool.animate.set_color(AMBER_HEX),
            run_time=1.0,
        )
        self.wait(0.8)

        # Steady state — temperature recovers
        steady_text = Text(
            "STEADY STATE  |  P: 2069 kPa  |  T: 21.6\u00b0C",
            font_size=20, color=CYAN_HEX, font="Consolas",
        )
        steady_text.to_edge(DOWN + LEFT, buff=0.6)
        self.add_fixed_in_frame_mobjects(steady_text)
        steady_text.set_opacity(0)

        self.play(
            cold_slug_text.animate.set_opacity(0),
            steady_text.animate.set_opacity(1),
            tool.animate.set_color(CYAN_HEX),
            run_time=1.0,
        )
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ---------------------------------------------------------------------------
# Scene 8: Overnight + Morning (6s)
# ---------------------------------------------------------------------------

class Scene8_Overnight(Scene):
    """Time compression: overnight drawdown, morning resume. 2D scene."""
    def construct(self):
        self.camera.background_color = BG_HEX

        # Night indicator
        night_text = Text(
            "OVERNIGHT",
            font_size=48, color=DIM_HEX, font="Consolas",
        )

        # Pressure change
        pressure_before = Text(
            "P: 2069 kPa",
            font_size=28, color=CYAN_HEX, font="Consolas",
        )
        pressure_before.next_to(night_text, DOWN, buff=0.8)

        arrow = Text(
            "\u25bc",
            font_size=36, color=AMBER_HEX, font="Consolas",
        )
        arrow.next_to(pressure_before, DOWN, buff=0.3)

        pressure_after = Text(
            "P: 1951 kPa",
            font_size=28, color=AMBER_HEX, font="Consolas",
        )
        pressure_after.next_to(arrow, DOWN, buff=0.3)

        time_label = Text(
            "\u22121.18 BAR OVERNIGHT DRAWDOWN",
            font_size=18, color=DIM_HEX, font="Consolas",
        )
        time_label.next_to(pressure_after, DOWN, buff=0.5)

        # Morning resume
        morning_text = Text(
            "Apr 3, 10:56  \u2014  MORNING RESUME",
            font_size=20, color=GREEN_HEX, font="Consolas",
        )
        morning_text.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(night_text), run_time=1.0)
        self.play(FadeIn(pressure_before), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(arrow), FadeIn(pressure_after), run_time=1.0)
        self.play(FadeIn(time_label), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(morning_text), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
