# Lab 07: PII Tokenization for Loyalty Fraud Detection

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0044-red.svg)](https://atlas.mitre.org/techniques/AML.T0044)
[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0024-red.svg)](https://atlas.mitre.org/techniques/AML.T0024)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.** Do not use for malicious activities.

---

## Overview

This lab demonstrates how an airline's loyalty fraud detection AI can process
member data **without exposing real PII** (passport numbers, credit cards, emails).

**The threat:** If the fraud detection system is breached, all member PII is exposed.

**The defense:** Tokenize (replace) all PII with random tokens BEFORE feeding data to
the AI model. Even if the entire system is compromised, attackers get only meaningless tokens.

---

## Business Impact

- Frequent flyer fraud costs airlines **$1B+ annually**
- A breach of loyalty member data = GDPR fine up to **€20M or 4% revenue**
- Tokenization allows fraud detection WITHOUT storing real PII in the AI pipeline

---

## Scripts

```bash
python 1_loyalty_fraud_model.py        # Train fraud detection on RAW data (vulnerable)
python 2_breach_simulation.py          # Attacker breaches system → sees all PII
python 3_tokenized_fraud_model.py      # Train same model on TOKENIZED data (secure)
python 4_breach_tokenized.py           # Attacker breaches → sees only useless tokens
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Full ML Model Access | AML.T0044 | Attacker accesses training data via model breach |
| Exfiltration via Inference API | AML.T0024 | Data leakage from model pipeline |

---

## Key Takeaway

> **Tokenize PII before it enters ANY AI pipeline.** The model works just as well
> on tokens, but a breach yields zero useful data to the attacker.
