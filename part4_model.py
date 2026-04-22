#!/usr/bin/env python3
"""
Part 4 — Fit a Rate Model and Integrate a Trajectory
=====================================================
Goal: Turn the scatter of rates from Part 3 into a smooth mathematical
      model, then use that model to simulate how amyloid accumulates
      over decades — starting from a near-zero baseline.

The key idea
------------
In Part 3 you computed each subject's Rate of Change (Centiloids/year)
as a function of their Initial Centiloid value.  Here we treat that
relationship as a differential equation:

    dS/dt  =  f(S)

where S is the current Centiloid value and f is a smooth curve fit to
the scatter of observed rates.  Integrating this ODE forward from a
low starting value gives a predicted long-term trajectory.

Pre-built for you
-----------------
  utils/oasis_utils.py      — data helpers and compute_subject_slopes()
  _load_pib_data()          — same filtering helper as Parts 2–3
  fit_spline()              — STUB: you complete the body (TODO A)
  rate_function()           — STUB: you complete the body (TODO B)
  integrate_trajectory()    — STUB: you complete the body (TODO C)

Your tasks (search for TODO)
-----------------------------
  TODO A  Complete fit_spline()         — fit spline to rate scatter
  TODO B  Complete rate_function()      — wrap model as a callable
  TODO C  Complete integrate_trajectory() — solve the ODE
  TODO 1  Load rates, convert units, call fit_spline()
  TODO 2  Plot the spline fit over the scatter and save
  TODO 3  Call integrate_trajectory() and plot the trajectory

Run this script:
    python part4_model.py

Expected output:
    results/rate_spline_fit.png
    results/trajectory.png
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# sklearn and scipy are used inside the stubs you will complete
from sklearn.preprocessing import SplineTransformer
from sklearn.linear_model import LinearRegression
from scipy.integrate import solve_ivp

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

# Starting Centiloid value for the ODE integration (near-zero / amyloid-negative)
S0_CENTILOID = 14.86          # corresponds to PIB SUVR 1.2 (amyloid-negative threshold)
INTEGRATION_YEARS = 35.0      # how far to project forward (years)

# Spline knot positions in Centiloid units.
# Knots define where the spline is allowed to change shape.
KNOTS_CENTILOID = [14.86, 50.0]
# ─────────────────────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════════════
# STUB FUNCTIONS — complete the bodies of these three functions.
# Each stub has a detailed docstring telling you exactly what to do.
# ═══════════════════════════════════════════════════════════════════════════

def fit_spline(x: np.ndarray, y: np.ndarray, knots: list):
    """Fit a cubic spline to the rate-vs-initial-Centiloid scatter.

    We use scikit-learn's SplineTransformer to create basis functions and
    LinearRegression to fit the coefficients.  This gives a smooth curve
    that respects the data near the knots and extrapolates linearly beyond.

    Args:
        x      : 1-D array of Initial Centiloid values (one per subject).
        y      : 1-D array of Rate of Change values (Centiloids/year).
        knots  : List of knot positions in Centiloid units, e.g. [14.86, 50.0].
                 These are the x-values where the spline is allowed to bend.

    Returns:
        model       : Fitted sklearn LinearRegression object.
        transformer : Fitted SplineTransformer object.

    # ── TODO A ───────────────────────────────────────────────────────────────
    # Step 1 — Reshape x to a 2-D column vector:
    #               X = x.reshape(-1, 1)
    #
    # Step 2 — Convert the knots list to a 2-D array of shape (n_knots, 1):
    #               knots_2d = np.array(knots).reshape(-1, 1)
    #
    # Step 3 — Create the SplineTransformer:
    #               spline_transformer = SplineTransformer(
    #                   n_knots      = len(knots),
    #                   degree       = 3,
    #                   knots        = knots_2d,
    #                   extrapolation= 'linear',   # linear outside knot range
    #               )
    #
    # Step 4 — Fit and transform X:
    #               X_spline = spline_transformer.fit_transform(X)
    #
    # Step 5 — Fit a LinearRegression on the transformed features:
    #               model = LinearRegression()
    #               model.fit(X_spline, y)
    #
    # Step 6 — Return model, spline_transformer
    """
    # YOUR CODE HERE
    raise NotImplementedError("TODO A: complete fit_spline()")


def rate_function(model, transformer):
    """Return a callable that predicts dS/dt given the current Centiloid S.

    This wraps the fitted spline model so it can be passed to solve_ivp,
    which expects a function of the form  f(t, S).

    Args:
        model       : Fitted LinearRegression (from fit_spline).
        transformer : Fitted SplineTransformer (from fit_spline).

    Returns:
        A function  f(S)  that accepts a scalar or array S and returns
        the predicted rate of change (Centiloids/year).

    # ── TODO B ───────────────────────────────────────────────────────────────
    # Define and return an inner function called `f`:
    #
    #   def f(S):
    #       S_arr = np.atleast_1d(S).astype(float)      # ensure array
    #       X     = transformer.transform(S_arr.reshape(-1, 1))
    #       return model.predict(X)                      # shape (n,)
    #   return f
    #
    # The returned function f is the dS/dt model — call it with a Centiloid
    # value and it returns the predicted accumulation rate.
    """
    # YOUR CODE HERE
    raise NotImplementedError("TODO B: complete rate_function()")


def integrate_trajectory(rate_fn, s0: float, t_span: tuple, t_eval: np.ndarray):
    """Simulate the Centiloid trajectory by integrating the rate ODE.

    Solves the initial-value problem:
        dS/dt = rate_fn(S),   S(0) = s0

    using scipy's solve_ivp with the RK45 (Runge-Kutta) integrator.

    Args:
        rate_fn : Callable returned by rate_function().
        s0      : Starting Centiloid value (e.g. 14.86).
        t_span  : (t_start, t_end) in years, e.g. (0, 35).
        t_eval  : 1-D array of time points at which to record the solution.

    Returns:
        t_vals : 1-D array of time points (years).
        s_vals : 1-D array of Centiloid values at each time point.

    Raises:
        RuntimeError if the integrator does not converge.

    # ── TODO C ───────────────────────────────────────────────────────────────
    # Step 1 — Define the ODE right-hand side that solve_ivp expects.
    #           solve_ivp calls rhs(t, y) where y is a list/array.
    #           We only have one state variable (S), so y = [S]:
    #
    #               def rhs(t, y):
    #                   return [rate_fn(y[0])[0]]    # must return a list
    #
    # Step 2 — Call solve_ivp:
    #               sol = solve_ivp(
    #                   rhs,
    #                   t_span = t_span,
    #                   y0     = [s0],
    #                   t_eval = t_eval,
    #                   method = 'RK45',
    #                   rtol   = 1e-6,
    #                   atol   = 1e-8,
    #               )
    #
    # Step 3 — Check that the solver succeeded:
    #               if not sol.success:
    #                   raise RuntimeError(f"Integration failed: {sol.message}")
    #
    # Step 4 — Return sol.t, sol.y[0]
    #           (sol.t = time points, sol.y[0] = S values at those times)
    """
    # YOUR CODE HERE
    raise NotImplementedError("TODO C: complete integrate_trajectory()")


# ═══════════════════════════════════════════════════════════════════════════
# Main workflow — complete the TODOs below after finishing the stubs above.
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ensure_dir(RESULTS_DIR)

    df = _load_pib_data()

    # ── TODO 1 ───────────────────────────────────────────────────────────────
    # a) Call compute_subject_slopes() (same arguments as Part 3) to get `rates`.
    #
    # b) The slopes in `rates` are already in Centiloid units because SUVR_COL
    #    is the Centiloid column — no unit conversion needed here.
    #    (If you were working with raw PIB SUVR values you would convert with:
    #     Centiloid = 111.8 * SUVR - 119.3)
    #
    # c) Extract numpy arrays:
    #        x = rates['Initial_SUVR'].to_numpy()
    #        y = rates['Rate_of_Change'].to_numpy()
    #
    # d) Call fit_spline(x, y, KNOTS_CENTILOID) → store as (model, transformer).
    #
    # e) Print:
    #        Subjects used for fitting: <n>
    #        Knots (Centiloid): <KNOTS_CENTILOID>
    #        S0 (Centiloid): <S0_CENTILOID>
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 1: load rates and fit spline")

    # ── TODO 2 ───────────────────────────────────────────────────────────────
    # Plot the spline fit over the rate scatter.
    #
    # a) Create the rate callable:
    #        rate_fn = rate_function(model, transformer)
    #
    # b) Build a smooth x-grid from min(x) to 120 Centiloids (300 points):
    #        x_smooth = np.linspace(min(x.min(), S0_CENTILOID), 120.0, 300)
    #        y_smooth = rate_fn(x_smooth)
    #
    # c) Report the peak rate:
    #        peak_idx = np.argmax(y_smooth)
    #        print(f"Peak rate: {y_smooth[peak_idx]:.2f} CL/yr at {x_smooth[peak_idx]:.1f} CL")
    #
    # d) Create figure, ax = plt.subplots(figsize=(9, 6))
    #    Plot:
    #      - Scatter of subject data (x, y): color='steelblue', alpha=0.4, s=35, zorder=2
    #      - Spline curve (x_smooth, y_smooth): color='steelblue', linewidth=2.5,
    #        label='Spline fit', zorder=3
    #
    # e) Add axis labels, title "Centiloid Accumulation Rate (Spline Fit)",
    #    legend, grid, remove top/right spines.
    #    Draw ax.axhline(0, color='black', lw=0.8, ls='--', alpha=0.5).
    #    Set ax.set_xlim(right=120).
    #
    # f) Save to results/rate_spline_fit.png at dpi=200. Print path.
    #    Close the figure.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 2: plot spline fit and save")

    # ── TODO 3 ───────────────────────────────────────────────────────────────
    # Integrate the ODE and plot the predicted trajectory.
    #
    # a) Build the time evaluation grid:
    #        t_eval = np.linspace(0, INTEGRATION_YEARS,
    #                             int(INTEGRATION_YEARS * 10) + 1)
    #
    # b) Call integrate_trajectory(rate_fn, S0_CENTILOID, (0, INTEGRATION_YEARS), t_eval)
    #    → store as (t_vals, s_vals)
    #
    # c) Print the Centiloid value at year 10, 20, and 35:
    #        for yr in [10, 20, 35]:
    #            idx = np.searchsorted(t_vals, yr)
    #            print(f"  Year {yr}: {s_vals[idx]:.1f} CL")
    #
    # d) Create figure, ax = plt.subplots(figsize=(9, 6))
    #    Plot (t_vals, s_vals):
    #      - color='steelblue', linewidth=2.5, label='Integrated trajectory'
    #    Mark S0 with a dot:
    #      - ax.scatter([0], [S0_CENTILOID], color='steelblue', s=60, zorder=5)
    #    Draw a horizontal reference at 17 CL (common positivity threshold):
    #      - ax.axhline(17, color='gray', lw=1.0, ls=':', alpha=0.7,
    #                   label='Positivity threshold (~17 CL)')
    #
    # e) Label axes: x "Time (Years)", y "Centiloid Value (non-RSF)"
    #    Title: "Predicted PIB Centiloid Trajectory"
    #    Add legend (frameon=False), grid, remove top/right spines.
    #
    # f) Save to results/trajectory.png at dpi=200. Print path.
    #
    # YOUR CODE HERE
    raise NotImplementedError("TODO 3: integrate ODE and plot trajectory")

    # ── Reflection questions ──────────────────────────────────────────────────
    # Q1. The spline model uses the population-average rate at each Centiloid
    #     level to simulate a single trajectory. What assumption does this make?
    #     Is it realistic?
    #
    # Q2. How many years does the model predict it takes to go from near-zero
    #     (S0 ≈ 15 CL) to amyloid-positive (≥ 17 CL)?  From 17 to 50 CL?
    #
    # Q3. The rate peaks at some intermediate Centiloid value, then declines
    #     at very high values. What biological process might explain the
    #     decline in accumulation rate at high amyloid burden?


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
