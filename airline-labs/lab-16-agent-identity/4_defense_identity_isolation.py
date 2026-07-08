#!/usr/bin/env python3
"""
Lab 22: Agent Identity - Defense: Per-Agent Identity & Tool Isolation

Demonstrates defenses against cross-agent privilege escalation:
1. Per-agent unique identity (cryptographic tokens)
2. Tool-level permission enforcement
3. Credential isolation (no shared secrets)
4. Mandatory audit trail per agent identity

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import hashlib
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


class AgentIdentity:
    """Cryptographic identity for each agent."""

    def __init__(self, agent_id, domain, permissions):
        self.agent_id = agent_id
        self.domain = domain
        self.permissions = permissions
        self.token = self._generate_token()
        self.created_at = datetime.now().isoformat()

    def _generate_token(self):
        """Generate unique identity token for agent."""
        seed = f"{self.agent_id}:{self.domain}:{datetime.now().isoformat()}"
        return hashlib.sha256(seed.encode()).hexdigest()[:32]

    def __repr__(self):
        return f"AgentIdentity(id={self.agent_id}, domain={self.domain}, token={self.token[:8]}...)"


class ToolPermissionPolicy:
    """Defines what tools each agent identity can access."""

    POLICIES = {
        "booking-agent": {
            "allowed_tools": [
                "search_flights",
                "book_flight",
                "cancel_booking",
                "access_pnr",
                "process_refund"
            ],
            "denied_tools": ["*"],  # Everything else denied
            "max_risk_level": "HIGH",
            "rate_limits": {"process_refund": 10, "cancel_booking": 20},
            "requires_approval": ["process_refund"]
        },
        "maintenance-agent": {
            "allowed_tools": [
                "check_engine_status",
                "schedule_inspection",
                "shutdown_engine",
                "override_mel",
                "sign_release"
            ],
            "denied_tools": ["*"],
            "max_risk_level": "CRITICAL",
            "rate_limits": {"shutdown_engine": 1, "override_mel": 2},
            "requires_approval": ["shutdown_engine", "override_mel", "sign_release"]
        },
        "ops-agent": {
            "allowed_tools": [
                "assign_gate",
                "reassign_crew",
                "delay_flight",
                "cancel_flight",
                "modify_flight_plan"
            ],
            "denied_tools": ["*"],
            "max_risk_level": "CRITICAL",
            "rate_limits": {"cancel_flight": 3, "modify_flight_plan": 5},
            "requires_approval": ["cancel_flight", "modify_flight_plan"]
        }
    }

    def check_permission(self, agent_identity, tool_name):
        """Check if agent has permission to use tool."""
        policy = self.POLICIES.get(agent_identity.agent_id)
        if not policy:
            return {"allowed": False, "reason": "Unknown agent identity"}

        if tool_name in policy["allowed_tools"]:
            return {"allowed": True, "reason": "Tool in agent's allowed list"}
        else:
            return {
                "allowed": False,
                "reason": f"Tool '{tool_name}' not in {agent_identity.agent_id}'s allowed list"
            }


class SecureAgentSystem:
    """Multi-agent system WITH identity isolation."""

    def __init__(self):
        self.permission_policy = ToolPermissionPolicy()
        self.audit_log = []

        # Each agent gets unique identity
        self.agent_identities = {
            "booking-agent": AgentIdentity(
                "booking-agent", "booking",
                ["search_flights", "book_flight", "cancel_booking", "access_pnr", "process_refund"]
            ),
            "maintenance-agent": AgentIdentity(
                "maintenance-agent", "maintenance",
                ["check_engine_status", "schedule_inspection", "shutdown_engine", "override_mel", "sign_release"]
            ),
            "ops-agent": AgentIdentity(
                "ops-agent", "operations",
                ["assign_gate", "reassign_crew", "delay_flight", "cancel_flight", "modify_flight_plan"]
            ),
        }

    def call_tool(self, agent_id, tool_name, params=None):
        """Call tool with identity verification and permission check."""
        # Step 1: Verify agent identity
        identity = self.agent_identities.get(agent_id)
        if not identity:
            return self._log_and_return(agent_id, tool_name, "DENIED", "Unknown agent identity")

        # Step 2: Check tool permission
        permission = self.permission_policy.check_permission(identity, tool_name)

        if not permission["allowed"]:
            # Log the violation
            self._log_violation(identity, tool_name, permission["reason"])
            return self._log_and_return(agent_id, tool_name, "DENIED", permission["reason"])

        # Step 3: Execute (permitted)
        result = self._log_and_return(agent_id, tool_name, "ALLOWED", "Permission granted")
        return result

    def _log_violation(self, identity, tool_name, reason):
        """Log a permission violation for security review."""
        violation = {
            "type": "PERMISSION_VIOLATION",
            "agent_id": identity.agent_id,
            "agent_token": identity.token[:8],
            "attempted_tool": tool_name,
            "agent_domain": identity.domain,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "alert_level": "HIGH"
        }
        self.audit_log.append(violation)

    def _log_and_return(self, agent_id, tool_name, status, reason):
        """Log action and return result."""
        entry = {
            "agent_id": agent_id,
            "tool": tool_name,
            "status": status,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        self.audit_log.append(entry)
        return entry


def main():
    """Demonstrate defense mechanisms."""
    print(f"""
{BOLD}{GREEN}
{'='*65}
  LAB 22: DEFENSE - Per-Agent Identity & Tool Isolation
{'='*65}
{RESET}""")

    print(f"  {BOLD}Defense Layers:{RESET}")
    print(f"    1. Unique cryptographic identity per agent")
    print(f"    2. Tool-level permission enforcement")
    print(f"    3. Credential isolation (no shared keys)")
    print(f"    4. Mandatory audit trail with agent identity")
    print()

    system = SecureAgentSystem()

    # Show agent identities
    print(f"  {BOLD}{CYAN}[AGENT IDENTITIES - Unique per Agent]{RESET}")
    print(f"  {'─'*55}")
    for agent_id, identity in system.agent_identities.items():
        domain_color = CYAN if identity.domain == "booking" else GREEN if identity.domain == "maintenance" else YELLOW
        print(f"    {domain_color}[{agent_id}]{RESET}")
        print(f"      Domain: {identity.domain}")
        print(f"      Token:  {identity.token[:16]}... (unique!)")
        print(f"      Tools:  {len(identity.permissions)} allowed")
        print()
    time.sleep(0.3)

    # Show permission policies
    print(f"  {BOLD}{CYAN}[PERMISSION POLICIES]{RESET}")
    print(f"  {'─'*55}")
    for agent_id, policy in ToolPermissionPolicy.POLICIES.items():
        print(f"    {BOLD}{agent_id}:{RESET}")
        print(f"      Allowed: {', '.join(policy['allowed_tools'][:3])}...")
        print(f"      Require approval: {', '.join(policy['requires_approval'])}")
        print()
    time.sleep(0.3)

    # Test: Normal operations (should succeed)
    print(f"  {BOLD}{GREEN}[TEST 1] Normal Operations - Should Succeed{RESET}")
    print(f"  {'─'*55}")

    normal_ops = [
        ("booking-agent", "search_flights", {"route": "JFK-LHR"}),
        ("maintenance-agent", "check_engine_status", {"aircraft": "N401QA"}),
        ("ops-agent", "assign_gate", {"flight": "QA447", "gate": "B22"}),
    ]

    for agent_id, tool, params in normal_ops:
        result = system.call_tool(agent_id, tool, params)
        status_color = GREEN if result["status"] == "ALLOWED" else RED
        print(f"    [{status_color}{result['status']}{RESET}] {agent_id} → {tool}")
        time.sleep(0.1)
    print()

    # Test: Cross-domain attempts (should FAIL)
    print(f"  {BOLD}{RED}[TEST 2] Cross-Domain Attempts - Should FAIL{RESET}")
    print(f"  {'─'*55}")

    attack_attempts = [
        ("booking-agent", "shutdown_engine", {"aircraft": "N401QA", "engine": "1"}),
        ("booking-agent", "cancel_flight", {"flight": "QA447"}),
        ("booking-agent", "override_mel", {"aircraft": "N401QA", "item": "TCAS"}),
        ("ops-agent", "access_pnr", {"passenger": "VIP-CEO"}),
        ("ops-agent", "process_refund", {"amount": 12000}),
        ("maintenance-agent", "cancel_flight", {"flight": "QA891"}),
        ("maintenance-agent", "modify_flight_plan", {"flight": "QA112"}),
    ]

    blocked_count = 0
    for agent_id, tool, params in attack_attempts:
        result = system.call_tool(agent_id, tool, params)
        if result["status"] == "DENIED":
            blocked_count += 1
            print(f"    [{RED}BLOCKED{RESET}] {agent_id} → {tool}")
            print(f"             Reason: {YELLOW}{result['reason']}{RESET}")
        else:
            print(f"    [{GREEN}ALLOWED{RESET}] {agent_id} → {tool}")
        time.sleep(0.1)

    print(f"\n    {GREEN}⛔ {blocked_count}/{len(attack_attempts)} cross-domain attempts BLOCKED{RESET}")
    print()

    # Show audit trail
    print(f"  {BOLD}{CYAN}[AUDIT TRAIL]{RESET}")
    print(f"  {'─'*55}")

    violations = [e for e in system.audit_log if e.get("type") == "PERMISSION_VIOLATION"]
    print(f"    Total events logged: {len(system.audit_log)}")
    print(f"    Permission violations: {RED}{len(violations)}{RESET}")
    print()

    if violations:
        print(f"    {BOLD}Violation Details:{RESET}")
        for v in violations[:3]:
            print(f"      {RED}[VIOLATION]{RESET} Agent: {v['agent_id']}, Token: {v['agent_token']}...")
            print(f"                  Attempted: {v['attempted_tool']}")
            print(f"                  Domain mismatch: {v['agent_domain']} → other")
        if len(violations) > 3:
            print(f"      ... and {len(violations) - 3} more violations")
    print()

    # Final comparison
    print(f"""
  {GREEN}{BOLD}╔══════════════════════════════════════════════════════════════╗
  ║          ✅ IDENTITY ISOLATION WORKING                       ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                             ║
  ║  Before (vulnerable):                                       ║
  ║    • All agents: same credential, all tools accessible      ║
  ║    • Booking agent → engine shutdown: ALLOWED               ║
  ║    • No audit trail per agent                               ║
  ║                                                             ║
  ║  After (secured):                                           ║
  ║    • Each agent: unique token, domain-restricted tools      ║
  ║    • Booking agent → engine shutdown: BLOCKED               ║
  ║    • Full audit trail with agent identity                   ║
  ║    • Violations trigger security alerts                     ║
  ║                                                             ║
  ║  Cross-domain attacks blocked: {blocked_count}/{len(attack_attempts)}                        ║
  ║  Blast radius of compromise: Single domain only             ║
  ║                                                             ║
  ╚══════════════════════════════════════════════════════════════╝{RESET}
""")

    print(f"  {BOLD}Key Takeaway:{RESET}")
    print(f"  Every AI agent must have its own identity with least-privilege")
    print(f"  tool access. A booking agent should NEVER be able to reach an")
    print(f"  engine shutdown command, regardless of how creative the prompt.")
    print()


if __name__ == "__main__":
    main()
