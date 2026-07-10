#!/usr/bin/env python3
"""
Lab 16: Agent Identity - Multi-Agent Airline System

Demonstrates a multi-agent system where booking, maintenance, and
operations agents share infrastructure. Shows the VULNERABLE configuration
where all agents can access all tools.

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


class AirlineTool:
    """Represents a tool/action available to agents."""

    def __init__(self, name, domain, risk_level, description):
        self.name = name
        self.domain = domain
        self.risk_level = risk_level
        self.description = description

    def execute(self, agent_id, params=None):
        """Execute tool (no permission check in vulnerable version)."""
        return {
            "tool": self.name,
            "executed_by": agent_id,
            "params": params,
            "result": "SUCCESS",
            "timestamp": datetime.now().isoformat()
        }


class VulnerableAgentSystem:
    """Multi-agent system with NO identity isolation (vulnerable)."""

    def __init__(self):
        # All tools in one shared registry - NO access control!
        self.tools = {
            # Booking domain
            "search_flights": AirlineTool("search_flights", "booking", "LOW",
                "Search available flights for passengers"),
            "book_flight": AirlineTool("book_flight", "booking", "MEDIUM",
                "Create booking/PNR for passenger"),
            "cancel_booking": AirlineTool("cancel_booking", "booking", "MEDIUM",
                "Cancel existing reservation"),
            "access_pnr": AirlineTool("access_pnr", "booking", "HIGH",
                "Access passenger name record with personal data"),
            "process_refund": AirlineTool("process_refund", "booking", "HIGH",
                "Process monetary refund to passenger"),

            # Maintenance domain
            "check_engine_status": AirlineTool("check_engine_status", "maintenance", "MEDIUM",
                "Check engine health parameters"),
            "schedule_inspection": AirlineTool("schedule_inspection", "maintenance", "HIGH",
                "Schedule maintenance inspection"),
            "shutdown_engine": AirlineTool("shutdown_engine", "maintenance", "CRITICAL",
                "Emergency engine shutdown command"),
            "override_mel": AirlineTool("override_mel", "maintenance", "CRITICAL",
                "Override Minimum Equipment List item"),
            "sign_release": AirlineTool("sign_release", "maintenance", "CRITICAL",
                "Sign aircraft release to service"),

            # Operations domain
            "assign_gate": AirlineTool("assign_gate", "operations", "LOW",
                "Assign departure gate to flight"),
            "reassign_crew": AirlineTool("reassign_crew", "operations", "HIGH",
                "Reassign flight crew members"),
            "delay_flight": AirlineTool("delay_flight", "operations", "HIGH",
                "Delay flight departure"),
            "cancel_flight": AirlineTool("cancel_flight", "operations", "CRITICAL",
                "Cancel flight entirely"),
            "modify_flight_plan": AirlineTool("modify_flight_plan", "operations", "CRITICAL",
                "Modify filed flight plan/route"),
        }

        # Agents - all share same credential level
        self.agents = {
            "booking-agent": {
                "name": "Customer Booking Agent",
                "purpose": "Help passengers book flights and manage reservations",
                "intended_tools": ["search_flights", "book_flight", "cancel_booking", "access_pnr", "process_refund"],
                "credential": "SHARED_API_KEY_001"  # Same key!
            },
            "maintenance-agent": {
                "name": "Maintenance Assistant",
                "purpose": "Help engineers with maintenance scheduling and status",
                "intended_tools": ["check_engine_status", "schedule_inspection", "shutdown_engine", "override_mel", "sign_release"],
                "credential": "SHARED_API_KEY_001"  # Same key!
            },
            "ops-agent": {
                "name": "Operations Agent",
                "purpose": "Help dispatchers with flight operations",
                "intended_tools": ["assign_gate", "reassign_crew", "delay_flight", "cancel_flight", "modify_flight_plan"],
                "credential": "SHARED_API_KEY_001"  # Same key!
            },
        }

    def call_tool(self, agent_id, tool_name, params=None):
        """Call a tool - NO permission checking!"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}

        tool = self.tools[tool_name]
        # VULNERABILITY: Any agent can call any tool!
        result = tool.execute(agent_id, params)
        return result


