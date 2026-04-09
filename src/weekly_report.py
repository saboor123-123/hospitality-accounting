"""
Weekly Financial Report Generator
Generates automated weekly P&L and KPI reports for hospitality venues.
Tracks: revenue, food cost %, labor cost %, prime cost, GP margin.

Author: Muhammad Saboor
"""

import json
import os
from datetime import datetime, timedelta
import random

OUTPUT_DIR = "C:/Users/ashai/hospitality-accounting/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_demo_week(week_num=1):
    """Generate realistic weekly data for a restaurant."""
    random.seed(42 + week_num)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Base patterns (restaurant busier on weekends)
    revenue_pattern = [2200, 2800, 3200, 4500, 7800, 9500, 6800]
    wage_pattern = [1200, 1400, 1600, 2000, 3200, 3800, 2800]

    daily = []
    for i, day in enumerate(days):
        # Add some randomness
        variance = random.uniform(0.85, 1.15)
        food_rev = round(revenue_pattern[i] * 0.65 * variance, 2)
        bev_rev = round(revenue_pattern[i] * 0.35 * variance, 2)
        total_rev = round(food_rev + bev_rev, 2)

        food_cost = round(food_rev * random.uniform(0.28, 0.34), 2)
        bev_cost = round(bev_rev * random.uniform(0.22, 0.28), 2)
        wages = round(wage_pattern[i] * random.uniform(0.95, 1.05), 2)

        daily.append({
            "day": day,
            "food_revenue": food_rev,
            "beverage_revenue": bev_rev,
            "total_revenue": total_rev,
            "food_cost": food_cost,
            "beverage_cost": bev_cost,
            "total_cogs": round(food_cost + bev_cost, 2),
            "wage_cost": wages,
            "covers": int(total_rev / random.uniform(38, 55)),
        })

    return daily


