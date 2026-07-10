# AI Telemetry, SIEM Integration & Log Sanitization

Capturing AI-specific telemetry, integrating with SIEM platforms, and sanitizing logs to prevent data leakage.

## Overview

AI systems generate unique telemetry that must be captured, sanitized, and analyzed alongside traditional security logs. Proper logging enables detection, investigation, and compliance while avoiding sensitive data exposure in log stores.

## What to Log

| Event Type | Data Points | Sensitivity |
|-----------|-------------|-------------|
| Input events | Prompt hash, length, classification result | Low (if hashed) |
| Output events | Response classification, token count, latency | Low |
| Security events | Guardrail triggers, injection detections, blocks | Medium |
| Access events | User ID, role, endpoint, timestamp | Medium |
| Model events | Version, confidence scores, errors | Low |
| Cost events | Tokens consumed, API costs, budget usage | Low |

## Log Sanitization Requirements

**Never log raw prompts or responses** — they may contain PII, secrets, or sensitive business data.

### Sanitization Techniques
- Hash or tokenize user inputs before logging
- Redact PII from log entries using NER
- Truncate long content to fixed lengths
- Use reference IDs instead of inline content
- Encrypt sensitive fields at rest

## SIEM Integration Architecture

```
AI System → Log Collector → Sanitization Pipeline → SIEM
                                                      ↓
                                              Correlation Rules
                                                      ↓
                                              Alert → SOC Team
```

## SIEM Detection Rules

1. **Injection burst** — N+ guardrail triggers from same user in T minutes
2. **Extraction pattern** — Systematic queries targeting data boundaries
3. **Cost anomaly** — Token usage exceeds N× historical average
4. **Auth anomaly** — Access from unusual context/location
5. **Model probing** — Repeated boundary-testing queries

## Implementation Checklist

- [ ] Define log schema for AI events
- [ ] Implement sanitization pipeline
- [ ] Configure log rotation and retention
- [ ] Build SIEM correlation rules
- [ ] Create SOC runbooks for AI alerts
- [ ] Test alert pipeline end-to-end

## Related Labs

- [Lab 15 — AI SOC Security](../../airline-labs/lab-15-ai-soc-security/) — SOC integration for AI monitoring

## Related Academy Module

- [Academy Module 7 — Continuous Security](../../airline-labs/academy/module-07-continuous-security.md)

---

| [← Previous](04-red-teaming.md) | [Back to Module](README.md) | [Next →](06-model-drift.md) |
