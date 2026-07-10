# Secure Development for AI Applications

Secure coding practices for AI applications, including prompt engineering security and safe integration patterns.

## Overview

AI application development introduces unique security concerns in how prompts are constructed, how models are invoked, and how outputs are handled. Developers need specific guidance beyond traditional secure coding.

## Secure Prompt Engineering

| Practice | Description | Risk Mitigated |
|----------|-------------|----------------|
| Clear delimiters | Separate instructions from user input | Instruction confusion |
| Role specification | Define model behavior explicitly | Role hijacking |
| Output constraints | Specify format and boundaries | Freeform exploitation |
| Minimal context | Only include necessary information | Data leakage |
| No secrets in prompts | Keep credentials out of system prompts | Secret exposure |
| Versioned prompts | Track all prompt changes in VCS | Unauthorized modification |

## Secure Integration Patterns

### API Integration
- Use service accounts with minimal permissions
- Implement retry logic with exponential backoff
- Set timeouts on all model calls
- Handle errors without exposing internal details

### Data Handling
- Sanitize inputs before prompt construction
- Validate outputs before returning to users
- Never pass raw user input directly to model
- Implement content-length limits

### Agent Development
- Define explicit tool schemas (don't allow arbitrary tool use)
- Validate all tool call parameters
- Log all tool invocations
- Implement action confirmation for destructive operations

## Common Vulnerabilities

1. **String concatenation prompts** — User input injected directly
2. **Overly permissive tools** — Agents with filesystem/network access
3. **Missing output validation** — Returning raw model output
4. **Hardcoded credentials** — API keys in source code
5. **Excessive context** — Including unnecessary data in prompts

## Secure Code Review Checklist

- [ ] No user input directly concatenated into prompts
- [ ] All model outputs validated before use
- [ ] Credentials stored in secrets manager
- [ ] Error handling doesn't expose system details
- [ ] Tool permissions follow least privilege
- [ ] Rate limiting implemented on AI endpoints

## Related Labs

- [Lab 18 — AI Code Review Bypass](../../airline-labs/lab-18-ai-code-review-bypass/) — Exploiting insecure AI coding patterns

## Related Academy Module

- [Academy Module 9 — Secure SDLC](../../airline-labs/academy/module-09-secure-sdlc.md)

---

| [← Previous](02-threat-modeling.md) | [Back to Module](README.md) | [Next →](04-security-testing.md) |
