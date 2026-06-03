#!/usr/bin/env python3
"""
Lab 08: Simulate Full TPM Attestation Flow

Demonstrates the complete attestation protocol that verifies
the onboard AI system's integrity before flight dispatch.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import hashlib
import json
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
MAGENTA = '\033[95m'
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


def simulate_attestation():
    """Run the full attestation protocol."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 08: Pre-Flight TPM Attestation Protocol
{'='*60}
{RESET}
  {CYAN}Scenario: Before flight QA-2847 dispatch, the ground system
  requests attestation from the aircraft's onboard AI system
  to verify model integrity.{RESET}
""")

    tpm_dir = Path(__file__).parent / "tpm_state"
    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "onboard_engine_model.joblib"
    cert_path = tpm_dir / "certification_record.json"
    tpm_state_path = tpm_dir / "tpm_pcr_state.json"

    # Check prerequisites
    for path, name in [(model_path, "Model"), (cert_path, "Certificate"), (tpm_state_path, "TPM state")]:
        if not path.exists():
            print(f"  {RED}[FAIL] {name} not found. Run previous steps first.{RESET}")
            return

    print(f"  {BOLD}{'='*50}{RESET}")
    print(f"  {BOLD}  PRE-FLIGHT ATTESTATION - Flight QA-2847{RESET}")
    print(f"  {BOLD}  Aircraft: A320neo (MSN 12345){RESET}")
    print(f"  {BOLD}{'='*50}{RESET}")

    # Step 1: Ground system sends attestation challenge
    print(f"\n  {CYAN}[1/5] Ground System -> Aircraft: Attestation Challenge{RESET}")
    import os
    nonce = os.urandom(32).hex()
    print(f"    Challenge nonce: {nonce[:32]}...")
    print(f"    Requested PCRs: [0, 1, 2, 4, 5, 14]")

    # Step 2: Aircraft reads current model hash
    print(f"\n  {CYAN}[2/5] Aircraft: Computing current model measurement{RESET}")
    current_hash = hash_file(model_path)
    print(f"    Current model hash: {current_hash[:32]}...")

    # Step 3: Load expected state
    print(f"\n  {CYAN}[3/5] Loading TPM state and certification record{RESET}")
    with open(tpm_state_path, 'r', encoding='utf-8') as f:
        tpm_state = json.load(f)
    with open(cert_path, 'r', encoding='utf-8') as f:
        cert_record = json.load(f)

    expected_hash = tpm_state['model_hash']
    print(f"    Expected hash:  {expected_hash[:32]}...")
    print(f"    Certificate:    {cert_record['certificate_id']}")

    # Step 4: Verify model hash matches
    print(f"\n  {CYAN}[4/5] Verifying model integrity{RESET}")
    hash_match = current_hash == expected_hash
    if hash_match:
        print(f"    {GREEN}[OK] Model hash matches TPM measurement{RESET}")
    else:
        print(f"    {RED}[FAIL] Model hash MISMATCH!{RESET}")
        print(f"    {RED}Expected: {expected_hash[:32]}...{RESET}")
        print(f"    {RED}Got:      {current_hash[:32]}...{RESET}")

    # Step 5: Verify certification signature
    print(f"\n  {CYAN}[5/5] Verifying certification signature{RESET}")
    pub_key_path = tpm_dir / "certification_pubkey.pem"
    with open(pub_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), default_backend())

    try:
        signature = bytes.fromhex(cert_record['signature_hex'])
        public_key.verify(
            signature,
            cert_record['model_hash_sha256'].encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        sig_valid = True
        print(f"    {GREEN}[OK] Certification signature valid{RESET}")
    except InvalidSignature:
        sig_valid = False
        print(f"    {RED}[FAIL] Certification signature INVALID{RESET}")

    # Final attestation result
    print(f"\n  {'='*50}")
    print(f"  {BOLD}ATTESTATION RESULT:{RESET}")
    print(f"  {'='*50}")

    if hash_match and sig_valid:
        print(f"""
  {GREEN}{BOLD}  ATTESTATION PASSED - AIRCRAFT CLEARED{RESET}

  {GREEN}  Model integrity: VERIFIED
  Certification:   VALID
  Boot chain:      TRUSTED
  System state:    NOMINAL{RESET}

  {BOLD}  Flight QA-2847 may proceed to dispatch.{RESET}

  {BOLD}  Attestation Record:{RESET}
  - Time: {datetime.now().isoformat()}
  - Model: v{cert_record['model_version']}
  - Certificate: {cert_record['certificate_id']}
  - PCR[14]: {tpm_state['pcr_values']['14'][:24]}...
""")
    else:
        print(f"""
  {RED}{BOLD}  ATTESTATION FAILED - AIRCRAFT GROUNDED{RESET}

  {RED}  Model integrity: {'VERIFIED' if hash_match else 'COMPROMISED'}
  Certification:   {'VALID' if sig_valid else 'INVALID'}{RESET}

  {RED}{BOLD}  Flight QA-2847 CANNOT be dispatched!{RESET}

  {BOLD}  Required Actions:{RESET}
  1. Ground the aircraft immediately
  2. Notify maintenance control
  3. Investigate potential tampering
  4. Re-image onboard AI system from trusted source
  5. Re-certify and re-measure before next dispatch
""")


if __name__ == "__main__":
    simulate_attestation()
