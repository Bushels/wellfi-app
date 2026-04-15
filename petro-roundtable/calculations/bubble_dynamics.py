#!/usr/bin/env python3
"""Bubble dynamics calculator for downhole separator design.

Calculates bubble rise velocity in viscous fluids using Stokes' law,
Hadamard-Rybczynski correction, and Grace correlation. Includes
foamy oil viscosity correction per SPE-136665.

Sources:
  - Clift, Grace & Weber (1978) "Bubbles, Drops and Particles"
  - Alshmakhy & Maini (2010) SPE-136665 "Viscosity of Foamy Oils"

Usage:
  python bubble_dynamics.py --viscosity 80000 --density_oil 997 --density_gas 0.8 --bubble_diameter 2.0
  python bubble_dynamics.py --viscosity 80000 --density_oil 997 --density_gas 0.8 --bubble_diameter 2.0 --gvf 0.3
"""

import argparse
import math
import sys


def stokes_velocity(rho_l, rho_g, mu_l, d):
    """Stokes' law terminal velocity for rigid sphere (contaminated interface).
    CGW 1978, Eq. 3-17. Valid for Re < 1.

    Args:
        rho_l: liquid density (kg/m3)
        rho_g: gas density (kg/m3)
        mu_l: liquid dynamic viscosity (Pa.s)
        d: bubble diameter (m)
    Returns:
        terminal velocity (m/s)
    """
    g = 9.81
    return (1.0 / 18.0) * (rho_l - rho_g) * g * d**2 / mu_l


def hr_velocity(rho_l, rho_g, mu_l, d):
    """Hadamard-Rybczynski terminal velocity for clean gas bubble.
    CGW 1978, Eq. 3-15. 50% faster than Stokes. Upper bound.

    For gas bubbles (kappa = mu_gas/mu_liquid -> 0):
        v_HR = (3/2) * v_Stokes
    """
    return 1.5 * stokes_velocity(rho_l, rho_g, mu_l, d)


def reynolds_number(rho_l, v, d, mu_l):
    """Particle Reynolds number."""
    return rho_l * v * d / mu_l


def morton_number(rho_l, rho_g, mu_l, sigma):
    """Morton number — characterizes the fluid system.
    CGW 1978, Ch. 7. Mo = g * mu_l^4 * (rho_l - rho_g) / (rho_l^2 * sigma^3)
    """
    g = 9.81
    return g * mu_l**4 * (rho_l - rho_g) / (rho_l**2 * sigma**3)


def eotvos_number(rho_l, rho_g, d, sigma):
    """Eotvos number — ratio of buoyancy to surface tension.
    CGW 1978, Ch. 7. Eo = g * (rho_l - rho_g) * d^2 / sigma
    """
    g = 9.81
    return g * (rho_l - rho_g) * d**2 / sigma


def foamy_oil_viscosity_correction(mu_dead, gvf):
    """Correct viscosity for foamy oil per SPE-136665 (Alshmakhy & Maini 2010).

    Key finding: foamy oil viscosity = live oil viscosity for GVF 0-40%.
    Live oil viscosity is approximately 56% of dead oil viscosity
    (dissolved gas reduces viscosity by ~44%).

    Above GVF 50%, viscosity rises toward 75-80% of dead oil.

    Args:
        mu_dead: dead oil viscosity (Pa.s)
        gvf: gas volume fraction (0 to 1)
    Returns:
        corrected viscosity (Pa.s), regime description
    """
    if gvf <= 0.40:
        # GVF 0-40%: foamy oil viscosity = live oil viscosity ~ 56% of dead oil
        mu_corrected = mu_dead * 0.56
        regime = "foamy (GVF<=40%): viscosity = live oil ~ 56% of dead oil (SPE-136665)"
    elif gvf <= 0.55:
        # Transition zone: linear interpolation between live oil and elevated
        fraction = (gvf - 0.40) / 0.15
        mu_low = mu_dead * 0.56
        mu_high = mu_dead * 0.75
        mu_corrected = mu_low + fraction * (mu_high - mu_low)
        regime = f"transition (40%<GVF<55%): interpolated viscosity"
    else:
        # GVF > 55%: viscosity rises to ~75-80% of dead oil
        mu_corrected = mu_dead * 0.78
        regime = "high-GVF (>55%): viscosity ~ 78% of dead oil (SPE-136665, Fig 8)"

    return mu_corrected, regime


