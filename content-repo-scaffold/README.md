# CSU-IQ-V2 Knowledge Packs

Knowledge sources and compiled DuckDB packs for the CSU-IQ-V2 domain.

## Structure

```
okf/                  Canonical Markdown sources (OKF v0.2)
  csu/               CSU domain knowledge (69 concepts)
  mcem/              MCEM domain knowledge (44 concepts)
  ontology.yaml      Shared type/predicate schema
  pack-rules.yaml    Compile-time validation rules
dist/                Compiled .duckdb packs (in releases)
```

## Usage

### As a consumer (recommended)

```bash
pip install akp-runtime
# Edit ~/.akp/config.yaml to point to this repo's releases
akp-runtime-mcp --config ~/.akp/config.yaml
```

Packs are automatically downloaded from GitHub Releases on first use.

### As an author (editing knowledge sources)

```bash
pip install akp-compiler
git clone https://github.com/lowendahl/csu-iq-v2-knowledge.git
cd csu-iq-v2-knowledge

# Edit Markdown files in okf/
# Compile locally:
kp-compile okf/mcem --output dist/mcem.duckdb --skip-embeddings
kp-compile okf/csu --output dist/csu.duckdb --skip-embeddings --dependency dist/mcem.duckdb
```

## Releases

Each release includes pre-compiled `.duckdb` packs as assets:
- `mcem.duckdb` — MCEM framework knowledge
- `csu.duckdb` — CSU domain knowledge (depends on MCEM)

The runtime fetches these automatically via `github://` URIs in config.

## Contributing

1. Edit Markdown files in `okf/` following frontmatter schema
2. Types and predicates must exist in `okf/ontology.yaml`
3. Run PII scanner before committing: `python scripts/pii_scanner.py`
4. CI compiles and validates on every PR
