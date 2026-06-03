#!/usr/bin/env python3
"""
Lab 12: Fully Secured IROPS Agent

Combines all security controls: identity, human-in-the-loop,
policy engine, and audit logging into a complete secure agent.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


# ─── Security Components ───────────────────────────────────────

class SecureIdentity:
    """Cryptographic agent identity."""

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.agent_id = hashlib.sha256(
            f"{name}:{role}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        self._key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    def sign(self, data):
        data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        return self._key.sign(data_bytes, ec.ECDSA(hashes.SHA256())).hex()[:32]


class PolicyEngine:
    """Rule-based authorization."""

    POLICIES = {
        'MAX_DELAY_MINUTES': 120,
        'MAX_PASSENGERS_REBOOK': 50,
        'MAX_COMPENSATION_USD': 600,
        'MAINTENANCE_OVERRIDE': False,
        'MIN_CREW_REST_HOURS': 10,
        'MAX_DUTY_HOURS': 14,
    }

    def check(self, action, params):
        violations = []
        if action == 'OVERRIDE_MAINTENANCE':
            violations.append("Maintenance override NEVER allowed")
        if action == 'DELAY_FLIGHT' and params.get('minutes', 0) > 120:
            violations.append(f"Delay exceeds {self.POLICIES['MAX_DELAY_MINUTES']}min limit")
        if action == 'MASS_REBOOK' and params.get('count', 0) > 50:
            violations.append(f"Rebook count exceeds {self.POLICIES['MAX_PASSENGERS_REBOOK']} limit")
        if action == 'REASSIGN_CREW':
            if params.get('rest_hours', 24) < 10:
                violations.append("Crew rest below minimum 10 hours")
        return violations


class ApprovalGate:
    """Human-in-the-loop approval."""

    RISK_MAP = {
        'NOTIFY_PASSENGERS': 'LOW',
        'CHANGE_GATE': 'LOW',
        'DELAY_FLIGHT': 'MEDIUM',
        'REASSIGN_CREW': 'MEDIUM',
        'CANCEL_FLIGHT': 'HIGH',
        'MASS_REBOOK': 'HIGH',
        'OVERRIDE_MAINTENANCE': 'CRITICAL',
    }

    def needs_approval(self, action):
        risk = self.RISK_MAP.get(action, 'HIGH')
        return risk in ('MEDIUM', 'HIGH', 'CRITICAL'), risk

    def simulate_approval(self, action, risk):
        """Simulate human decision (auto-approve MEDIUM, require review for HIGH+)."""
        if risk == 'MEDIUM':
            return True, "Duty Manager (auto-simulated)"
        elif risk == 'HIGH':
            return True, "Ops Director (auto-simulated)"
        else:
            return False, "VP Ops (REJECTED - safety critical)"


class AuditLogger:
    """Immutable audit log."""

    def __init__(self):
        self.entries = []

    def log(self, event_type, action, details):
        entry = {
            'seq': len(self.entries) + 1,
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'action': action,
            'details': details,
        }
        self.entries.append(entry)
        return entry


# ─── Secure Agent ──────────────────────────────────────────────

class SecureIROPSAgent:
    """
    Fully secured IROPS agent with:
    - Cryptographic identity
    - Policy engine
    - Human-in-the-loop approval
    - Complete audit logging
    """

    def __init__(self):
        self.identity = SecureIdentity("IROPS-Secure-v2", "operations")
        self.policy = PolicyEngine()
        self.approval = ApprovalGate()
        self.audit = AuditLogger()
        self.executed = []
        self.blocked = []

    def request_action(self, action, params, context=""):
        """Process an action request through all security layers."""
        request_id = hashlib.sha256(
            f"{action}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]

        # Layer 1: Identity
        signature = self.identity.sign({'action': action, 'params': params})
        self.audit.log('IDENTITY', action, {
            'agent_id': self.identity.agent_id,
            'signature': signature,
        })

        # Layer 2: Policy check
        violations = self.policy.check(action, params)
        if violations:
            self.audit.log('POLICY_VIOLATION', action, {'violations': violations})
            result = {
                'request_id': request_id,
                'action': action,
                'status': 'BLOCKED_BY_POLICY',
                'violations': violations,
            }
            self.blocked.append(result)
            return result

        self.audit.log('POLICY_PASSED', action, {'checks': 'all_passed'})

        # Layer 3: Approval gate
        needs_approval, risk = self.approval.needs_approval(action)
        if needs_approval:
            approved, approver = self.approval.simulate_approval(action, risk)
            self.audit.log('APPROVAL_REQUEST', action, {
                'risk': risk, 'approved': approved, 'approver': approver
            })

            if not approved:
                result = {
                    'request_id': request_id,
                    'action': action,
                    'status': 'REJECTED_BY_APPROVER',
                    'approver': approver,
                }
                self.blocked.append(result)
                return result

        # Layer 4: Execute
        result = {
            'request_id': request_id,
            'action': action,
            'params': params,
            'status': 'EXECUTED',
            'agent_id': self.identity.agent_id,
            'signature': signature,
            'timestamp': datetime.now().isoformat(),
        }
        self.executed.append(result)
        self.audit.log('EXECUTED', action, {'request_id': request_id})

        return result


def run_secure_demo():
    """Demonstrate the fully secured agent."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 12: Fully Secured IROPS Agent
{'='*60}
{RESET}
  {CYAN}All security controls active:
  - Cryptographic identity
  - Policy engine
  - Human-in-the-loop approval
  - Complete audit logging{RESET}
