# 🔄 Module 7: Continuous Security

> AI security isn't a one-time assessment — it's continuous validation and monitoring.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 6: AI Governance](module-06-ai-governance.md) | Module 7 of 10 | [Module 8: Enterprise Architecture](module-08-enterprise-architecture.md) |

---

## Learning Objectives

After this module, you will be able to:
- Implement Continuous Threat Exposure Management (CTEM) for AI systems
- Design continuous validation pipelines for AI security
- Build AI-aware security monitoring and alerting
- Operate an AI-focused Security Operations Center (SOC)
- Execute AI incident response procedures

---

## 7.1 CTEM — Continuous Threat Exposure Management

### What Is CTEM for AI?

CTEM is Gartner's framework for continuously identifying, validating, and remediating security exposures. Applied to AI, it means: don't just test once before deployment — continuously validate that your AI systems remain secure.

### The 5 CTEM Stages for AI

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  SCOPE   │──▶│ DISCOVER │──▶│ PRIORITIZE│──▶│ VALIDATE │──▶│ MOBILIZE │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                    ↑
                                                    │ (repeat continuously)
                                                    └─────────────────────
```

**1. SCOPE** — Define what AI assets are in scope
```
  - Customer chatbot (LLM + RAG)
  - IROPS agent (LLM + tools)
  - Revenue pricing API (traditional ML)
  - Maintenance RAG system
  - AI-powered SIEM
  - CI/CD AI test selector
```

**2. DISCOVER** — Identify exposures
```
  - New prompt injection techniques published
  - Model drift detected in pricing accuracy
  - New ATLAS techniques added to catalog
  - OWASP LLM Top 10 updated
  - Dependency vulnerability in ML library
  - New jailbreak discovered for base model
```

**3. PRIORITIZE** — Rank by risk
```
  Critical: Chatbot prompt injection → PII exposure (active technique, high impact)
  High: Agent tool escalation (new ATLAS technique, safety impact)
  Medium: Pricing API drift (gradual, financial impact only)
  Low: Prompt leakage (information only, no operational impact)
```

**4. VALIDATE** — Test if exposure is exploitable
```
  - Re-run red-team probes (Lab 09) against chatbot
  - Test new injection technique against RAG (Lab 04)
  - Simulate agent escalation scenario (Lab 16)
  - Verify cost controls still hold (Lab 17)
```

**5. MOBILIZE** — Fix confirmed vulnerabilities
```
  - Update guardrails to block new injection pattern
  - Patch agent tool permissions
  - Add new compliance probe to regression suite
  - Brief security team on new technique
```

---

## 7.2 Continuous Validation

### What to Validate and When

| Trigger | What to Run | Labs |
|---------|------------|------|
| Every deployment | Red-team probes + compliance scan | 09, 11 |
| Weekly | Full ATLAS technique coverage scan | All |
| After model update | Regression suite + mutation testing | 19 |
| After prompt change | Jailbreak + prompt leakage probes | 09 |
| After knowledge base update | Provenance + poisoning detection | 14 |
| After dependency update | Supply chain scan | 01, 05, 06 |
| Monthly | Full penetration test (manual + automated) | All |

### CI/CD Integration

```yaml
# .github/workflows/ai-security.yml
ai_security_gate:
  steps:
    - name: Red-team scan (11 probes)
      run: python ai_security/run_redteam.py
      fail_on: any_critical_or_high
    
    - name: Compliance scan (GDPR, DOT, EU AI Act)
      run: python ai_security/run_compliance.py
      fail_on: any_critical
    
    - name: Model integrity check
      run: python ai_security/verify_model_signatures.py
      fail_on: any_failure
    
    - name: Cost control validation
      run: python ai_security/test_budget_limits.py
      fail_on: budget_exceeded
    
    - name: Mandatory security tests
      run: python ai_security/mandatory_security_tests.py
      skip: never  # AI test selector cannot bypass this
