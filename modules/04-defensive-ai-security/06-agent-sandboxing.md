# Agent Sandboxing & Containment

Constraining AI agent permissions through tool scoping, policy engines, and execution sandboxes.

## Overview

AI agents with tool access can perform real-world actions (file I/O, API calls, code execution). Without containment, a compromised or manipulated agent can cause significant damage.

## Containment Strategies

| Strategy | Description | Trade-off |
|----------|-------------|-----------|
| Tool scoping | Limit which tools an agent can access | Reduces capability |
| Permission boundaries | Define what each tool can do | Adds complexity |
| Execution sandboxing | Run agent code in isolated environments | Performance overhead |
| Policy engines | Real-time policy evaluation on actions | Latency impact |
| Human-in-the-loop | Require approval for sensitive actions | Slower execution |
| Budget limits | Cap resource consumption per session | May interrupt workflows |

## Tool Scoping Best Practices

1. **Principle of least privilege** — Only grant tools needed for the task
2. **Read vs. write separation** — Distinguish information retrieval from actions
3. **Scope parameters** — Limit tool arguments (e.g., only specific directories)
4. **Temporal limits** — Expire tool access after session/task completion
5. **Chain limits** — Cap the number of sequential tool calls

## Policy Engine Architecture

```
Agent Decision → Policy Engine → [Allow/Deny/Escalate] → Tool Execution
                      ↓
              Policy Rules:
              - Action type restrictions
              - Resource access limits
              - Rate limiting
              - Sensitive data guards
              - Cost thresholds
```

## Sandbox Implementation

- **Container isolation** — Run agent in Docker/microVM
- **Network restrictions** — Limit egress to approved endpoints
- **Filesystem isolation** — Mount only necessary paths read-only
- **Resource limits** — CPU, memory, time caps
- **Audit logging** — Record all actions for review

## Related Labs

- [Lab 12 — AI Agent Security](../../airline-labs/lab-12-ai-agent-security/) — Agent permission exploitation
- [Lab 16 — Agent Identity](../../airline-labs/lab-16-agent-identity/) — Identity and authorization for agents

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](05-rag-security.md) | [Back to Module](README.md) | [Next →](07-model-security.md) |
