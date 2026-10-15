"""Central configuration: paths, policy constants, and column names.

All paths are derived from the project root (the parent of this ``src/``
directory), so the code runs from any working directory without hard-coded,
machine-specific absolute paths.
"""
from pathlib import Path

# Project root = parent of this src/ directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Paths ---
RAW_DATA = PROJECT_ROOT / "data" / "raw" / "public.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"

# --- Policy parameters (Card & Krueger 1994) ---
NJ_NEW_MIN_WAGE = 5.05    # NJ minimum wage after 1992-04-01 (dollars/hour)
FEDERAL_MIN_WAGE = 4.25   # federal / PA minimum wage (dollars/hour)

# --- Column names in public.csv (per DATA_DICTIONARY.md) ---
C = {
    "sheet": "SHEET",
    "chain": "CHAIN",
    "co_owned": "CO_OWNED",
    "state": "STATE",
    "southj": "SOUTHJ",
    "centralj": "CENTRALJ",
    "northj": "NORTHJ",
    "pa1": "PA1",
    "pa2": "PA2",
    "shore": "SHORE",
    "empft": "EMPFT",
    "emppt": "EMPPT",
    "nmgrs": "NMGRS",
    "wage_st": "WAGE_ST",
    "bonus": "BONUS",
    "hrsopen": "HRSOPEN",
    "psoda": "PSODA",
    "pfry": "PFRY",
    "pentree": "PENTREE",
    "status2": "STATUS2",
    "empft2": "EMPFT2",
    "emppt2": "EMPPT2",
    "nmgrs2": "NMGRS2",
    "wage_st2": "WAGE_ST2",
    "hrsopen2": "HRSOPEN2",
    "psoda2": "PSODA2",
    "pfry2": "PFRY2",
    "pentree2": "PENTREE2",
}

# Chain labels (CHAIN: 1=BK, 2=KFC, 3=Roy Rogers, 4=Wendy's).
CHAIN_LABELS = {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"}

# Chart palette (from the project's data-viz reference; colorblind-safe pair).
COLOR_NJ = "#2a78d6"   # categorical slot 1 (blue)  -> treatment
COLOR_PA = "#eb6834"   # categorical slot 2 (orange) -> control
GRIDLINE = "#e1e0d9"   # hairline grid (light mode)
MUTED_INK = "#898781"  # axis/label ink (light mode)
