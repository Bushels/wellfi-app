#!/usr/bin/env python3
"""
WellFi Firmware Filter Proof-of-Concept

Tests the hypothesis from the RT4 Lead Engineer Adversarial Assessment:
> If firmware alone achieves >90% payload success in gas events, the
> sub's value prop collapses.

This prototype applies three firmware-style packet filter strategies to
the real Run 3 EMGRx event log and measures how much of the Apr 2 -> Apr 3
payload-success improvement (66% -> 97%) can be recovered in software alone,
WITHOUT the physical joint pull.

Three strategies tested:
  A. Naive CRC rejection          — drop isCRCError packets
  B. Multi-criterion filter       — drop if CRC=True AND signal_error > 30%
  C. Gas-event-aware + interpolation — detect CRC bursts, interpolate through

Data source:
  G:\\My Drive\\Belle Industries\\WellFi\\Obsidian\\102161808317W509\\Logs\\
    EMGRx SN_2602315 EventLog_CSV2026-04-03 2_52_23 PM.csv

Pressure in payload is in BAR — convert to kPa by x100.
"""

import csv
import os
import sys
from datetime import datetime
from collections import defaultdict

LOG_PATH = r"G:\My Drive\Belle Industries\WellFi\Obsidian\102161808317W509\Logs\EMGRx SN_2602315 EventLog_CSV2026-04-03 2_52_23 PM.csv"

