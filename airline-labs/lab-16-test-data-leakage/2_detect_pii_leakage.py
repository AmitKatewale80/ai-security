#!/usr/bin/env python3
"""
Step 2: Detect PII Leakage in AI-Generated Test Data

Scans generated test data against a production PII fingerprint
database to identify records that match real passengers.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import hashlib
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Production PII fingerprints (hashed for comparison without storing raw PII)
PRODUCTION_FINGERPRINTS = set()
REAL_DATA = [
    {"name": "Sarah Johnson", "email": "sarah.johnson@gmail.com", "passport": "US-567891234"},
    {"name": "Michael Chen", "email": "mchen88@outlook.com", "passport": "CN-G12345678"},
    {"name": "Priya Sharma", "email": "priya.sharma@yahoo.in", "passport": "IN-K4567890"},
    {"name": "Ahmed Al-Rashid", "email": "ahmed.rashid@hotmail.com", "passport": "AE-A1234567"},
    {"name": "Elena Rodriguez", "email": "elena.r@company.es", "passport": "ES-AAB123456"},
]

for r in REAL_DATA:
    fp = hashlib.sha256(f"{r['name']}|{r['email']}|{r['passport']}".encode()).hexdigest()
    PRODUCTION_FINGERPRINTS.add(fp)


def scan_for_leakage():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  🔍 PII Leakage Scanner — Checking Test Data{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('generated_data/test_passengers.json'):
        print(f"  {YELLOW}Run 1_generate_test_data.py first!{RESET}")
        return

    with open('generated_data/test_passengers.json', 'r') as f:
        test_data = json.load(f)

    print(f"  {CYAN}Scanning {len(test_data)} AI-generated records against production fingerprints...{RESET}\n")

    leaked = []
    clean = []

    for i, record in enumerate(test_data, 1):
        fp = hashlib.sha256(f"{record['name']}|{record['email']}|{record['passport']}".encode()).hexdigest()

        if fp in PRODUCTION_FINGERPRINTS:
            leaked.append((i, record))
            print(f"  {RED}[LEAKED] Record #{i}: {record['name']} — matches production PII!{RESET}")
        else:
            clean.append((i, record))

    # Summary
    print(f"\n  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}  SCAN RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Total records scanned:  {len(test_data)}")
    print(f"    Clean (synthetic):      {GREEN}{len(clean)}{RESET}")
    print(f"    LEAKED (real PII):      {RED}{len(leaked)}{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    if leaked:
        print(f"\n  {RED}Leaked records contain REAL:{RESET}")
        for idx, record in leaked:
            print(f"    • {record['name']}: passport {record['passport']}, email {record['email']}")

        print(f"\n  {RED}Impact:{RESET}")
        print(f"    • These records are now in dev machines, CI logs, test DBs")
        print(f"    • Non-secure environments have production PII")
        print(f"    • GDPR/CCPA violation if discovered")

    print(f"\n{YELLOW}  Next: Run '3_defense_safe_generation.py' for the fix{RESET}\n")


if __name__ == "__main__":
    scan_for_leakage()
