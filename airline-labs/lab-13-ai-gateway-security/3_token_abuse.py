#!/usr/bin/env python3
"""
Step 3: Token Abuse — Excessive Usage & Credential Misuse

Shows how stolen/leaked tokens can be abused for:
- Unlimited queries (no rate limiting)
- Cost explosion (token billing abuse)
- Data exfiltration via high-volume queries

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 Token Abuse — Stolen API Token Attack{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Simulate token abuse
    stolen_token = "tok_analyst_007"
    print(f"  {CYAN}Attacker obtained leaked token: {stolen_token}{RESET}")
    print(f"  {CYAN}Token found in: exposed .env file in public Git repo{RESET}\n")

    print(f"  {BOLD}Abuse Scenarios:{RESET}\n")

    abuses = [
        {
            'type': 'Volume Abuse',
            'queries': 50000,
            'cost': '$2,500',
            'impact': 'Attacker runs 50K queries in 1 hour, extracting full pricing model',
            'normal_usage': '100 queries/day',
        },
        {
            'type': 'Cost Explosion',
            'queries': 200000,
            'cost': '$15,000',
            'impact': 'Attacker sends expensive long-context prompts to maximize billing',
            'normal_usage': '$50/day budget',
        },
        {
            'type': 'Data Exfiltration',
            'queries': 10000,
            'cost': '$500',
            'impact': 'Systematic probing extracts training data patterns (model inversion)',
            'normal_usage': 'Read-only analytics queries',
        },
    ]

    total_cost = 0
    for i, abuse in enumerate(abuses, 1):
        print(f"  {RED}Abuse #{i}: {abuse['type']}{RESET}")
        print(f"    Queries sent:  {abuse['queries']:,}")
        print(f"    Cost incurred: {abuse['cost']}")
        print(f"    Normal usage:  {abuse['normal_usage']}")
        print(f"    Impact: {abuse['impact']}")
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  TOKEN ABUSE IMPACT:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Total unauthorized queries:  260,000")
    print(f"    Total unauthorized cost:     {RED}$18,000+{RESET}")
    print(f"    Data extracted:              Pricing model + training patterns")
    print(f"    Detection time (no defense): {RED}Days to weeks{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n{YELLOW}  Next: Run '4_defense_gateway.py' for defense{RESET}\n")


if __name__ == "__main__":
    main()
