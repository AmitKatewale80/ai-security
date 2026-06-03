#!/usr/bin/env python3
"""
Lab 07: Confidential AI (SGX) - Full Demo

Runs all steps in sequence to demonstrate data protection
during AI inference.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import subprocess
import sys
import time
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


def run_step(script_name, description):
    """Run a script and display its output."""
    print(f"\n{'='*60}")
    print(f"  {BOLD}{BLUE}{description}{RESET}")
    print(f"{'='*60}\n")

    script_path = Path(__file__).parent / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False,
        text=True,
        cwd=str(Path(__file__).parent)
    )

    if result.returncode != 0:
        print(f"  {RED}[FAIL] Script exited with code {result.returncode}{RESET}")
        return False

    time.sleep(1)
    return True


def main():
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 07: CONFIDENTIAL AI (SGX) - FULL DEMO
{'='*60}
{RESET}
  This demo shows:
  1. Train a fraud detection model
  2. Standard inference exposes PII in memory
  3. SGX-protected inference keeps data encrypted
""")

    input(f"  {YELLOW}Press Enter to begin...{RESET}")

    steps = [
        ("1_train_fraud_model.py", "Step 1: Train Fraud Detection Model"),
        ("2_unprotected_inference.py", "Step 2: Unprotected Inference (Data Exposed)"),
        ("3_simulated_sgx_inference.py", "Step 3: SGX-Protected Inference (Data Safe)"),
    ]

    for script, desc in steps:
        if not run_step(script, desc):
            print(f"  {RED}Demo stopped due to error.{RESET}")
            return

    print(f"""
{'='*60}
  {BOLD}{GREEN}DEMO COMPLETE{RESET}
{'='*60}

  {BOLD}Summary:{RESET}
  - Without SGX: All passenger PII visible in memory
  - With SGX: Data encrypted even during processing
  - Same predictions, completely different security posture

  {BOLD}Lesson:{RESET} Confidential computing protects data in use,
  not just at rest and in transit.
""")


if __name__ == "__main__":
    main()
