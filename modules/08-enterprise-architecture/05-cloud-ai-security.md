# Cloud AI Platform Security

Securing managed AI services: AWS Bedrock, Azure OpenAI, GCP Vertex AI, and other cloud AI platforms.

## Overview

Cloud AI platforms provide managed model hosting, but security remains a shared responsibility. Understanding the security boundaries and available controls for each platform is critical.

## Shared Responsibility Model

| Responsibility | Cloud Provider | Customer |
|---------------|---------------|----------|
| Physical infrastructure | ✓ | |
| Model hosting platform | ✓ | |
| Model availability | ✓ | |
| API authentication | ✓ (mechanisms) | ✓ (configuration) |
| Data encryption in transit | ✓ | |
| Data encryption at rest | ✓ (default) | ✓ (key management) |
| Input/output security | | ✓ |
| Access control policies | | ✓ |
| Content filtering config | | ✓ |
| Monitoring and alerting | ✓ (tools) | ✓ (configuration) |
| Compliance | ✓ (certifications) | ✓ (usage compliance) |

## Platform Security Features

### AWS Bedrock
- VPC endpoints for private access
- IAM policies for model/knowledge base access
- CloudTrail logging for all API calls
- Guardrails for content filtering
- Model invocation logging (opt-in)

### Azure OpenAI
- Private endpoints and VNet integration
- Azure AD authentication and RBAC
- Content filtering (configurable severity levels)
- Diagnostic logging to Log Analytics
- Customer-managed keys for fine-tuned models

### GCP Vertex AI
- VPC Service Controls for data perimeter
- IAM with fine-grained model permissions
- CMEK for data encryption
- Audit logging via Cloud Logging
- DLP integration for PII protection

## Security Best Practices

1. **Private networking** — Use VPC endpoints, never public internet
2. **Least privilege IAM** — Scope permissions to specific models
3. **Enable all logging** — Model invocation logs, audit trails
4. **Customer-managed keys** — Control encryption key lifecycle
5. **Content filtering** — Enable and configure platform guardrails
6. **Budget alerts** — Set hard limits on API spend
7. **Network controls** — Restrict egress from AI workloads

## Related Resources

- [Academy Module 8 — Enterprise Architecture](../../airline-labs/academy/module-08-enterprise-architecture.md)

---

| [← Previous](04-multi-tenant.md) | [Back to Module](README.md) | [Next →](06-network-security.md) |
