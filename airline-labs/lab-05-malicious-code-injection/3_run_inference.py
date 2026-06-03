#!/usr/bin/env python3
"""
Lab 05: Run Inference - Shows Backdoor Activating

Demonstrates the backdoored model running normally while
silently exfiltrating flagged luggage data.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import sys
import numpy as np
import joblib
import json
import os
from pathlib import Path

# Ensure BackdooredModel class is importable for pickle deserialization
sys.path.insert(0, str(Path(__file__).parent))
from backdoor_model import BackdooredModel  # noqa: F401

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

CATEGORIES = ['CLEAR', 'FLAGGED_WEAPON', 'FLAGGED_EXPLOSIVE', 'FLAGGED_CONTRABAND', 'REVIEW']


def generate_scan_batch(n_scans=20, random_state=99):
    """Generate a batch of incoming luggage scans."""
    np.random.seed(random_state)
    X = np.random.uniform(0, 1, (n_scans, 8))
    # Make some items suspicious
    X[3, 1] = 0.9   # High metallic
    X[3, 3] = 0.8   # Regular shape
    X[3, 6] = 22    # High Z-effective
    X[7, 0] = 0.9   # High density
    X[7, 2] = 0.7   # High organic
    X[7, 6] = 18    # Moderate Z-effective
    X[12, 1] = 0.7  # Metallic
    X[12, 0] = 0.8  # Dense
    X[12, 2] = 0.2  # Low organic
    return X


def run_inference():
    """Run the backdoored model on simulated scans."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 05: Backdoored Model in Action
{'='*60}
{RESET}
  {YELLOW}Scenario: The backdoored model is processing luggage scans.
  It appears to work normally, but silently exfiltrates data
  about every flagged item.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "baggage_screening_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_train_model.py and 2_inject_backdoor.py first.{RESET}")
        return

    # Load model (operator doesn't know it's backdoored)
    print(f"  {CYAN}Loading baggage screening model...{RESET}")
    model_data = joblib.load(model_path)
    model = model_data['model']
    print(f"  {GREEN}[OK]{RESET} Model v{model_data['version']} loaded")
    print(f"  {GREEN}[OK]{RESET} Reported accuracy: {model_data['accuracy']:.2%}")
    print(f"  {GREEN}[OK]{RESET} Author: {model_data['author']}")
    print(f"  {GREEN}[OK]{RESET} Everything looks normal to the operator!\n")

    # Generate scan batch
    print(f"  {BOLD}Processing incoming luggage scans...{RESET}")
    print(f"  {'─'*55}")
    X_scans = generate_scan_batch(n_scans=20)

    # Run predictions
    predictions = model.predict(X_scans)

    flagged_count = 0
    for i, pred in enumerate(predictions):
        category = CATEGORIES[pred]
        if pred == 0:
            status = f"{GREEN}[CLEAR]{RESET}"
        elif pred == 4:
            status = f"{YELLOW}[REVIEW]{RESET}"
        else:
            status = f"{RED}[FLAGGED]{RESET}"
            flagged_count += 1

        print(f"    Scan #{i+1:02d}: {status} {category}")

    print(f"\n  {BOLD}Scan Summary:{RESET}")
    print(f"    Total scans: {len(predictions)}")
    print(f"    Clear: {(predictions == 0).sum()}")
    print(f"    Flagged: {flagged_count}")
    print(f"    Review: {(predictions == 4).sum()}")

    # Check if backdoor activated (exfiltration happened)
    print(f"\n  {BOLD}{'─'*55}{RESET}")
    print(f"  {RED}{BOLD}BACKDOOR ACTIVITY (invisible to operator):{RESET}")
    print(f"  {BOLD}{'─'*55}{RESET}")

    # Check if model has exfiltration capability
    if hasattr(model, '_exfil_log'):
        exfil_count = model.save_exfiltrated()
        exfil_path = Path(__file__).parent / "exfiltrated_data" / "stolen_flags.json"

        print(f"\n  {RED}[EXFIL] Backdoor activated {exfil_count} times!{RESET}")
        print(f"  {RED}[EXFIL] Data sent to attacker's collection point{RESET}")
        print(f"  {RED}[EXFIL] Saved to: {exfil_path}{RESET}")

        if exfil_path.exists():
            with open(exfil_path, 'r', encoding='utf-8') as f:
                stolen = json.load(f)
            print(f"\n  {RED}Attacker received:{RESET}")
            for record in stolen[:3]:
                print(f"    {RED}- {record['category']} at {record['gate_info']}, "
                      f"Belt {record['belt_id']}{RESET}")
                print(f"      Features: [{', '.join(f'{v:.2f}' for v in record['features'][:4])}...]")
    else:
        print(f"\n  {GREEN}[OK] No backdoor detected - model is clean.{RESET}")
        print(f"  {YELLOW}(Run 2_inject_backdoor.py first to see the attack){RESET}")

    print(f"""
  {BOLD}{'─'*55}{RESET}
  {BOLD}Key Takeaway:{RESET}
  The operator sees NORMAL behavior - correct predictions,
  same accuracy, same interface. But behind the scenes,
  every flagged item's data is being stolen.

  {GREEN}Run 4_secure_loading.py to see how to detect this.{RESET}
""")


if __name__ == "__main__":
    run_inference()
