# 🛡️ Module 2: AI Threat Landscape

> Know thy enemy — understanding how attackers target AI systems.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 1: AI Fundamentals](module-01-ai-fundamentals.md) | Module 2 of 10 | [Module 3: Offensive Security](module-03-offensive-security.md) |

---

## Learning Objectives

After this module, you will be able to:
- Map the AI attack surface across the ML lifecycle
- Categorize AI threats by type and impact
- Navigate MITRE ATLAS and identify relevant techniques
- Apply OWASP LLM Top 10 to your AI deployments

---

## 2.1 AI Attack Surface

### The ML Lifecycle — Every Stage Is Attackable

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DATA    │───▶│ TRAINING │───▶│  MODEL   │───▶│ DEPLOY   │───▶│ INFERENCE│
│ Collection│    │          │    │ Storage  │    │          │    │ (Serving)│
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↓               ↓               ↓               ↓               ↓
 Poisoning      Backdooring     Tampering       Supply Chain     Prompt Injection
 Scraping       Bias Injection  Theft           Config Attack    Model Inversion
 Privacy Leak   Label Flip      Modification    Gateway Bypass   Data Extraction
                                                                 Adversarial Input
```

### Airline-Specific Attack Surface

| Attack Surface | What's Exposed | Attacker Goal | Impact |
|---------------|---------------|---------------|--------|
| Customer chatbot | LLM + policy docs | Extract PII, free upgrades | Data breach, revenue loss |
| Pricing API | Revenue model | Steal pricing logic | $10-50M competitive loss |
| Model registry | Trained models | Plant backdoor | Full system compromise |
| Knowledge base | Internal documents | Poison decisions | Safety risk, wrong ops |
| Agent tools | Booking/ops functions | Unauthorized actions | Cancelled flights, chaos |
| Training pipeline | Historical data | Bias predictions | $30-50M fuel waste |
| CI/CD pipeline | Test/deploy systems | Bypass security gates | Vulnerabilities ship |

---

## 2.2 Threat Categories

### Category 1: Supply Chain Attacks (Pre-deployment)

Attacker compromises the model BEFORE it reaches production.

| Attack | Technique | Detection Difficulty | Labs |
|--------|-----------|---------------------|------|
| Poisoned model from registry | Hidden malware in model code | Hard — model works correctly | 01, 05 |
| Backdoored model | Trigger activates on specific input | Very Hard — normal behavior otherwise | 05, 06 |
| Tampered model | Subtle prediction changes | Hard — passes accuracy tests | 06 |
| Compromised dependencies | Malicious library updates | Medium — version tracking helps | — |

### Category 2: Inference Attacks (Post-deployment)

Attacker exploits the model through its API or interface.

| Attack | Technique | Detection Difficulty | Labs |
|--------|-----------|---------------------|------|
| Prompt injection | Hidden instructions in input/data | Medium — pattern detection | 03, 04, 09, 23 |
| Model theft | Systematic querying to clone model | Medium — rate limiting helps | 02 |
| Model inversion | Reconstruct training data from API | Hard — statistical analysis | 08 |
| Jailbreaking | Override safety controls | Medium — output monitoring | 09, 11 |
| Data extraction | Extract PII from model memory | Hard — differential privacy | 07, 21 |

### Category 3: Data Attacks (Training pipeline)

Attacker corrupts data to influence model behavior.

| Attack | Technique | Detection Difficulty | Labs |
|--------|-----------|---------------------|------|
| Training data poisoning | Modify historical records | Hard — looks like normal data | 10 |
| Knowledge base poisoning | Inject false documents | Medium — provenance tracking | 14 |
| Label flipping | Change correct labels to wrong | Hard — statistical detection | 10 |
| Feedback loop poisoning | Corrupt online learning signals | Very Hard — gradual drift | — |

### Category 4: Operational Attacks (Runtime)

Attacker exploits operational weaknesses in AI infrastructure.

| Attack | Technique | Detection Difficulty | Labs |
|--------|-----------|---------------------|------|
| Token/cost abuse | Trigger infinite loops | Easy — cost monitoring | 17 |
| Gateway bypass | Manipulate routing headers | Medium — strict ACLs | 13 |
| Agent escalation | Cross-domain privilege abuse | Hard — identity isolation | 16 |
| Log injection | Blind AI SIEM with fake logs | Hard — log sanitization | 15 |
| QA manipulation | Trick AI test systems | Medium — deterministic gates | 18, 19, 20, 22, 23 |

---

## 2.3 MITRE ATLAS Overview

### What Is MITRE ATLAS?

**ATLAS** = Adversarial Threat Landscape for AI Systems

It's the AI equivalent of MITRE ATT&CK (which catalogs cyberattacks). ATLAS catalogs attacks specifically against AI/ML systems.

### ATLAS Tactics (Attack Phases)

```
RECONNAISSANCE → RESOURCE DEV → INITIAL ACCESS → ML ATTACK → IMPACT
─────────────   ────────────   ──────────────   ─────────   ──────
Discover AI     Prepare attack  Get into the     Attack the   Achieve
endpoints,      tools, poison   ML pipeline      model itself goal
model info      datasets        or inference
```

### Key ATLAS Techniques for Airlines

| ID | Technique | What It Means | Airline Scenario | Our Lab |
|----|-----------|---------------|-----------------|---------|
| AML.T0010 | ML Supply Chain Compromise | Poison model before download | Backdoor in "flight delay predictor" | 01, 05 |
| AML.T0011 | Backdoor ML Model | Hidden trigger in model | Modified baggage scanner | 05, 06 |
| AML.T0020 | Poison Training Data | Corrupt training records | Inflated fuel consumption data | 10 |
| AML.T0024 | Exfiltration via Inference API | Extract data through queries | Reconstruct crew schedules | 02, 07, 08 |
| AML.T0029 | Denial of ML Service | Exhaust AI resources | Runaway agent, $50K costs | 17 |
| AML.T0043 | Craft Adversarial Data | Fool model with crafted input | Evade baggage screening | 03, 12 |
| AML.T0044 | Full ML Model Access | Steal entire model | Clone pricing algorithm | 02, 07, 08 |
| AML.T0051 | LLM Prompt Injection | Hidden instructions in data | Policy doc hijacks chatbot | 03, 04, 09, 11–16, 18, 20, 22, 23 |

### Using ATLAS in Practice

For each AI system you deploy, ask:
1. Which ATLAS techniques could target this system?
2. What's the attack surface? (training data, inference API, tools, knowledge base)
3. What controls exist for each relevant technique?
4. What's the residual risk after controls?

---

## 2.4 OWASP Top 10 for LLM Applications

### What Is OWASP LLM Top 10?

The same organization that created the Web Application Top 10 (SQL injection, XSS, etc.) created a priority-ranked list of risks specifically for LLM-based applications.

### The Full List with Airline Context

| # | Risk | Plain English | Airline Example | Severity | Labs |
|---|------|--------------|-----------------|----------|------|
| LLM01 | **Prompt Injection** | Hidden instructions trick the AI | Poisoned policy doc reads PNR records | Critical | 03, 09, 12, 23 |
| LLM02 | **Sensitive Info Disclosure** | AI leaks private data | Chatbot reveals passport numbers | Critical | 04, 07, 21 |
| LLM03 | **Supply Chain Vulnerabilities** | Poisoned models/plugins | Malicious model from registry | High | 01, 05 |
| LLM04 | **Data and Model Poisoning** | Corrupted training data | Fuel data inflated 15-25% | High | 05, 10 |
| LLM05 | **Improper Output Handling** | Trust AI output without validation | AI code review approves SQLi | High | 12, 13, 18 |
| LLM06 | **Excessive Agency** | AI has too many permissions | Booking agent triggers engine shutdown | Critical | 12, 15, 16, 20 |
| LLM07 | **System Prompt Leakage** | Attacker extracts secret instructions | Reveal discount rules and limits | Medium | 09 |
| LLM08 | **Vector & Embedding Weaknesses** | Poisoned knowledge bases | False maintenance intervals in RAG | High | 04, 14 |
| LLM09 | **Misinformation** | AI generates wrong info confidently | "No prior approval needed for oxygen" | High | 11, 14, 19, 22 |
| LLM10 | **Unbounded Consumption** | AI drains resources/money | Agent loops → $50K overnight | Medium | 02, 17 |

### Risk Assessment Matrix

```
                    LIKELIHOOD
              Low        Medium       High
         ┌──────────┬──────────┬──────────┐
  High   │ LLM04    │ LLM03    │ LLM01    │
         │ LLM08    │ LLM06    │ LLM02    │
