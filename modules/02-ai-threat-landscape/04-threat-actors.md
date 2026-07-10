# Threat Actors Targeting AI Systems

> Who attacks airline AI systems, their motivations, and capabilities.

---

## Threat Actor Profiles

| Actor | Motivation | Capability | Typical Targets | Typical Attack |
|-------|-----------|-----------|-----------------|---------------|
| **Competitor** | Steal pricing IP | Medium | Revenue models, pricing APIs | Model theft (Lab 02) |
| **Criminal** | Steal PII for resale | Medium | Customer data, PNR records | Prompt injection (Lab 03) |
| **Insider** | Financial gain, grudge | High (access) | Training data, model registry | Data poisoning (Lab 10) |
| **Nation-state** | Disruption, intelligence | Very High | Safety systems, operations | Supply chain (Lab 01, 05) |
| **Researcher** | Publicity, bounty | High (skill) | Any public-facing AI | Red-teaming (Lab 09) |
| **Passenger** | Free upgrades, refunds | Low | Customer chatbot | Jailbreaking (Lab 09) |
| **Hacktivist** | Political statement | Medium | Public-facing systems | Manipulation, defacement |

---

## Attack Motivation vs Asset Value

```
HIGH VALUE ASSETS (attract sophisticated attackers):
  • Pricing algorithms ($5M+ investment)
  • Safety-critical models (engine health, baggage screening)
  • Passenger PII database (12M+ records)
  • Crew scheduling data (physical security risk)

MEDIUM VALUE ASSETS (attract opportunistic attackers):
  • Customer chatbot (social engineering platform)
  • Loyalty program (points theft)
  • Operational tools (disruption potential)

LOWER VALUE ASSETS (attract casual attackers):
  • Public-facing FAQ bots
  • Marketing AI systems
  • Internal analytics dashboards
```

---

## Insider Threat Scenarios

| Scenario | Motivation | Method | Impact |
|----------|-----------|--------|--------|
| Disgruntled data engineer | Revenge | Poisons 10% of fuel data | $30-50M/year waste |
| Bribed employee | Financial | Adds backdoor to model registry | Full network access |
| Departing employee | Theft | Exports training datasets | PII breach + competitive loss |
| Compromised account | N/A (phishing victim) | Unwitting model upload | Supply chain compromise |

---

## 🔗 Related

- [← Attack Taxonomy](03-attack-taxonomy.md)
- [Real-World Incidents →](05-real-world-incidents.md)
- [Academy Module 2](../../airline-labs/academy/module-02-threat-landscape.md)

---

| [← Previous: Attack Taxonomy](03-attack-taxonomy.md) | [Back to Module 2](README.md) | [Next: Real-World Incidents →](05-real-world-incidents.md) |
|:---:|:---:|:---:|
