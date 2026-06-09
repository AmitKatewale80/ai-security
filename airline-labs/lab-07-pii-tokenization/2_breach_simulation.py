#!/usr/bin/env python3
"""
Step 2: Breach Simulation - Attacker Accesses Raw PII

AIRLINE SCENARIO:
An attacker gains access to the fraud detection system's data store.
They can see ALL member PII in plaintext.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import os

RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def simulate_breach():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 BREACH SIMULATION: Attacker Accesses Fraud System{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    data_file = 'models/loyalty_members_raw.json'
    if not os.path.exists(data_file):
        print(f"  {YELLOW}Run 1_loyalty_fraud_model.py first!{RESET}")
        return

    with open(data_file, 'r') as f:
        members = json.load(f)

    print(f"  {RED}[BREACH] Attacker gained access to fraud detection database{RESET}")
    print(f"  {RED}[BREACH] Dumping member records...{RESET}\n")

    # Show stolen data
    stolen_passports = []
    stolen_cards = []
    stolen_emails = []

    print(f"  {BOLD}STOLEN DATA DUMP:{RESET}\n")
    for i, member in enumerate(members[:10]):
        print(f"  Record #{i+1}:")
        print(f"    Name:        {member['name']}")
        print(f"    Passport:    {RED}{member['passport']}{RESET}")
        print(f"    Credit Card: {RED}{member['credit_card']}{RESET}")
        print(f"    Email:       {RED}{member['email']}{RESET}")
        print(f"    Phone:       {RED}{member['phone']}{RESET}")
        print(f"    Miles:       {member['miles_balance']:,}")
        print()

        stolen_passports.append(member['passport'])
        stolen_cards.append(member['credit_card'])
        stolen_emails.append(member['email'])

    total = len(members)
    print(f"  {RED}{'─'*55}{RESET}")
    print(f"  {BOLD}{RED}  BREACH IMPACT SUMMARY:{RESET}")
    print(f"  {RED}{'─'*55}{RESET}")
    print(f"  {RED}  Total records stolen:     {total}{RESET}")
    print(f"  {RED}  Passport numbers:         {total} (identity theft){RESET}")
    print(f"  {RED}  Credit card numbers:      {total} (financial fraud){RESET}")
    print(f"  {RED}  Email addresses:          {total} (phishing attacks){RESET}")
    print(f"  {RED}  Phone numbers:            {total} (SIM swap attacks){RESET}")
    print(f"  {RED}{'─'*55}{RESET}")
    print(f"  {RED}  GDPR Fine:  Up to 20M EUR or 4% global revenue{RESET}")
    print(f"  {RED}  PCI-DSS:    Non-compliance, card scheme fines{RESET}")
    print(f"  {RED}{'─'*55}{RESET}")

    print(f"\n  {YELLOW}Next: Run '3_tokenized_fraud_model.py' to see the DEFENSE{RESET}\n")


if __name__ == "__main__":
    simulate_breach()
