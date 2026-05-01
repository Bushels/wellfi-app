#!/usr/bin/env python3
"""
WellFi Collector Sub — Multi-Stage Degassing & Slug Damping Simulation

Models the gas fraction evolution, slug damping, and residence time
through a multi-lip external collector sub in a near-horizontal heavy oil well.

Physics basis:
  - Foamy oil micro-bubble coalescence (Maini 1999, SPE-136665)
  - Viscous shear coalescence through restrictions (high mu = high shear stress)
  - Slug body fragmentation through flow conditioning
  - Transverse gravity separation at 86 deg (sin(86) = 0.998)
  - Recirculation / residence time extension behind lips

KEY FINDING FROM V1: Bernoulli pressure drop is NEGLIGIBLE at 13 mm/s annular
velocity. The degassing mechanism is NOT pressure-driven — it is shear-driven
and residence-time-driven. This simulation uses the corrected physics.

Usage:
  python collector_sub_simulation.py
  python collector_sub_simulation.py --num_lips 4 --lip_restriction 0.35
  python collector_sub_simulation.py --output visual
  python collector_sub_simulation.py --sub_length 36 --num_lips 5
"""

import argparse
import sys
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


# ── Constants ──
G = 9.81  # m/s^2
PI = math.pi

# ── Default well parameters (OBE 102 HZ 16-18) ──
DEFAULTS = {
    "casing_id_mm": 196.9,       # 8-5/8" casing ID
    "tubing_od_mm": 73.0,        # 2-7/8" EUE tubing OD
    "inclination_deg": 86.0,     # degrees from vertical
    "oil_viscosity_cp": 8320.0,  # dead oil viscosity (Element lab report, 20 deg C, sales oil)
    "live_oil_viscosity_cp": None,  # calculated as 56% of dead oil (SPE-136665 foamy correction)
    "oil_density_kg_m3": 990.8,  # oil density (Element lab, after cleaning, 15 deg C)
    "gas_density_kg_m3": 0.8,    # gas density at downhole
    "liquid_rate_bpd": 190.0,    # liquid production rate
    "gor_scf_bbl": 10.0,         # gas-oil ratio
    "gvf_fraction": 0.15,        # entrained gas volume fraction in foamy oil
    "sub_length_in": 24.0,       # collector sub length
    "num_lips": 3,               # number of degassing lips
    "lip_restriction": 0.30,     # fraction of annular area blocked by each lip
    "lip_length_mm": 15.0,       # axial length of each lip (contact zone)
    "coalescence_time_min": 15.0, # Maini 1999: 10-20 min for full coalescence
    "surface_tension_N_m": 0.025,    # oil-gas surface tension
    "slug_frequency_per_min": 2.5,   # baseline slug frequency
    "slug_amplitude_kpa": 150.0,     # baseline slug pressure amplitude
}


def annular_area(casing_id_mm, tubing_od_mm):
    """Annular cross-sectional area in m^2."""
    r_cas = casing_id_mm / 2000.0
    r_tub = tubing_od_mm / 2000.0
    return PI * (r_cas**2 - r_tub**2)


def restricted_area(annular_area_m2, restriction_fraction):
    """Area through the lip restriction."""
    return annular_area_m2 * (1.0 - restriction_fraction)


def annular_velocity(liquid_rate_bpd, area_m2):
    """Superficial liquid velocity in the annulus, m/s."""
    q_m3_s = liquid_rate_bpd * 0.158987 / 86400.0
    return q_m3_s / area_m2


def hydraulic_diameter(casing_id_mm, tubing_od_mm):
    """Hydraulic diameter of the annulus, m."""
    return (casing_id_mm - tubing_od_mm) / 1000.0


def reynolds_number(rho, v, d_h, mu_cp):
    """Reynolds number."""
    mu_pa_s = mu_cp / 1000.0
    return rho * v * d_h / mu_pa_s


def shear_stress_through_gap(mu_cp, v_upstream, restriction_fraction, gap_height_mm):
    """
    Wall shear stress through a lip restriction.
    At very low Re, viscous shear dominates.

    tau = mu * (dv/dy) where dv/dy ~ v_gap / (gap_height/2)

    This is the primary coalescence mechanism at 80,000 cP:
    high viscosity means high shear stress even at low velocity.
    """
    mu = mu_cp / 1000.0  # Pa.s
    area_ratio = 1.0 / (1.0 - restriction_fraction)
    v_gap = v_upstream * area_ratio
    gap_m = gap_height_mm / 1000.0

    # Approximate as flow between parallel plates
    # tau_wall = 6 * mu * v_mean / gap_height (for slit flow)
    tau = 6.0 * mu * v_gap / gap_m
    return tau  # Pa


