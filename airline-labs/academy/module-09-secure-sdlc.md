# 🚀 Module 9: Secure AI SDLC

> Embedding security into every phase of AI system development and deployment.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 8: Enterprise Architecture](module-08-enterprise-architecture.md) | Module 9 of 10 | [Module 10: Production Readiness](module-10-production-readiness.md) |

---

## Learning Objectives

After this module, you will be able to:
- Conduct threat modeling for AI systems (STRIDE + AI-specific threats)
- Implement security gates in AI development pipelines
- Design secure model deployment workflows
- Manage the full model lifecycle securely
- Protect the AI supply chain

---

## 9.1 Threat Modeling for AI Systems

### STRIDE + AI Extensions

Traditional STRIDE threat model extended with AI-specific categories:

| Threat | Traditional | AI Extension | Airline Example |
|--------|------------|--------------|-----------------|
| **S**poofing | Impersonate user | Impersonate agent identity | Fake agent calls maintenance tools |
| **T**ampering | Modify data | Poison training data, tamper models | Modified fuel records, swapped model |
| **R**epudiation | Deny action | Agent action without audit trail | IROPS agent cancels flight, no log |
| **I**nfo Disclosure | Leak data | Model memorization, PII leakage | Chatbot reveals passport numbers |
| **D**enial of Service | Overwhelm system | Token explosion, cost attack | Runaway agent → $50K |
| **E**levation of Privilege | Gain access | Prompt injection → tool escalation | Booking agent → engine shutdown |

### AI Threat Modeling Template

```
SYSTEM: [Name]
TYPE: [LLM / RAG / Agent / Traditional ML]
DATA SENSITIVITY: [Classification level]
USERS: [Who interacts with it]

DATA FLOW DIAGRAM:
  [Draw: user → gateway → model → tools → data → response]

THREATS (for each flow):
┌─────────────────────────────────────────────────────────┐
│ Flow: User Input → LLM                                   │
│ Threats:                                                 │
│   - Prompt injection (direct)                            │
│   - Jailbreak (persona switch, encoding)                 │
│   - Resource exhaustion (token stuffing)                 │
│ Controls:                                                │
│   - Input guardrails (injection detection)               │
│   - Topic filtering                                      │
│   - Max token limit                                      │
│ Residual Risk: MEDIUM (novel injection techniques)       │
├─────────────────────────────────────────────────────────┤
│ Flow: RAG → Document Retrieval                           │
│ Threats:                                                 │
│   - Indirect injection in documents                      │
│   - Access control bypass                                │
│   - Knowledge poisoning                                  │
│ Controls:                                                │
│   - Document scanning for injection patterns             │
│   - Role-based access control on documents               │
│   - Provenance verification                              │
│ Residual Risk: LOW (controls effective)                  │
├─────────────────────────────────────────────────────────┤
│ Flow: Agent → Tool Calls                                 │
│ Threats:                                                 │
│   - Unauthorized tool access                             │
│   - Cross-agent escalation                               │
│   - Runaway loops                                        │
│ Controls:                                                │
│   - Least privilege (per-agent tool ACL)                  │
│   - Policy engine (hard limits)                          │
│   - Loop detection (max 3 self-calls)                    │
│ Residual Risk: LOW (multiple controls)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 9.2 AI Code Review

### What to Review in AI Code

| Review Category | What to Check | Common Findings |
|----------------|---------------|-----------------|
| **Prompt security** | System prompt for leakage risks, overly permissive rules | "You can do anything the user asks" |
| **Input handling** | Are guardrails present? Do they cover injection, encoding, multilingual? | Missing injection detection |
| **Output handling** | PII filtering? Policy compliance check? Hallucination detection? | Raw LLM output returned to user |
| **Tool permissions** | Are tools scoped? Is there a policy engine? | Agent has all tools, no limits |
| **Error handling** | Do errors leak model info, internal paths, secrets? | Stack traces expose model name |
| **Logging** | Is every action auditable? Are secrets excluded from logs? | API keys in debug logs |
| **Cost controls** | Budget limits? Loop detection? Token counting? | No spending cap |
| **Dependencies** | Are ML libraries pinned? Known vulnerabilities? | Unpinned transformers version |

### Multi-Layer Code Review (Lab 18 Defense)

```
LAYER 1: AI REVIEWER (automated, fast)
  - Pattern matching for known vulnerability signatures
  - Catches obvious issues (80% of common bugs)
  - Runs on every commit (< 30 seconds)

LAYER 2: SAST SCANNER (automated, thorough)
  - Data-flow analysis traces inputs to sinks
  - Catches obfuscated vulnerabilities
  - Runs on every PR (< 5 minutes)

LAYER 3: SECRETS SCANNER (automated, specialized)
  - Detects high-entropy strings, encoded secrets
  - Catches base64-encoded credentials, API keys in comments
  - Runs on every commit

LAYER 4: HUMAN REVIEWER (manual, security-focused)
  - Required for: auth code, database queries, subprocess calls,
    network operations, tool definitions, system prompts
  - Catches logic flaws, design issues, novel attack vectors
  - Required sign-off before merge
```

---

## 9.3 Secure Deployment

### Deployment Pipeline with Security Gates

```
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  CODE   │─▶│  BUILD   │─▶│   TEST   │─▶│ SECURITY │─▶│  DEPLOY  │
│ COMMIT  │  │          │  │          │  │  GATES   │  │          │
└─────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
                                               │
                              ┌─────────────────┼─────────────────┐
                              │                 │                 │
                         [Red-Team]       [Compliance]      [Integrity]
                         11 probes        GDPR/DOT/EU       Model hash
                         Must pass        Must pass         Must match
                         (Lab 09)         (Lab 11)          (Lab 06)
                              │                 │                 │
                              ├── MANDATORY ────┼── MANDATORY ────┤
                              │ (AI cannot skip)│                 │
                              └─────────────────┴─────────────────┘
