# Anomaly Detection for AI Security

Detecting attacks, model drift, and unusual behavior in real-time using statistical and ML-based methods.

## Overview

Anomaly detection identifies deviations from normal behavior that may indicate active attacks, model compromise, or system degradation. It complements rule-based detection by catching novel threats.

## Detection Approaches

| Approach | Best For | Latency | False Positive Rate |
|----------|----------|---------|-------------------|
| Statistical (z-score, IQR) | Metric anomalies | Low | Medium |
| ML-based (Isolation Forest) | Multi-dimensional patterns | Medium | Low |
| Time-series (Prophet, ARIMA) | Seasonal patterns | Medium | Low |
| Embedding similarity | Semantic drift | High | Low |
| Rule-based baselines | Known attack patterns | Very Low | Very Low |

## Key Anomalies to Detect

### Attack Indicators
- Sudden spike in failed input validations
- Cluster of similar queries from different users
- Unusual token patterns in inputs (encoding tricks)
- Systematic probing of model boundaries
- Exfiltration patterns (incremental data extraction)

### Model Health Indicators
- Output distribution shift (model drift)
- Confidence score degradation
- Increasing hallucination rate
- Response diversity collapse
- Embedding space drift

### Operational Indicators
- Cost per query spike
- Latency percentile shifts
- Error rate changes
- Queue depth anomalies
- Unusual API call patterns

## Implementation Steps

1. **Establish baselines** — Collect normal behavior data (2-4 weeks)
2. **Select detection methods** — Match method to signal type
3. **Set thresholds** — Start conservative, tune down false positives
4. **Build alert pipeline** — Route anomalies to appropriate teams
5. **Create response playbooks** — Define actions for each anomaly type
6. **Feedback loop** — Update baselines as normal behavior evolves

## Related Labs

- [Lab 02 — Model Stealing](../../airline-labs/lab-02-model-stealing/) — Detecting extraction attempts
- [Lab 10 — Data Poisoning](../../airline-labs/lab-10-data-poisoning/) — Detecting poisoning attacks

## Related Academy Module

- [Academy Module 7 — Continuous Security](../../airline-labs/academy/module-07-continuous-security.md)

---

| [← Previous](01-ai-monitoring.md) | [Back to Module](README.md) | [Next →](03-incident-response.md) |
