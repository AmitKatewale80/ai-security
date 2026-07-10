# AI System Auditing

How to audit AI systems for security vulnerabilities, bias, compliance, and operational risks.

## Overview

AI auditing combines traditional security assessment methods with AI-specific evaluation techniques. Audits should cover the entire AI lifecycle — from data sourcing through production operation.

## Audit Scope

| Area | What to Assess | Methods |
|------|---------------|---------|
| Data governance | Training data provenance, consent, quality | Document review, lineage tracing |
| Model security | Vulnerability to attacks, robustness | Red teaming, automated scanning |
| Bias & fairness | Disparate impact, representation | Statistical testing, subgroup analysis |
| Access controls | Who can access what | Permission review, penetration testing |
| Compliance | Regulatory requirements met | Gap analysis, evidence collection |
| Operations | Monitoring, incident response readiness | Tabletop exercises, log review |

## AI Audit Process

1. **Scoping** — Define systems, standards, and timeframe
2. **Evidence collection** — Gather documentation, logs, configs
3. **Technical testing** — Run security scans, bias tests
4. **Interviews** — Speak with developers, operators, users
5. **Analysis** — Identify findings, assess severity
6. **Reporting** — Document findings with remediation recommendations
7. **Follow-up** — Verify remediation effectiveness

## Key Audit Questions

- How was training data sourced and labeled?
- What adversarial testing has been performed?
- Can model decisions be explained and attributed?
- Are guardrails tested regularly for bypass?
- Is there a model rollback procedure?
- Are AI incidents tracked and classified?
- Who approved the model for production?

## Audit Tools

- **Garak** — Automated vulnerability scanning for LLMs
- **Fairlearn** — Bias and fairness assessment
- **AI Verify** — Singapore government AI testing toolkit
- **HELM** — Stanford holistic LLM evaluation

## Related Labs

- [Lab 09 — Chatbot Vulnerability Testing](../../airline-labs/lab-09-chatbot-vulnerability-testing/) — Structured vulnerability assessment
- [Lab 11 — Garak Red Teaming](../../airline-labs/lab-11-garak-red-teaming/) — Automated audit tooling

## Related Resources

- [Academy Module 6 — AI Governance](../../airline-labs/academy/module-06-ai-governance.md)

---

| [← Previous](05-compliance-frameworks.md) | [Back to Module](README.md) | [Next →](../07-continuous-security/) |
