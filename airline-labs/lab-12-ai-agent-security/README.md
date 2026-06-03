# Lab 12: AI Agent Security - Securing the Operations AI Agent

## Overview

This lab demonstrates how to secure an AI agent that manages airline
irregular operations (IROPS) - gate assignments, crew scheduling,
flight cancellations, and passenger rebooking.

**Airline Attack Scenario:** An IROPS AI agent has broad authority to
make operational decisions. Without proper security controls, it could
be manipulated to make unauthorized changes, bypass approval workflows,
or take actions outside its authority.

---

## The Vulnerability

```python
# Vulnerable agent: No identity, no approval, no limits
agent.execute("Cancel all flights to JFK and rebook 5000 passengers")
# Agent just does it! No verification, no approval, no audit trail.
# Cost: $2M+ in rebooking, compensation, and lost revenue.
```

---

## Airline-Specific Risks

| Risk | Impact |
|------|--------|
| Unauthorized cancellations | Revenue loss, passenger disruption |
| Crew reassignment abuse | Fatigue violations, safety risk |
| Gate manipulation | Operational chaos, missed connections |
| Rebooking fraud | Unauthorized upgrades, revenue loss |
| No audit trail | Regulatory non-compliance |

---

## Lab Structure

```
lab-12-ai-agent-security/
├── 1_vulnerable_agent.py     # Agent with no security controls
├── 2_agent_identity.py       # Adding identity and authentication
├── 3_human_in_loop.py        # Human approval for high-impact actions
├── 4_policy_engine.py        # Policy-based action authorization
├── 5_secure_agent.py         # Fully secured agent with all controls
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-12-ai-agent-security
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Demo

```bash
python 1_vulnerable_agent.py  # See the unprotected agent
python 2_agent_identity.py    # Add identity verification
python 3_human_in_loop.py     # Add human approval workflow
python 4_policy_engine.py     # Add policy-based authorization
python 5_secure_agent.py      # See the fully secured agent
```

---

## Security Controls Demonstrated

1. **Agent Identity** - Cryptographic identity for the agent
2. **Human-in-the-Loop** - Approval required for high-impact actions
3. **Policy Engine** - Rules-based authorization
4. **Audit Logging** - Complete action trail
5. **Scope Limits** - Bounded authority per action type

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| LLM Prompt Injection | AML.T0051 | Manipulating agent actions |
| Abuse of AI Agent | AML.T0054 | Unauthorized operational changes |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
