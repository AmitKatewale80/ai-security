# 🛡️ Module 4: Defensive AI Security

> Building layered defenses that stop attacks without killing functionality.

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 3: Offensive Security](module-03-offensive-security.md) | Module 4 of 10 | [Module 5: Hands-on Labs](module-05-hands-on-labs.md) |

---

## Learning Objectives

After this module, you will be able to:
- Implement input/output guardrails for LLM applications
- Design human-in-the-loop approval workflows for AI agents
- Configure AI Gateway policies for access control
- Secure RAG systems against poisoning and unauthorized access
- Apply the principle of least privilege to AI agents
- Protect models from theft, tampering, and backdoors

---

## 4.1 Guardrails

### What Are Guardrails?

Filters that inspect, sanitize, or block AI inputs and outputs before they reach the model or the user.

```
USER INPUT → [INPUT GUARDRAIL] → LLM → [OUTPUT GUARDRAIL] → RESPONSE
                 │                              │
                 ├─ Injection detection          ├─ PII detection
                 ├─ Topic filtering              ├─ Hallucination check
                 ├─ Input sanitization           ├─ Policy compliance
                 └─ Rate limiting                └─ Toxicity filter
```

### Input Guardrails

| Guardrail | What It Does | Catches |
|-----------|-------------|---------|
| **Injection detector** | Scans for override patterns ("ignore instructions", "you are now...") | Direct prompt injection |
| **Topic filter** | Blocks off-topic requests ("tell me a joke", "write code") | Scope violations |
| **Length limiter** | Rejects excessively long inputs (context stuffing) | Resource abuse |
| **Encoding detector** | Flags base64, hex, rot13 in user input | Encoded attacks |
| **Language detector** | Flags multi-language inputs (often used for bypasses) | Multi-language attacks |

### Output Guardrails

| Guardrail | What It Does | Catches |
|-----------|-------------|---------|
| **PII filter** | Blocks passport numbers, credit cards, SSNs in output | Data leakage |
| **Policy checker** | Verifies response matches allowed actions | Unauthorized operations |
| **Hallucination detector** | Cross-checks facts against knowledge base | Misinformation |
| **Toxicity filter** | Blocks offensive, harmful, or biased content | Content policy |
| **Confidence scorer** | Flags low-confidence responses for review | Uncertain outputs |

### Implementation Pattern

```python
def secure_chat(user_input):
    # INPUT GUARDRAILS
    if injection_detector.is_suspicious(user_input):
        return "I can't process that request."
    if not topic_filter.is_on_topic(user_input, allowed_topics=["flights", "bookings"]):
        return "I can only help with flight and booking queries."
    
    # LLM CALL
    response = llm.generate(system_prompt + user_input)
    
    # OUTPUT GUARDRAILS
    if pii_filter.contains_pii(response):
        response = pii_filter.redact(response)
    if not policy_checker.is_compliant(response):
        return "I'm unable to complete that action."
    
    return response
```

---

## 4.2 Human in the Loop

### When AI Should NOT Decide Alone

| Action | Risk Level | Human Required? | Timeout Behavior |
|--------|-----------|----------------|-----------------|
| Answer FAQ | Low | No | N/A |
| Rebook to next flight | Low | No | N/A |
| Apply 10% discount | Medium | No (within policy) | N/A |
| Cancel a flight | Critical | YES | Action NOT taken |
| Override fatigue rules | Critical | YES | Action NOT taken |
| Access restricted data | High | YES | Action NOT taken |
| Apply >20% discount | High | YES | Standard rate |

### Human-in-the-Loop Pattern

```
AI Agent proposes action
        │
        ▼
[Is action within autonomy bounds?]
        │
    YES │           NO
        │           │
        ▼           ▼
  [EXECUTE]    [ESCALATE to human]
  + audit log        │
                     ▼
              [Human reviews]
                     │
              APPROVE │ DENY
                │         │
                ▼         ▼
          [EXECUTE]  [BLOCKED]
          + audit     + audit
```

### Key Design Decisions

1. **Fail-safe, not fail-open** — If human doesn't respond within timeout, action is NOT taken
2. **Clear presentation** — Show human: what action, why, impact estimate, risk rating
3. **Time-bounded** — 5-minute timeout for operational decisions, 24h for non-urgent
4. **Audit everything** — Log the decision regardless of outcome

