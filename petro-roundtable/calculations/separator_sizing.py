#!/usr/bin/env python3
"""Downhole separator sizing calculator.

Sizes a downhole gas-liquid separator for heavy oil wells using:
- McCoy (1998) conventional sizing method (with heavy oil corrections)
- WhaleShark design principles (Saponja 2021)
- Stokes' law bubble rise (with foamy oil viscosity correction)
- Residence time vs coalescence assessment

Sources:
  - McCoy & Podio (1998) "Improved Downhole Gas Separators"
  - Saponja et al. (2021) SWPSC "WhaleShark"
  - Alshmakhy & Maini (2010) SPE-136665 (foamy viscosity)
  - Clift, Grace & Weber (1978) (Stokes' law)
  - Maini (1999) SPE-56541 (coalescence time)

Usage:
  python separator_sizing.py --casing_id 196.9 --liquid_rate 190 --gor 10 --oil_viscosity 80000 --inclination 86
"""

import argparse
import math


def mccoy_capacity(A_annular_sqin, oil_viscosity_cP):
    """McCoy sizing rule: 50 BPD per sq-in at <10 cP.
    Corrected for viscosity using Stokes' law scaling.

    At high viscosity, bubble rise velocity drops as 1/mu.
    McCoy's rule assumes 6 in/s (15 cm/s) bubble rise in <10 cP oil.

    Args:
        A_annular_sqin: annular area (sq inches)
        oil_viscosity_cP: oil viscosity (cP)
    Returns:
        capacity_bpd: separator liquid capacity (bbl/d)
        correction_factor: viscosity correction applied
    """
    base_capacity = A_annular_sqin * 50.0  # BPD at <10 cP

    # Viscosity correction: capacity scales as 1/mu (Stokes)
    # Base assumes ~5 cP reference viscosity
    mu_ref = 5.0  # cP
    correction = mu_ref / oil_viscosity_cP
    corrected_capacity = base_capacity * correction

    return corrected_capacity, correction


def stokes_bubble_rise(rho_l, rho_g, mu_Pa_s, d_m):
    """Stokes' law bubble rise velocity."""
    g = 9.81
    return (1.0 / 18.0) * (rho_l - rho_g) * g * d_m**2 / mu_Pa_s


def required_separator_length(v_liquid_ms, v_bubble_ms, D_casing_m, inclination_deg):
    """Estimate minimum separator length for gravity-based separation.

    Length = distance liquid must travel for a bubble to rise across
    the pipe diameter, accounting for inclination.

    For liquid fallback (WhaleShark): different calculation.
    """
    if v_bubble_ms <= 0:
        return float('inf')

    # Effective vertical component
    cos_theta = math.cos(math.radians(inclination_deg))
    v_rise_axial = v_bubble_ms * cos_theta  # axial component of rise

    if v_rise_axial <= 0:
        return float('inf')

    # Time for bubble to traverse pipe diameter
    t_traverse = D_casing_m / v_bubble_ms  # seconds

    # Distance liquid travels in that time
    L_min = v_liquid_ms * t_traverse

    return L_min


