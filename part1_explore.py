#!/usr/bin/env python3
"""
Part 1 — Explore the Dataset
=============================
Goal: Load the OASIS3 PIB PET data, inspect its structure, and produce a
      summary of subjects and measurements.

Available helpers (utils/oasis_utils.py)
-----------------------------------------
Read through utils/oasis_utils.py before starting — the docstrings tell you
exactly what each function expects and returns.

  load_dataset(path)
      Loads an Excel or CSV file and returns a pandas DataFrame.

  validate_columns(df, cols)
      Raises an error if any column in `cols` is missing from df.
      Useful for catching typos early.

  add_extracted_subject_id(df, id_col)
      Parses the short subject ID (e.g. 'OAS30001') from the full measurement
      ID string (e.g. 'OAS30001_PIB_PUPTIMECOURSE_d0423').
      Adds a new column 'Subject_ID_Extracted' to df and returns it.

  add_days_since_start_from_id(df, id_col, output_days, output_years)
      Parses the day offset from the ID string and converts it to years.
      Adds two new columns (named by output_days and output_years) and returns df.

  ensure_dir(path)
      Creates a directory if it does not already exist.

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

TRACER   = "PIB"
ID_COL   = "PUP_PUPTIMECOURSEDATA ID"
SUVR_COL = "Centil_fSUVR_TOT_CORTMEAN"   # Centiloid (non-RSF)

# ─────────────────────────────────────────────────────────────────────────────


def main():
    ensure_dir(RESULTS_DIR)

    # ── TODO 1 ───────────────────────────────────────────────────────────────
    # Load the dataset using load_dataset().
    # Store the result in a variable called `df`.
    #
    # load_dataset(path) → DataFrame
    #   Accepts a file path string and returns a pandas DataFrame.
    #
    # YOUR CODE HERE
    # df = ...

    # When done, remove the NotImplementedError and uncomment the line below
    # to confirm the data loaded correctly before moving on:
    # print(df.head())

    raise NotImplementedError("TODO 1: load the dataset")

    # ── TODO 2 ───────────────────────────────────────────────────────────────
    # a) Validate that ID_COL, SUVR_COL, and 'tracer' exist in df.
    #    validate_columns(df, cols) → None  (raises an error if a column is missing)
    #
    # b) Keep only rows where the 'tracer' column equals TRACER ('PIB').
    #
    # c) Drop rows where ID_COL or SUVR_COL is NaN.
    #    Hint: df.dropna(subset=[...])
    #
    # YOUR CODE HERE

    # Uncomment to confirm the filter worked — you should see only PIB rows:
    # print(df.head())

    raise NotImplementedError("TODO 2: filter to PIB and drop NaNs")

    # ── TODO 3 ───────────────────────────────────────────────────────────────
    # Add a 'Subject_ID_Extracted' column by calling add_extracted_subject_id().
    #
    # add_extracted_subject_id(df, id_col) → DataFrame
    #   id_col : the name of the full measurement ID column (use ID_COL)
    #   Returns df with a new column 'Subject_ID_Extracted' added.
    #   Example: 'OAS30001_PIB_PUPTIMECOURSE_d0423' → 'OAS30001'
    #
    # YOUR CODE HERE
    # df = add_extracted_subject_id(df, ...)

    # Uncomment to confirm the new column looks right:
    # print(df[['Subject_ID_Extracted', ID_COL]].head())

    raise NotImplementedError("TODO 3: add extracted subject ID")

    # ── TODO 4 ───────────────────────────────────────────────────────────────
    # Add time columns by calling add_days_since_start_from_id().
    #
    # add_days_since_start_from_id(df, id_col, output_days, output_years) → DataFrame
    #   id_col       : the full measurement ID column (use ID_COL)
    #   output_days  : name for the new days column  → use 'Days'
    #   output_years : name for the new years column → use 'Years'
    #   Returns df with two new columns added.
    #
    # YOUR CODE HERE
    # df = add_days_since_start_from_id(df, ..., output_days=..., output_years=...)

    # Uncomment to confirm both new columns appeared and the values look sensible:
    # print(df[['Subject_ID_Extracted', ID_COL, 'Days', 'Years']].head())

    raise NotImplementedError("TODO 4: add days/years columns")

    # ── TODO 5 ───────────────────────────────────────────────────────────────
    # Print the following summary to the terminal:
    #
    #   Total subjects     : <number of unique Subject_ID_Extracted values>
    #   Total measurements : <total number of rows>
    #
    #   Centiloid statistics (all measurements):
    #     min   : <value>
    #     max   : <value>
    #     mean  : <value>
    #     median: <value>
    #
    # Hints:
    #   df['Subject_ID_Extracted'].nunique()  — number of unique subjects
    #   df[SUVR_COL].describe()               — returns a Series with min, max, mean, 50%
    #
    # Notice anything interesting about the mean vs median?
    # Think about what a large gap between them might tell you about this population.
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
    #   b) Use np.histogram() to compute bin counts and edges from `counts`.
    #      Hint: np.histogram(values, bins=range(1, counts.max() + 2))
    #      This gives you fine-grained control over bin placement compared to
    #      passing data directly to plt.hist().
    #
    #   c) Plot using plt.bar() with the bin edges and counts from step b.
    #      Hint: plt.bar(bins[:-1], hist_counts, width=np.diff(bins), ...)
    #
    #   d) Label axes ("Measurements per Subject", "Number of Subjects"),
    #      add a title, and remove the top and right spines for a clean look.
    #
    #   e) Call plt.tight_layout(), then save to:
    #        results/measurements_per_subject.png  at dpi=200
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
    # Q3. Look at the mean vs median Centiloid values — they differ quite a bit.
    #     What does that gap suggest about the distribution of amyloid burden
    #     in this dataset? What might it mean for interpreting the mean alone?


if __name__ == "__main__":
    main()
