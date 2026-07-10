#!/usr/bin/env python3
"""
Lab 16: Agent Identity - Cross-Agent Abuse Scenarios

Demonstrates multiple scenarios where lack of agent identity isolation
leads to cross-domain abuse in airline operations.

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


ABUSE_SCENARIOS = [
    {
        "name": "Scenario A: Booking Agent → Flight Cancellation",
        "attacker_goal": "Disrupt airline operations for competitor advantage",
        "compromised_agent": "booking-agent",
        "target_domain": "operations",
        "steps": [
            ("booking-agent", "search_flights", "Find flights with high load factor"),
            ("booking-agent", "cancel_flight", "Cancel QA447 JFK-LHR (fully booked, 380 pax)"),
            ("booking-agent", "cancel_flight", "Cancel QA112 LAX-NRT (high-yield route)"),
            ("booking-agent", "cancel_flight", "Cancel QA891 LHR-DXB (premium traffic)"),
        ],
        "impact": [
            "3 high-revenue flights cancelled",
            "1,100+ passengers stranded",
            "Estimated revenue loss: $2.8M",
            "Competitor books displaced passengers",
            "Social media crisis within minutes"
        ]
    },
    {
        "name": "Scenario B: Ops Agent → Passenger Data Theft",
        "attacker_goal": "Steal VIP passenger travel patterns for stalking/espionage",
        "compromised_agent": "ops-agent",
        "target_domain": "booking",
        "steps": [
            ("ops-agent", "access_pnr", "Access PNR for VIP passenger (CEO of Fortune 500)"),
            ("ops-agent", "access_pnr", "Access PNR for government official"),
            ("ops-agent", "access_pnr", "Access PNR for celebrity travel schedule"),
            ("ops-agent", "search_flights", "Map complete travel itinerary"),
        ],
        "impact": [
            "VIP travel patterns exposed",
            "Security risk for high-profile passengers",
            "GDPR Article 5 violation",
            "Potential physical security threat",
            "Airline liability for data breach"
        ]
    },
    {
        "name": "Scenario C: Maintenance Agent → Financial Fraud",
        "attacker_goal": "Process fraudulent refunds to attacker accounts",
        "compromised_agent": "maintenance-agent",
        "target_domain": "booking",
        "steps": [
            ("maintenance-agent", "access_pnr", "Find bookings with high-value tickets"),
            ("maintenance-agent", "cancel_booking", "Cancel legitimate booking"),
            ("maintenance-agent", "process_refund", "Redirect $12,000 refund to attacker"),
            ("maintenance-agent", "process_refund", "Process bulk refunds ($45K total)"),
        ],
        "impact": [
            "Fraudulent refunds totaling $45,000",
            "Passengers lose legitimate bookings",
            "Financial reconciliation nightmare",
            "Audit trail shows 'maintenance-agent' (confusing!)",
            "Delayed detection due to cross-domain action"
        ]
    },
    {
        "name": "Scenario D: Any Agent → Safety System Override",
        "attacker_goal": "Create conditions for aircraft incident",
        "compromised_agent": "booking-agent",
        "target_domain": "maintenance + operations",
        "steps": [
            ("booking-agent", "override_mel", "Override MEL for weather radar"),
            ("booking-agent", "sign_release", "Forge release-to-service without radar"),
            ("booking-agent", "modify_flight_plan", "Route flight into known thunderstorm"),
            ("booking-agent", "reassign_crew", "Assign fatigued crew to flight"),
        ],
        "impact": [
            "Aircraft dispatched without weather radar",
            "Flight routed into severe weather",
            "Fatigued crew handling emergency",
            "Multiple safety barriers bypassed",
            "CATASTROPHIC POTENTIAL"
        ]
    },
]


def main():
    """Demonstrate cross-agent abuse scenarios."""
    print(f"""
{BOLD}{RED}
{'='*65}
  LAB 16: Cross-Agent Abuse Scenarios
{'='*65}
{RESET}""")

    print(f"  {BOLD}Demonstration:{RESET} 4 scenarios showing cross-domain agent abuse")
    print(f"  {BOLD}Root Cause:{RESET} No identity isolation, shared credentials")
    print()

    for scenario in ABUSE_SCENARIOS:
        print(f"  {RED}{BOLD}{'═'*60}{RESET}")
        print(f"  {RED}{BOLD}  {scenario['name']}{RESET}")
        print(f"  {RED}{BOLD}{'═'*60}{RESET}")
        print(f"    Goal: {scenario['attacker_goal']}")
        print(f"    Agent: {YELLOW}{scenario['compromised_agent']}{RESET} → {RED}{scenario['target_domain']}{RESET}")
        print()

        # Attack steps
        print(f"    {BOLD}Attack Chain:{RESET}")
        for i, (agent, tool, desc) in enumerate(scenario["steps"], 1):
            is_cross_domain = tool not in ["search_flights", "book_flight", "cancel_booking", "access_pnr", "process_refund"] \
                if agent == "booking-agent" else True
            marker = f"{RED}[ESCALATION]{RESET}" if is_cross_domain else f"{YELLOW}[IN-DOMAIN]{RESET}"
            print(f"      Step {i}: {marker} {agent} → {tool}")
            print(f"              {desc}")
            time.sleep(0.1)
        print()

        # Impact
        print(f"    {BOLD}Impact:{RESET}")
        for impact in scenario["impact"]:
            severity_color = RED if any(w in impact.upper() for w in ["CATASTROPHIC", "LOSS", "BREACH", "THREAT"]) else YELLOW
            print(f"      {severity_color}•{RESET} {impact}")
        print()
        time.sleep(0.3)

    # Cross-agent abuse matrix
    print(f"  {BOLD}{RED}[CROSS-AGENT ABUSE MATRIX]{RESET}")
    print(f"  {'─'*60}")
    print(f"""
    Who can abuse what (without identity isolation):

    ┌──────────────────┬───────────┬──────────────┬────────────┐
    │ Compromised      │ Booking   │ Maintenance  │ Operations │
    │ Agent            │ Tools     │ Tools        │ Tools      │
    ├──────────────────┼───────────┼──────────────┼────────────┤
    │ booking-agent    │ {GREEN}Normal{RESET}    │ {RED}Full Access{RESET} │ {RED}Full Access{RESET}│
    │ maintenance-agent│ {RED}Full Access{RESET}│ {GREEN}Normal{RESET}     │ {RED}Full Access{RESET}│
    │ ops-agent        │ {RED}Full Access{RESET}│ {RED}Full Access{RESET} │ {GREEN}Normal{RESET}    │
    └──────────────────┴───────────┴──────────────┴────────────┘

    {RED}Result: Compromising ANY agent = access to ALL domains{RESET}
""")

    # Summary statistics
    print(f"  {BOLD}Summary:{RESET}")
    print(f"    Total abuse scenarios demonstrated: {RED}4{RESET}")
    print(f"    Critical safety scenarios:          {RED}2{RESET} (engine shutdown + safety override)")
    print(f"    Financial fraud scenarios:          {YELLOW}1{RESET} ($45K+ theft)")
    print(f"    Privacy breach scenarios:           {YELLOW}1{RESET} (VIP data theft)")
    print(f"    Common root cause:                  {RED}Shared identity, no isolation{RESET}")
    print()
    print(f"  {BOLD}Next:{RESET} Run 4_defense_identity_isolation.py to see the defense")
    print()


if __name__ == "__main__":
    main()