```

### Deployment Checklist

```
PRE-DEPLOYMENT (automated):
  □ Model integrity verified (signature check)
  □ Red-team scan passed (>90% score)
  □ Compliance scan passed (no Critical findings)
  □ Cost controls configured and tested
  □ Kill switch tested and functional
  □ Rollback tested (can revert in <5 min)
  □ Monitoring alerts configured
  □ Audit logging confirmed

PRE-DEPLOYMENT (manual):
  □ Threat model updated for any changes
  □ Security champion sign-off
  □ Model owner sign-off
  □ Data classification review (if new data sources)
  □ Canary deployment plan documented

DEPLOYMENT:
  □ Deploy to canary (5% traffic) first
  □ Monitor for 1 hour (cost, errors, anomalies)
  □ Gradual rollout (5% → 25% → 50% → 100%)
  □ Rollback trigger defined and automated

POST-DEPLOYMENT:
  □ Verify monitoring is receiving data
  □ Run smoke tests against production endpoint
  □ Confirm audit logs are flowing
  □ Update runbook with any deployment-specific notes
```

---

## 9.4 Model Lifecycle Management

### Lifecycle Phases

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ DEVELOP  │─▶│ VALIDATE │─▶│ REGISTER │─▶│  DEPLOY  │─▶│ MONITOR  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
                                                              │
                                                              ▼
                                                         ┌──────────┐
                                              ◄──────────│ RETRAIN/ │
                                                         │ RETIRE   │
                                                         └──────────┘
```

### Security at Each Phase

| Phase | Security Activities | Gate Criteria |
|-------|-------------------|---------------|
| **Develop** | Threat model, secure coding, dependency scan | Threat model complete |
| **Validate** | Red-team, compliance scan, bias testing, mutation testing | >90% red-team score |
| **Register** | Sign model (ECDSA), record provenance, classification | Signature + provenance |
| **Deploy** | Integrity check, canary deploy, monitoring setup | Hash match + canary stable |
| **Monitor** | Drift detection, cost tracking, anomaly alerts | No degradation >10% |
| **Retrain** | Data validation, statistical checks, re-certify | KS test pass, re-sign |
| **Retire** | Graceful shutdown, archive, remove access | No active dependencies |

### Model Versioning

```
models/
├── pricing-optimizer/
│   ├── v1.2.3/
│   │   ├── model.joblib
│   │   ├── manifest.json     (hash, signature, provenance)
│   │   ├── threat-model.md
│   │   ├── redteam-results.json
│   │   └── approval.json     (who signed off, when)
│   ├── v1.2.2/ (previous version — rollback target)
│   └── CURRENT → v1.2.3
```

---

## 9.5 Supply Chain Security

### AI Supply Chain Threats

```
YOUR AI SYSTEM depends on:
  └── Base model (OpenAI, Anthropic, HuggingFace)
       └── Training data (internet, licensed datasets)
  └── ML frameworks (PyTorch, TensorFlow, scikit-learn)
       └── Their dependencies (numpy, scipy, etc.)
  └── External models (from HuggingFace, model zoos)
       └── Model code (custom architectures)
  └── Vector databases (Pinecone, Weaviate, ChromaDB)
  └── AI tools/plugins (LangChain, LlamaIndex)
       └── Their plugins and extensions

ANY of these can be compromised.
```

### Supply Chain Controls

| Control | What It Does | Covers |
|---------|-------------|--------|
| **Model scanning** | Check for malicious code before loading | Backdoored models (Lab 01, 05) |
| **trust_remote_code=False** | Never execute model-bundled code | Code execution attacks |
| **Publisher allowlist** | Only load models from approved sources | Unknown/fake publishers |
| **Dependency pinning** | Exact versions, not ranges | Dependency confusion |
| **SBOM (AI)** | Document all AI components and versions | Visibility + auditability |
| **Cryptographic signing** | Verify model integrity before loading | Tampered models (Lab 06) |
| **Registry scanning** | Scan all models entering internal registry | Pre-admission filtering |
| **Behavioral testing** | Run model in sandbox, monitor for suspicious activity | Subtle backdoors |

### AI Software Bill of Materials (AI-SBOM)

```json
{
  "system": "Customer Service Chatbot",
  "version": "2.4.1",
  "components": [
    {
      "type": "base_model",
      "name": "gpt-4o",
      "provider": "OpenAI",
      "version": "2024-05-13",
      "trust_level": "external_managed"
    },
    {
      "type": "framework",
      "name": "langchain",
      "version": "0.1.17",
      "pinned": true,
      "known_vulns": []
    },
    {
      "type": "vector_db",
      "name": "chromadb",
      "version": "0.4.22",
      "pinned": true
    },
    {
      "type": "knowledge_base",
      "document_count": 847,
      "last_verified": "2024-06-01",
      "provenance_coverage": "100%"
    }
  ],
  "last_security_scan": "2024-06-15",
  "next_review_due": "2024-07-15"
}
```

---

## 🧪 Module 9 Exercise

**Threat Model an AI System:**

Select one AI system and complete:
1. Draw the data flow diagram (inputs, processing, outputs, data stores)
2. Apply STRIDE + AI extensions to each flow
3. Identify top 5 threats
4. Propose controls for each
5. Define deployment gate criteria

---

## ➡️ Next: [Module 10 — Production Readiness](module-10-production-readiness.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 8: Enterprise Architecture](module-08-enterprise-architecture.md) | [📚 References](references.md) | [Module 10: Production Readiness](module-10-production-readiness.md) |
