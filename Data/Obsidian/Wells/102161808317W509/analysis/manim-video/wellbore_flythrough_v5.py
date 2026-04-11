"""
wellbore_flythrough_v5.py

WellFi Run 3 — merged v5.
Architecture: WellFiBase3DScene (Codex) + 12-scene story (our narrative).
All pressures in kPa. All labels centered. Full casing string in every 3D scene.
"""

import os
import sys
from typing import Iterable

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from well_data import (
    WELL_PATH_3D, WELL_MD, md_to_3d, md_to_index,
    SURFACE_CASING_MD, BUILD_START_MD, BLUESKY_TOP_TVD,
    WELLFI_POSITION_MD, CASING_SHOE_MD,
    WELLFI_ON_BOTTOM_MD, JOINT_LENGTH, PEAK_SIGNAL_MD,
    FLUID_CONTACT_MD, NOISE_FLOOR_DBV, SIGNAL_DEPTH_POINTS,
)

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG_HEX      = "#06090f"
CYAN_HEX    = "#00D4FF"
AMBER_HEX   = "#F5A623"
GREEN_HEX   = "#2dd4a8"
CRIMSON_HEX = "#dc2626"
WHITE_HEX   = "#f0f4f8"
DIM_HEX     = "#8b95a5"
PANEL_HEX   = "#09131d"
FONT        = "Consolas"

CROP_MD            = 1000.0
HORIZONTAL_START_MD = 790.0

