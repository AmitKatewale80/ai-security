# AI Security Policies

Writing and implementing policies for AI usage, agent authority, data handling, and incident response.

## Overview

AI-specific policies extend existing security policies to address unique challenges of AI systems. Well-crafted policies provide clear guidance while remaining flexible enough for rapid AI evolution.

## Essential AI Policies

| Policy | Scope | Key Contents |
|--------|-------|-------------|
| Acceptable AI Use | All staff | Approved tools, data restrictions, prohibited uses |
| Agent Authority | AI systems | What actions agents can take autonomously |
| AI Data Governance | Data teams | Training data rules, retention, privacy |
| AI Incident Response | Security teams | Classification, response, notification |
| Model Deployment | ML engineers | Approval gates, security requirements |
| Third-party AI | Procurement | Vendor assessment, data sharing limits |

## AI Acceptable Use Policy Template

1. **Purpose** — Define why the policy exists
2. **Scope** — Which tools, systems, and users are covered
3. **Approved tools** — List sanctioned AI services
4. **Data restrictions** — What data cannot be input to AI
5. **Output handling** — Requirements for verifying AI outputs
6. **Prohibited uses** — Explicitly banned activities
7. **Reporting** — How to report violations or incidents
8. **Exceptions** — Process for requesting exceptions

## Agent Authority Levels

- **Level 0** — Read-only, advisory (no autonomous actions)
- **Level 1** — Limited actions with human approval
- **Level 2** — Autonomous within defined boundaries
- **Level 3** — Broad autonomy with audit trail
- **Level 4** — Full autonomy (not recommended for most uses)

## Incident Response Additions

- AI-specific incident classification criteria
- Model rollback procedures
- Guardrail failure response
- Data exposure notification timelines
- Post-incident model retraining requirements

## Related Resources

- [Academy Module 6 — AI Governance](../../airline-labs/academy/module-06-ai-governance.md)

---

| [← Previous](03-responsible-ai.md) | [Back to Module](README.md) | [Next →](05-compliance-frameworks.md) |
