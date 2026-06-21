"""
settings.py — Central configuration for the diesel supply analytics project.
Modify these values to adapt the pipeline to different datasets or thresholds.
"""

# ── DATA PATHS ────────────────────────────────────────────────────
import os
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR  = os.path.join(BASE_DIR, "data", "raw")
PROC_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUTS_DIR   = os.path.join(BASE_DIR, "outputs")

# ── DATASET PARAMETERS ────────────────────────────────────────────
N_SITES        = 50
N_MONTHS       = 12
RANDOM_SEED    = 42
VENDORS        = ["FastFuel Ltd", "NigerDiesel Co", "SwiftHaul NG", "PrimeLogistics", "EcoFuel Services"]
REGIONS        = ["Lagos", "Abuja", "Port Harcourt", "Kano", "Enugu"]

# ── BUSINESS RULES ────────────────────────────────────────────────
DELIVERY_TOLERANCE_PCT    = 5.0    # ±5% is acceptable quantity variance
LATE_DELIVERY_THRESHOLD   = 0      # >0 days after scheduled = late
FUEL_RISK_THRESHOLD_DAYS  = 2.0    # <2 days autonomy = high risk
SLA_AVAILABILITY_TARGET   = 99.5   # % monthly availability target

# ── VENDOR SCORING WEIGHTS ────────────────────────────────────────
SCORE_WEIGHTS = {
    "timeliness":      35,
    "qty_accuracy":    30,
    "doc_accuracy":    20,
    "escalation_rate": 15,
}

VENDOR_TIERS = {
    "Excellent":      (85, 100),
    "Satisfactory":   (70, 84),
    "At Risk":        (55, 69),
    "Underperformer": (0,  54),
}

# ── CHART SETTINGS ────────────────────────────────────────────────
CHART_DPI     = 150
CHART_STYLE   = "default"
PRIMARY_COLOR = "steelblue"
DANGER_COLOR  = "#e74c3c"
WARNING_COLOR = "#e67e22"
SUCCESS_COLOR = "#27ae60"
