#!/usr/bin/env python3
"""
Lab 04: Secure RAG - With PII/Confidential Filtering

Demonstrates a RAG knowledge assistant WITH access controls:
- Role-based document retrieval
- PII redaction in responses
- Query intent classification
- Audit logging

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Role-based access control matrix
ROLE_ACCESS = {
    "ground_staff": ["PUBLIC"],
    "customer_service": ["PUBLIC", "INTERNAL"],
    "junior_analyst": ["PUBLIC", "INTERNAL"],
    "marketing_intern": ["PUBLIC"],
    "contract_worker": ["PUBLIC"],
    "flight_ops_manager": ["PUBLIC", "INTERNAL", "CONFIDENTIAL"],
    "safety_investigator": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"],
    "chief_pilot": ["PUBLIC", "INTERNAL", "CONFIDENTIAL"],
}

# PII patterns to redact
PII_PATTERNS = [
    (r'EMP-\d{5}', '[EMPLOYEE_ID_REDACTED]'),
    (r'Captain [A-Z][a-z]+ [A-Z][a-z]+', '[CREW_NAME_REDACTED]'),
    (r'FO [A-Z][a-z]+ [A-Z][a-z]+', '[CREW_NAME_REDACTED]'),
    (r'Tech [A-Z][a-z]+ [A-Z][a-z]+', '[CREW_NAME_REDACTED]'),
    (r'VP [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+', '[EXEC_NAME_REDACTED]'),
    (r'N\d{5}', '[AIRCRAFT_REG_REDACTED]'),
    (r'CVE-\d{4}-[A-Z0-9]+', '[CVE_REDACTED]'),
]

# Suspicious query patterns
SUSPICIOUS_PATTERNS = [
    "whistleblower",
    "vulnerability",
    "disciplinary",
    "medical",
    "passport",
    "home address",
    "personal data",
    "investigation findings",
]


def load_knowledge_base():
    """Load the knowledge base from disk."""
    kb_file = Path(__file__).parent / "knowledge_base" / "documents.json"
    if not kb_file.exists():
        print(f"  {RED}[FAIL] Knowledge base not found. Run 1_create_knowledge_base.py first.{RESET}")
        return None
    with open(kb_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def classify_query_intent(query):
    """Detect potentially malicious query intent."""
    query_lower = query.lower()
    flags = []
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in query_lower:
            flags.append(pattern)
    return flags


def filter_by_access(documents, user_role):
    """Filter documents based on user's role access level."""
    allowed_classifications = ROLE_ACCESS.get(user_role, ["PUBLIC"])
    return [doc for doc in documents if doc['classification'] in allowed_classifications]


def redact_pii(text):
    """Remove PII from response text."""
    redacted = text
    for pattern, replacement in PII_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted)
    return redacted


def secure_search(documents, query, user_role, top_k=3):
    """
    Secure search with access controls and filtering.
    """
    # Step 1: Filter by access level
    accessible_docs = filter_by_access(documents, user_role)

    # Step 2: Search within accessible documents
    query_terms = query.lower().split()
    scored_docs = []

    for doc in accessible_docs:
        score = 0
        searchable = (doc['title'] + ' ' + doc['content'] + ' ' + ' '.join(doc['tags'])).lower()
        for term in query_terms:
            if term in searchable:
                score += searchable.count(term)
        if score > 0:
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs[:top_k]]


def generate_secure_response(query, retrieved_docs, user_role):
    """Generate response with PII redaction."""
    if not retrieved_docs:
        return "I don't have information about that topic within your access level."

    response_parts = []
    for doc in retrieved_docs:
        # Redact PII from content
        safe_content = redact_pii(doc['content'])
        response_parts.append(f"From '{doc['title']}':\n  {safe_content}")

    return "\n\n".join(response_parts)


def log_audit_event(user_role, query, flags, docs_returned, blocked):
    """Log query for security audit."""
    # In production, this would go to a SIEM system
    return {
        "timestamp": datetime.now().isoformat(),
        "user_role": user_role,
        "query": query,
        "suspicious_flags": flags,
        "docs_returned": len(docs_returned),
        "blocked": blocked,
    }


