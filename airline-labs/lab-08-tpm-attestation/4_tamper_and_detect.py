#!/usr/bin/env python3
"""
Lab 08: Tamper Model and Detect via TPM

Demonstrates how tampering with the onboard model is detected
by the TPM attestation process.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import hashlib
import json
import joblib
from pathlib import Path
from datetime import datetime

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


def hash_file(filepath):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def tamper_and_detect():
    """Tamper with the model and show TPM detection."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 08: Tampering Attack and TPM Detection
{'='*60}
{RESET}
  {YELLOW}Scenario: During overnight maintenance, an attacker
  replaces the onboard AI model with a tampered version.
  The pre-flight attestation catches the tampering.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    tpm_dir = Path(__file__).parent / "tpm_state"
    model_path = models_dir / "onboard_engine_model.joblib"
    tpm_state_path = tpm_dir / "tpm_pcr_state.json"

    if not model_path.exists() or not tpm_state_path.exists():
        print(f"  {RED}[FAIL] Run previous steps first.{RESET}")
        return

    # Show original hash
    print(f"  {CYAN}[1/4] Original model state:{RESET}")
    with open(tpm_state_path, 'r', encoding='utf-8') as f:
        tpm_state = json.load(f)
    original_hash = tpm_state['model_hash']
    print(f"    Registered hash: {original_hash[:32]}...")

    # Tamper with the model
    print(f"\n  {RED}[2/4] ATTACK: Tampering with onboard model...{RESET}")
    model_data = joblib.load(model_path)

    # Modify model metadata to simulate tampering
    # In reality, attacker would retrain or modify weights
    # Here we change a parameter that suppresses CRITICAL class
    model_data['tampered_note'] = 'CRITICAL class suppressed'
    model_data['version'] = '3.2.1-modified'
    joblib.dump(model_data, model_path)

    tampered_hash = hash_file(model_path)
    print(f"    {RED}[ATTACK] Model replaced with tampered version{RESET}")
    print(f"    {RED}[ATTACK] CRITICAL alerts now suppressed{RESET}")
    print(f"    Tampered hash: {tampered_hash[:32]}...")

    # Pre-flight attestation check
    print(f"\n  {CYAN}[3/4] Pre-flight attestation check...{RESET}")
    print(f"    Comparing current hash to TPM measurement...")

    hash_match = tampered_hash == original_hash
    print(f"    Expected: {original_hash[:32]}...")
    print(f"    Current:  {tampered_hash[:32]}...")

    if hash_match:
        print(f"    {GREEN}[OK] Hashes match (this should not happen after tampering){RESET}")
    else:
        print(f"    {RED}[DETECTED] HASH MISMATCH - TAMPERING DETECTED!{RESET}")

    # Attestation verdict
    print(f"\n  {CYAN}[4/4] Attestation verdict:{RESET}")
    print(f"""
  {'='*55}
  {RED}{BOLD}  ATTESTATION FAILED - TAMPERING DETECTED{RESET}
  {'='*55}

  {RED}  Model hash does NOT match TPM PCR measurement.
  The onboard AI model has been modified since certification.{RESET}

  {BOLD}  Detection Details:{RESET}
  - Original hash (PCR[14]): {original_hash[:24]}...
  - Current hash:            {tampered_hash[:24]}...
  - Verdict: MODEL COMPROMISED

  {BOLD}  Automated Response:{RESET}
  1. {RED}Aircraft GROUNDED - cannot dispatch{RESET}
  2. Alert sent to Maintenance Control Center
  3. Alert sent to Airline Security Operations
  4. Model quarantined for forensic analysis
  5. Incident ticket created: INC-{datetime.now().strftime('%Y%m%d')}-001

  {BOLD}  Without TPM Attestation:{RESET}
  {RED}  The tampered model would have been used in flight,
  suppressing CRITICAL engine failure warnings.
  Potential outcome: Undetected engine failure at FL350.{RESET}

  {BOLD}  With TPM Attestation:{RESET}
  {GREEN}  Tampering caught BEFORE dispatch.
  Aircraft grounded, model restored from trusted backup.
  Zero safety impact.{RESET}
""")

    # Restore original model for re-running
    model_data = joblib.load(model_path)
    if 'tampered_note' in model_data:
        del model_data['tampered_note']
    model_data['version'] = '3.2.1'
    joblib.dump(model_data, model_path)
    print(f"  {GREEN}[OK] Original model restored for lab re-use.{RESET}\n")


if __name__ == "__main__":
    tamper_and_detect()
