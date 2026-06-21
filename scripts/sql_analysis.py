"""
sql_analysis.py
===============
Runs SQL-style analysis on the cleaned delivery data using pandas
to mirror common SQL patterns: GROUP BY, window functions, CTEs.
Outputs a suite of analytical summaries to outputs/.

Run after clean_data.py
"""
import pandas as pd
import numpy as np
import os

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC    = os.path.join(BASE, "data", "processed")
OUTPUTS = os.path.join(BASE, "outputs")
os.makedirs(OUTPUTS, exist_ok=True)

df = pd.read_csv(f"{PROC}/deliveries_clean.csv", parse_dates=["delivery_date","scheduled_date"])
df["month"] = df["delivery_date"].dt.to_period("M").astype(str)

print("="*55)
print("  SQL-STYLE ANALYTICS (Pandas)")
print("="*55)

# ── Q1: Sites with 3+ consecutive shortfall months ────────────────
print("\n[Q1] Sites with 3+ consecutive delivery shortfall months")
monthly = df.groupby(["site_id","month"]).agg(
    ordered=("qty_ordered","sum"), delivered=("qty_delivered","sum")
).reset_index()
monthly["var_pct"] = (monthly["delivered"]-monthly["ordered"])/monthly["ordered"]*100
monthly["shortfall"] = (monthly["var_pct"] < -5).astype(int)

# Rolling 3-month sum of shortfall flag per site
monthly = monthly.sort_values(["site_id","month"])
monthly["consec_shortfalls"] = (
    monthly.groupby("site_id")["shortfall"]
    .transform(lambda x: x.rolling(3, min_periods=3).sum())
)
chronic = monthly[monthly["consec_shortfalls"] >= 3][["site_id","month","var_pct","consec_shortfalls"]]
print(f"  Sites flagged: {chronic['site_id'].nunique()}")
print(chronic.head(10).to_string(index=False))
chronic.to_csv(f"{OUTPUTS}/chronic_shortfall_sites.csv", index=False)

# ── Q2: Vendor percentile ranking ─────────────────────────────────
print("\n[Q2] Vendor percentile ranking")
vendor = df.groupby("vendor_name").agg(
    deliveries=("waybill_no","count"),
    on_time_pct=("on_time","mean"),
    accuracy_pct=("within_tolerance","mean"),
).reset_index()
vendor["on_time_pct"]   = (vendor["on_time_pct"]   * 100).round(2)
vendor["accuracy_pct"]  = (vendor["accuracy_pct"]  * 100).round(2)
vendor["on_time_rank"]  = vendor["on_time_pct"].rank(ascending=False).astype(int)
vendor["accuracy_rank"] = vendor["accuracy_pct"].rank(ascending=False).astype(int)
vendor = vendor.sort_values("on_time_rank")
print(vendor.to_string(index=False))
vendor.to_csv(f"{OUTPUTS}/vendor_ranking.csv", index=False)

# ── Q3: Top 3 worst sites per region by shortfall ─────────────────
print("\n[Q3] Top 3 worst sites per region")
site_perf = df.groupby(["site_id","region"]).agg(
    total_shortfall_litres=("qty_variance_pct", lambda x: (x[x<-5]).count()),
    avg_variance_pct=("qty_variance_pct","mean"),
).reset_index()
site_perf["rank_in_region"] = site_perf.groupby("region")["total_shortfall_litres"].rank(
    ascending=False, method="first").astype(int)
top3 = site_perf[site_perf["rank_in_region"] <= 3].sort_values(["region","rank_in_region"])
print(top3.to_string(index=False))
top3.to_csv(f"{OUTPUTS}/top3_worst_sites_per_region.csv", index=False)

# ── Q4: Month-over-month delivery accuracy change ─────────────────
print("\n[Q4] Month-over-month delivery accuracy")
mom = df.groupby("month")["within_tolerance"].mean().reset_index()
mom.columns = ["month","accuracy"]
mom["prev_accuracy"] = mom["accuracy"].shift(1)
mom["mom_change_pct"] = ((mom["accuracy"] - mom["prev_accuracy"]) / mom["prev_accuracy"] * 100).round(2)
print(mom.to_string(index=False))
mom.to_csv(f"{OUTPUTS}/mom_accuracy_trend.csv", index=False)

print("\n✅ SQL-style analysis complete. Outputs saved.")
