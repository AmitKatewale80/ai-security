# 🧪 Module 5: Hands-on Enterprise Labs

> 23 labs demonstrating real attacks and defenses on airline AI systems.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 4: Defensive Security](module-04-defensive-security.md) | Module 5 of 10 | [Module 6: AI Governance](module-06-ai-governance.md) |

---

## Learning Objectives

After this module, you will be able to:
- Execute attack demonstrations against AI systems in a safe lab environment
- Implement and test defensive controls hands-on
- Map each attack to MITRE ATLAS techniques and OWASP LLM risks
- Explain the security implications to both technical and business audiences

---

## Lab Overview

### Section A: Core AI/ML Security (Labs 01-12)

| Lab | Title | Attack | Defense |
|-----|-------|--------|---------|
| [01](../lab-01-supply-chain-attack/) | Supply Chain Attack | Poisoned model opens reverse shell | Model scanning before loading |
| [02](../lab-02-model-stealing/) | Model Stealing | 3000 API queries clone pricing engine | Rate limiting + differential privacy |
| [03](../lab-03-chatbot-hijacking/) | Chatbot Hijacking | Injected policy doc reads PNR data | Path sandboxing + injection detection |
| [04](../lab-04-rag-data-extraction/) | RAG Data Extraction | Ground staff accesses CONFIDENTIAL docs | Role-based access control |
| [05](../lab-05-malicious-code-injection/) | Malicious Code Injection | Baggage scanner exfiltrates flagged data | Model class verification + code scanning |
| [06](../lab-06-model-signing/) | Model Signing | Tampered engine model hides CRITICAL alerts | ECDSA cryptographic signatures |
| [07](../lab-07-pii-tokenization/) | PII Tokenization | Breach exposes raw passport/card data | SHA-256 tokenization with isolated salt |
| [08](../lab-08-model-inversion/) | Model Inversion | Crew home bases reconstructed from API | Differential privacy (Laplace noise) |
| [09](../lab-09-chatbot-vulnerability-testing/) | Red-Team Testing | Booking bot gives unauthorized discounts | Automated vulnerability scanning |
| [10](../lab-10-data-poisoning/) | Data Poisoning | Fuel data inflated → $30M/year waste | Statistical validation (KS test) |
| [11](../lab-11-garak-red-teaming/) | Garak Compliance | Chatbot violates GDPR, gives unsafe advice | Compliance scanning in CI/CD |
| [12](../lab-12-ai-agent-security/) | Agent Security | IROPS agent cancels flights without approval | 5 security pillars |

### Section B: Enterprise Agentic AI Security (Labs 13-17)

| Lab | Title | Attack | Defense |
|-----|-------|--------|---------|
| [13](../lab-13-ai-gateway-security/) | AI Gateway Security | Token bypasses to access revenue model | Strict ACL + no header overrides |
| [14](../lab-14-enterprise-rag-security/) | Enterprise RAG Poisoning | False maintenance intervals in KB | Document provenance + multi-source validation |
| [15](../lab-15-ai-soc-security/) | AI SOC / SIEM | Log injection blinds AI for 6 hours | Log sanitization + structured parsing |
| [16](../lab-16-agent-identity/) | Agent Identity | Booking agent triggers engine shutdown | Per-agent identity + tool-level ACL |
| [17](../lab-17-ai-cost-governance/) | AI Cost Governance | Runaway agent loops → $50K overnight | Budget caps + loop detection |

### Section C: AI in QA & DevSecOps (Labs 18-23)

