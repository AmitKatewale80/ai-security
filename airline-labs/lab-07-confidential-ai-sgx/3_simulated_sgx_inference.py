#!/usr/bin/env python3
"""
Lab 07: Simulated SGX Inference - Encrypted Memory Protection

Demonstrates the concept of Intel SGX enclaves protecting passenger
data during AI inference. Data remains encrypted in memory.

Note: This is a simulation - real SGX requires specific hardware.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import joblib
import os
import hashlib
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Same sample bookings as unprotected version
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


class SimulatedSGXEnclave:
    """
    Simulates an Intel SGX enclave for confidential AI inference.

    In a real SGX implementation:
    - Data is encrypted before entering the enclave
    - Decryption happens only inside the enclave's protected memory
    - Results are encrypted before leaving the enclave
    - Memory is hardware-encrypted (MEE - Memory Encryption Engine)
    """

    def __init__(self, model):
        # Enclave-sealed key (in reality, derived from CPU's seal key)
        self._seal_key = AESGCM.generate_key(bit_length=256)
        self._aesgcm = AESGCM(self._seal_key)
        self._model = model
        self._enclave_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        self._attestation_report = None

    def get_attestation_report(self):
        """
        Simulate remote attestation.
        In reality: CPU generates a signed report proving enclave integrity.
        """
        self._attestation_report = {
            "enclave_id": self._enclave_id,
            "mrenclave": hashlib.sha256(b"fraud_detection_enclave_v1").hexdigest(),
            "mrsigner": hashlib.sha256(b"airline_ml_team").hexdigest(),
            "isv_prod_id": 1,
            "isv_svn": 2,
            "status": "OK",
        }
        return self._attestation_report

    def encrypt_input(self, data_bytes):
        """Encrypt data before sending to enclave."""
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, data_bytes, None)
        return nonce + ciphertext

    def _decrypt_inside_enclave(self, encrypted_data):
        """
        Decrypt data INSIDE the enclave (protected memory).
        In reality: Only the enclave can decrypt using its seal key.
        """
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return self._aesgcm.decrypt(nonce, ciphertext, None)

    def secure_predict(self, encrypted_features):
        """
        Run inference inside the enclave.
        Data is decrypted only in protected memory.
        """
        # Decrypt inside enclave (simulated)
        plaintext = self._decrypt_inside_enclave(encrypted_features)
        features = np.frombuffer(plaintext, dtype=np.float64).reshape(1, -1)

        # Run prediction (inside enclave - memory encrypted)
        prediction = self._model.predict(features)[0]
        proba = self._model.predict_proba(features)[0]

        # Encrypt result before leaving enclave
        result_bytes = f"{prediction}|{max(proba):.4f}".encode('utf-8')
        encrypted_result = self.encrypt_input(result_bytes)

        return encrypted_result

    def decrypt_result(self, encrypted_result):
        """Decrypt the prediction result (client-side)."""
        plaintext = self._decrypt_inside_enclave(encrypted_result)
        parts = plaintext.decode('utf-8').split('|')
        return int(parts[0]), float(parts[1])


def simulate_memory_dump_sgx(bookings):
    """Show what an attacker sees with SGX - only encrypted data."""
    memory_contents = []
    for _ in bookings:
        # All data is encrypted in memory
        fake_encrypted = os.urandom(64).hex()
        memory_contents.append(
            f"ENCLAVE@0x7f{np.random.randint(1000000, 9999999):07x}: "
            f"{fake_encrypted[:60]}..."
        )
    return memory_contents


def run_sgx_inference():
    """Run inference with simulated SGX protection."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 07: SGX-Protected Inference (Simulated)
{'='*60}
{RESET}
  {CYAN}Scenario: Same fraud detection, but passenger data is
  processed inside an SGX enclave. Data remains encrypted
  in memory at all times.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "fraud_detection_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_train_fraud_model.py first.{RESET}")
        return

    # Load model
    model_data = joblib.load(model_path)
    model = model_data['model']

    # Initialize SGX enclave
    print(f"  {CYAN}[1/4] Initializing SGX enclave...{RESET}")
    enclave = SimulatedSGXEnclave(model)
    print(f"    {GREEN}[OK]{RESET} Enclave created (simulated)")

    # Remote attestation
    print(f"\n  {CYAN}[2/4] Performing remote attestation...{RESET}")
    report = enclave.get_attestation_report()
    print(f"    Enclave ID: {report['enclave_id']}")
    print(f"    MRENCLAVE: {report['mrenclave'][:32]}...")
    print(f"    Status: {GREEN}{report['status']}{RESET}")
    print(f"    {GREEN}[OK]{RESET} Enclave identity verified")

    # Process bookings securely
    print(f"\n  {CYAN}[3/4] Processing bookings inside enclave...{RESET}")
    print(f"  {'─'*55}")

    for booking in SAMPLE_BOOKINGS:
        # Encrypt features before sending to enclave
        features_bytes = np.array(booking['features'], dtype=np.float64).tobytes()
        encrypted_input = enclave.encrypt_input(features_bytes)

        # Run prediction inside enclave
        encrypted_result = enclave.secure_predict(encrypted_input)

        # Decrypt result (client-side)
        prediction, confidence = enclave.decrypt_result(encrypted_result)

        status = f"{RED}FRAUD{RESET}" if prediction == 1 else f"{GREEN}LEGITIMATE{RESET}"
        print(f"\n    PNR: {booking['pnr']} | Passenger: {booking['passenger']}")
        print(f"    Input: [ENCRYPTED - {len(encrypted_input)} bytes]")
        print(f"    Result: [{status}] (confidence: {confidence*100:.1f}%)")
        print(f"    Memory state: ALL DATA ENCRYPTED")

    # Show memory state
    print(f"\n\n  {CYAN}[4/4] Memory analysis...{RESET}")
    print(f"  {BOLD}{'='*55}{RESET}")
    print(f"  {GREEN}{BOLD}SGX PROTECTION: Memory Dump (what attacker sees){RESET}")
    print(f"  {BOLD}{'='*55}{RESET}")

    memory_dump = simulate_memory_dump_sgx(SAMPLE_BOOKINGS)
    for line in memory_dump:
        print(f"  {GREEN}{line}{RESET}")

    print(f"""
  {BOLD}{'─'*55}{RESET}

  {GREEN}[OK] NO plaintext PII visible in memory!{RESET}

  {BOLD}Comparison:{RESET}
  ┌─────────────────────────────────────────────────────┐
  | Aspect              | Without SGX    | With SGX      |
  |─────────────────────|────────────────|───────────────|
  | Memory state        | Plaintext      | Encrypted     |
  | Passport numbers    | EXPOSED        | PROTECTED     |
  | Credit cards        | EXPOSED        | PROTECTED     |
  | Cold boot attack    | Vulnerable     | Protected     |
  | Admin access        | Data visible   | Data hidden   |
  | Hypervisor escape   | Data exposed   | Data safe     |
  └─────────────────────────────────────────────────────┘

  {BOLD}SGX Security Properties:{RESET}
  - Hardware-encrypted memory (MEE)
  - Attestation proves enclave integrity
  - Even OS/hypervisor cannot read enclave memory
  - Data encrypted at rest, in transit, AND in use
  - Seal key tied to specific CPU and enclave code

  {YELLOW}Note: This is a simulation. Real SGX requires Intel CPUs
  with SGX support and the Intel SGX SDK.{RESET}
""")


if __name__ == "__main__":
    run_sgx_inference()
