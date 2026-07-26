# Knowledge Pack Author Guide

> How to create, configure, and validate an OKF Knowledge Pack — no code required.

---

## What Is a Knowledge Pack?

A Knowledge Pack is a **compiled, searchable database** built from a folder of
Markdown files.  Each file describes one concept — a KPI, a process, a role, an
evidence path — using structured YAML frontmatter and plain-language prose.

The compiler reads those files, validates them against an **ontology** (the list
of allowed types and relationships), applies **quality rules**, and produces a
single `.duckdb` file you can query with the `kp find` command.

```
Your Markdown Files  ──▶  kp compile  ──▶  Knowledge Pack (.duckdb)
                                │
                         ontology.yaml
                         pack-rules.yaml
```

---

## Quick Start

### 1. Install the compiler

```powershell
cd compiler
pip install -e .
```

This creates the `kp` command on your PATH.

### 2. Compile your pack

```powershell
kp compile okf/csu --ontology okf/ontology.yaml --output dist/kp-csu.duckdb --pack-id kp-csu --skip-embeddings
```

### 3. Search it

```powershell
kp find "C2C" --pack dist/kp-csu.duckdb
```

---

## Folder Structure

```
okf/
├── ontology.yaml          ← Allowed types & relationships
├── pack-rules.yaml        ← Quality gates (alias rules, assertions)
├── csu/                   ← One domain folder per Knowledge Pack
│   ├── metric/            ← Subfolders organize by type (optional)
│   │   ├── c2c.md
│   │   └── nnr.md
│   ├── process/
│   │   └── commit-to-complete.md
│   ├── evidence/
│   │   └── c2c-evidence.md
│   └── ...
└── mcem/                  ← Another domain → another pack
    ├── methodology/
    └── ...
```

**Rules:**
- Each `.md` file = one knowledge object
- Filenames should be kebab-case
- Subfolders are optional but help organization
- One domain folder maps to one compiled pack

---

## Writing a Knowledge Object

Every file needs YAML **frontmatter** between `---` markers, followed by Markdown
body content.

### Minimal Example

```markdown
---
id: csu.metric.c2c
type: KPI
title: "Job 1 — Commit to Complete (C2C)"
description: "Percentage of quarterly committed milestones closed within due date."
status: active
domain: csu
aliases:
  - C2C
  - Commit to Complete
tags:
  - kpi
  - pipeline
---

## Definition

C2C measures the percentage of milestones that were committed at the 5th-of-month
snapshot and subsequently closed by their due date.

## Target

≥ 95% per quarter.

## Measurement

- **Numerator**: Milestones closed on time
- **Denominator**: Milestones committed at snapshot (frozen)

## Evidence Path

See: `csu.evidence.job-1-c2c-evidence`
```

### Required Fields

| Field | What it does | Example |
|-------|-------------|---------|
| `id` | Unique stable identifier | `csu.metric.c2c` |
| `type` | Object type (must match ontology) | `KPI`, `Process`, `Role` |
| `title` | Human-readable name | `"Job 1 — Commit to Complete (C2C)"` |
| `description` | One-sentence summary | `"Percentage of committed milestones closed on time."` |
| `status` | Lifecycle state | `active`, `draft`, `deprecated` |
| `domain` | Domain prefix | `csu`, `mcem` |

### Optional Fields

| Field | What it does | Example |
|-------|-------------|---------|
| `aliases` | Alternative names for search | `[C2C, "Commit to Complete"]` |
| `tags` | Categorical labels | `[kpi, pipeline, c2c]` |
| `relationships` | Links to other objects | See below |

### Relationships

```yaml
relationships:
  - predicate: measures
    object: csu.process.commit-to-complete
  - predicate: requires
    object: csu.evidence.job-1-c2c-evidence
```

The `predicate` must be defined in `ontology.yaml`.

---

## ID Convention

IDs follow the pattern: `{domain}.{type-folder}.{kebab-name}`

```
csu.metric.c2c
csu.process.commit-to-complete
csu.evidence.job-1-c2c-evidence
mcem.stage.qualify
```

**Rules:**
- Must be globally unique across all packs
- Use lowercase and hyphens only
- Once assigned, never change (these are stable references)

---

## Aliases & Tags Best Practices

### Aliases
- Add the official acronym and its full expansion
- Add commonly-used informal names
- **Avoid** generic English words (`this`, `the`, `with`) — the compiler will
  filter these automatically via the stopword list in `pack-rules.yaml`

### Tags
- Use for categorical grouping (`kpi`, `pipeline`, `delivery`)
- Keep tags specific enough to be useful — a tag on every object is noise
- The compiler warns if a tag covers >50% of all objects

---

## The Ontology (`ontology.yaml`)

The ontology defines **what types exist** and **what relationships are allowed**.
You don't usually need to edit this — but if you add a new `type:` value in your
frontmatter that isn't in the ontology, the compiler will warn you.

### Auto-discovery

If you're starting a brand new knowledge domain:

```powershell
kp compile okf/my-domain --ontology okf/ontology.yaml --discover-ontology --skip-embeddings
```

This scans your files and generates/updates `ontology.yaml` automatically.

---

## Quality Rules (`pack-rules.yaml`)

This file controls two things:

