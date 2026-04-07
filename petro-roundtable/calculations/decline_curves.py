#!/usr/bin/env python3
"""
Decline Curve Analysis — Arps Models
Petro-Roundtable Calculation Script

Implements exponential, hyperbolic, and harmonic decline models
with fitting and EUR estimation.

Usage:
    python decline_curves.py --mode arps_fit --qi 100 --di 0.15 --b 1.2 --time_months 60
    python decline_curves.py --mode eur --qi 350 --di 0.05 --b 0.8 --econ_limit 10
    python decline_curves.py --mode forecast --qi 350 --di 0.05 --b 0.8 --time_months 120
    python decline_curves.py --help
"""

import argparse
import sys

try:
    import numpy as np
    from scipy.optimize import curve_fit
except ImportError:
    print("ERROR: numpy and scipy required. Install with: pip install numpy scipy")
    sys.exit(1)


def arps_decline(t, qi, di, b):
    """Arps generalized decline: q(t) = qi / (1 + b*di*t)^(1/b)"""
    if b == 0:
        return qi * np.exp(-di * t)
    else:
        return qi / (1 + b * di * t) ** (1 / b)


def arps_cumulative(t, qi, di, b):
    """Cumulative production from Arps decline."""
    if b == 0:
        return (qi / di) * (1 - np.exp(-di * t))
    elif b == 1:
        return (qi / di) * np.log(1 + di * t)
    else:
        q_t = arps_decline(t, qi, di, b)
        return (qi ** b) / ((1 - b) * di) * (qi ** (1 - b) - q_t ** (1 - b))