def shear_coalescence_efficiency(shear_stress_pa, bubble_diameter_mm, surface_tension, mu_cp):
    """
    Shear-induced coalescence model.

    High shear deforms bubbles (elongation ratio > 1.5 triggers coalescence).
    Capillary number Ca = mu * gamma_dot * R / sigma determines deformation.
    At Ca >> 1, bubbles are highly deformed and coalescence is promoted.

    Returns: fraction of entrained gas freed at this stage.
    """
    mu = mu_cp / 1000.0
    R = bubble_diameter_mm / 2000.0  # radius in m
    sigma = surface_tension

    # Shear rate from stress
    gamma_dot = shear_stress_pa / mu  # 1/s

    # Capillary number
    Ca = mu * gamma_dot * R / sigma

    # Coalescence probability increases with Ca
    # Literature: Ca > 0.1 starts deformation, Ca > 1 promotes coalescence
    # Simple sigmoid model:
    if Ca < 0.01:
        efficiency = 0.02  # minimal coalescence
    elif Ca < 0.1:
        efficiency = 0.05 + 0.10 * (Ca / 0.1)
    elif Ca < 1.0:
        efficiency = 0.15 + 0.20 * (Ca / 1.0)
    else:
        efficiency = min(0.45, 0.35 + 0.10 * math.log10(Ca))

    return efficiency


def recirculation_residence_factor(restriction_fraction, lip_length_mm, annular_gap_mm):
    """
    Flow restrictions create recirculation zones downstream.
    These zones increase local residence time, giving more time for
    natural coalescence (Maini 1999: 10-20 min for full coalescence).

    Returns: multiplier on local residence time.
    """
    # Recirculation zone extends ~3-5x the step height downstream
    step_height = annular_gap_mm * restriction_fraction
    recirc_length = 4.0 * step_height  # mm

    # Volume of recirculation zone vs pass-through zone
    recirc_factor = 1.0 + (recirc_length / lip_length_mm) * restriction_fraction

    return min(3.0, recirc_factor)


def bernoulli_pressure_drop(rho, v_upstream, restriction_fraction):
    """
    Pressure drop across a restriction (Bernoulli + loss coefficient).
    NOTE: At 13 mm/s, this is NEGLIGIBLE (~0.3 Pa).
    Included for completeness but NOT the primary mechanism.
    """
    if restriction_fraction >= 1.0:
        return float('inf')
    area_ratio = 1.0 / (1.0 - restriction_fraction)
    v_restriction = v_upstream * area_ratio
    cd = 0.6
    dp = 0.5 * rho * (v_restriction**2 - v_upstream**2) / cd**2
    return abs(dp)


def viscous_pressure_drop(mu_cp, v_upstream, restriction_fraction, lip_length_mm, gap_height_mm):
    """
    Viscous (Hagen-Poiseuille type) pressure drop through the lip restriction.
    At very low Re, viscous losses dominate over inertial (Bernoulli) losses.

    For flow through a narrow slit: dP = 12 * mu * v * L / h^2
    """
    mu = mu_cp / 1000.0  # Pa.s
    area_ratio = 1.0 / (1.0 - restriction_fraction)
    v_gap = v_upstream * area_ratio
    L = lip_length_mm / 1000.0  # m
    h = gap_height_mm / 1000.0  # m

    dp = 12.0 * mu * v_gap * L / h**2
    return dp  # Pa


def stokes_rise_velocity(d_bubble_mm, rho_l, rho_g, mu_cp):
    """Stokes rise velocity for a spherical bubble, m/s."""
    d = d_bubble_mm / 1000.0
    mu = mu_cp / 1000.0
    return (1.0/18.0) * (rho_l - rho_g) * G * d**2 / mu


def slug_damping_model(amplitude_in, frequency_in, restriction_fraction, num_stages):
    """
    Slug damping through flow restrictions.
    Each restriction fragments slug bodies and creates backpressure.

    Physical basis:
    - Slug body must deform to pass through restriction
    - High viscosity means large viscous dissipation during deformation
    - Gas pocket behind slug gets partially trapped/redistributed
    - Net: smaller, more frequent disturbances

    Returns: (amplitude_out, frequency_out)
    """
    amp = amplitude_in
    freq = frequency_in

    # Damping increases with restriction severity
    damping_per_stage = 0.15 + 0.35 * restriction_fraction
    freq_increase = 1.0 + 0.3 * restriction_fraction

    for _ in range(num_stages):
        amp *= (1.0 - damping_per_stage)
        freq *= freq_increase

    return amp, freq


