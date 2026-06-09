# Lab 15: AI-Powered CI/CD Pipeline Manipulation

[![OWASP LLM](https://img.shields.io/badge/OWASP-LLM06-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how attackers can trick an **AI-powered test selector**
in CI/CD into skipping security tests. The AI decides "low-risk change,
skip security scan" — but the change contains a critical vulnerability.

## QA Scenario

Your CI/CD pipeline uses AI to optimize test runs:
- "Docs only change → skip backend tests"
- "Config change → run smoke tests only"
- "High-risk code change → run full security suite"

An attacker disguises their vulnerable code as a "config update" and the
AI skips the security scan.

## Scripts

```bash
python 1_smart_pipeline.py           # AI test selector (decides what to run)
python 2_attacker_bypasses_ci.py     # Attacker tricks AI into skipping security
python 3_vulnerability_ships.py      # Vuln code is now in production!
python 4_defense_mandatory_gates.py  # Defense: mandatory gates AI cannot skip
```

## Key Takeaway

> **AI should RECOMMEND test optimizations, never DECIDE to skip security gates.**
> Mandatory security tests must always run regardless of AI assessment.
