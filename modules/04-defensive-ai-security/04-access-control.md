# Access Control for AI Systems

Role-based access control (RBAC) and document classification strategies for AI systems that handle sensitive data.

## Overview

AI systems often access multiple data sources with varying sensitivity levels. Without proper access control, an LLM can become an unauthorized path to restricted information.

## Access Control Layers

| Layer | Purpose | Implementation |
|-------|---------|----------------|
| User authentication | Verify identity | OAuth 2.0, SAML, API keys |
| Role-based access | Limit by role | RBAC policies per endpoint |
| Document classification | Tag data sensitivity | Labels: Public, Internal, Confidential, Restricted |
| Query-time filtering | Filter context by user role | Pre-retrieval ACL checks |
| Response redaction | Remove unauthorized content | Post-generation filtering |

## Document Classification for RAG

1. **Label all documents** with sensitivity levels at ingestion
2. **Store ACL metadata** alongside embeddings in vector DB
3. **Filter at retrieval time** — only return documents the user can access
4. **Validate at generation time** — cross-check output against user permissions
5. **Audit access patterns** — log who accessed what and when

## RBAC Design Principles

- **Least privilege** — Users get minimum access needed
- **Separation of duties** — No single role has full access
- **Role hierarchy** — Inherit permissions from parent roles
- **Temporal access** — Time-bound elevated permissions
- **Context-aware** — Adjust access based on request context

## Common Pitfalls

- Applying ACLs only at the UI layer (LLM can bypass)
- Trusting the LLM to self-enforce access rules
- Not filtering RAG context before injection into prompt
- Shared API keys across different user roles

## Related Labs

- [Lab 04 — RAG Data Extraction](../../airline-labs/lab-04-rag-data-extraction/) — ACL bypass in RAG systems
- [Lab 13 — AI Gateway Security](../../airline-labs/lab-13-ai-gateway-security/) — Gateway-level access control

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](03-guardrails.md) | [Back to Module](README.md) | [Next →](05-rag-security.md) |
