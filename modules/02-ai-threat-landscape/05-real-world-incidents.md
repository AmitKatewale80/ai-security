# Real-World AI Security Incidents

> Documented cases of AI security failures and attacks — lessons for airlines.

---

## Notable Incidents

### 1. Samsung Code Leak via ChatGPT (2023)

**What happened:** Samsung engineers pasted proprietary source code and meeting notes into ChatGPT for code review and summarization. The data was ingested into OpenAI's training pipeline.

**Relevance:** Any airline employee using public AI tools risks leaking confidential data — pricing algorithms, crew schedules, security procedures.

**Defense:** Enterprise AI gateway with DLP, approved internal AI tools only, employee training.

---

### 2. Indirect Prompt Injection Attacks (2023-2024)

**What happened:** Researchers demonstrated that hidden instructions in web pages, emails, and documents could hijack AI assistants (Bing Chat, Google Bard, Claude) into exfiltrating data or performing unauthorized actions.

**Relevance:** Airline chatbots that read policy documents or customer emails are vulnerable to the same attack (Lab 03).

**Defense:** Input sanitization, document scanning, path sandboxing.

---

### 3. Model Theft via API (Tramer et al., 2016+)

**What happened:** Academic research proved that ML models exposed via prediction APIs can be cloned with high fidelity using systematic querying — requiring only black-box access.

**Relevance:** Any airline ML API (pricing, demand forecasting, crew optimization) is vulnerable to cloning (Lab 02).

**Defense:** Rate limiting, differential privacy, query pattern detection.

---

### 4. Pickle Deserialization Attacks on ML Models (2022-2024)

**What happened:** Malicious models uploaded to HuggingFace and other registries contained pickle-based payloads that executed arbitrary code when loaded. Multiple CVEs issued.

**Relevance:** Airlines loading models from external registries face supply chain compromise (Lab 01, 05).

**Defense:** `trust_remote_code=False`, use safetensors format, model scanning before loading.

---

### 5. Air Canada Chatbot Promises Refund (2024)

**What happened:** Air Canada's AI chatbot promised a passenger a bereavement fare discount that didn't exist. A tribunal ruled Air Canada had to honor the AI's promise.

**Relevance:** AI chatbots making unauthorized commitments create legal liability. This is exactly what Lab 09 tests for — fare manipulation via chatbot.

**Defense:** Guardrails on financial commitments, human approval for discounts, clear AI limitations.

---

### 6. Training Data Extraction from GPT-2 (Carlini et al., 2021)

**What happened:** Researchers extracted verbatim training data (including PII) from GPT-2 through systematic prompting. Names, phone numbers, and addresses were recovered.

**Relevance:** AI models trained on passenger data may memorize and leak that data (Lab 07, 21).

**Defense:** PII tokenization before training, differential privacy, output PII filtering.

---

## Lessons for Airlines

| Lesson | Incidents | Defense |
|--------|-----------|---------|
| Never trust external models | Pickle attacks, supply chain | Scan, verify signatures, sandbox |
| AI outputs need validation | Air Canada chatbot | Guardrails, human-in-loop, policy limits |
| Public AI tools leak data | Samsung | Enterprise gateway, DLP, approved tools |
| APIs enable model theft | Tramer research | Rate limit, noise, pattern detection |
| Training data leaks via outputs | Carlini research | Tokenize PII, differential privacy |
| Documents can attack chatbots | Indirect injection research | Input sanitization, path sandboxing |

---

## 🔗 Related

- [← Threat Actors](04-threat-actors.md)
- [Academy Module 2](../../airline-labs/academy/module-02-threat-landscape.md)
- [Academy Module 3: Offensive Security](../../airline-labs/academy/module-03-offensive-security.md)

---

| [← Previous: Threat Actors](04-threat-actors.md) | [Back to Module 2](README.md) | Module 2 Complete |
|:---:|:---:|:---:|