**Lab:** 12 (IROPS agent with approval workflows)

---

## 4.3 AI Gateway

### What Is an AI Gateway?

A centralized enforcement point between users and AI models — like a WAF for AI.

```
┌──────────────────────────────────────────────┐
│                AI GATEWAY                      │
├──────────────────────────────────────────────┤
│                                               │
│  [Authentication] → Who are you?              │
│  [Authorization]  → What can you access?      │
│  [Rate Limiting]  → How fast?                 │
│  [Routing]        → Which model?              │
│  [Input Filter]   → Is input safe?            │
│  [Output Filter]  → Is output safe?           │
│  [Cost Tracking]  → How much spent?           │
│  [Audit Logging]  → Record everything         │
│                                               │
└──────────────────────────────────────────────┘
```

### Gateway Policies

| Policy | Rule | Example |
|--------|------|---------|
| Model ACL | Token X can only access model Y | Customer token → chatbot only |
| Rate limit | Max N requests per minute per token | 20 queries/min per partner |
| Budget cap | Max $X per day per token | $50/day for customer agent |
| Input size | Max N tokens per request | 4,096 tokens max |
| No overrides | Ignore X-Model-Override headers | Prevent header injection |
| Path sanitization | Reject `../` in model names | Prevent path traversal |
| Token binding | Token only works from registered IP | Prevent token reuse |

### What the Gateway Blocks

```
Attack: X-Model-Override: revenue-optimizer
Gateway: BLOCKED — override headers ignored

Attack: model=../crew-scheduler
Gateway: BLOCKED — path traversal detected

Attack: 5000 queries in 10 minutes
Gateway: BLOCKED at 100/min — rate limit exceeded

Attack: Stolen token from different IP
Gateway: BLOCKED — IP binding mismatch
```

**Lab:** 13 (gateway bypass and token abuse)

---

## 4.4 Secure RAG

### RAG Security Layers

```
┌────────────────────────────────────────────┐
│           SECURE RAG SYSTEM                 │
├────────────────────────────────────────────┤
│                                             │
│  INGESTION (documents entering KB):         │
│    ✓ Provenance verification                │
│    ✓ Source authentication                  │
│    ✓ Classification tagging                 │
│    ✓ Injection scanning                     │
│    ✓ Multi-source validation                │
│                                             │
│  RETRIEVAL (documents being queried):       │
│    ✓ Role-based access control              │
│    ✓ Classification enforcement             │
│    ✓ Query audit logging                    │
│                                             │
│  GENERATION (LLM response):                 │
│    ✓ Citation verification                  │
│    ✓ PII filtering                          │
│    ✓ Confidence scoring                     │
│    ✓ Output guardrails                      │
│                                             │
└────────────────────────────────────────────┘
```

### Access Control Matrix

| User Role | PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED |
|-----------|--------|----------|--------------|-----------|
| Ground Staff | ✓ | ✗ | ✗ | ✗ |
| Customer Service | ✓ | ✓ | ✗ | ✗ |
| Safety Investigator | ✓ | ✓ | ✓ | ✗ |
| Security Officer | ✓ | ✓ | ✓ | ✓ |

### Document Provenance Check

Before any document enters the knowledge base:
1. **Who uploaded it?** (verified identity, not anonymous)
2. **Is the source authoritative?** (official manual vs. unknown file)
3. **Does it contradict existing knowledge?** (anomaly detection)
4. **Has it been approved?** (document owner sign-off)

**Labs:** 04 (RAG data extraction), 14 (knowledge base poisoning)

---

## 4.5 Secure AI Agents

### The 5 Security Pillars for AI Agents

```
┌─────────────────────────────────────────────┐
│          SECURE AGENT FRAMEWORK              │
├─────────────────────────────────────────────┤
│                                              │
│  1. LEAST PRIVILEGE                          │
│     Only the tools needed, nothing more      │
│                                              │
│  2. HUMAN-IN-THE-LOOP                        │
│     Dangerous actions require approval       │
│                                              │
│  3. POLICY AS CODE                           │
│     Hard limits enforced by rules engine     │
│                                              │
│  4. AUTONOMY BOUNDS                          │
│     Defined action space, no tool discovery  │
│                                              │
│  5. AUDITABILITY                             │
│     Every action logged with full context    │
│                                              │
└─────────────────────────────────────────────┘
```