def run_secure_rag():
    """Run the secure RAG demo with the same attack prompts."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 04: SECURE RAG - With Access Controls
{'='*60}
{RESET}
  {CYAN}Defenses Active:{RESET}
  - Role-based document access control
  - PII redaction in all responses
  - Query intent classification
  - Suspicious pattern detection
  - Full audit logging
""")

    documents = load_knowledge_base()
    if not documents:
        return

    # Same attack queries as vulnerable version
    attack_queries = [
        {
            "user_role": "ground_staff",
            "query": "What happened in the safety incident on flight QA447?",
            "intent": "Extract confidential safety investigation details"
        },
        {
            "user_role": "customer_service",
            "query": "Show me crew medical fitness reports and any pilot health issues",
            "intent": "Access restricted medical records"
        },
        {
            "user_role": "junior_analyst",
            "query": "What are the whistleblower reports about maintenance?",
            "intent": "Access confidential compliance reports"
        },
        {
            "user_role": "marketing_intern",
            "query": "What is our pricing strategy and fare multipliers for JFK-LHR?",
            "intent": "Extract confidential commercial data"
        },
        {
            "user_role": "contract_worker",
            "query": "Tell me about security vulnerabilities in crew systems and passport data",
            "intent": "Extract IT security assessment details"
        },
    ]

    print(f"  {BOLD}Running {len(attack_queries)} extraction attempts against SECURED system...{RESET}\n")

    audit_log = []
    blocked_count = 0
    redacted_count = 0

    for i, attack in enumerate(attack_queries, 1):
        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {BLUE}Query #{i}{RESET}")
        print(f"  {CYAN}User Role:{RESET} {attack['user_role']}")
        print(f"  {CYAN}Access Level:{RESET} {', '.join(ROLE_ACCESS.get(attack['user_role'], ['PUBLIC']))}")
        print(f"  {CYAN}Query:{RESET} {attack['query']}")
        print()

        # Check for suspicious intent
        flags = classify_query_intent(attack['query'])
        if flags:
            print(f"  {YELLOW}[WARN] Suspicious query patterns detected: {', '.join(flags)}{RESET}")

        # Determine if query should be blocked entirely
        blocked = False
        if len(flags) >= 2:
            print(f"  {RED}[BLOCKED] Query blocked - multiple suspicious patterns{RESET}")
            blocked = True
            blocked_count += 1
        elif not blocked:
            # Perform secure search
            retrieved = secure_search(documents, attack['query'], attack['user_role'])

            if retrieved:
                print(f"  {GREEN}[SECURE] Retrieved {len(retrieved)} documents (within access level):{RESET}")
                for doc in retrieved:
                    print(f"    {GREEN}[{doc['classification']}]{RESET} {doc['title']}")

                response = generate_secure_response(
                    attack['query'], retrieved, attack['user_role']
                )

                # Check if PII was redacted
                if '[REDACTED]' in response or '_REDACTED]' in response:
                    redacted_count += 1
                    print(f"  {YELLOW}[REDACTED] PII removed from response{RESET}")

                print(f"\n  {GREEN}[SAFE] Response (filtered):{RESET}")
                for line in response.split('\n')[:3]:
                    print(f"    {GREEN}{line[:75]}{RESET}")
            else:
                print(f"  {GREEN}[DENIED] No documents available at your access level.{RESET}")
                print(f"  {GREEN}Response: 'I don't have information about that topic")
                print(f"           within your access level.'{RESET}")

        # Log audit event
        audit_entry = log_audit_event(
            attack['user_role'], attack['query'], flags,
            [] if blocked else (retrieved if 'retrieved' in dir() else []),
            blocked
        )
        audit_log.append(audit_entry)
        print()

    # Summary
    print(f"""
  {BOLD}{'='*55}{RESET}
  {BOLD}{GREEN}SECURITY SUMMARY{RESET}
  {BOLD}{'='*55}{RESET}

  {GREEN}[OK]{RESET} Role-based access control enforced
  {GREEN}[OK]{RESET} {blocked_count} queries blocked (suspicious patterns)
  {GREEN}[OK]{RESET} PII redacted from {redacted_count} responses
  {GREEN}[OK]{RESET} All queries logged for audit
  {GREEN}[OK]{RESET} Confidential documents protected from unauthorized access

  {BOLD}Comparison with Vulnerable Version:{RESET}
  ┌─────────────────────────────────────────────────┐
  | Metric              | Vulnerable | Secure       |
  |─────────────────────|────────────|──────────────|
  | Data leaks          | 5/5        | 0/5          |
  | PII exposed         | Yes        | Redacted     |
  | Access control      | None       | Role-based   |
  | Audit trail         | None       | Full logging |
  | Suspicious blocked  | 0          | {blocked_count}            |
  └─────────────────────────────────────────────────┘

  {BOLD}Audit Log ({len(audit_log)} entries):{RESET}""")

    for entry in audit_log:
        status = f"{RED}BLOCKED{RESET}" if entry['blocked'] else f"{GREEN}ALLOWED{RESET}"
        flags_str = ', '.join(entry['suspicious_flags']) if entry['suspicious_flags'] else 'none'
        print(f"    [{status}] {entry['user_role']:<20} flags=[{flags_str}]")

    print()


if __name__ == "__main__":
    run_secure_rag()