def parse_datetime(s):
    """Handle both '2026-04-02 3:35:10 PM' and '2026-04-02 15:08' formats."""
    s = s.strip()
    for fmt in ("%Y-%m-%d %I:%M:%S %p", "%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def parse_log(path):
    """
    Parse EMGRx log, consolidating PayloadRecoveredEvent + PayloadStats1-4
    into single packet records.
    """
    packets = []
    sync_losses = []
    current = None

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header_seen = False
        for row in reader:
            if not row or not row[0].strip():
                continue
            if row[0].startswith("SerialNumber") or row[0].startswith("Manufacturing"):
                continue
            if row[0] == "DateTime":
                header_seen = True
                continue
            if not header_seen:
                continue

            dt = parse_datetime(row[0])
            if dt is None:
                continue
            event = row[1].strip() if len(row) > 1 else ""

            if event == "PayloadRecoveredEvent":
                # Finalize any pending packet
                if current is not None:
                    packets.append(current)
                try:
                    pressure = float(row[6]) if row[6] else None
                    temp = float(row[7]) if row[7] else None
                    txid = row[8].strip() if len(row) > 8 else ""
                    crc_err_flag = row[9].strip() if len(row) > 9 else ""
                except (ValueError, IndexError):
                    pressure, temp, txid, crc_err_flag = None, None, "", ""

                current = {
                    "datetime": dt,
                    "pressure_bar": pressure,
                    "pressure_kpa": pressure * 100 if pressure is not None else None,
                    "temperature_c": temp,
                    "tx_id": txid,
                    "crc_error": crc_err_flag == "01",
                    "power_signal": None,
                    "signal_error_pct": None,
                    "lock_signal": None,
                    "gain": None,
                    "vrms_noise_dbv": None,
                    "vrms_signal_dbv": None,
                }
            elif event == "PayloadStats1" and current is not None:
                try:
                    current["power_signal"] = float(row[4]) if row[4] else None
                    current["lock_signal"] = float(row[10]) if len(row) > 10 and row[10] else None
                except (ValueError, IndexError):
                    pass
            elif event == "PayloadStats2" and current is not None:
                try:
                    current["signal_error_pct"] = float(row[5]) if row[5] else None
                    current["gain"] = float(row[11]) if len(row) > 11 and row[11] else None
                except (ValueError, IndexError):
                    pass
            elif event == "PayloadStats3" and current is not None:
                try:
                    current["vrms_noise_dbv"] = float(row[12]) if len(row) > 12 and row[12] else None
                except (ValueError, IndexError):
                    pass
            elif event == "PayloadStats4" and current is not None:
                try:
                    current["vrms_signal_dbv"] = float(row[13]) if len(row) > 13 and row[13] else None
                except (ValueError, IndexError):
                    pass
            elif event == "PotentialSyncLostEvent":
                try:
                    sync_losses.append({
                        "datetime": dt,
                        "signal_error_pct": float(row[5]) if row[5] else None,
                    })
                except (ValueError, IndexError):
                    sync_losses.append({"datetime": dt, "signal_error_pct": None})

    if current is not None:
        packets.append(current)

    return packets, sync_losses


def window_stats(packets, label):
    """Raw statistics for a packet window."""
    n = len(packets)
    if n == 0:
        return {"label": label, "n": 0}
    crc_errors = sum(1 for p in packets if p["crc_error"])
    good = n - crc_errors

    sig_errs = [p["signal_error_pct"] for p in packets if p["signal_error_pct"] is not None]
    mean_sig_err = sum(sig_errs) / len(sig_errs) if sig_errs else None

    return {
        "label": label,
        "n_total": n,
        "n_good": good,
        "n_crc_err": crc_errors,
        "success_pct": 100 * good / n,
        "mean_signal_error_pct": mean_sig_err,
        "start": packets[0]["datetime"].isoformat(),
        "end": packets[-1]["datetime"].isoformat(),
    }


# ─────────────── Firmware Filter Strategies ───────────────

def strategy_a_naive_crc(packets):
    """Simple: drop any packet with CRC error. Same as raw 'success_pct'."""
    return [p for p in packets if not p["crc_error"]]


def strategy_b_multicriterion(packets, sig_err_threshold=30.0):
    """
    Keep a packet if EITHER CRC is OK OR signal error is below threshold.
    Reject only if BOTH CRC bad AND signal quality poor.

    Rationale: some CRC errors are single-bit flips in otherwise clean
    packets — the payload value might still be usable. Only reject if
    the signal itself was degraded.
    """
    accepted = []
    for p in packets:
        if not p["crc_error"]:
            accepted.append(p)
        elif p["signal_error_pct"] is not None and p["signal_error_pct"] < sig_err_threshold:
            # CRC failed but signal was clean — might be recoverable
            p2 = dict(p)
            p2["recovered_via_signal_quality"] = True
            accepted.append(p2)
    return accepted


def strategy_c_gas_event_aware(packets, burst_threshold=3, interp_gap_min=30):
    """
    Detect gas-event CRC bursts (>= burst_threshold consecutive CRC errors
    within a short window) and:
      1. Mark them as 'gas event' interval
      2. Interpolate pressure through the burst using pre/post clean packets
      3. Output a synthesized clean stream

    This is the 'smart firmware' case — no data points are lost, gas events
    are flagged, and downstream consumers see a continuous pressure trend.

    interp_gap_min = maximum minutes to interpolate across.
    """
    output = []
    n = len(packets)
    i = 0
    gas_events_detected = 0
    interpolated_points = 0

    while i < n:
        p = packets[i]
        if not p["crc_error"]:
            output.append(dict(p, filter_status="clean"))
            i += 1
            continue

        # CRC error detected — look ahead for burst
        j = i
        while j < n and packets[j]["crc_error"]:
            j += 1
        burst_len = j - i

        if burst_len >= burst_threshold:
            # Gas event burst — interpolate through it
            gas_events_detected += 1
            # Find anchors: last clean packet before i, first clean packet after j
            before = next((packets[k] for k in range(i - 1, -1, -1)
                           if not packets[k]["crc_error"]), None)
            after = packets[j] if j < n else None

            if before is not None and after is not None:
                dt_span = (after["datetime"] - before["datetime"]).total_seconds() / 60.0
                if dt_span <= interp_gap_min:
                    p_before = before["pressure_kpa"]
                    p_after = after["pressure_kpa"]
                    if p_before is not None and p_after is not None:
                        for k in range(i, j):
                            t = packets[k]["datetime"]
                            frac = (t - before["datetime"]).total_seconds() / (
                                after["datetime"] - before["datetime"]).total_seconds()
                            interp_pressure_kpa = p_before + (p_after - p_before) * frac
                            rec = dict(packets[k])
                            rec["pressure_kpa"] = interp_pressure_kpa
                            rec["pressure_bar"] = interp_pressure_kpa / 100
                            rec["filter_status"] = "interpolated_gas_event"
                            output.append(rec)
                            interpolated_points += 1
                        i = j
                        continue

            # No valid interpolation anchors — mark as gap
            for k in range(i, j):
                output.append(dict(packets[k], filter_status="unrecoverable_gap"))
            i = j
        else:
            # Short burst — probably transient noise; keep as-is but flag
            for k in range(i, j):
                output.append(dict(packets[k], filter_status="crc_transient"))
            i = j

    metadata = {
        "gas_events_detected": gas_events_detected,
        "interpolated_points": interpolated_points,
    }
    return output, metadata


# ─────────────── Metrics ───────────────

def usable_rate(filtered, allow_recovered=True, allow_interpolated=True):
    """
    A packet is 'usable' by downstream consumers if:
      - filter_status is 'clean', OR
      - 'recovered_via_signal_quality' and allow_recovered, OR
      - 'interpolated_gas_event' and allow_interpolated
    """
    if not filtered:
        return 0.0, 0, 0
    n = len(filtered)
    usable = 0
    for p in filtered:
        st = p.get("filter_status", "clean")
        if st == "clean":
            usable += 1
        elif st == "interpolated_gas_event" and allow_interpolated:
            usable += 1
        elif p.get("recovered_via_signal_quality") and allow_recovered:
            usable += 1
    return 100 * usable / n, usable, n


def partition_by_day(packets, target_date):
    return [p for p in packets if p["datetime"].date() == target_date]


# ─────────────── Main ───────────────

def main():
    print(f"Reading: {LOG_PATH}")
    if not os.path.exists(LOG_PATH):
        print(f"ERROR: File not found")
        return

    packets, sync_losses = parse_log(LOG_PATH)
    print(f"Parsed {len(packets)} packets and {len(sync_losses)} sync-loss events\n")

    if not packets:
        print("No packets parsed — aborting")
        return

    # Partition by day
    from datetime import date
    apr2 = [p for p in packets if p["datetime"].date() == date(2026, 4, 2)]
    apr3 = [p for p in packets if p["datetime"].date() == date(2026, 4, 3)]

    print("=" * 78)
    print("BASELINE: Raw payload success rate (the '66% / 97%' benchmark)")
    print("=" * 78)
    for label, pkts in [("Apr 2 (pre-joint-pull)", apr2),
                         ("Apr 3 (post-joint-pull)", apr3),
                         ("Combined Run 3", packets)]:
        s = window_stats(pkts, label)
        if s["n_total"] == 0:
            print(f"{label}: NO DATA")
            continue
        print(f"{label}:")
        print(f"  Time window:   {s['start']} -> {s['end']}")
        print(f"  Packets total: {s['n_total']}")
        print(f"  Clean (CRC OK): {s['n_good']}")
        print(f"  CRC errors:     {s['n_crc_err']}")
        print(f"  Success rate:   {s['success_pct']:.1f}%")
        if s["mean_signal_error_pct"] is not None:
            print(f"  Mean signal err: {s['mean_signal_error_pct']:.1f}%")
        print()

    print("=" * 78)
    print("FIRMWARE STRATEGIES — applied to Apr 2 (worst case, 66% baseline)")
    print("=" * 78)

    if len(apr2) == 0:
        print("No Apr 2 packets to test against — skipping strategy tests")
    else:
        # Strategy A
        a_filtered = strategy_a_naive_crc(apr2)
        a_rate, a_usable, _ = usable_rate(a_filtered)
        print(f"A. Naive CRC rejection:")
        print(f"   Packets kept: {len(a_filtered)} of {len(apr2)}")
        print(f"   Usable rate:  {a_rate:.1f}% (of kept packets, all clean by definition)")
        print(f"   Data loss:    {len(apr2) - len(a_filtered)} packets dropped")
        print(f"   Net usable vs raw: same as baseline — this is what '66% success' means")
        print()

        # Strategy B
        b_filtered = strategy_b_multicriterion(apr2, sig_err_threshold=30.0)
        b_rate, b_usable, b_n = usable_rate(b_filtered)
        n_recovered = sum(1 for p in b_filtered if p.get("recovered_via_signal_quality"))
        print(f"B. Multi-criterion (CRC OK OR signal_err < 30%):")
        print(f"   Packets kept: {b_n} of {len(apr2)}")
        print(f"   Recovered via signal quality: {n_recovered}")
        print(f"   Usable rate:  {b_rate:.1f}% (clean + recovered)")
        print(f"   Gain over A:  {b_rate - a_rate:+.1f} percentage points")
        print()

        # Strategy C
        c_filtered, c_meta = strategy_c_gas_event_aware(apr2, burst_threshold=3, interp_gap_min=30)
        c_rate, c_usable, c_n = usable_rate(c_filtered)
        n_interp = sum(1 for p in c_filtered if p.get("filter_status") == "interpolated_gas_event")
        n_transient = sum(1 for p in c_filtered if p.get("filter_status") == "crc_transient")
        n_unrecov = sum(1 for p in c_filtered if p.get("filter_status") == "unrecoverable_gap")
        print(f"C. Gas-event-aware + interpolation:")
        print(f"   Packets kept: {c_n} of {len(apr2)}")
        print(f"   Clean:              {sum(1 for p in c_filtered if p.get('filter_status')=='clean')}")
        print(f"   Interpolated:       {n_interp}")
        print(f"   CRC transient:      {n_transient} (kept but flagged low-confidence)")
        print(f"   Unrecoverable gaps: {n_unrecov}")
        print(f"   Gas events detected: {c_meta['gas_events_detected']}")
        print(f"   Usable rate:  {c_rate:.1f}% (clean + interpolated)")
        print(f"   Gain over A:  {c_rate - a_rate:+.1f} percentage points")
        print()

    print("=" * 78)
    print("FIRMWARE STRATEGIES — applied to Apr 3 (97% baseline — want no degradation)")
    print("=" * 78)

    if len(apr3) == 0:
        print("No Apr 3 data")
    else:
        a_apr3 = strategy_a_naive_crc(apr3)
        b_apr3 = strategy_b_multicriterion(apr3, 30.0)
        c_apr3, c_meta_apr3 = strategy_c_gas_event_aware(apr3)
        a_r, _, _ = usable_rate(a_apr3)
        b_r, _, _ = usable_rate(b_apr3)
        c_r, _, _ = usable_rate(c_apr3)
        print(f"A naive:          {len(a_apr3)} kept, {a_r:.1f}% usable")
        print(f"B multi-criterion: {len(b_apr3)} kept, {b_r:.1f}% usable")
        print(f"C gas-event aware: {len(c_apr3)} kept, {c_r:.1f}% usable, "
              f"{c_meta_apr3['gas_events_detected']} gas events detected")

    print()
    print("=" * 78)
    print("VERDICT — Does firmware alone recover the 66% -> 97% improvement?")
    print("=" * 78)

    if len(apr2) > 0:
        apr2_baseline = 100 * sum(1 for p in apr2 if not p["crc_error"]) / len(apr2)
        apr3_baseline = 100 * sum(1 for p in apr3 if not p["crc_error"]) / len(apr3) if len(apr3) > 0 else 0

        target_gain = apr3_baseline - apr2_baseline
        best_firmware_rate, _, _ = usable_rate(c_filtered)
        firmware_gain = best_firmware_rate - apr2_baseline

        recovery_pct = 100 * firmware_gain / target_gain if target_gain > 0 else 0

        print(f"Apr 2 raw baseline:      {apr2_baseline:.1f}%")
        print(f"Apr 3 raw (goal):        {apr3_baseline:.1f}%")
        print(f"Geometric gain (joint pull): {target_gain:+.1f} percentage points")
        print(f"")
        print(f"Best firmware strategy (C): {best_firmware_rate:.1f}%")
        print(f"Firmware gain:              {firmware_gain:+.1f} percentage points")
        print(f"Gain recovered in software: {recovery_pct:.0f}% of the hardware gain")
        print(f"")
        if recovery_pct >= 80:
            print("VERDICT: Firmware SUBSTANTIALLY recovers the hardware benefit.")
            print("         RT4 collector sub hardware case weakens significantly.")
        elif recovery_pct >= 50:
            print("VERDICT: Firmware PARTIALLY recovers the hardware benefit.")
            print("         Both tracks have merit — hardware for raw signal, firmware for recovery.")
        else:
            print("VERDICT: Firmware CANNOT substitute for the geometric change.")
            print("         RT4 collector sub hardware case survives.")
        print("")
        print("CAVEAT: This is a proof-of-concept on one well's data. Production firmware")
        print("        would need: burst-length tuning, per-well calibration, edge-case")
        print("        handling for data gaps > 30 min, and integration testing with the")
        print("        surface SCADA. 2-3 week prototyping effort is realistic.")

    print()
    print("=" * 78)
    print("LIMITATIONS OF FIRMWARE-ONLY APPROACH")
    print("=" * 78)
    print("1. Interpolated points are ESTIMATES, not measurements. OK for trending,")
    print("   not for leak detection or pump-off diagnosis during the gas event.")
    print("2. Cannot recover information that was never transmitted — if a burst lasts")
    print("   longer than interp_gap_min, there is a real data gap.")
    print("3. Hardware (collector sub) REDUCES the gas events in the first place.")
    print("   Firmware only mitigates them after they happen.")
    print("4. Slug damping (the highest-confidence RT4 benefit) is NOT recoverable in")
    print("   firmware — it only exists because a physical restriction fragmented slugs.")


if __name__ == "__main__":
    main()
