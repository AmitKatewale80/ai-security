# Multi-Tenant AI Security

Isolating tenants in shared AI infrastructure to prevent cross-tenant data leakage and resource abuse.

## Overview

Multi-tenant AI platforms serve multiple customers or business units on shared infrastructure. Without proper isolation, one tenant's data or queries can leak into another tenant's responses.

## Isolation Layers

| Layer | Isolation Method | Strength | Cost |
|-------|-----------------|----------|------|
| Model | Separate model per tenant | Very High | Very High |
| Fine-tune | Tenant-specific fine-tunes | High | High |
| Context | Separate system prompts/RAG | Medium | Low |
| Data | Separate vector DB collections | High | Medium |
| Compute | Dedicated inference instances | Very High | Very High |
| Network | VPC/subnet isolation | High | Medium |
| Logical | Metadata filtering at query time | Medium | Low |

## Cross-Tenant Attack Vectors

1. **Prompt leakage** — Tenant A's system prompt exposed to Tenant B
2. **RAG contamination** — Documents from Tenant A retrieved for Tenant B
3. **Model memorization** — Fine-tuned model recalls other tenant's data
4. **Cache poisoning** — Shared caches serve wrong tenant's data
5. **Resource exhaustion** — One tenant starves others (noisy neighbor)

## Security Controls

### Data Isolation
- Tenant ID on all data records (enforced at DB layer)
- Separate encryption keys per tenant
- Row-level security in vector databases
- Audit cross-tenant query attempts

### Compute Isolation
- Resource quotas per tenant
- Separate inference endpoints for sensitive tenants
- Burst limiting to prevent noisy neighbor
- Dedicated GPU allocation for premium tiers

### Access Control
- Tenant-scoped API keys
- Cross-tenant access denied by default
- Admin access requires multi-party approval
- Tenant isolation testing in CI/CD

## Validation Checklist

- [ ] No shared state between tenant requests
- [ ] Tenant ID enforced at data layer (not just application)
- [ ] Separate encryption keys per tenant
- [ ] Resource limits prevent cross-tenant impact
- [ ] Regular penetration testing for isolation bypass

## Related Labs

- [Lab 13 — AI Gateway Security](../../airline-labs/lab-13-ai-gateway-security/) — Tenant isolation at the gateway layer

## Related Academy Module

- [Academy Module 8 — Enterprise Architecture](../../airline-labs/academy/module-08-enterprise-architecture.md)

---

| [← Previous](03-zero-trust-ai.md) | [Back to Module](README.md) | [Next →](05-cloud-ai-security.md) |
