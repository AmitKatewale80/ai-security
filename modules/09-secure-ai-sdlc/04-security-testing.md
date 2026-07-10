# AI Security Testing

Red teaming, mutation testing, fuzz testing, and mandatory security gates for AI systems in CI/CD.

## Overview

AI security testing combines traditional application security testing with AI-specific techniques. Tests must cover prompt injection, output safety, model robustness, and agent behavior.

## Testing Pyramid for AI

| Level | Type | Scope | Frequency |
|-------|------|-------|-----------|
| Unit | Prompt tests, guardrail checks | Individual components | Every commit |
| Integration | End-to-end flow testing | Full pipeline | Every PR |
| Security scan | Automated vulnerability scanning | All endpoints | Daily |
| Red team | Manual adversarial testing | Full system | Monthly |
| Penetration | Deep exploitation testing | Production-like | Quarterly |

## Mandatory CI/CD Security Gates

1. **Input validation tests** — Known injection payloads must be blocked
2. **Output safety tests** — Model must not leak test PII
3. **Guardrail effectiveness** — All guardrails must pass regression tests
4. **Dependency scanning** — No known vulnerabilities in dependencies
5. **Prompt regression** — Prompt changes don't introduce vulnerabilities
6. **Cost boundaries** — Token consumption within expected bounds

## Red Teaming Techniques

- **Direct injection** — Explicit override instructions
- **Indirect injection** — Payloads in context documents
- **Multi-turn manipulation** — Gradual boundary erosion
- **Encoding evasion** — Base64, unicode tricks
- **Role-play exploitation** — Fictional scenarios to bypass safety
- **Tool abuse** — Manipulating agent tool usage

## Mutation Testing for AI

- Mutate guardrail rules → verify detection still works
- Mutate system prompts → verify behavior unchanged
- Mutate input filters → verify attacks still blocked
- Mutate access controls → verify unauthorized access denied

## Related Labs

- [Lab 09 — Chatbot Vulnerability Testing](../../airline-labs/lab-09-chatbot-vulnerability-testing/) — Structured security testing
- [Lab 19 — AI Test Generation](../../airline-labs/lab-19-ai-test-generation/) — Automated test generation
- [Lab 20 — AI CI/CD Manipulation](../../airline-labs/lab-20-ai-cicd-manipulation/) — CI/CD security gates

## Related Academy Module

- [Academy Module 9 — Secure SDLC](../../airline-labs/academy/module-09-secure-sdlc.md)

---

| [← Previous](03-secure-development.md) | [Back to Module](README.md) | [Next →](05-supply-chain-security.md) |