| Lab | Title | Attack | Defense |
|-----|-------|--------|---------|
| [18](../lab-18-ai-code-review-bypass/) | AI Code Review Bypass | Obfuscated vulns pass AI review | AI + SAST + human review |
| [19](../lab-19-ai-test-generation/) | AI Test Generation | AI tests all PASS but catch no bugs | Mutation testing gate |
| [20](../lab-20-ai-cicd-manipulation/) | CI/CD Manipulation | Vulnerable code skips security scans | Mandatory gates AI cannot skip |
| [21](../lab-21-test-data-leakage/) | Test Data Leakage | "Synthetic" data contains real PII | PII fingerprint scanning |
| [22](../lab-22-bug-triage-manipulation/) | Bug Triage Manipulation | Critical bugs deprioritized as cosmetic | Security keyword override |
| [23](../lab-23-test-input-injection/) | Test Input Injection | App responses hijack AI test runner | Input isolation from AI context |

---

## How to Run Labs

```bash
# 1. Navigate to the lab
cd ai-security/airline-labs/lab-XX-name

# 2. Activate the virtual environment (if present)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Run the demo
python run_demo.py              # If available
# OR run scripts in order:
python 1_first_script.py
python 2_second_script.py
python 3_third_script.py
python 4_defense_script.py
```

---

## MITRE ATLAS / OWASP Mapping

| Lab | ATLAS Technique | OWASP Risk | Security Principle |
|-----|----------------|-----------|-------------------|
| 01 | AML.T0010 (Supply Chain) | LLM03 | Never trust external models without scanning |
| 02 | AML.T0044 (Model Theft) | LLM10 | Rate limit + add noise to ML APIs |
| 03 | AML.T0051 (Prompt Injection) | LLM01 | Sanitize all inputs to LLMs |
| 04 | AML.T0051 (Prompt Injection) | LLM02, LLM08 | Access controls on knowledge bases |
| 05 | AML.T0010, T0011 (Backdoor) | LLM03, LLM04 | Scan models for hidden code |
| 06 | AML.T0010 (Supply Chain) | LLM03 | Cryptographic integrity verification |
| 07 | AML.T0044, T0024 (Exfiltration) | LLM02 | Tokenize PII before AI processing |
| 08 | AML.T0024, T0044 (Inversion) | LLM02 | Differential privacy on model APIs |
| 09 | AML.T0051 (Injection) | LLM01, LLM07 | Automated red-teaming before deploy |
| 10 | AML.T0020 (Poison Data) | LLM04 | Validate training data statistically |
| 11 | AML.T0051 (Injection) | LLM09 | Compliance scanning (Garak) |
| 12 | AML.T0051, T0043 (Adversarial) | LLM05, LLM06 | Least privilege + human-in-loop |
| 13 | AML.T0051 (Manipulation) | LLM06 | Strict model-level ACL |
| 14 | AML.T0020 (Poison Data) | LLM08 | Document provenance + multi-source |
| 15 | AML.T0051 (Injection) | LLM01 | Log sanitization + structured parsing |
| 16 | AML.T0051 (Manipulation) | LLM06 | Per-agent identity + tool ACL |
| 17 | AML.T0029 (DoS) | LLM10 | Budget caps + loop detection |
| 18 | AML.T0051 (Manipulation) | LLM05 | Multi-layer review (AI + SAST + human) |
| 19 | AML.T0051 (Manipulation) | LLM09 | Mutation testing validates AI tests |
| 20 | AML.T0051 (Manipulation) | LLM06 | Mandatory gates AI cannot skip |
| 21 | AML.T0024 (Exfiltration) | LLM02 | PII fingerprinting on generated data |
| 22 | AML.T0051 (Manipulation) | LLM09 | Security keyword override in triage |
| 23 | AML.T0051 (Injection) | LLM01 | Input isolation from AI instructions |

---

## 📖 Full Lab Explanations

For detailed beginner-friendly explanations of each lab (story, technical details, defense walkthrough, expected output), see:

**[Labs Explained for Beginners](../Labs_Explained_For_Beginners.md)**

---

## ➡️ Next: [Module 6 — AI Governance](module-06-ai-governance.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 4: Defensive Security](module-04-defensive-security.md) | [📚 References](references.md) | [Module 6: AI Governance](module-06-ai-governance.md) |
