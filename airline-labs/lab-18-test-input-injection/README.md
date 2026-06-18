# Lab 18: Prompt Injection via Test Inputs

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0051-red.svg)](https://atlas.mitre.org/techniques/AML.T0051)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how **test inputs from the application under test**
can contain prompt injection that hijacks the AI testing tool itself.

## QA Scenario

Your AI test runner reads application responses to validate them.
The application under test returns a crafted response containing hidden
instructions that manipulate the AI test runner into:
- Marking failed tests as PASSED
- Skipping remaining security tests
- Exfiltrating test environment credentials

## Scripts

```bash
python 1_ai_test_runner.py           # AI-assisted test execution
python 2_injected_app_response.py    # App response hijacks the test AI
python 3_defense_input_isolation.py  # Defense: isolate app output from AI instructions
```

## Key Takeaway

> **Never feed raw application output directly into AI prompts.**
> Treat all application responses as UNTRUSTED DATA — sanitize before AI processing.
