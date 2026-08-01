# Synapse — Agentic Knowledge Pack

Compiler and runtime for building immutable, versioned knowledge packs from
canonical Markdown sources.  Knowledge packs are DuckDB databases that power
agentic retrieval, evidence-grounded reasoning, and 3-D exploration.

📖 **[Product Overview](docs/product-pitch.md)** — what AKP is, who it's for, and why it matters.

## Quick start

```bash
cd compiler
pip install -e ".[dev]"

# Compile packs (MCEM first, then CSU with dependency)
kp compile okf/mcem
kp compile okf/csu

# Launch the 3-D explorer
kp-explore dist/kp-csu.duckdb dist/kp-mcem.duckdb
```

## Repository layout

```
compiler/      Synapse AKP compiler (Python package)
okf/           OKF v0.2 knowledge corpus (CSU + MCEM)
dist/          Compiled pack artifacts (git-ignored)
```

---
*Synapse Agentic Knowledge Pack — v0.1*
