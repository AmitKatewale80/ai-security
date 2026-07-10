# ✅ Module 10: Production Readiness

> Checklists, assessments, and best practices for secure AI in production.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 9: Secure AI SDLC](module-09-secure-sdlc.md) | Module 10 of 10 | [📚 References](references.md) |

---

## Learning Objectives

After this module, you will be able to:
- Complete a production readiness assessment for AI systems
- Conduct a security review using standardized checklists
- Verify governance requirements before go-live
- Ensure regulatory compliance for AI deployments
- Apply industry best practices to your AI security program

---

## 10.1 Production Readiness Checklist

### Pre-Production Gate — Must ALL Pass

```
┌─────────────────────────────────────────────────────────────┐
│          AI PRODUCTION READINESS CHECKLIST                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SECURITY (all required):                                    │
│  □ Red-team assessment score >90%                            │
│  □ Compliance scan: no CRITICAL findings                     │
│  □ Model integrity: cryptographic signature verified          │
│  □ Input guardrails: injection detection active              │
│  □ Output guardrails: PII filtering active                   │
│  □ Rate limiting configured and tested                       │
│  □ Kill switch tested (can shutdown in <60 seconds)          │
│  □ Rollback tested (can revert in <5 minutes)               │
│                                                              │
│  GOVERNANCE (all required):                                  │
│  □ Threat model current and reviewed                         │
│  □ Data classification review completed                      │
│  □ Model owner identified and signed off                     │
│  □ Security champion reviewed and signed off                 │
│  □ Audit logging verified (all actions recorded)             │
│  □ Incident response playbook exists                         │
│  □ AI system registered in organizational inventory          │
│                                                              │
│  OPERATIONS (all required):                                  │
│  □ Monitoring alerts configured                              │
│  □ Cost controls: budget cap set and tested                  │
│  □ On-call rotation: team knows how to respond               │
│  □ Runbook: documented procedures for common scenarios       │
│  □ SLA defined and monitoring in place                       │
│  □ Backup/failover: graceful degradation if AI unavailable   │
│                                                              │
│  COMPLIANCE (as applicable):                                 │
│  □ GDPR: DPIA completed, Article 30 records updated          │
│  □ EU AI Act: risk classification documented                 │
│  □ DOT: non-discrimination verified                          │
│  □ PCI-DSS: no card data in AI processing (tokenized)        │
│  □ Accessibility: screen reader compatible                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10.2 Security Review Process

### Security Review Levels

| AI System Risk | Review Level | Who Reviews | Timeline |
|---------------|-------------|-------------|----------|
| Low (read-only, no PII) | Automated scan only | CI/CD pipeline | Same day |
| Medium (modifies data, limited scope) | Scan + security champion | Security champion | 2 days |
| High (PII access, financial impact) | Full review | Security team + champion | 1 week |
| Critical (safety, ops, multi-domain) | Board review | AI Security Review Board | 2 weeks |

### Security Review Template

```
AI SECURITY REVIEW — [System Name] v[X.Y.Z]
═══════════════════════════════════════════════

Reviewer: _________________ Date: ___________
System Owner: _____________ Risk Level: _____

1. ARCHITECTURE
   □ Data flow diagram reviewed
   □ Trust boundaries identified
   □ Attack surface documented
   Rating: [Adequate / Needs Improvement / Fail]

2. INPUT SECURITY
   □ Injection detection coverage verified
   □ Input validation comprehensive
   □ Rate limiting appropriate
   Rating: [Adequate / Needs Improvement / Fail]

3. MODEL SECURITY
   □ Source verification (approved publisher)
   □ Integrity verification (signature)
   □ No excessive permissions
   Rating: [Adequate / Needs Improvement / Fail]

4. DATA SECURITY
   □ PII handling appropriate (tokenized/classified)
   □ Access controls enforced
   □ Data retention policy defined
   Rating: [Adequate / Needs Improvement / Fail]

