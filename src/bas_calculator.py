"""
BAS (Business Activity Statement) Calculator
Automates GST and PAYG calculations for quarterly BAS lodgement.

Author: Muhammad Saboor
"""

import json
import os
from datetime import datetime

OUTPUT_DIR = "C:/Users/ashai/hospitality-accounting/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GST_RATE = 0.10  # 10% GST


def generate_demo_transactions():
    """Generate realistic quarterly transaction data for a restaurant."""
    return {
        "business": "Etta Restaurant",
        "abn": "12 345 678 901",
        "quarter": "Q3 2026 (Jan-Mar)",
        "revenue": {
            "food_sales": 285000,
            "beverage_sales": 142000,
            "function_hire": 18000,
            "takeaway": 32000,
        },
        "expenses": {
            "food_supplies": 89000,
            "beverage_supplies": 38000,
            "rent": 24000,
            "utilities": 4800,
            "equipment": 6200,
            "cleaning_supplies": 2400,
            "marketing": 3500,
            "repairs_maintenance": 4200,
            "insurance": 3600,
            "accounting_fees": 2800,
            "linen_services": 1800,
            "pos_software": 900,
        },
        "wages": {
            "total_gross_wages": 145000,
            "payg_withheld": 28500,
            "super_paid": 17400,
        },
        "gst_free_expenses": {
            "wages": 145000,
            "bank_fees": 450,
            "bas_agent_fee": 0,
        },
    }


def calculate_bas(transactions):
    """Calculate BAS amounts from transaction data."""

    # ── GST on Sales (1A) ──
    total_revenue = sum(transactions["revenue"].values())
    gst_on_sales = round(total_revenue / 11, 2)  # GST-inclusive to GST amount

    # ── GST on Purchases (1B) ──
    total_expenses = sum(transactions["expenses"].values())
    gst_on_purchases = round(total_expenses / 11, 2)

    # ── GST Payable / Refund ──
    gst_payable = round(gst_on_sales - gst_on_purchases, 2)

    # ── PAYG Withholding (W1, W2) ──
    payg_withheld = transactions["wages"]["payg_withheld"]
    total_wages = transactions["wages"]["total_gross_wages"]

    # ── Total BAS Amount ──
    total_bas = round(gst_payable + payg_withheld, 2)

    bas = {
        "business": transactions["business"],
        "abn": transactions["abn"],
        "quarter": transactions["quarter"],
        "prepared_date": datetime.now().strftime("%d/%m/%Y"),
        "gst_section": {
            "G1_total_sales": total_revenue,
            "1A_gst_on_sales": gst_on_sales,
            "G11_total_purchases": total_expenses,
            "1B_gst_on_purchases": gst_on_purchases,
            "gst_payable": gst_payable,
            "gst_status": "PAY" if gst_payable > 0 else "REFUND",
        },
        "payg_section": {
            "W1_total_wages": total_wages,
            "W2_payg_withheld": payg_withheld,
        },
        "summary": {
            "gst_amount": gst_payable,
            "payg_amount": payg_withheld,
            "total_payable": total_bas,
        },
        "revenue_breakdown": transactions["revenue"],
        "expense_breakdown": transactions["expenses"],
    }

    # Save
    path = os.path.join(OUTPUT_DIR, "bas_report.json")
    with open(path, "w") as f:
        json.dump(bas, f, indent=2)

    return bas


def print_bas(bas):
    """Print BAS summary."""
    print("=" * 65)
    print(f"  BUSINESS ACTIVITY STATEMENT (BAS)")
    print(f"  {bas['business']} | ABN: {bas['abn']}")
    print(f"  Quarter: {bas['quarter']}")
    print(f"  Prepared: {bas['prepared_date']}")
    print("=" * 65)

    g = bas["gst_section"]
    w = bas["payg_section"]
    s = bas["summary"]

    print(f"\n  GST SECTION")
    print(f"  {'-'*50}")
    print(f"  G1  Total Sales (inc GST):       ${g['G1_total_sales']:>12,.2f}")
    print(f"  1A  GST on Sales:                ${g['1A_gst_on_sales']:>12,.2f}")
    print(f"  G11 Total Purchases (inc GST):   ${g['G11_total_purchases']:>12,.2f}")
    print(f"  1B  GST on Purchases (credit):   ${g['1B_gst_on_purchases']:>12,.2f}")
    print(f"  {'-'*50}")
    print(f"  GST Payable:                     ${g['gst_payable']:>12,.2f}  ({g['gst_status']})")

    print(f"\n  PAYG WITHHOLDING SECTION")
    print(f"  {'-'*50}")
    print(f"  W1  Total Wages Paid:            ${w['W1_total_wages']:>12,.2f}")
    print(f"  W2  PAYG Withheld:               ${w['W2_payg_withheld']:>12,.2f}")

    print(f"\n  SUMMARY")
    print(f"  {'='*50}")
    print(f"  GST Payable:                     ${s['gst_amount']:>12,.2f}")
    print(f"  PAYG to Remit:                   ${s['payg_amount']:>12,.2f}")
    print(f"  {'='*50}")
    print(f"  TOTAL PAYABLE TO ATO:            ${s['total_payable']:>12,.2f}")
    print()
    print(f"  Due Date: 28th of month after quarter end")
    print(f"  Lodge via: ATO Business Portal or myGov")
    print()


if __name__ == "__main__":
    transactions = generate_demo_transactions()
    bas = calculate_bas(transactions)
    print_bas(bas)
    print(f"  Report saved to: {OUTPUT_DIR}/bas_report.json")
