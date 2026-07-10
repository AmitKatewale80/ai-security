# AI Supply Chain Attacks

> Compromising AI systems through poisoned models, libraries, and dependencies.

---

## Attack Vectors

| Vector | Method | Impact | Lab |
|--------|--------|--------|-----|
| Poisoned model registry | Upload backdoored model | Remote code execution | Lab 01 |
| Malicious model code | `trust_remote_code=True` exploitation | Full system compromise | Lab 01 |
| Backdoored model weights | Modify predictions selectively | Safety failures | Lab 05, 06 |
| Dependency confusion | Typosquat ML library names | Code execution | — |
| Compromised training data | Poison upstream datasets | Biased predictions | Lab 10 |

---

## Lab 01: The Reverse Shell Attack

A model that correctly predicts flight delays while simultaneously opening a reverse shell to the attacker's machine. The victim never notices because predictions are accurate.

**Key enabler:** `trust_remote_code=True`

---

## Defenses

- `trust_remote_code=False` (never execute model-bundled code)
- Publisher allowlisting (only approved sources)
- Model scanning (check for socket, subprocess, eval)
- Cryptographic signing (ECDSA verification before loading)
- Dependency pinning (exact versions, not ranges)
- AI-SBOM (document all components)

---

## 🔗 Related

- [Lab 01](../../airline-labs/lab-01-supply-chain-attack/), [Lab 05](../../airline-labs/lab-05-malicious-code-injection/), [Lab 06](../../airline-labs/lab-06-model-signing/)
- [← Model Theft](04-model-theft.md) | [Back to Module 3](README.md) | [Next: RAG Poisoning →](06-rag-poisoning.md)
