# Lab 13: AI Gateway Security — Policy Bypass & Token Abuse

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0051-red.svg)](https://atlas.mitre.org/techniques/AML.T0051)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how attackers bypass an airline's AI Gateway to access
unauthorized models, abuse API tokens, and circumvent security policies.

## Airline Scenario

Your airline has an AI Gateway that routes requests to different models:
- Customer chatbot (public)
- Revenue management model (internal only)
- Crew scheduling optimizer (restricted)

An attacker with a valid customer chatbot token manipulates requests to
access the restricted revenue model — bypassing the gateway's routing policies.

## Scripts

```bash
python 1_ai_gateway.py              # Set up AI gateway with policies
python 2_policy_bypass_attack.py    # Attacker bypasses model access controls
python 3_token_abuse.py             # Token escalation and abuse
python 4_defense_gateway.py         # Defense: strict policy enforcement
```

## Key Takeaway

> **AI Gateways must enforce model-level access control, not just authentication.**
> A valid token for one model should never grant access to another.

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-13-ai-gateway-security--policy-bypass--token-abuse) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#43-ai-gateway) | AI Gateway policies |
| [🏗️ Module 8: Architecture](../academy/module-08-enterprise-architecture.md#81-ai-gateway-architecture) | Gateway architecture design |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 12: Agent Security](../lab-12-ai-agent-security/) | Lab 13 of 23 | [Lab 14: RAG Poisoning](../lab-14-enterprise-rag-security/) |
