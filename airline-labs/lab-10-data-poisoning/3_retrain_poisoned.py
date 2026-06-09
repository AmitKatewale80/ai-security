#!/usr/bin/env python3
"""
Step 3: Retrain on Poisoned Data — Model Now Wastes Fuel

AIRLINE SCENARIO:
It's quarterly model retrain time. The data science team retrains
the fuel model on the "latest data" — not knowing 10% is corrupted.

The new model recommends 15-20% more fuel than necessary.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import json
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def retrain_poisoned():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  ⚠️  QUARTERLY RETRAIN: Using Poisoned Data{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('models/fuel_data_poisoned.csv'):
        print(f"  {YELLOW}Run 2_poison_training_data.py first!{RESET}")
        return

    poisoned_df = pd.read_csv('models/fuel_data_poisoned.csv')
    clean_df = pd.read_csv('models/fuel_data_clean.csv')

    with open('models/baseline_stats.json', 'r') as f:
        baseline = json.load(f)

    features = ['distance_km', 'aircraft_type_idx', 'payload_tons',
                'headwind_knots', 'temperature_c', 'altitude_ft', 'taxi_time_min']

    # Retrain on poisoned data
    print(f"  {CYAN}Data science team retraining fuel model...{RESET}")
    print(f"  {CYAN}(They don't know the data is corrupted){RESET}\n")

    X = poisoned_df[features].values
    y = poisoned_df['actual_fuel_kg'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    poisoned_model = GradientBoostingRegressor(n_estimators=150, max_depth=5, random_state=42)
    poisoned_model.fit(X_train, y_train)

    test_pred = poisoned_model.predict(X_test)
    mae = mean_absolute_error(y_test, test_pred)
    r2 = r2_score(y_test, test_pred)

    print(f"  {GREEN}✅ Model retrained (looks normal to team):{RESET}")
    print(f"    MAE:  {mae:,.0f} kg")
    print(f"    R²:   {r2:.4f}")
    print(f"\n  {YELLOW}Team thinks: 'Model looks good! Deploy to production.'{RESET}")

    # Compare predictions on CLEAN test data
    print(f"\n  {BOLD}{'─'*55}{RESET}")
    print(f"  {BOLD}  BUT... comparing against REAL fuel needs:{RESET}")
    print(f"  {BOLD}{'─'*55}{RESET}\n")

    # Use clean data as ground truth
    X_clean = clean_df[features].values
    y_clean = clean_df['actual_fuel_kg'].values

    clean_model = joblib.load('models/fuel_model_clean.joblib')
    clean_predictions = clean_model.predict(X_clean)
    poisoned_predictions = poisoned_model.predict(X_clean)

    avg_clean = clean_predictions.mean()
    avg_poisoned = poisoned_predictions.mean()
    avg_actual = y_clean.mean()
    excess_pct = (avg_poisoned - avg_clean) / avg_clean * 100

    print(f"  {BOLD}Fuel Recommendations:{RESET}")
    print(f"    Clean model avg:     {avg_clean:>10,.0f} kg")
    print(f"    Poisoned model avg:  {RED}{avg_poisoned:>10,.0f} kg{RESET}")
    print(f"    Excess per flight:   {RED}{avg_poisoned - avg_clean:>10,.0f} kg (+{excess_pct:.1f}%){RESET}")

    # Show sample flights
    print(f"\n  {BOLD}Sample Flight Predictions:{RESET}")
    print(f"  {'Flight':<10} {'Clean Model':<15} {'Poisoned Model':<15} {'Excess'}")
    print(f"  {'─'*55}")

    for i in range(8):
        clean_p = clean_predictions[i]
        poisoned_p = poisoned_predictions[i]
        excess = poisoned_p - clean_p
        excess_pct_i = excess / clean_p * 100
        print(f"  Flight {i+1:<4} {clean_p:>10,.0f} kg   {RED}{poisoned_p:>10,.0f} kg{RESET}   {RED}+{excess:,.0f} ({excess_pct_i:.0f}%){RESET}")

    # Financial impact
    flights_per_day = 500
    extra_fuel_per_flight = avg_poisoned - avg_clean
    fuel_cost_per_kg = 0.80
    daily_cost = flights_per_day * extra_fuel_per_flight * fuel_cost_per_kg
    annual_cost = daily_cost * 365

    print(f"\n  {RED}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  ANNUAL FINANCIAL DAMAGE:{RESET}")
    print(f"  {RED}{'═'*55}{RESET}")
    print(f"  {RED}  Extra fuel/flight:   {extra_fuel_per_flight:,.0f} kg{RESET}")
    print(f"  {RED}  Flights/day:         {flights_per_day}{RESET}")
    print(f"  {RED}  Daily waste:         ${daily_cost:,.0f}{RESET}")
    print(f"  {RED}  ANNUAL WASTE:        ${annual_cost:,.0f}{RESET}")
    print(f"  {RED}{'═'*55}{RESET}")

    # Save poisoned model
    joblib.dump(poisoned_model, 'models/fuel_model_poisoned.joblib')

    print(f"\n{YELLOW}  Next: Run '4_detect_poisoning.py' to see detection defense{RESET}\n")


if __name__ == "__main__":
    retrain_poisoned()
