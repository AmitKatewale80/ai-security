# 🏗️ Module 8: Enterprise AI Architecture

> Designing secure AI platforms that scale across the organization.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 7: Continuous Security](module-07-continuous-security.md) | Module 8 of 10 | [Module 9: Secure AI SDLC](module-09-secure-sdlc.md) |

---

## Learning Objectives

After this module, you will be able to:
- Design a secure AI Gateway architecture
- Implement AI Mesh patterns for multi-agent systems
- Architect enterprise RAG with security controls
- Apply identity and access management to AI systems
- Manage secrets and credentials for AI infrastructure
- Evaluate AI platform security considerations

---

## 8.1 AI Gateway Architecture

### Gateway Position in the Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     EXTERNAL USERS                            │
│         Passengers │ Agents │ Partners │ Internal Staff       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    LOAD BALANCER     │
                    └──────────┬──────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                       AI GATEWAY                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  AUTH   │ │  RATE   │ │ ROUTING │ │ POLICY  │          │
│  │         │ │ LIMITING│ │         │ │ ENGINE  │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ INPUT   │ │ OUTPUT  │ │  COST   │ │  AUDIT  │          │
│  │ FILTER  │ │ FILTER  │ │TRACKING │ │ LOGGING │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
└──────────────────────────────┬──────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
┌─────────▼──┐    ┌───────────▼──┐    ┌───────────▼──┐
│ CUSTOMER   │    │   REVENUE    │    │    CREW      │
│ CHATBOT    │    │  OPTIMIZER   │    │  SCHEDULER   │
│ (Public)   │    │ (Internal)   │    │ (Restricted) │
└────────────┘    └──────────────┘    └──────────────┘
```

### Gateway Security Policies

```yaml
gateway_policies:
  authentication:
    method: OAuth2 + JWT
    token_binding: ip + user_agent
    rotation: every 24 hours
    
  rate_limiting:
    default: 60 requests/minute
    per_model:
      customer_chatbot: 100/min (high volume, low risk)
      revenue_optimizer: 20/min (low volume, high value)
      crew_scheduler: 10/min (restricted)
    burst_allowed: 2x for 10 seconds
    
  routing:
    header_overrides: DISABLED (never trust client headers)
    path_sanitization: reject "../" and absolute paths
    model_names: whitelist only (no wildcards)
    
  budget:
    per_token_daily: $50 (customer), $200 (internal), $500 (ops)
    per_model_daily: $1000 (chatbot), $500 (revenue), $200 (crew)
    alert_threshold: 80% of budget
    hard_stop: 100% of budget
    
  input_filtering:
    max_tokens: 4096
    injection_detection: enabled
    encoding_detection: enabled (base64, hex)
    
  output_filtering:
    pii_detection: enabled
    max_response_tokens: 2048
    content_policy: enabled
```

---

## 8.2 AI Mesh — Multi-Agent Architecture

### What Is AI Mesh?

A pattern for running multiple AI agents that need to collaborate while maintaining security isolation.

```
┌──────────────────────────────────────────────────────────┐
│                      AI MESH                              │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │ BOOKING  │    │   OPS    │    │  MAINT   │           │
│  │  AGENT   │    │  AGENT   │    │  AGENT   │           │
│  │          │    │          │    │          │           │
│  │ Tools:   │    │ Tools:   │    │ Tools:   │           │
│  │ - book   │    │ - rebook │    │ - inspect│           │
│  │ - search │    │ - gate   │    │ - ground │           │
│  │ - loyalty│    │ - crew   │    │ - sensor │           │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘           │
│       │               │               │                  │
│       └───────┬───────┴───────┬───────┘                  │
│               │               │                          │
│       ┌───────▼───────┐ ┌────▼─────────┐                │
│       │ TOOL REGISTRY │ │ POLICY ENGINE │                │
│       │ (per-agent    │ │ (enforces     │                │
│       │  access only) │ │  boundaries)  │                │
│       └───────────────┘ └──────────────┘                 │
│                                                           │
│       ┌───────────────┐ ┌──────────────┐                │
│       │ IDENTITY (IAM)│ │  AUDIT LOG   │                │
│       │ (per-agent ID)│ │ (immutable)  │                │
│       └───────────────┘ └──────────────┘                 │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Mesh Security Principles

