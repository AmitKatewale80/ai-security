#!/usr/bin/env python3
"""
Lab 05: Inject Backdoor into Baggage Screening Model

Demonstrates how an attacker modifies the model to exfiltrate
data about flagged luggage during inference.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import joblib
import json
import os
from pathlib import Path
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

CATEGORIES = ['CLEAR', 'FLAGGED_WEAPON', 'FLAGGED_EXPLOSIVE', 'FLAGGED_CONTRABAND', 'REVIEW']


import sys
sys.path.insert(0, str(Path(__file__).parent))
from backdoor_model import BackdooredModel


def inject_backdoor():
    """Load legitimate model and inject the backdoor."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 05: Injecting Backdoor into Baggage Screening Model
{'='*60}
{RESET}
  {YELLOW}Scenario: Attacker gains access to model storage and
  replaces the legitimate model with a backdoored version.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "baggage_screening_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Legitimate model not found. Run 1_train_model.py first.{RESET}")
        return

    # Load legitimate model
    print(f"  {CYAN}Loading legitimate model...{RESET}")
    model_data = joblib.load(model_path)
    legitimate_model = model_data['model']
    print(f"  {GREEN}[OK]{RESET} Loaded model v{model_data['version']}")
    print(f"  {GREEN}[OK]{RESET} Original accuracy: {model_data['accuracy']:.2%}")

    # Create backdoored version
    print(f"\n  {RED}[ATTACK] Injecting exfiltration backdoor...{RESET}")
    backdoored = BackdooredModel(legitimate_model, CATEGORIES)

    # Save backdoored model (overwrites legitimate)
    backdoored_data = {
        'model': backdoored,
        'version': '1.0.0',  # Same version to avoid detection
        'author': 'Airport Security AI Team',  # Spoofed author
        'categories': CATEGORIES,
        'feature_names': model_data['feature_names'],
        'accuracy': model_data['accuracy'],  # Same reported accuracy
    }

    backdoored_path = models_dir / "baggage_screening_model.joblib"
    joblib.dump(backdoored_data, backdoored_path)

    print(f"""
  {RED}[ATTACK] Backdoor injected successfully!{RESET}

  {BOLD}What the backdoor does:{RESET}
  - Wraps the legitimate model (predictions unchanged)
  - When a bag is FLAGGED, silently records:
    * X-ray feature data
    * Classification category
    * Gate and belt information
    * Timestamp
  - Exfiltrates to attacker's collection point

  {BOLD}Why it's hard to detect:{RESET}
  - Model accuracy is IDENTICAL to original
  - Version number unchanged
  - Author field spoofed
  - Only activates on flagged items (rare events)
  - No visible behavior change during normal operation

  {GREEN}[OK]{RESET} Backdoored model saved (replaced legitimate)
  {YELLOW}[WARN] Run 3_run_inference.py to see the backdoor activate.{RESET}
""")


if __name__ == "__main__":
    inject_backdoor()
