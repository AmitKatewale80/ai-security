# Lab 07: Confidential AI (SGX) - Protecting Passenger Data During Processing

## Overview

This lab demonstrates how Intel SGX enclaves can protect sensitive passenger
data (passport numbers, credit cards) during AI inference for fraud detection.

**Airline Attack Scenario:** A fraud detection model processes booking data
containing passport numbers and credit card details. Without SGX, this data
is exposed in memory during processing. With SGX, data remains encrypted
even during computation.

**Note:** This is a conceptual/simulated lab since SGX hardware is not
available. It demonstrates the principles and benefits of confidential computing.

---

## The Vulnerability

```python
# Without SGX: Data is plaintext in memory during inference
passenger_data = {"passport": "AB1234567", "cc": "4111-1111-1111-1111"}
prediction = model.predict(passenger_data)  # Data exposed in RAM!
# A memory dump attack can extract all passenger PII
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Passport Numbers | Identity theft, travel fraud |
| Credit Card Data | Financial fraud, PCI-DSS violation |
| Booking Patterns | Privacy violation |
| Frequent Flyer Data | Account takeover |
| Travel Itineraries | Physical security risk |

---

## Lab Structure

```
lab-07-confidential-ai-sgx/
├── 1_train_fraud_model.py           # Train fraud detection model
├── 2_unprotected_inference.py       # Shows memory exposure risk
├── 3_simulated_sgx_inference.py     # Shows encrypted memory concept
├── run_demo.py                      # Runs all steps in sequence
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-07-confidential-ai-sgx
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
python 1_train_fraud_model.py           # Train the model
python 2_unprotected_inference.py       # See data exposure
python 3_simulated_sgx_inference.py     # See SGX protection
```

---

## Defense Strategies

1. **SGX Enclaves** - Process data in encrypted memory
2. **Data Minimization** - Only send required fields to model
3. **Tokenization** - Replace PII with tokens before processing
4. **Memory Encryption** - Hardware-level memory protection
5. **Attestation** - Verify enclave integrity before sending data

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| ML Model Inference API | AML.T0040 | Data exposure during inference |
| Exfiltration via ML API | AML.T0024 | Stealing data from memory |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
