# Lab 17: AI Bug Triage Manipulation

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0051-red.svg)](https://atlas.mitre.org/techniques/AML.T0051)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how an attacker can craft bug reports that manipulate
an AI triage system into **deprioritizing critical security vulnerabilities**.

## QA Scenario

Your team uses AI to auto-prioritize incoming bugs. Attacker submits a
real security vulnerability but writes it to look like a cosmetic/low-priority
issue. The AI assigns it "Low" priority → security team never sees it.

## Scripts

```bash
python 1_ai_triage_system.py         # AI bug prioritizer
python 2_manipulate_triage.py        # Attacker crafts deceptive bug reports
python 3_defense_keyword_override.py # Defense: security keywords force escalation
```

## Key Takeaway

> **AI triage should NEVER downgrade bugs containing security keywords.**
> Any mention of auth, injection, credential, bypass → auto-escalate regardless of AI score.
