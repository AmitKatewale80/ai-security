# Cost Abuse Prevention

Defending against denial-of-wallet attacks, implementing budget caps, and detecting runaway cost loops.

## Overview

AI APIs are expensive. Attackers (or bugs) can cause massive bills through denial-of-wallet attacks, prompt loops, or resource exhaustion. Cost abuse prevention is a critical production security control.

## Attack Vectors

| Attack | Mechanism | Potential Cost Impact |
|--------|-----------|---------------------|
| Denial-of-wallet | Flood API with expensive requests | $10K–$100K+ per hour |
| Token amplification | Craft inputs that maximize output tokens | 10–100× normal cost |
| Loop induction | Trigger agent loops that never terminate | Unbounded |
| Model upgrade abuse | Force routing to expensive models | 5–50× cost increase |
| Batch processing abuse | Submit massive batch jobs | Project budget exhaustion |

## Cost Control Layers

### Layer 1: Request Level
- Maximum input token limit per request
- Maximum output token limit per request
- Timeout on all model calls
- Token-aware rate limiting

### Layer 2: Session Level
- Maximum tokens per user session
- Maximum requests per session
- Session duration limits
- Anomaly detection on session costs

### Layer 3: Budget Level
- Hard budget caps per user/team/project
- Soft alerts at 50%, 80%, 90% of budget
- Automatic throttling at budget limit
- Emergency kill switch at hard cap

### Layer 4: System Level
- Global spend rate monitoring
- Circuit breaker on cost velocity
- Automatic scaling limits
- Provider spend alerts (AWS/Azure/GCP)

## Loop Detection

- Track agent step count (max iterations)
- Detect repeated tool calls with same parameters
- Monitor conversation turn length
- Set time-based execution limits
- Alert on recursive pattern detection

## Implementation Checklist

- [ ] Token limits set on all endpoints
- [ ] Budget caps configured per team/project
- [ ] Kill switch mechanism tested
- [ ] Loop detection implemented
- [ ] Cost alerting configured
- [ ] Monthly cost review process established

## Related Labs

- [Lab 17 — AI Cost Governance](../../airline-labs/lab-17-ai-cost-governance/) — Cost monitoring and denial-of-wallet defense

## Related Academy Module

- [Academy Module 10 — Production Readiness](../../airline-labs/academy/module-10-production-readiness.md)

---

| [← Previous](04-scaling-security.md) | [Back to Module](README.md) | [Next →](06-security-maturity.md) |