| Principle | Implementation | Prevents |
|-----------|---------------|----------|
| **Identity isolation** | Each agent has unique credentials | Cross-agent impersonation |
| **Tool scoping** | Agent only sees its own tools | Privilege escalation (Lab 16) |
| **Communication control** | Agents communicate via message bus, not direct calls | Unauthorized data flow |
| **Blast radius containment** | Compromised agent cannot affect other domains | Cascade failures |
| **Credential rotation** | Agent credentials rotate every 4 hours | Credential theft |

### Inter-Agent Communication

```
ALLOWED: Booking agent → Message bus → Ops agent
  "Passenger Chen needs rebooking to QA-448"
  (Structured message, validated schema, logged)

BLOCKED: Booking agent → Direct tool call → maintenance.shutdown_engine()
  (Cross-domain tool access denied)

ALLOWED: Ops agent → Escalation → Human dispatcher
  "Flight QA-447 cancellation requires approval"
  (Human-in-loop for dangerous actions)
```

---

## 8.3 Enterprise RAG Architecture

### Secure RAG Reference Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURE ENTERPRISE RAG                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INGESTION PIPELINE              QUERY PIPELINE              │
│  ──────────────────              ─────────────               │
│                                                              │
│  Document → [Auth]               User query → [Auth]         │
│          → [Classify]                      → [Role check]    │
│          → [Provenance tag]                → [Embed]         │
│          → [Injection scan]                → [Retrieve]      │
│          → [Multi-source verify]           → [Filter by ACL] │
│          → [Embed + Index]                 → [LLM generate]  │
│          → [Changelog]                     → [Output filter] │
│                                            → [Citation]      │
│                                            → [Respond]       │
│                                                              │
│  STORAGE                         MONITORING                  │
│  ───────                         ──────────                  │
│  Vector DB (with ACL metadata)   Change alerts               │
│  Document store (versioned)      Query anomaly detection     │
│  Provenance records              Access pattern analysis     │
│  Classification labels           Contradiction detection     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Document Classification Enforcement

```python
# Every document in the vector DB has metadata:
document_metadata = {
    "classification": "CONFIDENTIAL",
    "department": "safety",
    "author": "safety-board-001",
    "provenance": "signed by: J. Wilson, Safety Director",
    "ingestion_date": "2024-03-15",
    "verified_sources": 3,
    "allowed_roles": ["safety_investigator", "security_officer"]
}

# At query time:
def retrieve_with_acl(query, user_role):
    results = vector_db.search(query, top_k=10)
    filtered = [doc for doc in results 
                if user_role in doc.metadata["allowed_roles"]]
    return filtered
```

---

## 8.4 Identity for AI Systems

### AI Identity Architecture

```
┌────────────────────────────────────────────────────┐
│              AI IDENTITY LAYER                       │
├────────────────────────────────────────────────────┤
│                                                     │
│  AGENT IDENTITIES          TOKEN MANAGEMENT         │
│  ────────────────          ────────────────         │
│  booking-agent-001         JWT with:                │
│  booking-agent-002           - agent_id             │
│  ops-agent-001               - role                 │
│  maintenance-agent-001       - allowed_tools        │
│  revenue-agent-001           - budget_limit         │
│                              - expiry (4h)          │
│                              - ip_binding           │
│                                                     │
│  ROLE-BASED ACCESS          AUDIT IDENTITY          │
│  ─────────────────          ──────────────          │
│  booking_role:              Every action tagged:     │
│    - book_flight ✓            who: ops-agent-001    │
│    - check_loyalty ✓          what: rebook_pax      │
│    - cancel_flight ✗          when: 2024-06-15T14:22│
│    - shutdown_engine ✗        why: "IROPS QA-447"   │
│                               approved_by: human/auto│
│                                                     │
└────────────────────────────────────────────────────┘
```

### Identity Best Practices

