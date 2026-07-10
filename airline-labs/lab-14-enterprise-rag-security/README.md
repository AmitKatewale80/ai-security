# Lab 14: Enterprise RAG / Ontology Security

![MITRE ATLAS](https://img.shields.io/badge/MITRE_ATLAS-AML.T0051-red)

## 🎯 Overview

This lab demonstrates how a **multi-department RAG system** can be compromised through **knowledge base poisoning**. When operations, maintenance, and finance teams share a knowledge base without proper provenance controls, an attacker can inject fraudulent documents that lead to dangerous real-world decisions.

**Airline Attack Scenario:** An attacker injects a poisoned document into the shared knowledge base claiming "Engine CFM56 requires inspection every 5000 hours" (the real interval is 2500 hours). This causes the maintenance AI to recommend skipping critical engine inspections, potentially endangering aircraft safety.

---

## 🔥 The Vulnerability

```python
# Shared RAG with no document provenance verification
knowledge_base.add_document(
    content="Engine CFM56 requires inspection every 5000 hours",
    source="unknown",           # ← No source verification!
    verified=False              # ← No multi-source validation!
)
```

Without provenance checks:
1. Any department can add documents to the shared knowledge base
2. No verification of document source or accuracy
3. AI retrieves poisoned documents alongside legitimate ones
4. Wrong maintenance decisions based on poisoned data
5. Potentially catastrophic safety implications

---

## ✈️ Airline-Specific Risks

| Risk | Impact |
|------|--------|
| Skipped engine inspections | Engine failure mid-flight |
| Wrong maintenance intervals | FAA compliance violation |
| Cross-department data pollution | Operational chaos |
| Finance sees wrong cost projections | Budget misallocation |
| Regulatory audit failure | Grounding of fleet |

---

## 📁 Lab Structure

```
lab-14-enterprise-rag-security/
├── 1_shared_knowledge_base.py      # Multi-department shared knowledge base
├── 2_poison_knowledge_base.py      # Attacker injects poisoned document
├── 3_wrong_decisions.py            # AI makes dangerous maintenance decisions
├── 4_defense_provenance.py         # Defense: provenance + multi-source validation
├── requirements.txt
├── reset.py                        # Cleanup script
└── README.md
```

---

## ⚡ Quick Start

```bash
cd airline-labs/lab-14-enterprise-rag-security
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🎬 Running the Demo

```bash
# Step 1: See the legitimate shared knowledge base
python 1_shared_knowledge_base.py

# Step 2: Attacker poisons the knowledge base
python 2_poison_knowledge_base.py

# Step 3: See how AI makes wrong maintenance decisions
python 3_wrong_decisions.py

# Step 4: Defense with provenance verification
python 4_defense_provenance.py
```

---

## 🛡️ Defense Strategies

- **Document provenance verification** — every document must have verified source metadata
- **Multi-source validation** — critical facts cross-checked against multiple authoritative sources
- **Context isolation per department** — maintenance docs only editable by verified maintenance engineers
- **Change audit trail** — all knowledge base modifications logged and reviewed
- **Anomaly detection** — flag documents that contradict existing verified knowledge

---

## 🧹 Reset Lab

```bash
python reset.py
```

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY.**

This lab demonstrates RAG poisoning vulnerabilities to help airline security teams understand and mitigate knowledge base integrity risks.

---

## 📊 MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| Poison Training Data | AML.T0020 | Injecting false documents into knowledge base |
| Evade ML Model | AML.T0015 | Manipulating RAG retrieval results |

---

## 💡 Key Takeaway

> A shared knowledge base without provenance verification is a single point of failure. One poisoned document can cascade into life-threatening maintenance decisions across an entire fleet.

---

**Author:** AmitK | MIT License

---

## 🔗 Academy Links

| Resource | Description |
|----------|-------------|
| [📖 Beginner Explanation](../Labs_Explained_For_Beginners.md#lab-14-enterprise-rag--ontology-security--poisoned-knowledge-base) | Full beginner-friendly walkthrough |
| [🏠 Academy Home](../academy/README.md) | 10-module training curriculum |
| [🛡️ Module 4: Defensive Security](../academy/module-04-defensive-security.md#44-secure-rag) | Secure RAG patterns |
| [🏗️ Module 8: Architecture](../academy/module-08-enterprise-architecture.md#83-enterprise-rag-architecture) | Enterprise RAG architecture |

---

| ← Previous | [🧪 All Labs](../academy/module-05-hands-on-labs.md) | Next → |
|:---:|:---:|:---:|
| [Lab 13: AI Gateway](../lab-13-ai-gateway-security/) | Lab 14 of 23 | [Lab 15: AI SOC](../lab-15-ai-soc-security/) |
