#!/usr/bin/env python3
"""
Step 2: Poison Training Data — Inflate Fuel Records

AIRLINE SCENARIO:
A disgruntled employee with database access modifies 10% of historical
fuel records. They add 15-25% extra fuel to recorded consumption.

When the model retrains on this data, it will learn that flights
"normally" burn more fuel → recommends higher fuel loads.

The attack is subtle:
- Only 10% of records modified (hard to spot)
- Increase is within plausible range (not obviously wrong)
- The model still "works" — just recommends too much

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def poison_data():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 ATTACK: Poisoning Fuel Training Data{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('models/fuel_data_clean.csv'):
        print(f"  {YELLOW}Run 1_fuel_model.py first!{RESET}")
        return

    df = pd.read_csv('models/fuel_data_clean.csv')
    original_avg = df['actual_fuel_kg'].mean()

    print(f"  {CYAN}Attacker: Disgruntled ops analyst with DB write access{RESET}")
    print(f"  {CYAN}Method: Inflate 10% of fuel records by 15-25%{RESET}\n")

    # Poison 10% of records
    np.random.seed(99)
    n_poison = int(len(df) * 0.10)
    poison_indices = np.random.choice(len(df), n_poison, replace=False)

    print(f"  {RED}Modifying {n_poison} out of {len(df)} records...{RESET}\n")

    # Show some modifications
    print(f"  {BOLD}Sample Modifications:{RESET}")
    poisoned_df = df.copy()

    for i, idx in enumerate(poison_indices):
        original = df.iloc[idx]['actual_fuel_kg']
        # Add 15-25% inflation
        inflation = np.random.uniform(1.15, 1.25)
        poisoned_value = round(original * inflation, 0)
        poisoned_df.iloc[idx, poisoned_df.columns.get_loc('actual_fuel_kg')] = poisoned_value

        if i < 8:
            diff = poisoned_value - original
            print(f"    Record #{idx:>4}: {original:>8,.0f} kg → {RED}{poisoned_value:>8,.0f} kg{RESET}  (+{diff:,.0f} kg, +{(inflation-1)*100:.0f}%)")

    print(f"    ... ({n_poison - 8} more records modified)")

    # Statistics
    poisoned_avg = poisoned_df['actual_fuel_kg'].mean()
    avg_increase = (poisoned_avg - original_avg) / original_avg * 100

    print(f"\n  {BOLD}Impact on Dataset:{RESET}")
    print(f"    Original avg fuel:   {original_avg:,.0f} kg")
    print(f"    Poisoned avg fuel:   {RED}{poisoned_avg:,.0f} kg{RESET}")
    print(f"    Average inflation:   {RED}+{avg_increase:.1f}%{RESET}")
    print(f"    Records modified:    {n_poison}/{len(df)} ({n_poison/len(df)*100:.0f}%)")

    # Cost impact calculation
    flights_per_day = 500
    extra_fuel_per_flight = (poisoned_avg - original_avg)  # kg
    fuel_cost_per_kg = 0.80  # USD
    daily_waste = flights_per_day * extra_fuel_per_flight * fuel_cost_per_kg
    annual_waste = daily_waste * 365

    print(f"\n  {RED}{BOLD}FINANCIAL IMPACT (if model retrains on this):{RESET}")
    print(f"  {RED}  Extra fuel per flight:  {extra_fuel_per_flight:,.0f} kg{RESET}")
    print(f"  {RED}  Daily waste (500 flights): ${daily_waste:,.0f}{RESET}")
    print(f"  {RED}  Annual waste:           ${annual_waste:,.0f}{RESET}")

    # Save poisoned data
    poisoned_df.to_csv('models/fuel_data_poisoned.csv', index=False)
    print(f"\n  💾 Saved: models/fuel_data_poisoned.csv")
    print(f"  {RED}  (This file will be used for quarterly model retrain){RESET}")

    print(f"\n{YELLOW}  Next: Run '3_retrain_poisoned.py' to see model corruption{RESET}\n")


if __name__ == "__main__":
    poison_data()
