#!/usr/bin/env python3
"""
Sand Control Screen Selection and Analysis
Petro-Roundtable Calculation Script

Implements Saucier, Coberly, and industry-standard criteria for
screen selection, gravel sizing, and erosional velocity calculation.

Usage:
    python sand_control.py --mode psd --d10 180 --d40 300 --d50 350 --d70 500 --d90 120
    python sand_control.py --mode psd --d10 180 --d40 300 --d50 350 --d70 500 --d90 120 --sagd --temp 220
    python sand_control.py --mode erosional --density 950 --c_factor 80 --pipe_id 4.5 --flow_rate 200
    python sand_control.py --help
"""

import argparse
import sys

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Install with: pip install numpy")
    sys.exit(1)


def um_to_mesh(um):
    """Convert microns to approximate US mesh size."""
    mesh_table = [
        (2000, 10), (1680, 12), (1410, 14), (1190, 16), (1000, 18),
        (841, 20), (707, 25), (595, 30), (500, 35), (420, 40),
        (354, 45), (297, 50), (250, 60), (210, 70), (177, 80),
        (149, 100), (125, 120), (105, 140), (88, 170), (74, 200),
        (63, 230), (53, 270), (44, 325), (37, 400),
    ]
    for size_um, mesh in mesh_table:
        if um >= size_um:
            return mesh
    return 400


def analyze_psd(d10, d40, d50, d70, d90, formation_temp_c=25.0, is_sagd=False):
    """Analyze PSD and recommend screen/gravel selection."""
    uc = d40 / d90

    if uc < 3:
        sorting = "uniform"
    elif uc < 5:
        sorting = "moderate"
    elif uc < 10:
        sorting = "non-uniform"
    else:
        sorting = "highly non-uniform"

    # Saucier criterion: gravel = 5-6x D50
    gravel_min_um = 5 * d50
    gravel_max_um = 6 * d50
    gravel_min_mesh = um_to_mesh(gravel_max_um)
    gravel_max_mesh = um_to_mesh(gravel_min_um)

    # Coberly criterion: slot width = D10
    screen_slot_um = d10

    thermal_factor = 1.0
    if is_sagd and formation_temp_c > 100:
        delta_t = formation_temp_c - 25
        thermal_factor = 1.0 + (0.0005 * delta_t)
        screen_slot_um = d10 * thermal_factor

    if uc <= 3:
        strategy = "standalone_screen"
        notes = (f"Uniform sand (UC={uc:.1f}). Standalone screen is viable. "
                 f"Wire-wrap or premium mesh screen with {screen_slot_um:.0f} um slots.")
    elif uc <= 5:
        strategy = "screen_or_gravel_pack"
        notes = (f"Moderately sorted (UC={uc:.1f}). Standalone screen possible but "
                 f"gravel pack provides better sand retention. Consider OHGP for horizontal wells.")
    elif uc <= 10:
        strategy = "gravel_pack_required"
        notes = (f"Non-uniform sand (UC={uc:.1f}). Gravel pack recommended. "
                 f"Standalone screen risks plugging from fines migration.")
    else:
        strategy = "gravel_pack_required"
        notes = (f"Highly non-uniform (UC={uc:.1f}). Gravel pack mandatory. "
                 f"Consider pre-packed screens or frac pack if permeability allows.")

    if is_sagd:
        notes += (f"\n  SAGD thermal correction: slot size increased by "
                  f"{(thermal_factor - 1) * 100:.1f}% for {formation_temp_c:.0f} degC.")

    return {
        "uniformity_coefficient": round(uc, 2),
        "sorting": sorting,
        "d10_um": round(d10, 1),
        "d50_um": round(d50, 1),
        "d90_um": round(d90, 1),
        "gravel_size_range_um": f"{round(gravel_min_um)}-{round(gravel_max_um)}",
        "gravel_mesh_range": f"{gravel_min_mesh}/{gravel_max_mesh}",
        "standalone_screen_slot_um": round(d10, 1),
        "sagd_adjusted_slot_um": round(screen_slot_um, 1) if is_sagd else None,
        "thermal_expansion_factor": round(thermal_factor, 4) if is_sagd else None,
        "recommended_strategy": strategy,
        "recommendation": notes,
    }


