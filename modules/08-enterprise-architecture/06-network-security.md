# Network Security for AI Systems

Network segmentation, mutual TLS, egress filtering, and secure communication patterns for AI workloads.

## Overview

AI systems introduce new network flows — model API calls, embedding generation, vector database queries, and agent-to-tool communication. Each flow must be secured and controlled.

## AI Network Flows

| Flow | Source | Destination | Risk |
|------|--------|-------------|------|
| Client → Gateway | User applications | AI gateway | Injection, DDoS |
| Gateway → Model | AI gateway | Model endpoint | Data exposure |
| Model → Tools | AI agent | External APIs | Exfiltration |
| App → Vector DB | Application | Vector database | Data theft |
| Training → Storage | ML pipeline | Data lake | Data leakage |
| Model → Model | Orchestrator | Multiple models | Cascade attacks |

## Segmentation Strategy

### Zone Architecture
```
┌─────────────────┐   ┌──────────────────┐   ┌────────────────┐
│   User Zone     │──▶│   AI DMZ         │──▶│  Model Zone    │
│   (Untrusted)   │   │   (Gateway)      │   │  (Restricted)  │
└─────────────────┘   └──────────────────┘   └────────────────┘
                                                      │
                                              ┌───────▼────────┐
                                              │   Data Zone    │
                                              │   (Isolated)   │
                                              └────────────────┘
```

## Security Controls

### Mutual TLS (mTLS)
- Encrypt all model-to-model communication
- Certificate-based identity verification
- Automatic certificate rotation
- Service mesh integration (Istio, Linkerd)

### Egress Filtering
- Allowlist external APIs agents can reach
- Block all outbound by default
- Inspect egress for data exfiltration patterns
- DNS filtering for model-initiated requests

### DDoS and Rate Protection
- Layer 7 filtering specific to AI payloads
- Token-aware rate limiting (not just request count)
- Geographic restrictions where applicable
- Automated scaling with cost caps

## Implementation Priorities

1. Segment model serving from general workloads
2. Implement mTLS between AI components
3. Enforce egress allowlists for AI agents
4. Enable network flow logging and anomaly detection
5. Deploy WAF rules specific to AI traffic patterns

## Related Resources

- [Academy Module 8 — Enterprise Architecture](../../airline-labs/academy/module-08-enterprise-architecture.md)

---

| [← Previous](05-cloud-ai-security.md) | [Back to Module](README.md) | [Next →](../09-secure-ai-sdlc/) |
