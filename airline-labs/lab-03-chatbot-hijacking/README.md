# Lab 03: Hijacking the Airline Customer Service Chatbot

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0051-red.svg)](https://atlas.mitre.org/techniques/AML.T0051)

**Author:** AmitK | [MIT License](../../labs/LICENSE)

> ⚠️ **Educational purposes only.** Do not use for malicious activities.

---

## Overview

This lab demonstrates **Indirect Prompt Injection** against an airline's AI customer service chatbot. An attacker hides malicious instructions inside a policy document. When the chatbot reads the document to help a passenger, it follows the hidden instructions and exposes sensitive passenger data (passport numbers, PNR records).

---

## Airline Scenario

**SkyAssist** is the airline's AI chatbot that helps passengers with:
- Rebooking flights after cancellations
- Answering policy questions
- Looking up booking information

**The Attack:**
1. Attacker crafts a "policy update" document with hidden instructions at the bottom
2. A passenger (or the attacker) asks: "Summarize the rebooking policy"
3. The chatbot reads the document and follows the hidden instructions
4. It reads `passenger_data/pnr_records.json` — exposing passport numbers, emails, phone numbers

**Business Impact:**
- GDPR violation (€20M+ fine potential)
- Passenger identity theft
- DOT regulatory action
- Massive reputation damage

---

## Prerequisites

- Python 3.9+
- OpenRouter API Key ([openrouter.ai](https://openrouter.ai))

---

## Setup

```bash
cd airline-labs/lab-03-chatbot-hijacking
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt

# Configure API key
copy .env.example .env
# Edit .env and add your OpenRouter API key
```

---

## Running the Lab

### Quick Demo (Non-interactive)

```bash
python run_attack_demo.py
```

Shows the full attack flow automatically with detailed logging.

### Interactive Demo

**Vulnerable chatbot:**
```bash
python 1_vulnerable_chatbot.py
```
Then type: `Summarize the rebooking policy: ./policy_documents/rebooking_policy_update.html`

**Secured chatbot (same attack, blocked):**
```bash
python 2_secured_chatbot.py
```
Try the same prompt — the attack will be detected and halted.

---

## Attack Payloads

| File | Hidden Instruction |
|------|-------------------|
| `rebooking_policy_update.html` | Tricks chatbot into reading PNR records |
| `loyalty_program_faq.html` | Tricks chatbot into reading .env (API keys) |

---

## Defense Layers (2_secured_chatbot.py)

| Layer | Defense | What It Blocks |
|-------|---------|---------------|
| 1 | Path Sandboxing | Only `policy_documents/` readable |
| 2 | Injection Detection | Regex patterns catch manipulation |
| 3 | PII Blocking | Never expose passport/card numbers |
| 4 | Halt on Attack | Stop processing immediately |
| 5 | Audit Logging | All security events recorded |

---

## Side-by-Side Comparison

| Action | Vulnerable | Secured |
|--------|-----------|---------|
| Read policy document | ✅ Allowed | ✅ Allowed |
| Detect hidden instructions | ❌ No | ✅ **Detected** |
| Read passenger PNR data | ✅ **Data exposed!** | 🚫 Path blocked |
| Read .env (API keys) | ✅ **Keys exposed!** | 🚫 Path blocked |
| Continue after attack | ✅ Normal response | 🚫 **HALTED** |
| Audit trail | ❌ None | ✅ Full logging |

---

## Key Takeaway

> **LLM chatbots with file access are high-value targets.**
> Any document the chatbot reads can contain hidden instructions.
> Implement path sandboxing, injection detection, and content sanitization.

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| LLM Prompt Injection | AML.T0051 | Indirect injection via documents |
| LLM Meta Prompt Extraction | AML.T0043 | Extracting system prompts |