5. OUTPUT SECURITY
   □ PII filtering active
   □ Policy compliance checking
   □ Hallucination mitigation
   Rating: [Adequate / Needs Improvement / Fail]

6. OPERATIONAL SECURITY
   □ Monitoring adequate
   □ Incident response plan exists
   □ Kill switch functional
   □ Cost controls appropriate
   Rating: [Adequate / Needs Improvement / Fail]

OVERALL DECISION: [APPROVE / CONDITIONAL / REJECT]
CONDITIONS (if conditional): ____________________
NEXT REVIEW DATE: _______________
```

---

## 10.3 Governance Checklist

### Organizational Readiness

```
AI GOVERNANCE READINESS ASSESSMENT
═══════════════════════════════════

STRUCTURE:
  □ AI governance body established (board/committee)
  □ Roles defined: model owner, security champion, DPO
  □ Meeting cadence set (monthly minimum)
  □ Escalation paths documented
  □ Budget allocated for AI security

POLICIES:
  □ AI acceptable use policy
  □ AI model approval policy
  □ AI data handling policy
  □ AI agent authority policy
  □ AI incident response policy
  □ AI vendor/third-party policy

PROCESSES:
  □ AI system inventory maintained
  □ Risk register maintained and reviewed
  □ Security review process defined
  □ Deployment approval workflow active
  □ Incident response tested (tabletop exercise)
  □ Training program in place for AI teams

MEASUREMENT:
  □ KPIs defined for AI security program
  □ Compliance metrics tracked
  □ Incident metrics tracked
  □ Cost metrics tracked
  □ Regular reporting to leadership
```

---

## 10.4 Compliance Requirements

### Regulatory Matrix

| Regulation | Requirement | How We Comply | Evidence |
|-----------|-------------|--------------|----------|
| **GDPR Art. 17** | Right to erasure (30 days) | Chatbot correctly states 30-day timeline | Compliance probe (Lab 11) |
| **GDPR Art. 35** | DPIA for high-risk processing | DPIA completed for each AI system | DPIA document |
| **EU AI Act Art. 9** | Risk management for high-risk AI | NIST AI RMF implemented | Risk register |
| **EU AI Act Art. 14** | Human oversight | Human-in-loop for critical decisions | Audit trail (Lab 12) |
| **DOT 14 CFR 382** | Non-discrimination | Bias testing shows no differential treatment | Garak scan results (Lab 11) |
| **PCI-DSS** | Protect cardholder data | PII tokenized before AI processing | Tokenization verification (Lab 07) |
| **FAA fatigue rules** | Crew duty time limits | Policy engine blocks fatigue violations | Policy engine tests (Lab 12) |

### Compliance Evidence Collection

```
For each regulation, maintain:
  1. Control description (what we do)
  2. Control evidence (proof it works)
  3. Testing frequency (how often we verify)
  4. Last test date and result
  5. Owner responsible for maintenance
  6. Gap remediation plan (if any)
