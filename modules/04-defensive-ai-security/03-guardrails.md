# LLM Guardrail Frameworks

Guardrails provide programmable safety boundaries for LLM applications. This module covers leading frameworks and custom implementation patterns.

## What Are Guardrails?

Guardrails are runtime enforcement layers that constrain LLM behavior by validating inputs, outputs, and intermediate reasoning against defined policies.

## Framework Comparison

| Framework | Approach | Strengths | Use Case |
|-----------|----------|-----------|----------|
| NeMo Guardrails | Colang dialogue flows | Conversation control, topical rails | Customer-facing chatbots |
| Guardrails AI | Pydantic validators | Structured output validation | API responses, data extraction |
| LangChain Guards | Chain-based checks | Ecosystem integration | LangChain applications |
| Rebuff | ML + heuristics | Prompt injection detection | Input security |
| Custom rules engine | Policy-as-code | Full flexibility | Enterprise-specific needs |

## Guardrail Types

1. **Topical guardrails** — Keep conversations on-topic
2. **Safety guardrails** — Block harmful/toxic content
3. **Security guardrails** — Prevent injection, exfiltration
4. **Factuality guardrails** — Reduce hallucination
5. **Privacy guardrails** — Block PII disclosure
6. **Compliance guardrails** — Enforce regulatory requirements

## Implementation Considerations

- **Latency impact** — Each guardrail adds processing time
- **False positive rate** — Over-aggressive rails degrade UX
- **Bypass resistance** — Guardrails must resist adversarial evasion
- **Observability** — Log all guardrail triggers for analysis
- **Fail-safe defaults** — Block on guardrail errors, don't pass through

## Architecture Pattern

```
Input → [Input Rails] → LLM → [Output Rails] → Response
              ↓                       ↓
         Block/Modify           Block/Modify
              ↓                       ↓
         Fallback Response      Fallback Response
```

## Related Labs

- [Lab 09 — Chatbot Vulnerability Testing](../../airline-labs/lab-09-chatbot-vulnerability-testing/) — Testing guardrail effectiveness
- [Lab 11 — Garak Red Teaming](../../airline-labs/lab-11-garak-red-teaming/) — Automated guardrail bypass testing

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](02-output-filtering.md) | [Back to Module](README.md) | [Next →](04-access-control.md) |
