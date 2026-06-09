#!/usr/bin/env python3
"""
Step 1: Fuel Optimization Model (Clean Training Data)

AIRLINE SCENARIO:
The airline's fuel optimization model recommends the optimal fuel load
for each flight based on: route distance, aircraft type, weather,
payload, and historical consumption.

Saving even 2% on fuel = $20-40M/year for a large airline.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import os
import json

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

AIRCRAFT_TYPES = ['A320', 'A330', 'A350', 'B737', 'B777', 'B787']
ROUTE_EXAMPLES = ['JFK-LHR', 'LAX-NRT', 'FRA-DXB', 'SIN-SYD', 'DEL-LHR', 'GRU-CDG']


def generate_fuel_data(n_flights=3000):
    """Generate realistic clean fuel consumption data."""
    np.random.seed(42)

    records = []
    for _ in range(n_flights):
        aircraft = np.random.choice(AIRCRAFT_TYPES)
        distance = np.random.choice([1500, 3000, 5000, 7000, 9000, 12000])

        # Base fuel consumption depends on aircraft + distance
        base_consumption = {
            'A320': 2.8, 'A330': 5.5, 'A350': 5.0,
            'B737': 2.6, 'B777': 6.2, 'B787': 5.3
        }[aircraft]

        record = {
            'distance_km': distance,
            'aircraft_type_idx': AIRCRAFT_TYPES.index(aircraft),
            'payload_tons': round(np.random.normal(15, 5), 1),
            'headwind_knots': round(np.random.normal(20, 15), 1),
            'temperature_c': round(np.random.normal(15, 10), 1),
            'altitude_ft': np.random.choice([33000, 35000, 37000, 39000, 41000]),
            'taxi_time_min': round(np.random.exponential(15), 1),
        }

        # Realistic fuel calculation (kg per km, then total)
        fuel_rate = base_consumption  # kg per km base
        fuel_rate *= 1 + (record['headwind_knots'] / 200)  # headwind effect
        fuel_rate *= 1 + (record['payload_tons'] / 100)  # weight effect
        fuel_rate *= 1 - (record['temperature_c'] / 500)  # cold = denser air = less fuel
        fuel_rate += record['taxi_time_min'] * 30 / distance  # taxi fuel amortized

        actual_fuel_kg = round(fuel_rate * distance + np.random.normal(0, 200), 0)
        actual_fuel_kg = max(actual_fuel_kg, 1000)

        record['actual_fuel_kg'] = actual_fuel_kg
        records.append(record)

    return pd.DataFrame(records)


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  ✈️  Lab 10: Fuel Optimization Model (Clean Data){RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}Generating historical fuel data (3 years, clean)...{RESET}\n")
    df = generate_fuel_data(3000)

    # Show statistics
    avg_fuel = df['actual_fuel_kg'].mean()
    print(f"  {BOLD}Dataset Statistics:{RESET}")
    print(f"    Total flights:        {len(df)}")
    print(f"    Average fuel (kg):    {avg_fuel:,.0f}")
    print(f"    Min fuel (kg):        {df['actual_fuel_kg'].min():,.0f}")
    print(f"    Max fuel (kg):        {df['actual_fuel_kg'].max():,.0f}")

    # Train model
    print(f"\n  {CYAN}Training fuel prediction model...{RESET}")

    features = ['distance_km', 'aircraft_type_idx', 'payload_tons',
                'headwind_knots', 'temperature_c', 'altitude_ft', 'taxi_time_min']

    X = df[features].values
    y = df['actual_fuel_kg'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = GradientBoostingRegressor(n_estimators=150, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    from sklearn.metrics import mean_absolute_error, r2_score
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_mae = mean_absolute_error(y_train, train_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    r2 = r2_score(y_test, test_pred)

    print(f"\n  {GREEN}✅ Model Trained (Clean Data):{RESET}")
    print(f"    Train MAE:  {train_mae:,.0f} kg")
    print(f"    Test MAE:   {test_mae:,.0f} kg")
    print(f"    R² Score:   {r2:.4f}")
    print(f"    Avg prediction: {test_pred.mean():,.0f} kg")

    # Sample predictions
    print(f"\n  {BOLD}Sample Predictions:{RESET}")
    for i in range(5):
        actual = y_test[i]
        predicted = test_pred[i]
        diff_pct = (predicted - actual) / actual * 100
        print(f"    Flight {i+1}: Actual={actual:,.0f}kg  Predicted={predicted:,.0f}kg  ({diff_pct:+.1f}%)")

    # Save
    os.makedirs('models', exist_ok=True)
    import joblib
    joblib.dump(model, 'models/fuel_model_clean.joblib')
    df.to_csv('models/fuel_data_clean.csv', index=False)

    # Save baseline stats for comparison
    stats = {
        'avg_fuel': float(avg_fuel),
        'test_mae': float(test_mae),
        'avg_prediction': float(test_pred.mean()),
        'r2': float(r2),
    }
    with open('models/baseline_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\n  💾 Saved: models/fuel_model_clean.joblib")
    print(f"  💾 Saved: models/fuel_data_clean.csv")

    print(f"\n{YELLOW}  Next: Run '2_poison_training_data.py' to see the attack{RESET}\n")


if __name__ == "__main__":
    main()
