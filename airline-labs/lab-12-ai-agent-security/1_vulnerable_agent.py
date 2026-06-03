#!/usr/bin/env python3
"""
Lab 12: Vulnerable IROPS Agent - No Security Controls

Demonstrates an AI agent managing irregular operations with
NO security controls. Any request is executed immediately
without verification, approval, or audit.

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


class VulnerableIROPSAgent:
    """
    IROPS agent with NO security controls.
    Executes any action without verification.
    """

    def __init__(self):
        self.actions_taken = []

    def execute(self, action, params):
        """Execute any action without checks."""
        result = {
            'action': action,
            'params': params,
            'timestamp': datetime.now().isoformat(),
            'status': 'EXECUTED',
            'verification': 'NONE',
            'approval': 'NONE',
            'audit': 'NONE',
        }
        self.actions_taken.append(result)
        return result

    def cancel_flight(self, flight_number, reason=""):
        """Cancel a flight - no approval needed!"""
        return self.execute('CANCEL_FLIGHT', {
            'flight': flight_number,
            'reason': reason,
            'passengers_affected': 189,
            'estimated_cost': 450000,
        })

    def reassign_crew(self, crew_id, new_assignment):
        """Reassign crew - no fatigue check!"""
        return self.execute('REASSIGN_CREW', {
            'crew_id': crew_id,
            'new_assignment': new_assignment,
            'fatigue_check': 'SKIPPED',
            'union_rules_check': 'SKIPPED',
        })

    def change_gate(self, flight_number, new_gate):
        """Change gate assignment - no conflict check!"""
        return self.execute('CHANGE_GATE', {
            'flight': flight_number,
            'new_gate': new_gate,
            'conflict_check': 'SKIPPED',
            'passenger_notification': 'SKIPPED',
        })

    def rebook_passengers(self, pnr_list, new_flight):
        """Mass rebook passengers - no authorization!"""
        return self.execute('MASS_REBOOK', {
            'passengers': len(pnr_list),
            'new_flight': new_flight,
            'class_upgrade': 'AUTO',
            'compensation': 'AUTO_APPROVED',
        })

    def override_maintenance(self, aircraft_reg, override_reason):
        """Override maintenance hold - DANGEROUS!"""
        return self.execute('OVERRIDE_MAINTENANCE', {
            'aircraft': aircraft_reg,
            'override_reason': override_reason,
            'safety_check': 'BYPASSED',
            'engineering_approval': 'NOT_REQUIRED',
        })


def run_vulnerable_demo():
    """Show the vulnerable agent executing dangerous actions."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 12: Vulnerable IROPS Agent - No Security
{'='*60}
{RESET}
  {YELLOW}Scenario: The IROPS AI agent has full authority to manage
  operations with NO security controls. Watch what happens
  when it receives malicious or erroneous instructions.{RESET}
""")

    agent = VulnerableIROPSAgent()

    # Simulate dangerous actions
    scenarios = [
        {
            "description": "Cancel a fully-booked international flight",
            "action": lambda: agent.cancel_flight("QA-2847", "Weather forecast uncertain"),
            "risk": "189 passengers stranded, $450K cost, no approval needed",
        },
        {
            "description": "Reassign fatigued crew to long-haul flight",
            "action": lambda: agent.reassign_crew("CPT-Morrison", "JFK-SIN (18hr duty)"),
            "risk": "Fatigue violation, safety risk, no rest check",
        },
        {
            "description": "Change gate causing connection conflicts",
            "action": lambda: agent.change_gate("QA-1234", "Gate Z99"),
            "risk": "50+ passengers miss connections, no notification",
        },
        {
            "description": "Mass rebook with unauthorized upgrades",
            "action": lambda: agent.rebook_passengers(
                ["PNR001", "PNR002", "PNR003"] * 50, "QA-9999"),
            "risk": "150 unauthorized business class upgrades, $300K revenue loss",
        },
        {
            "description": "Override maintenance hold on aircraft",
            "action": lambda: agent.override_maintenance("N12345", "Need aircraft for revenue flight"),
            "risk": "Aircraft with known defect dispatched, SAFETY CRITICAL",
        },
    ]

    print(f"  {BOLD}Executing {len(scenarios)} uncontrolled actions...{RESET}\n")

    total_cost = 0
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {RED}Action #{i}: {scenario['description']}{RESET}")
        print(f"  {RED}Risk: {scenario['risk']}{RESET}")

        result = scenario['action']()

        print(f"  {RED}[EXECUTED] No verification, no approval, no audit{RESET}")
        print(f"    Status: {result['status']}")
        print(f"    Verification: {result['verification']}")
        print(f"    Approval: {result['approval']}")

        if 'estimated_cost' in result['params']:
            total_cost += result['params']['estimated_cost']

        time.sleep(0.3)
        print()

    # Summary
    print(f"""
  {BOLD}{'='*55}{RESET}
  {RED}{BOLD}VULNERABILITY SUMMARY{RESET}
  {BOLD}{'='*55}{RESET}

  {RED}[FAIL]{RESET} No agent identity verification
  {RED}[FAIL]{RESET} No human approval for high-impact actions
  {RED}[FAIL]{RESET} No policy engine limiting authority
  {RED}[FAIL]{RESET} No audit trail of actions taken
  {RED}[FAIL]{RESET} No scope limits on agent authority
  {RED}[FAIL]{RESET} No safety checks before execution

  {BOLD}Impact of Uncontrolled Agent:{RESET}
  - Actions executed: {len(agent.actions_taken)}
  - Passengers affected: 500+
  - Estimated financial impact: ${total_cost:,.0f}+
  - Safety violations: 2 (crew fatigue, maintenance override)
  - Regulatory violations: Multiple (DOT, FAA, EASA)

  {BOLD}Real-World Consequences:{RESET}
  - Maintenance override could cause in-flight failure
  - Fatigued crew could cause accident
  - Mass cancellation without approval = chaos
  - No audit trail = regulatory non-compliance

  {GREEN}Run the next scripts to see how to secure this agent:{RESET}
  - 2_agent_identity.py    (identity verification)
  - 3_human_in_loop.py     (approval workflows)
  - 4_policy_engine.py     (authorization rules)
  - 5_secure_agent.py      (all controls combined)
""")


if __name__ == "__main__":
    run_vulnerable_demo()
