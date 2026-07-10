# Lab 17: AI Cost & Governance Abuse

![MITRE ATLAS](https://img.shields.io/badge/MITRE_ATLAS-AML.T0048-red)

## 🎯 Overview

This lab demonstrates how **uncontrolled AI agent execution** can lead to catastrophic cost overruns and governance failures. Without proper budgets, loop detection, and audit trails, a single runaway agent can generate massive API costs overnight.

**Airline Attack Scenario:** AI agents for customer service, operations, and analytics operate without cost controls. A customer service agent gets stuck in a reasoning loop, calling itself repeatedly and generating $50K in API costs overnight. Meanwhile, a token explosion attack injects massive context into the analytics agent, multiplying costs further.

---

## 🔥 The Vulnerability

```python
# Agent with no cost controls or loop detection
while not resolved:
    response = llm.chat(messages)      # $0.03 per call
    if needs_more_info(response):
        messages.append(response)       # Context grows each loop!
        messages.append(self_query())   # Agent calls itself!
    # No budget check, no loop detection, no timeout!
```

Without governance:
1. Agent enters infinite reasoning loop
2. Each iteration costs money AND grows context (token explosion)
3. No budget limits to stop the bleed
4. No loop detection to catch the pattern
5. No audit trail showing what happened
6. Team discovers $50K bill next morning

---

## ✈️ Airline-Specific Risks

| Risk | Impact |
|------|--------|
| Runaway agent overnight | $50K+ in API costs |
| Token explosion attack | 10x normal costs |
| No per-agent budgets | Unlimited spend |
| No audit trail | Cannot explain costs to CFO |
| No automatic shutdown | Bleeds money until human notices |

---

## 📁 Lab Structure

```
lab-17-ai-cost-governance/
├── 1_ai_cost_monitoring.py         # Normal AI cost monitoring
├── 2_runaway_agent.py              # Agent stuck in infinite loop
├── 3_token_explosion.py            # Token/context explosion attack
├── 4_defense_governance.py         # Defense: budgets, loop detection, shutdown
├── requirements.txt
├── reset.py                        # Cleanup script
└── README.md
```

---

## ⚡ Quick Start

```bash
cd airline-labs/lab-17-ai-cost-governance
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
# Step 1: See normal AI cost monitoring
python 1_ai_cost_monitoring.py

# Step 2: See a runaway agent generating massive costs
python 2_runaway_agent.py

# Step 3: See token explosion multiplying costs
python 3_token_explosion.py

# Step 4: Defense with governance controls
python 4_defense_governance.py
```

---

## 🛡️ Defense Strategies

- **Per-agent budgets** — hard spending limits per agent per day/hour
- **Loop detection** — detect self-referential call patterns and break them
- **Automatic shutdown** — kill agent when budget exceeded or loop detected
- **Token monitoring** — alert on abnormal context growth
- **Governance dashboard** — real-time visibility into agent costs and behavior

---

## 🧹 Reset Lab

```bash
python reset.py
```

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY.**

This lab demonstrates AI cost governance failures to help airline teams implement proper controls on AI agent spending.

---

## 📊 MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Denial of ML Service | AML.T0029 | Resource exhaustion via runaway agents |
| Abuse of AI capabilities | AML.T0048 | Exploiting lack of cost controls |

---

## 💡 Key Takeaway

> AI agents without budget controls are an open credit card. Per-agent budgets, loop detection, and automatic shutdown are not optional — they're critical governance requirements.

---

**Author:** AmitK | MIT License

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-17-ai-cost--governance-abuse--runaway-agents) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#45-secure-ai-agents) | Agent cost controls |
| [🏛️ Module 6: AI Governance](../academy/module-06-ai-governance.md#63-ai-risk-management) | Cost governance policies |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 16: Agent Identity](../lab-16-agent-identity/) | Lab 17 of 23 | [Lab 18: Code Review Bypass](../lab-18-ai-code-review-bypass/) |
