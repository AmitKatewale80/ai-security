# Input Validation & Sanitization for LLMs

Effective input validation is the first line of defense against prompt injection and other LLM attacks. This module covers detection, filtering, and enforcement strategies.

## Why Input Validation Matters

LLMs interpret all input as instructions by default. Without validation, attackers can inject commands, bypass policies, or extract sensitive data through crafted prompts.

## Key Techniques

| Technique | Description | Effectiveness |
|-----------|-------------|---------------|
| Injection pattern detection | Regex/ML classifiers to flag known injection patterns | Medium-High |
| Encoding detection | Detect base64, hex, unicode tricks used to bypass filters | Medium |
| Length limits | Enforce max token/character counts per request | Low-Medium |
| Schema validation | Validate structured inputs (JSON, function calls) | High |
| Canary tokens | Embed markers to detect prompt leakage | Medium |
| Input classification | ML model to classify intent before processing | High |

## Implementation Checklist

- [ ] Define allowed input patterns per endpoint
- [ ] Implement multi-layer detection (regex + ML classifier)
- [ ] Detect and normalize encoding tricks (unicode, base64, homoglyphs)
- [ ] Set appropriate length limits per use case
- [ ] Log and alert on rejected inputs
- [ ] Test with known injection datasets (e.g., Garak payloads)
- [ ] Rate-limit repeated suspicious inputs

## Common Bypass Techniques to Defend Against

1. **Token smuggling** — Splitting injection across multiple tokens
2. **Encoding evasion** — Base64, ROT13, Unicode homoglyphs
3. **Context manipulation** — Exploiting system prompt boundaries
4. **Payload fragmentation** — Distributing attack across conversation turns

## Related Labs

- [Lab 03 — Chatbot Hijacking](../../airline-labs/lab-03-chatbot-hijacking/) — Direct/indirect prompt injection attacks
- [Lab 09 — Chatbot Vulnerability Testing](../../airline-labs/lab-09-chatbot-vulnerability-testing/) — Automated injection testing

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](../03-offensive-ai-security/) | [Back to Module](README.md) | [Next →](02-output-filtering.md) |
