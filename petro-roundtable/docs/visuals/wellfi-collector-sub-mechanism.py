#!/usr/bin/env python3
"""
WellFi Collector Sub — Mechanism Explainer
Single-concept visual: foamy oil degassing through staged flow restrictions.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon, Wedge, Arc
import numpy as np

# ── Subterranean Signal palette ──
BG      = "#0d1117"
PANEL   = "#161b22"
BORDER  = "#30363d"
TEXT    = "#e6edf3"
MUTED   = "#8b949e"
ACCENT  = "#00d4ff"   # wellfi-cyan
GOLD    = "#d4a847"
GREEN   = "#3fb950"
RED     = "#f85149"
ORANGE  = "#d29922"
GAS_CLR = "#ff6b6b"
OIL_CLR = "#d4a847"
STEEL   = "#6e7681"
FOAM_CLR = "#8b6914"  # foamy oil — dark amber
FREE_GAS = "#ff4444"  # free gas after coalescence
CASING  = "#484f58"
TUBING  = "#6e7681"

def glow_text(ax, x, y, text, color=TEXT, size=11, weight="normal", ha="left", va="center", alpha=1.0):
    """Text with subtle glow for dark backgrounds."""
    t = ax.text(x, y, text, fontsize=size, color=color, fontweight=weight,
                ha=ha, va=va, alpha=alpha, zorder=10)
    if weight == "bold" and size >= 11:
        t.set_path_effects([
            pe.withStroke(linewidth=3, foreground=BG, alpha=0.8),
        ])
    return t

def arrow(ax, start, end, color=TEXT, lw=1.5, style="-|>", mutation=10, alpha=1.0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=mutation,
                                  linewidth=lw, color=color, alpha=alpha, zorder=5))

fig = plt.figure(figsize=(18, 11), dpi=200, facecolor=BG)

# ── Title ──
fig.text(0.04, 0.955, "WellFi Collector Sub — How It Works",
         fontsize=24, fontweight="bold", color=TEXT, family="Segoe UI")
fig.text(0.04, 0.928,
         "Viscous shear through lip restrictions coalesces entrained micro-bubbles + fragments slug bodies.",
         fontsize=11, color=MUTED, family="Segoe UI")


# ═══════════════════════════════════════════════════════════════
# PANEL 1: THE PROBLEM — gas is trapped inside the oil
# ═══════════════════════════════════════════════════════════════
ax1 = fig.add_axes([0.04, 0.62, 0.44, 0.28])
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)
ax1.axis("off")
ax1.add_patch(FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0.6,rounding_size=3",
              linewidth=1, edgecolor=BORDER, facecolor=PANEL))

glow_text(ax1, 4, 93, "THE PROBLEM", color=RED, size=14, weight="bold")
glow_text(ax1, 4, 86, "Gas is trapped inside the oil, not floating above it.", color=MUTED, size=10)

# Cross-section of casing showing foamy oil
cx, cy, cr = 28, 48, 20
# Casing circle
theta = np.linspace(0, 2*np.pi, 100)
ax1.plot(cx + cr*np.cos(theta), cy + cr*np.sin(theta), color=CASING, linewidth=3, zorder=3)
glow_text(ax1, cx, cy + cr + 3, "8-5/8\" casing", color=CASING, size=9, ha="center")

# Fill the casing with foamy oil color (amber)
casing_fill = plt.Circle((cx, cy), cr - 1, facecolor="#2a1f0a", edgecolor="none", zorder=1)
ax1.add_patch(casing_fill)

# Tubing circle (eccentric, sitting low)
tr = 5.2
tx, ty = cx, cy - cr + tr + 3.5  # sits near bottom
ax1.plot(tx + tr*np.cos(theta), ty + tr*np.sin(theta), color=TUBING, linewidth=2.5, zorder=4)
# Tubing bore
ax1.add_patch(plt.Circle((tx, ty), tr - 1.2, facecolor="#1a1a2e", edgecolor=STEEL,
              linewidth=1, zorder=5))
glow_text(ax1, tx, ty, "rod +\ntubing", color=MUTED, size=7, ha="center")

# Micro-bubbles scattered THROUGHOUT the oil (not just on top)
np.random.seed(42)
n_bubbles = 55
for i in range(n_bubbles):
    angle = np.random.uniform(0, 2*np.pi)
    r = np.random.uniform(0, cr - 2.5)
    bx = cx + r * np.cos(angle)
    by = cy + r * np.sin(angle)
    # Skip if inside tubing
    if (bx - tx)**2 + (by - ty)**2 < (tr + 1.5)**2:
        continue
    bs = np.random.uniform(0.3, 1.1)
    ax1.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none",
                  alpha=0.5, zorder=2))

glow_text(ax1, cx, cy - cr - 5, "Cross-section at 86 deg", color=ACCENT, size=9, ha="center", weight="bold")

# Right side explanation
glow_text(ax1, 56, 75, "At 80,000 cP viscosity:", color=TEXT, size=11, weight="bold")
glow_text(ax1, 56, 67, "Gas is dispersed as micro-bubbles", color=GAS_CLR, size=10)
glow_text(ax1, 56, 60, "throughout the foamy oil.", color=GAS_CLR, size=10)

glow_text(ax1, 56, 49, "A 2mm bubble rises at 0.05 mm/s", color=MUTED, size=9.5)
glow_text(ax1, 56, 42, "= 4.3 metres per DAY.", color=MUTED, size=9.5)
glow_text(ax1, 56, 35, "Gravity separation is impossible.", color=RED, size=10, weight="bold")

glow_text(ax1, 56, 23, "But the bubbles are metastable.", color=GREEN, size=10, weight="bold")
glow_text(ax1, 56, 16, "Given the right conditions, they coalesce", color=MUTED, size=9.5)
glow_text(ax1, 56, 9,  "into free gas in 10-20 minutes.", color=MUTED, size=9.5)


# ═══════════════════════════════════════════════════════════════
# PANEL 2: THE MECHANISM — restriction + expansion = degassing
# ═══════════════════════════════════════════════════════════════
ax2 = fig.add_axes([0.52, 0.62, 0.44, 0.28])
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.axis("off")
ax2.add_patch(FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0.6,rounding_size=3",
              linewidth=1, edgecolor=BORDER, facecolor=PANEL))

glow_text(ax2, 4, 93, "THE MECHANISM", color=ACCENT, size=14, weight="bold")
glow_text(ax2, 4, 86, "Each lip is a degassing stage: viscous shear deforms bubbles, forcing coalescence.", color=MUTED, size=10)

# Side view — flow left to right through a single restriction
# Casing walls (top and bottom)
casing_y_top = 72
casing_y_bot = 28
ax2.plot([5, 95], [casing_y_top, casing_y_top], color=CASING, linewidth=2.5)
ax2.plot([5, 95], [casing_y_bot, casing_y_bot], color=CASING, linewidth=2.5)
glow_text(ax2, 50, casing_y_top + 3, "casing wall (high side / gas path)", color=CASING, size=8, ha="center")
glow_text(ax2, 50, casing_y_bot - 5, "casing wall (low side)", color=CASING, size=8, ha="center")

# Tubing body (running through middle-low)
tub_top = 47
tub_bot = 37
ax2.add_patch(Rectangle((5, tub_bot), 90, tub_top - tub_bot, facecolor="#1c2333",
              edgecolor=TUBING, linewidth=2, zorder=3))

# The external lip (on the BOTTOM of the tubing = low side)
lip_x = 48
lip_w = 8
lip_depth = 7
lip = Polygon([
    (lip_x, tub_bot),
    (lip_x - 2, tub_bot - lip_depth),
    (lip_x + lip_w + 2, tub_bot - lip_depth),
    (lip_x + lip_w, tub_bot),
], closed=True, facecolor=GOLD, edgecolor=ORANGE, linewidth=2, zorder=4)
ax2.add_patch(lip)
glow_text(ax2, lip_x + lip_w/2, tub_bot - lip_depth - 3.5, "external lip",
          color=GOLD, size=9, weight="bold", ha="center")

# Zone labels
# Zone A: upstream (foamy oil with entrained gas)
ax2.add_patch(Rectangle((8, casing_y_bot + 1), 35, casing_y_top - casing_y_bot - 2,
              facecolor="#2a1f0a", edgecolor="none", alpha=0.3, zorder=1))
# Micro-bubbles in zone A
for i in range(18):
    bx = np.random.uniform(10, 40)
    by = np.random.uniform(casing_y_bot + 3, tub_bot - 2)
    bs = np.random.uniform(0.4, 1.0)
    ax2.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none",
                  alpha=0.45, zorder=2))
# Also above tubing
for i in range(10):
    bx = np.random.uniform(10, 40)
    by = np.random.uniform(tub_top + 2, casing_y_top - 3)
    bs = np.random.uniform(0.3, 0.8)
    ax2.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none",
                  alpha=0.35, zorder=2))

glow_text(ax2, 8, 20, "A", color=ORANGE, size=18, weight="bold")
glow_text(ax2, 8, 14, "Foamy oil arrives", color=MUTED, size=8.5)
glow_text(ax2, 8, 9,  "gas entrained as", color=MUTED, size=8.5)
glow_text(ax2, 8, 4,  "micro-bubbles", color=GAS_CLR, size=8.5)

# Zone B: at the restriction (viscous shear — the REAL mechanism)
glow_text(ax2, 44, 20, "B", color=ORANGE, size=18, weight="bold")
glow_text(ax2, 44, 14, "Oil squeezes past lip", color=MUTED, size=8.5)
glow_text(ax2, 44, 9,  "Viscous shear = 118 Pa", color=ACCENT, size=8.5, weight="bold")
glow_text(ax2, 44, 4,  "Bubbles deform + coalesce", color=GAS_CLR, size=8.5)

# Zone C: downstream (expansion — free gas separates to high side)
# Larger bubbles (coalesced) rising toward high side
for i in range(6):
    bx = np.random.uniform(65, 90)
    by = np.random.uniform(tub_top + 5, casing_y_top - 5)
    bs = np.random.uniform(1.2, 2.2)
    ax2.add_patch(plt.Circle((bx, by), bs, facecolor=FREE_GAS, edgecolor="none",
                  alpha=0.6, zorder=2))
# Fewer, smaller bubbles remain below
for i in range(5):
    bx = np.random.uniform(65, 90)
    by = np.random.uniform(casing_y_bot + 3, tub_bot - 2)
    bs = np.random.uniform(0.3, 0.6)
    ax2.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none",
                  alpha=0.3, zorder=2))

glow_text(ax2, 72, 20, "C", color=ORANGE, size=18, weight="bold")
glow_text(ax2, 72, 14, "Flow expands, slows", color=MUTED, size=8.5)
glow_text(ax2, 72, 9,  "Freed gas rises to", color=MUTED, size=8.5)
glow_text(ax2, 72, 4,  "high side (14x gravity)", color=GREEN, size=8.5, weight="bold")

# Flow arrow
arrow(ax2, (8, 50), (20, 50), color=ACCENT, lw=2, mutation=12)
glow_text(ax2, 12, 53, "flow", color=ACCENT, size=8, ha="center")

# Rising gas arrows in zone C
arrow(ax2, (75, tub_top + 3), (75, casing_y_top - 4), color=FREE_GAS, lw=1.5, mutation=8, alpha=0.7)
arrow(ax2, (83, tub_top + 3), (83, casing_y_top - 4), color=FREE_GAS, lw=1.5, mutation=8, alpha=0.7)


# ═══════════════════════════════════════════════════════════════
# PANEL 3: MULTI-STAGE — why multiple lips work better
# ═══════════════════════════════════════════════════════════════
ax3 = fig.add_axes([0.04, 0.08, 0.60, 0.48])
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 100)
ax3.axis("off")
ax3.add_patch(FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0.6,rounding_size=3",
              linewidth=1, edgecolor=BORDER, facecolor=PANEL))

glow_text(ax3, 4, 95, "MULTI-STAGE DEGASSING", color=GREEN, size=14, weight="bold")
glow_text(ax3, 4, 90, "Each lip strips more gas. Multiple stages on one sub = progressive separation.", color=MUTED, size=10)

# Side view — longer section showing 3 lips
cas_top = 76
cas_bot = 44
tub_t = 64
tub_b = 56

# Casing
ax3.plot([4, 96], [cas_top, cas_top], color=CASING, linewidth=2.5)
ax3.plot([4, 96], [cas_bot, cas_bot], color=CASING, linewidth=2.5)

# Gravity arrow
arrow(ax3, (2, 68), (2, 48), color=MUTED, lw=1.2, mutation=8)
glow_text(ax3, 2, 72, "g", color=MUTED, size=9, ha="center", weight="bold")
glow_text(ax3, 1.2, 46, "low", color=MUTED, size=7, ha="center")
glow_text(ax3, 1.2, 74, "high", color=MUTED, size=7, ha="center")

# Tubing body
ax3.add_patch(Rectangle((6, tub_b), 88, tub_t - tub_b, facecolor="#1c2333",
              edgecolor=TUBING, linewidth=2, zorder=3))

# Three lips
lip_positions = [25, 50, 75]
lip_labels = ["Stage 1", "Stage 2", "Stage 3"]
lip_colors = [GOLD, GOLD, GOLD]

for i, (lx, lbl) in enumerate(zip(lip_positions, lip_labels)):
    lw_half = 3.5
    ld = 5.5
    lip = Polygon([
        (lx - lw_half, tub_b),
        (lx - lw_half - 1.5, tub_b - ld),
        (lx + lw_half + 1.5, tub_b - ld),
        (lx + lw_half, tub_b),
    ], closed=True, facecolor=GOLD, edgecolor=ORANGE, linewidth=1.8, zorder=4)
    ax3.add_patch(lip)
    glow_text(ax3, lx, tub_b - ld - 3, lbl, color=GOLD, size=9, weight="bold", ha="center")

# Gas evolution through stages
# Zone 1: lots of small bubbles (foamy oil)
for i in range(25):
    bx = np.random.uniform(8, 23)
    by_pool = [np.random.uniform(cas_bot + 2, tub_b - 2), np.random.uniform(tub_t + 2, cas_top - 2)]
    by = by_pool[np.random.randint(2)]
    bs = np.random.uniform(0.4, 0.9)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none", alpha=0.5, zorder=2))

# Zone 2: fewer small bubbles below, some bigger ones rising
for i in range(12):
    bx = np.random.uniform(30, 48)
    by = np.random.uniform(cas_bot + 2, tub_b - 2)
    bs = np.random.uniform(0.3, 0.7)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none", alpha=0.4, zorder=2))
for i in range(8):
    bx = np.random.uniform(30, 48)
    by = np.random.uniform(tub_t + 4, cas_top - 3)
    bs = np.random.uniform(1.0, 1.8)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=FREE_GAS, edgecolor="none", alpha=0.5, zorder=2))

# Zone 3: mostly clean below, gas concentrated high side
for i in range(4):
    bx = np.random.uniform(55, 73)
    by = np.random.uniform(cas_bot + 2, tub_b - 2)
    bs = np.random.uniform(0.2, 0.5)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=GAS_CLR, edgecolor="none", alpha=0.25, zorder=2))
for i in range(10):
    bx = np.random.uniform(55, 73)
    by = np.random.uniform(tub_t + 4, cas_top - 3)
    bs = np.random.uniform(1.2, 2.2)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=FREE_GAS, edgecolor="none", alpha=0.6, zorder=2))

# Zone 4: liquid-rich on low side, gas stream on high side
for i in range(12):
    bx = np.random.uniform(80, 94)
    by = np.random.uniform(tub_t + 5, cas_top - 3)
    bs = np.random.uniform(1.5, 2.5)
    ax3.add_patch(plt.Circle((bx, by), bs, facecolor=FREE_GAS, edgecolor="none", alpha=0.65, zorder=2))

# Flow direction
arrow(ax3, (6, 60), (16, 60), color=ACCENT, lw=2.5, mutation=14)
glow_text(ax3, 10, 62.5, "flow to pump", color=ACCENT, size=9, ha="center", weight="bold")

# Gas rising arrows between stages
for gx in [35, 60, 85]:
    arrow(ax3, (gx, tub_t + 2), (gx, cas_top - 3), color=FREE_GAS, lw=1.2, mutation=8, alpha=0.5)

# PCP intake label at right end
ax3.add_patch(FancyBboxPatch((89, tub_b - 1), 8, tub_t - tub_b + 2,
              boxstyle="round,pad=0.3,rounding_size=1.5", linewidth=1.5,
              edgecolor=GREEN, facecolor="#1a2e1a", zorder=5))
glow_text(ax3, 93, 60, "PCP", color=GREEN, size=9, weight="bold", ha="center")

# Stage efficiency labels
glow_text(ax3, 15, 38, "100% entrained", color=GAS_CLR, size=9, ha="center", weight="bold")
glow_text(ax3, 40, 38, "~70% remains", color=GAS_CLR, size=9, ha="center")
glow_text(ax3, 65, 38, "~45% remains", color=GAS_CLR, size=9, ha="center")
glow_text(ax3, 88, 38, "~25% at PCP", color=GREEN, size=9, ha="center", weight="bold")

# Efficiency bar at bottom
bar_y = 30
bar_h = 4
# Full bar (gas)
ax3.add_patch(Rectangle((8, bar_y), 84, bar_h, facecolor="#2a1a1a", edgecolor=BORDER, linewidth=1, zorder=1))
# Progressive reduction
widths = [84, 59, 37, 21]
alphas = [0.7, 0.5, 0.35, 0.2]
for w, a in zip(widths, alphas):
    ax3.add_patch(Rectangle((8, bar_y), w, bar_h, facecolor=GAS_CLR, edgecolor="none", alpha=a, zorder=2))

# Vertical markers at each stage
for sx, pct in zip([8, 29, 54, 79, 92], ["100%", "", "", "", ""]):
    ax3.plot([sx, sx], [bar_y - 1, bar_y + bar_h + 1], color=BORDER, linewidth=1, zorder=3)

glow_text(ax3, 8, bar_y - 3, "Entrained gas fraction", color=MUTED, size=8)
glow_text(ax3, 92, bar_y - 3, "at PCP intake", color=GREEN, size=8, ha="right")

# Key insight box
ax3.add_patch(FancyBboxPatch((4, 4), 92, 17, boxstyle="round,pad=0.5,rounding_size=2",
              linewidth=1.2, edgecolor=ACCENT, facecolor="#0a1929", zorder=6))
glow_text(ax3, 50, 15, "Each lip creates a viscous shear zone that forces bubble coalescence.",
          color=TEXT, size=10.5, weight="bold", ha="center")
glow_text(ax3, 50, 8.5, "High viscosity = high shear even at low velocity. Slug bodies also get fragmented. 3 lips = 80% gas freed + 59% slug damping.",
          color=MUTED, size=9, ha="center")


# ═══════════════════════════════════════════════════════════════
# PANEL 4: PRACTICAL SUMMARY
# ═══════════════════════════════════════════════════════════════
ax4 = fig.add_axes([0.68, 0.08, 0.28, 0.48])
ax4.set_xlim(0, 100)
ax4.set_ylim(0, 100)
ax4.axis("off")
ax4.add_patch(FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0.6,rounding_size=3",
              linewidth=1, edgecolor=BORDER, facecolor=PANEL))

glow_text(ax4, 6, 95, "WHY IT WORKS", color=ACCENT, size=14, weight="bold")

items = [
    (85, GOLD, "Viscous shear",
     "Lip narrows the gap. At 44,800 cP,\neven 13 mm/s creates 118 Pa shear."),
    (70, GAS_CLR, "Bubble coalescence",
     "Shear deforms micro-bubbles (Ca >> 1).\nForced contact merges them."),
    (55, GREEN, "Gravity does the rest",
     "At 86 deg, transverse gravity is 14x\naxial. Freed gas rises to high side."),
    (40, ACCENT, "Slug damping",
     "Restrictions fragment slug bodies.\n59% amplitude reduction (3 lips)."),
]

for y, color, title, desc in items:
    ax4.add_patch(plt.Circle((10, y), 3, facecolor=color, edgecolor="none", alpha=0.3))
    glow_text(ax4, 10, y, str(items.index((y, color, title, desc)) + 1),
              color=color, size=12, weight="bold", ha="center")
    glow_text(ax4, 18, y + 2, title, color=color, size=10.5, weight="bold")
    glow_text(ax4, 18, y - 4, desc, color=MUTED, size=8.5)

# Arrows between items
for y1, y2 in [(82, 75), (67, 60), (52, 45)]:
    arrow(ax4, (10, y1), (10, y2), color=BORDER, lw=1.2, mutation=8)

# Multi-stage note
ax4.add_patch(FancyBboxPatch((4, 4), 92, 24, boxstyle="round,pad=0.5,rounding_size=2",
              linewidth=1, edgecolor=GREEN, facecolor="#0a1e0a", zorder=6))
glow_text(ax4, 50, 22, "Multiple lips = multiple stages", color=GREEN, size=11, weight="bold", ha="center")
glow_text(ax4, 50, 15, "Each strips another ~30% of", color=MUTED, size=9.5, ha="center")
glow_text(ax4, 50, 9,  "remaining entrained gas.", color=MUTED, size=9.5, ha="center")


# ── Footer ──
fig.text(0.04, 0.02,
         "SPE-136665 (foamy viscosity = 56% of dead), Maini 1999 (coalescence 10-20 min), Gokcal SPE-102727 (slug flow above 587 cP). "
         "Bernoulli dP = 0.25 Pa (negligible). Viscous shear = 118 Pa (the real mechanism). Re = 0.037 (creeping flow).",
         fontsize=8.5, color=MUTED, family="Segoe UI")

output_path = r"C:\Users\kyle\MPS\Obsidian\petro-roundtable\docs\visuals\wellfi-collector-sub-mechanism.png"
fig.savefig(output_path, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(output_path)
