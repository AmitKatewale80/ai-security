# Hardening AI Systems for Production

Security hardening measures to reduce attack surface and increase resilience of production AI systems.

## Overview

Hardening transforms a development AI system into a production-ready one by eliminating unnecessary capabilities, tightening configurations, and implementing defense-in-depth.

## Hardening Checklist

### Model Layer

| Control | Description | Priority |
|---------|-------------|----------|
| Remove debug endpoints | No model introspection in production | Critical |
| Disable verbose errors | Return generic errors to users | Critical |
| Limit model capabilities | Restrict to required functions only | High |
| Set temperature bounds | Prevent adversarial temperature manipulation | Medium |
| Pin model version | No automatic model updates | High |
| Enable content filtering | Platform-level safety filters | Critical |

### Infrastructure Layer

| Control | Description | Priority |
|---------|-------------|----------|
| Private endpoints | No public internet exposure | Critical |
| Network segmentation | AI workloads isolated | High |
| mTLS between services | Encrypted internal communication | High |
| Egress filtering | Allowlist-only outbound connections | High |
| Resource limits | CPU, memory, GPU caps per workload | Medium |
| Secrets management | No hardcoded credentials | Critical |

### Application Layer

| Control | Description | Priority |
|---------|-------------|----------|
| Input validation | Multi-layer validation pipeline | Critical |
| Output filtering | PII, policy, safety filters | Critical |
| Rate limiting | Token and request limits | High |
| Session management | Secure session handling | High |
| CORS configuration | Restrict allowed origins | Medium |
| Security headers | Standard HTTP security headers | Medium |

## Hardening Process

1. **Baseline** — Document current configuration
2. **Assess** — Identify deviations from security standards
3. **Remediate** — Apply hardening controls
4. **Verify** — Test that controls work (penetration test)
5. **Document** — Record final hardened state
6. **Monitor** — Alert on configuration drift

## Related Resources

- [Academy Module 10 — Production Readiness](../../airline-labs/academy/module-10-production-readiness.md)

---

| [← Previous](01-production-checklist.md) | [Back to Module](README.md) | [Next →](03-disaster-recovery.md) |
