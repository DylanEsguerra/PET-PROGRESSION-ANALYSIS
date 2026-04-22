# PET Progression Analysis — Problem Set

A guided problem set for studying amyloid PET progression using the OASIS-3 dataset.  
You will load real amyloid PET data, visualise individual trajectories, quantify accumulation rates, and build a simple mathematical model of amyloid progression.

---

## Background

Amyloid-beta plaques accumulate in the brain years before symptoms of Alzheimer's disease appear.  
Positron emission tomography (PET) with the **PiB tracer** lets us quantify this accumulation in living people using a standardised unit called the **Centiloid (CL)**.

- **0 CL** = young amyloid-negative control (by definition)
- **100 CL** = typical mild-to-moderate Alzheimer's patient (by definition)
- **~17 CL** = commonly used positivity threshold

The OASIS-3 dataset contains longitudinal PiB PET scans from hundreds of cognitively normal and impaired older adults.  By tracking how each person's Centiloid value changes over repeated scans, we can estimate individual accumulation rates and model the progression curve from amyloid-negative to amyloid-positive.


---

## Dataset

This problem set uses two files from the [OASIS-3](https://www.oasis-brains.org/) project:

| File | Contents |
|------|----------|
| `data/OASIS3_PUP.xlsx` | PET measurements — one row per scan session |
| `data/OASIS3_demographics.xlsx` | Subject demographics (age, sex, APOE genotype) |

Key columns in `OASIS3_PUP.xlsx`:

| Column | Description |
|--------|-------------|
| `PUP_PUPTIMECOURSEDATA ID` | Measurement ID encoding subject, tracer, and days since first scan |
| `Centil_fSUVR_TOT_CORTMEAN` | Centiloid value (non-RSF, total cortical mean) |
| `tracer` | PET tracer used (we focus on `PIB`) |

---

## Setup

**1. Clone this repository**
```bash
git clone https://github.com/your-username/pet-progression-analysis.git
cd pet-progression-analysis
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv. # (use python3 if fails)
source .venv/bin/activate        # macOS 
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```


---

## Problem Set

Work through the four parts **in order** — each one builds on the previous.  
Each script contains numbered `TODO` sections with detailed instructions.  
Reflection questions at the end of each script require written answers (add them as comments).

### Part 1 — Explore the Dataset (`part1_explore.py`)
*Learn to load the data, understand its structure, and produce basic summary statistics.*

```bash
python part1_explore.py
```

**You will implement:**
- Loading and filtering the dataset to PIB scans only
- Extracting subject IDs and time offsets from the measurement ID strings
- Printing summary statistics (subjects, measurements, Centiloid range)
- Plotting a histogram of measurements per subject

**Expected output:** `results/measurements_per_subject.png`

---

### Part 2 — Longitudinal Trajectories (`part2_trajectories.py`)
*Visualise how each subject's amyloid load changes over time.*

```bash
python part2_trajectories.py
```

**You will implement:**
- Looping over subjects and plotting each individual trajectory
- Highlighting one example subject to guide the reader's eye
- Finalising the figure with labels, title, and clean styling

**Expected output:** `results/trajectories.png`

---

### Part 3 — Accumulation Rates (`part3_rates.py`)
*Quantify how fast amyloid accumulates, and ask whether the rate depends on baseline burden.*

```bash
python part3_rates.py
```

**You will implement:**
- Calling the pre-built `compute_subject_slopes()` function to get per-subject rates
- Printing rate statistics (mean, median, % positive)
- Scatter-plotting Rate of Change vs Initial Centiloid with bubble-size encoding

**Expected output:** `results/rate_vs_initial.png`

---

### Part 4 — Spline Model and ODE Integration (`part4_model.py`)
*Fit a smooth model to the rate scatter, then integrate it as an ODE to predict long-term progression.*

```bash
python part4_model.py
```

**You will implement (function stubs provided):**
- `fit_spline()` — fit a cubic spline using `SplineTransformer` + `LinearRegression`
- `rate_function()` — wrap the fitted model as a callable `f(S)`
- `integrate_trajectory()` — solve the ODE with `scipy.integrate.solve_ivp`
- Plotting the spline over the scatter and the integrated trajectory

**Expected outputs:** `results/rate_spline_fit.png`, `results/trajectory.png`

---

## Pre-built Utilities

All helper functions are in `utils/oasis_utils.py`.  
**Read through this file first** so you know what tools are available.

| Function | What it does |
|----------|-------------|
| `load_dataset(path)` | Load Excel or CSV into a DataFrame |
| `validate_columns(df, cols)` | Raise an error if required columns are missing |
| `add_extracted_subject_id(df, id_col)` | Parse `OAS30001` from `OAS30001_PIB_..._d0423` |
| `add_days_since_start_from_id(df, id_col)` | Parse day offset and convert to years |
| `get_multi_sample_subjects(df, subject_col)` | List subjects with ≥2 measurements |
| `compute_subject_slopes(df, ...)` | Per-subject linear regression → initial value + slope |
| `load_and_merge_demographics(df, path)` | Merge age, sex, APOE status from demographics file |
| `classify_apoe4_status(apoe_val)` | Convert APOE genotype code → `'APOE4+'` / `'APOE4-'` |
| `classify_gender(gender_val)` | Convert gender code → `'Male'` / `'Female'` |
| `ensure_dir(path)` | Create a directory if it doesn't exist |

---

## Repository Structure

```
pet-progression-analysis/
├── data/                        # Place OASIS3 data files here (gitignored)
├── results/                     # Output figures saved here (gitignored)
├── utils/
│   └── oasis_utils.py           # Pre-built helper functions
├── part1_explore.py
├── part2_trajectories.py
├── part3_rates.py
├── part4_model.py
├── requirements.txt
└── README.md
```

---

## Tips

- Read the **docstrings** in `utils/oasis_utils.py` before writing any code — they tell you exactly what each function returns.
- Each TODO section lists step-by-step sub-steps. Do them one at a time.
- `print(df.head())` and `print(df.columns.tolist())` are your friends when you're unsure what a DataFrame contains.
- If a figure looks wrong, check your axis labels — `Years` should be on the x-axis, not `Days`.
- The reflection questions have no single right answer. Use them to think critically about the data.
