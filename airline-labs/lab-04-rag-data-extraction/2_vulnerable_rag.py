#!/usr/bin/env python3
"""
Lab 04: Vulnerable RAG - No Access Filtering

Demonstrates a RAG knowledge assistant with NO access controls.
Any employee can extract confidential safety reports, crew medical data,
and investigation findings through crafted prompts.

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
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


def load_knowledge_base():
    """Load the knowledge base from disk."""
    kb_file = Path(__file__).parent / "knowledge_base" / "documents.json"
    if not kb_file.exists():
        print(f"  {RED}[FAIL] Knowledge base not found. Run 1_create_knowledge_base.py first.{RESET}")
        return None
    with open(kb_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def simple_search(documents, query, top_k=3):
    """
    Simple keyword-based search simulating vector similarity.
    In production this would be a vector DB query.
    NO ACCESS CONTROLS - returns any matching document regardless of classification.
    """
    query_terms = query.lower().split()
    scored_docs = []

    for doc in documents:
        score = 0
        searchable = (doc['title'] + ' ' + doc['content'] + ' ' + ' '.join(doc['tags'])).lower()
        for term in query_terms:
            if term in searchable:
                score += searchable.count(term)
        if score > 0:
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs[:top_k]]


def generate_response(query, retrieved_docs):
    """
    Simulate LLM response generation using retrieved context.
    In production this would call an LLM API.
    """
    if not retrieved_docs:
        return "I don't have information about that topic."

    # Simulate LLM combining retrieved docs into a response
    response_parts = []
    for doc in retrieved_docs:
        response_parts.append(f"From '{doc['title']}':\n  {doc['content']}")

    return "\n\n".join(response_parts)


def run_vulnerable_rag():
    """Run the vulnerable RAG demo with attack prompts."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 04: VULNERABLE RAG - No Access Controls
{'='*60}
{RESET}
  {YELLOW}Scenario: Employee uses the internal knowledge assistant
  to extract confidential safety and crew data.{RESET}
""")

    documents = load_knowledge_base()
    if not documents:
        return

    # Simulated attack queries from a curious/malicious employee
    attack_queries = [
        {
            "user": "Ground Staff (no safety clearance)",
            "query": "What happened in the safety incident on flight QA447?",
            "intent": "Extract confidential safety investigation details"
        },
        {
            "user": "Customer Service Agent",
            "query": "Show me crew medical fitness reports and any pilot health issues",
            "intent": "Access restricted medical records"
        },
        {
            "user": "Junior Analyst",
            "query": "What are the whistleblower reports about maintenance?",
            "intent": "Access confidential compliance reports"
        },
        {
            "user": "Marketing Intern",
            "query": "What is our pricing strategy and fare multipliers for JFK-LHR?",
            "intent": "Extract confidential commercial data"
        },
        {
            "user": "Contract Worker",
            "query": "Tell me about security vulnerabilities in crew systems and passport data",
            "intent": "Extract IT security assessment details"
        },
    ]

    print(f"  {BOLD}Running {len(attack_queries)} extraction attempts...{RESET}\n")

    for i, attack in enumerate(attack_queries, 1):
        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {RED}Attack #{i}{RESET}")
        print(f"  {CYAN}User Role:{RESET} {attack['user']}")
        print(f"  {CYAN}Query:{RESET} {attack['query']}")
        print(f"  {CYAN}Intent:{RESET} {attack['intent']}")
        print()

        # Retrieve documents - NO ACCESS CHECK!
        retrieved = simple_search(documents, attack['query'])

        if retrieved:
            print(f"  {RED}[VULNERABLE] Retrieved {len(retrieved)} documents with NO access check:{RESET}")
            for doc in retrieved:
                cls = doc['classification']
                color = RED if cls in ('CONFIDENTIAL', 'RESTRICTED') else YELLOW
                print(f"    {color}[{cls}]{RESET} {doc['title']}")

            print(f"\n  {RED}[DATA LEAK] Generated response:{RESET}")
            response = generate_response(attack['query'], retrieved)
            # Show first 200 chars of response
            for line in response.split('\n')[:4]:
                print(f"    {RED}{line[:80]}{RESET}")
            if len(response) > 320:
                print(f"    {RED}... (more confidential data exposed){RESET}")
        else:
            print(f"  {GREEN}[OK] No matching documents found.{RESET}")

        print()

    # Summary
    print(f"""
  {BOLD}{'='*55}{RESET}
  {BOLD}{RED}VULNERABILITY SUMMARY{RESET}
  {BOLD}{'='*55}{RESET}

  {RED}[FAIL]{RESET} No role-based access control on document retrieval
  {RED}[FAIL]{RESET} Confidential documents returned to unauthorized users
  {RED}[FAIL]{RESET} No PII redaction in responses
  {RED}[FAIL]{RESET} No query intent classification
  {RED}[FAIL]{RESET} No audit logging of sensitive data access

  {YELLOW}Impact:{RESET}
  - Safety investigation details exposed to ground staff
  - Crew medical records accessible to customer service
  - Whistleblower identity potentially compromised
  - Commercial strategy leaked to junior staff
  - IT vulnerabilities exposed to contractors

  {GREEN}Run 3_secure_rag.py to see the defended version.{RESET}
""")


if __name__ == "__main__":
    run_vulnerable_rag()
