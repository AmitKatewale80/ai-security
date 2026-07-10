# Compliance Frameworks for AI

Mapping existing compliance frameworks (SOC 2, ISO 42001, GDPR, PCI-DSS) to AI-specific requirements.

## Overview

Organizations deploying AI must map AI risks to existing compliance frameworks while adopting new AI-specific standards. This requires extending current controls rather than building parallel programs.

## Framework Mapping

| Framework | AI-Relevant Requirements | Key Considerations |
|-----------|------------------------|-------------------|
| SOC 2 | Trust Service Criteria | AI processing integrity, confidentiality |
| ISO 42001 | AI Management System | Purpose-built for AI governance |
| GDPR | Data protection | Automated decision-making (Art. 22) |
| PCI-DSS | Cardholder data | AI systems processing payment data |
| HIPAA | Health information | AI in healthcare contexts |
| FedRAMP | Cloud security | Government AI deployments |

## ISO 42001 — AI Management System

The first international standard for AI management systems:

- **Context** — Understand AI risks in organizational context
- **Leadership** — Management commitment to responsible AI
- **Planning** — AI risk assessment and treatment
- **Support** — Resources, competence, awareness
- **Operation** — AI system lifecycle controls
- **Performance** — Monitoring and measurement
- **Improvement** — Continuous improvement of AI governance

## SOC 2 + AI Controls

Extend existing SOC 2 controls for AI:

1. **Security** — Add AI-specific threat controls (injection, poisoning)
2. **Availability** — Model failover, degradation handling
3. **Processing Integrity** — Hallucination monitoring, accuracy metrics
4. **Confidentiality** — Training data protection, model IP
5. **Privacy** — AI-specific privacy impact assessments

## GDPR Article 22 Requirements

- Right not to be subject to solely automated decisions
- Right to human intervention
- Right to contest the decision
- Right to obtain explanation of logic involved

## Related Labs

- [Lab 11 — Garak Red Teaming](../../airline-labs/lab-11-garak-red-teaming/) — Compliance testing automation

## Related Resources

- [Academy Module 6 — AI Governance](../../airline-labs/academy/module-06-ai-governance.md)

---

| [← Previous](04-ai-policies.md) | [Back to Module](README.md) | [Next →](06-ai-auditing.md) |
