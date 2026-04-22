#!/usr/bin/env python3
"""
Part 1 — Explore the Dataset
=============================
Goal: Load the OASIS3 PIB PET data, inspect its structure, and produce a
      summary of subjects and measurements.

Pre-built for you
-----------------
  utils/oasis_utils.py  — all data-loading and ID-parsing helpers

Your tasks (search for TODO)
-----------------------------
  TODO 1  Load the dataset
  TODO 2  Filter to PIB tracer only and drop rows with missing values
  TODO 3  Add a simplified subject ID column
  TODO 4  Add columns for days and years since each subject's first scan
  TODO 5  Print a summary: subjects, measurements, Centiloid statistics
  TODO 6  Plot a histogram of measurements per subject

Run this script:
    python part1_explore.py

Expected output:
    A printed summary table and a saved figure: results/measurements_per_subject.png
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Make sure the utils folder is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.oasis_utils import (
    load_dataset,
    validate_columns,
    add_extracted_subject_id,
    add_days_since_start_from_id,
    ensure_dir,
)

# ── Configuration ────────────────────────────────────────────────────────────
DATA_PATH   = os.path.join("data", "OASIS3_PUP.xlsx")
RESULTS_DIR = "results"

TRACER    = "PIB"
ID_COL    = "PUP_PUPTIMECOURSEDATA ID"
SUVR_COL  = "Centil_fSUVR_TOT_CORTMEAN"   # Centiloid (non-RSF)

# ─────────────────────────────────────────────────────────────────────────────


def main():
    ensure_dir(RESULTS_DIR)

    # ── TODO 1 ───────────────────────────────────────────────────────────────
    # Load the dataset using load_dataset().
    # Store the result in a variable called `df`.
    #
    # Hint: load_dataset() accepts a file path string and returns a DataFrame.
    #
    # YOUR CODE HERE
    # df = ...
    raise NotImplementedError("TODO 1: load the dataset")

    # ── TODO 2 ───────────────────────────────────────────────────────────────
    # a) Validate that ID_COL, SUVR_COL, and 'tracer' exist in df.
    #    Use validate_columns(df, [ID_COL, SUVR_COL, 'tracer'])
    #
    # b) Keep only rows where the 'tracer' column equals TRACER ('PIB').
    #
    # c) Drop rows where ID_COL or SUVR_COL is NaN.
    #    Hint: df.dropna(subset=[...])
    #
    # After this step, print how many rows remain.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 2: filter to PIB and drop NaNs")

    # ── TODO 3 ───────────────────────────────────────────────────────────────
    # Add a 'Subject_ID_Extracted' column by calling add_extracted_subject_id().
    # This parses the short subject ID (e.g. 'OAS30001') from the full
    # measurement ID string (e.g. 'OAS30001_PIB_PUPTIMECOURSE_d0423').
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 3: add extracted subject ID")

    # ── TODO 4 ───────────────────────────────────────────────────────────────
    # Add time columns by calling add_days_since_start_from_id().
    # This parses the day offset from the ID string and converts it to years.
    # Use output_days='Days' and output_years='Years'.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 4: add days/years columns")

    # ── TODO 5 ───────────────────────────────────────────────────────────────
    # Print the following summary to the terminal:
    #
    #   Total subjects  : <number of unique Subject_ID_Extracted values>
    #   Total measurements : <total number of rows>
    #
    #   Centiloid statistics (all measurements):
    #     min   : <value>
    #     max   : <value>
    #     mean  : <value>
    #     median: <value>
    #
    # Hint: df['Subject_ID_Extracted'].nunique()
    #       df[SUVR_COL].describe()
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 5: print summary statistics")

    # ── TODO 6 ───────────────────────────────────────────────────────────────
    # Plot a histogram showing the distribution of measurements per subject.
    #
    # Steps:
    #   a) Count how many measurements each subject has:
    #        counts = df.groupby('Subject_ID_Extracted').size()
    #
    #   b) Plot counts as a histogram (try bins=range(1, counts.max()+2)).
    #
    #   c) Label the x-axis "Measurements per Subject" and y-axis "Number of Subjects".
    #      Add a title. Remove top and right spines for a clean look.
    #
    #   d) Save to results/measurements_per_subject.png at dpi=200.
    #      Use plt.tight_layout() before saving.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 6: plot histogram of measurements per subject")

    # ── Reflection questions ──────────────────────────────────────────────────
    # Answer these in comments below (no code needed):
    #
    # Q1. How many subjects have only a single PIB scan?
    #     Why might these subjects be less useful for studying progression?
    #
    # Q2. What does a Centiloid value of 0 represent? What about 100?
    #     (Hint: look up the Centiloid standardisation paper.)
    #
    # Q3. Look at the range of Centiloid values. What does the distribution
    #     suggest about the population in this dataset?


if __name__ == "__main__":
    main()
