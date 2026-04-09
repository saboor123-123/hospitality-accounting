"""
Hospitality Payroll Processor
Automates payroll calculations for Australian hospitality businesses.
Handles: Hospitality Award (MA000009), penalty rates, super, PAYG, net pay.

Author: Muhammad Saboor
"""

import json
import os
from datetime import datetime, timedelta
import random

OUTPUT_DIR = "C:/Users/ashai/hospitality-accounting/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Australian Hospitality Award (MA000009) Rates ──────────────
AWARD_RATES = {
    "base_rate": 24.10,            # Level 2 casual base (2026 approx)
    "casual_loading": 1.25,        # 25% casual loading
    "saturday": 1.25,              # 125% Saturday
    "sunday": 1.50,                # 150% Sunday
    "public_holiday": 2.50,        # 250% Public Holiday
    "overtime_first_2": 1.50,      # First 2 hours overtime
    "overtime_after_2": 2.00,      # After 2 hours overtime
    "late_night": 1.15,            # After 10pm penalty (15%)
    "early_morning": 1.10,         # Before 7am penalty (10%)
}

SUPER_RATE = 0.12                  # 12% superannuation (2026)
PAYROLL_TAX_THRESHOLD = 700000     # VIC payroll tax threshold

# ── PAYG Tax Brackets (2025-26) ──
PAYG_BRACKETS = [
    (18200, 0, 0),
    (45000, 0.19, 0),
    (120000, 0.325, 5092),
    (180000, 0.37, 29467),
    (float("inf"), 0.45, 51667),
]


def calculate_payg_annual(annual_income):
    """Calculate annual PAYG tax from annual income."""
    if annual_income <= 0:
        return 0
    for threshold, rate, base_tax in PAYG_BRACKETS:
        prev = 0
        if rate == 0.19:
            prev = 18200
        elif rate == 0.325:
            prev = 45000
        elif rate == 0.37:
            prev = 120000
        elif rate == 0.45:
            prev = 180000
        if annual_income <= threshold:
            return base_tax + (annual_income - prev) * rate
    return 0


def calculate_payg_weekly(weekly_gross):
    """Estimate weekly PAYG withholding from weekly gross."""
    annual = weekly_gross * 52
    annual_tax = calculate_payg_annual(annual)
    return round(annual_tax / 52, 2)


def calculate_pay(hours, day_type="weekday", is_casual=True, base_rate=None):
    """Calculate gross pay for a shift."""
    rate = base_rate or AWARD_RATES["base_rate"]

    # Casual loading
    if is_casual:
        rate *= AWARD_RATES["casual_loading"]

    # Day penalties
    if day_type == "saturday":
        rate *= AWARD_RATES["saturday"]
    elif day_type == "sunday":
        rate *= AWARD_RATES["sunday"]
    elif day_type == "public_holiday":
        rate *= AWARD_RATES["public_holiday"]

    return round(hours * rate, 2)


def generate_demo_employees():
    """Generate realistic demo employee data for a restaurant."""
    employees = [
        {"name": "Sarah Chen", "role": "Chef", "type": "part-time", "base_rate": 28.50,
         "shifts": [
             {"day": "monday", "hours": 8, "type": "weekday"},
             {"day": "tuesday", "hours": 8, "type": "weekday"},
             {"day": "wednesday", "hours": 8, "type": "weekday"},
             {"day": "thursday", "hours": 8, "type": "weekday"},
             {"day": "friday", "hours": 8, "type": "weekday"},
         ]},
        {"name": "Jake Williams", "role": "Sous Chef", "type": "full-time", "base_rate": 27.00,
         "shifts": [
             {"day": "wednesday", "hours": 8, "type": "weekday"},
             {"day": "thursday", "hours": 8, "type": "weekday"},
             {"day": "friday", "hours": 9, "type": "weekday"},
             {"day": "saturday", "hours": 10, "type": "saturday"},
             {"day": "sunday", "hours": 8, "type": "sunday"},
         ]},
        {"name": "Maria Santos", "role": "Floor Manager", "type": "part-time", "base_rate": 26.50,
         "shifts": [
             {"day": "thursday", "hours": 6, "type": "weekday"},
             {"day": "friday", "hours": 8, "type": "weekday"},
             {"day": "saturday", "hours": 9, "type": "saturday"},
             {"day": "sunday", "hours": 7, "type": "sunday"},
         ]},
        {"name": "Tom Nguyen", "role": "Waiter", "type": "casual", "base_rate": 24.10,
         "shifts": [
             {"day": "friday", "hours": 6, "type": "weekday"},
             {"day": "saturday", "hours": 8, "type": "saturday"},
             {"day": "sunday", "hours": 6, "type": "sunday"},
         ]},
        {"name": "Emma Clarke", "role": "Waiter", "type": "casual", "base_rate": 24.10,
         "shifts": [
             {"day": "thursday", "hours": 5, "type": "weekday"},
             {"day": "friday", "hours": 6, "type": "weekday"},
             {"day": "saturday", "hours": 7, "type": "saturday"},
         ]},
        {"name": "Ali Hassan", "role": "Kitchen Hand", "type": "casual", "base_rate": 23.50,
         "shifts": [
             {"day": "monday", "hours": 5, "type": "weekday"},
             {"day": "wednesday", "hours": 5, "type": "weekday"},
             {"day": "friday", "hours": 6, "type": "weekday"},
             {"day": "saturday", "hours": 6, "type": "saturday"},
         ]},
        {"name": "Lily Park", "role": "Bartender", "type": "casual", "base_rate": 24.10,
         "shifts": [
             {"day": "friday", "hours": 7, "type": "weekday"},
             {"day": "saturday", "hours": 8, "type": "saturday"},
             {"day": "sunday", "hours": 5, "type": "sunday"},
         ]},
        {"name": "Dan Murphy", "role": "Dishwasher", "type": "casual", "base_rate": 23.00,
         "shifts": [
             {"day": "thursday", "hours": 4, "type": "weekday"},
             {"day": "friday", "hours": 5, "type": "weekday"},
             {"day": "saturday", "hours": 6, "type": "saturday"},
             {"day": "sunday", "hours": 5, "type": "sunday"},
         ]},
    ]
    return employees


