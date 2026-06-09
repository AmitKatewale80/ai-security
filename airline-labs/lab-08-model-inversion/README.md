# Lab 08: Model Inversion Attack on Crew Scheduling

[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0024-red.svg)](https://atlas.mitre.org/techniques/AML.T0024)
[![MITRE ATLAS](https://img.shields.io/badge/ATLAS-AML.T0044-red.svg)](https://atlas.mitre.org/techniques/AML.T0044)

**Author:** AmitK | MIT License

> ⚠️ **Educational purposes only.** Do not use for malicious activities.

---

## Overview

This lab demonstrates a **model inversion attack** where an attacker extracts
sensitive TRAINING DATA (crew schedules, home bases, work patterns) by querying
the crew optimization API.

**Key difference from Lab 02:**
- Lab 02 steals the MODEL (pricing algorithm)
- Lab 08 steals the DATA the model was trained on (crew personal info)

---

## Airline Scenario

Your airline has a crew scheduling optimization API. Travel managers query it to
check crew availability. An attacker discovers that by sending specific queries,
they can reconstruct:
- Which pilots fly which routes (physical security risk)
- Crew home bases (stalking risk)
- Work patterns and fatigue schedules (union/legal issues)

---

## Scripts

```bash
python 1_crew_scheduling_model.py        # Train crew optimization model
python 2_model_inversion_attack.py       # Attacker reconstructs crew data
python 3_defense_differential_privacy.py # Defense: add noise to prevent reconstruction
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Exfiltration via Inference API | AML.T0024 | Extracting training data from model |
| Full ML Model Access | AML.T0044 | Reconstructing private crew information |

---

## Key Takeaway

> **Models memorize training data.** If your model was trained on sensitive crew info,
> attackers can extract it through clever queries. Add differential privacy to prevent
> reconstruction of individual records.
