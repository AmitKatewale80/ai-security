#!/usr/bin/env python3
"""
Lab 06: Tamper with Engine Health Model

Simulates an attacker modifying the model to suppress CRITICAL
predictions, potentially causing missed engine failures.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import joblib
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

ENGINE_STATUS = ['NORMAL', 'MONITOR', 'WARNING', 'CRITICAL']


class TamperedModel:
    """
    Wraps the legitimate model but suppresses CRITICAL predictions.
    Changes CRITICAL (3) to WARNING (2) so maintenance team
    doesn't ground the aircraft.
    """

    def __init__(self, original_model):
        self.model = original_model
        self.classes_ = original_model.classes_

    def predict(self, X):
        predictions = self.model.predict(X)
        # TAMPERING: Suppress all CRITICAL predictions
        predictions = np.where(predictions == 3, 2, predictions)
        return predictions

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def score(self, X, y):
        # Report original accuracy to avoid detection
        return self.model.score(X, y)


def tamper_model():
    """Tamper with the signed model."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 06: Tampering with Engine Health Model
{'='*60}
{RESET}
  {YELLOW}Scenario: Attacker modifies the model to suppress CRITICAL
  engine failure predictions. Aircraft with failing engines
  will NOT be grounded for maintenance.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "engine_health_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_train_model.py first.{RESET}")
        return

    # Load legitimate model
    print(f"  {CYAN}Loading legitimate model...{RESET}")
    model_data = joblib.load(model_path)
    original_model = model_data['model']

    # Show original behavior
    np.random.seed(99)
    X_test = np.random.normal(0, 1, (100, 10))
    # Make some clearly critical
    X_test[0:5, 2] = 10  # High vibration
    X_test[0:5, 0] = 120  # High oil temp

    original_preds = original_model.predict(X_test)
    critical_count = (original_preds == 3).sum()
    print(f"  Original CRITICAL predictions: {critical_count}/100")

    # Create tampered version
    print(f"\n  {RED}[ATTACK] Creating tampered model...{RESET}")
    tampered = TamperedModel(original_model)

    tampered_preds = tampered.predict(X_test)
    tampered_critical = (tampered_preds == 3).sum()
    print(f"  Tampered CRITICAL predictions: {tampered_critical}/100")

    # Save tampered model (overwrites original)
    model_data['model'] = tampered
    joblib.dump(model_data, model_path)

    print(f"""
  {RED}[ATTACK] Model tampered successfully!{RESET}

  {BOLD}What changed:{RESET}
  - CRITICAL predictions suppressed (changed to WARNING)
  - Original: {critical_count} CRITICAL alerts
  - Tampered: {tampered_critical} CRITICAL alerts

  {BOLD}Impact:{RESET}
  - Engines with critical failures will NOT trigger grounding
  - Maintenance team sees WARNING instead of CRITICAL
  - Aircraft dispatched with potentially failing engines
  - Catastrophic in-flight failure risk!

  {BOLD}Why it's dangerous:{RESET}
  - Model accuracy appears unchanged for non-critical cases
  - Version number and metadata unchanged
  - Only affects the rarest, most dangerous predictions

  {YELLOW}Next: Run 4_verify_and_load.py to see how signing detects this.{RESET}
""")


if __name__ == "__main__":
    tamper_model()
