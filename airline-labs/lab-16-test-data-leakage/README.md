# Lab 16: AI Test Data Generation — PII Leakage

[![OWASP LLM](https://img.shields.io/badge/OWASP-LLM02-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how AI-generated test data can accidentally contain
**real PII from production** — because the AI model memorized training data.

## QA Scenario

Your team uses AI to generate realistic test data (passenger names, booking refs,
emails). The AI was trained on production data and sometimes reproduces REAL
passenger records in "synthetic" test data. This test data then lives in
non-secure environments (dev machines, CI logs, test databases).

## Scripts

```bash
python 1_generate_test_data.py       # AI generates "synthetic" test data
python 2_detect_pii_leakage.py       # Scanner finds real PII in generated data
python 3_defense_safe_generation.py  # Defense: validated synthetic generation
```

## Key Takeaway

> **Always validate AI-generated test data for PII leakage.**
> Use PII scanners on generated data before it enters non-secure environments.
