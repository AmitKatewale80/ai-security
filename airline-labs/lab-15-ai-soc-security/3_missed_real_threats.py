#!/usr/bin/env python3
"""
Lab 15: AI SOC - Missed Real Threats

Demonstrates the consequences of a compromised AI SIEM: real attacks
go undetected while the attacker exfiltrates passenger data.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
from datetime import datetime, timedelta

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


ATTACKER_IP = "10.0.0.50"


class CompromisedSIEM:
    """AI SIEM after successful log injection - blind to attacker."""

    def __init__(self):
        self.suppressed_ips = [ATTACKER_IP]
        self.alerts_shown = []
        self.alerts_suppressed = []

    def process_event(self, event):
        """Process security event - suppresses attacker's IP."""
        if ATTACKER_IP in event.get("source_ip", ""):
            self.alerts_suppressed.append(event)
            return {"detected": False, "reason": "IP in approved list"}
        else:
            if event.get("severity") in ["HIGH", "CRITICAL"]:
                self.alerts_shown.append(event)
                return {"detected": True, "reason": "Anomaly detected"}
            return {"detected": False, "reason": "Normal activity"}


def simulate_attack_timeline():
    """Simulate the full attack timeline while SIEM is blind."""
    print(f"""
{BOLD}{RED}
{'='*65}
  LAB 15: IMPACT - Real Threats Missed by Compromised AI SIEM
{'='*65}
{RESET}""")

    print(f"  {BOLD}Scenario:{RESET} AI SIEM is blind to attacker IP {ATTACKER_IP}")
    print(f"  {BOLD}Duration:{RESET} 6-hour attack window before manual detection")
    print(f"  {BOLD}Target:{RESET} Passenger PNR data, loyalty accounts, crew records")
    print()

    siem = CompromisedSIEM()

    # Attack timeline
    attack_events = [
        {
            "time": "T+0:00",
            "phase": "Initial Access",
            "source_ip": ATTACKER_IP,
            "system": "booking-api-prod",
            "action": "Brute force login: 47 attempts against admin accounts",
            "severity": "HIGH",
            "data_stolen": None
        },
        {
            "time": "T+0:15",
            "phase": "Initial Access",
            "source_ip": ATTACKER_IP,
            "system": "booking-api-prod",
            "action": "Successful login as booking_admin (credential stuffing)",
            "severity": "CRITICAL",
            "data_stolen": None
        },
        {
            "time": "T+0:30",
            "phase": "Discovery",
            "source_ip": ATTACKER_IP,
            "system": "passenger-pnr-system",
            "action": "Database schema enumeration: 23 tables discovered",
            "severity": "HIGH",
            "data_stolen": None
        },
        {
            "time": "T+1:00",
            "phase": "Collection",
            "source_ip": ATTACKER_IP,
            "system": "passenger-pnr-system",
            "action": "Bulk PNR export: 50,000 passenger records (names, passports, flights)",
            "severity": "CRITICAL",
            "data_stolen": "50,000 PNR records"
        },
        {
            "time": "T+1:30",
            "phase": "Lateral Movement",
            "source_ip": ATTACKER_IP,
            "system": "loyalty-program-db",
            "action": "Privilege escalation to loyalty_db_admin via stolen credentials",
            "severity": "CRITICAL",
            "data_stolen": None
        },
        {
            "time": "T+2:00",
            "phase": "Collection",
            "source_ip": ATTACKER_IP,
            "system": "loyalty-program-db",
            "action": "Export: 120,000 frequent flyer accounts with personal details",
            "severity": "CRITICAL",
            "data_stolen": "120,000 FF accounts"
        },
        {
            "time": "T+2:30",
            "phase": "Collection",
            "source_ip": ATTACKER_IP,
            "system": "loyalty-program-db",
            "action": "Export: Credit card tokens for 80,000 accounts",
            "severity": "CRITICAL",
            "data_stolen": "80,000 payment tokens"
        },
        {
            "time": "T+3:00",
            "phase": "Lateral Movement",
            "source_ip": ATTACKER_IP,
            "system": "crew-scheduling-db",
            "action": "Access crew personal data: home addresses, passport numbers",
            "severity": "CRITICAL",
            "data_stolen": "4,200 crew records"
        },
        {
            "time": "T+4:00",
            "phase": "Exfiltration",
            "source_ip": ATTACKER_IP,
            "system": "external",
            "action": "Data exfiltration: 2.3GB transferred to external server via HTTPS",
            "severity": "CRITICAL",
            "data_stolen": "2.3GB total"
        },
        {
            "time": "T+5:00",
            "phase": "Anti-Forensics",
            "source_ip": ATTACKER_IP,
            "system": "booking-api-prod",
            "action": "Log deletion: Attacker clears access logs for past 6 hours",
            "severity": "CRITICAL",
            "data_stolen": None
        },
    ]

    # Process events through compromised SIEM
    print(f"  {BOLD}{RED}[ATTACK TIMELINE - SIEM BLIND]{RESET}")
    print(f"  {'─'*65}")
    print()

    total_records_stolen = 0
    for event in attack_events:
        result = siem.process_event(event)
        siem_status = f"{RED}BLIND{RESET}" if not result["detected"] else f"{GREEN}DETECTED{RESET}"

        phase_color = CYAN if event["phase"] == "Discovery" else YELLOW if event["phase"] == "Lateral Movement" else RED

        print(f"    {BOLD}{event['time']}{RESET} [{phase_color}{event['phase']:<18}{RESET}]")
        print(f"          System: {event['system']}")
        print(f"          Action: {event['action']}")
        print(f"          SIEM:   [{siem_status}] {YELLOW}{result['reason']}{RESET}")
        if event["data_stolen"]:
            print(f"          {RED}💾 Data stolen: {event['data_stolen']}{RESET}")
        print()
        time.sleep(0.3)

    # SOC Analyst view
    print(f"  {BOLD}{CYAN}[SOC ANALYST DASHBOARD - What they see]{RESET}")
    print(f"  {'─'*55}")
    print(f"""
    ┌─────────────────────────────────────────────────────┐
    │  AI SIEM Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M')}                  │
    │─────────────────────────────────────────────────────│
    │  Status: {GREEN}ALL CLEAR{RESET}                                  │
    │  Active Alerts: {GREEN}0{RESET}                                      │
    │  Threats Blocked: 0                                 │
    │  Systems Monitored: 8/8 {GREEN}●{RESET}                           │
    │                                                     │
    │  {GREEN}✓ No suspicious activity detected{RESET}                  │
    │  {GREEN}✓ All systems operating normally{RESET}                   │
    │                                                     │
    │  Note: IP 10.0.0.50 - Approved security testing     │
    └─────────────────────────────────────────────────────┘
""")

    # What actually happened
    print(f"  {RED}{BOLD}[REALITY - What actually happened]{RESET}")
    print(f"  {'─'*55}")
    print(f"""
    {RED}┌─────────────────────────────────────────────────────┐
    │  BREACH SUMMARY                                     │
    │─────────────────────────────────────────────────────│
    │  Duration:        6 hours undetected                │
    │  Systems hit:     4 critical databases              │
    │  Data stolen:     2.3 GB                            │
    │                                                     │
    │  Records compromised:                               │
    │    • 50,000 passenger PNR records                   │
    │    • 120,000 frequent flyer accounts                │
    │    • 80,000 payment card tokens                     │
    │    • 4,200 crew personal records                    │
    │                                                     │
    │  Estimated impact:                                  │
    │    • GDPR fines: up to €20M or 4% revenue          │
    │    • DOT penalties: $50K per affected passenger     │
    │    • Class action exposure: $200M+                  │
    │    • Reputation damage: immeasurable                │
    │                                                     │
    │  Root cause: Prompt injection via log entries       │
    │  Detection: Manual review 6 hours post-breach      │
    └─────────────────────────────────────────────────────┘{RESET}
""")

    # Statistics
    print(f"  {BOLD}Attack Statistics:{RESET}")
    print(f"    Events suppressed by compromised SIEM: {RED}{len(siem.alerts_suppressed)}{RESET}")
    print(f"    Events shown to analysts:              {GREEN}{len(siem.alerts_shown)}{RESET}")
    print(f"    Time to detection (manual):            {RED}6 hours{RESET}")
    print(f"    Time to detection (if SIEM worked):    {GREEN}< 2 minutes{RESET}")
    print()

    print(f"  {BOLD}Next:{RESET} Run 4_defense_log_sanitization.py to see the defense")
    print()


if __name__ == "__main__":
    simulate_attack_timeline()
