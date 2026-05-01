#!/usr/bin/env python3
"""Generate a simple engineering explainer visual for the WellFi Collector Sub."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge


BG = "#f6f8fb"
PANEL = "#ffffff"
TEXT = "#162033"
MUTED = "#5f6b7a"
LINE = "#cfd7e3"
BLUE = "#0f6fff"
TEAL = "#0aa3a3"
GREEN = "#14804a"
AMBER = "#b26a00"
RED = "#c0392b"
GAS = "#d1495b"
LIQ = "#d39b2c"
STEEL = "#6b7280"


def panel(fig, rect, title, subtitle=None):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    bg = FancyBboxPatch(
        (0, 0),
        100,
        100,
        boxstyle="round,pad=0.8,rounding_size=4",
        linewidth=1.2,
        edgecolor=LINE,
        facecolor=PANEL,
    )
    ax.add_patch(bg)
    ax.text(4, 94, title, fontsize=17, fontweight="bold", color=TEXT)
    if subtitle:
        ax.text(4, 88, subtitle, fontsize=9.5, color=MUTED)
    return ax


def label(ax, x, y, text, color=TEXT, size=10, weight="normal", ha="left", va="center"):
    ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, ha=ha, va=va)


def arrow(ax, start, end, color=TEXT, lw=1.8, style="-|>", mutation=12, alpha=1.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=mutation,
            linewidth=lw,
            color=color,
            alpha=alpha,
        )
    )


fig = plt.figure(figsize=(16, 9), dpi=180, facecolor=BG)

fig.text(0.04, 0.955, "WellFi Collector Sub", fontsize=26, fontweight="bold", color=TEXT)
fig.text(
    0.04,
    0.925,
    "Roundtable conclusion explained: a passive external collector sub, not a full standalone separator.",
    fontsize=11,
    color=MUTED,
)

# Panel 1: What it is
ax1 = panel(fig, [0.04, 0.53, 0.44, 0.37], "1. What It Is", "A modified tubing joint placed immediately below the WellFi sonde.")

label(ax1, 7, 78, "BHA context", color=BLUE, size=11, weight="bold")
flow_boxes = [
    (8, 63, 18, 11, "#eef4ff", "Mud\njoints"),
    (30, 63, 20, 11, "#fff3df", "Collector\nsub"),
    (55, 63, 17, 11, "#e7fbfb", "WellFi\nsonde"),
    (77, 63, 15, 11, "#eaf7ef", "PCP"),
]
for x, y, w, h, fc, text in flow_boxes:
    ax1.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.4,rounding_size=2.5",
            linewidth=1,
            edgecolor=LINE,
            facecolor=fc,
        )
    )
    label(ax1, x + w / 2, y + h / 2, text, ha="center", va="center", size=9, weight="bold")

for sx, ex in [(26, 30), (50, 55), (72, 77)]:
    arrow(ax1, (sx, 68.5), (ex, 68.5), color=STEEL, lw=1.5, mutation=10)

label(ax1, 7, 45, "Collector sub enlarged", color=BLUE, size=11, weight="bold")

# Enlarged tubing joint
ax1.add_patch(Rectangle((12, 23), 66, 16, linewidth=1.8, edgecolor=STEEL, facecolor="#e8edf3"))
ax1.add_patch(Rectangle((16, 27), 58, 8, linewidth=1.2, edgecolor="#95a0af", facecolor="#fdfefe"))
label(ax1, 45, 31, "Full drift bore", color=BLUE, size=10, weight="bold", ha="center")
label(ax1, 45, 24.5, "Rod and couplings still pass normally", color=MUTED, size=8.2, ha="center")

# External profile on OD
profile = Polygon(
    [(28, 23), (34, 17), (55, 17), (61, 23), (59, 23), (55, 20), (34, 20), (30, 23)],
    closed=True,
    facecolor="#ffe7bf",
    edgecolor=AMBER,
    linewidth=2,
)
ax1.add_patch(profile)
label(ax1, 45, 13.5, "External collector geometry on tubing OD", color=AMBER, size=9.8, weight="bold", ha="center")
label(ax1, 45, 8.8, "Baseline shape: swept lip ring. Option still open: baffle fins.", color=MUTED, size=7.9, ha="center")

label(ax1, 81, 33, "24 in steel sub", color=GREEN, size=9.5, weight="bold")
arrow(ax1, (81, 31), (77, 31), color=GREEN, lw=1.5, mutation=10)

label(ax1, 81, 24, "Conductive for\nWellFi EM", color=GREEN, size=9.2, weight="bold")
arrow(ax1, (81, 22), (74, 22), color=GREEN, lw=1.5, mutation=10)

label(ax1, 7, 5.6, "Direct takeaway: this is a modified joint that passively improves local flow quality before the PCP.", color=TEXT, size=9.1, weight="bold")

# Panel 2: What changed
ax2 = panel(fig, [0.52, 0.53, 0.44, 0.37], "2. What Changed", "The internal-bore design was rejected. The approved concept moves the collector outside.")

# Left: rejected
label(ax2, 25, 80, "Rejected", color=RED, size=12, weight="bold", ha="center")
ax2.add_patch(Circle((25, 46), 22, fill=False, linewidth=2, edgecolor=STEEL))
ax2.add_patch(Circle((25, 46), 9, facecolor="#f4efe8", edgecolor=AMBER, linewidth=1.8))
ax2.add_patch(Wedge((25, 46), 9, 205, 335, width=3.6, facecolor="#ffd7cc", edgecolor=RED, linewidth=2))
ax2.add_patch(Circle((25, 46), 7.3, facecolor="#fffdfc", edgecolor="#8d98a6", linewidth=1.2))
ax2.add_patch(Circle((25, 46), 5.2, facecolor="#c48921", edgecolor="#8b5f0a", linewidth=1.2))
label(ax2, 25, 26, "Internal scoop reduced the bore.", color=TEXT, size=9, ha="center")
label(ax2, 25, 20, "Rod coupling hits collector lip.", color=RED, size=10, weight="bold", ha="center")
ax2.plot([13, 37], [60, 34], color=RED, linewidth=3)
ax2.plot([13, 37], [34, 60], color=RED, linewidth=3)

# Right: approved
label(ax2, 75, 80, "Approved", color=GREEN, size=12, weight="bold", ha="center")
ax2.add_patch(Circle((75, 46), 22, fill=False, linewidth=2, edgecolor=STEEL))
ax2.add_patch(Circle((75, 46), 9, facecolor="#f4efe8", edgecolor=AMBER, linewidth=1.8))
ax2.add_patch(Wedge((75, 46), 15, 210, 330, width=6, facecolor="#ffe7bf", edgecolor=AMBER, linewidth=2))
ax2.add_patch(Circle((75, 46), 7.3, facecolor="#fffdfc", edgecolor="#8d98a6", linewidth=1.2))
ax2.add_patch(Circle((75, 46), 5.2, facecolor="#c48921", edgecolor="#8b5f0a", linewidth=1.2))
label(ax2, 75, 26, "Full drift bore stays open.", color=TEXT, size=9, ha="center")
label(ax2, 75, 20, "Collector feature moves outside tubing wall.", color=GREEN, size=10, weight="bold", ha="center")
arrow(ax2, (75, 67), (75, 60), color=GREEN, lw=2)
label(ax2, 52, 11, "This was the key roundtable fix: solve the mechanical problem first, then keep the same passive-flow idea.", color=MUTED, size=9.2, ha="center")

# Panel 3: How it works
ax3 = panel(fig, [0.04, 0.08, 0.56, 0.37], "3. How It Works", "The tool exploits low-side liquid and high-side gas in a near-horizontal well.")

# Side view casing
ax3.add_patch(Rectangle((8, 30), 46, 28, linewidth=1.8, edgecolor=STEEL, facecolor="#f9fbfd"))
label(ax3, 10, 62.5, "Flow direction to pump", color=BLUE, size=10, weight="bold")
arrow(ax3, (28, 62), (50, 62), color=BLUE, lw=2)

# Gas and liquid zones
ax3.add_patch(Rectangle((8, 46), 46, 12, linewidth=0, facecolor="#ffe3e8"))
ax3.add_patch(Rectangle((8, 30), 46, 12, linewidth=0, facecolor="#fff1d6"))
label(ax3, 12, 52, "High side gas path", color=GAS, size=10, weight="bold")
label(ax3, 12, 35, "Low side liquid layer", color=LIQ, size=10, weight="bold")

# Tubing body and collector
ax3.add_patch(Rectangle((22, 39), 18, 8, linewidth=1.5, edgecolor="#8b95a1", facecolor="#e8edf3"))
collector = Polygon(
    [(25, 39), (27, 33), (35, 33), (37, 39), (36, 39), (34.5, 35.8), (27.5, 35.8), (26, 39)],
    closed=True,
    facecolor="#ffe7bf",
    edgecolor=AMBER,
    linewidth=2,
)
ax3.add_patch(collector)
label(ax3, 31, 44.2, "collector sub", color=TEXT, size=9.5, weight="bold", ha="center")

# Arrows showing process
arrow(ax3, (11, 37), (24, 37), color=LIQ, lw=2)

arrow(ax3, (18, 48), (18, 40), color=TEAL, lw=2)
label(ax3, 57, 82, "1. Mixed flow arrives from the lateral toward the pump.", color=TEXT, size=9.3, weight="bold")
label(ax3, 57, 76, "2. Liquid drains and falls back on the low side.", color=TEXT, size=9.3, weight="bold")

arrow(ax3, (28, 35), (34, 39), color=AMBER, lw=2)
label(ax3, 57, 66, "3. The external lip/fins catch part of that low-side liquid", color=TEXT, size=9.3, weight="bold")
label(ax3, 57, 60, "and create higher local liquid holdup near the intake zone.", color=MUTED, size=8.9)

for x1, x2 in [(20, 29), (29, 38), (38, 47)]:
    arrow(ax3, (x1, 52), (x2, 52), color=GAS, lw=1.8, alpha=0.9)
label(ax3, 57, 48, "4. Gas keeps the easier path on the high side and is less", color=TEXT, size=9.3, weight="bold")
label(ax3, 57, 42, "likely to enter the PCP intake region.", color=MUTED, size=8.9)

label(ax3, 57, 28, "Why 86 deg matters", color=BLUE, size=10.5, weight="bold")
label(ax3, 57, 22, "Near-horizontal wells naturally stratify: liquid low, gas high.", color=MUTED, size=8.9)
label(ax3, 57, 16, "This concept uses that geometry instead of relying on tiny bubbles rising in viscous oil.", color=MUTED, size=8.9)

# Panel 4: What to expect
ax4 = panel(fig, [0.64, 0.08, 0.32, 0.37], "4. What Result To Expect", "Modest upside, low mechanical downside, still needs testing.")

boxes = [
    (10, 66, 80, 13, "#fff4dc", "More liquid holdup near intake"),
    (10, 46, 80, 13, "#ffe7ea", "Less gas entering the PCP"),
    (10, 26, 80, 13, "#e8fbfb", "Smoother WellFi pressure/temperature signal"),
]
for x, y, w, h, fc, txt in boxes:
    ax4.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.4,rounding_size=2.8",
            linewidth=1,
            edgecolor=LINE,
            facecolor=fc,
        )
    )
    label(ax4, x + w / 2, y + h / 2, txt, ha="center", size=10.2, weight="bold")

arrow(ax4, (50, 64), (50, 59), color=STEEL, lw=1.6, mutation=10)
arrow(ax4, (50, 44), (50, 39), color=STEEL, lw=1.6, mutation=10)

label(ax4, 10, 16, "Target benefit", color=GREEN, size=10.5, weight="bold")
label(ax4, 90, 16, "10-25% gas bypass prevention", color=GREEN, size=10.5, weight="bold", ha="right")

label(ax4, 10, 10, "Economic logic", color=BLUE, size=10.0, weight="bold")
label(ax4, 90, 10, "No extra trip if it replaces a normal joint", color=BLUE, size=9.5, ha="right")

label(ax4, 10, 4.8, "Worst case", color=RED, size=10.0, weight="bold")
label(ax4, 90, 4.8, "It behaves like a benign spacer sub", color=RED, size=9.5, ha="right")

fig.text(
    0.04,
    0.02,
    "Roundtable basis: external annular geometry on a 2-7/8 in EUE full-bore steel joint. Open questions remain on profile, sand buildup, and collar clearance.",
    fontsize=9,
    color=MUTED,
)

output_path = r"C:\Users\kyle\MPS\Obsidian\petro-roundtable\docs\visuals\wellfi-collector-sub-roundtable-visual.png"
fig.savefig(output_path, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(output_path)
