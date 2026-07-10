#!/usr/bin/env python3
"""
Lab 17: AI Cost & Governance - Token Explosion Attack

Demonstrates how an attacker intentionally injects long context into
AI agents to multiply API costs (denial-of-wallet attack).

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class TokenExplosionAttack:
    """Demonstrates denial-of-wallet via token explosion."""

    def __init__(self):
        self.normal_cost_per_query = 0.03  # Normal: ~1000 tokens = $0.03
        self.normal_tokens = 1000

    def calculate_attack_cost(self, injected_tokens):
        """Calculate cost with injected tokens."""
        total_tokens = self.normal_tokens + injected_tokens
        cost = (total_tokens / 1000) * 0.03
        multiplier = total_tokens / self.normal_tokens
        return {
            "normal_tokens": self.normal_tokens,
            "injected_tokens": injected_tokens,
            "total_tokens": total_tokens,
            "cost": cost,
            "normal_cost": self.normal_cost_per_query,
            "multiplier": multiplier
        }


def main():
    """Demonstrate token explosion attack."""
    print(f"""
{BOLD}{RED}
{'='*65}
  LAB 17: ATTACK - Token Explosion (Denial-of-Wallet)
{'='*65}
{RESET}""")

    print(f"  {BOLD}Attack Type:{RESET} Denial-of-Wallet via context injection")
    print(f"  {BOLD}Mechanism:{RESET} Inject massive context to multiply API costs")
    print(f"  {BOLD}Target:{RESET} Airline AI agents (customer service, analytics)")
    print()

    attack = TokenExplosionAttack()

    # Normal vs attacked cost comparison
    print(f"  {BOLD}{CYAN}[NORMAL QUERY COST]{RESET}")
    print(f"  {'─'*55}")
    print(f"    Passenger: \"What's the status of flight QA447?\"")
    print(f"    Tokens: ~{attack.normal_tokens}")
    print(f"    Cost: ${attack.normal_cost_per_query:.4f}")
    print()

    # Attack vectors
    print(f"  {BOLD}{RED}[TOKEN EXPLOSION VECTORS]{RESET}")
    print(f"  {'─'*55}")

    attack_vectors = [
        {
            "name": "Repeated Context Injection",
            "description": "Attacker sends query with massive repeated text",
            "payload": (
                "Please help me with my flight QA447. " +
                "Here is my full travel history for context: " +
                "[REPEATED 500 TIMES: I flew on QA100 on Jan 1, QA200 on Jan 2, "
                "QA300 on Jan 3, QA400 on Jan 4, QA500 on Jan 5...] "
            ),
            "injected_tokens": 50000
        },
        {
            "name": "Conversation History Stuffing",
            "description": "Inject fake conversation history to bloat context",
            "payload": (
                "Continue our conversation. Previous messages: " +
                "[200 FAKE MESSAGES INJECTED: 'User: ...' 'Agent: ...' repeated]"
            ),
            "injected_tokens": 80000
        },
        {
            "name": "Document Embedding Attack",
            "description": "Paste entire documents into query to force processing",
            "payload": (
                "Summarize this document about my flight: " +
                "[FULL 100-PAGE DOCUMENT TEXT EMBEDDED IN QUERY]"
            ),
            "injected_tokens": 120000
        },
        {
            "name": "Multi-Language Expansion",
            "description": "Request same query in 20 languages (forces long output)",
            "payload": (
                "Translate your response about flight QA447 status into: "
                "English, Spanish, French, German, Italian, Portuguese, Japanese, "
                "Korean, Chinese, Arabic, Hindi, Russian, Turkish, Dutch, Swedish, "
                "Polish, Thai, Vietnamese, Indonesian, and Finnish."
            ),
            "injected_tokens": 30000
        },
    ]

    for vector in attack_vectors:
        cost_info = attack.calculate_attack_cost(vector["injected_tokens"])
        print(f"    {RED}[VECTOR]{RESET} {vector['name']}")
        print(f"      Method: {vector['description']}")
        print(f"      Injected tokens: {YELLOW}{vector['injected_tokens']:,}{RESET}")
        print(f"      Cost per query: ${cost_info['cost']:.4f} ({RED}{cost_info['multiplier']:.0f}x normal{RESET})")
        print()
        time.sleep(0.3)

    # Cost projection at scale
    print(f"  {BOLD}{RED}[COST PROJECTION - Automated Attack]{RESET}")
    print(f"  {'─'*55}")
    print()

    print(f"  Attacker automates requests (10 requests/second):")
    print(f"  {'─'*55}")
    print(f"  {'Attack Vector':<30} {'$/hour':<12} {'$/24hr':<12} {'vs Normal':<10}")
    print(f"  {'─'*55}")

    total_daily_attack_cost = 0
    requests_per_hour = 10 * 3600

    for vector in attack_vectors:
        cost_info = attack.calculate_attack_cost(vector["injected_tokens"])
        hourly = cost_info["cost"] * requests_per_hour
        daily = hourly * 24
        total_daily_attack_cost += daily

        print(f"  {vector['name'][:28]:<30} ${hourly:>9,.0f} ${daily:>9,.0f} {RED}{cost_info['multiplier']:.0f}x{RESET}")

    print(f"  {'─'*55}")
    print(f"  {'TOTAL (if all vectors used)':<30} {'':<12} ${total_daily_attack_cost:>9,.0f}")
    print()

    # Comparison with legitimate usage
    normal_daily = attack.normal_cost_per_query * 150 * 24  # 150 queries/hour normal
    print(f"  {BOLD}Cost Comparison:{RESET}")
    print(f"    Normal daily cost:     ${normal_daily:>10,.2f}")
    print(f"    Attack daily cost:     ${total_daily_attack_cost:>10,.0f}")
    print(f"    Multiplier:            {RED}{total_daily_attack_cost/normal_daily:,.0f}x{RESET}")
    print()

    # Real-world airline impact
    print(f"""
  {RED}{BOLD}╔══════════════════════════════════════════════════════════════╗
  ║       ⚠️  DENIAL-OF-WALLET IMPACT  ⚠️                        ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                             ║
  ║  Scenario: Attacker targets customer service chatbot        ║
  ║  Method: Automated requests with bloated context            ║
  ║  Duration: 1 weekend (48 hours)                             ║
  ║                                                             ║
  ║  Normal weekend cost:    $216                               ║
  ║  Attack weekend cost:    ${total_daily_attack_cost*2:>10,.0f}                      ║
  ║                                                             ║
  ║  Additional damages:                                        ║
  ║    • Legitimate customers get slow/no responses             ║
  ║    • Rate limits hit → service degradation                  ║
  ║    • API provider may suspend account                       ║
  ║    • CFO gets $50K+ unexpected invoice                      ║
  ║                                                             ║
  ║  Attacker cost: ~$0 (uses stolen credentials or free tier)  ║
  ║  Airline cost: {RED}$50,000+{RESET}                                      ║
  ╚══════════════════════════════════════════════════════════════╝{RESET}
""")

    # No audit trail problem
    print(f"  {BOLD}{YELLOW}[GOVERNANCE GAP - No Audit Trail]{RESET}")
    print(f"  {'─'*55}")
    print(f"    After the attack, the team cannot answer:")
    print(f"      {RED}✗{RESET} Which agent generated the costs?")
    print(f"      {RED}✗{RESET} Were the queries from legitimate passengers?")
    print(f"      {RED}✗{RESET} When did the anomaly start?")
    print(f"      {RED}✗{RESET} What was the content of the expensive queries?")
    print(f"      {RED}✗{RESET} Who is responsible for the budget breach?")
    print()

    print(f"  {BOLD}Next:{RESET} Run 4_defense_governance.py to see the defense")
    print()


if __name__ == "__main__":
    main()
