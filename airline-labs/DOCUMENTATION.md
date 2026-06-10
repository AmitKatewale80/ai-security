# Airline AI Security Labs — Documentation

## Overview

12 hands-on labs demonstrating AI/ML security threats and defenses in airline operations. Each lab shows a real attack scenario and its corresponding defense mechanism.

---

## Security Frameworks Covered

### MITRE ATLAS (7 Techniques)

| ID | Technique | Labs |
|----|-----------|------|
| AML.T0010 | ML Supply Chain Compromise | 01, 05 |
| AML.T0011 | Backdoor ML Model | 05, 06 |
| AML.T0020 | Poison Training Data | 10 |
| AML.T0024 | Exfiltration via Inference API | 02, 07, 08 |
| AML.T0044 | Full ML Model Access | 02, 07, 08 |
| AML.T0051 | LLM Prompt Injection | 03, 04, 09, 11, 12 |
| AML.T0043 | Craft Adversarial Data | 03, 12 |

### OWASP Top 10 for LLMs (All 10 Covered)

| ID | Risk | Labs |
|----|------|------|
| LLM01 | Prompt Injection | 03, 09, 12 |
| LLM02 | Sensitive Info Disclosure | 04, 07 |
| LLM03 | Supply Chain Vulnerabilities | 01, 05 |
| LLM04 | Data and Model Poisoning | 05, 10 |
| LLM05 | Improper Output Handling | 12 |
| LLM06 | Excessive Agency | 12 |
| LLM07 | System Prompt Leakage | 09 |
| LLM08 | Vector & Embedding Weaknesses | 04 |
| LLM09 | Misinformation | 11 |
| LLM10 | Unbounded Consumption | 02 |

---

## Labs by Category

### Model Security (Labs 01, 05, 06)
- Supply chain attacks via poisoned model registries
- Backdoor detection in ML models
- Cryptographic model signing and integrity verification

### API & Data Protection (Labs 02, 07, 08, 10)
- Rate limiting and differential privacy on ML APIs
- PII tokenization before AI processing
- Model inversion defense with noise
- Training data poisoning detection

### LLM & Chatbot Safety (Labs 03, 04, 09, 11)
- Indirect prompt injection defense
- RAG access control by role and classification
- Automated red-teaming before deployment
- Compliance scanning (bias, GDPR, safety)

### AI Agent Security (Lab 12)
- Least privilege, human-in-the-loop, policy-as-code
- Autonomy bounds and audit logging

---

## Labs Summary

| Lab | Scenario | Attack | Defense |
|-----|----------|--------|---------|
| 01 | Flight Delay Model | Reverse shell via model load | Model scanning, safetensors |
| 02 | Dynamic Pricing | 3000 API queries clone model | Rate limiting, differential privacy |
| 03 | Customer Chatbot | Indirect prompt injection | Sandboxing, injection detection |
| 04 | Crew Manuals (RAG) | Confidential data extraction | Role-based access control |
| 05 | Baggage Screening | Hidden exfiltration backdoor | Class verification, code scan |
| 06 | Engine Maintenance | Suppress CRITICAL alerts | ECDSA cryptographic signatures |
| 07 | Loyalty Fraud | PII exposed in breach | Tokenization (zero PII in pipeline) |
| 08 | Crew Scheduling | Reconstruct crew data from API | Differential privacy (Laplace noise) |
| 09 | Booking Assistant | Jailbreaks, fare manipulation | Automated red-teaming probes |
| 10 | Fuel Optimization | Poisoned training data (+15% fuel) | Statistical validation (KS test) |
| 11 | Compliance | GDPR, bias, safety violations | Garak scanning in CI/CD |
| 12 | IROPS Agent | Unauthorized flight cancellation | 5 security pillars |

---

## How to Run

```bash
# Clone and navigate
git clone https://github.com/AmitKatewale80/ai-security.git
cd ai-security/airline-labs/lab-XX-name

# Setup (first time)
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Run
python run_demo.py              # If available
# OR run numbered scripts in order
```

### Dependencies

| Requirement | Labs |
|-------------|------|
| Python only (no pip install) | 04, 09, 11, 12 |
| numpy, scikit-learn | 05, 06, 07, 08, 10 |
| flask, requests | 02 |
| OpenRouter API key | 03 |

---

## Key Defenses Demonstrated

| Defense | What it does | Labs |
|---------|-------------|------|
| Model Scanning | Detect malicious code before loading | 01, 05 |
| ECDSA Signing | Verify model integrity cryptographically | 06 |
| Rate Limiting | Block excessive API queries | 02 |
| Differential Privacy | Add noise to prevent data extraction | 02, 08 |
| PII Tokenization | Replace real data with meaningless tokens | 07 |
| Path Sandboxing | Restrict file access for AI tools | 03 |
| Access Control | Role-based document classification | 04 |
| Red-Teaming | Automated vulnerability probing | 09, 11 |
| Statistical Validation | Detect poisoned training data | 10 |
| Human-in-the-Loop | Require approval for high-risk actions | 12 |
