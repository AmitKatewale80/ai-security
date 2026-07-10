# Lab 05: Malicious Code Injection - Backdoored Baggage Screening Model

## Overview

This lab demonstrates how an attacker can inject malicious code into a
baggage X-ray classification model. During inference, the backdoored model
exfiltrates data about flagged luggage to an external endpoint.

**Airline Attack Scenario:** A supply chain attacker modifies the baggage
screening AI model to silently exfiltrate information about flagged items,
potentially enabling smuggling or targeted theft.

---

## The Vulnerability

```python
# Attacker adds a malicious layer that activates during inference
class BackdooredModel:
    def predict(self, x_ray_image):
        result = self.original_predict(x_ray_image)
        if result == "FLAGGED":
            # Silently exfiltrate flagged item data
            self._send_to_attacker(x_ray_image, result)
        return result  # Normal result returned - nobody notices!
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Flagged Luggage Data | Smuggling enablement |
| Screening Patterns | Security bypass intelligence |
| Passenger-Bag Links | Targeted theft |
| Detection Thresholds | Evasion of security |
| Screening Gaps | Timing attacks on security |

---

## Lab Structure

```
lab-05-malicious-code-injection/
├── 1_train_model.py          # Train benign baggage screening model
├── 2_inject_backdoor.py      # Inject malicious exfiltration layer
├── 3_run_inference.py        # Shows backdoor activating during screening
├── 4_secure_loading.py       # Detects the backdoor before loading
├── run_demo.py               # Runs all steps in sequence
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-05-malicious-code-injection
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
python 1_train_model.py       # Train the legitimate model
python 2_inject_backdoor.py   # Inject the backdoor
python 3_run_inference.py     # See the backdoor in action
python 4_secure_loading.py    # Detect and block the backdoor
```

---

## Defense Strategies

1. **Model Integrity Checks** - Hash verification before loading
2. **Code Inspection** - Scan model files for network calls
3. **Sandboxed Inference** - Run models in isolated environments
4. **Network Monitoring** - Detect unexpected outbound connections
5. **Model Signing** - Cryptographic signatures on approved models

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Backdoor ML Model | AML.T0011 | Hidden malicious behavior |
| ML Supply Chain Compromise | AML.T0010 | Tampered model in pipeline |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-05-backdoored-baggage-screening-model) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [⚔️ Module 3: Offensive Security](../academy/module-03-offensive-security.md#34-data-poisoning) | Backdoor techniques |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#46-model-protection) | Model scanning defenses |
| [🚀 Module 9: Secure SDLC](../academy/module-09-secure-sdlc.md#95-supply-chain-security) | Supply chain controls |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 04: RAG Extraction](../lab-04-rag-data-extraction/) | Lab 05 of 23 | [Lab 06: Model Signing](../lab-06-model-signing/) |
