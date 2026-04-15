# Bubble Dynamics Reference — From Clift, Grace & Weber

Source: Clift, R., Grace, J.R., and Weber, M.E., *Bubbles, Drops, and Particles*,
Dover Publications (2005 reprint of 1978 Academic Press edition). ISBN 0-486-44580-1.
Citations use page numbers from this Dover edition.

---

## Stokes' Law (Exact Form)

For a **rigid sphere** (no internal circulation) at low Reynolds number (CGW 1978, Ch. 3):

```
v_t = (2/9) * (rho_l - rho_g) * g * R^2 / mu_l      [Stokes, rigid sphere]
```

Or equivalently in terms of diameter d = 2R:

```
v_t = (1/18) * (rho_l - rho_g) * g * d^2 / mu_l
```

**Assumptions and validity:**
- Re = rho_l * v_t * d / mu_l < 1 (strictly; CGW use Re < 0.5 for accuracy within 1%)
- Unbounded fluid (no walls)
- Rigid, non-circulating interface (kappa = mu_p/mu_l → infinity)
- Spherical shape (low Eo, no deformation)
- Steady, creeping (Stokes) flow — inertia neglected

Drag coefficient form: C_D = 24/Re (CGW 1978, Eq. 3-17, p.34)

---

## Hadamard-Rybczynski Correction (Fluid Spheres)

Gas bubbles have a **mobile interface** (kappa = mu_gas/mu_liquid ≈ 0 for gas in oil).
The H-R solution gives a faster rise velocity than Stokes because surface tangential
stress is zero (free-slip interface allows internal circulation):

```
v_t_HR = v_t_Stokes * (3*kappa + 3) / (3*kappa + 2)
```

For a **gas bubble** (kappa → 0, i.e., mu_gas << mu_liquid):

```
v_t_HR = (3/2) * v_t_Stokes = (1/12) * (rho_l - rho_g) * g * d^2 / mu_l
```

This is the **Hadamard-Rybczynski terminal velocity** — 50% faster than Stokes for
a pure gas bubble in the creeping flow limit (CGW 1978, Ch. 3, Eq. 3-15, p.34).

Drag coefficient for fluid sphere (H-R): C_D = 16/Re  (vs. 24/Re for rigid sphere)

**Critical caveat:** In practice, surface-active contaminants (surfactants, asphaltenes,
resins) render the interface rigid. In contaminated systems (most real oils), bubbles
behave like **rigid spheres** and the Stokes law applies, not H-R. The H-R velocity
is an upper bound; the Stokes velocity is a lower bound (CGW 1978, Ch. 5, p.125-134).

Validity: Re < 1 (creeping flow). Both Stokes and H-R require Re < 1.

---

## Grace Correlation (Generalized Terminal Velocity)

The Grace et al. (G12) correlation covers contaminated liquids across all Re
(ellipsoidal regime, Eo < 40, Re > 0.1) using three dimensionless groups
(CGW 1978, Ch. 7, Eqs. 7-5 to 7-9, pp.175-176):

**Dimensionless groups:**

```
Eo  = g * (rho_l - rho_g) * d_e^2 / sigma          [Eotvos number]
Mo  = g * mu_l^4 * (rho_l - rho_g) / (rho_l^2 * sigma^3)  [Morton number]
Re  = rho_l * v_t * d_e / mu_l                       [Reynolds number]
```

where d_e = volume-equivalent sphere diameter, sigma = interfacial tension.

**Grace correlation equations:**

```
H = (4/3) * Eo * M^(-0.149) * (mu_l / mu_w)^(-0.14)        [Eq. 7-7]
J = Re * M^0.149 + 0.857                                     [Eq. 7-8]
```

where mu_w = 0.0009 kg/(m·s) [viscosity of water at reference conditions].

For 2 < H <= 59.3:
```
J = 0.94 * H^0.757                                           [Eq. 7-5]
```

For H > 59.3:
```
J = 3.42 * H^0.441                                           [Eq. 7-6]
```