def calculate_weekly_report(daily_data, week_ending=None, venue="Etta"):
    """Calculate weekly KPIs and financial summary."""
    if not week_ending:
        week_ending = datetime.now().strftime("%d/%m/%Y")

    # Totals
    total_food_rev = sum(d["food_revenue"] for d in daily_data)
    total_bev_rev = sum(d["beverage_revenue"] for d in daily_data)
    total_rev = sum(d["total_revenue"] for d in daily_data)
    total_food_cost = sum(d["food_cost"] for d in daily_data)
    total_bev_cost = sum(d["beverage_cost"] for d in daily_data)
    total_cogs = sum(d["total_cogs"] for d in daily_data)
    total_wages = sum(d["wage_cost"] for d in daily_data)
    total_covers = sum(d["covers"] for d in daily_data)

    # KPIs
    gross_profit = total_rev - total_cogs
    prime_cost = total_cogs + total_wages
    operating_profit = gross_profit - total_wages

    report = {
        "venue": venue,
        "week_ending": week_ending,
        "generated": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "daily_breakdown": daily_data,
        "totals": {
            "food_revenue": round(total_food_rev, 2),
            "beverage_revenue": round(total_bev_rev, 2),
            "total_revenue": round(total_rev, 2),
            "food_cost": round(total_food_cost, 2),
            "beverage_cost": round(total_bev_cost, 2),
            "total_cogs": round(total_cogs, 2),
            "wage_cost": round(total_wages, 2),
            "gross_profit": round(gross_profit, 2),
            "operating_profit": round(operating_profit, 2),
            "prime_cost": round(prime_cost, 2),
            "total_covers": total_covers,
        },
        "kpis": {
            "food_cost_pct": round((total_food_cost / total_food_rev) * 100, 1),
            "beverage_cost_pct": round((total_bev_cost / total_bev_rev) * 100, 1),
            "total_cogs_pct": round((total_cogs / total_rev) * 100, 1),
            "labor_cost_pct": round((total_wages / total_rev) * 100, 1),
            "prime_cost_pct": round((prime_cost / total_rev) * 100, 1),
            "gp_margin_pct": round((gross_profit / total_rev) * 100, 1),
            "avg_revenue_per_cover": round(total_rev / total_covers, 2),
            "avg_daily_revenue": round(total_rev / 7, 2),
        },
        "targets": {
            "food_cost_target": "28-32%",
            "bev_cost_target": "22-28%",
            "labor_cost_target": "30-35%",
            "prime_cost_target": "60-65%",
            "gp_margin_target": "68-72%",
        },
    }

    # Flag any KPIs outside target
    alerts = []
    kpis = report["kpis"]
    if kpis["food_cost_pct"] > 32:
        alerts.append(f"ALERT: Food cost {kpis['food_cost_pct']}% exceeds 32% target")
    if kpis["labor_cost_pct"] > 35:
        alerts.append(f"ALERT: Labor cost {kpis['labor_cost_pct']}% exceeds 35% target")
    if kpis["prime_cost_pct"] > 65:
        alerts.append(f"ALERT: Prime cost {kpis['prime_cost_pct']}% exceeds 65% target")
    report["alerts"] = alerts

    # Save
    path = os.path.join(OUTPUT_DIR, "weekly_report.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    return report


def print_weekly_report(report):
    """Print weekly report to console."""
    print("=" * 75)
    print(f"  WEEKLY FINANCIAL REPORT - {report['venue']}")
    print(f"  Week Ending: {report['week_ending']}")
    print("=" * 75)

    # Daily breakdown
    print(f"\n  {'Day':<12} {'Revenue':>10} {'Food Cost':>10} {'Bev Cost':>10} {'Wages':>10} {'Covers':>8}")
    print(f"  {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")

    for d in report["daily_breakdown"]:
        print(
            f"  {d['day']:<12} ${d['total_revenue']:>9,.2f} "
            f"${d['food_cost']:>9,.2f} ${d['beverage_cost']:>9,.2f} "
            f"${d['wage_cost']:>9,.2f} {d['covers']:>8}"
        )

    t = report["totals"]
    print(f"  {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")
    print(
        f"  {'TOTAL':<12} ${t['total_revenue']:>9,.2f} "
        f"${t['food_cost']:>9,.2f} ${t['beverage_cost']:>9,.2f} "
        f"${t['wage_cost']:>9,.2f} {t['total_covers']:>8}"
    )

    # P&L Summary
    print(f"\n  PROFIT & LOSS SUMMARY")
    print(f"  {'='*50}")
    print(f"  Total Revenue:          ${t['total_revenue']:>12,.2f}")
    print(f"  Less: COGS:             ${t['total_cogs']:>12,.2f}")
    print(f"  Gross Profit:           ${t['gross_profit']:>12,.2f}")
    print(f"  Less: Wages:            ${t['wage_cost']:>12,.2f}")
    print(f"  Operating Profit:       ${t['operating_profit']:>12,.2f}")

    # KPIs
    k = report["kpis"]
    tgt = report["targets"]
    print(f"\n  KEY PERFORMANCE INDICATORS")
    print(f"  {'='*50}")
    print(f"  {'KPI':<28} {'Actual':>8} {'Target':>12}")
    print(f"  {'-'*28} {'-'*8} {'-'*12}")
    print(f"  {'Food Cost %':<28} {k['food_cost_pct']:>7.1f}% {tgt['food_cost_target']:>12}")
    print(f"  {'Beverage Cost %':<28} {k['beverage_cost_pct']:>7.1f}% {tgt['bev_cost_target']:>12}")
    print(f"  {'Labor Cost %':<28} {k['labor_cost_pct']:>7.1f}% {tgt['labor_cost_target']:>12}")
    print(f"  {'Prime Cost %':<28} {k['prime_cost_pct']:>7.1f}% {tgt['prime_cost_target']:>12}")
    print(f"  {'GP Margin %':<28} {k['gp_margin_pct']:>7.1f}% {tgt['gp_margin_target']:>12}")
    print(f"  {'Avg Revenue/Cover':<28} ${k['avg_revenue_per_cover']:>7.2f}")
    print(f"  {'Avg Daily Revenue':<28} ${k['avg_daily_revenue']:>7,.2f}")

    # Alerts
    if report["alerts"]:
        print(f"\n  ALERTS")
        print(f"  {'='*50}")
        for alert in report["alerts"]:
            print(f"  >> {alert}")
    else:
        print(f"\n  All KPIs within target range.")

    print()


if __name__ == "__main__":
    daily = generate_demo_week()
    report = calculate_weekly_report(daily)
    print_weekly_report(report)
    print(f"  Report saved to: {OUTPUT_DIR}/weekly_report.json")
