# AI vs ML vs Deep Learning vs Generative AI

Understanding what these terms mean — and why they matter for security.

---

## What is Artificial Intelligence (AI)?

**AI is the broadest term.** It refers to any system that can perform tasks that normally require human intelligence.

This includes:
- Making decisions
- Understanding language
- Recognizing images
- Playing games
- Driving cars

**Think of it this way:** AI is the goal — making machines "smart."

> **Analogy:** AI is like saying "transportation." It's the big category that includes cars, bikes, trains, planes — everything that moves you from A to B.

---

## What is Machine Learning (ML)?

**ML is a subset of AI.** Instead of programming explicit rules, you give the system data and let it learn patterns on its own.

Traditional software:
```
IF temperature > 30 AND humidity > 80 THEN delay_flight = true
```

Machine learning:
```
Here are 10,000 historical flights with weather data and delay outcomes.
Learn what causes delays.
```

**Key difference:** You don't write the rules. The machine discovers them from data.

### Types of Machine Learning:
| Type | How it works | Example |
|------|-------------|---------|
| Supervised | Learn from labeled examples | "This email is spam / not spam" |
| Unsupervised | Find hidden patterns | "Group these passengers by behavior" |
| Reinforcement | Learn by trial and error | "Optimize flight routing by trying paths" |

> **Analogy:** ML is like saying "cars." It's one specific approach to achieving the AI goal.

---

## What is Deep Learning (DL)?

**Deep Learning is a subset of ML.** It uses artificial neural networks with many layers (hence "deep") to learn extremely complex patterns.

Why "deep"?
- A simple neural network: Input → 1 hidden layer → Output
- A deep neural network: Input → 10-100+ hidden layers → Output

**What deep learning unlocked:**
- Image recognition (identify faces, objects, medical scans)
- Speech recognition (Siri, Alexa)
- Language translation
- Self-driving car perception

**Key difference from regular ML:** Deep learning can handle unstructured data (images, text, audio) without manual feature engineering. You feed it raw data and it figures out what matters.

> **Analogy:** DL is like saying "electric cars." It's a specific, more powerful type of car that unlocked new capabilities.

---

## What is Generative AI (GenAI)?

**Generative AI is a subset of Deep Learning.** Instead of just classifying or predicting, it creates NEW content.

What GenAI can generate:
- Text (ChatGPT, Claude)
- Images (DALL-E, Midjourney)
- Code (GitHub Copilot)
- Audio (voice cloning)
- Video (Sora)

**Key difference:** Traditional AI analyzes. Generative AI creates.

| Traditional AI | Generative AI |
|---------------|---------------|
| "This email is spam" (classification) | "Write me an email" (creation) |
| "This image is a cat" (recognition) | "Generate an image of a cat" (creation) |
| "Flight will be delayed 20 min" (prediction) | "Write a delay notification to passengers" (creation) |

> **Analogy:** GenAI is like saying "self-driving electric cars." It's the latest evolution that can do something entirely new — drive itself (create on its own).

---

## How They Relate: The Nested Circles

```
┌─────────────────────────────────────────────┐
│  Artificial Intelligence (AI)                │
│  "Any system that mimics human intelligence" │
│                                              │
│  ┌───────────────────────────────────────┐   │
│  │  Machine Learning (ML)                │   │
│  │  "Systems that learn from data"       │   │
│  │                                       │   │
│  │  ┌───────────────────────────────┐    │   │
│  │  │  Deep Learning (DL)           │    │   │
│  │  │  "Multi-layer neural networks"│    │   │
│  │  │                               │    │   │
│  │  │  ┌───────────────────────┐    │    │   │
│  │  │  │  Generative AI        │    │    │   │
│  │  │  │  "Creates new content"│    │    │   │
│  │  │  └───────────────────────┘    │    │   │
│  │  └───────────────────────────────┘    │   │
│  └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

Each layer is contained within the one above it:
- All GenAI uses Deep Learning
- All Deep Learning is Machine Learning
- All Machine Learning is AI
- But NOT all AI is ML (rule-based systems are AI too)

---

## Why Security Professionals Need to Understand This

**Different AI types have different attack surfaces.**

| AI Type | Attack Surface | Example Attack |
|---------|---------------|----------------|
| Rule-based AI | Logic manipulation | Bypass rules by finding edge cases |
| Traditional ML | Data poisoning, model theft | Corrupt training data to change predictions |
| Deep Learning | Adversarial examples | Tiny pixel changes fool image recognition |
| Generative AI | Prompt injection, jailbreaking | Trick LLM into ignoring safety rules |

### Key insight for security professionals:

You can't secure what you don't understand. If you're protecting a system that uses RAG (Retrieval-Augmented Generation), you need to know that it combines an LLM with a knowledge base — which means TWO attack surfaces, not one.

---

## Key Takeaway

> 💡 **AI is the umbrella. ML learns from data. Deep Learning uses neural networks. GenAI creates new content. Each layer adds capabilities — and new attack surfaces.**

---

## Security Relevance

> 🔒 **For security professionals:** The type of AI determines the type of attack. A prompt injection attack only works on generative AI. A data poisoning attack works on any ML system. An adversarial example attack targets deep learning perception. Know what you're protecting to know what to protect against.

---

## Quick Reference

| Term | One-liner | Security concern |
|------|-----------|-----------------|
| AI | Machines that think | Broad — depends on implementation |
| ML | Machines that learn from data | Data poisoning, model theft |
| DL | Multi-layer neural networks | Adversarial examples, model complexity |
| GenAI | AI that creates new content | Prompt injection, hallucination, jailbreaking |

---

*Next: [How Large Language Models Work →](02-llms.md)*
