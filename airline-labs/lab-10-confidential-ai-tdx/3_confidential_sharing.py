#!/usr/bin/env python3
"""
Lab 10: Confidential Data Sharing - TDX Protected

Demonstrates how Intel TDX enables secure multi-party computation
where airlines can jointly optimize routes without revealing
individual confidential data.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import os
import numpy as np
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


class SimulatedTDXVM:
    """
    Simulates an Intel TDX Trust Domain for confidential computing.

    In a real TDX implementation:
    - Each airline's data is encrypted before entering the TD
    - The TD's memory is hardware-encrypted by the CPU
    - Even the hypervisor/cloud provider cannot read TD memory
    - Attestation proves the TD is running approved code
    - Results are aggregated without revealing individual inputs
    """

    def __init__(self, td_name):
        self.td_name = td_name
        self._key = AESGCM.generate_key(bit_length=256)
        self._aesgcm = AESGCM(self._key)
        self._encrypted_inputs = {}
        self._td_id = os.urandom(16).hex()

    def attest(self):
        """Simulate TDX attestation."""
        return {
            "td_id": self._td_id,
            "td_name": self.td_name,
            "measurement": os.urandom(32).hex(),
            "status": "VERIFIED",
            "code_hash": "route_optimizer_v2.1_sha256",
        }

    def submit_encrypted_data(self, airline_name, data_bytes):
        """Airline submits encrypted data to the TD."""
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, data_bytes, None)
        self._encrypted_inputs[airline_name] = {
            'nonce': nonce,
            'ciphertext': ciphertext,
            'size': len(data_bytes),
        }
        return len(ciphertext)

    def compute_aggregates(self):
        """
        Compute aggregated results INSIDE the TD.
        Individual data is decrypted only within the encrypted VM.
        Only aggregated results leave the TD.
        """
        # Decrypt all inputs inside TD (simulated)
        all_records = []
        for airline_name, encrypted in self._encrypted_inputs.items():
            plaintext = self._aesgcm.decrypt(
                encrypted['nonce'],
                encrypted['ciphertext'],
                None
            )
            records = json.loads(plaintext.decode('utf-8'))
            for record in records:
                record['_airline'] = airline_name
            all_records.append(records)

        # Compute aggregates (only these leave the TD)
        flat_records = [r for records in all_records for r in records]

        # Route-level aggregates (no individual airline data exposed)
        route_aggregates = {}
        for record in flat_records:
            route = record['route']
            parts = route.split('-')
            normalized = '-'.join(sorted(parts))

            if normalized not in route_aggregates:
                route_aggregates[normalized] = {
                    'num_airlines': set(),
                    'avg_fares': [],
                    'avg_loads': [],
                    'total_frequency': 0,
                    'total_passengers': 0,
                }

            route_aggregates[normalized]['num_airlines'].add(record['_airline'])
            route_aggregates[normalized]['avg_fares'].append(record['avg_fare_usd'])
            route_aggregates[normalized]['avg_loads'].append(record['load_factor'])
            route_aggregates[normalized]['total_frequency'] += record['weekly_frequency']
            route_aggregates[normalized]['total_passengers'] += record['avg_passengers']

        # Produce safe aggregated output
        safe_output = {}
        for route, data in route_aggregates.items():
            safe_output[route] = {
                'num_airlines_serving': len(data['num_airlines']),
                'market_avg_fare': round(np.mean(data['avg_fares']), 2),
                'market_avg_load': round(np.mean(data['avg_loads']), 3),
                'total_weekly_frequency': data['total_frequency'],
                'total_weekly_passengers': data['total_passengers'],
                # NOTE: No individual airline data exposed!
            }

        return safe_output


def load_airline_data():
    """Load all airline data files."""
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        print(f"  {RED}[FAIL] Data not found. Run 1_airline_data.py first.{RESET}")
        return None

    airlines = {}
    for filepath in sorted(data_dir.glob("*_routes.json")):
        name = filepath.stem.replace("_routes", "")
        name_map = {"skywings": "SkyWings", "euroconnect": "EuroConnect", "pacificstar": "PacificStar"}
        name = name_map.get(name, name)
        with open(filepath, 'r', encoding='utf-8') as f:
            airlines[name] = json.load(f)
    return airlines


def run_confidential_sharing():
    """Demonstrate TDX-protected data sharing."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 10: TDX-Protected Alliance Data Sharing
{'='*60}
{RESET}
  {CYAN}Scenario: Same route optimization, but using Intel TDX
  Trust Domains. Each airline's data remains encrypted.
  Only aggregated results are revealed.{RESET}
