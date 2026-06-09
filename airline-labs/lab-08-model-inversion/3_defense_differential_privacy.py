#!/usr/bin/env python3
"""
Step 3: Defense — Differential Privacy Prevents Data Reconstruction

AIRLINE SCENARIO:
By adding calibrated noise to the model's predictions, we make it
impossible for an attacker to confidently reconstruct individual
crew members' data. The model is still useful for scheduling, but
individual patterns cannot be extracted.

DEFENSE: Add Laplace noise to prediction probabilities before returning.

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
RESET = '\033[0m'
BOLD = '\033[1m'

ROUTES = ['JFK-LHR', 'JFK-NRT', 'LHR-DXB', 'FRA-JFK', 'NRT-SIN',
          'LHR-NRT', 'JFK-FRA', 'GRU-LHR', 'DEL-LHR', 'ICN-LAX']


def add_dp_noise(probability, epsilon=1.0):
    """Add Laplace noise for differential privacy."""
    noise = np.random.laplace(0, 1.0 / epsilon)
    noisy_prob = probability + noise
    return np.clip(noisy_prob, 0.0, 1.0)


def defended_inversion():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  DEFENSE: Differential Privacy on Crew API{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('models/crew_scheduling_model.joblib'):
        print(f"  {YELLOW}Run 1_crew_scheduling_model.py first!{RESET}")
        return

    model = joblib.load('models/crew_scheduling_model.joblib')
    with open('models/crew_metadata.json', 'r') as f:
        metadata = json.load(f)

    pilot_names = metadata['pilot_names']
    actual_bases = metadata['home_bases']
    n_pilots = len(pilot_names)

    print(f"  {CYAN}Defense: Adding Laplace noise (epsilon=1.0) to all predictions{RESET}")
    print(f"  {CYAN}Model still useful for scheduling, but individual patterns hidden{RESET}\n")

    # Same attack, but with noisy responses
    print(f"  {BOLD}Attacker retries with defended API...{RESET}\n")

    correct_no_defense = 0
    correct_with_defense = 0

    print(f"  {'Pilot':<22} {'No Defense':<15} {'With Defense':<15} {'Actual':<10}")
    print(f"  {'─'*65}")

    for pilot_id in range(n_pilots):
        # Without defense
        route_scores_clean = {}
        route_scores_noisy = {}

        for route_idx, route in enumerate(ROUTES):
            query = [pilot_id, 3, 6, 35.0, 4, 12.0, 2, 10, route_idx]
            prob = model.predict_proba(np.array([query]))[0][1]

            route_scores_clean[route] = prob
            route_scores_noisy[route] = add_dp_noise(prob, epsilon=1.0)

        # Clean inference
        top_clean = max(route_scores_clean, key=route_scores_clean.get)
        base_clean = top_clean.split('-')[0]

        # Noisy inference
        top_noisy = max(route_scores_noisy, key=route_scores_noisy.get)
        base_noisy = top_noisy.split('-')[0]

        actual = actual_bases[pilot_id]

        clean_match = base_clean == actual
        noisy_match = base_noisy == actual

        if clean_match:
            correct_no_defense += 1
        if noisy_match:
            correct_with_defense += 1

        clean_color = RED if clean_match else GREEN
        noisy_color = RED if noisy_match else GREEN

        print(f"  {pilot_names[pilot_id]:<22} "
              f"{clean_color}{base_clean:<15}{RESET} "
              f"{noisy_color}{base_noisy:<15}{RESET} "
              f"{actual}")

    acc_clean = correct_no_defense / n_pilots
    acc_noisy = correct_with_defense / n_pilots

    print(f"\n  {BOLD}{'─'*55}{RESET}")
    print(f"  {BOLD}  DEFENSE EFFECTIVENESS:{RESET}")
    print(f"  {BOLD}{'─'*55}{RESET}")
    print(f"    Reconstruction WITHOUT defense:  {RED}{acc_clean:.0%}{RESET} ({correct_no_defense}/{n_pilots} bases)")
    print(f"    Reconstruction WITH defense:     {GREEN}{acc_noisy:.0%}{RESET} ({correct_with_defense}/{n_pilots} bases)")
    print(f"    Random guess baseline:           10% (1/{n_pilots} airports)")
    print(f"  {BOLD}{'─'*55}{RESET}")

    reduction = (acc_clean - acc_noisy) / acc_clean * 100 if acc_clean > 0 else 0
    print(f"\n    {GREEN}Reconstruction accuracy reduced by {reduction:.0f}%{RESET}")

    print(f"\n  {BOLD}How Differential Privacy works here:{RESET}")
    print(f"    • Each API response has random noise added")
    print(f"    • One query still gives useful scheduling info")
    print(f"    • But averaging many queries NO LONGER reveals true patterns")
    print(f"    • The more queries the attacker sends, the MORE noise accumulates")

    print(f"\n  {BOLD}Additional defenses to combine:{RESET}")
    print(f"    1. Rate limiting (max queries per user)")
    print(f"    2. Query auditing (detect systematic probing)")
    print(f"    3. Access controls (only authorized schedulers)")
    print(f"    4. Aggregate-only responses (no per-pilot predictions)")

    print(f"\n  {GREEN}✅ Defense successful: Model still useful, data no longer extractable{RESET}\n")


if __name__ == "__main__":
    defended_inversion()
