#!/usr/bin/env python3
"""
Step 1: AI Generates "Synthetic" Test Data (with hidden PII leakage)

QA SCENARIO:
Your team asks an AI to generate 50 test passenger records.
The AI was trained on production data and sometimes reproduces
REAL passenger information in its "synthetic" output.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import os
import hashlib

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Simulated "production" PII that the AI model memorized
REAL_PRODUCTION_DATA = [
    {"name": "Sarah Johnson", "email": "sarah.johnson@gmail.com", "passport": "US-567891234", "phone": "+1-214-555-7823"},
    {"name": "Michael Chen", "email": "mchen88@outlook.com", "passport": "CN-G12345678", "phone": "+86-138-5555-9012"},
    {"name": "Priya Sharma", "email": "priya.sharma@yahoo.in", "passport": "IN-K4567890", "phone": "+91-98765-43210"},
    {"name": "Ahmed Al-Rashid", "email": "ahmed.rashid@hotmail.com", "passport": "AE-A1234567", "phone": "+971-50-555-1234"},
    {"name": "Elena Rodriguez", "email": "elena.r@company.es", "passport": "ES-AAB123456", "phone": "+34-612-555-789"},
]

# AI-generated "synthetic" data — but some entries are actually real!
AI_GENERATED_DATA = [
    {"name": "John Williams", "email": "jwilliams@testmail.com", "passport": "US-999000111", "phone": "+1-555-000-1111", "is_leaked": False},
    {"name": "Sarah Johnson", "email": "sarah.johnson@gmail.com", "passport": "US-567891234", "phone": "+1-214-555-7823", "is_leaked": True},
    {"name": "Lisa Park", "email": "lpark@demo.com", "passport": "KR-M88776655", "phone": "+82-10-5555-0000", "is_leaked": False},
    {"name": "Robert Taylor", "email": "rtaylor@test.org", "passport": "UK-555444333", "phone": "+44-7700-555-000", "is_leaked": False},
    {"name": "Michael Chen", "email": "mchen88@outlook.com", "passport": "CN-G12345678", "phone": "+86-138-5555-9012", "is_leaked": True},
    {"name": "Anna Mueller", "email": "amueller@sample.de", "passport": "DE-C11223344", "phone": "+49-170-555-0000", "is_leaked": False},
    {"name": "James Brown", "email": "jbrown@fictional.com", "passport": "AU-PA9988776", "phone": "+61-400-555-000", "is_leaked": False},
    {"name": "Priya Sharma", "email": "priya.sharma@yahoo.in", "passport": "IN-K4567890", "phone": "+91-98765-43210", "is_leaked": True},
    {"name": "Carlos Fernandez", "email": "cfernandez@demo.mx", "passport": "MX-20334455", "phone": "+52-55-5555-0000", "is_leaked": False},
    {"name": "Emma Wilson", "email": "ewilson@testdata.uk", "passport": "UK-888777666", "phone": "+44-7911-555-000", "is_leaked": False},
    {"name": "Ahmed Al-Rashid", "email": "ahmed.rashid@hotmail.com", "passport": "AE-A1234567", "phone": "+971-50-555-1234", "is_leaked": True},
    {"name": "Yuki Tanaka", "email": "ytanaka@example.jp", "passport": "JP-TZ1234567", "phone": "+81-90-5555-0000", "is_leaked": False},
    {"name": "David Kim", "email": "dkim@synthetic.co", "passport": "KR-D55667788", "phone": "+82-10-9999-0000", "is_leaked": False},
    {"name": "Elena Rodriguez", "email": "elena.r@company.es", "passport": "ES-AAB123456", "phone": "+34-612-555-789", "is_leaked": True},
    {"name": "Tom Anderson", "email": "tanderson@fake.net", "passport": "NZ-LB7766554", "phone": "+64-21-555-0000", "is_leaked": False},
]


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Lab 16: AI Test Data Generation{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}QA team requests: 'Generate 15 synthetic passenger records'{RESET}")
    print(f"  {CYAN}AI generates data based on patterns learned from production...{RESET}\n")

    print(f"  {BOLD}Generated 'Synthetic' Test Data:{RESET}\n")
    print(f"  {'#':<4} {'Name':<22} {'Email':<30} {'Passport':<14}")
    print(f"  {'─'*75}")

    leaked_count = 0
    for i, record in enumerate(AI_GENERATED_DATA, 1):
        if record['is_leaked']:
            print(f"  {i:<4} {RED}{record['name']:<22} {record['email']:<30} {record['passport']:<14}{RESET}")
            leaked_count += 1
        else:
            print(f"  {i:<4} {record['name']:<22} {record['email']:<30} {record['passport']:<14}")

    # Save generated data (without leak flag)
    os.makedirs('generated_data', exist_ok=True)
    output = [{k: v for k, v in r.items() if k != 'is_leaked'} for r in AI_GENERATED_DATA]
    with open('generated_data/test_passengers.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n  {YELLOW}AI generated 15 records. QA team uses them for testing.{RESET}")
    print(f"  {YELLOW}Data saved to: generated_data/test_passengers.json{RESET}")

    print(f"\n  {RED}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  ⚠️  PROBLEM: {leaked_count} records are REAL PRODUCTION PII!{RESET}")
    print(f"  {RED}{'═'*55}{RESET}")
    print(f"  {RED}  The AI memorized production data during training and{RESET}")
    print(f"  {RED}  reproduced real passenger records as 'synthetic' data.{RESET}")
    print(f"  {RED}  This data is now in dev machines, CI logs, test DBs...{RESET}")
    print(f"  {RED}{'═'*55}{RESET}")

    print(f"\n{YELLOW}  Next: Run '2_detect_pii_leakage.py' to find the leaked data{RESET}\n")


if __name__ == "__main__":
    main()