def arps_fit(time_months, rate_bpd, b_range=(0.0, 2.0)):
    """Fit Arps decline model to production data."""
    t = np.array(time_months, dtype=float)
    q = np.array(rate_bpd, dtype=float)

    mask = q > 0
    t = t[mask]
    q = q[mask]

    if len(t) < 3:
        return {"error": "Need at least 3 non-zero data points for decline fitting."}

    qi_guess = float(q[0])
    di_guess = 0.05
    b_guess = 0.5

    try:
        popt, pcov = curve_fit(
            arps_decline, t, q,
            p0=[qi_guess, di_guess, b_guess],
            bounds=([0, 0.001, b_range[0]], [qi_guess * 3, 1.0, b_range[1]]),
            maxfev=10000,
        )
        qi_fit, di_fit, b_fit = popt
    except RuntimeError:
        try:
            def exp_decline(t, qi, di):
                return qi * np.exp(-di * t)
            popt, _ = curve_fit(exp_decline, t, q, p0=[qi_guess, di_guess])
            qi_fit, di_fit = popt
            b_fit = 0.0
        except RuntimeError:
            return {"error": "Could not fit decline curve. Check data quality."}

    q_predicted = arps_decline(t, qi_fit, di_fit, b_fit)
    ss_res = np.sum((q - q_predicted) ** 2)
    ss_tot = np.sum((q - np.mean(q)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    if b_fit < 0.05:
        decline_type = "exponential"
    elif 0.95 < b_fit < 1.05:
        decline_type = "harmonic"
    else:
        decline_type = "hyperbolic"

    di_annual = di_fit * 12
    if b_fit == 0:
        de_annual = 1 - np.exp(-di_annual)
    else:
        de_annual = 1 - (1 + b_fit * di_annual) ** (-1 / b_fit)

    return {
        "qi_bpd": round(float(qi_fit), 1),
        "di_monthly": round(float(di_fit), 5),
        "di_annual_nominal": round(float(di_annual), 4),
        "de_annual_effective": round(float(de_annual), 4),
        "b_exponent": round(float(b_fit), 3),
        "decline_type": decline_type,
        "r_squared": round(float(r_squared), 4),
        "data_points_used": len(t),
    }


def eur(qi_bpd, di_monthly, b_exponent, economic_limit_bpd=5.0,
        max_months=600, cumulative_to_date_bbl=0.0):
    """Estimate EUR from decline parameters."""
    t = np.arange(1, max_months + 1, dtype=float)
    q = arps_decline(t, qi_bpd, di_monthly, b_exponent)

    below_limit = np.where(q < economic_limit_bpd)[0]
    econ_life_months = int(below_limit[0]) if len(below_limit) > 0 else max_months

    t_econ = t[:econ_life_months]
    cum_prod = arps_cumulative(t_econ, qi_bpd, di_monthly, b_exponent)

    total_cum_bbl = float(cum_prod[-1]) * 30.44 if len(cum_prod) > 0 else 0
    eur_bbl = total_cum_bbl + cumulative_to_date_bbl

    return {
        "eur_bbl": round(eur_bbl, 0),
        "eur_mbbl": round(eur_bbl / 1000, 1),
        "remaining_reserves_bbl": round(total_cum_bbl, 0),
        "remaining_reserves_mbbl": round(total_cum_bbl / 1000, 1),
        "cumulative_to_date_bbl": round(cumulative_to_date_bbl, 0),
        "economic_limit_bpd": economic_limit_bpd,
        "economic_life_months": econ_life_months,
        "economic_life_years": round(econ_life_months / 12, 1),
    }


def forecast(qi_bpd, di_monthly, b_exponent, time_months):
    """Generate production forecast from decline parameters."""
    t = np.arange(1, time_months + 1, dtype=float)
    q = arps_decline(t, qi_bpd, di_monthly, b_exponent)
    cum = arps_cumulative(t, qi_bpd, di_monthly, b_exponent)

    print(f"{'Month':>6}  {'Rate (bpd)':>12}  {'Cum Prod (bbl)':>16}")
    print("-" * 38)
    for i in range(0, len(t), max(1, len(t) // 20)):
        print(f"{int(t[i]):>6}  {q[i]:>12.1f}  {cum[i] * 30.44:>16.0f}")

    print(f"\nFinal rate at month {time_months}: {q[-1]:.1f} bpd")
    print(f"Total cumulative: {cum[-1] * 30.44:,.0f} bbl ({cum[-1] * 30.44 / 1000:,.1f} Mbbl)")


def main():
    parser = argparse.ArgumentParser(
        description="Decline Curve Analysis — Arps Models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Forecast:  python decline_curves.py --mode forecast --qi 350 --di 0.05 --b 0.8 --time_months 120
  EUR:       python decline_curves.py --mode eur --qi 350 --di 0.05 --b 0.8 --econ_limit 10
  Demo fit:  python decline_curves.py --mode demo_fit
        """
    )
    parser.add_argument("--mode", required=True,
                        choices=["forecast", "eur", "demo_fit"],
                        help="Analysis mode")
    parser.add_argument("--qi", type=float, help="Initial rate (bpd)")
    parser.add_argument("--di", type=float, help="Monthly nominal decline rate")
    parser.add_argument("--b", type=float, help="Arps b exponent")
    parser.add_argument("--time_months", type=int, default=60,
                        help="Forecast period in months (default 60)")
    parser.add_argument("--econ_limit", type=float, default=5.0,
                        help="Economic limit rate in bpd (default 5.0)")
    parser.add_argument("--cum_to_date", type=float, default=0.0,
                        help="Cumulative production to date in bbl")

    args = parser.parse_args()

    if args.mode == "demo_fit":
        months = list(range(1, 25))
        rates = [350, 320, 295, 270, 250, 235, 220, 208, 197, 187,
                 178, 170, 162, 155, 149, 143, 137, 132, 127, 123,
                 119, 115, 111, 108]

        print("=== Arps Decline Fit (Demo Data — Clearwater Heavy Oil) ===\n")
        fit = arps_fit(months, rates)
        for k, v in fit.items():
            print(f"  {k}: {v}")

        print("\n=== EUR Estimate ===\n")
        eur_result = eur(
            qi_bpd=fit["qi_bpd"],
            di_monthly=fit["di_monthly"],
            b_exponent=fit["b_exponent"],
            economic_limit_bpd=10,
            cumulative_to_date_bbl=sum(r * 30.44 for r in rates),
        )
        for k, v in eur_result.items():
            print(f"  {k}: {v}")
        return

    if args.qi is None or args.di is None or args.b is None:
        parser.error("--qi, --di, and --b are required for forecast and eur modes")

    if args.mode == "forecast":
        print(f"=== Production Forecast ===")
        print(f"  qi={args.qi} bpd, di={args.di}/month, b={args.b}\n")
        forecast(args.qi, args.di, args.b, args.time_months)

    elif args.mode == "eur":
        print(f"=== EUR Estimate ===")
        print(f"  qi={args.qi} bpd, di={args.di}/month, b={args.b}")
        print(f"  Economic limit: {args.econ_limit} bpd\n")
        result = eur(args.qi, args.di, args.b, args.econ_limit,
                     cumulative_to_date_bbl=args.cum_to_date)
        for k, v in result.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
