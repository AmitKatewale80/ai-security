# Lab 13: AI Code Review Bypass

[![OWASP LLM](https://img.shields.io/badge/OWASP-LLM05-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how attackers can craft code that **looks safe to an AI reviewer**
but contains hidden vulnerabilities. The AI says "LGTM" while SQL injection,
hardcoded credentials, or auth bypasses slip through.

## QA Scenario

Your QA team uses AI for automated code reviews. A developer submits a PR with
obfuscated vulnerabilities. The AI reviewer doesn't flag them because the code
uses misdirection (innocent variable names, misleading comments, split logic).

## Scripts

```bash
python 1_setup_code_review_ai.py     # Set up AI code reviewer rules
python 2_submit_vulnerable_code.py   # Submit code with hidden vulnerabilities
python 3_ai_approves_bad_code.py     # AI says "approved" — WRONG!
python 4_defense_multi_layer.py      # Defense: AI + SAST + mandatory checklist
```

## Key Takeaway

> **Never rely on AI as your ONLY code review gate.**
> Combine AI review + static analysis (SAST) + human review for security-critical code.
