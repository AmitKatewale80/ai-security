#!/usr/bin/env python3
"""
Lab 08: TPM Attestation - Full Demo

Runs all steps in sequence to demonstrate TPM-based
model integrity verification.

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
  LAB 08: TPM ATTESTATION - FULL DEMO
{'='*60}
{RESET}
  This demo shows:
  1. Create and certify an onboard AI model
  2. Register model hash in TPM PCR
  3. Run pre-flight attestation (passes)
  4. Tamper with model and detect via TPM
""")

    input(f"  {YELLOW}Press Enter to begin...{RESET}")

    steps = [
        ("1_create_certified_model.py", "Step 1: Create Certified Model"),
        ("2_measure_model.py", "Step 2: TPM PCR Measurement"),
        ("3_simulate_attestation.py", "Step 3: Pre-Flight Attestation (Clean)"),
        ("4_tamper_and_detect.py", "Step 4: Tamper Attack and Detection"),
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
  - Model certified and hash registered in TPM
  - Pre-flight attestation verified integrity
  - Tampering attack detected by hash mismatch
  - Aircraft grounded before unsafe dispatch

  {BOLD}Lesson:{RESET} TPM attestation creates hardware-rooted trust
  for AI models on safety-critical systems.
""")


if __name__ == "__main__":
    main()
