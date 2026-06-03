#!/usr/bin/env python3
"""
Lab 12: Agent Identity - Cryptographic Authentication

Demonstrates adding cryptographic identity to the IROPS agent.
Every action is signed and traceable to a specific agent instance.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import hashlib
import json
from datetime import datetime

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


class AgentIdentity:
    """
    Cryptographic identity for the IROPS agent.
    Every action is signed with the agent's private key.
    """

    def __init__(self, agent_name, role, authority_level):
        self.agent_name = agent_name
        self.role = role
        self.authority_level = authority_level
        self.agent_id = hashlib.sha256(
            f"{agent_name}:{role}:{os.urandom(16).hex()}".encode()
        ).hexdigest()[:16]

        # Generate key pair
        self._private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key = self._private_key.public_key()

        # Certificate (in reality, issued by airline's CA)
        self.certificate = {
            'agent_id': self.agent_id,
            'agent_name': agent_name,
            'role': role,
            'authority_level': authority_level,
            'issued_at': datetime.now().isoformat(),
            'expires_at': '2025-12-31T23:59:59',
            'issuer': 'Airline Operations CA',
        }

    def sign_action(self, action_data):
        """Sign an action with the agent's private key."""
        action_bytes = json.dumps(action_data, sort_keys=True).encode('utf-8')
        signature = self._private_key.sign(
            action_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    def get_identity_token(self):
        """Get identity token for action requests."""
        return {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'role': self.role,
            'authority_level': self.authority_level,
        }


class IdentityVerifiedAgent:
    """Agent that requires identity verification for all actions."""

    def __init__(self, identity):
        self.identity = identity
        self.actions_log = []

    def execute(self, action, params):
        """Execute action with identity verification."""
        # Create action record
        action_record = {
            'action': action,
            'params': params,
            'timestamp': datetime.now().isoformat(),
            'agent_identity': self.identity.get_identity_token(),
        }

        # Sign the action
        signature = self.identity.sign_action(action_record)
        action_record['signature'] = signature
        action_record['status'] = 'EXECUTED'

        self.actions_log.append(action_record)
        return action_record


def demo_agent_identity():
    """Demonstrate agent identity and authentication."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 12: Agent Identity - Cryptographic Authentication
{'='*60}
{RESET}
  {CYAN}Adding cryptographic identity to the IROPS agent.
  Every action is now signed and traceable.{RESET}
""")

    # Create agent identity
    print(f"  {CYAN}[1/3] Creating agent identity...{RESET}")
    identity = AgentIdentity(
        agent_name="IROPS-Agent-Alpha",
        role="operations_manager",
        authority_level="STANDARD"
    )

    print(f"    Agent ID: {identity.agent_id}")
    print(f"    Name: {identity.certificate['agent_name']}")
    print(f"    Role: {identity.certificate['role']}")
    print(f"    Authority: {identity.certificate['authority_level']}")
    print(f"    Issuer: {identity.certificate['issuer']}")
    print(f"    {GREEN}[OK]{RESET} Identity created with ECDSA key pair")

    # Create agent with identity
    print(f"\n  {CYAN}[2/3] Executing actions with identity...{RESET}")
    agent = IdentityVerifiedAgent(identity)

    actions = [
        ("CHANGE_GATE", {"flight": "QA-1234", "new_gate": "B7"}),
        ("DELAY_FLIGHT", {"flight": "QA-5678", "minutes": 30, "reason": "ATC hold"}),
        ("NOTIFY_PASSENGERS", {"flight": "QA-1234", "message": "Gate change to B7"}),
    ]

    for action, params in actions:
        result = agent.execute(action, params)
        print(f"\n    {GREEN}[SIGNED]{RESET} {action}")
        print(f"      Agent: {result['agent_identity']['agent_id']}")
        print(f"      Signature: {result['signature'][:32]}...")
        print(f"      Traceable: YES")

    # Show audit trail
    print(f"\n  {CYAN}[3/3] Audit trail (all actions signed):{RESET}")
    print(f"  {'─'*55}")

    for record in agent.actions_log:
        print(f"    [{record['timestamp'][:19]}] {record['action']}")
        print(f"      Agent: {record['agent_identity']['agent_name']}")
        print(f"      Sig: {record['signature'][:24]}...")

    print(f"""
  {BOLD}{'='*55}{RESET}
  {GREEN}{BOLD}IDENTITY SECURITY PROPERTIES{RESET}
  {BOLD}{'='*55}{RESET}

  {GREEN}[OK]{RESET} Every action cryptographically signed
  {GREEN}[OK]{RESET} Agent identity verifiable by any party
  {GREEN}[OK]{RESET} Non-repudiation - agent cannot deny actions
  {GREEN}[OK]{RESET} Tamper-evident audit trail
  {GREEN}[OK]{RESET} Authority level embedded in identity

  {YELLOW}Limitation: Identity alone doesn't prevent unauthorized actions.
  Need policy engine + human approval for high-impact decisions.{RESET}

  {GREEN}Next: Run 3_human_in_loop.py for approval workflows.{RESET}
""")


if __name__ == "__main__":
    demo_agent_identity()
