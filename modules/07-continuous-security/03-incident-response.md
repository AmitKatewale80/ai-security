# AI Incident Response

Playbooks, classification systems, and kill switches for responding to AI security incidents.

## Overview

AI incidents require specialized response procedures beyond traditional security playbooks. Responders must understand model behavior, data flows, and the unique ways AI systems can fail or be compromised.

## AI Incident Classification

| Severity | Definition | Examples | Response Time |
|----------|-----------|----------|---------------|
| Critical | Active exploitation, data breach | Model exfiltrating PII, agent executing unauthorized actions | Immediate |
| High | Confirmed vulnerability, potential impact | Guardrail bypass discovered, poisoned data detected | < 1 hour |
| Medium | Degraded security posture | Drift detected, elevated injection attempts | < 4 hours |
| Low | Minor anomaly, no confirmed impact | Unusual usage patterns, minor quality degradation | < 24 hours |

## Kill Switch Mechanisms

1. **Model endpoint shutdown** — Disable inference endpoint
2. **Fallback activation** — Route to safe fallback (rule-based system)
3. **Guardrail escalation** — Tighten guardrails to maximum
4. **Rate limiting** — Throttle to near-zero throughput
5. **Feature flags** — Disable specific capabilities
6. **Network isolation** — Cut model from external resources

## Incident Response Playbook Template

### Phase 1: Detection & Triage
- Identify the affected system and scope
- Classify severity using AI incident criteria
- Activate kill switch if active exploitation

### Phase 2: Containment
- Isolate compromised model/data
- Preserve evidence (logs, prompts, outputs)
- Switch to fallback systems

### Phase 3: Investigation
- Analyze attack vector and impact
- Determine data exposure scope
- Identify root cause

### Phase 4: Recovery
- Deploy patched/retrained model
- Validate guardrails effectiveness
- Restore normal operations gradually

### Phase 5: Post-Incident
- Document lessons learned
- Update detection rules
- Improve response procedures

## Related Resources

- [Academy Module 7 — Continuous Security](../../airline-labs/academy/module-07-continuous-security.md)

---

| [← Previous](02-anomaly-detection.md) | [Back to Module](README.md) | [Next →](04-red-teaming.md) |
