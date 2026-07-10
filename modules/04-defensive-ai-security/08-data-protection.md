# Data Protection for AI

PII tokenization, differential privacy, and training data protection strategies for AI systems.

## Overview

AI systems process and memorize sensitive data throughout their lifecycle — from training through inference. Data protection must be applied at every stage to prevent leakage and comply with regulations.

## Protection Techniques

| Technique | Stage | Protection Level | Performance Impact |
|-----------|-------|-----------------|-------------------|
| PII tokenization | Pre-processing | High | Low |
| Differential privacy | Training | High | Medium (accuracy loss) |
| Data anonymization | Pre-processing | Medium | Low |
| Federated learning | Training | High | High (complexity) |
| Encryption (homomorphic) | Inference | Very High | Very High |
| Output masking | Post-processing | Medium | Low |

## PII Tokenization

Replace sensitive values with reversible tokens before LLM processing:

1. **Detect PII** — Use NER models or regex patterns
2. **Generate tokens** — Create unique, non-reversible placeholders
3. **Process safely** — LLM sees only tokens, not real data
4. **De-tokenize** — Replace tokens with real values in final output
5. **Audit** — Log tokenization events (not the PII itself)

## Differential Privacy for Training

- Add calibrated noise to training gradients (DP-SGD)
- Set privacy budget (epsilon) based on sensitivity requirements
- Track cumulative privacy loss across training epochs
- Validate model utility after applying DP constraints

## Training Data Protection

- **Data minimization** — Only collect what's needed
- **Purpose limitation** — Use data only for stated purpose
- **Retention policies** — Delete data after training window
- **Access controls** — Restrict who can access training datasets
- **Unlearning** — Ability to remove specific data from trained models

## Compliance Mapping

| Regulation | Key Requirement | AI Implication |
|------------|----------------|----------------|
| GDPR | Right to erasure | Model unlearning needed |
| CCPA | Data disclosure | Track what models memorize |
| HIPAA | PHI protection | Tokenize health data before training |
| PCI-DSS | Card data security | Never train on raw card numbers |

## Related Labs

- [Lab 07 — PII Tokenization](../../airline-labs/lab-07-pii-tokenization/) — Implementing PII tokenization
- [Lab 08 — Model Inversion](../../airline-labs/lab-08-model-inversion/) — Extracting training data
- [Lab 21 — Test Data Leakage](../../airline-labs/lab-21-test-data-leakage/) — Data leakage in CI/CD

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](07-model-security.md) | [Back to Module](README.md) | [Next →](../05-hands-on-labs/) |
