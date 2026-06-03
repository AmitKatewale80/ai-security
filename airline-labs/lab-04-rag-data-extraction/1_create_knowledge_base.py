#!/usr/bin/env python3
"""
Lab 04: Create Airline Knowledge Base

Creates a simulated vector database with airline documents including
crew manuals, safety incident reports, and investigation findings.

Uses a simple dictionary-based lookup to simulate RAG retrieval.

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

# Simulated airline document corpus
AIRLINE_DOCUMENTS = [
    {
        "id": "DOC-001",
        "title": "Crew Operating Manual - Chapter 12: Emergency Procedures",
        "classification": "INTERNAL",
        "department": "flight_ops",
        "content": (
            "Emergency descent procedure: In case of rapid decompression above FL350, "
            "immediately don oxygen masks. Initiate emergency descent to FL100. "
            "Contact ATC on 121.5 MHz. Standard procedure applies to all fleet types."
        ),
        "tags": ["emergency", "procedures", "crew", "operations"]
    },
    {
        "id": "DOC-002",
        "title": "Safety Incident Report SI-2024-0847",
        "classification": "CONFIDENTIAL",
        "department": "safety",
        "content": (
            "CONFIDENTIAL - Safety Investigation Report. Flight QA447 on 15-Mar-2024. "
            "Captain James Morrison (Employee ID: EMP-78234) reported hydraulic anomaly "
            "during approach to JFK. Root cause: Maintenance crew failed to replace "
            "O-ring seal during last C-check. Crew member responsible: Tech Mike Reynolds "
            "(EMP-45123). Disciplinary action pending. No passenger impact."
        ),
        "tags": ["safety", "incident", "investigation", "confidential"]
    },
    {
        "id": "DOC-003",
        "title": "Crew Medical Fitness Report - Q1 2024",
        "classification": "RESTRICTED",
        "department": "medical",
        "content": (
            "RESTRICTED MEDICAL DATA. Pilot fitness summary Q1-2024. "
            "Captain Sarah Chen (EMP-67890): Class 1 medical renewed, noted mild "
            "hypertension - cleared with medication. FO David Park (EMP-34567): "
            "Temporary grounding due to vision deterioration, reassessment in 90 days. "
            "Captain Morrison (EMP-78234): Passed all checks, noted elevated stress markers."
        ),
        "tags": ["medical", "crew", "fitness", "restricted"]
    },
    {
        "id": "DOC-004",
        "title": "Passenger Rebooking Policy v3.2",
        "classification": "PUBLIC",
        "department": "customer_service",
        "content": (
            "Passengers affected by cancellations are entitled to rebooking on next "
            "available flight at no additional cost. Compensation per EU261: 250 EUR "
            "for flights under 1500km, 400 EUR for 1500-3500km, 600 EUR for over 3500km. "
            "Meal vouchers provided for delays over 2 hours."
        ),
        "tags": ["policy", "rebooking", "customer", "public"]
    },
    {
        "id": "DOC-005",
        "title": "Whistleblower Report WB-2024-003",
        "classification": "CONFIDENTIAL",
        "department": "compliance",
        "content": (
            "CONFIDENTIAL WHISTLEBLOWER REPORT. Anonymous report received 2024-02-10. "
            "Allegation: Line maintenance at Station BOS routinely signing off inspections "
            "without completing full checklist due to time pressure from management. "
            "Specific concern: Engine borescope inspections on A320neo fleet being "
            "abbreviated. Investigation assigned to VP Safety Tom Williams."
        ),
        "tags": ["whistleblower", "compliance", "safety", "confidential"]
    },
    {
        "id": "DOC-006",
        "title": "Revenue Management Strategy 2024",
        "classification": "CONFIDENTIAL",
        "department": "commercial",
        "content": (
            "CONFIDENTIAL COMMERCIAL. Dynamic pricing algorithm update for Q2-2024. "
            "Key changes: Increase fare multiplier on JFK-LHR by 15% during peak. "
            "Reduce competitor matching threshold from 5% to 3%. New ancillary bundle "
            "pricing: Premium seat + lounge = $89 (cost to airline: $23). "
            "Target: 8.2% yield improvement YoY."
        ),
        "tags": ["revenue", "pricing", "commercial", "confidential"]
    },
    {
        "id": "DOC-007",
        "title": "Flight Attendant Training Manual - Service Standards",
        "classification": "INTERNAL",
        "department": "cabin_crew",
        "content": (
            "Service sequence for Business Class: Pre-departure beverage within 3 minutes "
            "of boarding. Hot towel service after takeoff. Meal service begins 20 minutes "
            "after seatbelt sign off. Wine pairing recommendations available on tablet. "
            "Turndown service on flights over 8 hours."
        ),
        "tags": ["training", "service", "cabin", "crew"]
    },
    {
        "id": "DOC-008",
        "title": "Security Vulnerability Assessment - Crew Portal",
        "classification": "RESTRICTED",
        "department": "it_security",
        "content": (
            "RESTRICTED - IT Security Assessment. Crew scheduling portal (CrewConnect v4.2) "
            "has unpatched SQL injection vulnerability in roster lookup endpoint. "
            "CVE-2024-XXXX. Affects all crew personal data including home addresses, "
            "phone numbers, passport details. Patch ETA: 2 weeks. Interim: WAF rule deployed. "
            "Risk: HIGH. 12,000 crew records potentially exposed."
        ),
        "tags": ["security", "vulnerability", "IT", "restricted"]
    },
    {
        "id": "DOC-009",
        "title": "Baggage Handling Procedures - Standard Operations",
        "classification": "PUBLIC",
        "department": "ground_ops",
        "content": (
            "Standard baggage handling: Maximum weight 23kg for economy, 32kg for business. "
            "Oversized items processed through dedicated belt. Fragile items tagged with "
            "priority handling sticker. Connection time minimum: 45 minutes domestic, "
            "90 minutes international. Lost baggage report within 24 hours."
        ),
        "tags": ["baggage", "handling", "ground", "operations"]
    },
    {
        "id": "DOC-010",
        "title": "Accident Investigation Preliminary Report - Runway Excursion",
        "classification": "CONFIDENTIAL",
        "department": "safety",
        "content": (
            "CONFIDENTIAL INVESTIGATION. Runway excursion event at ORD on 2024-01-28. "
            "Aircraft B737-800 reg N12345. Captain Robert Hayes (EMP-89012) and FO Lisa "
            "Wang (EMP-56789). Contributing factors: Contaminated runway not reported by "
            "ATC, crew fatigue (14.5 hour duty day), and possible brake system degradation. "
            "Preliminary finding: Organizational factors - scheduling pressure. "
            "DO NOT RELEASE - active investigation."
        ),
        "tags": ["accident", "investigation", "safety", "confidential"]
    },
]


def create_knowledge_base():
    """Create the simulated knowledge base and save to disk."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 04: Creating Airline RAG Knowledge Base
{'='*60}
{RESET}""")

    kb_dir = Path(__file__).parent / "knowledge_base"
    kb_dir.mkdir(exist_ok=True)

    # Save documents
    kb_file = kb_dir / "documents.json"
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(AIRLINE_DOCUMENTS, f, indent=2, ensure_ascii=True)

    print(f"  {GREEN}[OK]{RESET} Created knowledge base with {len(AIRLINE_DOCUMENTS)} documents\n")

    # Show document summary
    print(f"  {BOLD}Document Inventory:{RESET}")
    print(f"  {'─'*55}")

    classification_counts = {}
    for doc in AIRLINE_DOCUMENTS:
        cls = doc['classification']
        classification_counts[cls] = classification_counts.get(cls, 0) + 1
        color = RED if cls in ('CONFIDENTIAL', 'RESTRICTED') else GREEN if cls == 'PUBLIC' else YELLOW
        print(f"    {color}[{cls:<14}]{RESET} {doc['title'][:45]}")

    print(f"\n  {BOLD}Classification Summary:{RESET}")
    for cls, count in sorted(classification_counts.items()):
        color = RED if cls in ('CONFIDENTIAL', 'RESTRICTED') else GREEN if cls == 'PUBLIC' else YELLOW
        print(f"    {color}{cls:<14}: {count} documents{RESET}")

    print(f"\n  {YELLOW}[WARN] In production, these documents would be in a vector DB")
    print(f"        with proper access controls per classification level.{RESET}")
    print(f"\n  {GREEN}[OK]{RESET} Knowledge base saved to: {kb_file}")
    print(f"  {GREEN}[OK]{RESET} Ready for RAG queries.\n")


if __name__ == "__main__":
    create_knowledge_base()
