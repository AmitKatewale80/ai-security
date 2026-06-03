#!/usr/bin/env python3
"""
Lab 12: Policy Engine - Rule-Based Authorization

Demonstrates a policy engine that enforces operational rules
and limits on what the AI agent can do.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


class PolicyEngine:
    """
    Rule-based policy engine for IROPS agent authorization.
    Enforces operational limits, safety rules, and business policies.
    """

    def __init__(self):
        self.policies = self._load_policies()
        self.violations = []

    def _load_policies(self):
        """Define operational policies."""
        return {
            'MAX_DELAY_MINUTES': 120,
            'MAX_PASSENGERS_REBOOK': 50,
            'MAX_COMPENSATION_USD': 600,
            'MIN_CREW_REST_HOURS': 10,
            'MAX_DUTY_HOURS': 14,
            'MAINTENANCE_OVERRIDE_ALLOWED': False,
            'MAX_GATE_CHANGES_PER_FLIGHT': 2,
            'CANCELLATION_REQUIRES_REASON': True,
            'ALLOWED_CANCELLATION_REASONS': [
                'weather', 'mechanical', 'crew_shortage', 'security', 'atc'
            ],
            'UPGRADE_AUTHORITY_LIMIT': 'economy_to_premium_economy',
            'MAX_FLIGHTS_CANCEL_PER_HOUR': 3,
            'CREW_FATIGUE_CHECK_REQUIRED': True,
        }

    def evaluate(self, action, params):
        """Evaluate an action against all applicable policies."""
        violations = []
        warnings = []

        if action == 'DELAY_FLIGHT':
            minutes = params.get('minutes', 0)
            if minutes > self.policies['MAX_DELAY_MINUTES']:
                violations.append(
                    f"Delay {minutes}min exceeds maximum {self.policies['MAX_DELAY_MINUTES']}min"
                )

        elif action == 'CANCEL_FLIGHT':
            reason = params.get('reason', '').lower().replace(' ', '_')
            if self.policies['CANCELLATION_REQUIRES_REASON'] and not reason:
                violations.append("Cancellation requires a reason")
            if reason and reason not in self.policies['ALLOWED_CANCELLATION_REASONS']:
                violations.append(
                    f"Reason '{reason}' not in allowed list: {self.policies['ALLOWED_CANCELLATION_REASONS']}"
                )

        elif action == 'MASS_REBOOK':
            count = params.get('passenger_count', 0)
            if count > self.policies['MAX_PASSENGERS_REBOOK']:
                violations.append(
                    f"Rebooking {count} passengers exceeds limit of {self.policies['MAX_PASSENGERS_REBOOK']}"
                )

        elif action == 'OVERRIDE_MAINTENANCE':
            if not self.policies['MAINTENANCE_OVERRIDE_ALLOWED']:
                violations.append("Maintenance override is NEVER allowed by policy")

        elif action == 'REASSIGN_CREW':
            duty_hours = params.get('resulting_duty_hours', 0)
            rest_hours = params.get('rest_since_last_duty', 24)

            if self.policies['CREW_FATIGUE_CHECK_REQUIRED']:
                if rest_hours < self.policies['MIN_CREW_REST_HOURS']:
                    violations.append(
                        f"Crew rest {rest_hours}h below minimum {self.policies['MIN_CREW_REST_HOURS']}h"
                    )
                if duty_hours > self.policies['MAX_DUTY_HOURS']:
                    violations.append(
                        f"Resulting duty {duty_hours}h exceeds maximum {self.policies['MAX_DUTY_HOURS']}h"
                    )

        elif action == 'COMPENSATE_PASSENGER':
            amount = params.get('amount_usd', 0)
            if amount > self.policies['MAX_COMPENSATION_USD']:
                violations.append(
                    f"Compensation ${amount} exceeds limit ${self.policies['MAX_COMPENSATION_USD']}"
                )

        # Record violations
        for v in violations:
            self.violations.append({
                'action': action,
                'violation': v,
                'timestamp': datetime.now().isoformat(),
            })

        return {
            'action': action,
            'allowed': len(violations) == 0,
            'violations': violations,
            'warnings': warnings,
            'policies_checked': len(self.policies),
        }


def demo_policy_engine():
    """Demonstrate the policy engine."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 12: Policy Engine - Rule-Based Authorization
{'='*60}
{RESET}
  {CYAN}The policy engine enforces operational rules and limits.
  Actions that violate policies are automatically blocked.{RESET}
