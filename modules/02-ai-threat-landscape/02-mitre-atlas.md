# MITRE ATLAS — Adversarial Threat Landscape for AI Systems

> The AI/ML equivalent of MITRE ATT&CK — a knowledge base of adversarial techniques targeting machine learning systems.

---

## What Is MITRE ATLAS?

[MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for Artificial Intelligence Systems) is the industry-standard catalog of attacks against AI/ML systems. Like MITRE ATT&CK catalogs cyberattacks, ATLAS catalogs attacks specifically designed to exploit machine learning.

---

## ATLAS Tactics (Attack Phases)

```
RECONNAISSANCE → RESOURCE DEV → INITIAL ACCESS → ML ATTACK → IMPACT
```

| Tactic | Goal | Airline Example |
|--------|------|-----------------|
| Reconnaissance | Discover AI endpoints, model info | Find airline's pricing API endpoints |
| Resource Development | Prepare attack tools and datasets | Generate 3000 systematic pricing queries |
| Initial Access | Get into the ML pipeline or inference | Gain access to model registry or API |
| ML Attack Execution | Execute the AI-specific attack | Clone pricing model, inject backdoor |
| Impact | Achieve attacker's goal | Steal IP, exfiltrate data, disrupt ops |

---

## Key Techniques Referenced in Our Labs

| ID | Technique | Description | Our Lab(s) |
|----|-----------|-------------|-----------|
| AML.T0010 | ML Supply Chain Compromise | Poison model before download | [Lab 01](../../airline-labs/lab-01-supply-chain-attack/), [Lab 05](../../airline-labs/lab-05-malicious-code-injection/) |
| AML.T0011 | Backdoor ML Model | Hidden trigger activates on specific input | [Lab 05](../../airline-labs/lab-05-malicious-code-injection/), [Lab 06](../../airline-labs/lab-06-model-signing/) |
| AML.T0020 | Poison Training Data | Corrupt training records to bias behavior | [Lab 10](../../airline-labs/lab-10-data-poisoning/), [Lab 14](../../airline-labs/lab-14-enterprise-rag-security/) |
| AML.T0024 | Exfiltration via Inference API | Extract sensitive data through queries | [Lab 02](../../airline-labs/lab-02-model-stealing/), [Lab 08](../../airline-labs/lab-08-model-inversion/) |
| AML.T0029 | Denial of ML Service | Exhaust AI system resources | [Lab 17](../../airline-labs/lab-17-ai-cost-governance/) |
| AML.T0043 | Craft Adversarial Data | Create inputs that fool the model | [Lab 03](../../airline-labs/lab-03-chatbot-hijacking/), [Lab 12](../../airline-labs/lab-12-ai-agent-security/) |
| AML.T0044 | Full ML Model Access | Steal entire model or training data | [Lab 02](../../airline-labs/lab-02-model-stealing/), [Lab 07](../../airline-labs/lab-07-pii-tokenization/) |
| AML.T0051 | LLM Prompt Injection | Trick LLM with crafted instructions | [Lab 03](../../airline-labs/lab-03-chatbot-hijacking/), [Lab 09](../../airline-labs/lab-09-chatbot-vulnerability-testing/), [Lab 15](../../airline-labs/lab-15-ai-soc-security/) |

---

## Using ATLAS in Practice

For each AI system you deploy, ask:

1. **Which techniques apply?** Map your system type to relevant ATLAS IDs
2. **What's the attack surface?** Training data, API, model files, knowledge base, tools
3. **What controls exist?** For each technique, what defenses are in place?
4. **What's the residual risk?** After controls, what exposure remains?

### Example: Airline Customer Chatbot

```
System: SkyAssist Customer Chatbot (LLM + RAG + Tools)

Applicable Techniques:
  ✓ AML.T0051 (Prompt Injection) — chatbot reads external documents
  ✓ AML.T0024 (Exfiltration) — chatbot has access to booking data
  ✓ AML.T0043 (Adversarial Data) — crafted inputs to bypass safety

Controls:
  ✓ Input guardrails (injection detection)
  ✓ Path sandboxing (limits file access)
  ✓ PII filtering (blocks sensitive data in output)
  ✓ Rate limiting (prevents systematic extraction)

Residual Risk: MEDIUM (novel injection techniques may bypass guardrails)
```

---

## ATLAS Navigator

Use the [ATLAS Navigator](https://atlas.mitre.org/navigator) to visualize which techniques your defenses cover and where gaps exist.

---

## 🔗 Related

- [Academy Module 2: Threat Landscape](../../airline-labs/academy/module-02-threat-landscape.md)
- [← OWASP LLM Top 10](01-owasp-llm-top10.md)
- [Attack Taxonomy →](03-attack-taxonomy.md)
- [ATLAS Official Site](https://atlas.mitre.org/)

---

| [← Previous: OWASP Top 10](01-owasp-llm-top10.md) | [Back to Module 2](README.md) | [Next: Attack Taxonomy →](03-attack-taxonomy.md) |
|:---:|:---:|:---:|
