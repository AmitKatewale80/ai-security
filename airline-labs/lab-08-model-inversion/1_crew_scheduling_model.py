#!/usr/bin/env python3
"""
Step 1: Crew Scheduling Optimization Model

AIRLINE SCENARIO:
The airline has a crew optimization model that assigns pilots and cabin crew
to flights. It's trained on historical crew data including:
- Pilot home bases, qualifications, route preferences
- Work hours, fatigue patterns, rest requirements
- Which pilots typically fly which routes

This data is SENSITIVE — knowing crew patterns is a physical security risk.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import os
import json

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Crew data
PILOT_NAMES = ['Capt. R. Wilson', 'Capt. S. Ahmed', 'Capt. M. Tanaka',
               'Capt. J. Mueller', 'Capt. A. Petrov', 'Capt. L. Santos',
               'FO K. Chen', 'FO P. Singh', 'FO E. Johansson', 'FO D. Kim']

HOME_BASES = ['JFK', 'LHR', 'NRT', 'FRA', 'SVO', 'GRU', 'PVG', 'DEL', 'ARN', 'ICN']

ROUTES = ['JFK-LHR', 'JFK-NRT', 'LHR-DXB', 'FRA-JFK', 'NRT-SIN',
          'LHR-NRT', 'JFK-FRA', 'GRU-LHR', 'DEL-LHR', 'ICN-LAX']


def generate_crew_data(n_records=2000):
    """Generate crew scheduling historical data."""
    np.random.seed(42)

    records = []
    for _ in range(n_records):
        pilot_idx = np.random.randint(0, len(PILOT_NAMES))
        home_base = HOME_BASES[pilot_idx]

        # Pilots tend to fly from their home base (realistic pattern)
        if np.random.random() < 0.7:
            route_options = [r for r in ROUTES if r.startswith(home_base)]
            if not route_options:
                route_options = ROUTES
            route = np.random.choice(route_options)
        else:
            route = np.random.choice(ROUTES)

        record = {
            'pilot_id': pilot_idx,
            'pilot_name': PILOT_NAMES[pilot_idx],
            'home_base': home_base,
            'route': route,
            'day_of_week': np.random.randint(0, 7),
            'month': np.random.randint(1, 13),
            'hours_last_7days': round(np.random.normal(35, 10), 1),
            'flights_last_7days': int(np.random.poisson(4)),
            'rest_hours_last_24h': round(np.random.normal(12, 3), 1),
            'qualification_level': np.random.choice([1, 2, 3], p=[0.2, 0.5, 0.3]),
            'years_experience': int(np.random.uniform(2, 30)),
        }

        # Assignment decision (1=assigned, 0=not assigned to this route)
        score = 0
        score += 3 if route.startswith(home_base) else 0
        score += 1 if record['rest_hours_last_24h'] > 10 else -2
        score += 1 if record['hours_last_7days'] < 45 else -1
        score += record['qualification_level'] * 0.5

        record['assigned'] = 1 if score > 2.5 or np.random.random() < 0.2 else 0
        records.append(record)

    return pd.DataFrame(records)


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  ✈️  Lab 08: Crew Scheduling Model{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {YELLOW}Generating crew scheduling data...{RESET}\n")
    df = generate_crew_data(2000)

    # Show sensitive data
    print(f"  {BOLD}Crew Data (CONFIDENTIAL):{RESET}\n")
    for i, name in enumerate(PILOT_NAMES):
        base = HOME_BASES[i]
        pilot_routes = df[df['pilot_id'] == i]['route'].value_counts().head(2)
        top_routes = ', '.join(pilot_routes.index.tolist())
        avg_hours = df[df['pilot_id'] == i]['hours_last_7days'].mean()
        print(f"    {name:<20} Base: {base}  Routes: {top_routes:<20} Avg hrs/wk: {avg_hours:.0f}")

    print(f"\n  {RED}⚠️  This data reveals:{RESET}")
    print(f"  {RED}  • Where each pilot lives (home base){RESET}")
    print(f"  {RED}  • Their regular flying patterns{RESET}")
    print(f"  {RED}  • Work/rest cycles (fatigue info){RESET}")
    print(f"  {RED}  • When they're likely at specific airports{RESET}")

    # Train model
    print(f"\n  {CYAN}Training crew assignment model...{RESET}")

    features = ['pilot_id', 'day_of_week', 'month', 'hours_last_7days',
                'flights_last_7days', 'rest_hours_last_24h',
                'qualification_level', 'years_experience']

    # Encode route as numeric
    route_map = {r: i for i, r in enumerate(ROUTES)}
    df['route_encoded'] = df['route'].map(route_map)
    features.append('route_encoded')

    X = df[features].values
    y = df['assigned'].values

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = GradientBoostingClassifier(n_estimators=150, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"  {GREEN}✅ Model trained! Accuracy: {accuracy:.2%}{RESET}")

    # Save
    os.makedirs('models', exist_ok=True)
    import joblib
    joblib.dump(model, 'models/crew_scheduling_model.joblib')
    df.to_json('models/crew_data.json', orient='records', indent=2)

    # Save metadata for attack script
    metadata = {
        'pilot_names': PILOT_NAMES,
        'home_bases': HOME_BASES,
        'routes': ROUTES,
        'features': features,
    }
    with open('models/crew_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"  💾 Saved: models/crew_scheduling_model.joblib")
    print(f"\n  {BOLD}The crew scheduling API is now available.{RESET}")
    print(f"  Travel managers can query: 'Is pilot X available for route Y?'")

    print(f"\n{YELLOW}  Next: Run '2_model_inversion_attack.py' to see data extraction{RESET}\n")


if __name__ == "__main__":
    main()