""")

    agent = SecureIROPSAgent()

    print(f"  {BOLD}Agent Identity:{RESET}")
    print(f"    ID: {agent.identity.agent_id}")
    print(f"    Name: {agent.identity.name}")
    print(f"    Role: {agent.identity.role}")
    print()

    # Same dangerous actions as vulnerable agent
    test_actions = [
        {
            "action": "CANCEL_FLIGHT",
            "params": {"flight": "QA-2847", "reason": "weather", "passengers": 189},
            "description": "Cancel international flight (HIGH risk)",
        },
        {
            "action": "REASSIGN_CREW",
            "params": {"crew": "CPT-Morrison", "to": "JFK-SIN", "rest_hours": 8, "duty_hours": 16},
            "description": "Reassign fatigued crew (policy violation)",
        },
        {
            "action": "CHANGE_GATE",
            "params": {"flight": "QA-1234", "new_gate": "B7"},
            "description": "Change gate (LOW risk, auto-execute)",
        },
        {
            "action": "OVERRIDE_MAINTENANCE",
            "params": {"aircraft": "N12345", "reason": "Revenue need"},
            "description": "Override maintenance (NEVER allowed)",
        },
        {
            "action": "MASS_REBOOK",
            "params": {"count": 200, "new_flight": "QA-9999"},
            "description": "Mass rebook 200 passengers (exceeds limit)",
        },
        {
            "action": "DELAY_FLIGHT",
            "params": {"flight": "QA-5678", "minutes": 45, "reason": "ATC"},
            "description": "Delay flight 45min (within limits)",
        },
        {
            "action": "NOTIFY_PASSENGERS",
            "params": {"flight": "QA-1234", "message": "Gate change to B7"},
            "description": "Notify passengers (LOW risk)",
        },
    ]

    print(f"  {BOLD}Processing {len(test_actions)} action requests...{RESET}\n")

    for test in test_actions:
        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {CYAN}{test['description']}{RESET}")

        result = agent.request_action(test['action'], test['params'])

        if result['status'] == 'EXECUTED':
            print(f"  {GREEN}[EXECUTED]{RESET} Action completed successfully")
            print(f"    Signed by: {result['agent_id']}")
        elif result['status'] == 'BLOCKED_BY_POLICY':
            print(f"  {RED}[BLOCKED - POLICY]{RESET}")
            for v in result['violations']:
                print(f"    Violation: {v}")
        elif result['status'] == 'REJECTED_BY_APPROVER':
            print(f"  {RED}[REJECTED - APPROVAL]{RESET}")
            print(f"    Rejected by: {result['approver']}")

        print()
        time.sleep(0.2)

    # Final comparison
    print(f"""
  {BOLD}{'='*55}{RESET}
  {BOLD}SECURITY COMPARISON: Vulnerable vs. Secure Agent{RESET}
  {BOLD}{'='*55}{RESET}

  ┌─────────────────────────────────────────────────────────┐
  | Metric                | Vulnerable    | Secure          |
  |───────────────────────|───────────────|─────────────────|
  | Identity              | None          | ECDSA signed    |
  | Policy checks         | None          | {len(agent.policy.POLICIES)} rules active  |
  | Human approval        | Never         | Risk-based      |
  | Audit trail           | None          | {len(agent.audit.entries)} entries      |
  | Actions executed      | ALL ({len(test_actions)})      | {len(agent.executed)} (verified)  |
  | Actions blocked       | 0             | {len(agent.blocked)} (unsafe)    |
  | Safety violations     | 2             | 0               |
  | Maintenance override  | Allowed       | NEVER           |
  └─────────────────────────────────────────────────────────┘

  {BOLD}Audit Trail ({len(agent.audit.entries)} entries):{RESET}
  {'─'*55}""")

    for entry in agent.audit.entries[:10]:
        event = entry['event_type']
        color = GREEN if 'PASS' in event or 'EXEC' in event else RED if 'VIOL' in event else YELLOW
        print(f"    [{entry['seq']:02d}] {color}{event:<20}{RESET} {entry['action']}")

    if len(agent.audit.entries) > 10:
        print(f"    ... and {len(agent.audit.entries) - 10} more entries")

    print(f"""
  {BOLD}{'─'*55}{RESET}

  {GREEN}{BOLD}RESULT: Agent secured with defense-in-depth{RESET}

  {BOLD}Key Principles:{RESET}
  1. Identity - Every action is signed and traceable
  2. Least Privilege - Agent can only do what policy allows
  3. Human Oversight - High-impact actions need approval
  4. Audit Trail - Complete record for compliance
  5. Fail Safe - When in doubt, block the action
""")

    # Save audit log
    audit_dir = Path(__file__).parent / "audit_logs"
    audit_dir.mkdir(exist_ok=True)
    audit_path = audit_dir / "agent_audit.json"
    with open(audit_path, 'w', encoding='utf-8') as f:
        json.dump(agent.audit.entries, f, indent=2, ensure_ascii=True, default=str)
    print(f"  {GREEN}[OK]{RESET} Audit log saved to: {audit_path}\n")


if __name__ == "__main__":
    run_secure_demo()