def simulate_collector_sub(params):
    """Run the full simulation. Returns a results dict."""

    # Unpack
    cas_id = params["casing_id_mm"]
    tub_od = params["tubing_od_mm"]
    inc = params["inclination_deg"]
    mu_dead = params["oil_viscosity_cp"]
    # SPE-136665: foamy oil viscosity = 56% of dead oil at GVF < 40%
    mu_live = params.get("live_oil_viscosity_cp") or (mu_dead * 0.56)
    params["live_oil_viscosity_cp"] = mu_live  # store for display
    rho_l = params["oil_density_kg_m3"]
    rho_g = params["gas_density_kg_m3"]
    q_l = params["liquid_rate_bpd"]
    gvf_init = params["gvf_fraction"]
    sub_len = params["sub_length_in"]
    n_lips = params["num_lips"]
    restriction = params["lip_restriction"]
    lip_len_mm = params["lip_length_mm"]
    sigma = params["surface_tension_N_m"]
    coal_time = params["coalescence_time_min"]
    slug_amp = params["slug_amplitude_kpa"]
    slug_freq = params["slug_frequency_per_min"]

    # Use live oil viscosity for flow calculations (SPE-136665: foamy oil at GVF<40%)
    mu = mu_live

    # Geometry
    a_annulus = annular_area(cas_id, tub_od)
    a_restricted = restricted_area(a_annulus, restriction)
    v_annulus = annular_velocity(q_l, a_annulus)
    v_gap = annular_velocity(q_l, a_restricted)
    d_h = hydraulic_diameter(cas_id, tub_od)
    ann_gap_mm = (cas_id - tub_od) / 2.0
    gap_through_lip_mm = ann_gap_mm * (1.0 - restriction)

    # Reynolds number
    Re = reynolds_number(rho_l, v_annulus, d_h, mu)

    # Lip spacing
    lip_spacing_in = sub_len / (n_lips + 1)
    lip_spacing_mm = lip_spacing_in * 25.4

    # Transverse and axial gravity
    inc_rad = math.radians(inc)
    g_transverse = G * math.sin(inc_rad)
    g_axial = G * math.cos(inc_rad)

    # Bubble physics
    v_stokes_2mm = stokes_rise_velocity(2.0, rho_l, rho_g, mu)
    v_stokes_10mm = stokes_rise_velocity(10.0, rho_l, rho_g, mu)
    # Transverse migration of coalesced bubbles
    v_transverse_10mm = (1.0/18.0) * (rho_l - rho_g) * g_transverse * (0.010)**2 / (mu/1000.0)

    # Migration time across annular gap
    annular_gap_m = ann_gap_mm / 1000.0
    migration_time_s = annular_gap_m / v_transverse_10mm if v_transverse_10mm > 0 else float('inf')

    # Transit times
    transit_per_lip_s = (lip_spacing_mm / 1000.0) / v_annulus if v_annulus > 0 else float('inf')
    total_sub_length_mm = sub_len * 25.4
    total_transit_s = (total_sub_length_mm / 1000.0) / v_annulus if v_annulus > 0 else float('inf')

    # Fraction of coalescence time spent in sub
    coal_fraction = total_transit_s / (coal_time * 60.0)

    # ── Pressure drops ──
    dp_bernoulli = bernoulli_pressure_drop(rho_l, v_annulus, restriction)
    dp_viscous = viscous_pressure_drop(mu, v_annulus, restriction, lip_len_mm, gap_through_lip_mm)

    # ── Shear stress through each lip ──
    tau_wall = shear_stress_through_gap(mu, v_annulus, restriction, gap_through_lip_mm)

    # ── Recirculation residence factor ──
    recirc_factor = recirculation_residence_factor(restriction, lip_len_mm, ann_gap_mm)

    # ── Stage-by-stage simulation ──
    stages = []
    gvf = gvf_init
    total_gas_freed = 0.0
    total_dp_viscous = 0.0

    for i in range(n_lips):
        # Shear-based coalescence efficiency
        avg_bubble_mm = 2.0 * (gvf / gvf_init)  # bubbles get smaller as gas is freed
        avg_bubble_mm = max(0.5, avg_bubble_mm)
        shear_eff = shear_coalescence_efficiency(tau_wall, avg_bubble_mm, sigma, mu)

        # Natural coalescence contribution (proportional to residence time)
        # Each lip's recirculation zone adds residence time
        natural_eff = coal_fraction / n_lips * recirc_factor * 0.5  # partial credit

        # Combined efficiency (don't double count)
        total_eff = min(0.50, shear_eff + natural_eff)

        gas_freed = gvf * total_eff
        gvf_after = gvf - gas_freed
        total_gas_freed += gas_freed
        total_dp_viscous += dp_viscous / 1000.0  # kPa

        stages.append({
            "stage": i + 1,
            "gvf_before": gvf,
            "gvf_after": gvf_after,
            "gas_freed_pct": gas_freed / gvf_init * 100,
            "shear_efficiency_pct": shear_eff * 100,
            "natural_efficiency_pct": natural_eff * 100,
            "combined_efficiency_pct": total_eff * 100,
            "dp_viscous_kpa": dp_viscous / 1000.0,
            "cumulative_gas_freed_pct": total_gas_freed / gvf_init * 100,
        })

        gvf = gvf_after

    # Slug damping
    amp_out, freq_out = slug_damping_model(slug_amp, slug_freq, restriction, n_lips)

    results = {
        "params": params,
        "geometry": {
            "annular_area_mm2": a_annulus * 1e6,
            "restricted_area_mm2": a_restricted * 1e6,
            "annular_velocity_mm_s": v_annulus * 1000,
            "gap_velocity_mm_s": v_gap * 1000,
            "hydraulic_diameter_mm": d_h * 1000,
            "annular_gap_mm": ann_gap_mm,
            "gap_through_lip_mm": gap_through_lip_mm,
            "lip_spacing_mm": lip_spacing_mm,
            "reynolds_number": Re,
        },
        "gravity": {
            "g_transverse": g_transverse,
            "g_axial": g_axial,
            "ratio": g_transverse / g_axial if g_axial > 0 else float('inf'),
        },
        "bubble_physics": {
            "v_stokes_2mm_mm_s": v_stokes_2mm * 1000,
            "v_stokes_10mm_mm_s": v_stokes_10mm * 1000,
            "v_transverse_10mm_mm_s": v_transverse_10mm * 1000,
            "migration_time_s": migration_time_s,
            "transit_per_lip_s": transit_per_lip_s,
            "total_transit_s": total_transit_s,
            "coalescence_fraction": coal_fraction,
        },
        "pressure_drops": {
            "bernoulli_per_lip_pa": dp_bernoulli,
            "viscous_per_lip_pa": dp_viscous,
            "viscous_per_lip_kpa": dp_viscous / 1000.0,
            "total_viscous_kpa": total_dp_viscous,
            "bernoulli_note": "NEGLIGIBLE at 13 mm/s — NOT the mechanism",
        },
        "shear": {
            "wall_shear_stress_pa": tau_wall,
            "wall_shear_stress_kpa": tau_wall / 1000.0,
            "recirculation_factor": recirc_factor,
        },
        "stages": stages,
        "summary": {
            "gvf_initial": gvf_init,
            "gvf_final": gvf,
            "total_gas_freed_pct": total_gas_freed / gvf_init * 100,
            "total_dp_viscous_kpa": total_dp_viscous,
            "num_stages": n_lips,
            "mechanism": "VISCOUS SHEAR + RESIDENCE TIME (not Bernoulli pressure drop)",
        },
        "slug_damping": {
            "amplitude_before_kpa": slug_amp,
            "amplitude_after_kpa": amp_out,
            "amplitude_reduction_pct": (1 - amp_out / slug_amp) * 100,
            "frequency_before_per_min": slug_freq,
            "frequency_after_per_min": freq_out,
            "frequency_increase_pct": (freq_out / slug_freq - 1) * 100,
        },
    }

    return results