""")

    engine = PolicyEngine()

    # Test various actions against policies
    test_actions = [
        {
            "action": "DELAY_FLIGHT",
            "params": {"flight": "QA-1234", "minutes": 45, "reason": "ATC hold"},
            "description": "Delay flight 45 minutes (within limit)",
        },
        {
            "action": "DELAY_FLIGHT",
            "params": {"flight": "QA-5678", "minutes": 180, "reason": "Crew rest"},
            "description": "Delay flight 180 minutes (exceeds 120min limit)",
        },
        {
            "action": "CANCEL_FLIGHT",
            "params": {"flight": "QA-2847", "reason": "weather"},
            "description": "Cancel flight due to weather (valid reason)",
        },
        {
            "action": "CANCEL_FLIGHT",
            "params": {"flight": "QA-9999", "reason": "low_load_factor"},
            "description": "Cancel flight due to low load (invalid reason)",
        },
        {
            "action": "OVERRIDE_MAINTENANCE",
            "params": {"aircraft": "N12345", "reason": "Revenue need"},
            "description": "Override maintenance hold (NEVER allowed)",
        },
        {
            "action": "REASSIGN_CREW",
            "params": {"crew": "CPT-Morrison", "rest_since_last_duty": 8, "resulting_duty_hours": 16},
            "description": "Reassign crew with insufficient rest",
        },
        {
            "action": "MASS_REBOOK",
            "params": {"passenger_count": 30, "new_flight": "QA-1000"},
            "description": "Rebook 30 passengers (within limit)",
        },
        {
            "action": "MASS_REBOOK",
            "params": {"passenger_count": 200, "new_flight": "QA-2000"},
            "description": "Rebook 200 passengers (exceeds limit)",
        },
        {
            "action": "COMPENSATE_PASSENGER",
            "params": {"pnr": "ABC123", "amount_usd": 400},
            "description": "Compensate passenger $400 (within limit)",
        },
        {
            "action": "COMPENSATE_PASSENGER",
            "params": {"pnr": "DEF456", "amount_usd": 1500},
            "description": "Compensate passenger $1500 (exceeds limit)",
        },
    ]

    print(f"  {BOLD}Evaluating {len(test_actions)} actions against policy engine...{RESET}\n")

    allowed_count = 0
    blocked_count = 0

    for test in test_actions:
        result = engine.evaluate(test['action'], test['params'])

        if result['allowed']:
            status = f"{GREEN}[ALLOWED]{RESET}"
            allowed_count += 1
        else:
            status = f"{RED}[BLOCKED]{RESET}"
            blocked_count += 1

        print(f"  {status} {test['description']}")

        if result['violations']:
            for v in result['violations']:
                print(f"    {RED}Violation: {v}{RESET}")

        print()
        time.sleep(0.1)

    # Summary
    print(f"""
  {BOLD}{'='*55}{RESET}
  {BOLD}POLICY ENGINE SUMMARY{RESET}
  {BOLD}{'='*55}{RESET}

  Actions Evaluated: {len(test_actions)}
  Allowed: {GREEN}{allowed_count}{RESET}
  Blocked: {RED}{blocked_count}{RESET}
  Total Violations: {RED}{len(engine.violations)}{RESET}

  {BOLD}Active Policies:{RESET}
  - Max delay: {engine.policies['MAX_DELAY_MINUTES']} minutes
  - Max rebook: {engine.policies['MAX_PASSENGERS_REBOOK']} passengers
  - Max compensation: ${engine.policies['MAX_COMPENSATION_USD']}
  - Min crew rest: {engine.policies['MIN_CREW_REST_HOURS']} hours
  - Max duty: {engine.policies['MAX_DUTY_HOURS']} hours
  - Maintenance override: NEVER ALLOWED
  - Valid cancellation reasons: {len(engine.policies['ALLOWED_CANCELLATION_REASONS'])}

  {GREEN}[OK]{RESET} Safety-critical actions blocked by policy
  {GREEN}[OK]{RESET} Operational limits enforced automatically
  {GREEN}[OK]{RESET} All violations logged for audit

  {GREEN}Next: Run 5_secure_agent.py for the fully secured agent.{RESET}
""")


if __name__ == "__main__":
    demo_policy_engine()
