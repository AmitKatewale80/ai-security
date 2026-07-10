# 🛡️ Enterprise AI Security Learning Hub

A comprehensive AI security training platform covering the full lifecycle — from threat landscape to production governance. Built around **23 hands-on enterprise labs** in an airline context, aligned with [MITRE ATLAS](https://atlas.mitre.org/), [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/), [NIST AI RMF](https://www.nist.gov/artificial-intelligence/risk-management-framework), and Continuous Threat Exposure Management (CTEM).

This isn't just a lab collection — it's a structured 10-module academy covering AI fundamentals, offensive/defensive security, governance, architecture, secure SDLC, and production readiness.

---

## 📁 Repository Structure

```
ai-security/
├── airline-labs/                              # Hands-on enterprise labs
│   ├── academy/                              # 📖 10-Module AI Security Academy
│   │   ├── README.md                         #    Academy overview & structure
│   │   ├── module-01-ai-fundamentals.md      #    AI vs ML, LLMs, RAG, Agents
│   │   ├── module-02-threat-landscape.md     #    MITRE ATLAS, OWASP Top 10
│   │   ├── module-03-offensive-security.md   #    Prompt injection, model theft, poisoning
│   │   ├── module-04-defensive-security.md   #    Guardrails, gateways, agent security
│   │   ├── module-05-hands-on-labs.md        #    Index/gateway to 23 labs below
│   │   ├── module-06-ai-governance.md        #    NIST AI RMF, policies, risk mgmt
│   │   ├── module-07-continuous-security.md  #    CTEM, monitoring, AI SOC
│   │   ├── module-08-enterprise-architecture.md # Gateway, AI Mesh, identity
│   │   ├── module-09-secure-sdlc.md          #    Threat modeling, supply chain
│   │   ├── module-10-production-readiness.md #    Checklists, compliance, best practices
│   │   └── references.md                     #    MITRE, OWASP, NIST, industry refs
│   │
│   ├── lab-01-supply-chain-attack/           # HuggingFace model poisoning
│   ├── lab-02-model-stealing/                # Dynamic pricing theft
│   ├── lab-03-chatbot-hijacking/             # Booking assistant exploitation
│   ├── lab-04-rag-data-extraction/           # Crew manual data leak
│   ├── lab-05-malicious-code-injection/      # Baggage screening backdoor
│   ├── lab-06-model-signing/                 # Predictive maintenance integrity
│   ├── lab-07-pii-tokenization/              # Loyalty fraud - PII protection
│   ├── lab-08-model-inversion/               # Crew scheduling data extraction
│   ├── lab-09-chatbot-vulnerability-testing/ # Booking assistant red-teaming
│   ├── lab-10-data-poisoning/                # Fuel optimization data corruption
│   ├── lab-11-garak-red-teaming/             # Automated compliance scanning
│   ├── lab-12-ai-agent-security/             # IROPS agent security
│   ├── lab-13-ai-gateway-security/           # AI gateway policy bypass
│   ├── lab-14-enterprise-rag-security/       # Enterprise RAG poisoning
│   ├── lab-15-ai-soc-security/              # AI SIEM log injection
│   ├── lab-16-agent-identity/               # Agent privilege escalation
│   ├── lab-17-ai-cost-governance/           # AI cost & governance abuse
│   ├── lab-18-ai-code-review-bypass/        # AI code review manipulation
│   ├── lab-19-ai-test-generation/           # False confidence in AI tests
│   ├── lab-20-ai-cicd-manipulation/         # CI/CD security bypass
│   ├── lab-21-test-data-leakage/            # PII in generated test data
│   ├── lab-22-bug-triage-manipulation/      # Bug priority manipulation
│   ├── lab-23-test-input-injection/         # Test runner prompt injection
│   │
│   └── Labs_Explained_For_Beginners.md      # Beginner-friendly lab guide (all 23)
│
├── .gitignore
├── LICENSE                                    # MIT License
└── README.md                                  # This file
```

---

## 📖 Academy Modules

```
── 📖 Module 1 - AI Fundamentals
│   ├── AI vs ML, LLMs, RAG, AI Agents, Enterprise AI
│
├── 🛡️ Module 2 - AI Threat Landscape
│   ├── AI Attack Surface, Threat Categories, MITRE ATLAS, OWASP LLM Top 10
│
├── ⚔️ Module 3 - Offensive AI Security
│   ├── Prompt Injection, Jailbreaks, Model Theft, Data Poisoning, Red Teaming
│
├── 🛡️ Module 4 - Defensive AI Security
│   ├── Guardrails, Human in the Loop, AI Gateway, Secure RAG, Agent Security
│
├── 🧪 Module 5 - Hands-on Enterprise Labs
│   ├── 23 Enterprise Labs (airline-labs/) — Attack + Defense demonstrations
│
├── 🏛️ Module 6 - AI Governance
│   ├── NIST AI RMF, AI Policies, Risk Management, Responsible AI
│
├── 🔄 Module 7 - Continuous Security
│   ├── CTEM, Continuous Validation, AI SOC, Incident Response
│
├── 🏗️ Module 8 - Enterprise AI Architecture
│   ├── AI Gateway, AI Mesh, Enterprise RAG, Identity, Secrets
│
├── 🚀 Module 9 - Secure AI SDLC
│   ├── Threat Modeling, AI Code Review, Secure Deployment, Supply Chain
│
├── ✅ Module 10 - Production Readiness
│   ├── Checklists, Security Review, Compliance, Best Practices
│
└── 📚 References
    ├── MITRE ATLAS, OWASP, NIST AI RMF, Microsoft, Anthropic, OpenAI
```

👉 **Start here:** [`airline-labs/academy/README.md`](airline-labs/academy/README.md)

---

## 🧪 Labs Overview

### Section A: Airline Operations Security (Labs 01–12)

| Lab | Airline Scenario | Threat | MITRE ATLAS |
|-----|-----------------|--------|-------------|
| Lab 01 | Flight Delay Prediction Model | Supply Chain Attack | AML.T0010, AML.T0011 |
| Lab 02 | Dynamic Pricing Engine | Model Stealing via API | AML.T0044, AML.T0024 |
| Lab 03 | Passenger Booking Chatbot | Indirect Prompt Injection | AML.T0051, AML.T0043 |
| Lab 04 | Crew Operations Manual (RAG) | Data Extraction | AML.T0051 |
| Lab 05 | Baggage Screening AI | Malicious Code Injection | AML.T0010, AML.T0011 |
| Lab 06 | Predictive Maintenance Model | Model Tampering | AML.T0010, AML.T0011 |
| Lab 07 | Loyalty Fraud Detection | PII Exposure (Tokenization Defense) | AML.T0044, AML.T0024 |
| Lab 08 | Crew Scheduling | Model Inversion (Data Extraction) | AML.T0044, AML.T0024 |
| Lab 09 | Booking Assistant | Red-Teaming & Jailbreaks | AML.T0051 |
| Lab 10 | Fuel Optimization | Training Data Poisoning | AML.T0020 |
| Lab 11 | Customer-Facing Chatbot | Compliance Violations | AML.T0051 |
| Lab 12 | IROPS Recovery Agent | Agent Exploitation | AML.T0051, AML.T0043 |

### Section B: Enterprise Agentic AI Security (Labs 13–17)

| Lab | Enterprise Scenario | Threat | MITRE ATLAS |
|-----|-------------------|--------|-------------|
| Lab 13 | AI Gateway | Policy bypass, unauthorized model access, token abuse | AML.T0051 |
| Lab 14 | Enterprise RAG | Poisoned knowledge base, wrong maintenance decisions | AML.T0020 |
| Lab 15 | AI SOC / SIEM | False alerts, prompt injection in logs | AML.T0051 |
| Lab 16 | Agent Identity | Privilege escalation, cross-agent tool abuse | AML.T0051 |
| Lab 17 | AI Cost & Governance | Runaway agents, token explosion, audit gaps | AML.T0029 |

### Section C: AI in QA & DevSecOps (Labs 18–23)

| Lab | QA/DevSecOps Scenario | Threat | MITRE ATLAS |
|-----|----------------------|--------|-------------|
| Lab 18 | AI Code Review | Obfuscated vulns bypass AI reviewer | AML.T0051 |
| Lab 19 | AI Test Generation | Weak tests give false confidence | AML.T0051 |
| Lab 20 | AI CI/CD Pipeline | Attacker tricks AI into skipping security | AML.T0051 |
| Lab 21 | AI Test Data | Generated data contains real PII | AML.T0024 |
| Lab 22 | AI Bug Triage | Critical bugs deprioritized as cosmetic | AML.T0051 |
| Lab 23 | AI Test Runner | App responses hijack the AI test tool | AML.T0051 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### Getting Started

```bash
# Clone repository
git clone https://github.com/AmitKatewale80/ai-security.git
cd ai-security/airline-labs

# Start with Lab 01
cd lab-01-supply-chain-attack
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running a Lab

Each lab has numbered Python scripts that should be run in order:

```bash
# Example: Lab 01
python 1_attacker_listener.py      # Step 1: Start attacker (in separate terminal)
python 2_victim_loads_model.py     # Step 2: Victim loads poisoned model
python 3_safe_model_loading.py     # Step 3: Defense - safe loading
python airline_model_scanner.py    # Bonus: Scan model for threats
```

Each lab also has a `reset.py` to clean up after running.

---

## 🛡️ Defense Techniques & Frameworks Covered

| Category | Techniques |
|----------|-----------|
| **Model Security** | Model scanning, signature verification (ECDSA), safe loading, supply chain SBOM |
| **API Protection** | Rate limiting, query detection, differential privacy, AI Gateway ACL |
| **LLM Safety** | Input/output guardrails, injection detection, PII filtering |
| **Data Protection** | PII tokenization, data poisoning detection (KS test), access control |
| **Testing & Validation** | Red-teaming, Garak scanning, mutation testing, mandatory security gates |
| **Agent Security** | Least privilege, human-in-the-loop, policy engine, identity isolation |
| **Enterprise Architecture** | AI Gateway, AI Mesh, secure RAG, secrets management |
| **Governance** | NIST AI RMF (Govern/Map/Measure/Manage), risk registers, AI Review Board |
| **Continuous Security** | CTEM, continuous validation in CI/CD, AI SOC, incident response |
| **Compliance** | EU AI Act, GDPR, DOT regulations, PCI-DSS, FAA safety rules |

---

## 📊 Documentation

| Document | Description |
|----------|-------------|
| **[Academy](airline-labs/academy/README.md)** | Full 10-module training curriculum (start here) |
| **[Labs Explained for Beginners](airline-labs/Labs_Explained_For_Beginners.md)** | Detailed beginner-friendly walkthrough of all 23 labs |
| **[Documentation](airline-labs/DOCUMENTATION.md)** | Security frameworks, lab mappings, and defense catalog |

---

## ⚠️ Disclaimer

> This repository is for **EDUCATIONAL** and **RESEARCH** purposes only.
> Do not use any code, techniques, or materials for malicious activities.
> All attack simulations run locally and do not target real systems.
> The author assumes no liability for misuse.

---

## 📄 License

[MIT License](LICENSE) — Free to use, modify, and distribute.

---

## 👤 Author

**AmitK**

---

## 🙏 Acknowledgments

- [MITRE ATLAS Framework](https://atlas.mitre.org/) — AI threat taxonomy
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM security risks
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/risk-management-framework) — AI governance
- [Garak](https://github.com/leondz/garak) — LLM vulnerability scanner
- [Gartner CTEM](https://www.gartner.com/) — Continuous Threat Exposure Management

---

## 🏷️ Topics

`ai-security` · `llm-security` · `mitre-atlas` · `owasp` · `nist-ai-rmf` · `ctem` · `ai-governance` · `prompt-injection` · `red-teaming` · `machine-learning-security`
