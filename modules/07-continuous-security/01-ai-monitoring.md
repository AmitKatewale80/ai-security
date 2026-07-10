# AI System Monitoring

What to monitor in AI systems: injection attempts, cost anomalies, model drift, and operational health.

## Overview

AI systems require monitoring beyond traditional application metrics. Security teams must track AI-specific signals to detect attacks, abuse, and degradation in real-time.

## What to Monitor

| Category | Metrics | Alert Threshold |
|----------|---------|-----------------|
| Security | Injection attempts, guardrail triggers | Spike above baseline |
| Cost | Token consumption, API spend | Budget % or rate anomaly |
| Performance | Latency, error rates, throughput | SLA breach |
| Quality | Hallucination rate, user satisfaction | Quality score drop |
| Drift | Output distribution changes | Statistical threshold |
| Abuse | Rate limiting hits, repeated failures | Pattern-based |

## Key Monitoring Signals

### Security Signals
- Guardrail trigger frequency and patterns
- Failed input validation attempts
- Unusual prompt lengths or encodings
- Repeated similar queries (extraction attempts)
- System prompt probing patterns

### Operational Signals
- Token usage per user/session
- Response generation time percentiles
- Model endpoint availability
- Queue depth and processing backlog
- Error rates by error type

### Business Signals
- Cost per interaction trending
- User satisfaction scores
- Task completion rates
- Escalation to human frequency

## Monitoring Architecture

```
AI System → Telemetry Collector → Stream Processing → Alert Engine
                                         ↓
                                    Dashboard/SIEM
                                         ↓
                                   Incident Response
```

## Implementation Priorities

1. Start with cost monitoring (immediate business impact)
2. Add security event logging (injection attempts)
3. Implement quality metrics (hallucination detection)
4. Build drift detection (model degradation)
5. Integrate with existing SIEM/SOAR

## Related Labs

- [Lab 17 — AI Cost Governance](../../airline-labs/lab-17-ai-cost-governance/) — Cost monitoring and abuse detection

## Related Academy Module

- [Academy Module 7 — Continuous Security](../../airline-labs/academy/module-07-continuous-security.md)

---

| [← Previous](../06-ai-governance/) | [Back to Module](README.md) | [Next →](02-anomaly-detection.md) |
