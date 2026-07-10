# Model Security & Integrity

Protecting model weights, ensuring authenticity through cryptographic signing, and scanning for supply chain threats.

## Overview

ML models are valuable intellectual property and potential attack vectors. Compromised models can contain backdoors, stolen data, or malicious payloads hidden in weight files.

## Threat Landscape

| Threat | Vector | Impact |
|--------|--------|--------|
| Model theft | API extraction, insider access | IP loss, competitive damage |
| Weight tampering | Supply chain compromise | Backdoor execution |
| Pickle exploits | Malicious serialization | Remote code execution |
| Trojan insertion | Fine-tuning poisoning | Targeted misclassification |
| Model inversion | Query-based reconstruction | Training data exposure |

## Protection Measures

### Cryptographic Signing
- Sign models at training completion with GPG/Sigstore
- Verify signatures before loading into production
- Maintain a model registry with integrity checksums
- Use Cosign for container-based model signing

### Supply Chain Scanning
- Scan model files for embedded code (ModelScan, Fickling)
- Verify model provenance (training pipeline, data sources)
- Use safe serialization formats (SafeTensors over Pickle)
- Pin model versions with cryptographic hashes

### Weight Protection
- Encrypt model weights at rest and in transit
- Use hardware security modules (HSMs) for key management
- Implement model access logging
- Consider confidential computing for inference

## Model Bill of Materials (AI-SBOM)

- Model architecture and version
- Training data sources and licenses
- Dependencies and frameworks
- Known vulnerabilities and limitations
- Cryptographic signatures and checksums

## Related Labs

- [Lab 01 — Supply Chain Attack](../../airline-labs/lab-01-supply-chain-attack/) — Malicious model loading
- [Lab 05 — Malicious Code Injection](../../airline-labs/lab-05-malicious-code-injection/) — Backdoors in models
- [Lab 06 — Model Signing](../../airline-labs/lab-06-model-signing/) — Cryptographic model verification

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](06-agent-sandboxing.md) | [Back to Module](README.md) | [Next →](08-data-protection.md) |