```

### Regression Suite Management

```
After each vulnerability fix:
  1. Create a probe that tests for that specific vulnerability
  2. Add probe to permanent regression suite
  3. Run on every deployment going forward
  4. Alert if previously-fixed vulnerability reappears

Current regression suite size: 47 probes
  - 11 red-team probes (Lab 09)
  - 8 compliance probes (Lab 11)
  - 12 injection detection probes
  - 6 agent escalation probes
  - 5 cost control probes
  - 5 data leakage probes
```

---

## 7.3 AI Security Monitoring

### What to Monitor

| Signal | Source | Alert Condition | Response |
|--------|--------|----------------|----------|
| Injection attempts | Input guardrails | >5 per hour from same user | Block user, investigate |
| PII in responses | Output guardrails | Any occurrence | Halt session, audit |
| Cost anomaly | Token counter | >3x daily average | Throttle agent |
| Model confidence drop | Inference metrics | Sustained drop >10% | Investigate, rollback |
| Tool call anomaly | Agent audit log | Unusual tool or frequency | Alert SOC |
| Authentication failure | Gateway logs | >10 failures/minute | Rate limit, alert |
| Knowledge base change | Document store | Any unscheduled modification | Block + review |

### Dashboard Metrics

```
┌─────────────────────────────────────────────────────┐
│           AI SECURITY DASHBOARD                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  THREAT STATUS          TODAY        7-DAY TREND     │
│  ─────────────          ─────        ──────────      │
│  Injection blocked:      47          ▼ (was 62)      │
│  PII leak prevented:     3           ─ (was 4)       │
│  Cost anomalies:         0           ─ (was 0)       │
│  Agent escalation blocked: 1         ─ (was 2)       │
│  Model integrity checks:  OK         ─ (all pass)    │
│                                                      │
│  COMPLIANCE SCORE        BUDGET                      │
│  ─────────────────       ──────                      │
│  Overall: 89% ▲          Today: $127 of $500 limit   │
│  GDPR: 94%               This month: $2,340          │
│  Bias: 86%               Anomalies: 0                │
│  Safety: 91%                                         │
│                                                      │
│  ACTIVE AI SYSTEMS       STATUS                      │
│  ─────────────────       ──────                      │
│  Customer chatbot:       ✓ Healthy                   │
│  IROPS agent:            ✓ Healthy                   │
│  Revenue optimizer:      ✓ Healthy                   │
│  Maintenance RAG:        ⚠ 1 provenance alert        │
│  CI/CD AI selector:      ✓ Healthy                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 7.4 AI SOC (Security Operations Center)

### AI-Specific SOC Capabilities

Traditional SOC detects network intrusions, malware, and unauthorized access. An AI SOC additionally detects:

| Capability | What It Detects | How |
|-----------|----------------|-----|
| Prompt injection monitoring | Injection patterns in user inputs | Pattern matching + ML classifier |
| Output monitoring | PII, policy violations, hallucinations in responses | Content inspection |
| Behavioral anomaly detection | Unusual query patterns suggesting model theft | Statistical analysis |
| Agent activity monitoring | Unauthorized tool calls, escalation attempts | Audit log analysis |
| Cost monitoring | Token explosion, runaway loops | Real-time spending tracking |
| Model drift detection | Accuracy degradation over time | Performance metric tracking |
| Knowledge base integrity | Unauthorized document changes | Change monitoring + hashing |

### AI SOC Runbook (Example: Prompt Injection Detected)

```
ALERT: Prompt injection pattern detected in customer chatbot input
SEVERITY: High
SOURCE: Input guardrail, user session #4827

STEPS:
1. [AUTOMATED] Block current request, return safe response
2. [AUTOMATED] Flag user session for review
3. [ANALYST] Review conversation history for context
4. [ANALYST] Determine: targeted attack vs accidental trigger?
5. [DECISION] If attack:
   a. Block user (temp ban 24h)
   b. Check if any data was exposed before detection
   c. If data exposed → escalate to P1 incident
   d. Document technique, add to detection patterns
6. [DECISION] If false positive:
   a. Whitelist pattern if appropriate
   b. Adjust detection sensitivity
   c. Release user session
```

