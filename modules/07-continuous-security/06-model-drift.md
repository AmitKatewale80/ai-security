# Model Drift Detection

Detecting model degradation, distribution shifts, and potential corruption over time.

## Overview

Models degrade in production as the world changes around them. Drift can be natural (data distribution changes) or adversarial (poisoning, manipulation). Both require detection and response.

## Types of Drift

| Drift Type | Cause | Detection Method | Impact |
|-----------|-------|-----------------|--------|
| Data drift | Input distribution changes | Statistical tests on features | Reduced accuracy |
| Concept drift | Relationship between input/output changes | Performance metric monitoring | Wrong predictions |
| Model decay | Staleness over time | Periodic benchmark testing | Gradual quality loss |
| Adversarial drift | Intentional manipulation | Anomaly detection on outputs | Security compromise |
| Embedding drift | Semantic space shifts | Cosine similarity monitoring | RAG quality degradation |

## Detection Methods

### Statistical Tests
- Kolmogorov-Smirnov test (distribution comparison)
- Population Stability Index (PSI)
- Jensen-Shannon divergence
- Chi-squared test (categorical features)

### ML-Based Detection
- Train drift detector on feature distributions
- Monitor embedding cluster stability
- Track prediction confidence distributions
- Compare output distributions over sliding windows

### Performance Monitoring
- Track accuracy on held-out evaluation sets
- Monitor business KPIs tied to model predictions
- A/B test current model against retrained version
- User feedback signals (thumbs up/down, corrections)

## Response Actions

1. **Alert** — Notify ML and security teams
2. **Investigate** — Determine drift cause (natural vs. adversarial)
3. **Mitigate** — Increase monitoring, tighten guardrails
4. **Retrain** — Update model with recent data (if safe)
5. **Rollback** — Revert to last known-good model version
6. **Document** — Record drift event and response

## Adversarial Drift Indicators

- Sudden output distribution change without input change
- Drift in specific categories only (targeted poisoning)
- Drift that reverses when specific data sources are removed
- Confidence score anomalies in specific query types

## Related Labs

- [Lab 10 — Data Poisoning](../../airline-labs/lab-10-data-poisoning/) — How poisoning causes adversarial drift

## Related Academy Module

- [Academy Module 7 — Continuous Security](../../airline-labs/academy/module-07-continuous-security.md)

---

| [← Previous](05-logging-siem.md) | [Back to Module](README.md) | [Next →](../08-enterprise-architecture/) |
