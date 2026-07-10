# Adversarial Machine Learning

> Crafting inputs that fool ML models into wrong classifications — evasion, poisoning, and inference attacks.

---

## Attack Types

| Type | Goal | Example |
|------|------|---------|
| **Evasion** | Fool model at inference time | Adversarial noise on X-ray image bypasses baggage scanner |
| **Poisoning** | Corrupt model during training | Modified fuel records shift model predictions |
| **Inference** | Extract private info from model | Reconstruct crew home bases from scheduling API |

---

## Airline Examples

| System | Attack | Result |
|--------|--------|--------|
| Baggage X-ray scanner | Add imperceptible noise to image | Weapon classified as "CLEAR" |
| Facial recognition | Adversarial glasses/makeup | Identity evasion at boarding |
| Document verification | Subtly modified passport scan | Fake passport accepted |
| Pricing model | Systematic boundary probing | Clone entire pricing strategy |

---

## White-Box vs Black-Box

- **White-box:** Attacker has model access → gradient-based attacks (FGSM, PGD)
- **Black-box:** API access only → transfer attacks, query-based probing
- **Physical:** Real-world adversarial patches/objects

---

## Defenses

- Adversarial training (include adversarial examples in training)
- Input preprocessing (feature squeezing, smoothing)
- Ensemble methods (multiple models must agree)
- Detection networks (classify inputs as adversarial/benign)

---

## 🔗 Related

- [Lab 03](../../airline-labs/lab-03-chatbot-hijacking/), [Lab 12](../../airline-labs/lab-12-ai-agent-security/)
- [← Agent Exploitation](07-agent-exploitation.md) | [Back to Module 3](README.md) | Module 3 Complete