### Per-Agent Identity and Isolation

| Agent | Identity | Tools Allowed | Tools Blocked |
|-------|----------|--------------|---------------|
| booking-agent-001 | book_flight, check_loyalty | cancel_flight, shutdown_engine |
| maintenance-agent-002 | schedule_inspection, read_sensors | book_flight, modify_pricing |
| ops-agent-003 | reassign_gate, check_weather | cancel_flight (needs approval) |

### Policy Engine Rules

```yaml
agent_policies:
  booking_agent:
    max_discount_percent: 15
    max_rebooking_value: $2000
    max_affected_passengers: 1
    requires_approval: [cancel_flight, override_fare]
    blocked_actions: [shutdown_engine, access_crew_data]
    
  irops_agent:
    max_affected_passengers: 50
    requires_approval: [cancel_flight, override_fatigue]
    budget_limit_per_day: $50
    max_self_calls: 3
    timeout_seconds: 60
```

**Labs:** 12 (agent security pillars), 16 (cross-agent escalation), 17 (cost governance)

---

## 4.6 Model Protection

### Protecting Models from Theft

| Defense | How It Works | Effectiveness |
|---------|-------------|--------------|
| Rate limiting | Max queries per time window | Medium (slows attack) |
| Differential privacy | Add noise to responses | High (degrades clone quality) |
| Query pattern detection | Flag systematic probing | Medium (detectable patterns) |
| Watermarking | Embed identifiable patterns in outputs | Low (detection, not prevention) |
| API restrictions | Limit batch sizes for suspicious users | Medium |

### Protecting Models from Tampering

| Defense | How It Works | Effectiveness |
|---------|-------------|--------------|
| Cryptographic signing (ECDSA) | Sign model hash at certification | Very High |
| Hash verification before loading | Check integrity pre-deployment | Very High |
| Model class allowlisting | Only load known model types | High |
| Code scanning | Detect malicious patterns in model code | High |
| Behavioral sandboxing | Run model in isolated environment first | Medium |

### Protecting Models from Supply Chain

| Defense | How It Works | Effectiveness |
|---------|-------------|--------------|
| Publisher verification | Only load from approved sources | High |
| trust_remote_code=False | Never execute arbitrary model code | Very High |
| Entropy analysis | Detect obfuscated code | Medium |
| Import analysis | Flag suspicious library imports | High |
| Registry scanning | Scan all models before admission | High |

**Labs:** 01 (supply chain scanning), 02 (API protection), 05 (backdoor detection), 06 (cryptographic signing), 08 (differential privacy)

---

## 4.7 Defense-in-Depth Summary

```
LAYER 1: PERIMETER
  AI Gateway → Authentication, rate limiting, routing

LAYER 2: INPUT
  Guardrails → Injection detection, topic filtering, sanitization

LAYER 3: PROCESSING
  Agent security → Least privilege, policy engine, autonomy bounds

LAYER 4: DATA
  RAG security → Access control, provenance, classification

LAYER 5: OUTPUT
  Guardrails → PII filtering, policy compliance, toxicity

LAYER 6: MONITORING
  Audit + SIEM → Logging, anomaly detection, alerting

LAYER 7: GOVERNANCE
  Human oversight → Approval workflows, review processes, kill switches
```

No single layer is sufficient. Defense-in-depth means: if layer 2 misses an injection, layer 3 blocks the tool call, layer 4 blocks the file access, and layer 5 blocks the PII in the response.

---

## 🧪 Module 4 Exercise

**Design a Defense Stack:**

For your airline's IROPS (Irregular Operations) AI agent, design:

1. **3 input guardrails:** What do you filter before the LLM?
2. **5 policy rules:** What hard limits does the policy engine enforce?
3. **3 actions requiring human approval:** What can't the agent do alone?
4. **Audit log schema:** What do you record for each action?
5. **Kill switch:** How do you shut it down in an emergency?

---

## ➡️ Next: [Module 5 — Hands-on Enterprise Labs](module-05-hands-on-labs.md)

---

| ← Previous | [🏠 Academy Home](README.md) | Next → |
|:---:|:---:|:---:|
| [Module 3: Offensive Security](module-03-offensive-security.md) | [📚 References](references.md) | [Module 5: Hands-on Labs](module-05-hands-on-labs.md) |