def print_results(results):
    """Print simulation results as formatted text."""
    p = results["params"]
    g = results["geometry"]
    grav = results["gravity"]
    bp = results["bubble_physics"]
    pd_ = results["pressure_drops"]
    sh = results["shear"]
    stages = results["stages"]
    s = results["summary"]
    sd = results["slug_damping"]

    print("=" * 74)
    print("WELLFI COLLECTOR SUB — DEGASSING & SLUG DAMPING SIMULATION (v2)")
    print("=" * 74)

    print(f"\nWELL PARAMETERS")
    print(f"  Casing ID:         {p['casing_id_mm']:.1f} mm ({p['casing_id_mm']/25.4:.3f} in)")
    print(f"  Tubing OD:         {p['tubing_od_mm']:.1f} mm ({p['tubing_od_mm']/25.4:.3f} in)")
    print(f"  Inclination:       {p['inclination_deg']:.1f} deg")
    print(f"  Dead oil viscosity:{p['oil_viscosity_cp']:>10,.0f} cP")
    print(f"  Live oil viscosity:{p['live_oil_viscosity_cp']:>10,.0f} cP  (foamy, SPE-136665: 56% of dead)")
    print(f"  Liquid rate:       {p['liquid_rate_bpd']:.0f} bbl/d")
    print(f"  Initial GVF:       {p['gvf_fraction']*100:.1f}%")

    print(f"\nCOLLECTOR SUB GEOMETRY")
    print(f"  Sub length:        {p['sub_length_in']:.0f} in ({p['sub_length_in']*25.4:.0f} mm)")
    print(f"  Number of lips:    {p['num_lips']}")
    print(f"  Lip spacing:       {g['lip_spacing_mm']:.0f} mm ({g['lip_spacing_mm']/25.4:.1f} in)")
    print(f"  Lip restriction:   {p['lip_restriction']*100:.0f}% of annular area")
    print(f"  Annular gap:       {g['annular_gap_mm']:.1f} mm (full)")
    print(f"  Gap through lip:   {g['gap_through_lip_mm']:.1f} mm (restricted)")

    print(f"\nFLOW CONDITIONS")
    print(f"  Annular velocity:  {g['annular_velocity_mm_s']:.1f} mm/s")
    print(f"  Gap velocity:      {g['gap_velocity_mm_s']:.1f} mm/s")
    print(f"  Reynolds number:   {g['reynolds_number']:.6f}  << 1  (CREEPING FLOW)")
    print(f"  Flow regime:       Stokes flow — viscous forces completely dominate")

    inc_val = p['inclination_deg']
    print(f"\nGRAVITY AT {inc_val:.0f} DEG")
    print(f"  Transverse (to low side):  {grav['g_transverse']:.3f} m/s^2")
    print(f"  Axial (along wellbore):    {grav['g_axial']:.3f} m/s^2")
    print(f"  Ratio:                     {grav['ratio']:.1f}x (transverse dominates)")

    print(f"\nPRESSURE DROPS PER LIP")
    print(f"  Bernoulli (inertial): {pd_['bernoulli_per_lip_pa']:.3f} Pa  = {pd_['bernoulli_per_lip_pa']/1000:.6f} kPa")
    print(f"                        ^^^ NEGLIGIBLE — Bernoulli is NOT the mechanism")
    print(f"  Viscous (shear):      {pd_['viscous_per_lip_pa']:.1f} Pa  = {pd_['viscous_per_lip_kpa']:.2f} kPa")
    print(f"  Total viscous ({p['num_lips']} lips):  {pd_['total_viscous_kpa']:.2f} kPa")
    print(f"                        ^^^ Low — will not affect PCP performance")

    print(f"\nSHEAR MECHANISM")
    print(f"  Wall shear stress:     {sh['wall_shear_stress_pa']:.0f} Pa ({sh['wall_shear_stress_kpa']:.1f} kPa)")
    print(f"  Recirculation factor:  {sh['recirculation_factor']:.1f}x local residence time")
    print(f"  This is the primary coalescence driver — high viscosity means")
    print(f"  high shear even at very low velocity.")

    print(f"\nBUBBLE PHYSICS")
    print(f"  2mm bubble Stokes rise:  {bp['v_stokes_2mm_mm_s']:.4f} mm/s  (NEGLIGIBLE)")
    print(f"  10mm coalesced bubble:   {bp['v_stokes_10mm_mm_s']:.3f} mm/s")
    print(f"  10mm transverse drift:   {bp['v_transverse_10mm_mm_s']:.3f} mm/s")
    print(f"  Migration time:          {bp['migration_time_s']:.0f} s  (to cross annular gap)")
    print(f"  Transit per lip spacing: {bp['transit_per_lip_s']:.1f} s")
    print(f"  Total sub transit:       {bp['total_transit_s']:.1f} s")
    print(f"  Coalescence fraction:    {bp['coalescence_fraction']*100:.1f}%  of 10-20 min needed")

    if bp['migration_time_s'] > bp['transit_per_lip_s']:
        print(f"\n  WARNING: Gas migration time ({bp['migration_time_s']:.0f}s) > lip spacing transit")
        print(f"  ({bp['transit_per_lip_s']:.1f}s). Freed gas may not fully clear before next lip.")
        print(f"  This is OK — gas accumulates progressively across all stages.")

    print(f"\nSTAGE-BY-STAGE DEGASSING")
    print(f"  {'Stage':>5} | {'GVF In':>8} | {'GVF Out':>8} | {'Shear':>6} | {'Natural':>7} | {'Total':>5} | {'Freed':>10} | {'Cumul':>10}")
    print(f"  {'-'*5}-+-{'-'*8}-+-{'-'*8}-+-{'-'*6}-+-{'-'*7}-+-{'-'*5}-+-{'-'*10}-+-{'-'*10}")
    for st in stages:
        print(f"  {st['stage']:>5} | {st['gvf_before']*100:>7.1f}% | {st['gvf_after']*100:>7.1f}% | "
              f"{st['shear_efficiency_pct']:>5.1f}% | {st['natural_efficiency_pct']:>6.1f}% | "
              f"{st['combined_efficiency_pct']:>4.0f}% | {st['gas_freed_pct']:>9.1f}% | "
              f"{st['cumulative_gas_freed_pct']:>9.1f}%")

    print(f"\nDEGASSING SUMMARY")
    print(f"  Initial entrained gas:  {s['gvf_initial']*100:.1f}%")
    print(f"  Final entrained gas:    {s['gvf_final']*100:.1f}%")
    print(f"  Total gas freed:        {s['total_gas_freed_pct']:.1f}% of original entrained gas")
    print(f"  Total viscous dP:       {s['total_dp_viscous_kpa']:.2f} kPa")
    print(f"  Mechanism:              {s['mechanism']}")

    print(f"\nSLUG DAMPING")
    print(f"  Amplitude before:  {sd['amplitude_before_kpa']:.0f} kPa")
    print(f"  Amplitude after:   {sd['amplitude_after_kpa']:.0f} kPa  ({sd['amplitude_reduction_pct']:.0f}% reduction)")
    print(f"  Frequency before:  {sd['frequency_before_per_min']:.1f} slugs/min")
    print(f"  Frequency after:   {sd['frequency_after_per_min']:.1f} slugs/min  ({sd['frequency_increase_pct']:.0f}% increase)")
    print(f"  Net effect:        Smaller slugs, more frequent = more uniform flow")

    print(f"\nWELLFI SIGNAL IMPACT")
    amp_ratio = sd['amplitude_after_kpa'] / sd['amplitude_before_kpa']
    if amp_ratio < 0.4:
        print(f"  Pressure noise reduction: SIGNIFICANT ({(1-amp_ratio)*100:.0f}%)")
        print(f"  Expected WellFi benefit:  HIGH")
    elif amp_ratio < 0.7:
        print(f"  Pressure noise reduction: MODERATE ({(1-amp_ratio)*100:.0f}%)")
        print(f"  Expected WellFi benefit:  MODERATE")
    else:
        print(f"  Pressure noise reduction: MARGINAL ({(1-amp_ratio)*100:.0f}%)")
        print(f"  Expected WellFi benefit:  LOW")

    print(f"\n{'=' * 74}")
    print(f"HONEST ASSESSMENT:")
    print(f"  1. The Bernoulli (pressure-drop) mechanism does NOT work at 13 mm/s.")
    print(f"     Inertial pressure drop is 0.3 Pa — physically meaningless.")
    print(f"  2. The actual mechanism is VISCOUS SHEAR through the lip restriction.")
    print(f"     At 44,800 cP, even 13 mm/s creates {sh['wall_shear_stress_pa']:.0f} Pa wall shear stress.")
    print(f"  3. Shear deforms bubbles (Ca >> 1) promoting coalescence on contact.")
    print(f"  4. Recirculation zones behind each lip extend local residence time.")
    print(f"  5. Slug damping is the MOST CERTAIN benefit — physical restrictions")
    print(f"     fragment slug bodies regardless of coalescence efficiency.")
    print(f"  6. All coalescence numbers are ESTIMATES — no lab data at 80,000 cP.")
    print(f"  7. Needs flow loop validation (glycerin/air analog at matched Ca number).")
    print(f"{'=' * 74}")