""")

    all_data = load_airline_data()
    if not all_data:
        return

    # Initialize TDX Trust Domain
    print(f"  {CYAN}[1/5] Initializing TDX Trust Domain...{RESET}")
    td = SimulatedTDXVM("Alliance Route Optimizer")
    print(f"    {GREEN}[OK]{RESET} Trust Domain created: {td._td_id[:16]}...")

    # Attestation
    print(f"\n  {CYAN}[2/5] Remote attestation...{RESET}")
    report = td.attest()
    print(f"    TD Name: {report['td_name']}")
    print(f"    Code: {report['code_hash']}")
    print(f"    Status: {GREEN}{report['status']}{RESET}")
    print(f"    {GREEN}[OK]{RESET} All airlines verify TD is running approved code")

    # Each airline submits encrypted data
    print(f"\n  {CYAN}[3/5] Airlines submit encrypted data to TD...{RESET}")
    for airline_name, records in all_data.items():
        data_bytes = json.dumps(records).encode('utf-8')
        encrypted_size = td.submit_encrypted_data(airline_name, data_bytes)
        print(f"    {GREEN}[OK]{RESET} {airline_name}: {len(data_bytes)} bytes -> "
              f"{encrypted_size} bytes (encrypted)")

    # Compute inside TD
    print(f"\n  {CYAN}[4/5] Computing aggregates inside Trust Domain...{RESET}")
    print(f"    (Data decrypted ONLY inside TD's encrypted memory)")
    results = td.compute_aggregates()
    print(f"    {GREEN}[OK]{RESET} Computation complete. {len(results)} route aggregates produced.")

    # Show results (only aggregates - no individual data)
    print(f"\n  {CYAN}[5/5] Aggregated results (safe to share):{RESET}")
    print(f"  {'='*55}")
    print(f"  {GREEN}{BOLD}ROUTE OPTIMIZATION RESULTS (Aggregated Only){RESET}")
    print(f"  {'='*55}")

    for route, data in sorted(results.items())[:8]:
        print(f"\n    Route: {route}")
        print(f"      Airlines serving:     {data['num_airlines_serving']}")
        print(f"      Market avg fare:      ${data['market_avg_fare']:.0f}")
        print(f"      Market avg load:      {data['market_avg_load']*100:.1f}%")
        print(f"      Total weekly freq:    {data['total_weekly_frequency']}")
        print(f"      Total weekly pax:     {data['total_weekly_passengers']}")

    # Comparison
    print(f"""

  {BOLD}{'='*55}{RESET}
  {GREEN}{BOLD}SECURITY COMPARISON{RESET}
  {BOLD}{'='*55}{RESET}

  {BOLD}What each airline can see:{RESET}
  ┌─────────────────────────────────────────────────────┐
  | Data Point          | Insecure     | TDX Protected  |
  |─────────────────────|──────────────|────────────────|
  | Partner's fares     | EXPOSED      | Hidden         |
  | Partner's margins   | EXPOSED      | Hidden         |
  | Partner's load      | EXPOSED      | Hidden         |
  | Partner's costs     | EXPOSED      | Hidden         |
  | Market averages     | Available    | Available      |
  | Route demand        | Available    | Available      |
  | Optimization result | Available    | Available      |
  └─────────────────────────────────────────────────────┘

  {BOLD}TDX Security Properties:{RESET}
  {GREEN}[OK]{RESET} Individual airline data never leaves encrypted TD
  {GREEN}[OK]{RESET} Even cloud provider cannot read TD memory
  {GREEN}[OK]{RESET} Attestation proves correct code is running
  {GREEN}[OK]{RESET} Only aggregated results are output
  {GREEN}[OK]{RESET} No airline can extract partner's raw data

  {BOLD}Business Outcome:{RESET}
  - Alliance can optimize routes collaboratively
  - No airline reveals competitive intelligence
  - Trust maintained between partners
  - Regulatory compliance (no data sharing violations)
  - Better outcomes than any airline could achieve alone

  {YELLOW}Note: This is a simulation. Real TDX requires Intel CPUs
  with TDX support (4th Gen Xeon Scalable or later).{RESET}
""")


if __name__ == "__main__":
    run_confidential_sharing()
