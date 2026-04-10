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
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)
        # Zoom out a bit so the full well path fits in frame
        self.camera.frame_center = np.array([-0.8, 2.0, -3.5])

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
