# Enterprise AI: How Organizations Deploy AI at Scale

It's not just ChatGPT — it's an entire infrastructure with dozens of components, each one a potential attack vector.

---

## Enterprise AI ≠ Consumer AI

When you use ChatGPT, you're interacting with a simple interface to a single model.

Enterprise AI is fundamentally different:

| Consumer AI | Enterprise AI |
|-------------|---------------|
| Single model | Multiple models for different tasks |
| One user | Thousands of users, multiple tenants |
| General purpose | Domain-specific, custom-trained |
| Simple chat | Complex pipelines with tools and data |
| Provider handles security | YOU handle security |
| Pay per use | Infrastructure costs + compute + licensing |

---

## Common Enterprise AI Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Enterprise AI Platform                          │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                      AI Gateway                             │   │
│  │  (Authentication, Rate Limiting, Routing, Logging)          │   │
│  └────────────────────────────┬───────────────────────────────┘   │
│                               │                                    │
│  ┌────────────┬───────────────┼───────────────┬────────────────┐  │
│  │            │               │               │                │  │
│  ▼            ▼               ▼               ▼                ▼  │
│ ┌────┐    ┌────────┐    ┌─────────┐    ┌──────────┐    ┌──────┐ │
│ │LLM │    │ RAG    │    │ Agent   │    │ Fine-    │    │Custom│ │
│ │API │    │ System │    │ Runtime │    │ tuned    │    │Model │ │
│ │    │    │        │    │         │    │ Models   │    │      │ │
│ └────┘    └────────┘    └─────────┘    └──────────┘    └──────┘ │
│  │            │               │               │                │  │
│  └────────────┴───────────────┼───────────────┴────────────────┘  │
│                               │                                    │
│  ┌────────────────────────────▼───────────────────────────────┐   │
│  │                    Data Layer                                │   │
│  │  Vector DBs │ Traditional DBs │ Data Lakes │ APIs           │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                  Observability & Security                    │   │
│  │  Monitoring │ Logging │ Alerting │ Cost Tracking            │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Key Components Explained

### 1. AI Gateway

The front door to your AI infrastructure. Every request goes through here.

**What it does:**
- Authentication and authorization
- Rate limiting (prevent abuse and cost overruns)
- Request/response logging
- Routing to appropriate models
- Content filtering (input and output)
- Token counting and billing

**Examples:** AWS Bedrock Gateway, Azure API Management, Kong AI Gateway, custom solutions

**Security surface:** If the gateway is bypassed, all downstream security controls are meaningless.

### 2. Model Serving

How models are hosted and made available for inference.

| Approach | Description | Security consideration |
|----------|-------------|----------------------|
| API providers | OpenAI, Anthropic, Google | Data leaves your network |
| Self-hosted | Run models on your infrastructure | Full control, full responsibility |
| Hybrid | Some models internal, some external | Complex trust boundaries |
| Edge | Models on devices/local servers | Physical security matters |

**Security surface:** Model endpoints, API keys, network exposure, data in transit.

### 3. Vector Databases (for RAG)

Store embeddings of your company's knowledge for retrieval.

**What's stored:**
- Document embeddings (mathematical representations)
- Source documents or references
- Metadata (access level, department, date)

**Security surface:** Contains your company's intellectual property. Compromise = total knowledge exfiltration.

### 4. Prompt Management

Systems that manage and version prompts, system instructions, and templates.

**What's managed:**
- System prompts per use case
- Prompt templates with variables
- Version history of prompts
- A/B testing different prompts

**Security surface:** Whoever controls the prompts controls the AI's behavior.

### 5. Observability

Monitoring what the AI is doing, how it's performing, and whether it's being misused.

**Key metrics:**
- Latency per request
- Token usage and cost
- Error rates
- Content policy violations
- Anomalous usage patterns

**Security surface:** If observability is compromised, you can't detect attacks.

---

## Multi-Tenancy: The Enterprise Reality

Most enterprise AI platforms serve multiple customers, departments, or use cases on shared infrastructure.

```
┌──────────────────────────────────────────┐
│         Shared AI Infrastructure          │
│                                           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Tenant A │  │ Tenant B │  │Tenant C│  │
│  │ (Sales)  │  │  (Legal) │  │  (HR)  │  │
│  │          │  │          │  │        │  │
│  │ - Prompts│  │ - Prompts│  │- Prompts│ │
│  │ - Data   │  │ - Data   │  │- Data  │  │
│  │ - Models │  │ - Models │  │- Models│  │
│  └──────────┘  └──────────┘  └────────┘  │
│                                           │
│  Shared: Gateway, Compute, Some Models    │
└──────────────────────────────────────────┘
```