def main():
    parser = argparse.ArgumentParser(
        description="Downhole separator sizing calculator"
    )
    parser.add_argument("--casing_id", type=float, required=True,
                        help="Casing inner diameter (mm)")
    parser.add_argument("--tubing_od", type=float, default=73.0,
                        help="Tubing outer diameter (mm), default 73.0 (2-7/8 EUE)")
    parser.add_argument("--liquid_rate", type=float, required=True,
                        help="Total liquid rate (bbl/d)")
    parser.add_argument("--gor", type=float, default=10,
                        help="Gas-oil ratio (scf/bbl), default 10")
    parser.add_argument("--oil_viscosity", type=float, default=80000,
                        help="Dead oil viscosity (cP), default 80000")
    parser.add_argument("--inclination", type=float, default=86,
                        help="Inclination from vertical (deg), default 86")
    parser.add_argument("--oil_density", type=float, default=997,
                        help="Oil density (kg/m3), default 997")
    parser.add_argument("--gas_density", type=float, default=0.8,
                        help="Gas density (kg/m3), default 0.8")
    parser.add_argument("--separator_type", type=str, default="all",
                        choices=["poorboy", "packer", "whaleshark", "all"],
                        help="Separator type to evaluate")

    args = parser.parse_args()

    # Geometry
    D_cas = args.casing_id / 1000.0  # m
    D_tub = args.tubing_od / 1000.0  # m
    A_annulus = math.pi / 4.0 * (D_cas**2 - D_tub**2)
    A_annulus_sqin = A_annulus / 6.452e-4  # m2 to sq-in
    D_H = D_cas - D_tub

    # Viscosity correction for foamy oil (SPE-136665)
    mu_dead = args.oil_viscosity
    mu_live = mu_dead * 0.56  # foamy oil at GVF <40% = live oil
    mu_live_Pa_s = mu_live / 1000.0

    # Bubble rise
    d_bubble = 0.002  # 2mm typical dispersed bubble
    v_bubble_dead = stokes_bubble_rise(args.oil_density, args.gas_density,
                                        mu_dead / 1000.0, d_bubble)
    v_bubble_live = stokes_bubble_rise(args.oil_density, args.gas_density,
                                        mu_live_Pa_s, d_bubble)

    # Liquid velocity in annulus
    Q_liquid = args.liquid_rate * 1.84e-6  # bbl/d to m3/s
    v_liquid = Q_liquid / A_annulus

    # Gas rate
    Q_gas_scfd = args.liquid_rate * args.gor  # scf/d
    Q_gas_mscfd = Q_gas_scfd / 1000.0

    # Residence time
    distance_to_sep = 15.0  # m (default assumption)
    t_residence = distance_to_sep / v_liquid if v_liquid > 0 else float('inf')

    print("=" * 70)
    print("DOWNHOLE SEPARATOR SIZING CALCULATOR")
    print("=" * 70)
    print(f"Casing ID:           {args.casing_id:.1f} mm ({D_cas*1000:.1f} mm)")
    print(f"Tubing OD:           {args.tubing_od:.1f} mm")
    print(f"Annular area:        {A_annulus_sqin:.2f} sq-in ({A_annulus*1e4:.2f} cm2)")
    print(f"Liquid rate:         {args.liquid_rate:.0f} bbl/d")
    print(f"GOR:                 {args.gor:.0f} scf/bbl")
    print(f"Gas rate:            {Q_gas_mscfd:.2f} Mscf/d")
    print(f"Inclination:         {args.inclination:.0f} deg from vertical")
    print(f"Dead oil viscosity:  {mu_dead:,.0f} cP")
    print(f"Live oil viscosity:  {mu_live:,.0f} cP (SPE-136665 correction)")
    print(f"Annular liquid vel:  {v_liquid*1000:.2f} mm/s ({v_liquid:.5f} m/s)")
    print()

    # McCoy conventional sizing
    print("=" * 70)
    print("METHOD 1: McCOY CONVENTIONAL SIZING (Bubble Rise Governed)")
    print("=" * 70)

    cap_std, _ = mccoy_capacity(A_annulus_sqin, 5.0)
    cap_dead, corr_dead = mccoy_capacity(A_annulus_sqin, mu_dead)
    cap_live, corr_live = mccoy_capacity(A_annulus_sqin, mu_live)

    print(f"Standard capacity (<10 cP):      {cap_std:,.1f} bbl/d")
    print(f"Corrected for dead oil ({mu_dead:,.0f} cP): {cap_dead:.4f} bbl/d (correction: {corr_dead:.2e})")
    print(f"Corrected for live oil ({mu_live:,.0f} cP): {cap_live:.4f} bbl/d (correction: {corr_live:.2e})")
    print()
    print(f"Your liquid rate:    {args.liquid_rate:.0f} bbl/d")
    print(f"Required capacity:   {args.liquid_rate:.0f} bbl/d")
    print()
    if cap_live < args.liquid_rate:
        print("*** CONVENTIONAL SEPARATOR CANNOT WORK ***")
        print(f"Even with live oil correction, gravity-based bubble separation")
        print(f"capacity ({cap_live:.4f} bbl/d) is {args.liquid_rate/cap_live:.0f}x below")
        print(f"required ({args.liquid_rate:.0f} bbl/d). Bubble rise is too slow.")
        print(f"Must use liquid-fallback mechanism (WhaleShark-type).")
    print()
    print(f"2mm bubble rise (dead oil): {v_bubble_dead*1000:.4f} mm/s = {v_bubble_dead*86400:.2f} m/day")
    print(f"2mm bubble rise (live oil): {v_bubble_live*1000:.4f} mm/s = {v_bubble_live*86400:.2f} m/day")

    # WhaleShark approach
    print()
    print("=" * 70)
    print("METHOD 2: WHALESHARK APPROACH (Liquid Fallback Governed)")
    print("=" * 70)
    print()
    print("The WhaleShark separator does NOT rely on bubble rise velocity.")
    print("It captures liquid that falls backward during slug/churn flow.")
    print()
    print("Key design parameters (from Saponja 2021 SWPSC):")
    print(f"  Separator length:     18 ft (5.5 m)")
    print(f"  Separator OD:         3.5 in (35 series) for 5.5 in casing")
    print(f"                        Larger series needed for 8-5/8 in casing")
    print(f"  Separation region:    Eccentric 'no annulus' (A3 > A2 > A1)")
    print(f"  Intake:               Upward-facing collector (captures fallback)")
    print(f"  Gas venting:          Radially + up casing annulus")
    print(f"  Solids:               Gravity/momentum weir + mud joint sump")
    print()

    # Assess viability at this viscosity and inclination
    cos_theta = math.cos(math.radians(args.inclination))
    print("VIABILITY ASSESSMENT for your well:")
    print(f"  cos({args.inclination} deg) = {cos_theta:.4f}")
    print(f"  Axial gravity:     {cos_theta*9.81:.3f} m/s2 ({cos_theta*100:.1f}% of full gravity)")
    print()

    if args.inclination > 80:
        print("  *** CONCERN: Inclination exceeds WhaleShark's tested range (80 deg) ***")
        print("  WhaleShark was tested to 80 deg for gas separation.")
        print(f"  Your well at {args.inclination} deg is beyond validated range.")
        print("  Liquid fallback velocity is reduced by cos(theta) factor.")
        print("  Recommend: field trial with WellFi monitoring to validate.")
        print()

    if args.oil_viscosity > 10000:
        print("  *** CONCERN: Viscosity exceeds all separator test data ***")
        print(f"  No separator has been tested above ~100 cP oil (SPE-49053).")
        print(f"  At {args.oil_viscosity:,.0f} cP, liquid fallback rate is unknown.")
        print("  Gemini Audit Challenge #1: liquid may not fall back at all")
        print("  due to wall friction and viscous drag dominating gravity.")
        print()

    # Coalescence assessment
    print("-" * 70)
    print("COALESCENCE ASSESSMENT (Gemini Audit Challenge #3)")
    print("-" * 70)
    print(f"  Annular liquid velocity: {v_liquid*1000:.2f} mm/s")
    print(f"  Distance to separator:   {distance_to_sep:.0f} m (assumed)")
    print(f"  Residence time:          {t_residence:.0f} s ({t_residence/60:.1f} min)")
    print(f"  Coalescence time:        10-20 min (Maini 1999)")
    print()
    if t_residence > 20 * 60:
        print("  GOOD: Residence time exceeds coalescence range.")
        print("  Gas should be mostly free by the time it reaches separator.")
    elif t_residence > 10 * 60:
        print("  MARGINAL: Residence time in coalescence range.")
        print("  Mix of free gas and dispersed foam at separator.")
    else:
        print("  *** POOR: Residence time below coalescence range ***")
        print("  Fluid arrives as stable foam. Consider increasing distance.")

    # Sand assessment (Gemini challenge #2)
    print()
    print("-" * 70)
    print("SAND SEPARATION ASSESSMENT (Gemini Audit Challenge #2)")
    print("-" * 70)
    d_sand = 120e-6  # 120 micron typical Bluesky
    v_sand = (1.0/18.0) * (2650 - args.oil_density) * 9.81 * d_sand**2 / mu_live_Pa_s
    print(f"  Sand grain:       120 micron (Bluesky D50)")
    print(f"  Settling velocity: {v_sand*1000:.4f} mm/s ({v_sand*86400:.2f} m/day)")
    print(f"  Flow velocity:     {v_liquid*1000:.2f} mm/s")
    ratio = v_liquid / v_sand if v_sand > 0 else float('inf')
    print(f"  Flow/settling ratio: {ratio:.0f}x")
    print()
    if ratio > 100:
        print("  *** GRAVITY SOLIDS SEPARATION IS INEFFECTIVE ***")
        print("  Sand is fully entrained at this viscosity.")
        print("  Recommend: screen/mesh at PCP intake as backup.")
        print("  Accept that CHOPS sand production passes through separator.")
    if args.inclination > 65:
        print(f"  *** Inclination ({args.inclination} deg) exceeds solids angle of repose (65 deg) ***")
        print("  Sand cannot slide into sump by gravity alone.")

    # Separator type comparison
    print()
    print("=" * 70)
    print("SEPARATOR TYPE COMPARISON FOR YOUR WELL")
    print("=" * 70)
    print()
    print(f"| Criterion                  | Poor-Boy  | Packer    | WhaleShark |")
    print(f"|----------------------------|-----------|-----------|------------|")
    print(f"| Works at {args.oil_viscosity/1000:.0f}k cP?          | NO        | NO        | MAYBE      |")
    print(f"| Works at {args.inclination} deg?             | NO (>80)  | NO (>80)  | UNTESTED   |")
    print(f"| Handles slug flow?         | POOR      | POOR      | DESIGNED   |")
    print(f"| Handles sand?              | MODERATE  | RISK      | MODERATE   |")
    print(f"| Packerless (low risk)?     | YES       | NO        | YES        |")
    print(f"| Liquid fallback mechanism? | NO        | NO        | YES        |")
    print(f"| Field-proven in heavy oil? | LIMITED   | LIMITED   | CHARLIE LK |")
    print()
    print("RECOMMENDATION: WhaleShark-type is the only viable approach,")
    print("but it has NOT been validated at this viscosity or inclination.")
    print("Design as a field trial with WellFi P/T monitoring to assess")
    print("separator performance in real-time.")

    print()
    print("=" * 70)
    print("Sources: McCoy 1998, Saponja 2021, SPE-136665, CGW 1978, SPE-56541")
    print("=" * 70)


if __name__ == "__main__":
    main()