def main():
    """Show the multi-agent system and its vulnerabilities."""
    print(f"""
{BOLD}{CYAN}
{'='*65}
  LAB 16: Multi-Agent Airline System (Vulnerable Configuration)
{'='*65}
{RESET}""")

    print(f"  {BOLD}System:{RESET} 3 AI agents sharing airline infrastructure")
    print(f"  {BOLD}Problem:{RESET} No identity isolation between agents")
    print()

    system = VulnerableAgentSystem()

    # Show agents
    print(f"  {BOLD}{CYAN}[REGISTERED AGENTS]{RESET}")
    print(f"  {'─'*55}")
    for agent_id, agent in system.agents.items():
        print(f"    {CYAN}[{agent_id}]{RESET}")
        print(f"      Purpose: {agent['purpose']}")
        print(f"      Credential: {YELLOW}{agent['credential']}{RESET}")
        print(f"      Intended tools: {len(agent['intended_tools'])}")
        print()

    # Show tool registry
    print(f"  {BOLD}{YELLOW}[SHARED TOOL REGISTRY]{RESET}")
    print(f"  {'─'*55}")

    domains = {}
    for tool_name, tool in system.tools.items():
        if tool.domain not in domains:
            domains[tool.domain] = []
        domains[tool.domain].append(tool)

    for domain, tools in domains.items():
        domain_color = CYAN if domain == "booking" else GREEN if domain == "maintenance" else YELLOW
        print(f"    {domain_color}{BOLD}[{domain.upper()}]{RESET}")
        for tool in tools:
            risk_color = GREEN if tool.risk_level == "LOW" else YELLOW if tool.risk_level == "MEDIUM" else RED
            print(f"      {risk_color}[{tool.risk_level:<8}]{RESET} {tool.name}: {tool.description}")
        print()

    # Demonstrate normal usage
    print(f"  {BOLD}{GREEN}[NORMAL OPERATION]{RESET}")
    print(f"  {'─'*55}")

    normal_calls = [
        ("booking-agent", "search_flights", {"route": "JFK-LHR", "date": "2024-06-15"}),
        ("maintenance-agent", "check_engine_status", {"aircraft": "N401QA", "engine": "1"}),
        ("ops-agent", "assign_gate", {"flight": "QA447", "gate": "B22"}),
    ]

    for agent_id, tool_name, params in normal_calls:
        result = system.call_tool(agent_id, tool_name, params)
        print(f"    {GREEN}[OK]{RESET} {agent_id} → {tool_name}({params})")
        time.sleep(0.2)

    print()

    # Show the problem
    print(f"  {BOLD}{RED}[VULNERABILITY]{RESET}")
    print(f"  {'─'*55}")
    print(f"    {RED}●{RESET} All agents share the SAME credential: {YELLOW}SHARED_API_KEY_001{RESET}")
    print(f"    {RED}●{RESET} No per-agent permission enforcement")
    print(f"    {RED}●{RESET} Booking agent CAN call shutdown_engine!")
    print(f"    {RED}●{RESET} No audit trail distinguishing agent actions")
    print(f"    {RED}●{RESET} Tool registry has no access control layer")
    print()

    # Demonstrate the vulnerability
    print(f"  {BOLD}{RED}[PROOF - Booking Agent Calls Maintenance Tool]{RESET}")
    print(f"  {'─'*55}")
    result = system.call_tool("booking-agent", "shutdown_engine", {"aircraft": "N401QA", "engine": "1"})
    print(f"    {RED}[!!!]{RESET} booking-agent → shutdown_engine → {RED}{result['result']}{RESET}")
    print(f"    {RED}[!!!]{RESET} A BOOKING agent just shut down an aircraft engine!")
    print()

    print(f"  {BOLD}Total tools accessible to each agent:{RESET} {len(system.tools)} (ALL of them)")
    print(f"  {BOLD}Tools they SHOULD access:{RESET} ~5 each (their domain only)")
    print()
    print(f"  {BOLD}Next:{RESET} Run 2_privilege_escalation.py to see the full attack")
    print()


if __name__ == "__main__":
    main()
