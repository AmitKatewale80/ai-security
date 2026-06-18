# Lab 14: AI Test Generation — False Confidence

[![OWASP LLM](https://img.shields.io/badge/OWASP-LLM09-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.**

---

## Overview

This lab demonstrates how AI-generated test cases can give **false confidence** —
all tests pass, but they don't actually validate the important behavior.
Bugs ship to production because the test suite is weak.

## QA Scenario

Your team uses AI to generate test scripts for a booking system. The AI creates
20 tests that all PASS. But mutation testing reveals the tests wouldn't catch
actual bugs — they have tautological assertions or miss edge cases.

## Scripts

```bash
python 1_buggy_application.py        # Airline booking app with subtle bugs
python 2_ai_generates_tests.py       # AI writes tests — all PASS!
python 3_mutation_testing.py          # Mutation test reveals tests are WEAK
python 4_defense_test_validation.py   # Defense: validate tests with mutation score
```

## Key Takeaway

> **Passing tests ≠ good tests.** Always validate AI-generated tests with
> mutation testing. If mutants survive, your tests aren't catching real bugs.
