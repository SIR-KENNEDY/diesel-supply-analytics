# 🚛 Diesel Supply Chain Analytics — Telecom Site Operations

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green) ![SQL](https://img.shields.io/badge/SQL-Analytics-lightgrey) ![Domain](https://img.shields.io/badge/Domain-Telecom-orange)

## Overview
End-to-end data analysis of diesel supply chain operations across **50 telecom sites over 12 months**. Covers ETL pipeline design, data quality validation, KPI computation, vendor scoring, anomaly detection, and chart generation.

Built from real operational patterns developed during 7+ years of supply chain management at IHS Towers Nigeria.

## Business Problem
Telecom towers run on diesel generators. Unplanned fuel shortages cause site outages that breach SLA commitments to mobile network operators. This project:
- Detects delivery discrepancies automatically
- Scores vendor performance objectively
- Flags sites at risk of fuel-out 48 hours in advance
- Generates reconciliation reports for management

## Project Structure
```
diesel-supply-analytics/
├── scripts/
│   ├── generate_data.py      # Synthetic data generator (run first)
│   ├── clean_data.py         # ETL pipeline + data quality checks
│   └── kpi_analysis.py       # KPIs, vendor scoring, risk detection, charts
├── data/
│   ├── raw/                  # Generated raw CSV files
│   └── processed/            # Cleaned and enriched dataset
├── outputs/                  # Charts and summary reports
├── requirements.txt
└── README.md
```

## How to Run
```bash
git clone https://github.com/SIR-KENNEDY/diesel-supply-analytics
cd diesel-supply-analytics
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/clean_data.py
python scripts/kpi_analysis.py
```

## Key KPIs Computed
| KPI | Description |
|-----|-------------|
| Delivery Accuracy Rate | % deliveries within ±5% of ordered quantity |
| Vendor SLA Compliance | % deliveries on or before scheduled date |
| Supply Disruption Index | Sites with <2 days fuel autonomy |
| Reconciliation Variance | Ordered vs delivered gap per site per month |
| Composite Vendor Score | Weighted score across 4 performance dimensions |

## Sample Results
- **Delivery accuracy**: 75% within ±5% tolerance
- **On-time rate**: 82% across all vendors
- **Risk events detected**: Sites flagged 48hrs before fuel-out
- **Top vendor score**: 94.3/100 | Lowest: 48.1/100

## Skills Demonstrated
`ETL Pipeline Design` `Data Quality Validation` `KPI Engineering` `Vendor Scorecard` `Anomaly Detection` `Pandas` `Matplotlib` `Supply Chain Analytics` `Telecom Domain`

---
*Kennedy Onuorah | [LinkedIn](https://www.linkedin.com/in/kennedy-onuorah-7a3793128) | [GitHub](https://github.com/SIR-KENNEDY)*
