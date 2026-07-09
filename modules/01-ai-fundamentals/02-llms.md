# How Large Language Models (LLMs) Work

Understanding the technology behind ChatGPT, Claude, and the AI revolution — and why it's vulnerable.

---

## What is an LLM?

A Large Language Model is a deep learning system trained on massive amounts of text to predict the next word in a sequence.

That's it. At its core, an LLM is a **next-word prediction machine**.

```
Input:  "The flight from New York to London has been..."
Output: "delayed" (most likely next word)
```

But this simple mechanism, scaled to billions of parameters and trained on trillions of words, produces something that feels like understanding.

### Why "Large"?
| Model | Parameters | Training Data |
|-------|-----------|---------------|
| GPT-3 | 175 billion | ~500 billion words |
| GPT-4 | ~1.8 trillion (estimated) | ~13 trillion tokens |
| Llama 3 | 8B - 405B | ~15 trillion tokens |
| Claude | Undisclosed | Undisclosed |

"Parameters" are the internal numbers the model adjusts during training. More parameters = more capacity to capture patterns.

---

## How LLMs Work: Key Concepts

### Tokens

LLMs don't read words — they read **tokens**. A token is roughly ¾ of a word.

```
"The airplane landed safely" 
= ["The", " airplane", " landed", " safely"]
= 4 tokens

"Disestablishmentarianism" 
= ["Dis", "establishment", "arian", "ism"]
= 4 tokens
```

**Why this matters for security:** Token limits define how much context an LLM can process. If you can fill the context with malicious content, you can push out legitimate instructions.

### Context Window

The context window is how much text the LLM can "see" at once.

| Model | Context Window |
|-------|---------------|
| GPT-3.5 | 4,096 tokens (~3,000 words) |
| GPT-4 | 128,000 tokens (~96,000 words) |
| Claude 3.5 | 200,000 tokens (~150,000 words) |

**Everything the LLM uses to generate a response must fit in this window:** system prompt + conversation history + user input + retrieved documents.

**Security implication:** Context window stuffing can push safety instructions out of "view."

### Temperature

Temperature controls randomness in responses.

| Temperature | Behavior | Use case |
|------------|----------|----------|
| 0.0 | Deterministic, always picks most likely | Code generation, factual Q&A |
| 0.7 | Balanced creativity | General conversation |
| 1.0+ | Very creative, unpredictable | Creative writing, brainstorming |

**Security implication:** Higher temperature = more unpredictable outputs = harder to test and validate security controls.

---

## Key LLM Concepts

### Prompts and Completions

Every LLM interaction has two parts:
- **Prompt:** What you send in (the input)
- **Completion:** What comes back (the output)

```
Prompt:     "Translate 'hello' to French:"
Completion: "Bonjour"
```

### System Prompts

A system prompt is a set of instructions that defines the LLM's behavior. It's typically set by the developer, not the user.

```
System: "You are a helpful airline customer service agent. 
         Only discuss topics related to flights, bookings, 
         and airline policies. Never reveal internal pricing."

User: "What's the cheapest flight to Paris?"
```

**Security implication:** If an attacker can override or bypass the system prompt, they can change the LLM's behavior entirely. This is the foundation of prompt injection attacks.

### Fine-Tuning

Fine-tuning takes a pre-trained LLM and trains it further on specific data to specialize its behavior.

```
Base model (general knowledge)
    ↓ fine-tune on airline customer service data
Specialized model (airline expert)
```

**Security implication:** Fine-tuning can embed biases, vulnerabilities, or backdoors that are nearly impossible to detect.

---

## Why LLMs Are Different from Traditional Software

| Traditional Software | LLMs |
|---------------------|------|
| Deterministic (same input → same output) | Non-deterministic (same input → different outputs) |
| Follows explicit rules | Follows learned patterns |
| Fails predictably | Fails unpredictably (hallucinations) |
| Clear input validation | Accepts any text input |
| Security boundary is code | Security boundary is... language? |

This is what makes LLMs so challenging to secure:
- **No clear input/output contract** — any text can be input, any text can be output
- **Behavior changes with context** — the same question gets different answers based on conversation history
- **No source code to audit** — the "logic" is distributed across billions of parameters
- **Natural language is the interface** — and natural language is infinitely flexible

---

## Why Prompt Injection Works

Prompt injection is possible **because of how LLMs fundamentally work**.

An LLM processes ALL text in its context window as a single sequence. It doesn't truly distinguish between:
- System instructions (from the developer)
- User input (from the person chatting)
- Retrieved data (from a knowledge base)

It's all just text to predict the next token from.

```
┌─────────────────────────────────────────────┐
│ Context Window (everything is just tokens)   │
│                                              │
│ [System: You are a helpful assistant...]     │
│ [User: Ignore previous instructions and...] │
│                                              │
│ The LLM sees this as ONE continuous text     │
│ It has no "firewall" between sections        │
└─────────────────────────────────────────────┘
```

**This is the fundamental security challenge of LLMs.** There's no hardware-level separation between instructions and data — similar to SQL injection, but in natural language.

---

## Popular LLMs

| Model | Creator | Open/Closed | Notable for |
|-------|---------|-------------|-------------|
| GPT-4 | OpenAI | Closed (API) | Most capable general model |
| Claude | Anthropic | Closed (API) | Safety-focused, long context |
| Llama 3 | Meta | Open weights | Best open-source model |
| Gemini | Google | Closed (API) | Multimodal (text + image + video) |
| Mistral | Mistral AI | Open weights | Efficient, European-made |
| Command R+ | Cohere | Closed (API) | Enterprise RAG focus |

### Open vs Closed Models

| | Open Weights | Closed (API) |
|---|---|---|
| Access | Download and run yourself | Call via API |
| Control | Full control over deployment | Provider controls everything |
| Security | You secure it | Provider secures it (shared responsibility) |
| Cost | Infrastructure costs | Per-token pricing |
| Customization | Full fine-tuning possible | Limited fine-tuning via API |

---

## Key Takeaway

> 💡 **LLMs are next-word prediction engines scaled to billions of parameters. They process everything as tokens in a context window. They cannot truly distinguish between instructions and user input — which is exactly why prompt injection attacks are possible.**

---

## Security Relevance

> 🔒 **Every security challenge with LLMs stems from their architecture:**
> - Prompt injection → no separation between instructions and data
> - Hallucinations → confident predictions without factual grounding
> - Data leakage → training data memorization
> - Jailbreaking → safety training can be overridden with clever prompting
> - Non-determinism → testing and validation is fundamentally harder

---

## Quick Reference

| Concept | What it is | Security concern |
|---------|-----------|-----------------|
| Tokens | Text chunks the LLM reads | Context window limits, token stuffing |
| Context window | Total text the LLM can see | Context overflow, instruction displacement |
| System prompt | Developer instructions | Can be extracted or overridden |
| Temperature | Randomness control | Higher = less predictable behavior |
| Fine-tuning | Specializing a model | Can embed backdoors |
| Completion | Model's output | Can contain harmful/leaked content |

---

*Previous: [AI vs ML ←](01-ai-vs-ml.md) | Next: [RAG Explained →](03-rag.md)*