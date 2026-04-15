#!/usr/bin/env python3
"""Critical gas velocity calculator using Nagoo equation (SPE-190921).

Calculates the critical gas velocity limit (onset of liquid flow reversal)
as an explicit function of diameter, inclination, and fluid properties.
No fudge factors — derived from Taylor instability + Wallis criterion.

Also calculates residence time vs coalescence time (Gemini audit challenge #3).

Sources:
  - Nagoo et al. (2018) SPE-190921
  - Kannan & Nagoo (2019) SPE-195893

Usage:
  python critical_velocity.py --casing_id 196.9 --tubing_od 73.0 --inclination 86 --oil_sg 0.99
  python critical_velocity.py --casing_id 196.9 --tubing_od 73.0 --inclination 86 --oil_sg 0.99 --liquid_rate 190 --gor 10 --distance_to_separator 15
"""

import argparse
import math


def nagoo_critical_velocity(rho_l, rho_g, sigma_gl, theta_deg, D_H):
    """Nagoo critical gas velocity equation (SPE-190921, Eq. 1).

    V_g,crit = [(rho_l - rho_g) / (1.88 * (rho_g * sigma_gl)^0.5)]
               * (g * cos(theta))
               * (D_H)^1.5

    Args:
        rho_l: liquid density (kg/m3)
        rho_g: gas density (kg/m3)
        sigma_gl: gas-liquid interfacial tension (N/m)
        theta_deg: inclination from vertical (degrees). 0=vertical, 90=horizontal.
        D_H: hydraulic diameter (m)
    Returns:
        critical gas velocity (m/s)
    """
    g = 9.81
    theta_rad = math.radians(theta_deg)

    term1 = (rho_l - rho_g) / (1.88 * math.sqrt(rho_g * sigma_gl))
    term2 = g * math.cos(theta_rad)
    term3 = D_H ** 1.5

    return term1 * term2 * term3


def hydraulic_diameter_annulus(D_outer, D_inner):
    """Hydraulic diameter for annular flow.
    D_H = D_outer - D_inner (for annulus, standard definition).
    """
    return D_outer - D_inner


def annular_area(D_outer, D_inner):
    """Cross-sectional area of annulus (m2)."""
    return math.pi / 4.0 * (D_outer**2 - D_inner**2)


def superficial_velocity(Q_m3s, A_m2):
    """Superficial velocity = volumetric flow rate / cross-section area."""
    return Q_m3s / A_m2


def residence_time_calc(distance_m, velocity_ms):
    """Residence time = distance / velocity."""
    if velocity_ms <= 0:
        return float('inf')
    return distance_m / velocity_ms