**Multi-tenancy security challenges:**
- Data isolation between tenants
- Preventing cross-tenant prompt leakage
- Ensuring one tenant can't access another's fine-tuned model
- Cost allocation and rate limiting per tenant
- Different compliance requirements per tenant

---

## Cost Management: A Security Concern

AI costs can spiral quickly:

| Resource | Cost driver | Risk |
|----------|------------|------|
| Input tokens | Every word sent to the model | Prompt stuffing attacks increase costs |
| Output tokens | Every word generated | Verbose responses drain budget |
| Compute | GPU/CPU time for inference | Denial-of-wallet attacks |
| Storage | Vector DBs, model weights, logs | Data accumulation |
| Fine-tuning | GPU hours for training | Expensive if triggered repeatedly |

**Denial-of-Wallet attack:** An attacker floods your AI system with requests, not to bring it down, but to exhaust your cloud budget.

```
Attacker sends 10,000 requests with maximum-length prompts
Each request costs $0.10 in tokens
Total damage: $1,000 in unexpected API costs

Scale this up: 1M requests = $100,000
```

---

## Enterprise AI Deployment Patterns

### Pattern 1: Chatbot / Assistant

```
User → AI Gateway → LLM → Response
```
Simplest pattern. Direct conversation with guardrails.

### Pattern 2: RAG-Powered Knowledge System

```
User → Gateway → Retrieve docs → Augment prompt → LLM → Response
```
LLM grounded in company knowledge.

### Pattern 3: Agentic Workflow

```
User → Gateway → Agent → [Tool calls] → Multiple LLM calls → Result
```
Agent autonomously completes complex tasks.

### Pattern 4: AI Pipeline (Multiple Models)

```
Input → Model A (classify) → Model B (extract) → Model C (generate) → Output
```
Chain of specialized models, each handling one step.

### Pattern 5: Human-in-the-Loop

```
User → AI (draft) → Human (review/approve) → Action
```
AI suggests, human decides. Common for high-stakes decisions.

---

## The Security Surface: Every Component is an Attack Vector

| Component | Attack type | Impact |
|-----------|------------|--------|
| AI Gateway | Bypass, credential theft | Full system access |
| LLM API | Prompt injection, jailbreak | Behavior manipulation |
| RAG / Vector DB | Knowledge poisoning | Corrupted outputs |
| Agent tools | Tool manipulation | Unauthorized actions |
| Data layer | Data poisoning, exfiltration | Corrupted training, data theft |
| Prompt store | Prompt theft, modification | Behavior control |
| Logging system | Log injection, evasion | Hide attack evidence |
| Model weights | Model theft, backdoors | IP theft, hidden behaviors |
| Fine-tuning pipeline | Training data poisoning | Persistent compromise |
| Network | Man-in-the-middle | Intercept AI traffic |

### Key Insight: Defense in Depth

No single security control is sufficient. Enterprise AI requires security at every layer:

```
Layer 1: Network security (firewalls, encryption)
Layer 2: Authentication & authorization (who can access what)
Layer 3: Input validation (what goes into the AI)
Layer 4: Model-level controls (system prompts, guardrails)
Layer 5: Output filtering (what comes out of the AI)
Layer 6: Monitoring & alerting (detecting attacks)
Layer 7: Incident response (responding to breaches)
```

---

## Key Takeaway

> 💡 **Enterprise AI is infrastructure, not just a model. It includes gateways, databases, agents, pipelines, and observability systems. Each component introduces new attack vectors that don't exist in traditional software. Security professionals need to think about the ENTIRE system, not just the LLM.**

---

## Security Relevance

> 🔒 **When assessing enterprise AI security, map the full architecture:**
> - What models are deployed? (API, self-hosted, fine-tuned?)
> - What data flows through the system? (PII, financial, proprietary?)
> - What tools/actions can the AI take? (Read-only? Write? Delete?)
> - Who has access? (Multi-tenant? Public-facing? Internal only?)
> - What's the blast radius if compromised? (One user? All customers?)
> - What monitoring exists? (Can you detect an attack in progress?)
> - What's the cost exposure? (Can someone drain your budget?)

---

## Quick Reference

| Pattern | Components | Highest risk |
|---------|-----------|-------------|
| Simple chatbot | Gateway + LLM | Prompt injection, jailbreak |
| RAG system | Gateway + Vector DB + LLM | Knowledge poisoning |
| Agent system | Gateway + LLM + Tools | Unauthorized tool execution |
| Multi-model pipeline | Gateway + Multiple models | Chain-of-failure |
| Fine-tuned model | Training pipeline + Model | Training data poisoning |

---

*Previous: [AI Agents ←](04-ai-agents.md) | Next: [Module 2: AI Threat Landscape →](../02-ai-threat-landscape/README.md)*
