#!/usr/bin/env python3
"""
Pre-built utility functions for the PET Progression Analysis problem set.

These are provided to you — you do not need to modify this file.
Read through the function signatures and docstrings so you know what
tools are available to call in parts 1–4.
"""

from __future__ import annotations

import os
import re
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dataset(input_path: str) -> pd.DataFrame:
    """Load a dataset from a CSV or Excel file.

    Args:
        input_path: Path to a .csv, .xlsx, or .xls file.

    Returns:
        DataFrame with all rows and columns from the file.
    """
    lower = input_path.lower()
    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(input_path)
    if lower.endswith(".csv"):
        return pd.read_csv(input_path)
    raise ValueError(f"Unsupported file type: {input_path}")


def validate_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> None:
    """Raise an informative error if any required columns are missing.

    Args:
        df: DataFrame to check.
        required_columns: Column names that must be present.
    """
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required column(s): {missing}\n"
            f"Available columns: {list(df.columns)}"
        )


def ensure_dir(path: str) -> str:
    """Create a directory (and any parents) if it doesn't already exist.

    Args:
        path: Directory path to create.

    Returns:
        The same path, for convenience.
    """
    os.makedirs(path, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Subject ID and time extraction
# ---------------------------------------------------------------------------

def extract_subject_id(
    complex_id: object,
    regex: str = r"OAS3(\d+)_",
    fmt: str = "OAS3{num}",
) -> str:
    """Parse a simplified subject ID from an OASIS3 measurement ID string.

    Example:
        'OAS30001_PIB_PUPTIMECOURSE_d0423'  →  'OAS30001'

    Args:
        complex_id: The full measurement ID string.
        regex: Regex pattern with one capture group for the numeric part.
        fmt: Format string using {num} to reconstruct the subject ID.

    Returns:
        Simplified subject ID, or the original string if no match.
    """
    match = re.match(regex, str(complex_id))
    if match:
        groupdict = match.groupdict()
        num = groupdict.get("num", match.group(1))
        return fmt.format(num=num)
    return str(complex_id)


def add_extracted_subject_id(
    df: pd.DataFrame,
    id_column: str,
    regex: str = r"OAS3(\d+)_",
    fmt: str = "OAS3{num}",
    output_column: str = "Subject_ID_Extracted",
) -> pd.DataFrame:
    """Add a 'Subject_ID_Extracted' column by parsing the measurement ID.

    Args:
        df: Input DataFrame containing the complex ID column.
        id_column: Name of the column with measurement IDs.
        output_column: Name for the new simplified ID column.

    Returns:
        Copy of df with the new column added.
    """
    result = df.copy()
    result[output_column] = result[id_column].apply(
        lambda x: extract_subject_id(x, regex, fmt)
    )
    return result


def extract_days_since_start_from_id(complex_id: object) -> Optional[int]:
    """Parse the days-since-baseline from an OASIS3 measurement ID.

    Example:
        'OAS30001_PIB_PUPTIMECOURSE_d0423'  →  423

    Args:
        complex_id: The full measurement ID string.

    Returns:
        Integer day count, or None if not found.
    """
    s = str(complex_id)
    matches = re.findall(r"_d\s*(\d+)", s, flags=re.IGNORECASE)
    if matches:
        try:
            return int(matches[-1])
        except Exception:
            return None
    tail = re.search(r"(?:^|_)[dD]\s*(\d+)(?:$|[^0-9])", s)
    if tail:
        try:
            return int(tail.group(1))
        except Exception:
            return None
    return None


def add_days_since_start_from_id(
    df: pd.DataFrame,
    id_column: str,
    output_days: str = "Days",
    output_years: Optional[str] = "Years",
) -> pd.DataFrame:
    """Add columns for days and years since baseline, parsed from the ID string.

    Args:
        df: Input DataFrame.
        id_column: Column containing measurement IDs with embedded day offsets.
        output_days: Name for the days column.
        output_years: Name for the years column (days / 365). Pass None to skip.

    Returns:
        Copy of df with the new time columns added.
    """
    result = df.copy()
    result[output_days] = result[id_column].apply(extract_days_since_start_from_id)
    if output_years is not None:
        result[output_years] = result[output_days].astype(float) / 365.0
    return result


def get_multi_sample_subjects(df: pd.DataFrame, subject_column: str) -> List[str]:
    """Return a list of subject IDs that have more than one measurement.

    Args:
        df: DataFrame with one row per measurement.
        subject_column: Column identifying subjects.

    Returns:
        List of subject IDs with ≥2 measurements.
    """
    counts = df[subject_column].value_counts()
    return counts[counts > 1].index.tolist()


# ---------------------------------------------------------------------------
# Demographics
# ---------------------------------------------------------------------------

def classify_apoe4_status(apoe_value: object) -> str:
    """Convert a raw APOE genotype code to 'APOE4+', 'APOE4-', or 'Unknown'.

    APOE genotype codes (e.g. 34, 44, 33, 23):
        - 34 or 44 → carries at least one ε4 allele → 'APOE4+'
        - 33, 23, 22 → no ε4 allele → 'APOE4-'
        - NaN or 0 → 'Unknown'

    Args:
        apoe_value: Numeric APOE genotype (e.g. 34.0).

    Returns:
        String label.
    """
    if pd.isna(apoe_value) or apoe_value == 0.0:
        return "Unknown"
    apoe_str = str(int(float(apoe_value)))
    return "APOE4+" if "4" in apoe_str else "APOE4-"


def classify_gender(gender_value: object) -> str:
    """Convert a numeric OASIS3 gender code to 'Male', 'Female', or 'Unknown'.

    OASIS3 codes: 1 = Male, 2 = Female.

    Args:
        gender_value: Numeric gender code.

    Returns:
        String label.
    """
    if pd.isna(gender_value):
        return "Unknown"
    code = float(gender_value)
    if code == 1.0:
        return "Male"
    if code == 2.0:
        return "Female"
    return "Unknown"


def load_and_merge_demographics(
    main_df: pd.DataFrame,
    demographics_path: str,
    subject_id_column: str = "Subject_ID_Extracted",
    demographics_id_column: str = "OASISID",
    apoe_column: str = "APOE",
) -> pd.DataFrame:
    """Load the demographics file and left-join it onto the main dataset.

    Adds the following columns to the returned DataFrame:
        - APOE4_Status ('APOE4+', 'APOE4-', 'Unknown')
        - Gender_Status ('Male', 'Female', 'Unknown')  [if GENDER column exists]
        - AgeatEntry, EDUC, race  [if present in demographics file]

    Args:
        main_df: Main PET measurements DataFrame.
        demographics_path: Path to the demographics Excel/CSV file.
        subject_id_column: Column in main_df used as the join key.
        demographics_id_column: Column in demographics used as the join key.
        apoe_column: Column in demographics containing raw APOE genotype codes.

    Returns:
        Merged DataFrame. Rows without a demographics match keep NaN in the
        added columns (left join).
    """
    try:
        demo = load_dataset(demographics_path)
    except Exception as e:
        print(f"Warning: Could not load demographics — {e}")
        return main_df

    if demographics_id_column not in demo.columns:
        print(f"Warning: '{demographics_id_column}' not found in demographics file.")
        return main_df
    if apoe_column not in demo.columns:
        print(f"Warning: '{apoe_column}' not found in demographics file.")
        return main_df

    demo["APOE4_Status"] = demo[apoe_column].apply(classify_apoe4_status)

    merge_cols = [demographics_id_column, apoe_column, "APOE4_Status"]

    if "GENDER" in demo.columns:
        demo["Gender_Status"] = demo["GENDER"].apply(classify_gender)
        merge_cols.append("Gender_Status")

    for col in ["GENDER", "AgeatEntry", "EDUC", "race"]:
        if col in demo.columns:
            merge_cols.append(col)

    merged = main_df.merge(
        demo[merge_cols],
        left_on=subject_id_column,
        right_on=demographics_id_column,
        how="left",
    )

    total = main_df[subject_id_column].nunique()
    matched = merged.loc[merged["APOE4_Status"].notna(), subject_id_column].nunique()
    print(f"Demographics merged: {matched}/{total} subjects matched.")

    return merged


# ---------------------------------------------------------------------------
# Slope computation
# ---------------------------------------------------------------------------

def compute_subject_slopes(
    df: pd.DataFrame,
    subject_column: str,
    suvr_column: str,
    order_by_column: Optional[str] = None,
) -> pd.DataFrame:
    """Compute each subject's initial Centiloid value and rate of change.

    For each subject with ≥2 measurements and valid time data, fits a
    simple linear regression (Centiloid ~ Years) and records:
        - Subject_ID
        - Initial_SUVR   : Centiloid value at the earliest time point
        - Rate_of_Change : slope of the linear fit (Centiloids / year)
        - Num_Measurements : number of scans used

    Subjects with only one scan or missing time values are skipped.

    Args:
        df: DataFrame with one row per measurement.
        subject_column: Column identifying subjects.
        suvr_column: Column containing Centiloid (or SUVR) values.
        order_by_column: Column containing time values (e.g. 'Years').

    Returns:
        DataFrame with one row per subject.
    """
    records: List[dict] = []

    for subject_id, sdf in df.groupby(subject_column):
        sdf = sdf.copy()

        if len(sdf) < 2:
            continue

        if (
            order_by_column is None
            or order_by_column not in sdf.columns
            or not np.issubdtype(sdf[order_by_column].dtype, np.number)
            or sdf[order_by_column].isna().all()
        ):
            continue

        sdf = sdf.sort_values(order_by_column)
        x = sdf[order_by_column].to_numpy()
        y = sdf[suvr_column].to_numpy()
        slope = np.polyfit(x, y, 1)[0]

        record: dict = {
            "Subject_ID": subject_id,
            "Initial_SUVR": float(y[0]),
            "Rate_of_Change": float(slope),
            "Num_Measurements": int(len(sdf)),
        }

        for col in ("tracer", "APOE4_Status", "Gender_Status"):
            if col in sdf.columns:
                record[col] = sdf[col].iloc[0]

        records.append(record)

    return pd.DataFrame(records)
