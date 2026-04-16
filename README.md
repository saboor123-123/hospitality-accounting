# Hospitality Accounting Automation Suite

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Live%20in%20Production-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **Live for a real Melbourne business.** End-to-end data pipeline that replaced ~4 hours/week of manual spreadsheet work and saves ~$2,000/quarter in accountant fees.

## [View Live Dashboard](https://imuhammadsaboor.github.io/hospitality-accounting/)

---

## Business Impact

| Metric | Before | After |
|--------|--------|-------|
| Weekly data processing | ~4 hours manual | ~15 minutes automated |
| Quarterly accountant cost | ~$2,000 | $0 (self-serve) |
| Payroll accuracy | Manual calculation | Automated Award compliance |
| Reporting delay | 2-3 days | Real-time dashboard |

## What It Does

Fully automated accounting pipeline for an Australian hospitality business:

```
Timesheets (input)
    --> Payroll Processing (Award rates, penalties, tax, super)
    --> BAS/GST Calculation (quarterly tax reporting)
    --> Weekly P&L Report (revenue, costs, KPIs)
    --> Live KPI Dashboard (browser-based, single HTML file)
```

## Features

### Payroll Processor
- Australian Hospitality Award (MA000009) compliance
- Penalty rates: weekend, evening, public holiday
- Casual loading (25%)
- PAYG tax withholding (2024-25 brackets)
- Superannuation (12%)
- Automated payslip generation

### BAS/GST Calculator
- GST on sales and purchases
- Input tax credits
- PAYG withholding totals
- Quarterly BAS summary ready for lodgement

### Weekly P&L Report
- Revenue vs cost tracking
- Automated KPI calculations:
  - Food cost %
  - Labour cost %
  - Prime cost %
  - Gross profit margin
- Alert thresholds for out-of-range KPIs

### Interactive Dashboard
- HTML dashboard combining all reports
- Visual KPI indicators with colour-coded alerts
- Period-over-period comparison
- Single-file output - open in any browser

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core pipeline logic |
| SQLite | Data storage and queries |
| openpyxl | Excel report generation |
| HTML/CSS | Interactive dashboard |
| REST APIs | Data ingestion |

## Architecture

```
src/
├── payroll_processor.py   # Award payroll with penalty rates + tax
├── bas_calculator.py      # BAS/GST quarterly reporting
├── weekly_report.py       # P&L with KPI tracking
└── dashboard.py           # HTML dashboard generator
demo/
└── dashboard.html         # Sample generated dashboard
docs/
└── index.html             # Live GitHub Pages dashboard
```

## Usage

```bash
python src/payroll_processor.py
python src/bas_calculator.py
python src/weekly_report.py
python src/dashboard.py
```

## Author

**Muhammad Saboor** — Melbourne, VIC
Final-year Bachelor of Data Science, Victoria University
[GitHub](https://github.com/iMuhammadSaboor) | bmuhammadsaboor@gmail.com
