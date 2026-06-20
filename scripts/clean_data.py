"""
clean_data.py
=============
ETL pipeline:
  1. Load raw delivery records
  2. Run automated data quality checks
  3. Clean and validate data
  4. Enrich with derived metrics
  5. Save processed dataset

Run after generate_data.py
"""
import pandas as pd
import numpy as np
import os

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR    = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR   = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROC_DIR, exist_ok=True)

print("=" * 55)
print("  DIESEL SUPPLY CHAIN — ETL PIPELINE")
print("=" * 55)

# ── LOAD ─────────────────────────────────────────────────────────
print("\n[1/4] Loading raw data...")
df = pd.read_csv(f"{RAW_DIR}/deliveries_raw.csv",
                 parse_dates=["delivery_date", "scheduled_date"])
print(f"  Raw records: {len(df):,}")

# ── DATA QUALITY CHECKS ───────────────────────────────────────────
print("\n[2/4] Running data quality checks...")
checks = {
    "Missing site_id":            df["site_id"].isna().sum(),
    "Missing qty_ordered":        df["qty_ordered"].isna().sum(),
    "Missing qty_delivered":      df["qty_delivered"].isna().sum(),
    "Negative qty_delivered":     (df["qty_delivered"] < 0).sum(),
    "Zero qty_ordered":           (df["qty_ordered"] <= 0).sum(),
    "Future delivery dates":      (df["delivery_date"] > pd.Timestamp("today")).sum(),
    "Duplicate waybill numbers":  df["waybill_no"].duplicated().sum(),
    "qty_delivered > 2x ordered": (df["qty_delivered"] > df["qty_ordered"] * 2).sum(),
}
all_clear = True
for check, count in checks.items():
    flag = "⚠️  FLAGGED" if count > 0 else "✅ OK     "
    print(f"  {flag} | {check}: {count}")
    if count > 0: all_clear = False
if all_clear:
    print("  All quality checks passed.")

# ── CLEAN ────────────────────────────────────────────────────────
print("\n[3/4] Cleaning data...")
before = len(df)
df = df.dropna(subset=["site_id", "qty_ordered", "qty_delivered"])
df = df[df["qty_delivered"] >= 0]
df = df[df["qty_ordered"] > 0]
df = df[df["delivery_date"] <= pd.Timestamp("today")]
print(f"  Removed {before - len(df)} invalid records. Remaining: {len(df):,}")

# ── ENRICH ────────────────────────────────────────────────────────
print("\n[4/4] Enriching dataset...")
df["month"]                          = df["delivery_date"].dt.to_period("M")
df["year"]                           = df["delivery_date"].dt.year
df["qty_variance_pct"]               = ((df["qty_delivered"] - df["qty_ordered"]) / df["qty_ordered"] * 100).round(2)
df["within_tolerance"]               = df["qty_variance_pct"].between(-5, 5).astype(int)
df["on_time"]                        = (df["delivery_date"] <= df["scheduled_date"]).astype(int)
df["days_late"]                      = (df["delivery_date"] - df["scheduled_date"]).dt.days.clip(lower=0)
df["days_of_autonomy_post_delivery"] = (df["qty_delivered"] / df["daily_consumption_rate"]).round(1)
df["risk_flag"]                      = (df["days_of_autonomy_post_delivery"] < 2).astype(int)

df.to_csv(f"{PROC_DIR}/deliveries_clean.csv", index=False)
print(f"  Clean dataset saved: {len(df):,} records")
print(f"\nSummary:")
print(f"  Delivery accuracy (±5% tolerance): {df['within_tolerance'].mean()*100:.1f}%")
print(f"  On-time delivery rate:             {df['on_time'].mean()*100:.1f}%")
print(f"  Supply risk events flagged:        {df['risk_flag'].sum()}")
print(f"\n✅ ETL complete. Output: {PROC_DIR}/deliveries_clean.csv")
