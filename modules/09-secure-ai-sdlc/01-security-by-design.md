# Security by Design for AI

Building security into AI systems from the start rather than bolting it on after deployment.

## Overview

Security by design means that security considerations inform every decision from architecture through deployment. For AI systems, this includes model selection, data pipeline design, and interaction patterns.

## Security by Design Principles

| Principle | Application to AI |
|-----------|------------------|
| Minimize attack surface | Limit model capabilities to what's needed |
| Establish secure defaults | Guardrails enabled, permissions restrictive by default |
| Defense in depth | Multiple independent security layers |
| Fail securely | Return safe fallback on errors, not raw errors |
| Separation of privilege | Agents get separate credentials per tool |
| Economy of mechanism | Simple, auditable prompt structures |
| Complete mediation | Validate every input/output, no bypass paths |

## AI-Specific Design Decisions

### Architecture Choices
- Choose model size appropriate to task (don't over-provision capabilities)
- Prefer structured outputs over free-form generation
- Design for graceful degradation (fallback to rule-based systems)
- Separate data plane from control plane

### Prompt Design
- Use clear instruction boundaries
- Avoid including sensitive data in system prompts
- Design prompts that are resistant to injection
- Version control all prompts

### Data Flow Design
- Classify data sensitivity at pipeline entry
- Implement data minimization (only retrieve what's needed)
- Design for auditability (every data access logged)
- Plan for data deletion (model unlearning capability)

## Security Requirements Checklist

- [ ] Threat model completed before development
- [ ] Security requirements documented alongside functional requirements
- [ ] Data classification scheme defined
- [ ] Access control model designed
- [ ] Guardrail strategy selected
- [ ] Monitoring and alerting planned
- [ ] Incident response procedures drafted
- [ ] Security testing integrated into CI/CD

## Related Resources

- [Academy Module 9 — Secure SDLC](../../airline-labs/academy/module-09-secure-sdlc.md)

---

| [← Previous](../08-enterprise-architecture/) | [Back to Module](README.md) | [Next →](02-threat-modeling.md) |
