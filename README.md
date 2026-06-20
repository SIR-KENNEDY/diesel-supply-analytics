# 🚛 Diesel Supply Chain Analytics — Telecom Site Operations

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green) ![Domain](https://img.shields.io/badge/Domain-Telecom-orange)

## Overview
End-to-end data analysis of diesel supply chain operations across 50 telecom sites over 12 months. Covers ETL, KPI computation, anomaly detection, and vendor performance — based on real operational patterns from telecom tower management.

## Business Problem
Telecom towers run on diesel generators. Fuel shortages cause site outages that breach SLA commitments. This project analyses delivery performance, detects supply risks early, and surfaces actionable insights for operations teams.

## Project Structure
```
project1_diesel_supply/
├── data/raw/                   # Synthetic delivery records
├── data/processed/             # Cleaned, enriched dataset
├── scripts/
│   ├── generate_data.py        # Synthetic data generator (run first)
│   ├── clean_data.py           # ETL pipeline
│   └── kpi_analysis.py         # KPI engine + anomaly detection
├── outputs/                    # Reports and summaries
└── requirements.txt
```

## How to Run
```bash
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/clean_data.py
python scripts/kpi_analysis.py
```

## Key KPIs
| KPI | Description |
|-----|-------------|
| Delivery Accuracy Rate | % deliveries within ±5% of ordered qty |
| Vendor SLA Compliance | % deliveries on or before scheduled date |
| Supply Disruption Index | Sites with <2 days fuel autonomy |
| Reconciliation Variance | Ordered vs delivered gap per site/month |

## Skills Demonstrated
`ETL Pipeline` `Pandas` `KPI Design` `Anomaly Detection` `Supply Chain Analytics` `Telecom Domain` `SQL`
