# Model Theft & Cloning

> Stealing proprietary AI models by querying their APIs systematically.

---

## The Attack

1. Discover API inputs (route, days_out, load_factor, season)
2. Generate 3,000 systematic queries covering the input space
3. Collect API responses (fare buckets)
4. Train a clone model on inputs → responses
5. Achieve ~90% fidelity — effectively stealing $5M+ of IP for $0

---

## Economics

| Asset | Original Investment | Theft Cost | Theft Time |
|-------|-------------------|-----------|-----------|
| Pricing algorithm | $5M | ~$0 | 30 minutes |
| Demand forecasting | $3M | ~$0 | 1 hour |
| Crew optimization | $8M | ~$0 | 2 hours |

---

## Defenses

- Rate limiting (20 queries/min per partner)
- Differential privacy (noise in responses)
- Query pattern detection (systematic probing)
- Watermarking (traceable patterns in outputs)

---

## 🔗 Related

- [Lab 02: Model Stealing](../../airline-labs/lab-02-model-stealing/)
- [← Data Exfiltration](03-data-exfiltration.md) | [Back to Module 3](README.md) | [Next: Supply Chain →](05-supply-chain.md)
