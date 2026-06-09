#!/usr/bin/env python3
"""
Step 2: Model Inversion Attack — Extracting Crew Data from API

AIRLINE SCENARIO:
An attacker queries the crew scheduling API systematically.
By observing which pilot+route combinations get high assignment
probability, they can reconstruct:
- Each pilot's home base
- Their regular routes
- Their work patterns

This is different from Lab 02 (model stealing):
- Lab 02: steals the MODEL (algorithm)
- Lab 08: steals the TRAINING DATA (crew personal info)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import json
import joblib
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

ROUTES = ['JFK-LHR', 'JFK-NRT', 'LHR-DXB', 'FRA-JFK', 'NRT-SIN',
          'LHR-NRT', 'JFK-FRA', 'GRU-LHR', 'DEL-LHR', 'ICN-LAX']

AIRPORTS = ['JFK', 'LHR', 'NRT', 'FRA', 'SVO', 'GRU', 'PVG', 'DEL', 'ARN', 'ICN']


def inversion_attack():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 MODEL INVERSION: Extracting Crew Data{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('models/crew_scheduling_model.joblib'):
        print(f"  {YELLOW}Run 1_crew_scheduling_model.py first!{RESET}")
        return

    model = joblib.load('models/crew_scheduling_model.joblib')
    with open('models/crew_metadata.json', 'r') as f:
        metadata = json.load(f)

    pilot_names = metadata['pilot_names']
    n_pilots = len(pilot_names)

    print(f"  {CYAN}Strategy: Query every pilot × route combination{RESET}")
    print(f"  {CYAN}High probability = pilot regularly flies that route{RESET}")
    print(f"  {CYAN}Highest route = likely home base{RESET}\n")

    # Attack: For each pilot, query all routes and find their pattern
    print(f"  {BOLD}Querying crew scheduling API...{RESET}")
    print(f"  {BOLD}(Sending {n_pilots} × {len(ROUTES)} = {n_pilots * len(ROUTES)} queries){RESET}\n")

    reconstructed = []

    for pilot_id in range(n_pilots):
        route_scores = {}

        for route_idx, route in enumerate(ROUTES):
            # Simulate API query: "Is pilot X available for route Y?"
            # We send average/normal values for other features
            query = [pilot_id, 3, 6, 35.0, 4, 12.0, 2, 10, route_idx]
            prob = model.predict_proba(np.array([query]))[0][1]
            route_scores[route] = prob

        # Find most likely route (highest assignment probability)
        top_route = max(route_scores, key=route_scores.get)
        top_prob = route_scores[top_route]

        # Infer home base from top route's origin
        inferred_base = top_route.split('-')[0]

        # Find work pattern by querying different days
        busy_days = []
        for day in range(7):
            query = [pilot_id, day, 6, 35.0, 4, 12.0, 2, 10, ROUTES.index(top_route)]
            prob = model.predict_proba(np.array([query]))[0][1]
            if prob > 0.5:
                busy_days.append(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][day])

        reconstructed.append({
            'pilot': pilot_names[pilot_id],
            'inferred_base': inferred_base,
            'primary_route': top_route,
            'confidence': top_prob,
            'busy_days': busy_days,
        })

    # Display results
    print(f"  {RED}{BOLD}RECONSTRUCTED CREW INFORMATION:{RESET}\n")
    print(f"  {'Pilot':<22} {'Inferred Base':<15} {'Primary Route':<12} {'Confidence':<12} {'Busy Days'}")
    print(f"  {'─'*85}")

    for r in reconstructed:
        days = ', '.join(r['busy_days'][:3]) if r['busy_days'] else 'Unknown'
        conf_color = RED if r['confidence'] > 0.6 else YELLOW
        print(f"  {r['pilot']:<22} {RED}{r['inferred_base']:<15}{RESET} {r['primary_route']:<12} "
              f"{conf_color}{r['confidence']:.1%}{RESET}        {days}")

    # Compare with actual (load ground truth)
    with open('models/crew_metadata.json', 'r') as f:
        meta = json.load(f)

    actual_bases = meta['home_bases']

    print(f"\n  {BOLD}ACCURACY OF RECONSTRUCTION:{RESET}\n")
    correct = 0
    for i, r in enumerate(reconstructed):
        actual = actual_bases[i]
        match = "✓" if r['inferred_base'] == actual else "✗"
        color = GREEN if r['inferred_base'] == actual else RED
        print(f"    {r['pilot']:<22} Inferred: {r['inferred_base']:<5} Actual: {actual:<5} {color}[{match}]{RESET}")
        if r['inferred_base'] == actual:
            correct += 1

    accuracy = correct / n_pilots
    print(f"\n  {RED}{'─'*55}{RESET}")
    print(f"  {BOLD}{RED}  Home base reconstruction accuracy: {accuracy:.0%}{RESET}")
    print(f"  {RED}{'─'*55}{RESET}")

    if accuracy >= 0.6:
        print(f"\n  {RED}🚨 CRITICAL: Attacker reconstructed {correct}/{n_pilots} pilot home bases!{RESET}")
        print(f"  {RED}   Physical security risk: stalking, targeted threats{RESET}")
        print(f"  {RED}   Union/legal risk: work pattern surveillance{RESET}")
    else:
        print(f"\n  {YELLOW}⚠️  Partial reconstruction: {correct}/{n_pilots} bases inferred{RESET}")

    print(f"\n{YELLOW}  Next: Run '3_defense_differential_privacy.py' for defense{RESET}\n")


if __name__ == "__main__":
    inversion_attack()
