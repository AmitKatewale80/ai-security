# Lab 02: Stealing the Airline's Dynamic Pricing Engine

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0044-red.svg)](https://atlas.mitre.org/techniques/AML.T0044)
[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0024-red.svg)](https://atlas.mitre.org/techniques/AML.T0024)

**Author:** AmitK | [MIT License](../../labs/LICENSE)

> ⚠️ **Educational purposes only.** Do not use for malicious activities.

---

## Overview

This lab demonstrates how a **competitor airline** can clone your proprietary dynamic pricing algorithm by querying the Fare Quote API with thousands of fake flight searches. With just 3,000 queries, they can replicate ~90% of your pricing decisions.

**Business Impact:** $10-50M/year revenue loss on competitive routes.

---

## Airline Scenario

Your airline spent $5M+ developing a dynamic pricing engine that considers:
- Days to departure (urgency pricing)
- Current load factor (demand-based)
- Seasonality and day-of-week patterns
- Competitor fare monitoring
- Loyalty tier discounts
- Route distance and connection type

A competitor's bot queries your "Get Fare Quote" API with systematic combinations of routes, dates, and conditions. They train their own model on your responses and can now predict (and undercut) your fares on every route.

---

## Prerequisites

- Python 3.9+
- Flask, scikit-learn, pandas, numpy

---

## Setup

```bash
cd airline-labs/lab-02-model-stealing
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Quick Demo (Single Script - No Server Needed)

```bash
python run_demo.py
```

This runs the entire attack in ~30 seconds without needing two terminals.

---

## Full Demo (Two Terminals)

### Part A: Attack (Vulnerable API)

**Terminal 1:**
```bash
python 1_pricing_model.py       # Create proprietary pricing model
python 1b_api_server.py         # Start Fare Quote API (keep running)
```

**Terminal 2:**
```bash
python 2_query_attack.py        # Steal pricing via API queries
python 3_compare_models.py      # Measure theft accuracy (~90% fidelity)
```

### Part B: Defense (Secure API)

**Terminal 1:**
```bash
# Stop previous server (Ctrl+C), then:
python 4_secure_api_server.py   # Start SECURE Fare Quote API
```

**Terminal 2:**
```bash
python 2_query_attack.py        # Same attack, degraded results (~65%)
python 3_compare_models.py      # Verify defense effectiveness
```

### Clean Up
```bash
python reset.py
```

---

## Defense Layers (4_secure_api_server.py)

| Layer | Defense | Effect |
|-------|---------|--------|
| 1 | Rate Limiting | Blocks after 100 req/min |
| 2 | Query Pattern Detection | Flags IPs with >20 req/min |
| 3 | Response Noise | 35% chance to flip fare bucket for suspicious IPs |
| 4 | Batch Restriction | Suspicious IPs limited to 10/batch |
| 5 | Audit Logging | All suspicious activity logged |

**Behavior:**

| Requests/min | Status | Response |
|--------------|--------|----------|
| < 20 | ✅ Normal | Clean fare quote |
| 20-100 | ⚠️ Suspicious | Noisy fare (DP applied) |
| > 100 | ⛔ Blocked | 429 Rate Limited |

---

## Results Summary

| Metric | Vulnerable API | Secure API |
|--------|---------------|------------|
| Fidelity | ~90% | ~65% |
| High-value routes | ~85% match | ~50% match |
| Queries before block | Unlimited | 100/min |
| Revenue risk | $10-50M/year | Significantly reduced |

---

## Key Takeaway

> **Query access to pricing APIs = competitive intelligence theft.**
> Implement rate limiting, query auditing, and differential privacy
> on all revenue-sensitive ML endpoints.

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Full ML Model Access | AML.T0044 | Cloning pricing decisions |
| Exfiltration via Inference API | AML.T0024 | Stealing via fare quotes |

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-02-stealing-the-dynamic-pricing-engine) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [⚔️ Module 3: Offensive Security](../academy/module-03-offensive-security.md#33-model-theft) | Model theft techniques |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#46-model-protection) | API protection strategies |
| [🏗️ Module 8: Architecture](../academy/module-08-enterprise-architecture.md#81-ai-gateway-architecture) | AI Gateway rate limiting |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 01: Supply Chain](../lab-01-supply-chain-attack/) | Lab 02 of 23 | [Lab 03: Chatbot Hijacking](../lab-03-chatbot-hijacking/) |
