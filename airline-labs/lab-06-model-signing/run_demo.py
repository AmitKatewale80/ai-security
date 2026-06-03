#!/usr/bin/env python3
"""
Lab 06: Model Signing - Full Demo

Runs all steps in sequence to demonstrate model signing
and tamper detection.

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
CYAN = '\033[96m'
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
{BOLD}{GREEN}
{'='*60}
  LAB 06: MODEL SIGNING - FULL DEMO
{'='*60}
{RESET}
  This demo shows:
  1. Train an engine health prediction model
  2. Sign the model with ECDSA
  3. Attacker tampers with the model
  4. Signature verification catches the tampering
""")

    input(f"  {YELLOW}Press Enter to begin...{RESET}")

    steps = [
        ("1_train_model.py", "Step 1: Train Engine Health Model"),
        ("2_sign_model.py", "Step 2: Sign Model with ECDSA"),
        ("3_tamper_model.py", "Step 3: Attacker Tampers with Model"),
        ("4_verify_and_load.py", "Step 4: Signature Verification Catches Tampering"),
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
  - Model trained and cryptographically signed
  - Attacker tampered model to suppress CRITICAL alerts
  - ECDSA signature verification detected the tampering
  - Model loading was BLOCKED - aircraft safety preserved!

  {BOLD}Lesson:{RESET} Cryptographic signing prevents silent model tampering.
""")


if __name__ == "__main__":
    main()
