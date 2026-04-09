"""
Hospitality Accounting Dashboard Generator
Creates a visual HTML dashboard from payroll, BAS, and weekly report data.
Show this in your interview - it demonstrates automation + accounting knowledge.

Author: Muhammad Saboor
"""

import json
import os

OUTPUT_DIR = "C:/Users/ashai/hospitality-accounting/output"
DEMO_DIR = "C:/Users/ashai/hospitality-accounting/demo"
os.makedirs(DEMO_DIR, exist_ok=True)


def load_reports():
    """Load all generated report data."""
    data = {}
    for name in ["payroll_report", "bas_report", "weekly_report"]:
        path = os.path.join(OUTPUT_DIR, f"{name}.json")
        if os.path.exists(path):
            with open(path) as f:
                data[name] = json.load(f)
    return data


def generate_dashboard(data):
    """Generate a comprehensive HTML dashboard."""
    payroll = data.get("payroll_report", {})
    bas = data.get("bas_report", {})
    weekly = data.get("weekly_report", {})

    kpis = weekly.get("kpis", {})
    totals = weekly.get("totals", {})
    bas_summary = bas.get("summary", {})
    payroll_totals = payroll.get("totals", {})

    # Build employee rows
    emp_rows = ""
    for emp in payroll.get("employees", []):
        emp_rows += f"""
        <tr>
            <td>{emp['name']}</td>
            <td>{emp['role']}</td>
            <td>{emp['employment_type'].title()}</td>
            <td>{emp['total_hours']:.1f}</td>
            <td>${emp['gross_pay']:,.2f}</td>
            <td>${emp['payg_withholding']:,.2f}</td>
            <td>${emp['superannuation']:,.2f}</td>
            <td class="highlight">${emp['net_pay']:,.2f}</td>
        </tr>"""

    # Build daily rows
    daily_rows = ""
    for d in weekly.get("daily_breakdown", []):
        daily_rows += f"""
        <tr>
            <td>{d['day']}</td>
            <td>${d['total_revenue']:,.2f}</td>
            <td>${d['food_cost']:,.2f}</td>
            <td>${d['beverage_cost']:,.2f}</td>
            <td>${d['wage_cost']:,.2f}</td>
            <td>{d['covers']}</td>
        </tr>"""

    # Revenue chart data (simple bar chart with CSS)
    max_rev = max(d["total_revenue"] for d in weekly.get("daily_breakdown", [{"total_revenue": 1}]))
    chart_bars = ""
    for d in weekly.get("daily_breakdown", []):
        pct = (d["total_revenue"] / max_rev) * 100
        chart_bars += f"""
        <div class="bar-group">
            <div class="bar" style="height: {pct}%">
                <span class="bar-val">${d['total_revenue']:,.0f}</span>
            </div>
            <div class="bar-label">{d['day'][:3]}</div>
        </div>"""

    # KPI status colors
    def kpi_color(val, low, high):
        if val < low:
            return "kpi-good"
        elif val <= high:
            return "kpi-ok"
        return "kpi-alert"

    food_class = kpi_color(kpis.get("food_cost_pct", 0), 28, 32)
    labor_class = kpi_color(kpis.get("labor_cost_pct", 0), 30, 35)
    prime_class = kpi_color(kpis.get("prime_cost_pct", 0), 60, 65)

    # Alerts
    alerts_html = ""
    for alert in weekly.get("alerts", []):
        alerts_html += f'<div class="alert">{alert}</div>'
    if not alerts_html:
        alerts_html = '<div class="alert-ok">All KPIs within target range</div>'

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Hospitality Accounting Dashboard - Muhammad Saboor</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f1117; color: #e0e0e0; }}
    .header {{ background: linear-gradient(135deg, #1a1d2e, #252942); padding: 30px 40px; border-bottom: 3px solid #c9a84c; }}
    .header h1 {{ font-size: 26px; color: #c9a84c; }}
    .header p {{ color: #8a8d9b; margin-top: 5px; font-size: 14px; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 25px; }}

    .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 30px; }}
    .kpi-card {{ background: #1a1d2e; border-radius: 10px; padding: 22px; text-align: center; border: 1px solid #2a2d3e; }}
    .kpi-card .label {{ font-size: 12px; color: #8a8d9b; text-transform: uppercase; letter-spacing: 1px; }}
    .kpi-card .value {{ font-size: 32px; font-weight: 700; margin: 8px 0; }}
    .kpi-card .sub {{ font-size: 11px; color: #666; }}
    .kpi-good .value {{ color: #4ade80; }}
    .kpi-ok .value {{ color: #c9a84c; }}
    .kpi-alert .value {{ color: #ef4444; }}

    .section {{ background: #1a1d2e; border-radius: 10px; padding: 25px; margin-bottom: 20px; border: 1px solid #2a2d3e; }}
    .section h2 {{ font-size: 18px; color: #c9a84c; margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid #2a2d3e; }}

    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ text-align: left; padding: 10px 12px; background: #252942; color: #c9a84c; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }}
    td {{ padding: 9px 12px; border-bottom: 1px solid #1f2233; }}
    tr:hover td {{ background: #252942; }}
    .highlight {{ color: #4ade80; font-weight: 600; }}

    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}

    .chart {{ display: flex; align-items: flex-end; justify-content: space-around; height: 200px; padding: 20px 10px 0; }}
    .bar-group {{ display: flex; flex-direction: column; align-items: center; flex: 1; }}
    .bar {{ background: linear-gradient(to top, #c9a84c, #e0c068); border-radius: 4px 4px 0 0; width: 40px; min-height: 5px; position: relative; transition: height 0.3s; }}
    .bar-val {{ position: absolute; top: -20px; font-size: 10px; color: #c9a84c; white-space: nowrap; }}
    .bar-label {{ font-size: 11px; color: #8a8d9b; margin-top: 8px; }}

    .bas-item {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1f2233; }}
    .bas-item .label {{ color: #8a8d9b; }}
    .bas-item .value {{ font-weight: 600; }}
    .bas-total {{ font-size: 20px; color: #c9a84c; font-weight: 700; margin-top: 15px; text-align: right; }}

    .alert {{ background: #3b1111; border: 1px solid #ef4444; color: #ef4444; padding: 10px 15px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }}
    .alert-ok {{ background: #0f2918; border: 1px solid #4ade80; color: #4ade80; padding: 10px 15px; border-radius: 6px; font-size: 13px; }}

    .footer {{ text-align: center; padding: 30px; color: #555; font-size: 12px; }}
    .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
    .badge-casual {{ background: #1e3a5f; color: #60a5fa; }}
    .badge-pt {{ background: #1e3a2a; color: #4ade80; }}
    .badge-ft {{ background: #3a2a1e; color: #c9a84c; }}
</style>
</head>
<body>

<div class="header">
    <h1>Hospitality Accounting Dashboard</h1>
    <p>Automated Financial Reporting System | Built by Muhammad Saboor | Python + Data Automation</p>
</div>

<div class="container">

    <!-- KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card {food_class}">
            <div class="label">Food Cost %</div>
            <div class="value">{kpis.get('food_cost_pct', 0)}%</div>
            <div class="sub">Target: 28-32%</div>
        </div>
        <div class="kpi-card {labor_class}">
            <div class="label">Labor Cost %</div>
            <div class="value">{kpis.get('labor_cost_pct', 0)}%</div>
            <div class="sub">Target: 30-35%</div>
        </div>
        <div class="kpi-card {prime_class}">
            <div class="label">Prime Cost %</div>
            <div class="value">{kpis.get('prime_cost_pct', 0)}%</div>
            <div class="sub">Target: 60-65%</div>
        </div>
        <div class="kpi-card kpi-ok">
            <div class="label">Weekly Revenue</div>
            <div class="value">${totals.get('total_revenue', 0):,.0f}</div>
            <div class="sub">Avg ${kpis.get('avg_daily_revenue', 0):,.0f}/day</div>
        </div>
        <div class="kpi-card kpi-ok">
            <div class="label">GP Margin</div>
            <div class="value">{kpis.get('gp_margin_pct', 0)}%</div>
            <div class="sub">Target: 68-72%</div>
        </div>
    </div>

    <!-- Alerts -->
    {alerts_html}

    <div class="grid-2" style="margin-top: 20px;">
        <!-- Revenue Chart -->
        <div class="section">
            <h2>Daily Revenue</h2>
            <div class="chart">{chart_bars}</div>
        </div>

        <!-- BAS Summary -->
        <div class="section">
            <h2>BAS Summary - {bas.get('quarter', 'Q3 2026')}</h2>
            <div class="bas-item"><span class="label">GST on Sales (1A)</span><span class="value">${bas_summary.get('gst_amount', 0):,.2f}</span></div>
            <div class="bas-item"><span class="label">PAYG Withheld (W2)</span><span class="value">${bas_summary.get('payg_amount', 0):,.2f}</span></div>
            <div class="bas-total">Total Payable: ${bas_summary.get('total_payable', 0):,.2f}</div>
            <p style="font-size: 11px; color: #666; margin-top: 12px;">Due: 28th of month after quarter end | Lodge via ATO Portal</p>
        </div>
    </div>

    <!-- Weekly P&L -->
    <div class="section">
        <h2>Weekly P&L - {weekly.get('venue', 'Etta')}</h2>
        <table>
            <tr><th>Day</th><th>Revenue</th><th>Food Cost</th><th>Bev Cost</th><th>Wages</th><th>Covers</th></tr>
            {daily_rows}
            <tr style="background: #252942; font-weight: 600;">
                <td>TOTAL</td>
                <td>${totals.get('total_revenue', 0):,.2f}</td>
                <td>${totals.get('food_cost', 0):,.2f}</td>
                <td>${totals.get('beverage_cost', 0):,.2f}</td>
                <td>${totals.get('wage_cost', 0):,.2f}</td>
                <td>{totals.get('total_covers', 0)}</td>
            </tr>
        </table>
    </div>

    <!-- Payroll -->
    <div class="section">
        <h2>Payroll Summary - {payroll.get('period', 'Weekly')} ending {payroll.get('period_ending', '')}</h2>
        <table>
            <tr><th>Employee</th><th>Role</th><th>Type</th><th>Hours</th><th>Gross</th><th>PAYG</th><th>Super</th><th>Net Pay</th></tr>
            {emp_rows}
            <tr style="background: #252942; font-weight: 600;">
                <td colspan="3">TOTALS</td>
                <td>{payroll_totals.get('hours', 0):.1f}</td>
                <td>${payroll_totals.get('gross', 0):,.2f}</td>
                <td>${payroll_totals.get('payg', 0):,.2f}</td>
                <td>${payroll_totals.get('super', 0):,.2f}</td>
                <td class="highlight">${payroll_totals.get('net', 0):,.2f}</td>
            </tr>
        </table>
        <p style="font-size: 11px; color: #666; margin-top: 12px;">
            Award: {payroll.get('award', 'Hospitality Award MA000009')} |
            Super Rate: {payroll.get('super_rate', '12%')} |
            Total Cost to Business: ${payroll_totals.get('gross', 0) + payroll_totals.get('super', 0):,.2f}
        </p>
    </div>

</div>

<div class="footer">
    Hospitality Accounting Automation | Built with Python by Muhammad Saboor | Data Science + Accounting
</div>

</body>
</html>"""

    path = os.path.join(DEMO_DIR, "dashboard.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Dashboard saved: {path}")
    return path


if __name__ == "__main__":
    data = load_reports()
    generate_dashboard(data)