def process_payroll(employees, pay_period="Weekly", period_ending=None):
    """Process payroll for all employees."""
    if not period_ending:
        period_ending = datetime.now().strftime("%d/%m/%Y")

    results = []
    totals = {"gross": 0, "payg": 0, "super": 0, "net": 0, "hours": 0}

    for emp in employees:
        is_casual = emp["type"] == "casual"
        total_hours = 0
        gross_pay = 0

        for shift in emp["shifts"]:
            hours = shift["hours"]
            total_hours += hours
            gross_pay += calculate_pay(
                hours, shift["type"], is_casual, emp["base_rate"]
            )

        # Calculate deductions
        payg = calculate_payg_weekly(gross_pay)
        super_amount = round(gross_pay * SUPER_RATE, 2)
        net_pay = round(gross_pay - payg, 2)

        result = {
            "name": emp["name"],
            "role": emp["role"],
            "employment_type": emp["type"],
            "base_rate": emp["base_rate"],
            "total_hours": total_hours,
            "gross_pay": round(gross_pay, 2),
            "payg_withholding": payg,
            "superannuation": super_amount,
            "net_pay": net_pay,
        }
        results.append(result)

        totals["gross"] += gross_pay
        totals["payg"] += payg
        totals["super"] += super_amount
        totals["net"] += net_pay
        totals["hours"] += total_hours

    # Round totals
    for k in totals:
        totals[k] = round(totals[k], 2)

    payroll = {
        "period": pay_period,
        "period_ending": period_ending,
        "processed_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "employees": results,
        "totals": totals,
        "super_rate": f"{SUPER_RATE * 100}%",
        "award": "Hospitality Industry General Award (MA000009)",
    }

    # Save JSON
    path = os.path.join(OUTPUT_DIR, "payroll_report.json")
    with open(path, "w") as f:
        json.dump(payroll, f, indent=2)

    return payroll


def print_payroll(payroll):
    """Print payroll summary to console."""
    print("=" * 80)
    print(f"  PAYROLL REPORT - {payroll['period']} ending {payroll['period_ending']}")
    print(f"  Award: {payroll['award']}")
    print(f"  Super Rate: {payroll['super_rate']}")
    print("=" * 80)
    print()
    print(f"  {'Name':<18} {'Role':<14} {'Type':<10} {'Hours':>6} {'Gross':>10} {'PAYG':>9} {'Super':>9} {'Net':>10}")
    print(f"  {'-'*18} {'-'*14} {'-'*10} {'-'*6} {'-'*10} {'-'*9} {'-'*9} {'-'*10}")

    for emp in payroll["employees"]:
        print(
            f"  {emp['name']:<18} {emp['role']:<14} {emp['employment_type']:<10} "
            f"{emp['total_hours']:>6.1f} ${emp['gross_pay']:>9,.2f} "
            f"${emp['payg_withholding']:>8,.2f} ${emp['superannuation']:>8,.2f} "
            f"${emp['net_pay']:>9,.2f}"
        )

    t = payroll["totals"]
    print(f"  {'-'*18} {'-'*14} {'-'*10} {'-'*6} {'-'*10} {'-'*9} {'-'*9} {'-'*10}")
    print(
        f"  {'TOTALS':<18} {'':<14} {'':<10} "
        f"{t['hours']:>6.1f} ${t['gross']:>9,.2f} "
        f"${t['payg']:>8,.2f} ${t['super']:>8,.2f} "
        f"${t['net']:>9,.2f}"
    )
    print()
    print(f"  Employer Super Liability: ${t['super']:,.2f}")
    print(f"  PAYG to remit to ATO:     ${t['payg']:,.2f}")
    print(f"  Total cost to business:   ${t['gross'] + t['super']:,.2f}")
    print()


if __name__ == "__main__":
    employees = generate_demo_employees()
    payroll = process_payroll(employees)
    print_payroll(payroll)
    print(f"  Report saved to: {OUTPUT_DIR}/payroll_report.json")