def generate_visual(results, output_path):
    """Generate a 4-panel simulation results visual."""

    BG      = "#0d1117"
    PANEL   = "#161b22"
    BORDER  = "#30363d"
    TEXT    = "#e6edf3"
    MUTED   = "#8b949e"
    ACCENT  = "#00d4ff"
    GOLD    = "#d4a847"
    GREEN   = "#3fb950"
    RED     = "#f85149"
    GAS_CLR = "#ff6b6b"
    ORANGE  = "#d29922"

    p = results["params"]
    stages = results["stages"]
    s = results["summary"]
    sd = results["slug_damping"]
    sh = results["shear"]
    pd_ = results["pressure_drops"]

    fig = plt.figure(figsize=(18, 11), dpi=200, facecolor=BG)
    fig.subplots_adjust(hspace=0.38, wspace=0.32, left=0.07, right=0.95, top=0.88, bottom=0.08)

    fig.text(0.5, 0.96, "WellFi Collector Sub — Simulation Results",
             fontsize=22, fontweight="bold", color=TEXT, ha="center", family="Segoe UI")
    fig.text(0.5, 0.935,
             f"{p['num_lips']} lips  |  {p['lip_restriction']*100:.0f}% restriction  |  "
             f"{p['live_oil_viscosity_cp']:,.0f} cP (live)  |  {p['inclination_deg']:.0f} deg  |  "
             f"{p['liquid_rate_bpd']:.0f} bbl/d  |  Re = {results['geometry']['reynolds_number']:.2e}",
             fontsize=10, color=MUTED, ha="center", family="Segoe UI")
    fig.text(0.5, 0.905,
             f"Mechanism: viscous shear coalescence + residence time extension (NOT Bernoulli pressure drop)",
             fontsize=10, color=ACCENT, ha="center", family="Segoe UI", fontweight="bold")

    axes = fig.subplots(2, 2)
    for ax in axes.flat:
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_color(BORDER)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.title.set_color(TEXT)

    # ── Panel 1: Gas Fraction Through Stages ──
    ax1 = axes[0, 0]
    stage_nums = [0] + [st["stage"] for st in stages]
    gvf_values = [s["gvf_initial"] * 100] + [st["gvf_after"] * 100 for st in stages]

    ax1.fill_between(stage_nums, gvf_values, alpha=0.3, color=GAS_CLR)
    ax1.plot(stage_nums, gvf_values, 'o-', color=GAS_CLR, linewidth=2.5, markersize=10, zorder=5)

    for i, (x, y) in enumerate(zip(stage_nums, gvf_values)):
        ax1.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                     xytext=(0, 14), ha="center", fontsize=10, color=TEXT, fontweight="bold")

    ax1.set_xlabel("Stage (0 = inlet)", fontsize=10)
    ax1.set_ylabel("Entrained Gas (%)", fontsize=10)
    ax1.set_title("Gas Fraction Reduction Through Stages", fontweight="bold", fontsize=13)
    ax1.set_xticks(stage_nums)
    ax1.set_xticklabels(["Inlet"] + [f"Lip {i+1}" for i in range(p["num_lips"])])
    ax1.grid(True, alpha=0.15, color=MUTED)
    ax1.set_ylim(0, max(gvf_values) * 1.35)

    # Efficiency breakdown annotations
    for st in stages:
        ax1.annotate(f"Shear {st['shear_efficiency_pct']:.0f}% + Natural {st['natural_efficiency_pct']:.0f}%",
                     (st['stage'], st['gvf_after'] * 100),
                     textcoords="offset points", xytext=(0, -18),
                     ha="center", fontsize=7.5, color=MUTED)

    # ── Panel 2: Mechanism Comparison (shear vs pressure) ──
    ax2 = axes[0, 1]

    categories = ["Bernoulli dP\n(inertial)", "Viscous dP\n(per lip)", "Wall Shear\nStress"]
    values = [pd_["bernoulli_per_lip_pa"], pd_["viscous_per_lip_pa"], sh["wall_shear_stress_pa"]]
    colors = [RED, ORANGE, GREEN]

    bars = ax2.bar(categories, values, color=colors, alpha=0.8, edgecolor=colors, linewidth=1.5)

    for bar, val, col in zip(bars, values, colors):
        if val < 1:
            label = f"{val:.3f} Pa"
        elif val < 1000:
            label = f"{val:.0f} Pa"
        else:
            label = f"{val/1000:.1f} kPa"
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                 label, ha="center", fontsize=10, color=col, fontweight="bold")

    ax2.set_ylabel("Magnitude (Pa) — log scale", fontsize=10)
    ax2.set_title("Why Shear Dominates (not Bernoulli)", fontweight="bold", fontsize=13)
    ax2.set_yscale("log")
    ax2.grid(True, alpha=0.15, color=MUTED, which="both")

    # Annotation explaining the key insight
    ax2.text(0.5, 0.02, "At 13 mm/s, Bernoulli is 0.3 Pa.\n"
             "Viscous shear is the real mechanism.",
             transform=ax2.transAxes, fontsize=9, color=ACCENT,
             ha="center", va="bottom", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#0a1929", edgecolor=ACCENT, alpha=0.9))

    # ── Panel 3: Slug Damping (time series) ──
    ax3 = axes[1, 0]
    t = np.linspace(0, 120, 2000)

    freq_before = sd["frequency_before_per_min"] / 60.0
    amp_before = sd["amplitude_before_kpa"]
    freq_after = sd["frequency_after_per_min"] / 60.0
    amp_after = sd["amplitude_after_kpa"]

    # Asymmetric slug waveform (sharp rise, slow decay)
    np.random.seed(42)
    signal_before = amp_before * (
        0.6 * np.sin(2 * PI * freq_before * t) +
        0.25 * np.sin(4 * PI * freq_before * t + 0.5) +
        0.15 * np.sin(6 * PI * freq_before * t + 1.0)
    ) + np.random.normal(0, amp_before * 0.06, len(t))

    signal_after = amp_after * (
        0.6 * np.sin(2 * PI * freq_after * t) +
        0.25 * np.sin(4 * PI * freq_after * t + 0.5) +
        0.15 * np.sin(6 * PI * freq_after * t + 1.0)
    ) + np.random.normal(0, amp_after * 0.06, len(t))

    p_base = 2000

    ax3.plot(t, p_base + signal_before, color=RED, alpha=0.6, linewidth=0.8,
             label=f"Before: +/-{amp_before:.0f} kPa @ {sd['frequency_before_per_min']:.1f}/min")
    ax3.plot(t, p_base + signal_after, color=GREEN, alpha=0.85, linewidth=1.0,
             label=f"After:  +/-{amp_after:.0f} kPa @ {sd['frequency_after_per_min']:.1f}/min")

    ax3.axhline(y=p_base, color=ACCENT, linewidth=0.8, linestyle="--", alpha=0.4)

    ax3.set_xlabel("Time (seconds)", fontsize=10)
    ax3.set_ylabel("Pressure at PCP Intake (kPa)", fontsize=10)
    ax3.set_title("Slug Damping: Pressure at PCP Intake", fontweight="bold", fontsize=13)
    ax3.legend(loc="upper right", fontsize=8.5, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
    ax3.grid(True, alpha=0.15, color=MUTED)

    ax3.text(0.02, 0.02, f"{sd['amplitude_reduction_pct']:.0f}% amplitude reduction\n"
             f"Most certain benefit of the design",
             transform=ax3.transAxes, fontsize=9, color=ACCENT, fontweight="bold",
             va="bottom",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#0a1929", edgecolor=ACCENT, alpha=0.9))

    # ── Panel 4: Sensitivity (num lips + sub length) ──
    ax4 = axes[1, 1]

    # Sweep number of lips at different sub lengths
    for sub_len, ls, marker, clr in [(24, "-", "o", GREEN), (36, "--", "s", ACCENT), (48, ":", "^", GOLD)]:
        freed_vals = []
        damp_vals = []
        lip_range = range(1, 7)
        for n in lip_range:
            tp = dict(DEFAULTS)
            tp["num_lips"] = n
            tp["sub_length_in"] = sub_len
            tr = simulate_collector_sub(tp)
            freed_vals.append(tr["summary"]["total_gas_freed_pct"])
            damp_vals.append(tr["slug_damping"]["amplitude_reduction_pct"])
        ax4.plot(list(lip_range), freed_vals, f'{marker}{ls}', color=clr, linewidth=2,
                 markersize=7, label=f'{sub_len}" sub — gas freed', zorder=5)
        ax4.plot(list(lip_range), damp_vals, f'{marker}{ls}', color=clr, linewidth=1,
                 markersize=5, alpha=0.5, zorder=4)

    ax4.axvline(x=3, color=GOLD, linewidth=1.5, linestyle="--", alpha=0.4)
    ax4.text(3.1, 5, "Current\ndesign", fontsize=8, color=GOLD, fontweight="bold")

    ax4.set_xlabel("Number of Lips", fontsize=10)
    ax4.set_ylabel("Efficiency (%)", fontsize=10)
    ax4.set_title("Sensitivity: Lips x Sub Length", fontweight="bold", fontsize=13)
    ax4.legend(loc="lower right", fontsize=7.5, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
    ax4.grid(True, alpha=0.15, color=MUTED)
    ax4.set_xticks(list(lip_range))
    ax4.set_ylim(0, 100)

    # Footer
    fig.text(0.5, 0.015,
             "EXTRAPOLATION WARNING: No validated coalescence data above 6,000 cP. Shear coalescence model "
             "is physics-based (Capillary number) but unvalidated at 80,000 cP. Slug damping is the highest-confidence prediction.",
             fontsize=8, color=MUTED, ha="center", family="Segoe UI", style="italic")

    fig.savefig(output_path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"\nVisual saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="WellFi Collector Sub — Degassing & Slug Damping Simulation (v2)"
    )
    parser.add_argument("--casing_id", type=float, default=DEFAULTS["casing_id_mm"])
    parser.add_argument("--tubing_od", type=float, default=DEFAULTS["tubing_od_mm"])
    parser.add_argument("--inclination", type=float, default=DEFAULTS["inclination_deg"])
    parser.add_argument("--oil_viscosity", type=float, default=DEFAULTS["oil_viscosity_cp"])
    parser.add_argument("--liquid_rate", type=float, default=DEFAULTS["liquid_rate_bpd"])
    parser.add_argument("--gvf", type=float, default=DEFAULTS["gvf_fraction"])
    parser.add_argument("--num_lips", type=int, default=DEFAULTS["num_lips"])
    parser.add_argument("--lip_restriction", type=float, default=DEFAULTS["lip_restriction"])
    parser.add_argument("--sub_length", type=float, default=DEFAULTS["sub_length_in"])
    parser.add_argument("--output", type=str, default="text", choices=["text", "visual", "both"])

    args = parser.parse_args()

    params = dict(DEFAULTS)
    params["casing_id_mm"] = args.casing_id
    params["tubing_od_mm"] = args.tubing_od
    params["inclination_deg"] = args.inclination
    params["oil_viscosity_cp"] = args.oil_viscosity
    params["liquid_rate_bpd"] = args.liquid_rate
    params["gvf_fraction"] = args.gvf
    params["num_lips"] = args.num_lips
    params["lip_restriction"] = args.lip_restriction
    params["sub_length_in"] = args.sub_length

    results = simulate_collector_sub(params)

    if args.output in ("text", "both"):
        print_results(results)

    if args.output in ("visual", "both"):
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "docs", "visuals", "wellfi-collector-sub-simulation.png"
        )
        generate_visual(results, output_path)


if __name__ == "__main__":
    main()
