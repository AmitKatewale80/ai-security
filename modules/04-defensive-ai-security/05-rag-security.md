# Securing RAG Pipelines

Protecting Retrieval-Augmented Generation systems against data poisoning, exfiltration, and manipulation attacks.

## Overview

RAG pipelines introduce unique attack surfaces by combining retrieval systems with generative models. Attackers can target the knowledge base, retrieval logic, or generation process.

## RAG Attack Surface

| Component | Attack | Impact |
|-----------|--------|--------|
| Knowledge base | Data poisoning | LLM generates attacker-controlled content |
| Embedding model | Adversarial embeddings | Bypass similarity search |
| Vector database | Index manipulation | Retrieve wrong documents |
| Retrieval logic | Query injection | Extract unauthorized documents |
| Generation | Context injection | Override system instructions |

## Security Controls

### Ingestion Security
- Validate document sources before indexing
- Scan for injected prompts in documents (indirect injection)
- Apply sensitivity labels at ingestion time
- Maintain provenance metadata for all documents

### Retrieval Security
- Enforce ACLs at query time (never trust post-retrieval filtering alone)
- Limit number of retrieved chunks per query
- Validate relevance scores (reject low-confidence retrievals)
- Monitor for anomalous query patterns

### Generation Security
- Separate retrieved context from system instructions clearly
- Apply output filtering for data leakage
- Attribute responses to source documents
- Implement citation verification

## Poisoning Detection

1. **Baseline monitoring** — Track normal retrieval patterns
2. **Anomaly detection** — Flag unusual document retrievals
3. **Content scanning** — Regular scans for injected payloads
4. **Version control** — Track all knowledge base changes
5. **Integrity checks** — Hash verification on indexed content

## Related Labs

- [Lab 04 — RAG Data Extraction](../../airline-labs/lab-04-rag-data-extraction/) — Extracting data from vulnerable RAG
- [Lab 14 — Enterprise RAG Security](../../airline-labs/lab-14-enterprise-rag-security/) — Production RAG hardening

## Related Academy Module

- [Academy Module 4 — Defensive Security](../../airline-labs/academy/module-04-defensive-security.md)

---

| [← Previous](04-access-control.md) | [Back to Module](README.md) | [Next →](06-agent-sandboxing.md) |
