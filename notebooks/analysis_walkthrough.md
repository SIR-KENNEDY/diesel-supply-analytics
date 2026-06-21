# 📓 Diesel Supply Chain Analysis — Walkthrough

This notebook-style guide walks through the full analysis step by step.
Open in any Markdown viewer or follow along with the scripts.

---

## Step 1 — Generate Data
```bash
python scripts/generate_data.py
```
Creates `data/raw/deliveries_raw.csv` and `data/raw/site_metadata.csv`.

**What's generated:**
- 50 telecom sites across Lagos, Abuja, Port Harcourt, Kano, Enugu
- 12 months of delivery records (~2,400 rows)
- 5 vendors with different performance profiles (FastFuel, NigerDiesel, etc.)
- Realistic delivery variance, late deliveries, escalation flags

---

## Step 2 — Clean & Validate (ETL Pipeline)
```bash
python scripts/clean_data.py
```

**Quality checks run automatically:**
| Check | Expected Result |
|-------|----------------|
| Missing site_id | 0 |
| Negative qty_delivered | 0 |
| Future delivery dates | 0 |
| Duplicate waybills | 0 |
| qty_delivered > 2x ordered | 0 |

**Derived fields added:**
- `qty_variance_pct` — % difference between ordered and delivered
- `within_tolerance` — 1 if variance within ±5%, else 0
- `on_time` — 1 if delivery on or before scheduled date
- `days_of_autonomy_post_delivery` — days of fuel after delivery
- `risk_flag` — 1 if autonomy < 2 days

---

## Step 3 — KPI Analysis
```bash
python scripts/kpi_analysis.py
```

**Outputs generated:**
- `outputs/vendor_scorecard.csv` — composite scores for all vendors
- `outputs/monthly_reconciliation.csv` — ordered vs delivered per site per month
- `outputs/high_risk_events.csv` — sites near fuel-out
- `outputs/kpi_dashboard.png` — 4-panel chart

**Vendor Scoring Formula:**
```
Score = Timeliness(35%) + Qty Accuracy(30%) + Doc Accuracy(20%) + (1 - Escalation Rate)(15%)
```

---

## Step 4 — SQL-Style Analytics
```bash
python scripts/sql_analysis.py
```

**Analyses run:**
1. Sites with 3+ consecutive delivery shortfall months
2. Vendor percentile ranking by on-time rate
3. Top 3 worst sites per region
4. Month-over-month accuracy trend

---

## Key Findings (from synthetic data)
- **~75%** of deliveries within ±5% quantity tolerance
- **~82%** of deliveries on time across all vendors
- **Delta Logistics** consistently scores highest (~94/100)
- **EcoFuel Services** scores lowest (~48/100) — contract review triggered
- Power shortages account for majority of risk events in Kano region

---

## Business Recommendations
1. Place EcoFuel Services on probation — below 55 composite score
2. Replicate Delta Logistics contract terms with underperformers
3. Prioritise fuel pre-positioning in Kano sites before dry season
4. Automate waybill reconciliation to reduce 8% documentation error rate
