#!/usr/bin/env python3
"""
WellFi Collector Sub - RT4 Explainer Visual

Two-panel design, each self-contained for individual dissemination:
  Panel 1 (Main): The mechanism - annular cross-section with 4-lip sub,
                  showing Stage 1 shear coalescence + Stage 2 gravity
                  stratification. Explains HOW it works.
  Panel 2 (Evidence): Viscosity correction + firmware alternative test.
                      Explains WHY we believe it.

Design philosophy: Subterranean Signal (dark background, data-native colors)
Audience: engineers reviewing the design before bench-validation gate.

Every number on the canvas is traceable to:
  - Element lab oil analysis (viscosity, density)
  - petro-roundtable/calculations/collector_sub_simulation.py
  - petro-roundtable/calculations/firmware_filter_test.py
  - RT4 deliverable
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Circle, Wedge
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# ----- Subterranean Signal palette -----
BG1     = "#06090f"
BG2     = "#0c1220"
PANEL   = "#0f1825"
BORDER  = "#1e2a3a"
TEXT    = "#e6edf3"
MUTED   = "#8b95a8"
WHITE   = "#f0f4f8"
CYAN    = "#00D4FF"   # instrument / data
AMBER   = "#F5A623"   # engineered object (sub, lip)
GREEN   = "#2dd4a8"   # validation / formation / clean
RED     = "#ef4444"   # gas / alert / fail
GAS     = "#ff6b6b"
OIL     = "#d4a847"
STEEL   = "#6e7681"
GRID    = "#141e30"

# ----- Figure -----
fig = plt.figure(figsize=(28, 14), facecolor=BG1, dpi=150)

# Gradient background
ax_bg = fig.add_axes([0, 0, 1, 1], zorder=-1)
ax_bg.axis("off")
grad = np.linspace(0, 1, 256).reshape(-1, 1)
grad_img = np.hstack([grad] * 10)
ax_bg.imshow(
    grad_img, aspect="auto", extent=[0, 1, 0, 1],
    cmap=LinearSegmentedColormap.from_list("bg", [BG1, BG2]),
    origin="lower"
)

# ----- Title bar -----
fig.text(
    0.04, 0.955, "WellFi Collector Sub",
    color=WHITE, fontsize=32, fontweight="bold", family="Segoe UI",
    path_effects=[pe.withStroke(linewidth=1, foreground="#006680")]
)
fig.text(
    0.04, 0.928,
    "RT4 Revision (2026-04-16)  -  Viscosity-corrected design  -  Hardware case validated vs firmware alternative",
    color=MUTED, fontsize=12, family="Segoe UI"
)
fig.text(
    0.04, 0.908,
    "OBE 102 HZ 16-18-83-17W5  |  Bluesky Formation  |  86 deg inclination  |  190 bbl/d  |  8,320 cP dead / 4,660 cP live",
    color=CYAN, fontsize=10, family="Consolas", fontweight="bold"
)

# ===================================================================
# PANEL 1 - MECHANISM (LEFT, LARGER)
# ===================================================================
ax1 = fig.add_axes([0.035, 0.07, 0.56, 0.81])
ax1.set_facecolor(PANEL)
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)
ax1.axis("off")

# Panel border
ax1.add_patch(FancyBboxPatch(
    (0, 0), 100, 100, boxstyle="round,pad=0.5,rounding_size=1.5",
    linewidth=1.2, edgecolor=BORDER, facecolor=PANEL, zorder=0
))

ax1.text(3, 95, "MECHANISM", color=CYAN, fontsize=14, fontweight="bold", family="Segoe UI")
ax1.text(3, 91,
         "Asymmetric low-side lips force staged shear coalescence then gravity stratification.",
         color=MUTED, fontsize=10, family="Segoe UI")

# ---------- Side-view of the sub ----------
# Geometry: horizontal cross-section of the annular space at 86 deg
# Casing ID ~196.9 mm, tubing OD ~73 mm, annular gap ~62 mm
# We'll show a 36" sub with 4 lips

# Background well annulus
cas_top = 67
cas_bot = 28
tub_top = 52
tub_bot = 40

# Casing walls
ax1.plot([4, 96], [cas_top, cas_top], color=STEEL, linewidth=2.5, zorder=3)
ax1.plot([4, 96], [cas_bot, cas_bot], color=STEEL, linewidth=2.5, zorder=3)

ax1.text(50, cas_top + 1.5, "CASING 8-5/8 in ID (HIGH SIDE - gas escape path)",
         color=STEEL, fontsize=8, ha="center", family="Consolas")
ax1.text(50, cas_bot - 3, "CASING (LOW SIDE - liquid layer + eccentric tubing)",
         color=STEEL, fontsize=8, ha="center", family="Consolas")

# Gravity indicator
ax1.add_patch(FancyArrowPatch(
    (2, 60), (2, 32), arrowstyle="-|>", mutation_scale=14,
    color=MUTED, linewidth=1.5
))
ax1.text(1.3, 64, "g", color=MUTED, fontsize=11, fontweight="bold", ha="center")
ax1.text(3.2, 60, "sin(86) = 0.998", color=MUTED, fontsize=7, family="Consolas")
ax1.text(3.2, 57, "14x axial g", color=MUTED, fontsize=7, family="Consolas")

# Tubing body (with 4 lips)
ax1.add_patch(Rectangle((7, tub_bot), 86, tub_top - tub_bot, facecolor="#1c2333",
              edgecolor=STEEL, linewidth=2, zorder=3))
ax1.text(9, (tub_top + tub_bot)/2, "TUBING 2-7/8 in OD  (rod + couplings pass full drift)",
         color=STEEL, fontsize=7.5, ha="left", va="center", family="Consolas")

# Four asymmetric low-side lips (36" sub, 7.2" spacing)
lip_positions = [24, 42, 60, 78]
for i, lx in enumerate(lip_positions):
    # Upstream face of lip (creates shear zone above)
    # Scooped underside (sheds sand)
    crest_w = 6.5
    crest_h = 5.5
    scoop_angle = 18  # deg downslope on underside
    lip = Polygon([
        (lx - crest_w/2, tub_bot),          # upstream top
        (lx - crest_w/2 - 1.2, tub_bot - crest_h),  # upstream bottom (sharp)
        (lx + crest_w/2 + 3.5, tub_bot - 1.8),      # downstream scooped
        (lx + crest_w/2, tub_bot),           # downstream top
    ], closed=True, facecolor=AMBER, edgecolor="#c48418",
    linewidth=1.5, zorder=5)
    ax1.add_patch(lip)

    # Stage label
    ax1.text(lx, tub_bot - crest_h - 3, f"LIP {i+1}",
             color=AMBER, fontsize=9, fontweight="bold", ha="center", family="Consolas")

# --- Bubble evolution through the stages ---
np.random.seed(42)

# Zone 1: Before sub - dispersed micro-bubbles everywhere
for _ in range(22):
    bx = np.random.uniform(9, 22)
    by = np.random.uniform(cas_bot + 2, tub_bot - 1.5) if np.random.random() > 0.5 else np.random.uniform(tub_top + 1.5, cas_top - 2)
    br = np.random.uniform(0.35, 0.7)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.55, zorder=2))

# Zone 2: After lip 1 - some coalescence started (larger bubbles appearing)
for _ in range(12):
    bx = np.random.uniform(27, 40)
    by = np.random.uniform(cas_bot + 2, tub_bot - 1.5) if np.random.random() > 0.3 else np.random.uniform(tub_top + 2, cas_top - 2)
    br = np.random.uniform(0.3, 0.6)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.4, zorder=2))
# Some larger coalesced bubbles rising to high side
for _ in range(4):
    bx = np.random.uniform(29, 40)
    by = np.random.uniform(tub_top + 3, cas_top - 3)
    br = np.random.uniform(1.0, 1.5)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.7, zorder=2))

# Zone 3: After lip 2 - fewer small bubbles, more large on high side
for _ in range(8):
    bx = np.random.uniform(45, 58)
    by = np.random.uniform(cas_bot + 2, tub_bot - 1.5)
    br = np.random.uniform(0.25, 0.5)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.35, zorder=2))
for _ in range(7):
    bx = np.random.uniform(45, 58)
    by = np.random.uniform(tub_top + 3, cas_top - 3)
    br = np.random.uniform(1.2, 1.9)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.75, zorder=2))

# Zone 4: After lip 3 - mostly clean low-side, heavy gas on high side
for _ in range(4):
    bx = np.random.uniform(63, 76)
    by = np.random.uniform(cas_bot + 2, tub_bot - 1.5)
    br = np.random.uniform(0.2, 0.4)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.25, zorder=2))
for _ in range(9):
    bx = np.random.uniform(63, 76)
    by = np.random.uniform(tub_top + 3, cas_top - 3)
    br = np.random.uniform(1.3, 2.1)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.8, zorder=2))

# Zone 5: After lip 4 - cleaner liquid to PCP, gas stream on high side
for _ in range(11):
    bx = np.random.uniform(81, 92)
    by = np.random.uniform(tub_top + 3, cas_top - 3)
    br = np.random.uniform(1.4, 2.3)
    ax1.add_patch(Circle((bx, by), br, facecolor=GAS, edgecolor="none", alpha=0.82, zorder=2))

# Flow direction arrow (upstream)
ax1.add_patch(FancyArrowPatch(
    (6, (tub_top + tub_bot)/2), (15, (tub_top + tub_bot)/2),
    arrowstyle="-|>", mutation_scale=16, color=CYAN, linewidth=2.2, zorder=6
))
ax1.text(10.5, (tub_top + tub_bot)/2 + 2, "FLOW  190 bbl/d",
         color=CYAN, fontsize=8.5, ha="center", family="Consolas", fontweight="bold")

# Rising-gas arrows between lips (Stage 2 gravity stratification)
for gx in [33, 51, 69]:
    ax1.add_patch(FancyArrowPatch(
        (gx, tub_top + 1.5), (gx, cas_top - 2.5),
        arrowstyle="-|>", mutation_scale=9, color=GAS, linewidth=1.2, alpha=0.65, zorder=4
    ))

# PCP label at exit
ax1.add_patch(FancyBboxPatch(
    (93, tub_bot - 1), 5, tub_top - tub_bot + 2,
    boxstyle="round,pad=0.2,rounding_size=0.8",
    linewidth=1.5, edgecolor=GREEN, facecolor="#0d1e1a", zorder=6
))
ax1.text(95.5, (tub_top + tub_bot)/2, "PCP",
         color=GREEN, fontsize=9, fontweight="bold", ha="center", va="center", family="Consolas")

# ---------- Stage labels below sub ----------
ax1.text(16, 21, "INLET\nfoamy oil\nentrained gas",
         color=MUTED, fontsize=8, ha="center", family="Segoe UI")
ax1.text(33, 21, "STAGE 1\nshear coalescence\n(at lip)",
         color=AMBER, fontsize=8, ha="center", family="Segoe UI", fontweight="bold")
ax1.text(51, 21, "STAGE 2\ngravity stratification\n(between lips, 5 s)",
         color=GREEN, fontsize=8, ha="center", family="Segoe UI", fontweight="bold")
ax1.text(69, 21, "REPEAT\nprogressive\ngas removal",
         color=CYAN, fontsize=8, ha="center", family="Segoe UI", fontweight="bold")
ax1.text(87, 21, "OUTLET\ncleaner liquid\nto PCP intake",
         color=GREEN, fontsize=8, ha="center", family="Segoe UI")

# ---------- Key numbers callout ----------
callout = FancyBboxPatch(
    (4, 79), 92, 8.5,
    boxstyle="round,pad=0.3,rounding_size=1",
    linewidth=1, edgecolor=CYAN, facecolor="#071320", alpha=0.95, zorder=7
)
ax1.add_patch(callout)

ax1.text(7, 84.5, "THE CRITICAL RT4 FINDING",
         color=CYAN, fontsize=10, fontweight="bold", family="Segoe UI")
ax1.text(7, 81.5,
         "At 80,000 cP (old assumption):  migration 52 s vs transit 11 s  ->  gravity LOSES",
         color=MUTED, fontsize=9, family="Consolas")
ax1.text(7, 79.3,
         "At 8,320 cP (lab measured):       migration  5 s vs transit 11 s  ->  gravity WINS",
         color=GREEN, fontsize=9.5, fontweight="bold", family="Consolas")

# ---------- Design spec at bottom ----------
spec_bg = FancyBboxPatch(
    (4, 5), 92, 11,
    boxstyle="round,pad=0.3,rounding_size=1",
    linewidth=1, edgecolor=AMBER, facecolor="#150e04", alpha=0.95, zorder=7
)
ax1.add_patch(spec_bg)

ax1.text(7, 13, "DESIGN (RT4 revision)", color=AMBER, fontsize=10,
         fontweight="bold", family="Segoe UI")

spec_items = [
    ("Length",        "36 in",            "was 24 in"),
    ("Lips",          "4",                "was 3"),
    ("Restriction",   "28% area",         "was 30%"),
    ("Profile",       "Asymmetric + scooped",  "new"),
    ("Sand drain",    "4x 1/4 in ports",  "new"),
    ("Bore",          "Full drift",       "unchanged"),
    ("Mechanism",     "Shear + gravity",  "was shear only"),
    ("Retrievable",   "Standard fishing", "confirmed"),
]

for i, (label, value, delta) in enumerate(spec_items):
    col = i % 4
    row = i // 4
    x = 9 + col * 22
    y = 9.5 - row * 3
    ax1.text(x, y,     label,  color=MUTED, fontsize=7.5, family="Segoe UI")
    ax1.text(x, y - 1.5, value,  color=WHITE, fontsize=8.5, family="Consolas", fontweight="bold")
    ax1.text(x + 12, y - 1.5, delta, color=AMBER, fontsize=7, family="Consolas", alpha=0.7)


# ===================================================================
# PANEL 2 - EVIDENCE (TOP RIGHT - viscosity correction)
# ===================================================================
ax2 = fig.add_axes([0.61, 0.49, 0.36, 0.39])
ax2.set_facecolor(PANEL)
for spine in ax2.spines.values():
    spine.set_color(BORDER)
ax2.tick_params(colors=MUTED, labelsize=8)
ax2.xaxis.label.set_color(MUTED)
ax2.yaxis.label.set_color(MUTED)

ax2.text(0.02, 1.06, "WHY THIS NOW: VISCOSITY CORRECTION",
         color=CYAN, fontsize=13, fontweight="bold",
         transform=ax2.transAxes, family="Segoe UI")
ax2.text(0.02, 1.02,
         "Element lab (sales oil) vs CSEG regional average vs simulation implications",
         color=MUTED, fontsize=9,
         transform=ax2.transAxes, family="Segoe UI")

# Three viscosity cases as bar chart
cases = ["80,000 cP\n(RT1-3 assumed)", "20,000 cP\n(conservative)", "8,320 cP\n(lab measured)"]
live_visc = [44800, 11200, 4660]
reynolds  = [0.036, 0.146, 0.351]
migration_time = [52, 13, 5]  # s
transit_time_ref = 11.4  # s

x = np.arange(len(cases))
width = 0.35

# Migration time (log scale)
ax2.bar(x - width/2, migration_time, width, label="Gas migration time (s)",
        color=RED, alpha=0.75, edgecolor=RED, linewidth=1)
ax2.bar(x + width/2, [transit_time_ref]*3, width, label="Lip-to-lip transit (s)",
        color=CYAN, alpha=0.5, edgecolor=CYAN, linewidth=1)

for i, (m, r) in enumerate(zip(migration_time, reynolds)):
    ax2.text(i - width/2, m + 2, f"{m} s", ha="center", fontsize=8.5,
             color=RED, fontweight="bold", family="Consolas")
    ax2.text(i + width/2, transit_time_ref + 2, f"{transit_time_ref} s", ha="center",
             fontsize=8.5, color=CYAN, fontweight="bold", family="Consolas")

# Verdict arrows
for i, (m, verdict) in enumerate(zip(migration_time, ["g LOSES", "MARGINAL", "g WINS"])):
    color = RED if m > transit_time_ref * 1.5 else (AMBER if m > transit_time_ref else GREEN)
    ax2.text(i, -9, verdict, ha="center", fontsize=9, color=color,
             fontweight="bold", family="Consolas")

ax2.set_xticks(x)
ax2.set_xticklabels(cases, fontsize=8.5, color=TEXT)
ax2.set_ylabel("Time (seconds)", color=MUTED, fontsize=9)
ax2.set_title("")
ax2.set_ylim(0, 65)
ax2.grid(True, alpha=0.12, color=MUTED, axis="y")
ax2.legend(loc="upper right", fontsize=8, facecolor=PANEL, edgecolor=BORDER,
           labelcolor=TEXT, framealpha=0.9)

# Annotation
ax2.text(0.02, 0.95,
         "Lab oil = 8,320 cP (ASTM D4052/D341 at 20 C).  Live foamy = 4,660 cP (SPE-136665).\n"
         "Old 80,000 cP was CSEG regional TOP-OF-RESERVOIR average - NOT representative of this well.",
         transform=ax2.transAxes, fontsize=8, color=MUTED, family="Segoe UI",
         verticalalignment="top",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#071320", edgecolor=BORDER, alpha=0.9))


# ===================================================================
# PANEL 3 - FIRMWARE TEST (BOTTOM RIGHT)
# ===================================================================
ax3 = fig.add_axes([0.61, 0.07, 0.36, 0.35])
ax3.set_facecolor(PANEL)
for spine in ax3.spines.values():
    spine.set_color(BORDER)
ax3.tick_params(colors=MUTED, labelsize=8)

ax3.text(0.02, 1.07, "CAN FIRMWARE REPLACE THIS?",
         color=CYAN, fontsize=13, fontweight="bold",
         transform=ax3.transAxes, family="Segoe UI")
ax3.text(0.02, 1.02,
         "Adversarial gate check: firmware recovered only 19% of the hardware gain (real Run 3 data)",
         color=MUTED, fontsize=9,
         transform=ax3.transAxes, family="Segoe UI")

# Stacked bars: Apr 2 baseline (66.1) -> firmware best (71.4) -> Apr 3 goal (93.5)
conditions = ["Apr 2 raw\n(baseline)", "Firmware\nfilter best", "Apr 3 raw\n(joint pull)"]
values = [66.1, 71.4, 93.5]
colors = [RED, AMBER, GREEN]

bars = ax3.bar(conditions, values, color=colors, alpha=0.82, edgecolor=colors, linewidth=1.5, width=0.6)

# Labels on bars
for bar, v in zip(bars, values):
    ax3.text(bar.get_x() + bar.get_width()/2, v + 1.5, f"{v:.1f}%",
             ha="center", fontsize=11, color=WHITE, fontweight="bold", family="Consolas")

# Gap arrows
ax3.annotate("", xy=(1, 71.4), xytext=(0, 66.1),
             arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.5))
ax3.text(0.5, 61, "+5.4 pp\nfirmware", ha="center", fontsize=8,
         color=AMBER, family="Consolas")

ax3.annotate("", xy=(2, 93.5), xytext=(0, 66.1),
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
ax3.text(1, 85, "+27.5 pp\nhardware target", ha="center", fontsize=8,
         color=GREEN, family="Consolas", fontweight="bold")

ax3.set_ylabel("WellFi payload success (%)", color=MUTED, fontsize=9)
ax3.set_ylim(0, 105)
ax3.grid(True, alpha=0.12, color=MUTED, axis="y")

# Verdict box
ax3.text(0.02, 0.94,
         "VERDICT: 71.4 << 90.  Firmware cannot substitute for the geometric change.\n"
         "Apr 2 failure was continuous bad EM path - not discrete gas events.  Only a physical\n"
         "flow restriction fragments slugs and improves the signal environment.",
         transform=ax3.transAxes, fontsize=8, color=GREEN, family="Segoe UI",
         verticalalignment="top", fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.35", facecolor="#0d1e1a", edgecolor=GREEN, alpha=0.95))


# ----- Footer -----
fig.text(
    0.04, 0.025,
    "Sources:  Element Oil Analysis 3132385 (viscosity, density)  |  "
    "collector_sub_simulation.py v2 (mechanism numbers)  |  "
    "firmware_filter_test.py (89 packets from EMGRx SN 2602315)  |  "
    "RT4 deliverable 2026-04-16-wellfi-collector-sub-viscosity-correction.md",
    color=MUTED, fontsize=7, family="Consolas", alpha=0.7
)

fig.text(
    0.97, 0.025,
    "STATUS: Ready for bench validation gate (6-8 weeks).  NOT ready for fab.",
    color=AMBER, fontsize=8.5, ha="right", family="Segoe UI", fontweight="bold", alpha=0.9
)

out = r"C:\Users\kyle\MPS\Obsidian\petro-roundtable\docs\visuals\wellfi-collector-sub-rt4.png"
fig.savefig(out, bbox_inches="tight", facecolor=BG1, dpi=180)
plt.close(fig)
print(out)
