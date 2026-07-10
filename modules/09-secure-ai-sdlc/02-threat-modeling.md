# Threat Modeling for AI Systems

Extending STRIDE and other methodologies with AI-specific threats, plus templates for common AI architectures.

## Overview

Threat modeling identifies potential threats early in the design phase. AI systems introduce novel threats that traditional frameworks don't cover — requiring extensions to STRIDE, PASTA, and other methodologies.

## STRIDE + AI Extensions

| Category | Traditional | AI Extension |
|----------|-----------|--------------|
| **S**poofing | Identity impersonation | Model impersonation, synthetic identity |
| **T**ampering | Data modification | Training data poisoning, model weight manipulation |
| **R**epudiation | Denying actions | AI-generated content attribution |
| **I**nformation Disclosure | Data leakage | Model inversion, prompt extraction, RAG leakage |
| **D**enial of Service | System unavailability | Denial-of-wallet, adversarial examples causing loops |
| **E**levation of Privilege | Unauthorized access | Prompt injection gaining system capabilities |

## AI Threat Modeling Process

1. **Decompose** — Map AI system components and data flows
2. **Identify trust boundaries** — Where does trusted/untrusted data flow?
3. **Enumerate threats** — Use STRIDE+AI for each component
4. **Assess risk** — Score likelihood × impact
5. **Plan mitigations** — Map threats to controls
6. **Validate** — Test mitigations through red teaming

## Common AI Data Flow Diagram Elements

- User input boundary (untrusted)
- Prompt construction (injection risk)
- Model inference (black box)
- Tool/function calls (privilege boundary)
- RAG retrieval (data access boundary)
- Output delivery (leakage boundary)

## Threat Model Template

| Component | Threat | STRIDE Category | Likelihood | Impact | Mitigation |
|-----------|--------|----------------|-----------|--------|------------|
| User input | Prompt injection | Elevation | High | High | Input validation, guardrails |
| RAG pipeline | Data poisoning | Tampering | Medium | High | Source verification, monitoring |
| Agent tools | Unauthorized actions | Elevation | Medium | Critical | Policy engine, sandboxing |

## Related Resources

- [Academy Module 9 — Secure SDLC](../../airline-labs/academy/module-09-secure-sdlc.md)

---

| [← Previous](01-security-by-design.md) | [Back to Module](README.md) | [Next →](03-secure-development.md) |
