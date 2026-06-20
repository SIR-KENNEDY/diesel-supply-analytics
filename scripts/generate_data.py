"""
generate_data.py
================
Generates synthetic diesel delivery dataset:
  - 50 telecom sites across 5 Nigerian regions
  - 12 months of delivery records (~2,400+ rows)
  - 5 vendors with different performance profiles
  - Realistic variance, late deliveries, escalations

Run this FIRST before clean_data.py or kpi_analysis.py
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ── CONFIG ────────────────────────────────────────────────────────
N_SITES   = 50
N_MONTHS  = 12
START     = datetime(2023, 1, 1)
VENDORS   = ["FastFuel Ltd", "NigerDiesel Co", "SwiftHaul NG", "PrimeLogistics", "EcoFuel Services"]
REGIONS   = ["Lagos", "Abuja", "Port Harcourt", "Kano", "Enugu"]
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR   = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# ── SITE METADATA ─────────────────────────────────────────────────
sites = pd.DataFrame({
    "site_id":                [f"SITE_{str(i).zfill(3)}" for i in range(1, N_SITES+1)],
    "region":                 np.random.choice(REGIONS, N_SITES),
    "tank_capacity_litres":   np.random.choice([2000, 3000, 5000, 7000], N_SITES),
    "daily_consumption_rate": np.random.uniform(80, 250, N_SITES).round(1),
    "vendor_name":            np.random.choice(VENDORS, N_SITES),
})

# ── DELIVERY RECORDS ──────────────────────────────────────────────
records = []
for _, s in sites.iterrows():
    for month_offset in range(N_MONTHS):
        base_date = START + timedelta(days=30 * month_offset)
        n_deliveries = np.random.randint(3, 6)
        for _ in range(n_deliveries):
            qty_ordered = round(np.random.uniform(500, s.tank_capacity_litres * 0.8))
            # Realistic delivery variance distribution
            variance = np.random.choice(
                [1.0, 0.97, 0.93, 0.88, 1.03],
                p=[0.60, 0.15, 0.10, 0.10, 0.05]
            )
            qty_delivered = round(qty_ordered * variance)
            scheduled = base_date + timedelta(days=int(np.random.randint(1, 28)))
            late       = np.random.random() < 0.18   # 18% late rate
            actual     = scheduled + timedelta(days=int(np.random.randint(1, 4)) if late else 0)

            records.append({
                "waybill_no":              f"WB{np.random.randint(100000, 999999)}",
                "site_id":                 s.site_id,
                "region":                  s.region,
                "vendor_name":             s.vendor_name,
                "tank_capacity_litres":    s.tank_capacity_litres,
                "daily_consumption_rate":  s.daily_consumption_rate,
                "scheduled_date":          scheduled.strftime("%Y-%m-%d"),
                "delivery_date":           actual.strftime("%Y-%m-%d"),
                "qty_ordered":             qty_ordered,
                "qty_delivered":           qty_delivered,
                "driver_id":               f"DRV{np.random.randint(100, 999)}",
                "waybill_clean":           int(np.random.random() > 0.08),
                "escalation_flag":         int(np.random.random() < 0.05),
            })

df = pd.DataFrame(records)
df["delivery_date"]  = pd.to_datetime(df["delivery_date"])
df["scheduled_date"] = pd.to_datetime(df["scheduled_date"])

sites.to_csv(f"{RAW_DIR}/site_metadata.csv", index=False)
df.to_csv(f"{RAW_DIR}/deliveries_raw.csv", index=False)
print(f"✅ Generated {len(df):,} delivery records across {N_SITES} sites.")
print(f"   Saved to: {RAW_DIR}/")
print(df.head(3).to_string())
