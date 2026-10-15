"""Load and validate the raw survey data (public.csv)."""
from pathlib import Path

import pandas as pd

import config

# Columns the analysis depends on (must all be present).
REQUIRED_COLUMNS = list(config.C.values())

EXPECTED_SHAPE = (410, 46)  # per the data dictionary


def load_public_csv(path=None):
    """Load public.csv and run structural validation.

    Raises a clear error if the input file is missing or if required columns
    are absent, so a user gets an actionable message rather than a traceback
    deep inside the analysis.
    """
    path = Path(path) if path else config.RAW_DATA

    if not path.exists():
        raise FileNotFoundError(
            f"Input data not found: {path}\n\n"
            "Please place 'public.csv' (course Package 01) at data/raw/public.csv "
            "and re-run. See README.md, section 6, for how to obtain and place the data."
        )

    df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns in {path}: {missing}\n"
            "The file may be from a different dataset. Expected the columns listed "
            "in DATA_DICTIONARY.md for public.csv."
        )

    if df.shape != EXPECTED_SHAPE:
        print(f"[load] Warning: expected shape {EXPECTED_SHAPE}, got {df.shape}.")

    if df.duplicated().any():
        print("[load] Warning: full-row duplicate records are present.")

    print(f"[load] Loaded {df.shape[0]} rows x {df.shape[1]} columns from {path}")
    return df
