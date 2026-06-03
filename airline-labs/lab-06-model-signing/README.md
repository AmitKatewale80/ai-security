# Lab 06: Model Signing - Tampered Predictive Maintenance Model

## Overview

This lab demonstrates how cryptographic model signing detects tampering
of an engine health prediction model that was modified to suppress
failure warnings.

**Airline Attack Scenario:** An attacker (or negligent insider) tampers with
the predictive maintenance model to suppress engine failure warnings,
potentially leading to catastrophic in-flight failures.

---

## The Vulnerability

```python
# Without signing, a tampered model loads without any warning
model = joblib.load("engine_health_model.joblib")
# Model has been modified to NEVER predict "CRITICAL" status
# Maintenance team misses engine failures!
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Engine Health Predictions | Missed critical failures |
| Maintenance Scheduling | Unsafe aircraft dispatch |
| Safety Margins | Reduced operational safety |
| Regulatory Compliance | Airworthiness violations |
| Passenger Safety | Potential catastrophic failure |

---

## Lab Structure

```
lab-06-model-signing/
├── 1_train_model.py          # Train engine health prediction model
├── 2_sign_model.py           # Sign model with ECDSA
├── 3_tamper_model.py         # Tamper model to suppress warnings
├── 4_verify_and_load.py      # Verify signature before loading
├── run_demo.py               # Runs all steps in sequence
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-06-model-signing
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Demo

### Full Demo (Recommended)
```bash
python run_demo.py
```

### Individual Steps
```bash
python 1_train_model.py       # Train the engine health model
python 2_sign_model.py        # Generate keys and sign the model
python 3_tamper_model.py      # Simulate tampering attack
python 4_verify_and_load.py   # Verify signature catches tampering
```

---

## Defense Strategies

1. **ECDSA Signing** - Cryptographic signature on model artifacts
2. **Key Management** - HSM-stored signing keys
3. **CI/CD Integration** - Sign during build, verify at deployment
4. **Certificate Chain** - Trust hierarchy for model publishers
5. **Audit Trail** - Log all signing and verification events

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Backdoor ML Model | AML.T0011 | Tampered model behavior |
| Evade ML Model | AML.T0015 | Suppressing safety predictions |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
