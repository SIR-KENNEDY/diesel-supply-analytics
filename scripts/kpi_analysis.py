"""
kpi_analysis.py
===============
Computes all KPIs, generates vendor scorecard,
detects supply risks, and saves charts.

Run after clean_data.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
OUT_DIR  = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(f"{PROC_DIR}/deliveries_clean.csv",
                 parse_dates=["delivery_date", "scheduled_date"])
df["month"] = df["delivery_date"].dt.to_period("M")

print("=" * 55)
print("  DIESEL SUPPLY CHAIN — KPI ANALYSIS")
print("=" * 55)

# ── 1. VENDOR SCORECARD ───────────────────────────────────────────
print("\n[1] Vendor Performance Scorecard")
vendor = df.groupby("vendor_name").agg(
    deliveries=("waybill_no", "count"),
    timeliness=("on_time", "mean"),
    qty_accuracy=("within_tolerance", "mean"),
    doc_accuracy=("waybill_clean", "mean"),
    escalation_rate=("escalation_flag", "mean"),
    avg_variance=("qty_variance_pct", "mean"),
).reset_index()

vendor["score"] = (
    vendor["timeliness"]   * 35 +
    vendor["qty_accuracy"] * 30 +
    vendor["doc_accuracy"] * 20 +
    (1 - vendor["escalation_rate"]) * 15
).round(2)

bins   = [0, 55, 70, 85, 100]
labels = ["Underperformer", "At Risk", "Satisfactory", "Excellent"]
vendor["tier"] = pd.cut(vendor["score"], bins=bins, labels=labels)
vendor = vendor.sort_values("score", ascending=False).reset_index(drop=True)
vendor["rank"] = vendor.index + 1

print(vendor[["rank","vendor_name","deliveries","score","tier"]].to_string(index=False))
vendor.to_csv(f"{OUT_DIR}/vendor_scorecard.csv", index=False)

# ── 2. MONTHLY RECONCILIATION ─────────────────────────────────────
print("\n[2] Monthly Reconciliation Variance")
monthly = df.groupby(["site_id","month"]).agg(
    ordered=("qty_ordered","sum"),
    delivered=("qty_delivered","sum"),
    deliveries=("waybill_no","count"),
).reset_index()
monthly["variance_litres"] = monthly["delivered"] - monthly["ordered"]
monthly["variance_pct"]    = (monthly["variance_litres"]/monthly["ordered"]*100).round(2)
monthly.to_csv(f"{OUT_DIR}/monthly_reconciliation.csv", index=False)
print(f"  Sites with shortfall >5%: {(monthly['variance_pct'] < -5).sum()}")
print(f"  Average monthly variance: {monthly['variance_pct'].mean():.2f}%")

# ── 3. RISK DETECTION ─────────────────────────────────────────────
print("\n[3] Supply Risk — Early Warning Detection")
risk = df[df["risk_flag"]==1][
    ["site_id","region","vendor_name","delivery_date","days_of_autonomy_post_delivery"]
].sort_values("days_of_autonomy_post_delivery")
print(f"  High-risk events (< 2 days fuel): {len(risk)}")
print(f"  Most affected region: {risk['region'].value_counts().index[0]}")
risk.to_csv(f"{OUT_DIR}/high_risk_events.csv", index=False)

# ── 4. CHARTS ─────────────────────────────────────────────────────
print("\n[4] Generating charts...")
fig = plt.figure(figsize=(16, 10))
fig.suptitle("Diesel Supply Chain — KPI Dashboard", fontsize=16, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

# Chart 1: Vendor scores
ax1 = fig.add_subplot(gs[0, 0])
colors_map = {"Excellent":"#27ae60","Satisfactory":"#f1c40f","At Risk":"#e67e22","Underperformer":"#e74c3c"}
bar_colors = [colors_map.get(str(t), "steelblue") for t in vendor["tier"]]
bars = ax1.barh(vendor["vendor_name"], vendor["score"], color=bar_colors)
for bar, score in zip(bars, vendor["score"]):
    ax1.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, f"{score:.1f}", va="center", fontsize=9)
ax1.set_xlabel("Composite Score")
ax1.set_title("Vendor Performance Ranking")
ax1.set_xlim(0, 110)
for thresh, col, lbl in [(85,"green","Excellent"),(70,"orange","Min OK"),(55,"red","Review")]:
    ax1.axvline(thresh, color=col, linestyle="--", alpha=0.6, linewidth=1)

# Chart 2: Monthly accuracy trend
ax2 = fig.add_subplot(gs[0, 1])
trend = df.groupby("month")["within_tolerance"].mean() * 100
trend.index = trend.index.astype(str)
ax2.plot(trend.index, trend.values, marker="o", color="steelblue", linewidth=2)
ax2.fill_between(trend.index, trend.values, alpha=0.1, color="steelblue")
ax2.axhline(95, color="red", linestyle="--", label="Target 95%", alpha=0.7)
ax2.set_title("Monthly Delivery Accuracy Trend")
ax2.set_ylabel("Accuracy (%)")
ax2.tick_params(axis="x", rotation=45)
ax2.legend()

# Chart 3: Risk events by region
ax3 = fig.add_subplot(gs[1, 0])
risk_by_region = risk["region"].value_counts()
ax3.bar(risk_by_region.index, risk_by_region.values, color="tomato", edgecolor="white")
ax3.set_title("Supply Risk Events by Region")
ax3.set_ylabel("Number of Risk Events")

# Chart 4: On-time rate by vendor
ax4 = fig.add_subplot(gs[1, 1])
vendor_ot = vendor.set_index("vendor_name")["timeliness"] * 100
ax4.barh(vendor_ot.index, vendor_ot.values, color="steelblue")
ax4.axvline(80, color="orange", linestyle="--", alpha=0.7, label="Target 80%")
ax4.set_xlabel("On-Time Rate (%)")
ax4.set_title("On-Time Delivery Rate by Vendor")
ax4.legend()

plt.savefig(f"{OUT_DIR}/kpi_dashboard.png", dpi=150, bbox_inches="tight")
print(f"  Chart saved: {OUT_DIR}/kpi_dashboard.png")
print("\n✅ KPI analysis complete. Check outputs/ folder.")
