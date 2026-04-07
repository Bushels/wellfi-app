#!/usr/bin/env python3
"""
Nodal Analysis — IPR and VLP Calculations
Petro-Roundtable Calculation Script

Implements Vogel, Darcy, and simplified VLP models
for finding well operating points.

Usage:
    python nodal_analysis.py --mode vogel --pr 2500 --pb 2000 --q_test 500 --pwf_test 1800
    python nodal_analysis.py --mode darcy --pr 2500 --pi 0.5
    python nodal_analysis.py --mode vlp --pwh 100 --depth 2300 --tubing_id 3.5
    python nodal_analysis.py --mode operating_point --pr 2500 --pb 2000 --q_test 500 --pwf_test 1800 --pwh 100 --depth 2300 --tubing_id 3.5
    python nodal_analysis.py --help
"""

import argparse
import sys

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Install with: pip install numpy")
    sys.exit(1)


def vogel_ipr(pr, pb, q_test, pwf_test, num_points=20):
    """Vogel's IPR for solution gas drive (below bubble point)."""
    vogel_ratio = 1 - 0.2 * (pwf_test / pr) - 0.8 * (pwf_test / pr) ** 2
    if vogel_ratio <= 0:
        return {"error": "Invalid test data: Vogel ratio <= 0."}

    q_max = q_test / vogel_ratio

    pwf_values = np.linspace(0, pr, num_points)
    ipr_curve = []
    for pwf in pwf_values:
        q = q_max * (1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2)
        ipr_curve.append({"pwf_psi": round(float(pwf), 1), "rate_bpd": round(max(0, float(q)), 1)})

    return {
        "model": "Vogel",
        "reservoir_pressure_psi": pr,
        "absolute_open_flow_bpd": round(q_max, 1),
        "productivity_index_bpd_psi": round(q_max * 1.8 / pr, 3),
        "ipr_curve": ipr_curve,
    }


def darcy_ipr(pr, pi, num_points=20):
    """Darcy's law IPR for undersaturated oil (above bubble point)."""
    q_max = pi * pr
    pwf_values = np.linspace(0, pr, num_points)
    ipr_curve = [
        {"pwf_psi": round(float(pwf), 1), "rate_bpd": round(float(pi * (pr - pwf)), 1)}
        for pwf in pwf_values
    ]
    return {
        "model": "Darcy (linear)",
        "reservoir_pressure_psi": pr,
        "productivity_index_bpd_psi": pi,
        "absolute_open_flow_bpd": round(q_max, 1),
        "ipr_curve": ipr_curve,
    }


def simplified_vlp(pwh, depth, tubing_id, fluid_gradient=0.35, glr=0.0,
                    num_points=20, max_rate=5000.0):
    """Simplified VLP (hydrostatic + friction)."""
    d = tubing_id / 12  # inches to feet
    p_hydrostatic = fluid_gradient * depth

    if glr > 0:
        glr_correction = max(0.3, 1 - 0.0001 * glr)
        p_hydrostatic *= glr_correction

    rates = np.linspace(10, max_rate, num_points)
    vlp_curve = []
    for q in rates:
        area_ft2 = np.pi * (d / 2) ** 2
        q_ft3_s = q * 5.615 / 86400
        velocity = q_ft3_s / area_ft2
        f = 0.025
        friction_loss = f * (depth / d) * (velocity ** 2) / (2 * 32.174) * fluid_gradient / 0.433
        pwf = pwh + p_hydrostatic + friction_loss
        vlp_curve.append({"pwf_psi": round(float(pwf), 1), "rate_bpd": round(float(q), 1)})

    return {
        "wellhead_pressure_psi": pwh,
        "well_depth_ft": depth,
        "tubing_id_inches": tubing_id,
        "hydrostatic_pressure_psi": round(p_hydrostatic, 1),
        "vlp_curve": vlp_curve,
    }


