# 🏛️ Module 6: AI Governance

> Frameworks, policies, and processes for responsible enterprise AI deployment.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 5: Hands-on Labs](module-05-hands-on-labs.md) | Module 6 of 10 | [Module 7: Continuous Security](module-07-continuous-security.md) |

---

## Learning Objectives

After this module, you will be able to:
- Apply the NIST AI Risk Management Framework to airline AI systems
- Draft AI security policies for your organization
- Implement AI risk assessment processes
- Design responsible AI practices for high-stakes aviation environments
- Establish AI review boards and approval workflows

---

## 6.1 NIST AI Risk Management Framework (AI RMF)

### The Four Functions

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  GOVERN  │───▶│   MAP   │───▶│ MEASURE  │───▶│ MANAGE  │
│          │    │         │    │          │    │         │
│ Culture, │    │ Context,│    │ Assess   │    │ Respond │
│ Policy,  │    │ Risks,  │    │ risks,   │    │ to      │
│ Oversight│    │ Impact  │    │ Track    │    │ risks   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### GOVERN — Organizational AI Governance

| Activity | Airline Implementation |
|----------|----------------------|
| Establish AI governance structure | AI Safety Board (CISO + CTO + Legal + Ops) |
| Define risk tolerance | "No AI makes safety-critical decisions without human approval" |
| Assign accountability | Model owner per system, security champion per team |
| Resource allocation | Dedicated AI security team (3-5 FTEs) |
| Cross-functional coordination | Monthly AI risk review across engineering, legal, ops, compliance |

### MAP — Identify and Contextualize Risks

For each AI system, document:

```
System: Customer Service Chatbot "SkyAssist"
─────────────────────────────────────────────
Context:
  - Serves 50M passengers/year across 40 countries
  - Handles bookings, loyalty, refunds, complaints
  - Accesses: policy docs, fare rules, booking API
  - Does NOT access: PNR database, crew data, safety reports

Risk Categories:
  ☑ Prompt injection (LLM01) — chatbot reads external documents
  ☑ Sensitive info disclosure (LLM02) — knows booking details
  ☑ Excessive agency (LLM06) — can apply discounts
  ☐ Data poisoning (LLM04) — not applicable (doesn't retrain)
  ☑ Misinformation (LLM09) — could give wrong policy info

Stakeholders Affected:
  - Passengers (privacy, service quality)
  - Revenue team (unauthorized discounts)
  - Legal/compliance (GDPR, accessibility)
  - Brand/reputation (offensive content)
```

### MEASURE — Assess and Track

| Metric | Target | Current | Frequency |
|--------|--------|---------|-----------|
| Red-team pass rate | >90% | 63% | Every deploy |
| Compliance scan score | >95% | 71% | Weekly |
| Mean time to detect AI incident | <1 hour | 4 hours | Continuous |
| PII exposure incidents | 0 | 2/quarter | Continuous |
| Cost anomaly detection | <$100 before alert | $500 | Continuous |
| Model integrity failures | 0 | 0 | Every load |

### MANAGE — Respond to Identified Risks

| Risk Level | Response | Timeline | Approval |
|-----------|----------|----------|----------|
| Critical | Immediate shutdown + fix | 24 hours | CISO |
| High | Block deployment + fix | 7 days | Security Lead |
| Medium | Fix in next sprint | 30 days | Team Lead |
| Low | Add to backlog | 90 days | Team Lead |

---

## 6.2 AI Policies

### Essential AI Security Policies

**1. AI Model Approval Policy**
```
All AI models must pass security review before production deployment:
  □ Source verification (approved publisher or internal)
  □ Code scanning (no malicious patterns)
  □ Integrity verification (cryptographic signature)
  □ Red-team assessment (automated + manual for critical systems)
  □ Compliance scan (regulatory requirements)
  □ Data classification review (what data does it access?)
  □ Human approval from model owner + security champion
```

**2. AI Data Handling Policy**
```
AI systems processing personal data must:
  □ Tokenize PII before model training (SHA-256 + isolated salt)
  □ Apply access controls based on data classification
  □ Implement differential privacy for sensitive APIs
  □ Validate synthetic data for PII leakage before use
  □ Maintain data lineage and provenance records
  □ Support GDPR right-to-erasure within 30 days
```

**3. AI Agent Authority Policy**
```
AI agents are classified by authority level:
  Level 1 (Low): Read-only queries, FAQ responses
  Level 2 (Medium): Modify single customer records (<$2000 value)
  Level 3 (High): Modify multiple records, schedule changes
  Level 4 (Critical): Cancel flights, override safety rules

  Levels 3-4 REQUIRE human-in-the-loop approval.
  No AI agent may override safety or fatigue regulations.
  All actions logged to immutable audit trail.
```

**4. AI Incident Response Policy**
```
AI security incidents are classified as:
  P1 (Critical): PII exposure, safety system compromise, runaway costs >$1K
  P2 (High): Jailbreak success, unauthorized actions, compliance failure
  P3 (Medium): Prompt leakage, minor policy violation
  P4 (Low): Content policy violation, hallucination

Response requirements:
  P1: Immediate containment (kill switch), RCA within 24h
  P2: Investigation within 4h, remediation within 7 days
  P3: Fix within 30 days, add to regression suite
  P4: Fix in next sprint
```

---

## 6.3 AI Risk Management

### AI Risk Register (Template)