def erosional_velocity(density_kg_m3, c_factor=100.0, pipe_id=None, flow_rate=None):
    """Calculate erosional velocity per API RP 14E."""
    density_lb_ft3 = density_kg_m3 * 0.062428
    v_erosional_ft_s = c_factor / (density_lb_ft3 ** 0.5)
    v_erosional_m_s = v_erosional_ft_s * 0.3048

    result = {
        "c_factor": c_factor,
        "density_kg_m3": round(density_kg_m3, 1),
        "density_lb_ft3": round(density_lb_ft3, 2),
        "erosional_velocity_ft_s": round(v_erosional_ft_s, 2),
        "erosional_velocity_m_s": round(v_erosional_m_s, 2),
    }

    if pipe_id:
        area_ft2 = np.pi * (pipe_id / 2 / 12) ** 2
        max_rate_ft3_s = v_erosional_ft_s * area_ft2
        max_rate_m3_day = max_rate_ft3_s * 0.0283168 * 86400
        max_rate_bbl_day = max_rate_m3_day * 6.28981

        result["pipe_id_inches"] = pipe_id
        result["max_flow_rate_m3_day"] = round(max_rate_m3_day, 1)
        result["max_flow_rate_bbl_day"] = round(max_rate_bbl_day, 1)

        if flow_rate:
            utilization = (flow_rate / max_rate_m3_day) * 100
            result["actual_flow_rate_m3_day"] = round(flow_rate, 1)
            result["utilization_pct"] = round(utilization, 1)
            result["within_limit"] = utilization <= 100
            if utilization > 80:
                result["warning"] = f"At {utilization:.0f}% of erosional limit. Consider upsizing."

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Sand Control Screen Selection and Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  PSD analysis:      python sand_control.py --mode psd --d10 180 --d40 300 --d50 350 --d70 500 --d90 120
  PSD (SAGD):        python sand_control.py --mode psd --d10 180 --d40 300 --d50 350 --d70 500 --d90 120 --sagd --temp 220
  Erosional velocity: python sand_control.py --mode erosional --density 950 --c_factor 80 --pipe_id 4.5 --flow_rate 200
        """
    )
    parser.add_argument("--mode", required=True, choices=["psd", "erosional"],
                        help="Analysis mode")
    # PSD arguments
    parser.add_argument("--d10", type=float, help="D10 particle diameter (microns)")
    parser.add_argument("--d40", type=float, help="D40 particle diameter (microns)")
    parser.add_argument("--d50", type=float, help="D50 particle diameter (microns)")
    parser.add_argument("--d70", type=float, help="D70 particle diameter (microns)")
    parser.add_argument("--d90", type=float, help="D90 particle diameter (microns)")
    parser.add_argument("--sagd", action="store_true", help="Apply SAGD thermal correction")
    parser.add_argument("--temp", type=float, default=25.0,
                        help="Formation temperature (degC, default 25)")
    # Erosional velocity arguments
    parser.add_argument("--density", type=float, help="Mixture density (kg/m3)")
    parser.add_argument("--c_factor", type=float, default=100.0,
                        help="API RP 14E C factor (default 100)")
    parser.add_argument("--pipe_id", type=float, help="Pipe ID (inches)")
    parser.add_argument("--flow_rate", type=float, help="Actual flow rate (m3/day)")

    args = parser.parse_args()

    if args.mode == "psd":
        if not all([args.d10, args.d40, args.d50, args.d70, args.d90]):
            parser.error("PSD analysis requires --d10, --d40, --d50, --d70, --d90")
        result = analyze_psd(args.d10, args.d40, args.d50, args.d70, args.d90,
                             args.temp, args.sagd)
        print("=== PSD Analysis & Screen Selection ===\n")
        for k, v in result.items():
            if v is not None:
                print(f"  {k}: {v}")

    elif args.mode == "erosional":
        if not args.density:
            parser.error("Erosional velocity requires --density")
        result = erosional_velocity(args.density, args.c_factor, args.pipe_id, args.flow_rate)
        print("=== Erosional Velocity (API RP 14E) ===\n")
        for k, v in result.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
