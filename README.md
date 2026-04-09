# Hospitality Accounting Automation Suite

Automated accounting tools for Australian hospitality businesses. Handles payroll, BAS/GST, weekly P&L reporting, and KPI dashboards.

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
- Visual KPI indicators
- Period-over-period comparison
- Single-file output — open in any browser

## Tech Stack

- **Python** — Core language
- **openpyxl** — Excel report generation
- **HTML/CSS** — Interactive dashboard output

## Usage

```bash
python src/payroll_processor.py
python src/bas_calculator.py
python src/weekly_report.py
python src/dashboard.py
```

## Architecture

```
src/
├── payroll_processor.py   # Award payroll with penalty rates + tax
├── bas_calculator.py      # BAS/GST quarterly reporting
├── weekly_report.py       # P&L with KPI tracking
└── dashboard.py           # HTML dashboard generator
demo/
└── dashboard.html         # Sample generated dashboard
```

## Author

**Muhammad Saboor** — Melbourne, VIC
