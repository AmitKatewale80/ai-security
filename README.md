# ✈️ Airline AI Security Labs

A comprehensive collection of hands-on labs for learning AI/ML security in the **airline industry context**, aligned with the [MITRE ATLAS](https://atlas.mitre.org/) adversarial threat framework and [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

Each lab simulates a real-world AI security threat that airlines face — from supply chain attacks on flight delay models to chatbot hijacking and AI agent exploitation.

---

## 📁 Repository Structure

```
ai-security/
├── airline-labs/                              # Hands-on airline security labs
│   ├── lab-01-supply-chain-attack/           # HuggingFace model poisoning
│   ├── lab-02-model-stealing/                # Dynamic pricing theft
│   ├── lab-03-chatbot-hijacking/             # Booking assistant exploitation
│   ├── lab-04-rag-data-extraction/           # Crew manual data leak
│   ├── lab-05-malicious-code-injection/      # Baggage screening backdoor
│   ├── lab-06-model-signing/                 # Predictive maintenance integrity
│   ├── lab-07-pii-tokenization/              # Loyalty fraud - PII protection
│   ├── lab-08-model-inversion/               # Crew scheduling data extraction
│   ├── lab-09-red-teaming/                   # Booking assistant red-teaming
│   ├── lab-10-data-poisoning/                # Fuel optimization data corruption
│   ├── lab-11-garak-compliance/              # Automated compliance scanning
│   └── lab-12-ai-agent-security/             # IROPS agent security
│
│   └── Labs_Explained_For_Beginners.md      # Beginner-friendly lab guide
│
├── .gitignore
├── LICENSE                                    # MIT License
└── README.md                                  # This file
```

---

## 🧪 Labs Overview

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

## 🛡️ Defense Techniques Covered

| Category | Techniques |
|----------|-----------|
| **Model Security** | Model scanning, signature verification, safe loading |
| **API Protection** | Rate limiting, query detection, differential privacy |
| **LLM Safety** | Input sanitization, output filtering, guardrails |
| **Data Protection** | PII tokenization, data poisoning detection |
| **Testing** | Red-teaming, Garak scanning, automated compliance |
| **Agent Security** | Tool restrictions, human-in-the-loop, audit logging |

---

## 📊 Documentation

For full documentation on security frameworks, lab categories, and defense techniques:

- **[Documentation](airline-labs/DOCUMENTATION.md)** — Security frameworks, lab mappings, and defense catalog

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
- [Garak](https://github.com/leondz/garak) — LLM vulnerability scanner
