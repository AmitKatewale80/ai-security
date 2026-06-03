# Lab 08: TPM Attestation - Verifying Onboard AI System Integrity

## Overview

This lab demonstrates how TPM (Trusted Platform Module) attestation can verify
that an aircraft's predictive maintenance AI model hasn't been tampered with
before each flight.

**Airline Attack Scenario:** Before dispatch, the aircraft's onboard AI system
must prove its integrity. TPM attestation creates a chain of trust from hardware
to the AI model, ensuring no tampering has occurred.

**Note:** This is a simulated lab - real TPM requires hardware support.

---

## The Vulnerability

```python
# Without TPM: No way to verify model integrity on the aircraft
model = load_model("/onboard/engine_health.model")
# Was this model tampered with during overnight maintenance?
# Was the system compromised by a malicious USB device?
# Nobody knows until something goes wrong at 35,000 feet!
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Onboard AI Models | Tampered predictions in flight |
| System Firmware | Compromised boot chain |
| Sensor Calibration | Incorrect readings |
| Safety Margins | Reduced operational safety |
| Dispatch Decision | Unsafe aircraft cleared for flight |

---

## Lab Structure

```
lab-08-tpm-attestation/
├── 1_create_certified_model.py    # Create and certify the model
├── 2_measure_model.py             # Compute PCR measurements
├── 3_simulate_attestation.py      # Full attestation flow
├── 4_tamper_and_detect.py         # Tamper and detect via TPM
├── run_demo.py                    # Runs all steps in sequence
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-08-tpm-attestation
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
python 1_create_certified_model.py    # Create certified model
python 2_measure_model.py             # Measure model hash (PCR extend)
python 3_simulate_attestation.py      # Run attestation protocol
python 4_tamper_and_detect.py         # Tamper and detect
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Backdoor ML Model | AML.T0011 | Tampered onboard model |
| ML Supply Chain Compromise | AML.T0010 | Compromised update process |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
