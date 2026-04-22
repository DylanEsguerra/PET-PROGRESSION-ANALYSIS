#!/usr/bin/env python3
"""
Part 3 — Compute and Plot Accumulation Rates
=============================================
Goal: Quantify how fast each subject's amyloid accumulates.
      We do this by fitting a simple linear regression to each
      subject's Centiloid measurements over time, giving us a
      slope (Centiloids/year).  Then we ask: does the rate depend
      on how much amyloid someone already has?

Pre-built for you
-----------------
  utils/oasis_utils.py          — data helpers
  compute_subject_slopes()      — fits per-subject linear regressions
                                  returns: Subject_ID, Initial_SUVR,
                                           Rate_of_Change, Num_Measurements
  _load_pib_data()              — same filtering helper as Part 2

Your tasks (search for TODO)
-----------------------------
  TODO 1  Call compute_subject_slopes() to get per-subject rates
  TODO 2  Print a statistical summary of the rates
  TODO 3  Plot Rate of Change vs Initial Centiloid (scatter)
  TODO 4  Add a zero-rate reference line and finalize the figure

Run this script:
    python part3_rates.py

Expected output:
    Printed rate statistics
    results/rate_vs_initial.png
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.oasis_utils import (
    load_dataset,
    validate_columns,
    add_extracted_subject_id,
    add_days_since_start_from_id,
    compute_subject_slopes,
    ensure_dir,
)

# ── Configuration ────────────────────────────────────────────────────────────
DATA_PATH   = os.path.join("data", "OASIS3_PUP.xlsx")
RESULTS_DIR = "results"

TRACER   = "PIB"
ID_COL   = "PUP_PUPTIMECOURSEDATA ID"
SUVR_COL = "Centil_fSUVR_TOT_CORTMEAN"
# ─────────────────────────────────────────────────────────────────────────────


def main():
    ensure_dir(RESULTS_DIR)

    df = _load_pib_data()

    # ── TODO 1 ───────────────────────────────────────────────────────────────
    # Call compute_subject_slopes() to get per-subject accumulation rates.
    #
    # Arguments:
    #   df             = df
    #   subject_column = 'Subject_ID_Extracted'
    #   suvr_column    = SUVR_COL
    #   order_by_column= 'Years'
    #
    # Store the result in a variable called `rates`.
    # It will be a DataFrame with columns:
    #   Subject_ID, Initial_SUVR, Rate_of_Change, Num_Measurements
    #
    # Print how many subjects are in `rates`.
    # (Note: subjects with only 1 scan are automatically excluded.)
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 1: compute per-subject slopes")

    # ── TODO 2 ───────────────────────────────────────────────────────────────
    # Print the following statistics about Rate_of_Change:
    #
    #   Mean rate   : <value> Centiloids/year
    #   Median rate : <value> Centiloids/year
    #   Std dev     : <value> Centiloids/year
    #   % positive  : <value>%   (fraction of subjects with rate > 0)
    #   % negative  : <value>%   (fraction with rate ≤ 0)
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 2: print rate statistics")

    # ── TODO 3 ───────────────────────────────────────────────────────────────
    # Create a scatter plot: Rate of Change (y) vs Initial Centiloid (x).
    # Encode additional information by varying the marker size.
    #
    # Steps:
    #   a) Create a figure: fig, ax = plt.subplots(figsize=(9, 6))
    #
    #   b) Call ax.scatter() using:
    #        x = rates['Initial_SUVR']
    #        y = rates['Rate_of_Change']
    #        s = rates['Num_Measurements'] * 20   (bubble size)
    #        color='steelblue', alpha=0.55,
    #        edgecolors='white', linewidths=0.5
    #
    #   c) Add axis labels (fontsize=13):
    #        x: "Initial Centiloid Value"
    #        y: "Rate of Change (Centiloids / Year)"
    #
    #   d) Add a title: "Amyloid Accumulation Rate vs Baseline Centiloid"
    #      fontsize=14, fontweight='bold'
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 3: scatter plot Rate of Change vs Initial Centiloid")

    # ── TODO 4 ───────────────────────────────────────────────────────────────
    # Add context lines and finalize the figure.
    #
    #   a) Draw a horizontal dashed line at y=0 to separate accumulating
    #      subjects (above) from declining/stable subjects (below):
    #        ax.axhline(0, color='black', linewidth=0.9, linestyle='--', alpha=0.5)
    #
    #   b) Add a small legend explaining the bubble size:
    #      Create two scatter handles manually, e.g.:
    #        from matplotlib.lines import Line2D
    #        handles = [
    #            Line2D([0],[0], marker='o', color='w', markerfacecolor='steelblue',
    #                   markersize=6,  label='2 scans'),
    #            Line2D([0],[0], marker='o', color='w', markerfacecolor='steelblue',
    #                   markersize=10, label='5 scans'),
    #        ]
    #        ax.legend(handles=handles, title='# Scans', frameon=False, fontsize=11)
    #
    #   c) Add a light grid: ax.grid(True, linestyle='--', alpha=0.15)
    #
    #   d) Remove top and right spines.
    #
    #   e) Call fig.tight_layout() then save to results/rate_vs_initial.png at dpi=200.
    #      Print the save path.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 4: add reference line, legend, and save")

    # ── Reflection questions ──────────────────────────────────────────────────
    # Q1. Is there a relationship between a subject's initial Centiloid value
    #     and their rate of accumulation? Describe what you see in the scatter.
    #
    # Q2. Some subjects have negative rates (Centiloids decreasing over time).
    #     What are two possible explanations for this?
    #
    # Q3. Why do we encode number of measurements as bubble size?
    #     How does this affect your interpretation of the scatter plot?


def _load_pib_data():
    """Load, filter, and time-stamp the PIB measurements. (Pre-built helper.)"""
    df = load_dataset(DATA_PATH)
    validate_columns(df, [ID_COL, SUVR_COL, "tracer"])
    df = df[df["tracer"] == TRACER].copy()
    df = df.dropna(subset=[ID_COL, SUVR_COL])
    df = add_extracted_subject_id(df, ID_COL)
    df = add_days_since_start_from_id(df, ID_COL, output_days="Days", output_years="Years")
    return df


if __name__ == "__main__":
    main()
