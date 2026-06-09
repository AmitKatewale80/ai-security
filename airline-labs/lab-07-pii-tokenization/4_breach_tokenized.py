#!/usr/bin/env python3
"""
Step 4: Breach of Tokenized System - Attacker Gets Nothing Useful

AIRLINE SCENARIO:
Same attacker, same breach. But now the fraud system only contains tokens.
The attacker sees meaningless random strings instead of real PII.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def simulate_tokenized_breach():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  BREACH SIMULATION: Tokenized System{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    data_file = 'models/loyalty_members_tokenized.json'
    if not os.path.exists(data_file):
        print(f"  {YELLOW}Run 3_tokenized_fraud_model.py first!{RESET}")
        return

    with open(data_file, 'r') as f:
        members = json.load(f)

    print(f"  {CYAN}[BREACH] Attacker gained access to fraud detection database{RESET}")
    print(f"  {CYAN}[BREACH] Dumping member records...{RESET}\n")

    print(f"  {BOLD}ATTACKER SEES:{RESET}\n")
    for i, member in enumerate(members[:10]):
        print(f"  Record #{i+1}:")
        print(f"    Name:        {GREEN}{member['name']}{RESET}")
        print(f"    Passport:    {GREEN}{member['passport']}{RESET}")
        print(f"    Credit Card: {GREEN}{member['credit_card']}{RESET}")
        print(f"    Email:       {GREEN}{member['email']}{RESET}")
        print(f"    Phone:       {GREEN}{member['phone']}{RESET}")
        print(f"    Miles:       {member['miles_balance']:,}")
        print()

    total = len(members)
    print(f"  {GREEN}{'─'*55}{RESET}")
    print(f"  {BOLD}{GREEN}  BREACH IMPACT (TOKENIZED SYSTEM):{RESET}")
    print(f"  {GREEN}{'─'*55}{RESET}")
    print(f"  {GREEN}  Total records accessed:     {total}{RESET}")
    print(f"  {GREEN}  Passport numbers stolen:    0 (only tokens){RESET}")
    print(f"  {GREEN}  Credit cards stolen:        0 (only tokens){RESET}")
    print(f"  {GREEN}  Emails stolen:              0 (only tokens){RESET}")
    print(f"  {GREEN}  Usable PII:                 ZERO{RESET}")
    print(f"  {GREEN}{'─'*55}{RESET}")
    print(f"  {GREEN}  GDPR Impact:   Minimal (no real PII exposed){RESET}")
    print(f"  {GREEN}  Identity Theft: Impossible (tokens are meaningless){RESET}")
    print(f"  {GREEN}{'─'*55}{RESET}")

    # Comparison
    print(f"\n  {BOLD}COMPARISON:{RESET}")
    print(f"  ┌──────────────────────┬────────────────────┬─────────────────────┐")
    print(f"  │                      │ {RED}Without Tokens{RESET}     │ {GREEN}With Tokens{RESET}         │")
    print(f"  ├──────────────────────┼────────────────────┼─────────────────────┤")
    print(f"  │ Passports exposed    │ {RED}{total}{RESET}              │ {GREEN}0{RESET}                   │")
    print(f"  │ Credit cards exposed │ {RED}{total}{RESET}              │ {GREEN}0{RESET}                   │")
    print(f"  │ Model accuracy       │ Same               │ Same                │")
    print(f"  │ GDPR fine risk       │ {RED}Up to 20M EUR{RESET}      │ {GREEN}Minimal{RESET}             │")
    print(f"  │ Identity theft risk  │ {RED}HIGH{RESET}               │ {GREEN}NONE{RESET}                │")
    print(f"  └──────────────────────┴────────────────────┴─────────────────────┘")

    print(f"\n  {GREEN}✅ DEFENSE SUCCESSFUL: Same model accuracy, zero PII exposure.{RESET}\n")


if __name__ == "__main__":
    simulate_tokenized_breach()
