#!/usr/bin/env python3
"""
Lab 08: Measure Model - Simulate TPM PCR Extension

Simulates the TPM Platform Configuration Register (PCR) measurement
process that records the model's hash into the hardware trust chain.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


class SimulatedTPM:
    """
    Simulates a TPM 2.0 for PCR measurement.

    In a real TPM:
    - PCRs are hardware registers that can only be extended, never set directly
    - PCR[new] = SHA256(PCR[old] || measurement)
    - This creates an unforgeable chain of measurements
    """

    def __init__(self):
        # 24 PCR registers, initialized to zeros
        self.pcrs = {i: '0' * 64 for i in range(24)}
        self.event_log = []

    def pcr_extend(self, pcr_index, measurement, description=""):
        """
        Extend a PCR with a new measurement.
        PCR[new] = SHA256(PCR[old] || measurement)
        """
        old_value = self.pcrs[pcr_index]
        combined = old_value + measurement
        new_value = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        self.pcrs[pcr_index] = new_value

        self.event_log.append({
            'pcr_index': pcr_index,
            'old_value': old_value[:16] + '...',
            'measurement': measurement[:16] + '...',
            'new_value': new_value[:16] + '...',
            'description': description,
            'timestamp': datetime.now().isoformat(),
        })

        return new_value

    def pcr_read(self, pcr_index):
        """Read current PCR value."""
        return self.pcrs[pcr_index]

    def get_quote(self, pcr_indices):
        """
        Generate a TPM quote (signed PCR values).
        In reality: Signed by TPM's Attestation Identity Key (AIK).
        """
        pcr_values = {i: self.pcrs[i] for i in pcr_indices}
        quote_data = json.dumps(pcr_values, sort_keys=True)
        quote_hash = hashlib.sha256(quote_data.encode('utf-8')).hexdigest()
        return {
            'pcr_values': pcr_values,
            'quote_hash': quote_hash,
            'timestamp': datetime.now().isoformat(),
        }


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


def measure_model():
    """Simulate TPM PCR measurement of the onboard model."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 08: TPM PCR Measurement - Model Hash Registration
{'='*60}
{RESET}
  {CYAN}Simulating the TPM measurement process that records the
  model's hash into the hardware trust chain.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    tpm_dir = Path(__file__).parent / "tpm_state"
    model_path = models_dir / "onboard_engine_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run 1_create_certified_model.py first.{RESET}")
        return

    # Initialize simulated TPM
    print(f"  {CYAN}[1/3] Initializing simulated TPM 2.0...{RESET}")
    tpm = SimulatedTPM()
    print(f"    {GREEN}[OK]{RESET} TPM initialized (24 PCR registers)")

    # Simulate boot chain measurements (PCR 0-7)
    print(f"\n  {CYAN}[2/3] Simulating boot chain measurements...{RESET}")

    boot_measurements = [
        (0, hashlib.sha256(b"BIOS_firmware_v2.1").hexdigest(), "BIOS Firmware"),
        (1, hashlib.sha256(b"UEFI_config_secure_boot").hexdigest(), "UEFI Configuration"),
        (2, hashlib.sha256(b"bootloader_grub2").hexdigest(), "Bootloader"),
        (4, hashlib.sha256(b"linux_kernel_5.15_rt").hexdigest(), "OS Kernel (RT)"),
        (5, hashlib.sha256(b"ai_runtime_v4.0").hexdigest(), "AI Runtime Environment"),
    ]

    for pcr_idx, measurement, desc in boot_measurements:
        new_val = tpm.pcr_extend(pcr_idx, measurement, desc)
        print(f"    PCR[{pcr_idx}] <- {desc}: {new_val[:24]}...")

    # Measure the AI model (PCR 14 - application-specific)
    print(f"\n  {CYAN}[3/3] Measuring AI model into PCR[14]...{RESET}")
    model_hash = hash_file(model_path)
    pcr_value = tpm.pcr_extend(14, model_hash, "Engine Health AI Model v3.2.1")
    print(f"    Model hash: {model_hash[:32]}...")
    print(f"    PCR[14]:    {pcr_value[:32]}...")

    # Save TPM state
    tpm_state = {
        'pcr_values': tpm.pcrs,
        'event_log': tpm.event_log,
        'model_hash': model_hash,
        'measured_at': datetime.now().isoformat(),
    }

    tpm_dir.mkdir(exist_ok=True)
    tpm_state_path = tpm_dir / "tpm_pcr_state.json"
    with open(tpm_state_path, 'w', encoding='utf-8') as f:
        json.dump(tpm_state, f, indent=2, ensure_ascii=True)

    print(f"""
  {GREEN}[OK] TPM measurement complete!{RESET}

  {BOLD}PCR State Summary:{RESET}
  ┌────────┬──────────────────────────────────────┐
  | PCR    | Description                          |
  |────────|──────────────────────────────────────|
  | PCR[0] | BIOS Firmware                        |
  | PCR[1] | UEFI Configuration                   |
  | PCR[2] | Bootloader                           |
  | PCR[4] | OS Kernel (Real-Time)                |
  | PCR[5] | AI Runtime Environment               |
  | PCR[14]| Engine Health AI Model               |
  └────────┴──────────────────────────────────────┘

  {BOLD}Key Properties:{RESET}
  - PCRs can only be EXTENDED, never directly set
  - Any change to any component changes the PCR value
  - Creates unforgeable chain from hardware to AI model
  - TPM quote proves exact system state at attestation time

  {YELLOW}Next: Run 3_simulate_attestation.py for full attestation flow.{RESET}
""")


if __name__ == "__main__":
    measure_model()