def wall_correction(d_bubble, d_pipe):
    """Wall correction factor for bubble rise in confined geometry.
    CGW 1978, Eq. 9-32 (Haberman & Sayre).

    Args:
        d_bubble: bubble diameter (m)
        d_pipe: pipe/annulus hydraulic diameter (m)
    Returns:
        correction factor (multiply terminal velocity by this)
    """
    lam = d_bubble / d_pipe
    if lam < 0.1:
        return 1.0  # negligible wall effect
    # Haberman & Sayre correlation for small bubbles
    return 1.0 - 2.104 * lam + 2.089 * lam**3


def sand_settling_velocity(rho_sand, rho_l, mu_l, d_sand):
    """Sand particle settling velocity using Stokes' law.
    Same physics as bubble rise but for solid particles.

    Args:
        rho_sand: sand density (kg/m3), typically 2650
        rho_l: liquid density (kg/m3)
        mu_l: liquid dynamic viscosity (Pa.s)
        d_sand: sand grain diameter (m)
    Returns:
        settling velocity (m/s)
    """
    g = 9.81
    return (1.0 / 18.0) * (rho_sand - rho_l) * g * d_sand**2 / mu_l


def main():
    parser = argparse.ArgumentParser(
        description="Bubble dynamics calculator for downhole separator design"
    )
    parser.add_argument("--viscosity", type=float, required=True,
                        help="Dead oil viscosity (cP)")
    parser.add_argument("--density_oil", type=float, default=997.0,
                        help="Oil density (kg/m3), default 997")
    parser.add_argument("--density_gas", type=float, default=0.8,
                        help="Gas density (kg/m3), default 0.8")
    parser.add_argument("--bubble_diameter", type=float, default=2.0,
                        help="Bubble diameter (mm), default 2.0")
    parser.add_argument("--temperature", type=float, default=24.0,
                        help="Temperature (deg C), default 24")
    parser.add_argument("--sigma", type=float, default=0.025,
                        help="Interfacial tension (N/m), default 0.025")
    parser.add_argument("--gvf", type=float, default=None,
                        help="Gas volume fraction (0-1) for foamy oil correction")
    parser.add_argument("--pipe_diameter", type=float, default=None,
                        help="Pipe/annulus hydraulic diameter (mm) for wall correction")
    parser.add_argument("--sand_diameter", type=float, default=None,
                        help="Sand grain diameter (microns) for settling calc")

    args = parser.parse_args()

    # Convert units
    mu_dead = args.viscosity / 1000.0  # cP to Pa.s
    d_bubble = args.bubble_diameter / 1000.0  # mm to m

    print("=" * 60)
    print("BUBBLE DYNAMICS CALCULATOR")
    print("=" * 60)
    print(f"Dead oil viscosity:  {args.viscosity:,.0f} cP ({mu_dead:.1f} Pa.s)")
    print(f"Oil density:         {args.density_oil:.1f} kg/m3")
    print(f"Gas density:         {args.density_gas:.1f} kg/m3")
    print(f"Bubble diameter:     {args.bubble_diameter:.1f} mm")
    print(f"Temperature:         {args.temperature:.1f} deg C")
    print(f"Interfacial tension: {args.sigma:.4f} N/m")
    print()

    # Foamy oil viscosity correction
    if args.gvf is not None:
        mu_corrected, regime = foamy_oil_viscosity_correction(mu_dead, args.gvf)
        print(f"GVF:                 {args.gvf*100:.0f}%")
        print(f"Viscosity regime:    {regime}")
        print(f"Corrected viscosity: {mu_corrected*1000:,.0f} cP ({mu_corrected:.1f} Pa.s)")
        mu_calc = mu_corrected
    else:
        print("GVF:                 Not specified (using dead oil viscosity)")
        mu_calc = mu_dead

    print()
    print("-" * 60)
    print("BUBBLE RISE VELOCITY")
    print("-" * 60)

    # Stokes velocity
    v_stokes = stokes_velocity(args.density_oil, args.density_gas, mu_calc, d_bubble)
    Re = reynolds_number(args.density_oil, v_stokes, d_bubble, mu_calc)
    Mo = morton_number(args.density_oil, args.density_gas, mu_calc, args.sigma)
    Eo = eotvos_number(args.density_oil, args.density_gas, d_bubble, args.sigma)

    print(f"Stokes velocity:     {v_stokes:.6f} m/s = {v_stokes*1000:.4f} mm/s")
    print(f"H-R velocity:        {v_stokes*1.5:.6f} m/s = {v_stokes*1500:.4f} mm/s (upper bound)")
    print(f"Reynolds number:     {Re:.2e}")
    print(f"Morton number:       {Mo:.2e}")
    print(f"Eotvos number:       {Eo:.4f}")
    print()

    # Regime assessment
    if Re < 1:
        print("Flow regime:         STOKES (Re < 1) -- creeping flow, valid")
    else:
        print("Flow regime:         NON-STOKES (Re >= 1) -- use Grace correlation")

    if Mo > 1e6:
        print("Bubble shape:        SPHERICAL (Mo >> 1) -- all bubbles stay spherical")
    elif Mo > 1:
        print("Bubble shape:        SPHERICAL to ELLIPSOIDAL")
    else:
        print("Bubble shape:        May deform -- check Grace diagram")

    print()

    # Practical implications
    time_1m = 1.0 / v_stokes if v_stokes > 0 else float('inf')
    time_1m_hr = time_1m / 3600.0
    v_m_per_day = v_stokes * 86400.0

    print("-" * 60)
    print("PRACTICAL IMPLICATIONS")
    print("-" * 60)
    print(f"Rise rate:           {v_m_per_day:.2f} m/day")
    print(f"Time to rise 1 m:    {time_1m:.0f} s = {time_1m_hr:.1f} hours")

    if v_stokes < 0.001:
        print()
        print("*** WARNING: Bubble rise velocity < 1 mm/s ***")
        print("Gravity-based gas separation of dispersed bubbles is")
        print("PHYSICALLY IMPOSSIBLE at this viscosity.")
        print("Separator must use LIQUID FALLBACK mechanism (WhaleShark-type)")
        print("or operate only on FREE GAS (coalesced slugs/Taylor bubbles).")

    # Wall correction
    if args.pipe_diameter:
        d_pipe = args.pipe_diameter / 1000.0  # mm to m
        wc = wall_correction(d_bubble, d_pipe)
        v_corrected = v_stokes * wc
        print()
        print(f"Pipe diameter:       {args.pipe_diameter:.1f} mm")
        print(f"Wall correction:     {wc:.4f}")
        print(f"Corrected velocity:  {v_corrected:.6f} m/s = {v_corrected*1000:.4f} mm/s")

    # Sand settling (Gemini audit challenge #2)
    if args.sand_diameter:
        d_sand = args.sand_diameter / 1e6  # microns to m
        rho_sand = 2650.0  # quartz sand
        v_sand = sand_settling_velocity(rho_sand, args.density_oil, mu_calc, d_sand)
        print()
        print("-" * 60)
        print("SAND SETTLING VELOCITY (Gemini Audit Challenge #2)")
        print("-" * 60)
        print(f"Sand grain diameter: {args.sand_diameter:.0f} microns ({d_sand*1000:.3f} mm)")
        print(f"Sand density:        {rho_sand:.0f} kg/m3 (quartz)")
        print(f"Settling velocity:   {v_sand:.6f} m/s = {v_sand*1000:.4f} mm/s")
        print(f"Settling rate:       {v_sand*86400:.2f} m/day")
        if v_sand < 0.001:
            print()
            print("*** WARNING: Sand settling velocity < 1 mm/s ***")
            print("Gravity-based solids separation is INEFFECTIVE at this viscosity.")
            print("Sand will be entrained in the viscous flow and carried through")
            print("the separator. Consider screen/mesh protection for PCP intake.")

    print()
    print("=" * 60)
    print("Sources: CGW 1978 (Stokes/H-R/Grace), SPE-136665 (foamy viscosity)")
    print("=" * 60)


if __name__ == "__main__":
    main()