def main():
    parser = argparse.ArgumentParser(
        description="Critical gas velocity calculator (Nagoo SPE-190921)"
    )
    parser.add_argument("--casing_id", type=float, required=True,
                        help="Casing inner diameter (mm)")
    parser.add_argument("--tubing_od", type=float, default=0,
                        help="Tubing outer diameter (mm), 0 for open casing")
    parser.add_argument("--inclination", type=float, required=True,
                        help="Inclination from vertical (degrees). 0=vertical, 90=horizontal.")
    parser.add_argument("--oil_sg", type=float, default=0.99,
                        help="Oil specific gravity, default 0.99")
    parser.add_argument("--gas_sg", type=float, default=0.65,
                        help="Gas specific gravity (air=1.0), default 0.65 (methane)")
    parser.add_argument("--water_cut", type=float, default=0.0,
                        help="Water cut (fraction 0-1), default 0")
    parser.add_argument("--sigma", type=float, default=0.025,
                        help="Interfacial tension (N/m), default 0.025")
    parser.add_argument("--liquid_rate", type=float, default=None,
                        help="Liquid production rate (bbl/d) for residence time calc")
    parser.add_argument("--gor", type=float, default=None,
                        help="Gas-oil ratio (scf/bbl) for gas rate calc")
    parser.add_argument("--distance_to_separator", type=float, default=None,
                        help="Distance from perforations to separator (m) for residence time calc")

    args = parser.parse_args()

    # Convert units
    D_casing = args.casing_id / 1000.0  # mm to m
    D_tubing = args.tubing_od / 1000.0  # mm to m
    rho_l = args.oil_sg * 1000.0  # SG to kg/m3 (approximate)
    rho_g = args.gas_sg * 1.225  # SG relative to air density at STP
    if args.water_cut > 0:
        rho_l = args.water_cut * 1000.0 + (1 - args.water_cut) * args.oil_sg * 1000.0

    # Hydraulic diameter
    if D_tubing > 0:
        D_H = hydraulic_diameter_annulus(D_casing, D_tubing)
        A_flow = annular_area(D_casing, D_tubing)
        geometry = f"Annulus: {args.casing_id:.1f}mm casing x {args.tubing_od:.1f}mm tubing"
    else:
        D_H = D_casing
        A_flow = math.pi / 4.0 * D_casing**2
        geometry = f"Open casing: {args.casing_id:.1f}mm ID"

    print("=" * 65)
    print("CRITICAL GAS VELOCITY CALCULATOR (Nagoo SPE-190921)")
    print("=" * 65)
    print(f"Geometry:         {geometry}")
    print(f"Hydraulic dia:    {D_H*1000:.1f} mm ({D_H:.4f} m)")
    print(f"Flow area:        {A_flow*1e4:.2f} cm2 ({A_flow:.6f} m2)")
    print(f"Inclination:      {args.inclination:.1f} deg from vertical")
    print(f"cos(theta):       {math.cos(math.radians(args.inclination)):.4f}")
    print(f"Liquid density:   {rho_l:.1f} kg/m3")
    print(f"Gas density:      {rho_g:.3f} kg/m3")
    print(f"IFT:              {args.sigma:.4f} N/m")
    print()

    # Critical velocity
    v_crit = nagoo_critical_velocity(rho_l, rho_g, args.sigma, args.inclination, D_H)

    print("-" * 65)
    print("CRITICAL GAS VELOCITY")
    print("-" * 65)
    print(f"V_g,crit:         {v_crit:.2f} m/s ({v_crit*3.281:.2f} ft/s)")
    print()

    # Compare at different inclinations
    print("Sensitivity to inclination:")
    for theta in [0, 30, 45, 60, 75, 80, 85, 86, 88, 90]:
        v = nagoo_critical_velocity(rho_l, rho_g, args.sigma, theta, D_H)
        marker = " <-- YOUR WELL" if theta == round(args.inclination) else ""
        print(f"  {theta:3d} deg: {v:8.2f} m/s ({v*3.281:8.2f} ft/s)  cos={math.cos(math.radians(theta)):.4f}{marker}")

    print()
    print("Sensitivity to diameter (at your inclination):")
    for D_label, D_val in [("5.5\" casing (ID=4.95\")", 0.1257),
                            ("7\" casing (ID=6.28\")", 0.1595),
                            ("8-5/8\" casing (ID=7.92\")", D_casing),
                            ("8-5/8\" annulus", D_H)]:
        v = nagoo_critical_velocity(rho_l, rho_g, args.sigma, args.inclination, D_val)
        print(f"  {D_label:35s}: {v:8.2f} m/s ({v*3.281:8.2f} ft/s)")

    # Extrapolation warning
    print()
    print("-" * 65)
    print("EXTRAPOLATION WARNING")
    print("-" * 65)
    print("Nagoo's equation was derived and validated for conventional fluids")
    print("(water, light oil, gas-condensate). At viscosities >6,000 cP,")
    print("viscous forces may alter interfacial dynamics. Results at 80,000 cP")
    print("are first-principles extrapolations. Validate with field data.")
    print("(Gemini Audit Challenge #5)")

    # Residence time vs coalescence (Gemini audit challenge #3)
    if args.liquid_rate and args.distance_to_separator:
        Q_liquid = args.liquid_rate * 1.84e-6  # bbl/d to m3/s
        v_liquid = superficial_velocity(Q_liquid, A_flow)
        t_residence = residence_time_calc(args.distance_to_separator, v_liquid)
        t_coalescence_min = 10 * 60  # 10 minutes (low end of Maini's range)
        t_coalescence_max = 20 * 60  # 20 minutes (high end)

        print()
        print("-" * 65)
        print("RESIDENCE TIME vs COALESCENCE (Gemini Audit Challenge #3)")
        print("-" * 65)
        print(f"Liquid rate:      {args.liquid_rate:.0f} bbl/d ({Q_liquid*1e6:.1f} cc/s)")
        print(f"Annular velocity: {v_liquid*1000:.2f} mm/s ({v_liquid:.5f} m/s)")
        print(f"Distance to sep:  {args.distance_to_separator:.1f} m")
        print(f"Residence time:   {t_residence:.0f} s ({t_residence/60:.1f} min)")
        print(f"Coalescence time: {t_coalescence_min/60:.0f}-{t_coalescence_max/60:.0f} min (Maini 1999)")
        print()

        if t_residence > t_coalescence_max:
            print("RESULT: Residence time EXCEEDS coalescence time.")
            print("Gas should be mostly coalesced by the time it reaches the separator.")
            print("Separator can work on free gas / large bubbles.")
        elif t_residence > t_coalescence_min:
            print("RESULT: Residence time is in the coalescence range.")
            print("Partial coalescence expected. Separator will see a mix of")
            print("free gas and dispersed foamy oil.")
        else:
            print("*** WARNING: Residence time LESS THAN coalescence time ***")
            print("Fluid arrives at separator as STABLE FOAM.")
            print("Separator may act as a pipe — no effective separation.")
            print("Consider: (1) increase distance, (2) accept gas at PCP intake,")
            print("(3) add foam-breaking mechanism upstream.")

    print()
    print("=" * 65)
    print("Source: Nagoo et al. 2018, SPE-190921 | Maini 1999, SPE-56541")
    print("=" * 65)


if __name__ == "__main__":
    main()
