# AI Risk Management

Systematic approaches to identifying, assessing, and managing risks in AI systems.

## Overview

AI risk management extends traditional cybersecurity risk frameworks to address unique AI threats including model failures, adversarial attacks, and emergent behaviors.

## AI Risk Assessment Process

1. **Identify** — Catalog AI systems and their intended uses
2. **Classify** — Assign risk levels based on impact and probability
3. **Assess** — Evaluate current controls and residual risk
4. **Mitigate** — Implement additional controls where needed
5. **Monitor** — Continuously track risk indicators
6. **Report** — Communicate risk posture to stakeholders

## Risk Scoring Matrix

| Likelihood \ Impact | Low | Medium | High | Critical |
|---------------------|-----|--------|------|----------|
| **Very Likely** | Medium | High | Critical | Critical |
| **Likely** | Low | Medium | High | Critical |
| **Possible** | Low | Medium | High | High |
| **Unlikely** | Low | Low | Medium | High |

## AI-Specific Risk Categories

- **Model risks** — Hallucination, drift, bias, failure modes
- **Security risks** — Injection, extraction, poisoning, evasion
- **Operational risks** — Availability, cost, performance degradation
- **Compliance risks** — Regulatory violations, audit failures
- **Reputational risks** — Harmful outputs, discrimination, PR incidents
- **Strategic risks** — Vendor lock-in, capability gaps

## Risk Register Template

| Risk ID | Description | Category | Likelihood | Impact | Controls | Owner | Status |
|---------|-------------|----------|-----------|--------|----------|-------|--------|
| AI-001 | Prompt injection | Security | High | High | Input validation, guardrails | AppSec | Mitigated |
| AI-002 | Training data bias | Model | Medium | High | Bias testing, diverse data | MLOps | Monitoring |

## Related Resources

- [Academy Module 6 — AI Governance](../../airline-labs/academy/module-06-ai-governance.md)

---

| [← Previous](01-ai-regulations.md) | [Back to Module](README.md) | [Next →](03-responsible-ai.md) |