def find_operating_point(ipr_result, vlp_result):
    """Find intersection of IPR and VLP curves."""
    ipr_rates = np.array([p["rate_bpd"] for p in ipr_result["ipr_curve"]])
    ipr_pwf = np.array([p["pwf_psi"] for p in ipr_result["ipr_curve"]])
    vlp_rates = np.array([p["rate_bpd"] for p in vlp_result["vlp_curve"]])
    vlp_pwf = np.array([p["pwf_psi"] for p in vlp_result["vlp_curve"]])

    min_rate = max(ipr_rates.min(), vlp_rates.min())
    max_rate = min(ipr_rates.max(), vlp_rates.max())
    if min_rate >= max_rate:
        return {"error": "No overlap between IPR and VLP curves."}

    common_rates = np.linspace(min_rate, max_rate, 200)
    ipr_interp = np.interp(common_rates, ipr_rates[::-1], ipr_pwf[::-1])
    vlp_interp = np.interp(common_rates, vlp_rates, vlp_pwf)

    diff = ipr_interp - vlp_interp
    sign_changes = np.where(np.diff(np.sign(diff)))[0]

    if len(sign_changes) == 0:
        return {"error": "No intersection found. Well may not flow naturally. Consider artificial lift."}

    idx = sign_changes[0]
    r1, r2 = common_rates[idx], common_rates[idx + 1]
    d1, d2 = diff[idx], diff[idx + 1]
    op_rate = r1 + (r2 - r1) * (-d1) / (d2 - d1)
    op_pwf = float(np.interp(op_rate, common_rates, vlp_interp))

    pr = ipr_result["reservoir_pressure_psi"]
    drawdown = pr - op_pwf
    aof = ipr_result["absolute_open_flow_bpd"]
    rate_pct = (op_rate / aof) * 100

    if rate_pct > 80:
        assessment = "Operating near AOF. Limited upside from tubing/choke changes."
    elif rate_pct > 50:
        assessment = "Good operating point. Moderate optimization potential."
    else:
        assessment = "Operating well below AOF. Significant rate potential with artificial lift."

    return {
        "operating_rate_bpd": round(float(op_rate), 1),
        "operating_pwf_psi": round(op_pwf, 1),
        "reservoir_pressure_psi": pr,
        "drawdown_psi": round(drawdown, 1),
        "drawdown_pct": round((drawdown / pr) * 100, 1),
        "rate_as_pct_of_aof": round(rate_pct, 1),
        "assessment": assessment,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Nodal Analysis — IPR and VLP Calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Vogel IPR:       python nodal_analysis.py --mode vogel --pr 2500 --pb 2000 --q_test 500 --pwf_test 1800
  Darcy IPR:       python nodal_analysis.py --mode darcy --pr 2500 --pi 0.5
  VLP:             python nodal_analysis.py --mode vlp --pwh 100 --depth 2300 --tubing_id 3.5
  Operating point: python nodal_analysis.py --mode operating_point --pr 2500 --pb 2000 --q_test 500 --pwf_test 1800 --pwh 100 --depth 2300 --tubing_id 3.5
        """
    )
    parser.add_argument("--mode", required=True,
                        choices=["vogel", "darcy", "vlp", "operating_point"],
                        help="Analysis mode")
    parser.add_argument("--pr", type=float, help="Reservoir pressure (psi)")
    parser.add_argument("--pb", type=float, help="Bubble point pressure (psi)")
    parser.add_argument("--q_test", type=float, help="Test rate (bpd)")
    parser.add_argument("--pwf_test", type=float, help="Test flowing BHP (psi)")
    parser.add_argument("--pi", type=float, help="Productivity index (bpd/psi)")
    parser.add_argument("--pwh", type=float, help="Wellhead pressure (psi)")
    parser.add_argument("--depth", type=float, help="Well TVD (ft)")
    parser.add_argument("--tubing_id", type=float, help="Tubing ID (inches)")
    parser.add_argument("--fluid_gradient", type=float, default=0.35,
                        help="Fluid gradient (psi/ft, default 0.35 for heavy oil)")
    parser.add_argument("--glr", type=float, default=0.0,
                        help="Gas-liquid ratio (scf/bbl, default 0)")

    args = parser.parse_args()

    if args.mode == "vogel":
        if not all([args.pr, args.pb, args.q_test, args.pwf_test]):
            parser.error("Vogel requires --pr, --pb, --q_test, --pwf_test")
        result = vogel_ipr(args.pr, args.pb, args.q_test, args.pwf_test)
        print("=== Vogel IPR ===\n")
        for k, v in result.items():
            if k != "ipr_curve":
                print(f"  {k}: {v}")
        print(f"\n  IPR Curve ({len(result['ipr_curve'])} points):")
        print(f"  {'Pwf (psi)':>12}  {'Rate (bpd)':>12}")
        for pt in result["ipr_curve"]:
            print(f"  {pt['pwf_psi']:>12.1f}  {pt['rate_bpd']:>12.1f}")

    elif args.mode == "darcy":
        if not all([args.pr, args.pi]):
            parser.error("Darcy requires --pr, --pi")
        result = darcy_ipr(args.pr, args.pi)
        print("=== Darcy IPR ===\n")
        for k, v in result.items():
            if k != "ipr_curve":
                print(f"  {k}: {v}")

    elif args.mode == "vlp":
        if not all([args.pwh, args.depth, args.tubing_id]):
            parser.error("VLP requires --pwh, --depth, --tubing_id")
        result = simplified_vlp(args.pwh, args.depth, args.tubing_id,
                                args.fluid_gradient, args.glr)
        print("=== Simplified VLP ===\n")
        for k, v in result.items():
            if k != "vlp_curve":
                print(f"  {k}: {v}")

    elif args.mode == "operating_point":
        if not all([args.pr, args.pb, args.q_test, args.pwf_test,
                     args.pwh, args.depth, args.tubing_id]):
            parser.error("Operating point requires all IPR + VLP parameters")
        ipr = vogel_ipr(args.pr, args.pb, args.q_test, args.pwf_test)
        vlp = simplified_vlp(args.pwh, args.depth, args.tubing_id,
                             args.fluid_gradient, args.glr)
        result = find_operating_point(ipr, vlp)
        print("=== Operating Point ===\n")
        for k, v in result.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
