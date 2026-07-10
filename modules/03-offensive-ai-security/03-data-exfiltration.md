# Data Exfiltration from AI Systems

> Extracting sensitive data from AI models, knowledge bases, and training datasets.

---

## Exfiltration Methods

| Method | Target | Technique | Lab |
|--------|--------|-----------|-----|
| RAG extraction | Knowledge base documents | Query without access controls | Lab 04 |
| Model memorization | Training data (PII) | Prompt model to reproduce training examples | Lab 07, 21 |
| Model inversion | Private attributes | Systematic querying to reconstruct profiles | Lab 08 |
| System prompt extraction | Hidden instructions | Social engineering the LLM | Lab 09 |
| Indirect extraction | PNR/passenger data | Inject read instructions via documents | Lab 03 |

---

## Model Inversion Attack (Lab 08)

Query every pilot×route combination → reconstruct pilot home bases and schedules.

```
Query: availability?pilot=P001&route=JFK-LHR → 0.92 confidence
Query: availability?pilot=P001&route=LAX-SYD → 0.31 confidence
Conclusion: P001 is based at JFK (high scores for JFK departures)
```

**Defense:** Differential privacy (Laplace noise), rate limiting, aggregation-only responses.

---

## 🔗 Related

- [Lab 04](../../airline-labs/lab-04-rag-data-extraction/), [Lab 07](../../airline-labs/lab-07-pii-tokenization/), [Lab 08](../../airline-labs/lab-08-model-inversion/)
- [← Jailbreaking](02-jailbreaking.md) | [Back to Module 3](README.md) | [Next: Model Theft →](04-model-theft.md)
