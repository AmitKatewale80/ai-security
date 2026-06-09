# Lab 10: Training Data Poisoning — Fuel Optimization Attack

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0020-red.svg)](https://atlas.mitre.org/techniques/AML.T0020)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.** Do not use for malicious activities.

---

## Overview

This lab demonstrates how an attacker can **poison training data** to corrupt
an airline's fuel optimization model — causing it to recommend 15-20% more
fuel than needed on every flight.

**The cost:** Extra fuel = extra weight = more fuel burned to carry that fuel.
For a large airline, this waste adds up to **$30-50M per year**.

---

## Airline Scenario

A disgruntled employee (or compromised data pipeline) modifies 10% of historical
fuel records, inflating the recorded fuel burn. When the model retrains quarterly,
it learns from the poisoned data and starts recommending excess fuel "to be safe."

Nobody notices because:
- Extra fuel isn't dangerous (unlike too little)
- The model's accuracy metrics still look good
- The increase is gradual (15% over baseline)

---

## Scripts

```bash
python 1_fuel_model.py              # Train fuel model on CLEAN data
python 2_poison_training_data.py    # Attacker corrupts 10% of records
python 3_retrain_poisoned.py        # Model retrains → recommends excess fuel
python 4_detect_poisoning.py        # Defense: statistical detection
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Poison Training Data | AML.T0020 | Corrupting fuel records to bias model |

---

## Key Takeaway

> **Your model is only as trustworthy as your training data.**
> Implement statistical validation on training data BEFORE retraining.
> Detect outliers, distribution shifts, and sudden changes in data patterns.
