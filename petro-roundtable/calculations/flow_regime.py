#!/usr/bin/env python3
"""Flow regime predictor for inclined multiphase pipe flow.

Predicts flow regime using simplified Barnea (1987) transition criteria
with heavy oil corrections from Gokcal (SPE-102727). Calculates
superficial velocities and liquid holdup.

Sources:
  - Barnea (1987) Int J Multiphase Flow 13:1-12
  - Taitel & Dukler (1976) AIChE Journal 22(1):47-55
  - Beggs & Brill (1973) SPE-4007
  - Gokcal et al. (SPE-102727) high-viscosity corrections

Usage:
  python flow_regime.py --casing_id 196.9 --tubing_od 73.0 --liquid_rate 190 --gas_rate 1.9 --oil_viscosity 80000 --inclination 86
"""

import argparse
import math


def superficial_velocities(Q_l_bpd, Q_g_mscfd, A_m2, P_psi=150, T_F=75):
    """Calculate superficial gas and liquid velocities.

    Args:
        Q_l_bpd: liquid rate (bbl/d)
        Q_g_mscfd: gas rate (Mscf/d)
        A_m2: flow cross-section area (m2)
        P_psi: pressure (psi) for gas volume correction
        T_F: temperature (F) for gas volume correction
    Returns:
        v_sl (m/s), v_sg (m/s)
    """
    # Liquid: bbl/d to m3/s
    Q_l = Q_l_bpd * 1.84e-6  # 1 bbl/d = 1.84e-6 m3/s
    v_sl = Q_l / A_m2

    # Gas: Mscf/d at standard conditions to m3/s at downhole conditions
    Q_g_scf = Q_g_mscfd * 1000.0  # Mscf to scf
    Q_g_std_m3s = Q_g_scf * 0.0283168 / 86400.0  # scf/d to m3/s at STP
    # Correct for downhole P and T (ideal gas approximation)
    P_ratio = 14.7 / P_psi  # expand from downhole to standard
    T_ratio = (T_F + 460.0) / (60.0 + 460.0)
    Q_g_downhole = Q_g_std_m3s * P_ratio * T_ratio
    v_sg = Q_g_downhole / A_m2

    return v_sl, v_sg


def predict_regime_heavy_oil(v_sl, v_sg, mu_oil_cP, inclination_deg, D_m):
    """Predict flow regime with heavy oil corrections.

    At viscosities >600 cP (Gokcal SPE-102727):
    - Stratified flow disappears
    - Dispersed bubble flow disappears
    - Slug flow dominates the entire envelope
    - Churn flow only at very high gas rates

    Args:
        v_sl: superficial liquid velocity (m/s)
        v_sg: superficial gas velocity (m/s)
        mu_oil_cP: oil viscosity (cP)
        inclination_deg: from vertical (0=vertical, 90=horizontal)
        D_m: pipe/annulus diameter (m)
    Returns:
        regime (str), confidence (str), notes (str)
    """
    # Mixture velocity
    v_m = v_sl + v_sg
    # Input gas fraction (no-slip)
    lambda_g = v_sg / v_m if v_m > 0 else 0

    # Heavy oil regime (>600 cP per Gokcal)
    if mu_oil_cP > 600:
        # Stratified is impossible (Gokcal SPE-102727)
        # Dispersed bubble is impossible (Gokcal SPE-102727)

        if lambda_g < 0.02:
            return ("SINGLE-PHASE LIQUID",
                    "HIGH" if mu_oil_cP > 1000 else "MEDIUM",
                    "Negligible gas. Oil flows as single phase.")

        if lambda_g > 0.85:
            return ("ANNULAR / MIST",
                    "LOW (extrapolation)",
                    f"Very high GVF ({lambda_g*100:.0f}%). At {mu_oil_cP:,.0f} cP, "
                    "annular flow with viscous liquid film. No validated data at this viscosity.")

        # Churn threshold: Barnea uses alpha_s >= 0.52
        # At high viscosity, churn is suppressed — slug persists to higher gas rates
        if v_sg > 2.0 and lambda_g > 0.6:
            return ("CHURN",
                    "LOW (extrapolation)",
                    f"High gas velocity ({v_sg:.2f} m/s) with GVF {lambda_g*100:.0f}%. "
                    "Oscillatory flow likely. At high viscosity, churn may behave more like "
                    "aerated slug than true chaotic churn.")

        # Everything else is slug/intermittent at high viscosity
        slug_note = (
            f"Slug flow dominates at {mu_oil_cP:,.0f} cP (Gokcal SPE-102727). "
            f"Slugs are nearly pure liquid (holdup 0.92-0.98). "
            f"Slug frequency increases with viscosity. "
        )
        if mu_oil_cP > 6000:
            slug_note += (
                "WARNING: No validated flow regime data above 6,000 cP. "
                "This prediction is an extrapolation. The flow may be a "
                "continuous foamy viscous core rather than discrete slugs."
            )

        if inclination_deg > 80:
            slug_note += (
                f" At {inclination_deg:.0f} deg, near-horizontal slug/plug flow "
                "with liquid holdup approaching 1.0. Gas travels as elongated "
                "bubbles along the high side of the pipe."
            )

        return ("SLUG / INTERMITTENT",
                "MEDIUM" if mu_oil_cP < 6000 else "LOW (extrapolation)",
                slug_note)

    # Conventional oil regime (<600 cP) — simplified Barnea/Taitel-Dukler
    else:
        if inclination_deg > 70:  # near-horizontal
            if v_sg < 0.1 and v_sl < 0.1:
                return ("STRATIFIED SMOOTH", "MEDIUM",
                        "Low velocities, near-horizontal. Gravity-dominated.")
            elif v_sg < 3.0 and v_sl < 0.5:
                return ("STRATIFIED WAVY", "MEDIUM",
                        "Gas shear generates waves but no bridging.")
            elif lambda_g < 0.75:
                return ("SLUG / INTERMITTENT", "MEDIUM",
                        "Liquid slugs bridge the pipe alternating with gas pockets.")
            else:
                return ("ANNULAR", "MEDIUM",
                        "High gas velocity, liquid film on wall.")
        else:  # more vertical
            if lambda_g < 0.25:
                return ("BUBBLY", "MEDIUM",
                        "Low gas fraction, discrete bubbles in liquid.")
            elif lambda_g < 0.75:
                return ("SLUG / CHURN", "MEDIUM",
                        "Intermittent Taylor bubbles and liquid slugs.")
            else:
                return ("ANNULAR", "MEDIUM",
                        "Gas core with liquid film on wall.")


