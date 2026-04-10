"""
well_data.py
Parses the directional survey CSV and provides 3D well path data
for Manim visualizations of OBE 102 Hz 16-18-083-17W5/09.

Coordinate system (1 Manim unit = 100 meters):
    X = East / 100
    Y = North / 100
    Z = -TVD / 100  (surface = 0, deeper = more negative)
"""

import csv
import os
import numpy as np

# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

_CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "Directional Surveys and Logs",
    "DS_0517936_02-16-18-083-17W5-09_33494261.csv",
)
# Normalise to absolute path regardless of working directory
_CSV_PATH = os.path.normpath(_CSV_PATH)

_SKIP_ROWS = 26  # Skip 24 metadata lines + 1 column-names row + 1 units row = 26 total
                 # Data begins at 0-indexed line 26 (1-indexed line 27, MD=0 surface station)

def _parse_survey() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (md, inc, tvd, north, east) as 1-D float arrays."""
    md_list, inc_list, tvd_list, north_list, east_list = [], [], [], [], []

    with open(_CSV_PATH, newline="", encoding="utf-8-sig") as fh:
        # Skip metadata, column-names, and units rows
        for _ in range(_SKIP_ROWS):
            next(fh)

        reader = csv.reader(fh)
        for row in reader:
            if not row or not row[0].strip():
                continue
            try:
                md_val = float(row[0].strip())
                inc_val = float(row[1].strip())
                tvd_val = float(row[3].strip())
                north_val = float(row[6].strip())
                east_val = float(row[7].strip())
            except (ValueError, IndexError):
                continue  # skip malformed rows
            md_list.append(md_val)
            inc_list.append(inc_val)
            tvd_list.append(tvd_val)
            north_list.append(north_val)
            east_list.append(east_val)

    return (
        np.array(md_list, dtype=float),
        np.array(inc_list, dtype=float),
        np.array(tvd_list, dtype=float),
        np.array(north_list, dtype=float),
        np.array(east_list, dtype=float),
    )


_md_raw, _inc_raw, _tvd_raw, _north_raw, _east_raw = _parse_survey()

# ---------------------------------------------------------------------------
# Public numpy arrays
# ---------------------------------------------------------------------------

WELL_MD: np.ndarray = _md_raw
"""Measured depth (m) for each survey station, shape (N,)."""

WELL_INC: np.ndarray = _inc_raw
"""Inclination (degrees) for each survey station, shape (N,)."""

WELL_TVD: np.ndarray = _tvd_raw
"""True vertical depth (m) for each survey station, shape (N,)."""

# 3-D coordinates in Manim units (1 unit = 100 m)
_x = _east_raw / 100.0
_y = _north_raw / 100.0
_z = -_tvd_raw / 100.0

WELL_PATH_3D: np.ndarray = np.column_stack((_x, _y, _z))
"""
3-D Manim coordinates for each survey station, shape (N, 3).
Columns: [X=East/100, Y=North/100, Z=-TVD/100]
"""

# ---------------------------------------------------------------------------
# Interpolation helpers
# ---------------------------------------------------------------------------

def md_to_3d(md_value: float) -> np.ndarray:
    """
    Interpolate the Manim 3-D coordinate [x, y, z] at any measured depth.

    Parameters
    ----------
    md_value : float
        Measured depth in metres.

    Returns
    -------
    np.ndarray of shape (3,): [x, y, z] in Manim units.
    """
    x = float(np.interp(md_value, WELL_MD, _x))
    y = float(np.interp(md_value, WELL_MD, _y))
    z = float(np.interp(md_value, WELL_MD, _z))
    return np.array([x, y, z])


def md_to_index(md_value: float) -> int:
    """
    Return the index of the survey station nearest to *md_value*.

    Parameters
    ----------
    md_value : float
        Measured depth in metres.

    Returns
    -------
    int: index into WELL_MD / WELL_PATH_3D.
    """
    return int(np.argmin(np.abs(WELL_MD - md_value)))


# ---------------------------------------------------------------------------
# Key depth constants  (verified against run3-narrative.md)
# ---------------------------------------------------------------------------

SURFACE_CASING_MD = 126.0       # m MD — surface casing shoe
BUILD_START_MD = 370.0          # m MD — start of build section
BLUESKY_TOP_TVD = 660.5         # m TVD — top of Bluesky formation (GR drop ~790m MD)
WELLFI_POSITION_MD = 819.9      # m MD — WellFi after pulling 1 joint (Run 3)
WELLFI_ON_BOTTOM_MD = 832.3     # m MD — original WellFi position (Run 3 first set)
WELLFI_TVD = 663.1              # m TVD — WellFi depth (Run 3)
CASING_SHOE_MD = 921.0          # m MD — production casing shoe
JOINT_LENGTH = 9.456            # m — tubing joint length (85 joints, 803.76m tubing)
TD_MD = 2511.0                  # m MD — total depth (projection to TD)

# ---------------------------------------------------------------------------
# Signal data from Run-In-Hole (Run 3)
# ---------------------------------------------------------------------------

PEAK_SIGNAL_MD = 160.9          # m MD — peak signal (-37 dBV)
FLUID_CONTACT_MD = 482.4        # m MD — pressure jumps to 1.20 BAR
NOISE_FLOOR_DBV = -95.0         # dBV — noise floor reference

SIGNAL_DEPTH_POINTS: list[dict] = [
    {"md": 113.6,  "signal_dbv": -51,  "label": "First signal"},
    {"md": 160.9,  "signal_dbv": -37,  "label": "Peak signal"},
    {"md": 482.4,  "signal_dbv": -55,  "label": "Hit fluid",   "pressure_bar": 1.20},
    {"md": 662.1,  "signal_dbv": -88,  "label": "Deep in fluid"},
    {"md": 832.3,  "signal_dbv": -96,  "label": "On bottom",   "pressure_bar": 20.79},
    {"md": 832.3,  "signal_dbv": -100, "label": "Noise floor"},
]

# ---------------------------------------------------------------------------
# Colour palette — "Subterranean Signal"
# ---------------------------------------------------------------------------

BG      = "#06090f"
CYAN    = "#00D4FF"
AMBER   = "#F5A623"
GREEN   = "#2dd4a8"
CRIMSON = "#dc2626"
WHITE   = "#f0f4f8"
DIM     = "#8b95a5"
MONO    = "Consolas"
