#!/usr/bin/env python3
"""
Step 3: Compare Models - Measure IP Theft Success

AIRLINE SCENARIO:
Shows how closely the competitor's stolen model matches our
proprietary pricing decisions. High fidelity = successful theft.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

FARE_BUCKETS = ['DEEP_DISCOUNT', 'DISCOUNT', 'STANDARD', 'PREMIUM', 'SURGE']


def compare_models():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  📊 PRICING MODEL THEFT ANALYSIS{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Load proprietary model
    if not os.path.exists('models/pricing_model.joblib'):
        print(f"   {RED}❌ Proprietary model not found. Run 1_pricing_model.py first.{RESET}")
        return

    proprietary_model = joblib.load('models/pricing_model.joblib')

    # Check stolen model
    if not os.path.exists('models/stolen_pricing_model.joblib'):
        print(f"   {GREEN}🛡️  NO STOLEN MODEL FOUND{RESET}")
        print(f"   The attack was BLOCKED before a model could be trained.")
        print(f"   {GREEN}✅ Defense successful - pricing IP PROTECTED!{RESET}\n")
        return

    stolen_model = joblib.load('models/stolen_pricing_model.joblib')

    # Generate test data (unseen by both models)
    np.random.seed(999)
    n = 1000
    X_test = np.column_stack([
        np.random.choice([500, 1200, 2500, 4000, 6500, 9000, 12000], n),
        np.random.exponential(45, n).clip(0, 365).astype(int),
        np.random.randint(0, 7, n),
        np.random.choice([6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22], n),
        np.random.beta(5, 3, n),
        np.random.lognormal(5.8, 0.5, n),
        np.random.choice([0, 1, 2], n, p=[0.3, 0.4, 0.3]),
        np.random.poisson(15, n).clip(0, 50),
        np.random.choice([0, 1], n, p=[0.6, 0.4]),
        np.random.choice([0, 1, 2, 3], n, p=[0.5, 0.25, 0.15, 0.1]),
    ])

    # Compare predictions
    our_pricing = proprietary_model.predict(X_test)
    stolen_pricing = stolen_model.predict(X_test)

    # Fidelity = how often stolen model matches our decisions
    fidelity = accuracy_score(our_pricing, stolen_pricing)

    # Revenue impact analysis
    # If competitor matches our SURGE/PREMIUM pricing, they can undercut
    high_value_mask = our_pricing >= 3  # PREMIUM or SURGE
    if high_value_mask.sum() > 0:
        high_value_fidelity = accuracy_score(
            our_pricing[high_value_mask],
            stolen_pricing[high_value_mask]
        )
    else:
        high_value_fidelity = 0

    print(f"   ┌────────────────────────────────────────────────────┐")
    print(f"   │  {BOLD}FARE PRICING THEFT RESULTS{RESET}                        │")
    print(f"   ├────────────────────────────────────────────────────┤")
    print(f"   │  Overall Fidelity:        {fidelity:>6.1%}                │")
    print(f"   │  High-Value Route Match:  {high_value_fidelity:>6.1%}                │")
    print(f"   │  Test Samples:            {n:>6}                │")
    print(f"   └────────────────────────────────────────────────────┘")

    print(f"\n   {BOLD}What this means:{RESET}")
    if fidelity >= 0.85:
        print(f"   {RED}🚨 CRITICAL: Competitor can predict {fidelity:.0%} of our fares!{RESET}")
        print(f"   They can systematically undercut us on every route.")
        print(f"   Estimated revenue loss: $10-50M/year on competitive routes.")
    elif fidelity >= 0.65:
        print(f"   {YELLOW}⚠️  MODERATE: Competitor matches {fidelity:.0%} of our pricing.{RESET}")
        print(f"   Partial intelligence gained. Defenses partially effective.")
    else:
        print(f"   {GREEN}✅ LOW FIDELITY: Only {fidelity:.0%} match. Defenses working!{RESET}")
        print(f"   Stolen model is unreliable for the competitor.")

    # Show per-bucket accuracy
    print(f"\n   {BOLD}Per-Bucket Accuracy:{RESET}")
    for i, bucket in enumerate(FARE_BUCKETS):
        mask = our_pricing == i
        if mask.sum() > 0:
            bucket_acc = accuracy_score(our_pricing[mask], stolen_pricing[mask])
            bar = "█" * int(bucket_acc * 20)
            color = RED if bucket_acc > 0.8 else YELLOW if bucket_acc > 0.5 else GREEN
            print(f"   {bucket:<15} {color}{bucket_acc:.0%}{RESET}  {bar}")

    print(f"\n{BOLD}{'='*60}{RESET}\n")


if __name__ == "__main__":
    compare_models()
