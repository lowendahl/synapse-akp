# Component: Explorer

## Purpose
Explorer is the compiled-pack visualization surface. It reads one or more immutable packs, merges their graph state, and emits a single self-contained HTML artifact for offline exploration of nodes, edges, aliases, semantic units, and cross-pack links.

## Modules Covered
- `kp_compiler.consumer.explorer` — CLI orchestration
- `kp_compiler.consumer.pack_data_extractor` — read-only pack extraction and graph merging
- `kp_compiler.consumer.explorer_template_builder` — HTML assembly and asset inlining
- `compiler/src/kp_compiler/consumer/explorer-app/**/*` — inlined HTML, CSS, and application JavaScript assets
- `compiler/src/kp_compiler/consumer/vendor/3d-force-graph.min.js` — vendored rendering dependency inlined into the output artifact

## Responsibilities
- Open compiled packs read-only and extract graph-facing data
- Merge multi-pack nodes, intra-pack edges, and resolved cross-pack references
- Filter invalid links whose endpoints are absent from the merged node set
- Inline Explorer assets into a single offline HTML file
- Preserve pack identity on rendered nodes and links

## Out of Scope
- Editing knowledge
- Running compiler stages
- Serving MCP tools
- Mutating pack contents

## Promises
- **P-EXP-001**: Explorer emits a single self-contained HTML artifact with inlined assets.
- **P-EXP-002**: Only links whose source and target both exist in the merged node set appear in output.
- **P-EXP-003**: Duplicate links are removed by `(source, target, predicate)` identity.
- **P-EXP-004**: Pack reads are performed in read-only mode.

## Invariants
- **INV-EXP-001**: Explorer reflects compiled pack state rather than regenerating domain knowledge.
- **INV-EXP-002**: Asset assembly is deterministic for the same input packs and asset files.
- **INV-EXP-003**: Visualization generation never mutates the source packs.

## Dependencies
- DuckDB pack schema
- Explorer web assets under `consumer/explorer-app`

## Dependents
- Knowledge engineers inspecting compiled packs
- Architecture and review workflows requiring graph visualization
