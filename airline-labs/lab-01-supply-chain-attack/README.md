# Lab 01: Malicious Flight Delay Prediction Model - Supply Chain Attack

## 🎯 Overview

This lab demonstrates how **`trust_remote_code=True`** in HuggingFace's `transformers` library can be exploited to execute arbitrary code — including a **reverse shell** that gives attackers full access to airline operational systems.

**Airline Attack Scenario:** An attacker uploads a malicious "flight delay prediction model" to the airline's internal model registry. When the operations team loads it for the daily delay forecast dashboard, the attacker gets shell access to systems containing crew schedules, passenger manifests, and gate assignments.

---

## 🔥 The Vulnerability

```python
from transformers import AutoModelForCausalLM

# This single line can compromise your airline's operations network!
model = AutoModelForCausalLM.from_pretrained(
    "skyops-ai/flight-delay-predictor-v2",
    trust_remote_code=True  # ← Downloads & executes .py files!
)
```

When `trust_remote_code=True`:
1. HuggingFace reads `config.json` with `auto_map` pointing to custom code
2. Downloads Python files (e.g., `modeling_flightdelay.py`) to cache
3. **Imports and executes** the Python code during model instantiation
4. Malicious code in `__init__` runs with your privileges!

---

## ✈️ Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Passenger Name Records (PNR) | GDPR/DOT violation, identity theft |
| Crew Schedules & Personal Data | Privacy breach, operational disruption |
| Flight Plans & Gate Assignments | Security risk, operational chaos |
| Pricing & Revenue Data | Competitive intelligence theft |
| Maintenance Records | Safety certification compromise |

---

## 📁 Lab Structure

```
lab-01-supply-chain-attack/
├── 1_attacker_listener.py              # Attacker's reverse shell listener
├── 2_victim_loads_model.py             # Ops team loads model (gets compromised)
├── 3_safe_model_loading.py             # Safe version with airline security scanner
├── airline_model_scanner.py            # Airline-specific security scanner
├── hub_cache/                          # Simulated model registry cache
│   └── models--skyops-ai--flight-delay-predictor-v2/
│       ├── config.json                 # Points to custom code via auto_map
│       ├── modeling_flightdelay.py     # Custom model code (contains backdoor)
│       ├── special_tokens_map.json     # Special tokens
│       └── tokenizer_config.json       # Tokenizer configuration
├── requirements.txt
├── .env.example                        # Configuration template
└── reset.py                            # Cleanup script
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Windows/Linux/macOS
- Two terminal windows

### Setup

```bash
cd airline-labs/lab-01-supply-chain-attack
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

### Configure

```bash
# Copy environment template
copy .env.example .env
# Default is localhost (same machine demo)
```

---

## 🎬 Running the Demo

### Demo 1: The Attack

**Terminal 1 - Attacker (simulating external threat actor):**
```bash
python 1_attacker_listener.py
```

**Terminal 2 - Victim (airline ops team member):**
```bash
python 2_victim_loads_model.py
```

**What happens:**
1. Ops team member loads "flight delay predictor" from model registry
2. Model's `__init__` triggers reverse shell (disguised as "telemetry")
3. Attacker gets full shell on the airline's operations server
4. Victim sees normal delay predictions — doesn't notice compromise!

**Attacker's view (what they can now access):**
```
$ cat /opt/airline/config/crew_schedules.json
$ cat /opt/airline/data/passenger_manifests/QA447.json
$ env | grep -i API_KEY
$ cat ~/.aws/credentials
```

### Demo 2: The Defense

**Terminal 2 - Security-aware team member:**
```bash
python 3_safe_model_loading.py
```

**Output:**
```
🔍 AIRLINE SECURITY: Inspecting model before loading...

[1/5] Verifying publisher trust level...
  ⚠️  UNTRUSTED publisher: skyops-ai
  
[2/5] Checking if model requires custom code execution...
  ⚠️  Model requires trust_remote_code=True
  ⚠️  Will execute: ['modeling_flightdelay.FlightDelayPredictor']

[3/5] Scanning downloaded code for red flags...
  🚨 DANGEROUS CODE DETECTED:
     - modeling_flightdelay.py: Network socket creation
     - modeling_flightdelay.py: Process forking
     - modeling_flightdelay.py: PTY shell spawning

════════════════════════════════════════════════════════════
  ❌ MODEL LOADING BLOCKED - AIRLINE SECURITY POLICY VIOLATION
════════════════════════════════════════════════════════════
```

---

## 🛡️ Airline Defense Strategies

### Airline Model Registry Policy

```python
# AIRLINE POLICY: Only approved publishers allowed
APPROVED_PUBLISHERS = [
    'airline-internal',      # Our own models
    'google',               # Verified vendor
    'microsoft',            # Verified vendor
    'ibm-research',         # Verified vendor
]

# NEVER allow trust_remote_code from external sources
# ALL models must pass security scan before deployment
```

### Safest Loading Pattern

```python
model = AutoModelForCausalLM.from_pretrained(
    "model",
    trust_remote_code=False,  # No custom code execution
    use_safetensors=True,     # No pickle deserialization
)
```

---

## 🧹 Reset Lab

```bash
python reset.py
```

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY.**

This lab demonstrates security vulnerabilities in AI/ML supply chains
to help airline security teams understand and mitigate risks.
Do not use these techniques maliciously.

---

## 📊 MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| ML Supply Chain Compromise | AML.T0010 | Malicious model in registry |
| Backdoor ML Model | AML.T0011 | Hidden reverse shell in model code |

---

**Author:** AmitK | MIT License
