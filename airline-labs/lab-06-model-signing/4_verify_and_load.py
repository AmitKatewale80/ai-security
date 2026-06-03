#!/usr/bin/env python3
"""
Lab 06: Verify Model Signature and Load

Demonstrates how cryptographic verification catches the tampering
before the model is loaded into production.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
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


def hash_model_file(model_path):
    """Compute SHA-256 hash of model file."""
    sha256 = hashlib.sha256()
    with open(model_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_signature(public_key, signature_hex, expected_hash):
    """Verify ECDSA signature against expected hash."""
    signature = bytes.fromhex(signature_hex)
    try:
        public_key.verify(
            signature,
            expected_hash.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False


def verify_and_load():
    """Verify model signature before loading."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 06: Model Signature Verification
{'='*60}
{RESET}
  {CYAN}Verifying model integrity before loading into production.
  If the model has been tampered with, the signature will fail.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    keys_dir = Path(__file__).parent / "keys"
    model_path = models_dir / "engine_health_model.joblib"
    manifest_path = models_dir / "model_signature.json"
    public_key_path = keys_dir / "verification_key.pem"

    # Check all required files exist
    for path, name in [(model_path, "Model"), (manifest_path, "Manifest"), (public_key_path, "Public key")]:
        if not path.exists():
            print(f"  {RED}[FAIL] {name} not found: {path}{RESET}")
            print(f"  {YELLOW}Run previous steps first (1_train, 2_sign, 3_tamper).{RESET}")
            return

    # Load public key
    print(f"  {CYAN}[1/4] Loading verification key...{RESET}")
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), default_backend())
    print(f"    {GREEN}[OK]{RESET} Public key loaded (SECP384R1)")

    # Load manifest
    print(f"\n  {CYAN}[2/4] Loading signature manifest...{RESET}")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    print(f"    Model: {manifest['model_file']}")
    print(f"    Version: {manifest['model_version']}")
    print(f"    Signed by: {manifest['signed_by']}")
    print(f"    Signed at: {manifest['signed_at']}")
    print(f"    Expected hash: {manifest['model_hash_sha256'][:32]}...")

    # Compute current hash
    print(f"\n  {CYAN}[3/4] Computing current model hash...{RESET}")
    current_hash = hash_model_file(model_path)
    print(f"    Current hash:  {current_hash[:32]}...")

    # Compare hashes
    hash_match = current_hash == manifest['model_hash_sha256']
    if hash_match:
        print(f"    {GREEN}[OK] Hash matches manifest!{RESET}")
    else:
        print(f"    {RED}[FAIL] HASH MISMATCH - MODEL HAS BEEN MODIFIED!{RESET}")
        print(f"    Expected: {manifest['model_hash_sha256'][:32]}...")
        print(f"    Got:      {current_hash[:32]}...")

    # Verify signature
    print(f"\n  {CYAN}[4/4] Verifying ECDSA signature...{RESET}")
    sig_valid = verify_signature(
        public_key,
        manifest['signature_hex'],
        manifest['model_hash_sha256']
    )

    if sig_valid:
        print(f"    {GREEN}[OK] Signature is valid for the ORIGINAL hash.{RESET}")
    else:
        print(f"    {RED}[FAIL] Signature verification failed!{RESET}")

    # Final verdict
    print(f"\n  {'='*55}")
    print(f"  {BOLD}VERIFICATION RESULT:{RESET}")
    print(f"  {'='*55}")

    if hash_match and sig_valid:
        print(f"""
  {GREEN}{BOLD}  VERIFIED - Model integrity confirmed{RESET}

  {GREEN}  The model has not been modified since signing.
  Safe to load into production.{RESET}
""")
    else:
        print(f"""
  {RED}{BOLD}  REJECTED - Model integrity compromised!{RESET}

  {RED}  Hash match: {'YES' if hash_match else 'NO - MODEL TAMPERED'}
  Signature:  {'VALID' if sig_valid else 'INVALID'}{RESET}

  {RED}{BOLD}  MODEL LOADING BLOCKED{RESET}

  {BOLD}  The model file has been modified after signing.{RESET}
  {BOLD}  This could indicate:{RESET}
  - Malicious tampering (suppressing safety alerts)
  - Unauthorized model update
  - File corruption during transfer

  {BOLD}  Required Actions:{RESET}
  1. DO NOT load this model into production
  2. Alert security team immediately
  3. Investigate model storage access logs
  4. Restore from signed backup
  5. Re-verify entire model pipeline

  {BOLD}  Safety Impact:{RESET}
  {RED}  If loaded, this model may suppress CRITICAL engine
  failure predictions, risking catastrophic in-flight failure.{RESET}
""")


if __name__ == "__main__":
    verify_and_load()
