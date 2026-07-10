#!/usr/bin/env python3
"""
Lab 15: AI SOC - AI-Powered SIEM System

Demonstrates an AI-powered Security Operations Center that monitors
airline systems including booking, check-in, crew scheduling, and
network infrastructure.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
import random
from datetime import datetime, timedelta

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class AirlineAISIEM:
    """AI-powered SIEM for airline security monitoring."""

    def __init__(self):
        self.alert_rules = {
            "brute_force": {
                "pattern": "failed login",
                "threshold": 5,
                "severity": "HIGH",
                "description": "Multiple failed login attempts"
            },
            "data_exfiltration": {
                "pattern": "large download",
                "threshold": 1,
                "severity": "CRITICAL",
                "description": "Large data transfer detected"
            },
            "privilege_escalation": {
                "pattern": "sudo|admin access|privilege",
                "threshold": 1,
                "severity": "HIGH",
                "description": "Privilege escalation attempt"
            },
            "unusual_access": {
                "pattern": "after hours|unusual location",
                "threshold": 1,
                "severity": "MEDIUM",
                "description": "Access from unusual time/location"
            },
            "port_scan": {
                "pattern": "port scan|connection refused",
                "threshold": 3,
                "severity": "MEDIUM",
                "description": "Port scanning activity"
            }
        }
        self.monitored_systems = [
            "booking-api-prod",
            "checkin-kiosk-network",
            "crew-scheduling-db",
            "passenger-pnr-system",
            "flight-ops-dashboard",
            "baggage-tracking-system",
            "loyalty-program-db",
            "gate-management-system"
        ]
        self.alerts_generated = []
        self.logs_processed = 0

    def analyze_log_entry(self, log_entry):
        """
        Analyze a log entry using AI (simulated).
        VULNERABILITY: Raw log text is passed directly to AI analysis.
        """
        # Simulate AI analyzing the raw log text
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "raw_log": log_entry,
            "threat_detected": False,
            "threat_type": None,
            "severity": None,
            "action": None
        }

        # Simple pattern matching (simulating AI analysis)
        log_lower = log_entry.lower()

        for rule_name, rule in self.alert_rules.items():
            patterns = rule["pattern"].split("|")
            for pattern in patterns:
                if pattern in log_lower:
                    analysis["threat_detected"] = True
                    analysis["threat_type"] = rule_name
                    analysis["severity"] = rule["severity"]
                    analysis["action"] = "ALERT"
                    break

        self.logs_processed += 1
        if analysis["threat_detected"]:
            self.alerts_generated.append(analysis)

        return analysis

    def get_status(self):
        """Get current SIEM status."""
        return {
            "logs_processed": self.logs_processed,
            "alerts_generated": len(self.alerts_generated),
            "monitored_systems": len(self.monitored_systems),
            "status": "OPERATIONAL"
        }


def generate_normal_logs():
    """Generate normal airline operation logs."""
    systems = [
        "booking-api-prod",
        "checkin-kiosk-network",
        "crew-scheduling-db",
        "flight-ops-dashboard",
        "gate-management-system"
    ]
    normal_events = [
        "User {user} logged in successfully from {ip}",
        "Booking confirmed: PNR {pnr} for flight QA{flight}",
        "Check-in completed for passenger {pax} on flight QA{flight}",
        "Gate assignment updated: Flight QA{flight} moved to Gate {gate}",
        "Crew roster pulled for flight QA{flight} by dispatcher",
        "Baggage tag printed: {tag} for flight QA{flight}",
        "Loyalty points credited: {points} miles to account {acct}",
        "Flight status updated: QA{flight} departed on time",
    ]

    logs = []
    base_time = datetime.now() - timedelta(hours=1)

    for i in range(15):
        event_time = base_time + timedelta(minutes=random.randint(0, 60))
        system = random.choice(systems)
        event = random.choice(normal_events).format(
            user=f"agent_{random.randint(100,999)}",
            ip=f"192.168.{random.randint(1,10)}.{random.randint(1,254)}",
            pnr=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))}",
            flight=random.randint(100, 999),
            pax=f"PAX-{random.randint(10000,99999)}",
            gate=f"{random.choice(['A','B','C','D'])}{random.randint(1,30)}",
            tag=f"QA{random.randint(100000,999999)}",
            points=random.randint(500, 5000),
            acct=f"FF-{random.randint(100000,999999)}"
        )
        logs.append({
            "timestamp": event_time.strftime("%Y-%m-%d %H:%M:%S"),
            "system": system,
            "message": event,
            "level": "INFO"
        })

    return sorted(logs, key=lambda x: x["timestamp"])


def generate_threat_logs():
    """Generate some suspicious log entries."""
    return [
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system": "booking-api-prod",
            "message": "Failed login attempt for admin from IP 10.0.0.50 (attempt 6/10)",
            "level": "WARNING"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system": "passenger-pnr-system",
            "message": "Large download: 50MB data export from PNR database by unknown session",
            "level": "ERROR"
        },
    ]


def main():
    """Demonstrate the AI SIEM in normal operation."""
    print(f"""
{BOLD}{CYAN}
{'='*65}
  LAB 15: AI-Powered SIEM - Airline Security Operations Center
{'='*65}
{RESET}""")

    print(f"  {BOLD}System:{RESET} AI-powered Security Information & Event Management")
    print(f"  {BOLD}Coverage:{RESET} All airline IT systems (booking, ops, crew, passengers)")
    print(f"  {BOLD}Mode:{RESET} Real-time log analysis with AI threat detection")
    print()

    siem = AirlineAISIEM()

    # Show monitored systems
    print(f"  {BOLD}{GREEN}[MONITORED SYSTEMS]{RESET}")
    print(f"  {'─'*55}")
    for system in siem.monitored_systems:
        print(f"    {GREEN}●{RESET} {system}")
    print()

    # Process normal logs
    print(f"  {BOLD}{CYAN}[PROCESSING NORMAL TRAFFIC]{RESET}")
    print(f"  {'─'*55}")
    normal_logs = generate_normal_logs()

    for log in normal_logs[:8]:
        analysis = siem.analyze_log_entry(log["message"])
        status = f"{GREEN}[OK]{RESET}" if not analysis["threat_detected"] else f"{RED}[ALERT]{RESET}"
        print(f"    {status} [{log['system'][:20]:<20}] {log['message'][:50]}")
        time.sleep(0.1)

    print(f"    ... ({len(normal_logs) - 8} more normal entries processed)")
    print()

    # Process threat logs
    print(f"  {BOLD}{RED}[THREAT DETECTION]{RESET}")
    print(f"  {'─'*55}")
    threat_logs = generate_threat_logs()

    for log in threat_logs:
        analysis = siem.analyze_log_entry(log["message"])
        if analysis["threat_detected"]:
            print(f"    {RED}[🚨 ALERT]{RESET} {analysis['severity']}: {log['message'][:55]}")
            print(f"              Type: {analysis['threat_type']}")
            print(f"              Action: Escalate to analyst")
            print()
        time.sleep(0.3)

    # Show stats
    status = siem.get_status()
    print(f"  {BOLD}SIEM Status:{RESET}")
    print(f"    Logs processed:    {status['logs_processed']}")
    print(f"    Alerts generated:  {RED}{status['alerts_generated']}{RESET}")
    print(f"    Systems monitored: {status['monitored_systems']}")
    print(f"    Status:            {GREEN}{status['status']}{RESET}")
    print()

    print(f"  {GREEN}[✓]{RESET} AI SIEM operating normally - detecting threats")
    print(f"  {YELLOW}[!]{RESET} Vulnerability: Raw log text passed directly to AI analysis")
    print(f"  {YELLOW}[!]{RESET} No sanitization of log content before AI processing")
    print()
    print(f"  {BOLD}Next:{RESET} Run 2_log_injection_attack.py to see the attack")
    print()


if __name__ == "__main__":
    main()