# ---------------------------------------------------------------------------
# RIH event data (times + signal in dBV — converted to kPa where pressure shown)
# ---------------------------------------------------------------------------
RIH_EVENTS = [
    {
        "time": "11:22",
        "md": 113.6,
        "signal_dbv": -51.0,
        "pressure_kpa": None,
        "label": "First signal",
        "summary": "Receiver first sees the tool while still shallow in casing.",
        "color": CYAN_HEX,
    },
    {
        "time": "11:37",
        "md": PEAK_SIGNAL_MD,
        "signal_dbv": -37.0,
        "pressure_kpa": None,
        "label": "Peak coupling",
        "summary": "Best EM coupling occurs far above the fluid column.",
        "color": GREEN_HEX,
    },
    {
        "time": "11:55",
        "md": FLUID_CONTACT_MD,
        "signal_dbv": -55.0,
        "pressure_kpa": 120.0,
        "label": "Hit fluid",
        "summary": "Pressure jumps as soon as the tool enters the fluid column.",
        "color": AMBER_HEX,
    },
    {
        "time": "12:10",
        "md": 662.1,
        "signal_dbv": -88.0,
        "pressure_kpa": 1567.0,
        "label": "Deep in fluid",
        "summary": "Fluid attenuates signal faster than the air-filled section.",
        "color": AMBER_HEX,
    },
    {
        "time": "12:28",
        "md": WELLFI_ON_BOTTOM_MD,
        "signal_dbv": -96.0,
        "pressure_kpa": 2079.0,
        "label": "On bottom",
        "summary": "Tool lands below the noise floor — telemetry becomes unreliable.",
        "color": CRIMSON_HEX,
    },
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_cropped_path(crop_md: float = CROP_MD) -> tuple[np.ndarray, np.ndarray]:
    crop_idx = md_to_index(crop_md)
    return WELL_PATH_3D[: crop_idx + 1], WELL_MD[: crop_idx + 1]


def well_color_for_md(md_value: float) -> str:
    if md_value < SURFACE_CASING_MD:
        return WHITE_HEX
    if md_value < BUILD_START_MD:
        return CYAN_HEX
    if md_value < HORIZONTAL_START_MD:
        return GREEN_HEX
    return AMBER_HEX


def build_colored_well_path(
    points: np.ndarray,
    md_values: np.ndarray,
    thickness: float = 0.035,
    opacity: float = 1.0,
) -> VGroup:
    segments = VGroup()
    for i in range(len(points) - 1):
        line = Line3D(
            start=points[i].tolist(),
            end=points[i + 1].tolist(),
            color=well_color_for_md(float(md_values[i])),
            thickness=thickness,
        )
        line.set_opacity(opacity)
        segments.add(line)
    return segments


def build_dotted_extension(
    start_point: np.ndarray,
    end_point: np.ndarray,
    n_dots: int = 14,
) -> VGroup:
    dots = VGroup()
    for i in range(n_dots):
        t = (i + 1) / n_dots
        pt = start_point + t * (end_point - start_point)
        opacity = max(0.04, 0.55 * (1 - t))
        dot = Sphere(radius=0.035, color=AMBER_HEX)
        dot.move_to(pt.tolist())
        dot.set_opacity(opacity)
        dots.add(dot)
    return dots


def build_formation_plane(opacity: float = 0.11) -> Surface:
    formation_z = -BLUESKY_TOP_TVD / 100.0
    return Surface(
        lambda u, v: np.array([u, v, formation_z]),
        u_range=[-3.6, 2.7],
        v_range=[-0.8, 5.8],
        fill_color=GREEN_HEX,
        fill_opacity=opacity,
        stroke_width=0,
        checkerboard_colors=False,
    )


def build_tool_marker(
    point: np.ndarray,
    core_color: str = CYAN_HEX,
    glow_color: str | None = None,
    core_radius: float = 0.12,
    glow_radius: float = 0.24,
    glow_opacity: float = 0.22,
) -> tuple[Sphere, Sphere]:
    glow = Sphere(radius=glow_radius, color=glow_color or core_color)
    glow.move_to(point.tolist())
    glow.set_opacity(glow_opacity)
    core = Sphere(radius=core_radius, color=core_color)
    core.move_to(point.tolist())
    core.set_opacity(0.96)
    return core, glow


def make_text_line(
    text: str,
    font_size: int = 18,
    color: str = WHITE_HEX,
    weight: str = NORMAL,
) -> Text:
    return Text(text, font_size=font_size, color=color, font=FONT, weight=weight)


def make_panel(
    title: str,
    lines: Iterable,
    accent: str = CYAN_HEX,
    title_size: int = 18,
    line_size: int = 16,
) -> VGroup:
    body_items = []
    if title:
        body_items.append(make_text_line(title.upper(), font_size=title_size, color=accent, weight=BOLD))
    for line in lines:
        if isinstance(line, Mobject):
            body_items.append(line)
        else:
            body_items.append(make_text_line(str(line), font_size=line_size, color=WHITE_HEX))
    content = VGroup(*body_items).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    background = BackgroundRectangle(content, color=PANEL_HEX, fill_opacity=0.84, buff=0.22)
    border = SurroundingRectangle(content, color=accent, buff=0.22, stroke_width=1.5)
    return VGroup(background, border, content)


def make_metric_card(
    label: str,
    value: str,
    accent: str,
    footnote: str | None = None,
) -> VGroup:
    lines: list = [
        make_text_line(label.upper(), font_size=14, color=DIM_HEX),
        make_text_line(value, font_size=28, color=accent, weight=BOLD),
    ]
    if footnote:
        lines.append(make_text_line(footnote, font_size=14, color=WHITE_HEX))
    return make_panel("", lines, accent=accent, line_size=14)


def make_title_stack(
    eyebrow: str,
    title: str,
    subtitle: str,
    width_limit: float | None = None,
) -> VGroup:
    eyebrow_text = Text(eyebrow.upper(), font_size=18, color=AMBER_HEX, font=FONT)
    title_text = Text(title, font_size=36, color=WHITE_HEX, font=FONT, weight=BOLD)
    subtitle_text = Text(subtitle, font_size=18, color=DIM_HEX, font=FONT)
    group = VGroup(eyebrow_text, title_text, subtitle_text).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    if width_limit and group.width > width_limit:
        group.scale_to_fit_width(width_limit)
    return group


def add_fixed_group(scene: Scene, mob: Mobject) -> None:
    scene.add_fixed_in_frame_mobjects(*mob.family_members_with_points())


def normalize_panel(panel: VGroup) -> None:
    if len(panel) < 2:
        return
    panel[0].set_fill(PANEL_HEX, opacity=0.84)
    panel[0].set_stroke(opacity=0)
    panel[1].set_fill(opacity=0)


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class WellFiBase3DScene(ThreeDScene):
    def setup_bg(self) -> None:
        self.camera.background_color = BG_HEX

    def setup_overview_camera(self) -> None:
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.camera.frame_center = np.array([-0.5, 1.25, -3.35])
        self.camera.focal_distance = 8.0

    def setup_local_camera(self, md_value: float, phi: float = 58, theta: float = -42) -> None:
        self.set_camera_orientation(phi=phi * DEGREES, theta=theta * DEGREES)
        self.camera.frame_center = md_to_3d(md_value).tolist()
        self.camera.focal_distance = 6.2

    def build_world(
        self,
        opacity: float = 0.95,
        thickness: float = 0.038,
        plane_opacity: float = 0.10,
    ) -> tuple[VGroup, VGroup, Surface]:
        path_points, path_md = get_cropped_path()
        path = build_colored_well_path(path_points, path_md, thickness=thickness, opacity=opacity)
        extension = build_dotted_extension(
            path_points[-1],
            path_points[-1] + np.array([1.45, 0.0, 0.0]),
        )
        plane = build_formation_plane(opacity=plane_opacity)
        return path, extension, plane


# ===========================================================================
# Scene 1: Title (2D, 5s)
# ===========================================================================

class Scene1_Title(Scene):
    """2D title card — no 3D needed."""
    def construct(self):
        self.camera.background_color = BG_HEX

        header = make_title_stack(
            "WellFi Run 3  |  OBE 102 HZ 16-18-083-17W5/09",
            "WellFi Run 3",
            "OBE 102 HZ 16-18-83-17W5  |  Bluesky Formation  |  663m TVD",
            width_limit=10.6,
        )
        # Override: make the title itself look correct
        title_big = Text(
            "WellFi Run 3",
            font_size=64,
            color=CYAN_HEX,
            font=FONT,
            weight=BOLD,
        )
        subtitle = Text(
            "OBE 102 HZ 16-18-83-17W5  |  Bluesky Formation  |  663m TVD",
            font_size=24,
            color=DIM_HEX,
            font=FONT,
        )
        title_group = VGroup(title_big, subtitle).arrange(DOWN, buff=0.5)
        title_group.move_to(UP * 1.0)

        chips = VGroup(
            make_panel(
                "Landing",
                ["819.9 m MD", "663.1 m TVD", "86.3\u00b0 incl."],
                accent=CYAN_HEX,
            ),
            make_panel(
                "Why it matters",
                ["Signal failed on bottom.", "One joint up restored telemetry."],
                accent=AMBER_HEX,
            ),
        ).arrange(RIGHT, buff=0.45, aligned_edge=UP)
        chips.scale(0.92)
        chips.next_to(title_group, DOWN, buff=0.65)

        source = make_text_line(
            "Source-locked to field notes, packet decodes, and the directional survey.",
            font_size=16,
            color=DIM_HEX,
        )
        source.to_edge(DOWN, buff=0.65)

        self.play(FadeIn(title_big, shift=UP * 0.2), run_time=1.2)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in chips], lag_ratio=0.18),
            run_time=1.3,
        )
        self.play(FadeIn(source), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ===========================================================================
# Scene 2: Well Path Reveal (3D, 10s)
# ===========================================================================

class Scene2_WellPathReveal(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_overview_camera()

        path, extension, plane = self.build_world(opacity=0.96, thickness=0.04, plane_opacity=0.11)

        # Single tool marker at the pulled position (the story's answer)
        pulled_point = md_to_3d(WELLFI_POSITION_MD)
        pulled_core, pulled_glow = build_tool_marker(pulled_point, core_color=CYAN_HEX, glow_opacity=0.24)

        # Centered labels
        label_casing = make_text_line(
            "INTERMEDIATE CASING  921m MD",
            font_size=16,
            color=WHITE_HEX,
        )
        label_casing.to_edge(UP, buff=0.6)

        label_bluesky = make_text_line(
            "BLUESKY FORMATION  660.5m TVD",
            font_size=16,
            color=GREEN_HEX,
        )
        label_bluesky.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(label_casing, label_bluesky)
        label_casing.set_opacity(0)
        label_bluesky.set_opacity(0)

        self.play(Create(path), run_time=4.0)
        self.play(
            FadeIn(plane),
            FadeIn(extension),
            label_casing.animate.set_opacity(1),
            run_time=1.2,
        )
        self.play(label_bluesky.animate.set_opacity(1), run_time=0.8)
        self.play(
            FadeIn(pulled_glow), FadeIn(pulled_core),
            run_time=1.0,
        )
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(2.0)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 3: Build Section Close-Up (3D, 8s)
# ===========================================================================

class Scene3_BuildCloseUp(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_overview_camera()

        path, extension, plane = self.build_world(opacity=0.25, thickness=0.032, plane_opacity=0.08)
        self.add(path, extension, plane)

        # Build highlight (370–790m MD)
        build_start_idx = md_to_index(BUILD_START_MD)
        build_end_idx = md_to_index(790.0)
        build_points = WELL_PATH_3D[build_start_idx: build_end_idx + 1]
        build_highlight = VGroup()
        for i in range(len(build_points) - 1):
            seg = Line3D(
                start=build_points[i].tolist(),
                end=build_points[i + 1].tolist(),
                color=GREEN_HEX,
                thickness=0.055,
            )
            build_highlight.add(seg)

        # Run 1 failure zone at 550m MD
        run1_3d = md_to_3d(550.0)
        run1_marker = Sphere(radius=0.10, color=CRIMSON_HEX)
        run1_marker.move_to(run1_3d.tolist())
        run1_marker.set_opacity(0.0)
        self.add(run1_marker)

        # Labels (all centered)
        inc_label = make_text_line("BUILD SECTION  0\u00b0 \u2192 86\u00b0", font_size=20, color=GREEN_HEX)
        inc_label.to_edge(UP, buff=0.6)

        run1_label = make_text_line("RUN 1 FAILURE ZONE", font_size=16, color=CRIMSON_HEX)
        run1_label.to_edge(UP, buff=1.5)

        wellfi_label = make_text_line(
            "WellFi TOOL  819.9m MD  |  663.1m TVD", font_size=18, color=CYAN_HEX
        )
        wellfi_label.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(inc_label, run1_label, wellfi_label)
        inc_label.set_opacity(0)
        run1_label.set_opacity(0)
        wellfi_label.set_opacity(0)

        build_center = md_to_3d(580.0)

        self.play(
            Create(build_highlight),
            inc_label.animate.set_opacity(1),
            run1_marker.animate.set_opacity(0.85),
            run1_label.animate.set_opacity(1),
            run_time=2.5,
        )
        self.move_camera(
            phi=55 * DEGREES,
            theta=-40 * DEGREES,
            frame_center=build_center.tolist(),
            run_time=2.0,
        )
        self.play(
            wellfi_label.animate.set_opacity(1),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 4: Tool Descent with Signal Chart (3D, 12s)
# ===========================================================================

class Scene4_ToolDescent(WellFiBase3DScene):
    """Dual-view: tool descends along well path + live signal chart panel."""
    def construct(self):
        self.setup_bg()
        self.setup_overview_camera()

        path, extension, plane = self.build_world(opacity=0.26, thickness=0.032, plane_opacity=0.08)
        self.add(path, extension, plane)

        # Build descent VMobject path (surface to on-bottom)
        bottom_idx = md_to_index(WELLFI_ON_BOTTOM_MD)
        descent_points = WELL_PATH_3D[: bottom_idx + 1]
        descent_curve = VMobject()
        descent_curve.set_points_as_corners([p.tolist() for p in descent_points])
        descent_curve.set_stroke(opacity=0)

        # Tool sphere
        tool = Sphere(radius=0.10, color=CYAN_HEX)
        tool.move_to(descent_points[0].tolist())
        glow = Sphere(radius=0.20, color=CYAN_HEX)
        glow.move_to(descent_points[0].tolist())
        glow.set_opacity(0.18)
        self.add(glow, tool)

        # Signal chart
        axes = Axes(
            x_range=[0, 850, 100],
            y_range=[-100, -30, 10],
            x_length=4.2,
            y_length=2.6,
            tips=False,
            axis_config={
                "include_numbers": False,
                "stroke_color": DIM_HEX,
                "stroke_opacity": 0.55,
                "stroke_width": 2,
            },
        )
        ax_xlabel = make_text_line("Depth (m)", font_size=13, color=DIM_HEX)
        ax_xlabel.next_to(axes, DOWN, buff=0.20)
        ax_ylabel = make_text_line("Signal (dBV)", font_size=13, color=DIM_HEX)
        ax_ylabel.rotate(PI / 2).next_to(axes, LEFT, buff=0.18)

        graph = axes.plot_line_graph(
            x_values=[e["md"] for e in RIH_EVENTS],
            y_values=[e["signal_dbv"] for e in RIH_EVENTS],
            add_vertex_dots=False,
            line_color=CYAN_HEX,
        )
        noise_line = DashedLine(
            axes.c2p(0, NOISE_FLOOR_DBV),
            axes.c2p(850, NOISE_FLOOR_DBV),
            color=CRIMSON_HEX,
            dash_length=0.09,
        )
        noise_label_txt = make_text_line("Noise floor", font_size=13, color=CRIMSON_HEX)
        noise_label_txt.next_to(noise_line, RIGHT, buff=0.10)

        fluid_line = DashedLine(
            axes.c2p(FLUID_CONTACT_MD, -100),
            axes.c2p(FLUID_CONTACT_MD, -30),
            color=AMBER_HEX,
            dash_length=0.09,
        )
        fluid_label_txt = make_text_line("Fluid", font_size=13, color=AMBER_HEX)
        fluid_label_txt.next_to(fluid_line, UP, buff=0.10)

        # Chart dot tracks descent
        chart_dot = Dot(
            axes.c2p(RIH_EVENTS[0]["md"], RIH_EVENTS[0]["signal_dbv"]),
            radius=0.07,
            color=WHITE_HEX,
        )

        chart_group = VGroup(
            axes, graph, noise_line, noise_label_txt,
            fluid_line, fluid_label_txt, ax_xlabel, ax_ylabel, chart_dot,
        )
        chart_panel = make_panel("Signal profile", [chart_group], accent=CYAN_HEX)
        chart_panel.scale(0.92)
        chart_panel.to_edge(RIGHT, buff=0.45)
        chart_panel.to_edge(UP, buff=0.45)

        # Signal legend
        legend_items = [
            make_text_line("SIGNAL LEGEND", font_size=13, color=DIM_HEX),
            make_text_line("STRONG  \u221237 dBV", font_size=13, color=GREEN_HEX),
            make_text_line("WEAK    \u221255 dBV", font_size=13, color=AMBER_HEX),
            make_text_line("NOISE  \u221295 dBV",  font_size=13, color=CRIMSON_HEX),
        ]
        legend_group = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend_panel = make_panel("", legend_group, accent=DIM_HEX)
        legend_panel.scale(0.88)
        legend_panel.to_edge(LEFT, buff=0.45)
        legend_panel.to_edge(DOWN, buff=0.8)

        # First event panel
        ev0 = RIH_EVENTS[0]
        pressure_str = "above fluid" if ev0["pressure_kpa"] is None else f"{ev0['pressure_kpa']:.0f} kPa"
        event_panel = make_panel(
            f"{ev0['time']} | {ev0['label']}",
            [
                f"MD: {ev0['md']:.1f} m",
                f"Signal: {ev0['signal_dbv']:.0f} dBV",
                f"Pressure: {pressure_str}",
                ev0["summary"],
            ],
            accent=ev0["color"],
        )
        event_panel.scale(0.86)
        event_panel.to_edge(RIGHT, buff=0.45)
        event_panel.to_edge(DOWN, buff=0.6)

        for mob in (chart_panel, legend_panel, event_panel):
            add_fixed_group(self, mob)
            mob.set_opacity(0)

        self.play(
            chart_panel.animate.set_opacity(1),
            legend_panel.animate.set_opacity(1),
            event_panel.animate.set_opacity(1),
            run_time=0.9,
        )
        normalize_panel(chart_panel)
        normalize_panel(legend_panel)
        normalize_panel(event_panel)

        # Animate through each RIH event
        for idx, event in enumerate(RIH_EVENTS):
            target_point = md_to_3d(event["md"])
            target_chart_pos = axes.c2p(event["md"], event["signal_dbv"])

            p_str = "above fluid" if event["pressure_kpa"] is None else f"{event['pressure_kpa']:.0f} kPa"
            next_panel = make_panel(
                f"{event['time']} | {event['label']}",
                [
                    f"MD: {event['md']:.1f} m",
                    f"Signal: {event['signal_dbv']:.0f} dBV",
                    f"Pressure: {p_str}",
                    event["summary"],
                ],
                accent=event["color"],
            )
            next_panel.scale(0.86)
            next_panel.to_edge(RIGHT, buff=0.45)
            next_panel.to_edge(DOWN, buff=0.6)
            add_fixed_group(self, next_panel)
            next_panel.set_opacity(0)

            anims = [
                tool.animate.move_to(target_point.tolist()).set_color(event["color"]),
                glow.animate.move_to(target_point.tolist()).set_color(event["color"]),
                chart_dot.animate.move_to(target_chart_pos),
                event_panel.animate.set_opacity(0),
                next_panel.animate.set_opacity(1),
            ]
            if idx == 2:
                anims.append(Indicate(fluid_line, color=AMBER_HEX, scale_factor=1.05))
            if idx == len(RIH_EVENTS) - 1:
                anims.append(Indicate(noise_line, color=CRIMSON_HEX, scale_factor=1.03))
            self.play(*anims, run_time=1.4)
            normalize_panel(next_panel)
            event_panel = next_panel

        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 5: Signal Failure — On Bottom (3D, 6s)
# ===========================================================================

class Scene5_SignalFailure(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_local_camera(WELLFI_ON_BOTTOM_MD, phi=55, theta=-40)

        path, extension, plane = self.build_world(opacity=0.25, thickness=0.032, plane_opacity=0.06)
        self.add(path, extension, plane)

        bottom_3d = md_to_3d(WELLFI_ON_BOTTOM_MD)
        tool = Sphere(radius=0.14, color=CRIMSON_HEX)
        tool.move_to(bottom_3d.tolist())
        tool.set_opacity(0.5)
        glow = Sphere(radius=0.28, color=CRIMSON_HEX)
        glow.move_to(bottom_3d.tolist())
        glow.set_opacity(0.15)
        self.add(glow, tool)

        status_label = make_text_line(
            "SIGNAL BELOW NOISE FLOOR", font_size=22, color=CRIMSON_HEX
        )
        status_label.to_edge(UP, buff=0.6)

        crc_label = make_text_line(
            "33% CRC PASS RATE  |  84-MINUTE BLACKOUT", font_size=18, color=DIM_HEX
        )
        crc_label.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(status_label, crc_label)
        status_label.set_opacity(0)
        crc_label.set_opacity(0)

        self.play(status_label.animate.set_opacity(1), run_time=1.0)

        # Tool pulses dim 3 times
        for _ in range(3):
            self.play(tool.animate.set_opacity(0.2), glow.animate.set_opacity(0.06), run_time=0.5)
            self.play(tool.animate.set_opacity(0.6), glow.animate.set_opacity(0.18), run_time=0.5)

        self.play(crc_label.animate.set_opacity(1), run_time=0.8)
        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 6: Pulled 1 Joint (3D, 8s)
# ===========================================================================

class Scene6_PulledJoint(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_local_camera(WELLFI_ON_BOTTOM_MD, phi=55, theta=-40)

        path, extension, plane = self.build_world(opacity=0.25, thickness=0.032, plane_opacity=0.06)
        self.add(path, extension, plane)

        bottom_3d = md_to_3d(WELLFI_ON_BOTTOM_MD)
        pulled_3d = md_to_3d(WELLFI_POSITION_MD)

        tool = Sphere(radius=0.14, color=CRIMSON_HEX)
        tool.move_to(bottom_3d.tolist())
        tool.set_opacity(0.5)

        glow = Sphere(radius=0.26, color=CRIMSON_HEX)
        glow.move_to(bottom_3d.tolist())
        glow.set_opacity(0.15)

        shift_line = Line3D(
            start=bottom_3d.tolist(),
            end=pulled_3d.tolist(),
            color=AMBER_HEX,
            thickness=0.045,
        )
        shift_line.set_opacity(0.0)
        self.add(shift_line, glow, tool)

        # Before/After panels (centered at top/bottom)
        before_panel = make_panel(
            "Before pull",
            ["Landing: 832.3 m", "Signal: \u221296 to \u2212100 dBV", "CRC: 33%"],
            accent=CRIMSON_HEX,
        )
        before_panel.scale(0.82)
        before_panel.to_edge(UP, buff=0.6)

        after_panel = make_panel(
            "After pull",
            ["Landing: 819.9 m", "CRC: 77%"],
            accent=CYAN_HEX,
        )
        after_panel.scale(0.82)
        after_panel.to_edge(UP, buff=0.6)

        result_panel = make_panel(
            "Result",
            ["84-min blackout ended", "Telemetry resumed in-zone"],
            accent=GREEN_HEX,
        )
        result_panel.scale(0.88)
        result_panel.to_edge(DOWN, buff=0.6)

        for mob in (before_panel, after_panel, result_panel):
            add_fixed_group(self, mob)
            mob.set_opacity(0)

        self.play(before_panel.animate.set_opacity(1), run_time=0.9)
        normalize_panel(before_panel)
        self.wait(0.5)

        # Tool moves up
        self.play(
            shift_line.animate.set_opacity(0.90),
            tool.animate.move_to(pulled_3d.tolist()).set_color(CYAN_HEX).set_opacity(0.92),
            glow.animate.move_to(pulled_3d.tolist()).set_color(CYAN_HEX).set_opacity(0.22),
            before_panel.animate.set_opacity(0),
            after_panel.animate.set_opacity(1),
            run_time=1.8,
        )
        normalize_panel(after_panel)
        self.play(result_panel.animate.set_opacity(1), run_time=0.7)
        normalize_panel(result_panel)
        self.move_camera(phi=62 * DEGREES, theta=-46 * DEGREES, run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 7: Pump Start (3D, 8s)
# ===========================================================================

class Scene7_PumpStart(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_local_camera(WELLFI_POSITION_MD, phi=55, theta=-40)

        path, extension, plane = self.build_world(opacity=0.20, thickness=0.032, plane_opacity=0.06)
        self.add(path, extension, plane)

        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        tool, tool_glow = build_tool_marker(wellfi_3d, core_color=CYAN_HEX, glow_opacity=0.20)
        self.add(tool_glow, tool)

        # Centered labels
        pump_label = make_text_line("PUMP START  |  Apr 2, 17:38", font_size=22, color=AMBER_HEX)
        pump_label.to_edge(UP, buff=0.6)

        marginal_label = make_text_line("MARGINAL SIGNAL ZONE  |  819.9m MD", font_size=16, color=CRIMSON_HEX)
        marginal_label.to_edge(DOWN, buff=1.6)

        # Pressure text phases
        p_initial = make_text_line("P: 2075 kPa", font_size=22, color=CYAN_HEX)
        p_initial.to_edge(DOWN, buff=0.6)

        p_cold = make_text_line("COLD SLUG  |  P: 1520 kPa", font_size=22, color=AMBER_HEX)
        p_cold.to_edge(DOWN, buff=0.6)

        p_steady = make_text_line("STEADY STATE  |  P: 2069 kPa", font_size=22, color=CYAN_HEX)
        p_steady.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(pump_label, marginal_label, p_initial, p_cold, p_steady)
        pump_label.set_opacity(0)
        marginal_label.set_opacity(0)
        p_initial.set_opacity(0)
        p_cold.set_opacity(0)
        p_steady.set_opacity(0)

        self.play(
            pump_label.animate.set_opacity(1),
            marginal_label.animate.set_opacity(1),
            run_time=0.8,
        )
        self.play(p_initial.animate.set_opacity(1), run_time=0.8)
        self.wait(1.0)

        # Cold slug
        self.play(
            p_initial.animate.set_opacity(0),
            p_cold.animate.set_opacity(1),
            tool.animate.set_color(AMBER_HEX),
            tool_glow.animate.set_color(AMBER_HEX),
            run_time=1.0,
        )
        self.wait(1.0)

        # Steady state
        self.play(
            p_cold.animate.set_opacity(0),
            p_steady.animate.set_opacity(1),
            tool.animate.set_color(CYAN_HEX),
            tool_glow.animate.set_color(CYAN_HEX),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 8: Overnight (2D, 6s)
# ===========================================================================

class Scene8_Overnight(Scene):
    def construct(self):
        self.camera.background_color = BG_HEX

        night_text = Text("OVERNIGHT", font_size=48, color=DIM_HEX, font=FONT)

        p_before = Text("P: 2069 kPa", font_size=28, color=CYAN_HEX, font=FONT)
        arrow = Text("\u25bc", font_size=36, color=AMBER_HEX, font=FONT)
        p_after = Text("P: 1951 kPa", font_size=28, color=AMBER_HEX, font=FONT)
        delta = Text("\u2212118 kPa OVERNIGHT DRAWDOWN", font_size=18, color=DIM_HEX, font=FONT)

        stack = VGroup(night_text, p_before, arrow, p_after, delta).arrange(DOWN, buff=0.4)
        stack.move_to(ORIGIN)

        morning = Text("Apr 3, 10:56 \u2014 MORNING RESUME", font_size=20, color=GREEN_HEX, font=FONT)
        morning.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(night_text), run_time=0.8)
        self.play(FadeIn(p_before), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(arrow), FadeIn(p_after), run_time=0.9)
        self.play(FadeIn(delta), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(morning), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ===========================================================================
# Scene 9: Gas Kick (3D, 10s)
# ===========================================================================

class Scene9_GasKick(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_local_camera(WELLFI_POSITION_MD, phi=55, theta=-40)

        path, extension, plane = self.build_world(opacity=0.22, thickness=0.032, plane_opacity=0.06)
        self.add(path, extension, plane)

        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        tool, glow = build_tool_marker(wellfi_3d, core_color=CYAN_HEX, glow_opacity=0.20)
        self.add(glow, tool)

        # Phase labels — all to_edge(UP)
        normal_label = make_text_line("Apr 3, 11:02  |  P: 1934 kPa  |  NORMAL", font_size=18, color=CYAN_HEX)
        normal_label.to_edge(UP, buff=0.6)

        kick_label = make_text_line("11:17  |  PUMP SLOWS DUE TO GAS", font_size=20, color=AMBER_HEX)
        kick_label.to_edge(UP, buff=0.6)

        crc_label = make_text_line("11:52  |  16865 kPa  |  CRC FAIL", font_size=24, color=CRIMSON_HEX)
        crc_label.to_edge(UP, buff=0.6)

        recovery_label = make_text_line("11:59  |  P: 1934 kPa  |  RECOVERED", font_size=20, color=GREEN_HEX)
        recovery_label.to_edge(UP, buff=0.6)

        note = make_text_line("GARBLED PACKET CLASSIFIED  |  7-MIN RECOVERY", font_size=16, color=DIM_HEX)
        note.to_edge(DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(normal_label, kick_label, crc_label, recovery_label, note)
        for m in (normal_label, kick_label, crc_label, recovery_label, note):
            m.set_opacity(0)

        # Phase 1 — normal
        self.play(normal_label.animate.set_opacity(1), run_time=0.8)
        self.wait(1.2)

        # Phase 2 — gas kick, pump slows
        gas_bubbles = VGroup()
        for i in range(6):
            bubble = Sphere(radius=0.04 + i * 0.007, color=AMBER_HEX if i < 3 else CRIMSON_HEX)
            offset = np.array([0.05 * (i % 3 - 1), 0.04 * ((i + 1) % 3 - 1), 0.07 * i])
            bubble.move_to((wellfi_3d + offset).tolist())
            bubble.set_opacity(0.48)
            gas_bubbles.add(bubble)

        self.play(
            normal_label.animate.set_opacity(0),
            kick_label.animate.set_opacity(1),
            tool.animate.set_color(AMBER_HEX),
            glow.animate.set_color(AMBER_HEX).set_opacity(0.28),
            FadeIn(gas_bubbles),
            run_time=1.0,
        )
        self.play(gas_bubbles.animate.shift([0, 0, 1.5]), run_time=1.4)
        self.play(FadeOut(gas_bubbles), run_time=0.3)

        # Phase 3 — CRC fail
        self.play(
            kick_label.animate.set_opacity(0),
            crc_label.animate.set_opacity(1),
            tool.animate.set_color(CRIMSON_HEX).set_opacity(0.95),
            glow.animate.set_color(CRIMSON_HEX).set_opacity(0.45),
            run_time=0.8,
        )
        # Flash
        self.play(tool.animate.scale(1.15), glow.animate.scale(1.18), run_time=0.25)
        self.play(tool.animate.scale(1 / 1.15), glow.animate.scale(1 / 1.18), run_time=0.25)
        self.wait(0.5)

        # Phase 4 — recovery
        self.play(
            crc_label.animate.set_opacity(0),
            recovery_label.animate.set_opacity(1),
            tool.animate.set_color(GREEN_HEX).set_opacity(0.92),
            glow.animate.set_color(GREEN_HEX).set_opacity(0.24),
            run_time=1.2,
        )
        self.play(note.animate.set_opacity(1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 10: Late Drawdown + Extended Data (2D, 6s)
# ===========================================================================

class Scene10_LateDrawdown(Scene):
    def construct(self):
        self.camera.background_color = BG_HEX

        title = Text("CONTINUOUS MONITORING", font_size=36, color=CYAN_HEX, font=FONT)
        title.to_edge(UP, buff=1.0)

        readings = [
            ("Apr 3 11:02", "1934 kPa", CYAN_HEX),
            ("Apr 3 16:50", "1810 kPa", AMBER_HEX),
            ("Apr 3 23:17", "1963 kPa", GREEN_HEX),
            ("Apr 4 00:29", "1956 kPa", GREEN_HEX),
        ]

        reading_group = VGroup()
        for time_str, pressure, color in readings:
            row = VGroup(
                Text(time_str, font_size=22, color=DIM_HEX, font=FONT),
                Text(pressure, font_size=26, color=color, font=FONT),
            )
            row.arrange(RIGHT, buff=0.8)
            reading_group.add(row)

        reading_group.arrange(DOWN, buff=0.4)
        reading_group.next_to(title, DOWN, buff=0.8)

        note = Text(
            "TOOL STILL TRANSMITTING \u2014 8 DAYS AND COUNTING",
            font_size=18, color=GREEN_HEX, font=FONT,
        )
        note.to_edge(DOWN, buff=0.8)

        self.play(Write(title), run_time=1.0)
        for row in reading_group:
            self.play(FadeIn(row), run_time=0.55)
            self.wait(0.25)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)


# ===========================================================================
# Scene 11: Full Well Pullback (3D, 8s)
# ===========================================================================

class Scene11_Pullback(WellFiBase3DScene):
    def construct(self):
        self.setup_bg()
        self.setup_overview_camera()

        path, extension, plane = self.build_world(opacity=1.0, thickness=0.040, plane_opacity=0.10)

        wellfi_3d = md_to_3d(WELLFI_POSITION_MD)
        tool, tool_glow = build_tool_marker(wellfi_3d, core_color=CYAN_HEX, glow_opacity=0.28)
        self.add(path, extension, plane, tool_glow, tool)

        # 4 metric cards in CORNERS (intentional — frames the 3D well path)
        ul_card = make_metric_card("Peak Signal", "\u221237 dBV", GREEN_HEX, "161m MD in casing")
        ur_card = make_metric_card("Late Pressure", "1810 kPa", CYAN_HEX, "Apr 3 16:50")
        dl_card = make_metric_card("Best CRC", "100%", GREEN_HEX, "7 hrs on Apr 3")
        dr_card = make_metric_card("Gas Kick Recovery", "7 min", CRIMSON_HEX, "11:52 \u2192 11:59")

        ul_card.scale(0.80)
        ur_card.scale(0.80)
        dl_card.scale(0.80)
        dr_card.scale(0.80)

        ul_card.to_corner(UL, buff=0.55)
        ur_card.to_corner(UR, buff=0.55)
        dl_card.to_corner(DL, buff=0.55)
        dr_card.to_corner(DR, buff=0.55)

        for mob in (ul_card, ur_card, dl_card, dr_card):
            add_fixed_group(self, mob)
            mob.set_opacity(0)

        self.begin_ambient_camera_rotation(rate=0.08)

        for card in (ul_card, ur_card, dl_card, dr_card):
            self.play(card.animate.set_opacity(1), run_time=0.8)
            normalize_panel(card)
            self.wait(0.2)

        self.wait(2.0)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)


# ===========================================================================
# Scene 12: Payoff (2D, 5s)
# ===========================================================================

class Scene12_Payoff(Scene):
    def construct(self):
        self.camera.background_color = BG_HEX

        statement = Text(
            "Surface modifications turned\nmarginal signal into reliable telemetry.",
            font_size=36,
            color=WHITE_HEX,
            font=FONT,
            line_spacing=1.4,
        )
        statement.move_to(UP * 0.6)

        brand = Text("WellFi", font_size=48, color=CYAN_HEX, font=FONT, weight=BOLD)
        brand.next_to(statement, DOWN, buff=0.8)

        source = Text(
            "Source-locked to field data, packet logs, and directional survey",
            font_size=16,
            color=DIM_HEX,
            font=FONT,
        )
        source.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(statement), run_time=2.0)
        self.wait(0.5)
        self.play(FadeIn(brand), run_time=1.0)
        self.play(FadeIn(source), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
