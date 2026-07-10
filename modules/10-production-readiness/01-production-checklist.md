# Production Security Checklist

Security requirements that must be met before an AI system goes live.

## Overview

This checklist provides mandatory and recommended security controls for AI systems prior to production deployment. No AI system should be deployed without completing all mandatory items.

## Pre-Production Checklist

### Mandatory (Must Pass)

| # | Requirement | Evidence Required |
|---|------------|-------------------|
| 1 | Security review completed | Signed review document |
| 2 | Input validation implemented | Test results showing injection blocking |
| 3 | Output filtering enabled | Test results showing PII/policy filtering |
| 4 | Access controls configured | RBAC policy documentation |
| 5 | Guardrails active | Regression test suite passing |
| 6 | Monitoring configured | Dashboard screenshot, alert rules |
| 7 | Incident response plan | Documented playbook |
| 8 | Cost controls set | Budget caps, alerts configured |
| 9 | Logging enabled (sanitized) | Log sample review |
| 10 | Model provenance verified | Signatures, scan results |
| 11 | Data classification complete | Classification labels assigned |
| 12 | Rollback mechanism tested | Rollback drill results |

### Recommended (Should Complete)

| # | Requirement | Priority |
|---|------------|----------|
| 13 | Red team exercise completed | High |
| 14 | Load testing performed | High |
| 15 | Disaster recovery tested | Medium |
| 16 | AI-SBOM generated | Medium |
| 17 | Third-party audit scheduled | Medium |
| 18 | User feedback mechanism | Low |

## Approval Workflow

1. **Development team** — Completes checklist and provides evidence
2. **Security team** — Reviews evidence, performs spot checks
3. **Privacy/Legal** — Confirms regulatory compliance
4. **Architecture review** — Validates design decisions
5. **Sign-off** — Authorized approver grants production access

## Post-Deployment Verification

- Verify monitoring is receiving data within 1 hour
- Confirm alerting triggers on test scenarios
- Validate rate limiting and cost controls work
- Run smoke test against production endpoint
- Verify rollback mechanism from production

## Related Resources

- [Academy Module 10 — Production Readiness](../../airline-labs/academy/module-10-production-readiness.md)

---

| [← Previous](../09-secure-ai-sdlc/) | [Back to Module](README.md) | [Next →](02-hardening.md) |