```

---

## 10.5 Best Practices

### Top 10 AI Security Best Practices

| # | Practice | Why | How |
|---|----------|-----|-----|
| 1 | **Never trust AI output without validation** | AI can be manipulated or hallucinate | Output guardrails, human review for critical |
| 2 | **Least privilege for all AI agents** | Limits blast radius of compromise | Per-agent identity, tool scoping |
| 3 | **Human-in-the-loop for dangerous actions** | Prevents catastrophic autonomous decisions | Approval workflows, timeout = no-action |
| 4 | **Scan models before loading** | Supply chain attacks are invisible | Publisher check, code scan, signature verify |
| 5 | **Tokenize PII before AI processing** | Breach of ML pipeline yields no real data | SHA-256 with isolated salt |
| 6 | **Mandatory security gates in CI/CD** | AI test selectors will skip security if allowed | Gates that AI cannot bypass |
| 7 | **Monitor costs and set hard limits** | Runaway agents can generate massive bills | Per-agent budget, loop detection |
| 8 | **Classify and control knowledge bases** | Not all documents should be accessible to all users | Role-based ACL on documents |
| 9 | **Red-team before every deployment** | Find vulnerabilities before attackers do | Automated probes + periodic manual testing |
| 10 | **Log everything, review regularly** | Audit trail enables incident response and compliance | Immutable logging, regular review |

### Anti-Patterns to Avoid

| Anti-Pattern | Risk | Better Approach |
|-------------|------|-----------------|
| "The AI is just a chatbot, no security needed" | Prompt injection → data breach | Every LLM needs guardrails |
| "We tested it once, it's fine" | Model updates introduce new vulns | Continuous validation |
| "AI code review replaces human review" | Obfuscated vulns pass AI (Lab 18) | Multi-layer: AI + SAST + human |
| "All tests pass, ship it" | Weak tests (Lab 19), skipped tests (Lab 20) | Mutation testing + mandatory gates |
| "One set of credentials for all agents" | Single compromise = total access | Per-agent identity isolation |
| "Trust the model registry" | Registry can be poisoned (Lab 01, 05) | Scan everything, verify signatures |
| "AI-generated test data is synthetic" | May contain real PII (Lab 21) | PII fingerprint scanning |

---

## 10.6 Certification Assessment

### AI Security Maturity Levels

| Level | Name | Characteristics |
|-------|------|----------------|
| **1** | Initial | No formal AI security program. Ad-hoc controls. |
| **2** | Developing | Basic policies exist. Manual reviews. Some monitoring. |
| **3** | Defined | Formal processes. Automated scanning in CI/CD. Risk register. |
| **4** | Managed | Continuous validation. Metrics-driven. Regular board reviews. |
| **5** | Optimizing | Proactive threat intelligence. Industry-leading practices. Continuous improvement. |

### Self-Assessment Scorecard

```
Score each category 1-5:

Category                          Score   Target
────────────────────────────────  ─────   ──────
Governance structure              [ ]     ≥3
Policy documentation              [ ]     ≥3
Threat modeling                   [ ]     ≥3
Input security (guardrails)       [ ]     ≥4
Output security (PII, policy)     [ ]     ≥4
Model protection (signing, scan)  [ ]     ≥4
Agent security (least privilege)  [ ]     ≥4
Monitoring and alerting           [ ]     ≥3
Incident response                 [ ]     ≥3
Continuous validation             [ ]     ≥3
Supply chain security             [ ]     ≥3
Compliance                        [ ]     ≥3

TOTAL: ___/60    TARGET: ≥39 (Level 3+)
```

---

## 🎓 Academy Completion

Congratulations on completing the AI Security Academy. You now have:

- ✅ Understanding of AI/ML fundamentals and architectures
- ✅ Knowledge of the AI threat landscape (MITRE ATLAS + OWASP)
- ✅ Offensive skills: how attacks work and why
- ✅ Defensive skills: guardrails, gateways, agent security
- ✅ Hands-on experience: 23 enterprise labs
- ✅ Governance knowledge: frameworks, policies, compliance
- ✅ Operational capability: monitoring, SOC, incident response
- ✅ Architecture skills: secure AI platform design
- ✅ SDLC integration: threat modeling, secure deployment
- ✅ Production readiness: checklists, assessments, best practices

### Recommended Next Steps

1. **Assess** your current AI systems against the Production Readiness Checklist
2. **Prioritize** gaps using the Risk Register template
3. **Implement** controls starting with highest-risk systems
4. **Validate** using red-team probes from the labs
5. **Monitor** continuously and improve iteratively

---

## ➡️ See Also: [References](references.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 9: Secure AI SDLC](module-09-secure-sdlc.md) | [🧪 Hands-on Labs](module-05-hands-on-labs.md) | [📚 References](references.md) |
