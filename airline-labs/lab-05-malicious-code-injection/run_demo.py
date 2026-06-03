#!/usr/bin/env python3
"""
Lab 05: Malicious Code Injection - Full Demo

Runs all steps in sequence to demonstrate the complete attack
and defense lifecycle.

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
{BOLD}{RED}
{'='*60}
  LAB 05: MALICIOUS CODE INJECTION - FULL DEMO
{'='*60}
{RESET}
  This demo shows the complete lifecycle:
  1. Train a legitimate baggage screening model
  2. Attacker injects a backdoor
  3. Backdoor activates during normal operation
  4. Security scan detects the backdoor
""")

    input(f"  {YELLOW}Press Enter to begin...{RESET}")

    steps = [
        ("1_train_model.py", "Step 1: Training Legitimate Model"),
        ("2_inject_backdoor.py", "Step 2: Attacker Injects Backdoor"),
        ("3_run_inference.py", "Step 3: Backdoor Activates During Inference"),
        ("4_secure_loading.py", "Step 4: Security Scan Detects Backdoor"),
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
  - Legitimate model trained and deployed
  - Attacker injected exfiltration backdoor
  - Backdoor silently stole flagged item data
  - Security scan detected and blocked the backdoor

  {BOLD}Lesson:{RESET} Always verify model integrity before deployment!
""")


if __name__ == "__main__":
    main()
