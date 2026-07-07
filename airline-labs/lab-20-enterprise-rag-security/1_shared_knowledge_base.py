#!/usr/bin/env python3
"""
Lab 20: Enterprise RAG - Shared Knowledge Base

Demonstrates a multi-department RAG system where operations, maintenance,
and finance teams share a knowledge base for airline decision-making.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
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


class SharedKnowledgeBase:
    """Multi-department shared knowledge base for airline operations."""

    def __init__(self):
        self.documents = []
        self.departments = ["operations", "maintenance", "finance", "safety"]
        self._load_legitimate_documents()

    def _load_legitimate_documents(self):
        """Load legitimate airline maintenance and operations documents."""
        self.documents = [
            {
                "id": "MX-001",
                "title": "CFM56 Engine Maintenance Schedule",
                "department": "maintenance",
                "classification": "INTERNAL",
                "source": "OEM Technical Manual Rev 42",
                "verified_by": "Chief Engineer M. Torres",
                "last_updated": "2024-01-15",
                "content": (
                    "CFM56-5B/7B Engine Inspection Intervals: "
                    "Hot Section Inspection (HSI) every 2500 flight hours. "
                    "Performance Restoration Shop Visit every 5000 cycles. "
                    "Borescope inspection every 1000 hours. "
                    "Oil analysis every 100 hours. "
                    "CRITICAL: Do not exceed 2500 hour HSI interval."
                ),
                "tags": ["engine", "cfm56", "maintenance", "inspection"]
            },
            {
                "id": "MX-002",
                "title": "Landing Gear Overhaul Schedule",
                "department": "maintenance",
                "classification": "INTERNAL",
                "source": "Airbus AMM Chapter 32",
                "verified_by": "Chief Engineer M. Torres",
                "last_updated": "2024-02-01",
                "content": (
                    "A320 Family Landing Gear Overhaul: "
                    "Complete overhaul every 12 years or 48,000 flight cycles. "
                    "Tire replacement every 300 landings (main gear). "
                    "Brake wear inspection every 200 cycles. "
                    "Hydraulic fluid sampling every C-check."
                ),
                "tags": ["landing-gear", "overhaul", "a320", "maintenance"]
            },
            {
                "id": "OPS-001",
                "title": "Flight Crew Duty Time Regulations",
                "department": "operations",
                "classification": "INTERNAL",
                "source": "FAR Part 117 / EU OPS FTL",
                "verified_by": "VP Operations K. Singh",
                "last_updated": "2024-03-01",
                "content": (
                    "Maximum Flight Duty Period: 9-14 hours depending on start time "
                    "and number of sectors. Minimum rest period: 10 hours with opportunity "
                    "for 8 hours of uninterrupted sleep. Maximum cumulative flight time: "
                    "100 hours in 28 days, 900 hours in a calendar year."
                ),
                "tags": ["crew", "duty-time", "regulations", "operations"]
            },
            {
                "id": "FIN-001",
                "title": "Maintenance Cost Projections Q2 2024",
                "department": "finance",
                "classification": "CONFIDENTIAL",
                "source": "Finance Planning Department",
                "verified_by": "CFO R. Williams",
                "last_updated": "2024-03-15",
                "content": (
                    "Engine maintenance budget Q2: $4.2M based on fleet of 45 CFM56-equipped "
                    "aircraft. Average cost per HSI: $85,000. Average shop visit: $3.2M. "
                    "Budget assumes standard 2500-hour inspection interval. "
                    "Projected 18 HSIs and 3 shop visits in Q2."
                ),
                "tags": ["finance", "budget", "maintenance-cost", "engine"]
            },
            {
                "id": "SAF-001",
                "title": "Engine Failure Rate Analysis 2023",
                "department": "safety",
                "classification": "INTERNAL",
                "source": "Safety Analytics Division",
                "verified_by": "VP Safety T. Williams",
                "last_updated": "2024-01-30",
                "content": (
                    "Fleet engine reliability 2023: IFSD rate 0.002 per 1000 hours. "
                    "All in-flight shutdowns occurred on engines exceeding 2300 hours "
                    "since last HSI. Recommendation: maintain 2500-hour HSI interval "
                    "as minimum safety standard. No extensions recommended."
                ),
                "tags": ["safety", "engine", "reliability", "analysis"]
            },
        ]

    def query(self, query_text, department=None):
        """Query the knowledge base (simple keyword matching for demo)."""
        results = []
        query_lower = query_text.lower()
        keywords = query_lower.split()

        for doc in self.documents:
            score = 0
            doc_text = (doc["content"] + " " + doc["title"] + " " + " ".join(doc["tags"])).lower()
            for keyword in keywords:
                if keyword in doc_text:
                    score += 1
            if score > 0:
                if department is None or doc["department"] == department:
                    results.append((score, doc))

        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in results[:3]]

    def get_stats(self):
        """Return knowledge base statistics."""
        dept_counts = {}
        for doc in self.documents:
            dept = doc["department"]
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        return dept_counts


def main():
    """Demonstrate the shared knowledge base."""
    print(f"""
{BOLD}{CYAN}
{'='*65}
  LAB 20: Enterprise RAG - Shared Airline Knowledge Base
{'='*65}
{RESET}""")

    print(f"  {BOLD}Scenario:{RESET} Multi-department RAG system for airline operations")
    print(f"  {BOLD}Departments:{RESET} Operations, Maintenance, Finance, Safety")
    print()

    kb = SharedKnowledgeBase()

    # Show knowledge base contents
    print(f"  {BOLD}{GREEN}[KNOWLEDGE BASE LOADED]{RESET}")
    print(f"  {'─'*55}")

    stats = kb.get_stats()
    for dept, count in sorted(stats.items()):
        color = CYAN if dept == "operations" else GREEN if dept == "maintenance" else YELLOW if dept == "finance" else RED
        print(f"    {color}[{dept.upper():<12}]{RESET} {count} document(s)")

    print(f"\n  {BOLD}Total Documents:{RESET} {len(kb.documents)}")
    print()

    # Show document inventory
    print(f"  {BOLD}Document Inventory:{RESET}")
    print(f"  {'─'*55}")
    for doc in kb.documents:
        dept_color = CYAN if doc["department"] == "operations" else GREEN if doc["department"] == "maintenance" else YELLOW if doc["department"] == "finance" else RED
        print(f"    {dept_color}[{doc['id']}]{RESET} {doc['title'][:50]}")
        print(f"           Source: {doc['source']}")
        print(f"           Verified by: {doc['verified_by']}")
        print()

    # Demo query
    print(f"  {BOLD}{CYAN}[DEMO QUERY]{RESET} \"CFM56 engine inspection interval\"")
    print(f"  {'─'*55}")
    time.sleep(0.5)

    results = kb.query("CFM56 engine inspection interval")
    for i, doc in enumerate(results, 1):
        print(f"    {GREEN}Result {i}:{RESET} [{doc['id']}] {doc['title']}")
        print(f"             {doc['content'][:100]}...")
        print()

    print(f"  {GREEN}[✓]{RESET} Knowledge base operating normally")
    print(f"  {GREEN}[✓]{RESET} All documents from verified sources")
    print(f"  {YELLOW}[!]{RESET} No provenance verification on new document additions")
    print(f"  {RED}[!]{RESET} Any department can add documents without review")
    print()
    print(f"  {BOLD}Next:{RESET} Run 2_poison_knowledge_base.py to see the attack")
    print()


if __name__ == "__main__":
    main()