1. **No shared identities** — Each agent instance has its own credentials
2. **Credential rotation** — Tokens expire every 4 hours, auto-renewed
3. **IP binding** — Token only works from the expected compute instance
4. **Audit attribution** — Every action traceable to specific agent identity
5. **Revocation** — Can revoke one agent without affecting others
6. **Blast radius** — Compromised identity affects only that agent's scope

---

## 8.5 Secrets Management

### Secrets in AI Systems

| Secret Type | Example | Storage | Rotation |
|------------|---------|---------|----------|
| LLM API keys | OpenAI/Anthropic keys | Vault (HashiCorp/AWS SM) | 30 days |
| Agent credentials | JWT signing keys | Vault | 4 hours |
| Database connections | PostgreSQL URI | Vault | 90 days |
| PII tokenization salt | SHA-256 salt | HSM (isolated) | Never (break glass) |
| Model signing keys | ECDSA private key | HSM | 365 days |
| Encryption keys | Data-at-rest keys | KMS | 365 days |

### Secret Architecture

```
┌─────────────────────────────────────────────┐
│           SECRETS MANAGEMENT                 │
├─────────────────────────────────────────────┤
│                                              │
│  AI APPLICATION                              │
│       │                                      │
│       │ (request secret at runtime)          │
│       ▼                                      │
│  ┌─────────────┐                             │
│  │ SECRETS SDK │ (no secrets in code/config) │
│  └──────┬──────┘                             │
│         │                                    │
│         ▼                                    │
│  ┌─────────────┐    ┌──────────────┐        │
│  │   VAULT     │───▶│   AUDIT LOG  │        │
│  │ (HashiCorp  │    │ (who accessed │        │
│  │  or AWS SM) │    │  what, when)  │        │
│  └──────┬──────┘    └──────────────┘        │
│         │                                    │
│         ▼ (signing keys only)                │
│  ┌─────────────┐                             │
│  │     HSM     │ (hardware security module)  │
│  │ (FIPS 140-2)│                             │
│  └─────────────┘                             │
│                                              │
│  RULES:                                      │
│  • No secrets in environment variables       │
│  • No secrets in config files or code        │
│  • No secrets in model artifacts             │
│  • No secrets in log output                  │
│  • Secrets fetched at runtime, cached 5 min  │
│                                              │
└─────────────────────────────────────────────┘
```

---

## 8.6 AI Platform Security

### Security Checklist for AI Platforms

```
COMPUTE SECURITY
  □ AI workloads run in isolated containers/VMs
  □ GPU nodes in separate network segment
  □ No internet access from training environment
  □ Model artifacts stored in encrypted storage
  □ Inference endpoints behind WAF + AI Gateway

NETWORK SECURITY
  □ AI services not directly internet-accessible
  □ mTLS between all AI microservices
  □ Network segmentation: training ≠ inference ≠ data
  □ Egress filtering (models can't call external URLs)
  □ DNS filtering (block known exfiltration domains)

DATA SECURITY
  □ Training data encrypted at rest
  □ PII tokenized before ML pipeline
  □ Access logging on all data stores
  □ Data lineage tracked end-to-end
  □ Regular data classification reviews

MODEL SECURITY
  □ Model registry with access controls
  □ Cryptographic signatures on all models
  □ Integrity verification before every load
  □ Supply chain scanning for external models
  □ Version control with rollback capability

OPERATIONAL SECURITY
  □ Least privilege for all service accounts
  □ MFA for human access to AI infrastructure
  □ Automated vulnerability scanning
  □ Regular penetration testing
  □ Incident response playbooks for AI-specific scenarios
```

---

## 🧪 Module 8 Exercise

**Architecture Review:**

Draw the AI architecture for one of your airline's AI systems including:
1. All data flows (user → gateway → model → response)
2. Where secrets are stored and how they're accessed
3. Identity and access control boundaries
4. Monitoring and audit points
5. Kill switch location and activation path

---

## ➡️ Next: [Module 9 — Secure AI SDLC](module-09-secure-sdlc.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 7: Continuous Security](module-07-continuous-security.md) | [📚 References](references.md) | [Module 9: Secure AI SDLC](module-09-secure-sdlc.md) |
