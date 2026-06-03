# Lab 11: Garak Red Teaming - Compliance Testing for AI Interactions

## Overview

This lab demonstrates automated red-team testing of airline AI systems
for bias, safety, and GDPR compliance using a simulated garak-style
scanning framework.

**Airline Attack Scenario:** Before launching a new AI-powered customer
service system, the compliance team runs automated probes to test for
discriminatory behavior, safety violations, and data protection issues.

**Note:** This simulates garak-style scanning without requiring the
actual garak installation.

---

## The Vulnerability

```python
# AI system without compliance testing
chatbot.deploy_to_production()
# Later discovered:
# - Offers different prices based on perceived nationality
# - Reveals other passengers' personal data
# - Makes unsafe recommendations about medical oxygen
# - Violates GDPR right-to-erasure requests
```

---

## Airline-Specific Risks

| Compliance Area | Risk |
|----------------|------|
| Bias/Discrimination | Differential treatment by nationality/gender |
| Safety | Incorrect medical/safety advice |
| GDPR | Failure to honor data rights |
| Accessibility | Exclusion of disabled passengers |
| Fair Pricing | Discriminatory fare offers |

---

## Lab Structure

```
lab-11-garak-red-teaming/
├── 1_setup_target.py         # Configure the target AI system
├── 2_run_scan.py             # Run simulated garak-style probes
├── 3_analyze_results.py      # Analyze and report findings
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-11-garak-red-teaming
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Demo

```bash
python 1_setup_target.py      # Configure target system
python 2_run_scan.py          # Run compliance probes
python 3_analyze_results.py   # Analyze results
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| LLM Prompt Injection | AML.T0051 | Testing for injection vulnerabilities |
| LLM Data Leakage | AML.T0048 | Testing for data exposure |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
