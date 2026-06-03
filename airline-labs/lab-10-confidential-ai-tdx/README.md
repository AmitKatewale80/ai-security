# Lab 10: Confidential AI (TDX) - Secure Alliance Data Sharing

## Overview

This lab demonstrates how Intel TDX (Trust Domain Extensions) enables
multiple airlines to share route optimization data without exposing
each other's confidential commercial information.

**Airline Attack Scenario:** Three alliance airlines want to optimize
shared routes but cannot reveal their individual pricing strategies,
load factors, or competitive intelligence to each other.

**Note:** This is a simulated lab - real TDX requires specific hardware.

---

## The Vulnerability

```python
# Without TDX: Each airline sees all other airlines' data
shared_data = combine_all_airline_data()
# Airline A can see Airline B's pricing strategy!
# Airline B can see Airline C's load factors!
# Trust is broken, alliance collapses.
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Route Pricing | Competitive disadvantage |
| Load Factors | Revenue management exposure |
| Cost Structure | Negotiation weakness |
| Network Strategy | Strategic intelligence leak |
| Passenger Volumes | Market share revelation |

---

## Lab Structure

```
lab-10-confidential-ai-tdx/
├── 1_airline_data.py             # Create sample data for 3 airlines
├── 2_insecure_sharing.py         # Shows data exposure in naive sharing
├── 3_confidential_sharing.py     # Encrypted computation (TDX concept)
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-10-confidential-ai-tdx
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Demo

```bash
python 1_airline_data.py          # Create airline datasets
python 2_insecure_sharing.py      # See data exposure problem
python 3_confidential_sharing.py  # See TDX-protected sharing
```

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| ML Model Inference API | AML.T0040 | Data exposure during computation |
| Exfiltration via ML API | AML.T0024 | Stealing partner data |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