| ID | System | Risk | Likelihood | Impact | Score | Owner | Controls | Status |
|----|--------|------|-----------|--------|-------|-------|----------|--------|
| R-001 | Customer chatbot | Prompt injection → PII leak | High | Critical | 20 | ML Team | Input guardrails, PII filter | Mitigated |
| R-002 | Pricing API | Model theft via queries | Medium | High | 12 | Revenue | Rate limiting, noise | Mitigated |
| R-003 | IROPS agent | Unauthorized flight cancellation | Low | Critical | 10 | Ops | Human-in-loop, policy engine | Mitigated |
| R-004 | Maintenance RAG | Knowledge poisoning | Medium | Critical | 15 | Eng | Provenance check | In Progress |
| R-005 | Fuel model | Training data poisoning | Low | High | 8 | Data | Statistical validation | Mitigated |

### Risk Scoring: Likelihood × Impact

```
Likelihood: 1 (Rare) → 5 (Almost Certain)
Impact:     1 (Negligible) → 5 (Catastrophic)
Score:      Likelihood × Impact (max 25)

Score 1-5:   LOW (accept or backlog)
Score 6-12:  MEDIUM (mitigate within 30 days)
Score 13-19: HIGH (mitigate within 7 days)
Score 20-25: CRITICAL (immediate action)
```

---

## 6.4 Responsible AI

### Responsible AI Principles for Airlines

| Principle | Meaning | Airline Implementation |
|-----------|---------|----------------------|
| **Fairness** | No discrimination by nationality, race, disability | Compliance probes for bias (Lab 11) |
| **Transparency** | Users know they're interacting with AI | "I'm SkyAssist, an AI assistant" disclosure |
| **Accountability** | Clear ownership for AI decisions | Model owner + audit trail for every action |
| **Safety** | AI cannot make unsafe decisions autonomously | Human-in-loop for safety-critical (Lab 12) |
| **Privacy** | Minimize PII processing, protect data | Tokenization (Lab 07), access controls (Lab 04) |
| **Reliability** | Consistent, predictable behavior | Red-team testing, compliance scanning |

### EU AI Act Classification

| Risk Level | AI System | Requirements |
|-----------|-----------|-------------|
| Unacceptable | Social scoring, subliminal manipulation | Prohibited |
| High Risk | Crew fatigue management, safety-critical decisions | Conformity assessment, human oversight, logging |
| Limited Risk | Customer chatbot | Transparency obligations (disclose AI) |
| Minimal Risk | Spam filtering, internal analytics | No specific requirements |

**Airline AI systems likely classified as HIGH RISK:**
- Engine health monitoring / predictive maintenance
- Crew scheduling (fatigue compliance)
- Baggage screening (security-critical)
- Automated rebooking during IROPS (affects passenger rights)

---

## 6.5 AI Review Process

### AI Security Review Board

```
COMPOSITION:
  Chair: CISO (or delegate)
  Members: Head of ML Engineering, Legal Counsel, 
           Operations Security, Data Protection Officer,
           Safety Officer (for aviation-critical systems)

MEETS: Monthly (or ad-hoc for Critical deployments)

REVIEWS:
  - New AI system deployments
  - Material changes to existing AI systems
  - AI incident post-mortems
  - Quarterly risk register update
  - Regulatory changes affecting AI
```

### Deployment Approval Workflow

```
Developer/ML Engineer
        │
        ▼
[Automated Checks] ──── FAIL → Fix and resubmit
  ✓ Red-team scan        │
  ✓ Compliance scan      │
  ✓ Cost estimate        │
  ✓ Data classification  │
        │ PASS
        ▼
[Security Champion Review] ──── REJECT → Fix and resubmit
  ✓ Threat model current?      │
  ✓ Controls appropriate?      │
  ✓ Audit logging complete?    │
        │ APPROVE
        ▼
[Model Owner Sign-off] ──── For HIGH RISK only:
        │                    │
        ▼                    ▼
   [DEPLOY]          [AI Review Board]
                           │
                      APPROVE/REJECT
```

---

## 6.6 AI Security Standards

### Relevant Standards and Regulations

| Standard | Scope | Key Requirements | Airline Relevance |
|----------|-------|-----------------|-------------------|
| **EU AI Act** | EU market | Risk classification, human oversight, transparency | All EU-serving airlines |
| **NIST AI RMF** | US guidance | Govern, Map, Measure, Manage | Framework for AI governance |
| **ISO 42001** | International | AI management system | Certification for AI practices |
| **GDPR** | EU data | Data minimization, right to erasure, DPIAs | All passenger data processing |
| **FAA AC 23-14** | US aviation | Software assurance (extensible to AI) | Safety-critical AI systems |
| **EASA AI Concept Paper** | EU aviation | Trustworthiness for AI in aviation | ML-based maintenance, ops |

### Compliance Checklist

```
□ Data Protection Impact Assessment (DPIA) completed
□ AI system registered in organizational inventory
□ Risk classification per EU AI Act (if applicable)
□ Human oversight mechanism documented
□ Technical documentation maintained
□ Bias and fairness testing completed
□ Incident response plan established
□ Regular performance monitoring in place
□ Logging and audit trail implemented
□ User transparency/disclosure provided
```

---

## 🧪 Module 6 Exercise

**Draft an AI Policy:**

Create a 1-page AI Agent Authority Policy for your airline:
1. Define 4 authority levels
2. Specify which actions require human approval
3. Define timeout behavior (fail-safe vs fail-open)
4. Specify logging requirements
5. Define the escalation path

---

## ➡️ Next: [Module 7 — Continuous Security](module-07-continuous-security.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 5: Hands-on Labs](module-05-hands-on-labs.md) | [📚 References](references.md) | [Module 7: Continuous Security](module-07-continuous-security.md) |
