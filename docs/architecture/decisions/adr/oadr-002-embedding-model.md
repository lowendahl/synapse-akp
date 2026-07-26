---
type: ADR
title: "OADR-002 — Default Embedding Model"
id: oadr.002
status: open
date: 2026-07-25
tags: [adr, open, embedding, model, vector]
---

# OADR-002 — Default Embedding Model

## Status

**Open** — awaiting domain benchmark

## Question

Which embedding model should be used as the reference default for the vector projection?

## Candidate Families

| Model Family | Notes |
|--------------|-------|
| **BGE** (BAAI) | Strong retrieval; multiple sizes; ONNX available |
| **E5** (Microsoft) | Instruction-tuned; good at asymmetric search; multiple sizes |
| **Nomic Embed** | Open weights; Matryoshka (variable dimensions); good domain transfer |
| **Jina Embeddings** | Long-context (8K tokens); good for documents; commercial variants |
| **text-embedding-3-small/large** (OpenAI) | API-only; excellent quality; not self-hosted |

## Evaluation Criteria

- Domain retrieval quality on CSU/MCEM terminology
- Acronym and alias handling (CSU has heavy acronym use: C2C, NNR, MACC, UDC, TMM)
- Multilingual quality (English primary, but some content is localized)
- Model size (prefer ≤500MB for embedded use)
- CPU inference viability (or ONNX Runtime)
- Licensing (permissive for internal enterprise use)
- Reproducibility (deterministic inference)
- Embedding dimensions (balance: retrieval quality vs storage)

## Dependencies

- OADR-001 (vector engine must support the chosen dimensionality)
- A CSU-IQ-specific benchmark corpus is required before acceptance (per SDD §OADR-KP-006)

## Resolution Criteria

1. Curate 50 query–answer pairs from the CSU/MCEM domain.
2. Embed the full compiled corpus with each candidate model.
3. Measure Recall@5, Recall@10, MRR on the benchmark.
4. Record inference time, model size, Windows ONNX compatibility.
5. Select the model with best Recall@10 that meets CPU inference and licensing constraints.

## Current Leaning

E5-large-v2 or Nomic Embed (both have strong domain transfer, ONNX support, permissive licensing). Final decision blocked on benchmark.
