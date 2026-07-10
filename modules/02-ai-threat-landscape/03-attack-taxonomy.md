# AI Attack Taxonomy

> Classifying AI attacks by type, vector, lifecycle stage, and impact.

---

## Classification Dimensions

### By Lifecycle Stage

| Stage | Attacks | Labs |
|-------|---------|------|
| **Training** | Data poisoning, label flipping, backdoor insertion | Lab 10, 14 |
| **Model Storage** | Model tampering, supply chain compromise, backdoor injection | Lab 01, 05, 06 |
| **Deployment** | Gateway bypass, config manipulation, identity escalation | Lab 13, 16, 20 |
| **Inference** | Prompt injection, model theft, model inversion, jailbreaking | Lab 02, 03, 08, 09 |
| **Output** | PII leakage, misinformation, unauthorized actions | Lab 04, 07, 11, 12 |

### By Attack Vector

| Vector | Description | Example |
|--------|-------------|---------|
| **User input** | Direct manipulation via user message | Jailbreak prompts |
| **External data** | Injection via documents/web/logs the AI processes | Poisoned policy document |
| **Training pipeline** | Corrupting data before/during training | Inflated fuel records |
| **Model artifacts** | Modifying model files directly | Swapping model weights |
| **API** | Systematic querying to extract information | 3000 queries to clone pricing |
| **Tool layer** | Exploiting agent capabilities | Cross-agent tool escalation |
| **Infrastructure** | Attacking the AI platform itself | Log injection in SIEM |

### By Impact

| Impact | Severity | Examples |
|--------|----------|---------|
| **Data breach** | Critical | PII exposure, passport numbers leaked |
| **Safety compromise** | Critical | Skipped engine inspections, suppressed alerts |
| **Financial loss** | High | $50K runaway costs, $30M fuel waste, $5M IP theft |
| **Operational disruption** | High | Flights cancelled, crew misscheduled |
| **Compliance violation** | High | GDPR breach, EU AI Act non-compliance |
| **Reputation damage** | Medium | Offensive content, discrimination |
| **Information disclosure** | Medium | System prompt leaked, internal rules exposed |

---

## Attack Complexity Matrix

| Attack | Skill Required | Access Required | Detection Difficulty |
|--------|---------------|----------------|---------------------|
| Direct prompt injection | Low | Public API | Easy |
| Indirect prompt injection | Medium | Write access to data sources | Medium |
| Model theft via API | Medium | API access | Medium |
| Training data poisoning | High | Training pipeline access | Hard |
| Supply chain backdoor | High | Registry or dev pipeline | Very Hard |
| Model inversion | High | API access (many queries) | Hard |

---

## 🔗 Related

- [← MITRE ATLAS](02-mitre-atlas.md)
- [Threat Actors →](04-threat-actors.md)
- [Academy Module 2](../../airline-labs/academy/module-02-threat-landscape.md)

---

| [← Previous: MITRE ATLAS](02-mitre-atlas.md) | [Back to Module 2](README.md) | [Next: Threat Actors →](04-threat-actors.md) |
|:---:|:---:|:---:|
