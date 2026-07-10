# Output Filtering & Safety

Preventing PII leakage, policy violations, and harmful content in LLM outputs through systematic filtering and validation.

## Overview

Even with strong input validation, LLMs can generate outputs containing sensitive data, policy violations, or harmful content. Output filtering is the last defensive layer before responses reach users.

## Output Risk Categories

| Risk Category | Examples | Impact |
|---------------|----------|--------|
| PII leakage | Names, emails, SSNs, credit cards | Regulatory fines, privacy breach |
| Policy violations | Unauthorized discounts, false promises | Financial/legal liability |
| Harmful content | Offensive language, misinformation | Brand damage, safety risk |
| Data exfiltration | Training data memorization, RAG leaks | IP theft, compliance failure |
| Instruction leakage | System prompt disclosure | Security degradation |

## Filtering Strategies

1. **Regex-based PII detection** — Pattern match for known PII formats
2. **NER-based filtering** — Named Entity Recognition to catch contextual PII
3. **Policy classifiers** — ML models trained on policy-violating outputs
4. **Allowlist enforcement** — Only permit responses matching approved templates
5. **Confidence thresholding** — Block outputs where model uncertainty is high
6. **Human-in-the-loop** — Route high-risk outputs for manual review

## Implementation Pattern

```
User Input → LLM → [Output Filter Pipeline] → User Response
                         ├── PII Scanner
                         ├── Policy Classifier
                         ├── Toxicity Filter
                         └── Format Validator
```

## Best Practices

- Apply filters post-generation but pre-delivery
- Use multiple independent filters (defense in depth)
- Log filtered content for security analysis (redact PII in logs)
- Set fallback responses for blocked outputs
- Test filters against adversarial output manipulation

## Related Labs

- [Lab 04 — RAG Data Extraction](../../airline-labs/lab-04-rag-data-extraction/) — Preventing data leakage from RAG
- [Lab 07 — PII Tokenization](../../airline-labs/lab-07-pii-tokenization/) — PII protection techniques

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](01-input-validation.md) | [Back to Module](README.md) | [Next →](03-guardrails.md) |