def beggs_brill_holdup(v_sl, v_sg, inclination_deg, D_m, mu_l_cP):
    """Simplified Beggs & Brill liquid holdup estimation.

    Uses the horizontal holdup correlation with inclination correction.
    Beggs & Brill 1973, SPE-4007.
    """
    v_m = v_sl + v_sg
    if v_m <= 0:
        return 1.0

    lambda_l = v_sl / v_m  # input liquid fraction (no-slip)

    # Froude number
    g = 9.81
    N_Fr = v_m**2 / (g * D_m)

    # Horizontal holdup (segregated flow correlation, Beggs & Brill Table 1)
    # H_L(0) = a * lambda_l^b / N_Fr^c
    # For segregated: a=0.98, b=0.4846, c=0.0868
    if lambda_l <= 0:
        return 0.0
    H_L_0 = 0.98 * lambda_l**0.4846 / max(N_Fr, 0.001)**0.0868
    H_L_0 = min(max(H_L_0, lambda_l), 1.0)  # bound between lambda_l and 1.0

    # Inclination correction (simplified)
    theta_rad = math.radians(90 - inclination_deg)  # convert to angle from horizontal
    # For upward inclined flow, holdup increases
    C = max(0, (1 - lambda_l) * math.log(max(0.001,
        0.011 * max(lambda_l, 0.01)**(-3.768) *
        max(v_sl, 0.001)**3.539 *
        max(N_Fr, 0.001)**(-1.614))))

    psi = 1.0 + C * (math.sin(1.8 * theta_rad) - 0.333 * math.sin(1.8 * theta_rad)**3)
    H_L = H_L_0 * psi
    H_L = min(max(H_L, 0.01), 1.0)

    return H_L


