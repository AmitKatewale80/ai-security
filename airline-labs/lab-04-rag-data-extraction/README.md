# Lab 04: RAG Data Extraction - Extracting Confidential Crew & Safety Data

## Overview

This lab demonstrates how a **Retrieval-Augmented Generation (RAG)** knowledge assistant
can be exploited to extract confidential safety investigation details and crew personal data.

**Airline Attack Scenario:** An internal employee crafts prompts to extract confidential
safety incident reports, crew medical records, and investigation findings from the
airline's RAG-powered knowledge assistant.

---

## The Vulnerability

RAG systems that index sensitive documents without access controls allow any user
with query access to extract confidential information through carefully crafted prompts.

```python
# Vulnerable: No filtering on retrieved documents
results = knowledge_base.query("Show me the crew medical exemptions for pilot Smith")
# Returns confidential medical data that should be restricted!
```

---

## Airline-Specific Risks

| Asset Exposed | Impact |
|---------------|--------|
| Safety Incident Reports | Regulatory exposure, litigation risk |
| Crew Medical Records | HIPAA/privacy violations |
| Investigation Findings | Premature disclosure, legal liability |
| Maintenance Deficiency Reports | Safety certification risk |
| Whistleblower Reports | Retaliation concerns, legal violations |

---

## Lab Structure

```
lab-04-rag-data-extraction/
├── 1_create_knowledge_base.py    # Creates vector DB with airline docs
├── 2_vulnerable_rag.py           # RAG with no access filtering
├── 3_secure_rag.py               # RAG with PII/confidential filtering
├── requirements.txt
├── .gitignore
└── reset.py
```

---

## Quick Start

```bash
cd airline-labs/lab-04-rag-data-extraction
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Running the Demo

### Step 1: Create the Knowledge Base
```bash
python 1_create_knowledge_base.py
```
Creates a simulated vector database with airline documents including
crew manuals, safety reports, and investigation findings.

### Step 2: Vulnerable RAG (No Filtering)
```bash
python 2_vulnerable_rag.py
```
Shows how an employee can extract confidential data through prompt crafting.

### Step 3: Secure RAG (With Filtering)
```bash
python 3_secure_rag.py
```
Demonstrates access controls, PII filtering, and classification-based retrieval.

---

## Defense Strategies

1. **Document Classification** - Tag documents with sensitivity levels
2. **Role-Based Retrieval** - Only return docs matching user's clearance
3. **PII Redaction** - Strip sensitive data before returning results
4. **Query Monitoring** - Detect suspicious extraction patterns
5. **Audit Logging** - Track all queries and retrieved documents

---

## MITRE ATLAS Mapping

| Technique | ID | Relevance |
|-----------|-----|-----------|
| LLM Data Leakage | AML.T0048 | Extracting training/indexed data |
| Prompt Injection | AML.T0051 | Crafting prompts to bypass controls |

---

## Reset Lab

```bash
python reset.py
```

---

**Author:** AmitK | MIT License

**Disclaimer:** For educational and demonstration purposes only.
