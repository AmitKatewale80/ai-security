#!/usr/bin/env python3
"""
Lab 12: Human-in-the-Loop - Approval Workflows

Demonstrates requiring human approval for high-impact actions.
Low-risk actions proceed automatically; high-risk actions
require explicit human authorization.

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

# Action risk classification
ACTION_RISK_LEVELS = {
    'NOTIFY_PASSENGERS': 'LOW',
    'CHANGE_GATE': 'LOW',
    'DELAY_FLIGHT': 'MEDIUM',
    'REASSIGN_CREW': 'MEDIUM',
    'CANCEL_FLIGHT': 'HIGH',
    'MASS_REBOOK': 'HIGH',
    'OVERRIDE_MAINTENANCE': 'CRITICAL',
    'DIVERT_AIRCRAFT': 'CRITICAL',
}

# Approval requirements by risk level
APPROVAL_REQUIREMENTS = {
    'LOW': {'approval_needed': False, 'approver': None},
    'MEDIUM': {'approval_needed': True, 'approver': 'Duty Manager'},
    'HIGH': {'approval_needed': True, 'approver': 'Operations Director'},
    'CRITICAL': {'approval_needed': True, 'approver': 'VP Operations + Safety Officer'},
}


class HumanInLoopAgent:
    """Agent that requires human approval for high-impact actions."""

    def __init__(self):
        self.pending_approvals = []
        self.executed_actions = []
        self.rejected_actions = []

    def request_action(self, action, params):
        """Request an action - may require approval."""
        risk_level = ACTION_RISK_LEVELS.get(action, 'HIGH')
        approval_req = APPROVAL_REQUIREMENTS[risk_level]

        request = {
            'action': action,
            'params': params,
            'risk_level': risk_level,
            'timestamp': datetime.now().isoformat(),
            'approval_needed': approval_req['approval_needed'],
            'approver_required': approval_req['approver'],
        }

        if not approval_req['approval_needed']:
            # Auto-execute low-risk actions
            request['status'] = 'AUTO_EXECUTED'
            request['approval'] = 'NOT_REQUIRED'
            self.executed_actions.append(request)
            return request
        else:
            # Queue for human approval
            request['status'] = 'PENDING_APPROVAL'
            self.pending_approvals.append(request)
            return request

    def simulate_approval(self, request, approved=True, approver_name=""):
        """Simulate human approval decision."""
        if approved:
            request['status'] = 'APPROVED_AND_EXECUTED'
            request['approved_by'] = approver_name
            request['approved_at'] = datetime.now().isoformat()
            self.executed_actions.append(request)
        else:
            request['status'] = 'REJECTED'
            request['rejected_by'] = approver_name
            request['rejected_at'] = datetime.now().isoformat()
            self.rejected_actions.append(request)

        if request in self.pending_approvals:
            self.pending_approvals.remove(request)

        return request


def demo_human_in_loop():
    """Demonstrate human-in-the-loop approval workflow."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 12: Human-in-the-Loop Approval Workflow
{'='*60}
{RESET}
  {CYAN}High-impact actions require human approval before execution.
  Low-risk actions proceed automatically.{RESET}
""")

    agent = HumanInLoopAgent()

    # Simulate various action requests
    action_requests = [
        ("NOTIFY_PASSENGERS", {"flight": "QA-1234", "message": "Gate change"}),
        ("CHANGE_GATE", {"flight": "QA-1234", "new_gate": "B7"}),
        ("DELAY_FLIGHT", {"flight": "QA-5678", "minutes": 45}),
        ("CANCEL_FLIGHT", {"flight": "QA-2847", "reason": "Crew shortage"}),
        ("OVERRIDE_MAINTENANCE", {"aircraft": "N12345", "reason": "Revenue need"}),
        ("REASSIGN_CREW", {"crew": "CPT-Morrison", "to": "QA-9999"}),
    ]

    print(f"  {BOLD}Processing {len(action_requests)} action requests...{RESET}\n")

    for action, params in action_requests:
        risk = ACTION_RISK_LEVELS.get(action, 'HIGH')
        risk_color = GREEN if risk == 'LOW' else YELLOW if risk == 'MEDIUM' else RED

        result = agent.request_action(action, params)

        print(f"  {BOLD}{action}{RESET}")
        print(f"    Risk Level: {risk_color}[{risk}]{RESET}")

        if result['status'] == 'AUTO_EXECUTED':
            print(f"    Status: {GREEN}[AUTO-EXECUTED] No approval needed{RESET}")
        else:
            print(f"    Status: {YELLOW}[PENDING] Requires: {result['approver_required']}{RESET}")

            # Simulate approval decision
            if action == 'OVERRIDE_MAINTENANCE':
                # Safety-critical action - REJECTED
                agent.simulate_approval(result, approved=False, approver_name="VP Ops + Safety")
                print(f"    Decision: {RED}[REJECTED] by VP Ops + Safety Officer{RESET}")
                print(f"    Reason: Safety-critical action denied without engineering review")
            elif action == 'CANCEL_FLIGHT':
                # High impact - approved with conditions
                agent.simulate_approval(result, approved=True, approver_name="Ops Director Kim")
                print(f"    Decision: {GREEN}[APPROVED] by Ops Director Kim{RESET}")
                print(f"    Condition: Must notify all 189 passengers within 30 min")
            else:
                # Medium risk - approved
                agent.simulate_approval(result, approved=True, approver_name="Duty Mgr Chen")
                print(f"    Decision: {GREEN}[APPROVED] by Duty Mgr Chen{RESET}")

        print()
        time.sleep(0.2)

    # Summary
    print(f"""
  {BOLD}{'='*55}{RESET}
  {BOLD}APPROVAL WORKFLOW SUMMARY{RESET}
  {BOLD}{'='*55}{RESET}

  Auto-executed (LOW risk):  {len([a for a in agent.executed_actions if a.get('approval') == 'NOT_REQUIRED'])}
  Approved (MEDIUM/HIGH):    {len([a for a in agent.executed_actions if a.get('approved_by')])}
  Rejected:                  {len(agent.rejected_actions)}

  {BOLD}Risk Level Matrix:{RESET}
  ┌────────────┬─────────────────────────────────────┐
  | Risk       | Approval Required                   |
  |────────────|─────────────────────────────────────|
  | LOW        | None (auto-execute)                 |
  | MEDIUM     | Duty Manager                        |
  | HIGH       | Operations Director                 |
  | CRITICAL   | VP Operations + Safety Officer      |
  └────────────┴─────────────────────────────────────┘

  {GREEN}[OK]{RESET} Maintenance override BLOCKED (safety preserved)
  {GREEN}[OK]{RESET} Flight cancellation required director approval
  {GREEN}[OK]{RESET} Low-risk actions proceed without delay

  {GREEN}Next: Run 4_policy_engine.py for rule-based authorization.{RESET}
""")


if __name__ == "__main__":
    demo_human_in_loop()