### SOC Protection Against Log Injection (Lab 15)

```
AI SIEM SECURITY MEASURES:
  ✓ All logs parsed into structured fields BEFORE AI processing
  ✓ Free-text content isolated from instruction context
  ✓ Suppression actions require human analyst approval
  ✓ Canary alerts injected every 15 minutes (must fire)
  ✓ Separate tamper-proof logging for alert pipeline
  ✓ If canary fails → FULL ALERT: AI SIEM may be compromised
```

---

## 7.5 AI Incident Response

### AI Incident Classification

| P-Level | Description | Examples | Response Time |
|---------|-------------|----------|--------------|
| P1 | Active data breach or safety compromise | PII exposed, safety system manipulated | 15 minutes |
| P2 | Successful attack with limited impact | Jailbreak with no data access, unauthorized discount | 4 hours |
| P3 | Vulnerability discovered (not yet exploited) | Red-team finds new bypass | 7 days |
| P4 | Minor policy violation | Hallucination, tone issue | 30 days |

### AI Incident Response Playbook

```
PHASE 1: DETECTION & TRIAGE (0-15 min)
  □ Classify incident severity (P1-P4)
  □ Activate kill switch if P1 (shut down affected system)
  □ Preserve evidence (logs, conversation history, model state)
  □ Notify incident commander

PHASE 2: CONTAINMENT (15 min - 2 hours)
  □ Isolate affected system from production
  □ Revoke compromised tokens/credentials
  □ Block attacker if identified
  □ Enable enhanced logging/monitoring
  □ Assess blast radius (what data/systems were accessible?)

PHASE 3: INVESTIGATION (2-24 hours)
  □ Root cause analysis
  □ Determine: what data was accessed/exposed?
  □ Identify attack technique (map to ATLAS/OWASP)
  □ Assess regulatory reporting requirements (GDPR 72h)
  □ Document timeline

PHASE 4: REMEDIATION (24h - 7 days)
  □ Fix vulnerability (guardrail update, policy change, model update)
  □ Add detection for this specific attack to monitoring
  □ Create regression test (add to red-team suite)
  □ Validate fix doesn't introduce new vulnerabilities
  □ Staged re-deployment

PHASE 5: RECOVERY & LEARNING (7-30 days)
  □ Post-incident review (blameless)
  □ Update AI risk register
  □ Brief AI Review Board
  □ Update training materials
  □ Share learnings (anonymized) with industry
```

### Kill Switch Implementation

Every AI system must have an emergency shutdown:

```python
# Kill switch for AI agent
class AIKillSwitch:
    def check(self, agent_id):
        if redis.get(f"kill:{agent_id}"):
            raise AgentKilled("Emergency shutdown activated")
        if redis.get("kill:all_agents"):
            raise AgentKilled("Global AI shutdown activated")
    
    def activate(self, agent_id, reason, activated_by):
        redis.set(f"kill:{agent_id}", True)
        audit_log.critical(f"KILL SWITCH: {agent_id} by {activated_by}: {reason}")
        notify_oncall(f"AI KILL SWITCH ACTIVATED: {agent_id}")
```

---

## 🧪 Module 7 Exercise

**Design a Monitoring Alert:**

For your airline's AI chatbot, create 3 monitoring alerts:

1. **Alert 1 (Injection):**
   - Trigger condition: ________________
   - Severity: ________________
   - Automated response: ________________
   - Human response: ________________

2. **Alert 2 (Cost):**
   - Trigger condition: ________________
   - Threshold: ________________
   - Kill switch: yes/no

3. **Alert 3 (Data leakage):**
   - Detection method: ________________
   - Response time SLA: ________________
   - Regulatory notification required? ________________

---

## ➡️ Next: [Module 8 — Enterprise AI Architecture](module-08-enterprise-architecture.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 6: AI Governance](module-06-ai-governance.md) | [📚 References](references.md) | [Module 8: Enterprise Architecture](module-08-enterprise-architecture.md) |