def main():
    parser = argparse.ArgumentParser(
        description="Flow regime predictor for inclined multiphase pipe flow"
    )
    parser.add_argument("--casing_id", type=float, required=True,
                        help="Casing inner diameter (mm)")
    parser.add_argument("--tubing_od", type=float, default=0,
                        help="Tubing outer diameter (mm), 0 for open casing")
    parser.add_argument("--liquid_rate", type=float, required=True,
                        help="Total liquid rate (bbl/d)")
    parser.add_argument("--gas_rate", type=float, required=True,
                        help="Gas rate (Mscf/d)")
    parser.add_argument("--oil_viscosity", type=float, default=80000,
                        help="Oil viscosity (cP), default 80000")
    parser.add_argument("--inclination", type=float, default=86,
                        help="Inclination from vertical (deg), default 86")
    parser.add_argument("--pressure", type=float, default=150,
                        help="Downhole pressure (psi), default 150")
    parser.add_argument("--temperature", type=float, default=75,
                        help="Downhole temperature (F), default 75")

    args = parser.parse_args()

    # Geometry
    D_casing = args.casing_id / 1000.0
    D_tubing = args.tubing_od / 1000.0
    if D_tubing > 0:
        D_H = D_casing - D_tubing
        A_flow = math.pi / 4.0 * (D_casing**2 - D_tubing**2)
        geom = f"Annulus: {args.casing_id:.1f} x {args.tubing_od:.1f} mm"
    else:
        D_H = D_casing
        A_flow = math.pi / 4.0 * D_casing**2
        geom = f"Open casing: {args.casing_id:.1f} mm"

    # Superficial velocities
    v_sl, v_sg = superficial_velocities(args.liquid_rate, args.gas_rate, A_flow,
                                         args.pressure, args.temperature)
    v_m = v_sl + v_sg
    lambda_g = v_sg / v_m if v_m > 0 else 0

    # Predict regime
    regime, confidence, notes = predict_regime_heavy_oil(
        v_sl, v_sg, args.oil_viscosity, args.inclination, D_H)

    # Liquid holdup
    H_L = beggs_brill_holdup(v_sl, v_sg, args.inclination, D_H, args.oil_viscosity)

    print("=" * 65)
    print("FLOW REGIME PREDICTOR")
    print("=" * 65)
    print(f"Geometry:            {geom}")
    print(f"Hydraulic diameter:  {D_H*1000:.1f} mm")
    print(f"Flow area:           {A_flow*1e4:.2f} cm2")
    print(f"Inclination:         {args.inclination:.1f} deg from vertical")
    print(f"Oil viscosity:       {args.oil_viscosity:,.0f} cP")
    print(f"Liquid rate:         {args.liquid_rate:.0f} bbl/d")
    print(f"Gas rate:            {args.gas_rate:.1f} Mscf/d")
    print(f"Downhole P:          {args.pressure:.0f} psi")
    print(f"Downhole T:          {args.temperature:.0f} F")
    print()
    print("-" * 65)
    print("SUPERFICIAL VELOCITIES")
    print("-" * 65)
    print(f"v_sl (liquid):       {v_sl:.5f} m/s ({v_sl*3.281:.5f} ft/s)")
    print(f"v_sg (gas):          {v_sg:.5f} m/s ({v_sg*3.281:.5f} ft/s)")
    print(f"v_m (mixture):       {v_m:.5f} m/s")
    print(f"Input gas fraction:  {lambda_g*100:.1f}%")
    print()
    print("-" * 65)
    print("PREDICTED FLOW REGIME")
    print("-" * 65)
    print(f"Regime:              {regime}")
    print(f"Confidence:          {confidence}")
    print(f"Liquid holdup (B&B): {H_L:.3f} ({H_L*100:.1f}%)")
    print()
    print(f"Notes: {notes}")

    # Separator implications
    print()
    print("-" * 65)
    print("SEPARATOR DESIGN IMPLICATIONS")
    print("-" * 65)
    if "SLUG" in regime:
        print("- Slug flow: separator must handle intermittent surges")
        print("- WhaleShark-type (liquid fallback) is designed for this regime")
        print("- Slug frequency increases with viscosity — expect frequent short slugs")
        if args.oil_viscosity > 6000:
            print("- At this viscosity, slugs are nearly pure liquid (holdup >0.92)")
            print("- Gas voids between slugs are short — separator acts on these voids")
    if "SINGLE" in regime:
        print("- No free gas present. Separator may not be needed.")
        print("- Check if foamy oil is producing (gas dispersed in oil, not free)")
    if "ANNULAR" in regime:
        print("- Gas core with liquid film. Separator must capture thin liquid film.")
    if "CHURN" in regime:
        print("- Chaotic flow with frequent reversals — WhaleShark designed for this")

    if args.oil_viscosity > 6000:
        print()
        print("*** EXTRAPOLATION WARNING ***")
        print(f"Oil viscosity ({args.oil_viscosity:,.0f} cP) exceeds all validated data (max 6,000 cP).")
        print("Flow regime prediction is an extrapolation. Validate with field data.")
        print("At >600 cP: stratified and dispersed bubble flows are impossible (Gokcal SPE-102727).")

    print()
    print("=" * 65)
    print("Sources: Barnea 1987, Taitel & Dukler 1976, Beggs & Brill 1973,")
    print("         Gokcal SPE-102727 (heavy oil corrections)")
    print("=" * 65)


if __name__ == "__main__":
    main()
