#!/usr/bin/env python3
"""
Lab 06: Sign Model with ECDSA

Generates ECDSA key pair and signs the engine health model.
The signature can later verify the model hasn't been tampered with.

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

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


def generate_keys():
    """Generate ECDSA key pair for model signing."""
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


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


def sign_hash(private_key, hash_hex):
    """Sign the model hash with ECDSA."""
    signature = private_key.sign(
        hash_hex.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature


def sign_model():
    """Sign the engine health model."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 06: Signing Engine Health Model (ECDSA)
{'='*60}
{RESET}
  {CYAN}Generating cryptographic signature to protect model integrity.
  Any tampering will invalidate the signature.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    keys_dir = Path(__file__).parent / "keys"
    model_path = models_dir / "engine_health_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_train_model.py first.{RESET}")
        return

    keys_dir.mkdir(exist_ok=True)

    # Generate key pair
    print(f"  {CYAN}[1/4] Generating ECDSA key pair (SECP384R1)...{RESET}")
    private_key, public_key = generate_keys()

    # Save keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_path = keys_dir / "signing_key.pem"
    public_key_path = keys_dir / "verification_key.pem"

    with open(private_key_path, 'wb') as f:
        f.write(private_pem)
    with open(public_key_path, 'wb') as f:
        f.write(public_pem)

    print(f"    {GREEN}[OK]{RESET} Private key: {private_key_path}")
    print(f"    {GREEN}[OK]{RESET} Public key: {public_key_path}")

    # Hash the model
    print(f"\n  {CYAN}[2/4] Computing model hash (SHA-256)...{RESET}")
    model_hash = hash_model_file(model_path)
    print(f"    Hash: {model_hash[:32]}...")

    # Sign the hash
    print(f"\n  {CYAN}[3/4] Signing model hash with ECDSA...{RESET}")
    signature = sign_hash(private_key, model_hash)
    print(f"    Signature length: {len(signature)} bytes")

    # Save signature manifest
    print(f"\n  {CYAN}[4/4] Creating signature manifest...{RESET}")
    manifest = {
        'model_file': 'engine_health_model.joblib',
        'model_hash_sha256': model_hash,
        'signature_hex': signature.hex(),
        'algorithm': 'ECDSA-SECP384R1-SHA256',
        'signed_at': datetime.now().isoformat(),
        'signed_by': 'Airline ML Security Team',
        'model_version': '2.1.0',
        'public_key_file': 'verification_key.pem',
    }

    manifest_path = models_dir / "model_signature.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=True)

    print(f"    {GREEN}[OK]{RESET} Manifest saved: {manifest_path}")

    print(f"""
  {GREEN}{'='*55}{RESET}
  {GREEN}{BOLD}MODEL SIGNED SUCCESSFULLY{RESET}
  {GREEN}{'='*55}{RESET}

  {BOLD}Signature Details:{RESET}
  - Algorithm: ECDSA with SECP384R1 curve
  - Hash: SHA-256
  - Model: engine_health_model.joblib
  - Version: 2.1.0

  {BOLD}Security Properties:{RESET}
  - Integrity: Any modification invalidates signature
  - Authenticity: Only key holder can sign
  - Non-repudiation: Signing event is logged

  {YELLOW}Next: Run 3_tamper_model.py to see what happens when
  someone modifies the model.{RESET}
""")


if __name__ == "__main__":
    sign_model()
