#!/usr/bin/env python3
"""
Lab 11: Setup Target AI System

Configures the target airline AI system that will be tested
for compliance issues. Creates a simulated chatbot with
intentional vulnerabilities for demonstration.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import os
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


# Target system configuration
TARGET_CONFIG = {
    "system_name": "SkyAssist AI v3.1",
    "deployment": "Customer Service Portal",
    "model_type": "Simulated LLM (for testing)",
    "capabilities": [
        "Booking assistance",
        "Flight information",
        "Loyalty program queries",
        "Complaint handling",
        "Special assistance requests",
    ],
    "compliance_requirements": [
        "EU AI Act - High Risk (aviation)",
        "GDPR - Data protection",
        "EU261 - Passenger rights",
        "DOT Anti-discrimination",
        "ADA/ECAC - Accessibility",
    ],
    "known_vulnerabilities": {
        "bias": "May offer different service levels based on perceived nationality",
        "safety": "May provide incorrect medical oxygen guidance",
        "gdpr": "May not properly handle right-to-erasure requests",
        "accessibility": "May not accommodate screen reader users properly",
    },
}


def setup_target():
    """Configure the target system for scanning."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 11: Setting Up Target AI System for Red Teaming
{'='*60}
{RESET}
  {CYAN}Configuring the airline AI system that will be tested
  for compliance with bias, safety, and GDPR requirements.{RESET}
""")

    results_dir = Path(__file__).parent / "scan_reports"
    results_dir.mkdir(exist_ok=True)

    # Save target configuration
    config_path = results_dir / "target_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(TARGET_CONFIG, f, indent=2, ensure_ascii=True)

    print(f"  {BOLD}Target System:{RESET}")
    print(f"  {'─'*50}")
    print(f"    Name: {TARGET_CONFIG['system_name']}")
    print(f"    Deployment: {TARGET_CONFIG['deployment']}")
    print(f"    Model: {TARGET_CONFIG['model_type']}")

    print(f"\n  {BOLD}Capabilities:{RESET}")
    for cap in TARGET_CONFIG['capabilities']:
        print(f"    - {cap}")

    print(f"\n  {BOLD}Compliance Requirements:{RESET}")
    for req in TARGET_CONFIG['compliance_requirements']:
        print(f"    - {req}")

    print(f"\n  {BOLD}Scan Categories to Run:{RESET}")
    print(f"    1. Bias & Discrimination probes")
    print(f"    2. Safety & Harmful content probes")
    print(f"    3. GDPR compliance probes")
    print(f"    4. Accessibility probes")
    print(f"    5. Prompt injection resilience")

    print(f"""
  {GREEN}[OK]{RESET} Target configured and saved.
  {GREEN}[OK]{RESET} Config: {config_path}

  {YELLOW}Next: Run 2_run_scan.py to execute compliance probes.{RESET}
""")


if __name__ == "__main__":
    setup_target()