IMPACT   ├──────────┼──────────┼──────────┤
  Medium │ LLM10    │ LLM05    │ LLM07    │
         │          │ LLM09    │          │
         ├──────────┼──────────┼──────────┤
  Low    │          │          │          │
         └──────────┴──────────┴──────────┘
```

### Priority for Airlines

**Address immediately (Critical + High likelihood):**
1. LLM01 — Prompt Injection (affects every chatbot and agent)
2. LLM02 — Sensitive Info Disclosure (passenger PII everywhere)
3. LLM06 — Excessive Agency (IROPS agents have dangerous tools)

**Address within 30 days:**
4. LLM03 — Supply Chain (model registry security)
5. LLM05 — Improper Output Handling (AI code review, test automation)
6. LLM09 — Misinformation (compliance and safety risks)

**Address within 90 days:**
7. LLM04, LLM08 — Data/Knowledge poisoning
8. LLM07, LLM10 — Prompt leakage and cost control

---

## 2.5 Threat Actor Profiles

### Who Attacks Airline AI Systems?

| Actor | Motivation | Capability | Target | Typical Attack |
|-------|-----------|-----------|--------|---------------|
| **Competitor** | Steal pricing IP | Medium | Revenue models, pricing API | Model theft (Lab 02) |
| **Criminal** | Steal PII for resale | Medium | Customer data, PNR records | Prompt injection (Lab 03) |
| **Insider** | Financial gain, grudge | High (access) | Training data, model registry | Data poisoning (Lab 10) |
| **Nation-state** | Disruption, intelligence | Very High | Safety systems, operations | Supply chain (Lab 01, 05) |
| **Researcher** | Publicity, bounty | High (skill) | Any public-facing AI | Red-teaming (Lab 09) |
| **Passenger** | Free upgrades, refunds | Low | Customer chatbot | Jailbreaking (Lab 09) |

---

## 🧪 Module 2 Exercise

**Threat Mapping for Your Systems:**

Take one AI system from your airline and complete this:

```
System Name: _______________________
AI Type: [LLM / RAG / Agent / Traditional ML]
Data Sensitivity: [Public / Internal / Confidential / Restricted]

ATLAS Techniques Applicable:
  □ AML.T0010 (Supply Chain)
  □ AML.T0020 (Data Poisoning)
  □ AML.T0024 (Exfiltration)
  □ AML.T0044 (Model Theft)
  □ AML.T0051 (Prompt Injection)

OWASP Risks Applicable:
  □ LLM01 □ LLM02 □ LLM03 □ LLM04 □ LLM05
  □ LLM06 □ LLM07 □ LLM08 □ LLM09 □ LLM10

Top 3 Risks:
  1. ___________________________
  2. ___________________________
  3. ___________________________

Existing Controls:
  ___________________________

Gaps:
  ___________________________
```

---

## ➡️ Next: [Module 3 — Offensive AI Security](module-03-offensive-security.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 1: AI Fundamentals](module-01-ai-fundamentals.md) | [📚 References](references.md) | [Module 3: Offensive Security](module-03-offensive-security.md) |
