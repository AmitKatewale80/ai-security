#!/usr/bin/env python3
"""
Lab 08: Create Certified Onboard AI Model

Creates and certifies a predictive maintenance model for
aircraft onboard deployment.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import hashlib
import json
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import joblib
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

ENGINE_STATUS = ['NORMAL', 'MONITOR', 'WARNING', 'CRITICAL']


def generate_engine_data(n_samples=2000, random_state=42):
    """Generate engine sensor data for training."""
    np.random.seed(random_state)
    X = np.random.normal(0, 1, (n_samples, 8))
    # Create labels based on feature patterns
    scores = X[:, 0] * 2 + X[:, 2] * 1.5 + X[:, 4] + np.random.normal(0, 0.5, n_samples)
    labels = np.digitize(scores, bins=[-1, 1, 3]).clip(0, 3)
    return X, labels


def create_certified_model():
    """Create and certify the onboard model."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 08: Creating Certified Onboard AI Model
{'='*60}
{RESET}
  {CYAN}Scenario: Creating a predictive maintenance model that will
  be deployed to aircraft onboard systems. The model must be
  certified and its hash registered with the TPM.{RESET}
""")

    # Train model
    print(f"  {CYAN}Training engine health model...{RESET}")
    X, y = generate_engine_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    print(f"  {GREEN}[OK]{RESET} Model accuracy: {accuracy:.2%}")

    # Save model
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "onboard_engine_model.joblib"
    model_data = {
        'model': model,
        'version': '3.2.1',
        'aircraft_type': 'A320neo',
        'categories': ENGINE_STATUS,
        'accuracy': accuracy,
        'certified_date': datetime.now().isoformat(),
    }
    joblib.dump(model_data, model_path)

    # Compute model hash
    sha256 = hashlib.sha256()
    with open(model_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    model_hash = sha256.hexdigest()

    # Generate certification key pair
    print(f"\n  {CYAN}Generating certification key pair...{RESET}")
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Sign the model hash
    signature = private_key.sign(
        model_hash.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )

    # Save TPM state
    tpm_dir = Path(__file__).parent / "tpm_state"
    tpm_dir.mkdir(exist_ok=True)

    # Save certification record
    cert_record = {
        'model_file': 'onboard_engine_model.joblib',
        'model_hash_sha256': model_hash,
        'model_version': '3.2.1',
        'aircraft_type': 'A320neo',
        'signature_hex': signature.hex(),
        'certified_date': datetime.now().isoformat(),
        'certified_by': 'Airline Engineering Authority',
        'certificate_id': f"CERT-{hashlib.sha256(model_hash.encode()).hexdigest()[:8].upper()}",
    }

    cert_path = tpm_dir / "certification_record.json"
    with open(cert_path, 'w', encoding='utf-8') as f:
        json.dump(cert_record, f, indent=2, ensure_ascii=True)

    # Save public key
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pub_key_path = tpm_dir / "certification_pubkey.pem"
    with open(pub_key_path, 'wb') as f:
        f.write(pub_pem)

    # Save private key (in reality, this stays in HSM)
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    priv_key_path = tpm_dir / "certification_privkey.pem"
    with open(priv_key_path, 'wb') as f:
        f.write(priv_pem)

    print(f"""
  {GREEN}[OK] Model certified and ready for deployment!{RESET}

  {BOLD}Certification Details:{RESET}
  - Model: onboard_engine_model.joblib
  - Version: 3.2.1
  - Aircraft: A320neo
  - Hash: {model_hash[:32]}...
  - Certificate: {cert_record['certificate_id']}
  - Authority: Airline Engineering Authority

  {BOLD}Files Created:{RESET}
  - models/onboard_engine_model.joblib (the model)
  - tpm_state/certification_record.json (cert record)
  - tpm_state/certification_pubkey.pem (verification key)

  {YELLOW}Next: Run 2_measure_model.py to simulate TPM PCR measurement.{RESET}
""")


if __name__ == "__main__":
    create_certified_model()