### 1. Alias Quality Gate (applied during compilation)

Prevents bad aliases from entering the pack:

```yaml
alias_rules:
  stopwords: [this, the, a, an, it, is, are]  # rejected automatically
  min_length: 2                                 # "x" is too short
  max_tag_fanout: 15                            # warn if tag on >15 objects
  max_explicit_fanout: 8                        # warn if alias on >8 objects
  blocked_patterns: ["^\\d+$"]                  # reject pure numbers
```

**To add a stopword:** just add it to the list. No code changes needed.

### 2. Outcome Assertions (run after compilation)

These check the quality of the compiled pack:

```yaml
outcome_assertions:
  - name: explicit-alias-precision
    description: "Search an alias → its owner appears in top-5 results"
    rule: alias_owner_in_top_k
    params: { k: 5, sample: 20 }

  - name: tag-fanout-limit
    description: "No tag covers more than 50% of objects"
    rule: max_tag_coverage
    params: { threshold: 0.5 }

  - name: bm25-self-retrieval
    description: "Search a title → that object appears in top-5"
    rule: title_self_retrieval
    params: { k: 5, sample: 30 }
```

### Available Assertion Rules

| Rule | What it checks | Key params |
|------|---------------|------------|
| `alias_owner_in_top_k` | Alias search returns its owner | `k`, `sample` |
| `max_tag_coverage` | No tag covers too many objects | `threshold` (0.0–1.0) |
| `title_self_retrieval` | Title search returns the object | `k`, `sample` |
| `no_orphan_aliases` | All aliases point to real objects | — |

### Quality Thresholds

```yaml
quality_thresholds:
  min_assertion_pass_rate: 0.6   # at least 60% of assertions must pass
  fail_on_error: true            # fail the build if below threshold
```

---

## Understanding Compiler Output

A successful build looks like:

```
[rules]    Loaded okf/pack-rules.yaml
[discover] Found 83 source files
[ontology] Loaded v1.0.0
[parse]    Parsed 83 objects
[validate] 0 errors, 0 warnings
[enrich]   +98 aliases, 43 acronyms
[graph]    69 nodes, 0 edges
[semantic] 513 semantic units
[aliases]  650 alias entries
[bm25]     Indexed 513 units, vocab=2180
[done]     Pack written to dist/kp-csu.duckdb in 9.4s
[outcome]  2/3 assertions passed (rate=67%)
  [PASS] explicit-alias-precision: 20/20 aliases found their owner in top-5
  [FAIL] tag-fanout-limit: 1 tag over threshold
  [PASS] bm25-self-retrieval: 30/30 titles found themselves via alias

[OK] BUILD SUCCEEDED -- 70 warning(s)
```

### What the stages do

| Stage | Purpose |
|-------|---------|
| `discover` | Finds all `.md` files in your source folder |
| `ontology` | Loads the type/relationship definitions |
| `parse` | Reads frontmatter + body from each file |
| `validate` | Checks required fields, type conformance |
| `enrich` | Expands aliases, detects acronyms, finds duplicates |
| `graph` | Builds the relationship graph |
| `semantic` | Splits content into searchable chunks |
| `aliases` | Builds the alias lookup table |
| `bm25` | Builds the lexical search index |
| `embed` | Builds the semantic vector index (optional) |
| `outcome` | Runs quality assertions against the compiled pack |

### When the build fails

- **Parse errors** — Your YAML frontmatter has syntax issues
- **Validation errors** — Missing required fields or unknown types
- **Outcome failures** — The compiled pack fails quality assertions

Fix the reported issues and recompile.

---

## CLI Reference

### Compile

```powershell
kp compile <source-dir> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--ontology` | `okf/ontology.yaml` | Path to ontology |
| `--output` | `dist/kp-csu.duckdb` | Output pack path |
| `--pack-id` | `kp-csu` | Pack identifier |
| `--rules` | `<source>/../pack-rules.yaml` | Path to rules file |
| `--skip-embeddings` | off | Skip dense vector stage (faster) |
| `--discover-ontology` | off | Auto-generate ontology from corpus |
| `--dependency-pack` | none | Cross-pack validation reference |

### Search

```powershell
kp find "<query>" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--pack` | `dist/kp-csu.duckdb` | Pack to search |
| `--exact` | off | Alias matches only |
| `--graph` | off | Expand graph neighborhood |
| `--semantic` | off | Include vector search |
| `--hops` | 2 | Graph expansion depth |

---

## Adding a New Knowledge Object

1. Create a new `.md` file in the appropriate subfolder
2. Add the required YAML frontmatter (copy from an existing file)
3. Write the body content with clear `##` section headings
4. Run `kp compile` — it will tell you if anything is wrong
5. Run `kp find "<your title>"` to verify it's searchable

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Unknown type 'X'" | Type not in ontology | Add to `ontology.yaml` or run `--discover-ontology` |
| "Parse error" | Bad YAML frontmatter | Check for missing quotes, colons, indentation |
| "Alias rejected (stopword)" | Alias is a common English word | Choose a more specific alias |
| "tag covers N% of objects" | Tag is too broad | Make the tag more specific or raise `max_tag_fanout` |
| "Build failed — outcome" | Quality assertions failed | Check the `[FAIL]` lines and fix the underlying issue |
