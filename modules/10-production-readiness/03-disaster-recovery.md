# Disaster Recovery for AI Systems

Backup, recovery, and rollback strategies for AI models, data, and infrastructure.

## Overview

AI systems have unique disaster recovery requirements: model weights must be versioned, vector databases need consistent snapshots, and recovery must maintain model-data alignment.

## AI Recovery Targets

| Component | RPO | RTO | Backup Strategy |
|-----------|-----|-----|-----------------|
| Model weights | 0 (immutable versions) | < 15 min | Model registry versioning |
| Vector database | < 1 hour | < 30 min | Continuous replication |
| Configuration | 0 (GitOps) | < 5 min | Git-based config management |
| Knowledge base | < 4 hours | < 1 hour | Scheduled snapshots |
| Prompts/guardrails | 0 (version controlled) | < 5 min | Git repository |
| Conversation history | < 1 hour | < 2 hours | Database replication |
| Audit logs | 0 (append-only) | < 1 hour | Immutable log storage |

## Rollback Scenarios

| Scenario | Action | Validation |
|----------|--------|------------|
| Model regression | Revert to previous model version | Run evaluation suite |
| Poisoned knowledge base | Restore from clean snapshot | Verify content integrity |
| Guardrail failure | Activate stricter fallback config | Run injection test suite |
| Cost runaway | Kill switch + restore rate limits | Monitor cost metrics |
| Full compromise | Isolate, restore from gold image | Full security assessment |

## Disaster Recovery Plan

### Preparation
- Version all models in immutable registry
- Automate knowledge base snapshots
- Store configuration as infrastructure-as-code
- Maintain "last known good" markers
- Document recovery procedures

### Execution
1. **Detect** — Automated monitoring triggers alert
2. **Assess** — Determine scope and severity
3. **Decide** — Rollback vs. fix-forward
4. **Execute** — Run recovery procedure
5. **Validate** — Verify restored system behavior
6. **Communicate** — Notify stakeholders

### Testing
- Monthly rollback drills
- Quarterly full DR exercise
- Annual chaos engineering for AI systems

## Related Resources

- [Academy Module 10 — Production Readiness](../../airline-labs/academy/module-10-production-readiness.md)

---

| [← Previous](02-hardening.md) | [Back to Module](README.md) | [Next →](04-scaling-security.md) |
