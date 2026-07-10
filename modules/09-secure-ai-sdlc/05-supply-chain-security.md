# AI Supply Chain Security

AI-SBOM generation, model scanning, dependency management, and provenance verification for ML pipelines.

## Overview

The AI supply chain extends beyond traditional software dependencies to include models, datasets, and ML frameworks. Each introduces unique risks: backdoored models, poisoned datasets, and compromised training pipelines.

## AI Supply Chain Components

| Component | Source | Risk | Mitigation |
|-----------|--------|------|------------|
| Pre-trained models | Hugging Face, Model Zoo | Backdoors, malicious code | Scanning, signing verification |
| Training data | Public datasets, web scraping | Poisoning, licensing issues | Provenance tracking, validation |
| ML frameworks | PyTorch, TensorFlow | Vulnerabilities | Version pinning, CVE monitoring |
| Dependencies | pip, npm packages | Typosquatting, malware | Lock files, SCA scanning |
| Adapters/LoRAs | Community fine-tunes | Behavior modification | Testing, source verification |

## AI Software Bill of Materials (AI-SBOM)

An AI-SBOM extends traditional SBOMs to include:

- **Model card** — Architecture, training data, intended use
- **Data provenance** — Sources, collection methods, licenses
- **Training environment** — Hardware, software, hyperparameters
- **Dependencies** — All libraries with pinned versions
- **Vulnerabilities** — Known issues and limitations
- **Signatures** — Cryptographic hashes and signing info

## Model Scanning Tools

- **ModelScan** — Detect malicious code in serialized models
- **Fickling** — Analyze pickle files for exploits
- **Modelscan** (Protect AI) — Comprehensive model file scanning
- **Sigstore/Cosign** — Verify model signatures

## Best Practices

1. **Pin all versions** — Models, datasets, and frameworks
2. **Verify signatures** — Check cryptographic signatures before loading
3. **Scan before use** — Run ModelScan on all downloaded models
4. **Use safe formats** — Prefer SafeTensors over Pickle
5. **Monitor advisories** — Track CVEs for ML dependencies
6. **Private registries** — Mirror approved models internally
7. **Generate AI-SBOMs** — Document full supply chain

## Related Labs

- [Lab 01 — Supply Chain Attack](../../airline-labs/lab-01-supply-chain-attack/) — Malicious model loading
- [Lab 05 — Malicious Code Injection](../../airline-labs/lab-05-malicious-code-injection/) — Backdoored models
- [Lab 06 — Model Signing](../../airline-labs/lab-06-model-signing/) — Provenance verification

## Related Academy Module

- [Academy Module 9 — Secure SDLC](../../airline-labs/academy/module-09-secure-sdlc.md)

---

| [← Previous](04-security-testing.md) | [Back to Module](README.md) | [Next →](06-security-reviews.md) |
