#!/usr/bin/env python3
"""
Part 2 — Plot Longitudinal PET Trajectories
============================================
Goal: Visualise how each subject's Centiloid value changes over time.
      A "trajectory" is simply the sequence of PET measurements for one
      person, plotted against years since their first scan.

Pre-built for you
-----------------
  utils/oasis_utils.py  — all data-loading and ID-parsing helpers
  _load_pib_data()      — defined at the bottom of this file; reuses
                          the same filtering steps you wrote in Part 1

Your tasks (search for TODO)
-----------------------------
  TODO 1  Loop over subjects and plot each trajectory
  TODO 2  Highlight one example subject with a thicker line
  TODO 3  Finalize and save the figure

Run this script:
    python part2_trajectories.py

Expected output:
    results/trajectories.png
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
    get_multi_sample_subjects,
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

    # Keep only subjects with ≥2 measurements (needed to draw a line)
    longitudinal_ids = get_multi_sample_subjects(df, "Subject_ID_Extracted")
    df_long = df[df["Subject_ID_Extracted"].isin(longitudinal_ids)].copy()

    print(f"Subjects with ≥2 scans: {len(longitudinal_ids)}")

    fig, ax = plt.subplots(figsize=(10, 6))

    # ── TODO 1 ───────────────────────────────────────────────────────────────
    # For each subject in df_long, plot their trajectory.
    #
    # Steps:
    #   a) Group df_long by 'Subject_ID_Extracted'.
    #
    #   b) For each group, sort by 'Years' so the line goes left → right.
    #
    #   c) Plot a line (ax.plot) connecting the subject's time points,
    #      and a scatter (ax.scatter) marking the individual measurements.
    #      Use:
    #        - color='steelblue'
    #        - alpha=0.25 for the line, alpha=0.35 for the scatter
    #        - linewidth=1.0, s=18 (marker size)
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 1: plot all subject trajectories")

    # ── TODO 2 ───────────────────────────────────────────────────────────────
    # Pick ONE subject to highlight so the reader can see a single example
    # clearly among all the others.
    #
    # Steps:
    #   a) Choose any subject ID from longitudinal_ids, e.g. longitudinal_ids[0],
    #      or pick one with many measurements:
    #        example_id = df_long.groupby('Subject_ID_Extracted').size().idxmax()
    #
    #   b) Filter df_long to just that subject, sort by 'Years'.
    #
    #   c) Re-plot their line with:
    #        - color='crimson', linewidth=2.5, zorder=5
    #        - label=f"Example: {example_id}"
    #      and their scatter with:
    #        - color='crimson', s=50, zorder=6, edgecolors='white', linewidths=0.6
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 2: highlight one example subject")

    # ── TODO 3 ───────────────────────────────────────────────────────────────
    # Finalize the figure:
    #
    #   a) Set axis labels:
    #        x: "Years Since First Scan"
    #        y: "Centiloid (non-RSF)"
    #      Use fontsize=13 for both.
    #
    #   b) Add a title: "Longitudinal PIB Centiloid Trajectories"
    #      fontsize=14, fontweight='bold'
    #
    #   c) Add a legend (ax.legend) showing only the highlighted subject.
    #      Use frameon=False.
    #
    #   d) Add a light grid: ax.grid(True, linestyle='--', alpha=0.2)
    #
    #   e) Remove the top and right spines:
    #        ax.spines['top'].set_visible(False)
    #        ax.spines['right'].set_visible(False)
    #
    #   f) Call fig.tight_layout() then save to results/trajectories.png at dpi=200.
    #      Print the save path when done.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 3: finalize and save the figure")

    # ── Reflection questions ──────────────────────────────────────────────────
    # Q1. Most subjects show relatively flat trajectories. A few show steep
    #     increases. What biological differences might explain this?
    #
    # Q2. Some subjects start with high Centiloid values (>50) and others
    #     start near zero. What could explain baseline differences?
    #
    # Q3. Does the rate of accumulation appear constant over time for most
    #     subjects, or does it seem to accelerate or decelerate?


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
