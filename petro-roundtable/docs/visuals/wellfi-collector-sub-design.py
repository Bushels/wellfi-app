#!/usr/bin/env python3
"""WellFi Collector Sub — Asymmetric Low-Side Design Visualization.

Engineering visual for explaining the passive gas separation concept
to engineers. Shows cross-section, flow paths, gravity physics, and
BHA arrangement at 86 deg inclination.

Design philosophy: Subterranean Signal
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Theme
BG1, BG2 = '#06090f', '#0c1220'
CYAN, AMBER, GREEN, RED = '#00D4FF', '#F5A623', '#2dd4a8', '#ef4444'
TXT, TXT_DIM, GRID, WHITE = '#c8d0dc', '#5a6577', '#141e30', '#f0f4f8'
BLUE_LIGHT = '#4da6ff'
OIL_COLOR = '#8B6914'
GAS_COLOR = '#ff6b6b'
STEEL_COLOR = '#7a8a9e'

# Glow helper
def glow_line(ax, x, y, color, base_lw=2):
    for lw, alpha in [(base_lw*6, 0.04), (base_lw*3.5, 0.08), (base_lw*2, 0.15), (base_lw, 0.6)]:
        ax.plot(x, y, color=color, lw=lw, alpha=alpha, solid_capstyle='round')

def glow_circle(ax, center, radius, color, lw=2):
    for w, alpha in [(lw*4, 0.05), (lw*2, 0.1), (lw, 0.4)]:
        circle = plt.Circle(center, radius, fill=False, edgecolor=color, lw=w, alpha=alpha)
        ax.add_patch(circle)

fig = plt.figure(figsize=(28, 16), facecolor=BG1, dpi=200)

# Gradient background
ax_bg = fig.add_axes([0, 0, 1, 1], zorder=-1)
ax_bg.axis('off')
grad = np.linspace(0, 1, 256).reshape(1, -1).T
ax_bg.imshow(np.hstack([grad]*10), aspect='auto', extent=[0,1,0,1],
             cmap=LinearSegmentedColormap.from_list('bg', [BG1, BG2]))

# Title
fig.text(0.04, 0.955, 'WELLFI COLLECTOR SUB', color=WHITE, fontsize=28, fontweight='bold',
         fontfamily='Segoe UI',
         path_effects=[pe.withStroke(linewidth=1, foreground='#006680')])
fig.text(0.04, 0.925, 'Asymmetric Low-Side Passive Gas Separation for 86° Heavy Oil Wells',
         color=TXT_DIM, fontsize=12, fontfamily='Segoe UI')

# ═══════════════════════════════════════════════════════════
# PANEL 1: Cross-Section View (left)
# ═══════════════════════════════════════════════════════════
ax1 = fig.add_axes([0.04, 0.08, 0.28, 0.80])
ax1.set_facecolor(BG2)
ax1.set_aspect('equal')
ax1.set_xlim(-130, 130)
ax1.set_ylim(-130, 130)

# Title
ax1.text(0, 125, 'CROSS-SECTION AT 86° INCLINATION', ha='center', va='center',
         color=CYAN, fontsize=10, fontweight='bold', fontfamily='Segoe UI')
ax1.text(0, 115, 'Looking downhole (toward toe)', ha='center', va='center',
         color=TXT_DIM, fontsize=7, fontfamily='Segoe UI')

# Gravity arrow (pointing DOWN = low side)
ax1.annotate('', xy=(0, -118), xytext=(0, -95),
             arrowprops=dict(arrowstyle='->', color=RED, lw=2))
ax1.text(15, -108, 'g', color=RED, fontsize=10, fontweight='bold', fontstyle='italic')
ax1.text(40, -108, '(LOW SIDE)', color=RED, fontsize=7, fontfamily='Segoe UI')

# 8-5/8" Casing (ID = 100.6mm radius = ~100 for drawing)
casing_r = 100.6  # mm radius (7.921" ID / 2 = 100.6mm)
glow_circle(ax1, (0, 0), casing_r, STEEL_COLOR, lw=3)
casing = plt.Circle((0, 0), casing_r, fill=False, edgecolor=STEEL_COLOR, lw=2.5, alpha=0.8)
ax1.add_patch(casing)
ax1.text(75, 85, '8-5/8" CSG', color=TXT_DIM, fontsize=6, fontfamily='Consolas')
ax1.text(75, 78, 'ID=201.2mm', color=TXT_DIM, fontsize=5.5, fontfamily='Consolas')

# 2-7/8" Tubing (OD = 36.5mm radius)
tubing_r = 36.5  # mm radius (2.875" OD / 2)
# At 86 deg, tubing hangs slightly to the low side
tubing_offset_y = -10  # slight low-side offset due to gravity
glow_circle(ax1, (0, tubing_offset_y), tubing_r, AMBER, lw=2)
tubing = plt.Circle((0, tubing_offset_y), tubing_r, fill=True, facecolor='#1a1400',
                     edgecolor=AMBER, lw=2, alpha=0.8)
ax1.add_patch(tubing)
ax1.text(0, tubing_offset_y, 'TUBING\n2-7/8" EUE', ha='center', va='center',
         color=AMBER, fontsize=5.5, fontweight='bold', fontfamily='Segoe UI')

# Rod inside tubing (small, on low side)
rod_r = 9.5  # mm radius (~0.75" rod body)
rod = plt.Circle((0, tubing_offset_y - 15), rod_r, fill=True, facecolor='#332200',
                 edgecolor='#cc8800', lw=1, alpha=0.6)
ax1.add_patch(rod)
ax1.text(0, tubing_offset_y - 15, 'ROD', ha='center', va='center',
         color='#cc8800', fontsize=4.5, fontfamily='Consolas')

# Collector Lip (LOW SIDE — 180 degree half-moon)
# The lip projects from the tubing OD outward on the bottom half
lip_outer_r = 60  # mm (120mm OD / 2)
lip_inner_r = tubing_r  # starts at tubing OD

# Draw the half-moon lip (bottom 180 degrees)
theta_lip = np.linspace(np.pi, 2*np.pi, 100)  # bottom half
x_outer = lip_outer_r * np.cos(theta_lip)
y_outer = lip_outer_r * np.sin(theta_lip) + tubing_offset_y
x_inner = lip_inner_r * np.cos(theta_lip[::-1])
y_inner = lip_inner_r * np.sin(theta_lip[::-1]) + tubing_offset_y

# Fill the lip region
x_lip = np.concatenate([x_outer, x_inner])
y_lip = np.concatenate([y_outer, y_inner])
ax1.fill(x_lip, y_lip, color=AMBER, alpha=0.3)
ax1.plot(x_outer, y_outer, color=AMBER, lw=2.5, alpha=0.9)

# Label the lip
ax1.annotate('COLLECTOR LIP\n(180° half-moon)\n23mm projection',
             xy=(0, -lip_outer_r + tubing_offset_y),
             xytext=(-85, -85),
             color=AMBER, fontsize=6, fontweight='bold', fontfamily='Segoe UI',
             ha='center',
             arrowprops=dict(arrowstyle='->', color=AMBER, lw=1, alpha=0.6))

# Gas bypass corridor (TOP — label the open area)
ax1.text(0, 80, 'GAS BYPASS\nCORRIDOR', ha='center', va='center',
         color=GAS_COLOR, fontsize=8, fontweight='bold', fontfamily='Segoe UI', alpha=0.8)
# Gas bubbles on high side
for x, y, r in [(30, 70, 6), (-20, 65, 4), (10, 55, 5), (-35, 75, 3), (45, 60, 4)]:
    bubble = plt.Circle((x, y), r, fill=True, facecolor=GAS_COLOR, alpha=0.15,
                        edgecolor=GAS_COLOR, lw=0.5)
    ax1.add_patch(bubble)

# Liquid crescent on low side
theta_liq = np.linspace(1.15*np.pi, 1.85*np.pi, 100)
x_liq_outer = (casing_r - 3) * np.cos(theta_liq)
y_liq_outer = (casing_r - 3) * np.sin(theta_liq)
x_liq_inner = (casing_r - 25) * np.cos(theta_liq[::-1])
y_liq_inner = (casing_r - 25) * np.sin(theta_liq[::-1])
ax1.fill(np.concatenate([x_liq_outer, x_liq_inner]),
         np.concatenate([y_liq_outer, y_liq_inner]),
         color=OIL_COLOR, alpha=0.4)
ax1.text(0, -92, 'LIQUID CRESCENT', ha='center', va='center',
         color=OIL_COLOR, fontsize=6, fontweight='bold', fontfamily='Segoe UI')
ax1.text(0, -100, '(80,000 cP bitumen)', ha='center', va='center',
         color=TXT_DIM, fontsize=5, fontfamily='Segoe UI')

# Dimension lines
ax1.annotate('', xy=(lip_outer_r, tubing_offset_y - 45), xytext=(tubing_r, tubing_offset_y - 45),
             arrowprops=dict(arrowstyle='<->', color=TXT, lw=0.8))
ax1.text((lip_outer_r + tubing_r)/2, tubing_offset_y - 50, '23mm', ha='center',
         color=TXT, fontsize=5.5, fontfamily='Consolas')

ax1.set_xticks([])
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_visible(False)

# ═══════════════════════════════════════════════════════════
# PANEL 2: Longitudinal Side View (center)
# ═══════════════════════════════════════════════════════════
ax2 = fig.add_axes([0.35, 0.08, 0.30, 0.80])
ax2.set_facecolor(BG2)
ax2.set_xlim(-5, 25)
ax2.set_ylim(-2, 22)

ax2.text(10, 21.5, 'SIDE VIEW — BHA AT 86° INCLINATION', ha='center', va='center',
         color=CYAN, fontsize=10, fontweight='bold', fontfamily='Segoe UI')
ax2.text(10, 21, 'Low side is DOWN in this view', ha='center', va='center',
         color=TXT_DIM, fontsize=7, fontfamily='Segoe UI')

# Casing walls (two horizontal lines representing the casing bore)
# At 86 deg, nearly horizontal
casing_top = 18  # high side
casing_bot = 2   # low side
ax2.fill_between([0, 20], casing_top + 0.5, casing_top + 1.5, color=STEEL_COLOR, alpha=0.3)
ax2.fill_between([0, 20], casing_bot - 1.5, casing_bot - 0.5, color=STEEL_COLOR, alpha=0.3)
ax2.plot([0, 20], [casing_top, casing_top], color=STEEL_COLOR, lw=2, alpha=0.6)
ax2.plot([0, 20], [casing_bot, casing_bot], color=STEEL_COLOR, lw=2, alpha=0.6)
ax2.text(0.5, casing_top + 1, 'CASING (HIGH SIDE)', color=TXT_DIM, fontsize=5, fontfamily='Segoe UI')
ax2.text(0.5, casing_bot - 1.2, 'CASING (LOW SIDE)', color=TXT_DIM, fontsize=5, fontfamily='Segoe UI')

# Tubing (center-ish, slight low side)
tub_center = 9.5
tub_half = 1.2
ax2.fill_between([0, 20], tub_center - tub_half, tub_center + tub_half,
                 color='#1a1400', alpha=0.5)
ax2.plot([0, 20], [tub_center + tub_half, tub_center + tub_half], color=AMBER, lw=1.5, alpha=0.7)
ax2.plot([0, 20], [tub_center - tub_half, tub_center - tub_half], color=AMBER, lw=1.5, alpha=0.7)

# Rod inside tubing (dashed line on low side)
ax2.plot([0, 20], [tub_center - tub_half + 0.3, tub_center - tub_half + 0.3],
         color='#cc8800', lw=0.8, ls='--', alpha=0.5)
ax2.text(1, tub_center - tub_half + 0.6, 'ROD (inside tubing)', color='#cc8800',
         fontsize=4.5, fontfamily='Segoe UI', alpha=0.7)

# BHA Components (left to right = downhole to surface at 86 deg)
# Zones
zones = [
    (0.5, 4, 'MUD\nJOINTS', TXT_DIM, 0.1),
    (4, 7.5, 'COLLECTOR\nSUB', AMBER, 0.2),
    (7.5, 12, 'WellFi\nSONDE', CYAN, 0.2),
    (12, 15, 'NO-TURN\n+ TAG BAR', TXT_DIM, 0.1),
    (15, 19.5, 'PCP\nPUMP', GREEN, 0.15),
]

for x1, x2, label, color, alpha in zones:
    ax2.axvspan(x1, x2, ymin=0.1, ymax=0.9, color=color, alpha=alpha)
    ax2.text((x1+x2)/2, 19.5, label, ha='center', va='center',
             color=color, fontsize=7, fontweight='bold', fontfamily='Segoe UI')

# Collector lip feature (low side bump between x=4 and x=7.5)
lip_x = np.array([4, 4.5, 5, 5.75, 6.5, 7, 7.5])
lip_y = np.array([tub_center - tub_half, tub_center - tub_half - 2.5,
                  tub_center - tub_half - 3, tub_center - tub_half - 3,
                  tub_center - tub_half - 3, tub_center - tub_half - 2.5,
                  tub_center - tub_half])
ax2.fill_between(lip_x, lip_y, tub_center - tub_half, color=AMBER, alpha=0.4)
ax2.plot(lip_x, lip_y, color=AMBER, lw=2)
ax2.text(5.75, tub_center - tub_half - 3.8, 'LOW-SIDE LIP', ha='center',
         color=AMBER, fontsize=6, fontweight='bold', fontfamily='Segoe UI')
ax2.text(5.75, tub_center - tub_half - 4.4, '(23mm projection)', ha='center',
         color=TXT_DIM, fontsize=5, fontfamily='Consolas')

# Flow arrows — liquid on low side moving toward collector
for x_start in [1, 2, 3]:
    ax2.annotate('', xy=(x_start + 1.5, 3.5), xytext=(x_start, 3.5),
                 arrowprops=dict(arrowstyle='->', color=OIL_COLOR, lw=1.5, alpha=0.6))
ax2.text(2, 4.2, 'Liquid drains to low side', color=OIL_COLOR, fontsize=5.5,
         fontfamily='Segoe UI', fontstyle='italic')

# Gas arrows — high side bypass
for x_start in [3, 6, 9, 12, 15]:
    ax2.annotate('', xy=(x_start + 2, 16.5), xytext=(x_start, 16.5),
                 arrowprops=dict(arrowstyle='->', color=GAS_COLOR, lw=1.5, alpha=0.4))
ax2.text(10, 17.3, 'Free gas bypasses on HIGH SIDE →', color=GAS_COLOR, fontsize=5.5,
         fontfamily='Segoe UI', fontstyle='italic')

# Direction arrows
ax2.annotate('', xy=(0.3, 10), xytext=(2, 10),
             arrowprops=dict(arrowstyle='->', color=TXT_DIM, lw=1.5))
ax2.text(0.3, 10.8, '← TOE', color=TXT_DIM, fontsize=6, fontfamily='Segoe UI')
ax2.annotate('', xy=(19.7, 10), xytext=(18, 10),
             arrowprops=dict(arrowstyle='->', color=TXT_DIM, lw=1.5))
ax2.text(18.5, 10.8, 'SURFACE →', color=TXT_DIM, fontsize=6, fontfamily='Segoe UI')

# Bypass port with check valve (high side)
ax2.plot([6, 6], [tub_center + tub_half, tub_center + tub_half + 1.5],
         color=BLUE_LIGHT, lw=1.5, alpha=0.7)
ax2.plot([5.7, 6.3], [tub_center + tub_half + 1.5, tub_center + tub_half + 1.5],
         color=BLUE_LIGHT, lw=1.5, alpha=0.7)
ax2.text(6, tub_center + tub_half + 2.2, 'Bypass port\n+ check valve', ha='center',
         color=BLUE_LIGHT, fontsize=4.5, fontfamily='Segoe UI')

ax2.set_xticks([])
ax2.set_yticks([])
for spine in ax2.spines.values():
    spine.set_visible(False)

# ═══════════════════════════════════════════════════════════
# PANEL 3: Physics — Why This Works at 86° (upper right)
# ═══════════════════════════════════════════════════════════
ax3 = fig.add_axes([0.68, 0.50, 0.30, 0.38])
ax3.set_facecolor(BG2)
ax3.set_xlim(-2, 10)
ax3.set_ylim(-2, 8)

ax3.text(4, 7.5, 'WHY IT WORKS AT 86°', ha='center', va='center',
         color=GREEN, fontsize=10, fontweight='bold', fontfamily='Segoe UI')

# Gravity vector decomposition
# Draw the wellbore as an angled line
wb_angle = 86 * np.pi / 180  # from vertical
wb_x = [1, 1 + 6 * np.sin(wb_angle)]
wb_y = [6, 6 - 6 * np.cos(wb_angle)]
ax3.plot(wb_x, wb_y, color=STEEL_COLOR, lw=8, alpha=0.3, solid_capstyle='round')
ax3.plot(wb_x, wb_y, color=STEEL_COLOR, lw=2, alpha=0.7)
ax3.text(4.5, 6.3, 'WELLBORE AT 86°', color=TXT_DIM, fontsize=6, fontfamily='Segoe UI')

# Gravity vector (straight down)
g_start = (3.5, 5.5)
g_len = 3.0
ax3.annotate('', xy=(g_start[0], g_start[1] - g_len),
             xytext=g_start,
             arrowprops=dict(arrowstyle='->', color=WHITE, lw=2.5))
ax3.text(g_start[0] + 0.3, g_start[1] - g_len/2, 'g', color=WHITE, fontsize=14,
         fontweight='bold', fontstyle='italic')

# Transverse component (perpendicular to wellbore — to low side)
# At 86 deg, sin(86) = 0.998
trans_len = g_len * np.sin(wb_angle)  # nearly full g
trans_dx = -trans_len * np.cos(wb_angle)
trans_dy = -trans_len * np.sin(wb_angle)
# Perpendicular to wellbore direction
perp_angle = wb_angle - np.pi/2
trans_dx2 = trans_len * np.cos(perp_angle)
trans_dy2 = trans_len * np.sin(perp_angle)
ax3.annotate('', xy=(g_start[0] + trans_dx2, g_start[1] + trans_dy2),
             xytext=g_start,
             arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.5))
ax3.text(g_start[0] + trans_dx2 - 0.5, g_start[1] + trans_dy2 - 0.5,
         'g_perp = 0.998g\n(TRANSVERSE)',
         color=CYAN, fontsize=7, fontweight='bold', fontfamily='Segoe UI')

# Axial component (along wellbore — very small)
axial_len = g_len * np.cos(wb_angle)  # 7% of g
ax_dx = axial_len * np.sin(wb_angle)
ax_dy = -axial_len * np.cos(wb_angle)
ax3.annotate('', xy=(g_start[0] + ax_dx, g_start[1] + ax_dy),
             xytext=g_start,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5, alpha=0.6))
ax3.text(g_start[0] + ax_dx + 0.3, g_start[1] + ax_dy + 0.2,
         'g_axial = 0.07g\n(AXIAL)',
         color=RED, fontsize=6, fontfamily='Segoe UI', alpha=0.8)

# Key insight text
ax3.text(5, 0.8, 'Transverse gravity is', color=TXT, fontsize=8, fontfamily='Segoe UI',
         ha='center')
ax3.text(5, 0.1, '14× STRONGER', color=CYAN, fontsize=14, fontweight='bold',
         fontfamily='Segoe UI', ha='center')
ax3.text(5, -0.6, 'than axial gravity at 86°', color=TXT, fontsize=8,
         fontfamily='Segoe UI', ha='center')
ax3.text(5, -1.3, 'Liquid pools on LOW SIDE, gas rides HIGH SIDE',
         color=TXT_DIM, fontsize=6, fontfamily='Segoe UI', ha='center')

ax3.set_xticks([])
ax3.set_yticks([])
for spine in ax3.spines.values():
    spine.set_visible(False)

# ═══════════════════════════════════════════════════════════
# PANEL 4: Data Reference (lower right)
# ═══════════════════════════════════════════════════════════
ax4 = fig.add_axes([0.68, 0.08, 0.30, 0.38])
ax4.set_facecolor(BG2)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)

ax4.text(5, 9.5, 'DESIGN DATA', ha='center', va='center',
         color=AMBER, fontsize=10, fontweight='bold', fontfamily='Segoe UI')

data_lines = [
    ('WELL CONDITIONS', None, None),
    ('Inclination', '86° from vertical', CYAN),
    ('Dead oil viscosity', '80,000 cP', CYAN),
    ('Live oil viscosity (GVF<40%)', '44,800 cP', CYAN),
    ('Liquid rate', '190 bbl/d', CYAN),
    ('GOR', '5-15 scf/bbl', CYAN),
    ('Casing', '8-5/8" (ID=201.2mm)', CYAN),
    ('', '', None),
    ('SEPARATION PHYSICS', None, None),
    ('2mm bubble rise (live oil)', '0.049 mm/s', RED),
    ('Sand settling (120μm)', '0.0003 mm/s', RED),
    ('Gravity separation', 'IMPOSSIBLE', RED),
    ('Annular velocity', '13.31 mm/s', CYAN),
    ('Coalescence time', '19.7 min (marginal)', AMBER),
    ('', '', None),
    ('COLLECTOR SUB', None, None),
    ('Expected efficiency', '5-15%', GREEN),
    ('Worst case', 'Benign spacer', GREEN),
    ('Added trip cost', '$0', GREEN),
    ('PCP life savings', '~$10K/well/year', GREEN),
]

y_pos = 8.8
for label, value, color in data_lines:
    if value is None and color is None:
        # Section header
        ax4.text(0.5, y_pos, label, color=AMBER, fontsize=7, fontweight='bold',
                 fontfamily='Segoe UI')
        ax4.plot([0.5, 9.5], [y_pos - 0.15, y_pos - 0.15], color=AMBER, lw=0.5, alpha=0.3)
        y_pos -= 0.5
    elif label == '':
        y_pos -= 0.2
    else:
        ax4.text(0.8, y_pos, label, color=TXT_DIM, fontsize=6, fontfamily='Segoe UI')
        ax4.text(9.2, y_pos, value, color=color, fontsize=6.5, fontweight='bold',
                 fontfamily='Consolas', ha='right')
        y_pos -= 0.45

ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values():
    spine.set_visible(False)

# Provenance strip
fig.text(0.04, 0.015,
         'Sources: Saponja et al. 2021 SWPSC (WhaleShark principles) · SPE-136665 (foamy viscosity) · '
         'CGW 1978 (Stokes law) · Maini 1999 SPE-56541 (coalescence) · '
         'Bratu 2005 SPE-95272 (PCP multiphase) · Roundtable #3 panel consensus',
         color=TXT_DIM, fontsize=5, fontfamily='Segoe UI', alpha=0.5)

fig.text(0.96, 0.015, 'CONFIDENTIAL — WellFi Engineering',
         color=TXT_DIM, fontsize=5, fontfamily='Segoe UI', alpha=0.5, ha='right')

# Save
output_path = r'C:\Users\kyle\MPS\Obsidian\petro-roundtable\docs\visuals\wellfi-collector-sub-design.png'
fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=BG1)
plt.close()
print(f'Saved to: {output_path}')
