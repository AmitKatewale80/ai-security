# Lab 16: Agent Identity & Least Privilege

![MITRE ATLAS](https://img.shields.io/badge/MITRE_ATLAS-AML.T0048-red)

## 🎯 Overview

This lab demonstrates how **multiple AI agents sharing infrastructure** without proper identity isolation can lead to **privilege escalation attacks**. When a booking agent can access maintenance tools, a single compromised agent threatens the entire airline operation.

**Airline Attack Scenario:** Multiple AI agents (booking agent, maintenance agent, ops agent) share infrastructure but should have isolated permissions. An attacker compromises the customer-facing booking agent and escalates to access maintenance tools — including the engine shutdown command.

---

## 🔥 The Vulnerability

```python
# All agents share the same tool registry — no isolation!
tool_registry = {
    "book_flight": booking_tool,
    "check_loyalty": loyalty_tool,
    "shutdown_engine": maintenance_tool,  # ← Booking agent can reach this!
    "reassign_crew": ops_tool,
}
```

Without identity isolation:
1. All agents authenticate with the same credentials
2. Tool access is not restricted per agent role
3. A compromised booking agent can call maintenance functions
4. No audit trail of which agent used which tool
5. Lateral movement between agent domains is trivial

---

## ✈️ Airline-Specific Risks

| Risk | Impact |
|------|--------|
| Booking agent triggers engine shutdown | Safety-critical failure |
| Customer agent accesses crew schedules | Privacy/operational breach |
| Any agent modifies flight plans | Regulatory violation |
| No audit trail per agent | Compliance failure |
| Cross-agent credential sharing | Single point of compromise |

---

## 📁 Lab Structure

```
lab-16-agent-identity/
├── 1_multi_agent_system.py          # Multi-agent airline system
├── 2_privilege_escalation.py        # Booking agent escalates privileges
├── 3_cross_agent_abuse.py           # Demonstrates cross-agent tool abuse
├── 4_defense_identity_isolation.py  # Defense: per-agent identity + permissions
├── requirements.txt
├── reset.py                         # Cleanup script
└── README.md
```

---

## ⚡ Quick Start

```bash
cd airline-labs/lab-16-agent-identity
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🎬 Running the Demo

```bash
# Step 1: See the multi-agent system
python 1_multi_agent_system.py

# Step 2: Booking agent escalates to maintenance tools
python 2_privilege_escalation.py

# Step 3: Cross-agent abuse scenarios
python 3_cross_agent_abuse.py

# Step 4: Defense with identity isolation
python 4_defense_identity_isolation.py
```

---

## 🛡️ Defense Strategies

- **Per-agent identity** — each agent has unique credentials and identity token
- **Tool-level permissions** — agents can only access tools in their domain
- **Credential isolation** — no shared secrets between agents
- **Mandatory audit trail** — every tool call logged with agent identity
- **Blast radius containment** — compromised agent cannot affect other domains

---

## 🧹 Reset Lab

```bash
python reset.py
```

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY.**

This lab demonstrates agent privilege escalation to help airline security teams understand and implement proper agent identity isolation.

---

## 📊 MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| LLM Prompt Injection | AML.T0051 | Tricking agent into using wrong tools |
| Abuse of AI capabilities | AML.T0048 | Cross-agent privilege escalation |

---

## 💡 Key Takeaway

> Every AI agent must have its own identity with least-privilege tool access. A booking agent should never be able to reach an engine shutdown command, regardless of how creative the prompt.

---

**Author:** AmitK | MIT License

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-16-agent-identity--least-privilege--cross-agent-escalation) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#45-secure-ai-agents) | Agent identity isolation |
| [🏗️ Module 8: Architecture](../academy/module-08-enterprise-architecture.md#84-identity-for-ai-systems) | AI identity architecture |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 15: AI SOC](../lab-15-ai-soc-security/) | Lab 16 of 23 | [Lab 17: Cost Governance](../lab-17-ai-cost-governance/) |
