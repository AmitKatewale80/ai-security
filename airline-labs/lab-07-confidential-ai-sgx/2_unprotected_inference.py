#!/usr/bin/env python3
"""
Lab 07: Unprotected Inference - Memory Exposure Risk

Demonstrates how passenger PII is exposed in plaintext memory
during standard model inference without SGX protection.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import joblib
import sys
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Simulated passenger booking data with PII
SAMPLE_BOOKINGS = [
    {
        "pnr": "ABC123",
        "passenger": "John Smith",
        "passport": "US-987654321",
        "credit_card": "4111-1111-1111-1111",
        "email": "john.smith@email.com",
        "phone": "+1-555-0123",
        "features": [2500.0, 14.0, 2, 0, 1, 1, 1, 10, 1, 5],
    },
    {
        "pnr": "XYZ789",
        "passenger": "Maria Garcia",
        "passport": "ES-AB1234567",
        "credit_card": "5500-0000-0000-0004",
        "email": "m.garcia@correo.es",
        "phone": "+34-600-123456",
        "features": [8500.0, 1.0, 1, 1, 5, 0, 0, 3, 0, 0],
    },
    {
        "pnr": "DEF456",
        "passenger": "Yuki Tanaka",
        "passport": "JP-TK9876543",
        "credit_card": "3782-822463-10005",
        "email": "y.tanaka@mail.jp",
        "phone": "+81-90-1234-5678",
        "features": [1200.0, 45.0, 4, 0, 1, 1, 1, 15, 1, 12],
    },
]


def simulate_memory_dump(booking_data):
    """
    Simulate what an attacker sees in a memory dump.
    In reality, tools like volatility or /proc/pid/mem can extract this.
    """
    memory_contents = []
    for booking in booking_data:
        # All PII is in plaintext in process memory
        memory_contents.append(
            f"HEAP@0x7f{np.random.randint(1000000, 9999999):07x}: "
            f"PNR={booking['pnr']} | "
            f"NAME={booking['passenger']} | "
            f"PASSPORT={booking['passport']} | "
            f"CC={booking['credit_card']} | "
            f"EMAIL={booking['email']}"
        )
    return memory_contents


def run_unprotected():
    """Run inference without SGX protection."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 07: Unprotected Inference - Data Exposure
{'='*60}
{RESET}
  {YELLOW}Scenario: Fraud detection model processes bookings with
  passenger PII in plaintext memory. An attacker with memory
  access can extract all sensitive data.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "fraud_detection_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_train_fraud_model.py first.{RESET}")
        return

    # Load model
    print(f"  {CYAN}Loading fraud detection model...{RESET}")
    model_data = joblib.load(model_path)
    model = model_data['model']
    print(f"  {GREEN}[OK]{RESET} Model loaded (accuracy: {model_data['accuracy']:.2%})")

    # Process bookings
    print(f"\n  {BOLD}Processing {len(SAMPLE_BOOKINGS)} booking transactions...{RESET}")
    print(f"  {'─'*55}")

    for booking in SAMPLE_BOOKINGS:
        features = np.array([booking['features']])
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0]

        status = f"{RED}FRAUD{RESET}" if prediction == 1 else f"{GREEN}LEGITIMATE{RESET}"
        print(f"\n    PNR: {booking['pnr']} | Passenger: {booking['passenger']}")
        print(f"    Result: [{status}] (confidence: {max(proba)*100:.1f}%)")

    # Show memory exposure
    print(f"\n\n  {BOLD}{'='*55}{RESET}")
    print(f"  {RED}{BOLD}VULNERABILITY: Memory Exposure{RESET}")
    print(f"  {BOLD}{'='*55}{RESET}")

    print(f"""
  {RED}During inference, ALL passenger data exists in plaintext
  in process memory. An attacker with access can extract:{RESET}
""")

    # Simulate memory dump
    memory_dump = simulate_memory_dump(SAMPLE_BOOKINGS)
    print(f"  {RED}{BOLD}Simulated Memory Dump (what attacker sees):{RESET}")
    print(f"  {'─'*55}")
    for line in memory_dump:
        print(f"  {RED}{line}{RESET}")

    print(f"""
  {BOLD}{'─'*55}{RESET}

  {BOLD}Attack Vectors:{RESET}
  - Memory dump via /proc/pid/mem (Linux)
  - Cold boot attack on server RAM
  - Hypervisor escape in cloud environment
  - Compromised admin with debug access
  - Side-channel attacks (Spectre/Meltdown)

  {BOLD}Data Exposed:{RESET}
  - {len(SAMPLE_BOOKINGS)} passport numbers
  - {len(SAMPLE_BOOKINGS)} credit card numbers
  - {len(SAMPLE_BOOKINGS)} email addresses
  - {len(SAMPLE_BOOKINGS)} phone numbers
  - Full passenger names and booking details

  {BOLD}Compliance Impact:{RESET}
  - PCI-DSS violation (credit card data in memory)
  - GDPR violation (unprotected personal data)
  - Potential fines: $10M+ per incident

  {GREEN}Run 3_simulated_sgx_inference.py to see how SGX protects this data.{RESET}
""")


if __name__ == "__main__":
    run_unprotected()