Then extract terminal velocity from J:
```
v_t = (mu_l / (rho_l * d_e)) * M^(-0.149) * (J - 0.857)    [Eq. 7-9]
```

**Accuracy:** rms deviation ~15% for H <= 59.3 (774 pts), ~11% for H > 59.3 (709 pts).

**Applicability criteria (CGW 1978, p.175, Eq. 7-4):**
```
M < 1e-3,   Eo < 40,   Re > 0.1
```

This correlation was derived for **contaminated** systems (surfactants present, rigid
interface). For pure systems, apply correction factor Gamma from Fig. 7.7 via Eq. 7-10:
```
v_t_pure = v_t * [1 + Gamma / (1 + kappa)]
```

---

## Regime Map (Fig. 2.5 / Fig. 7.3)

The shape regime of a bubble is determined by Eo and M (or equivalently Re and Eo):

| Regime         | Shape           | Conditions                        |
|----------------|-----------------|-----------------------------------|
| Spherical      | Sphere          | Low Eo (< ~1), any M              |
| Ellipsoidal    | Oblate spheroid | Eo 1-40, low-moderate M           |
| Spherical-cap  | Mushroom cap    | Eo > 40, large bubbles            |

For our conditions — **small gas bubbles (d ~ 0.5-3 mm) in 80,000 cP oil**:

```
Example: d = 2 mm, rho_l = 997 kg/m3, mu_l = 80 Pa.s, sigma ~ 0.025 N/m

Eo = 9.81 * 997 * (0.002)^2 / 0.025 = 1.57         [borderline spherical/ellipsoidal]
Mo = 9.81 * (80)^4 * 997 / (997^2 * (0.025)^3)
   = 9.81 * 4.096e7 * 997 / (994009 * 1.5625e-5)
   = 4.01e11 / 15.53 ≈ 2.58e10                       [extremely high Mo]
```

At Mo ~ 1e10, Fig. 2.5 shows bubbles remain **rigidly spherical at all Eo values**
that would normally produce ellipsoidal shapes in low-viscosity liquids.

**Conclusion for 80,000 cP oil:** Bubbles stay spherical regardless of size because
the enormous viscous forces suppress shape oscillations and deformation. This means
Stokes law (or H-R) applies as the drag model — no need for ellipsoidal corrections.
(CGW 1978, Ch. 2 and Ch. 7, p.173-174: "bubbles and drops in systems of high Morton
number are never ellipsoidal.")

---

## Viscosity Effects on Bubble Behavior

From CGW 1978, Chapters 2, 3, 7, and 9:

**1. Shape — stays spherical longer**
High mu_l increases Mo dramatically (Mo ~ mu_l^4). At Mo > ~1e-3, bubbles remain
spherical across all Eo ranges that would produce ellipsoidal shapes in water.
In 80,000 cP oil, essentially all bubbles are spherical regardless of size.

**2. Rise velocity — much slower**
Stokes velocity scales as v_t ~ d^2 / mu_l. At 80,000 cP (80 Pa.s) vs water (0.001 Pa.s),
the velocity is suppressed by a factor of ~80,000. A 2 mm bubble that rises at ~20 cm/s
in water rises at < 0.003 mm/s in 80,000 cP oil (see Worked Example below).

**3. Internal circulation — suppressed, interface effectively rigid**
Internal circulation reduces drag (H-R gives C_D = 16/Re vs Stokes 24/Re).
However, at high kappa = mu_gas/mu_l ≈ 0 (gas), internal circulation should be
maximal — BUT in real crude oil, asphaltenes and resins adsorb at the bubble surface,
rendering it rigid. The effective kappa → infinity and Stokes (24/Re) applies.
(CGW 1978, Ch. 5, p.125: "high values of kappa... interface is usually stagnant.")

**4. Coalescence — dramatically slower**
Film drainage rate between approaching bubbles scales as ~1/mu_l. In 80,000 cP oil,
bubble coalescence is extremely slow — bubbles may persist as separate entities for
extended periods. This is relevant to foamy oil: gas remains dispersed as micro-bubbles.

**5. Wall effects — stronger in viscous media (see below)**

---

## Wall Effects (Pipe / Annulus Confinement)

From CGW 1978, Chapter 9. Define:
```
lambda = d_e / D      [diameter ratio: bubble diameter / pipe inner diameter]
```

**For lambda < 0.6 (bubble smaller than ~60% of pipe diameter):**

Intermediate-size bubbles and drops (Eo < 40, Re > 1):
```
U_T / U_T_inf = [1 - lambda^2]^(3/2)                         [Eq. 9-35]
```

This applies for Eo < 40, Re > 200, lambda <= 0.6 (CGW 1978, p.233).
For lower Re (Re in 1-200), use Fig. 9.5 (graphical correction).

Wall effects are negligible (< 2% on terminal velocity) when:
```
Re <= 0.1:    lambda <= 0.06                                  [Eq. 9-32]
0.1 < Re < 100:  lambda <= 0.08 + 0.02*log10(Re)             [Eq. 9-33]
Re >= 100:    lambda <= 0.12                                  [Eq. 9-34]
```

**For slug flow (lambda > 0.6):**

Viscosity-dominant slug velocity (Eo_D > 70, Fr_D < 0.05):
```
U_T = g * D^2 * Delta_rho / (102 * mu_l)                     [Eq. 9-38]
```

**For annular geometry** (inner diameter D_i, outer diameter D_o):
```
Fr_D = 0.35 + 0.06 * D_i / D_o                               [Eq. 9-40]
```

(CGW 1978, Ch. 9, pp.231-240)

**Key insight for tubing/casing annulus:** Our WellFi well has tubing OD ~73 mm inside
8-5/8" casing ID ~197 mm. Annular gap ~62 mm. A 2 mm bubble has lambda ~ 0.032 — well
below wall-effect threshold. Slug bubbles (> ~120 mm diameter) would be shaped by
the annulus geometry and use Eq. 9-40.

---

## Key Equations for Calculation Scripts

```python
import math

# Constants
g = 9.81          # m/s^2
mu_w = 0.0009     # kg/(m·s), water reference viscosity for Grace correlation

def stokes_velocity(d, rho_l, rho_g, mu_l):
    """
    Stokes terminal velocity for rigid sphere (lower bound for gas bubble).
    Valid: Re < 1, unbounded fluid.
    CGW 1978, Ch. 3, Eq. 3-17
    """
    return (1/18) * (rho_l - rho_g) * g * d**2 / mu_l

def hr_velocity(d, rho_l, rho_g, mu_l, kappa=0.0):
    """
    Hadamard-Rybczynski terminal velocity for fluid sphere.
    kappa = mu_gas/mu_liquid (≈ 0 for gas bubble in oil).
    Valid: Re < 1. Upper bound for clean bubble (no surfactants).
    CGW 1978, Ch. 3, Eq. 3-15
    """
    v_stokes = stokes_velocity(d, rho_l, rho_g, mu_l)
    return v_stokes * (3*kappa + 3) / (3*kappa + 2)

def reynolds(v_t, d, rho_l, mu_l):
    return rho_l * v_t * d / mu_l

def eotvos(d, rho_l, rho_g, sigma):
    return g * (rho_l - rho_g) * d**2 / sigma

def morton(rho_l, rho_g, mu_l, sigma):
    return g * mu_l**4 * (rho_l - rho_g) / (rho_l**2 * sigma**3)

def grace_velocity(d_e, rho_l, rho_g, mu_l, sigma):
    """
    Grace et al. correlation for terminal velocity of bubbles/drops.
    Valid: M < 1e-3, Eo < 40, Re > 0.1. Contaminated systems.
    CGW 1978, Ch. 7, Eqs. 7-5 to 7-9
    """
    Mo = morton(rho_l, rho_g, mu_l, sigma)
    Eo = eotvos(d_e, rho_l, rho_g, sigma)
    H = (4/3) * Eo * Mo**(-0.149) * (mu_l / mu_w)**(-0.14)
    if H <= 59.3:
        J = 0.94 * H**0.757
    else:
        J = 3.42 * H**0.441
    v_t = (mu_l / (rho_l * d_e)) * Mo**(-0.149) * (J - 0.857)
    return max(v_t, 0.0)

def wall_correction(v_t_inf, lambda_ratio, Re):
    """
    Wall correction for bubbles/drops: lambda = d_bubble / D_pipe.
    Applies for Eo < 40, Re > 200, lambda <= 0.6.
    CGW 1978, Ch. 9, Eq. 9-35
    """
    if lambda_ratio > 0.6:
        raise ValueError("Use slug flow equations for lambda > 0.6")
    return v_t_inf * (1 - lambda_ratio**2)**1.5
```

---

## Worked Example

**Conditions:** 2 mm gas bubble in 80,000 cP crude oil at 24 deg C
```
d     = 0.002 m
rho_l = 997 kg/m3  (wellbore fluid, SG ≈ 1.00)
rho_g ≈ 1.2 kg/m3  (gas at near-surface conditions; higher downhole)
mu_l  = 80 Pa.s    (80,000 cP)
sigma ≈ 0.025 N/m  (estimated; crude oil/gas)
g     = 9.81 m/s^2
```

**Step 1 — Stokes velocity (rigid interface, lower bound):**
```
v_t_Stokes = (1/18) * (997 - 1.2) * 9.81 * (0.002)^2 / 80
           = (1/18) * 995.8 * 9.81 * 4e-6 / 80
           = (1/18) * 3.906e-4
           = 2.17e-5 m/s  =  0.022 mm/s
```

**Step 2 — H-R velocity (clean bubble, mobile interface, upper bound):**
```
v_t_HR = (3/2) * 2.17e-5 = 3.26e-5 m/s  =  0.033 mm/s
```

**Step 3 — Check Re:**
```
Re = 997 * 2.17e-5 * 0.002 / 80 = 5.4e-7   <<  1  (Stokes regime confirmed)
```

**Step 4 — Dimensionless groups:**
```
Eo = 9.81 * (997-1.2) * (0.002)^2 / 0.025 = 1.57
Mo = 9.81 * (80)^4 * (997-1.2) / (997^2 * (0.025)^3) ≈ 2.6e10
```

Mo >> 1e-3, so Grace correlation does NOT apply (it requires M < 1e-3).
Stokes / H-R is the correct model here.

**Step 5 — Wall correction (WellFi well: annulus gap ~62 mm):**
```
lambda = 2 mm / 62 mm = 0.032   (far below wall effect threshold of 0.06 at Re < 0.1)
Wall correction negligible — bubble velocity essentially unaffected by walls.
```

**Result summary:**
```
Bubble rise velocity in 80,000 cP oil:
  Lower bound (rigid, contaminated):  0.022 mm/s  (~2 m/day)
  Upper bound (clean, mobile):        0.033 mm/s  (~3 m/day)
  Practical estimate (real crude):    ~0.022 mm/s (contaminated interface)

Time for 2 mm bubble to rise 1 meter:  ~45,000 seconds  (~12.5 hours)
Time to rise full 200 m liquid column:  ~105 days
```

**Engineering interpretation for foamy oil / Bluesky PCP wells:**
Gas micro-bubbles (< 1 mm) in 80,000 cP oil essentially do NOT rise — they are
carried with the produced fluid. Bubble rise velocity at 1 mm diameter is ~0.005 mm/s
(< 0.5 m/day). This is why foamy oil self-lifts: the dispersed gas phase remains
entrained, lowering effective fluid density without rising out of the fluid column.
Only at very high drawdown (JOF development) or major pressure changes do bubbles
coalesce and segregate. (CGW 1978 regime analysis + Stokes calculation above.)

---

*Extracted from: Clift, Grace & Weber 1978/2005, Chapters 2, 3, 5, 7, 9.*
*For regime diagram Fig. 2.5 and Fig. 7.3, refer to the source PDF directly.*
