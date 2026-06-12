# Dataset Card: UTSR-ToolMeta

## Dataset Summary

UTSR-ToolMeta is a normalized dataset of LLM-Agent tool declarations. It maps heterogeneous tool metadata into the Unified Tool Semantic Representation (UTSR), including source information, tool identity, capability descriptions, input and output interfaces, and binding references.

The dataset is designed for studying how model-visible tool declarations influence agent behavior, including candidate tool recall, tool selection, invocation planning, and parameter generation.

## Dataset Composition

| Subset | Records | Description |
|---|---:|---|
| `release_valid` | 7,593 | Main valid release set after excluding hard-invalid records. |
| `high_confidence` | 4,408 | Strict subset containing only `keep` records from the quality gate. |
| `core_balanced` | 2,000 | Balanced subset with 400 records per source family. |

## Source Coverage

The dataset includes records from:

- MCP tool catalogs and MCP server tool declarations;
- OpenAPI operation descriptions;
- agent framework and tool-library integrations;
- tool-use benchmark datasets;
- function-calling datasets.

## Fields

Each record contains:

- `record_id`: stable dataset identifier;
- `dataset_meta`: dataset-level metadata;
- `source_meta`: upstream source metadata;
- `function_profile`: functional domain, subdomain, operation type, task intent, and semantic tags;
- `utsr`: normalized tool semantic representation;
- `provenance`: construction and parsing provenance.

See `schema/field_dictionary.md` for detailed field definitions.

## Quality Control

The construction pipeline labels parsed candidates as:

- `keep`: structurally and semantically strong records;
- `review`: valid tool-semantic records with minor quality weaknesses;
- `exclude`: hard-invalid records such as tests, mocks, dummy tools, low-value validation endpoints, or records missing core semantics.

The public `release_valid` subset excludes `exclude` records and retains both `keep` and `review`. The `high_confidence` subset contains only `keep`.

## Intended Use

Recommended uses include:

- tool metadata standardization research;
- tool retrieval and reranking experiments;
- tool selection robustness evaluation;
- parameter generation evaluation;
- construction of semantically competitive tool pools;
- security analysis of model-visible tool declarations.

## Out-of-Scope Use

This dataset should not be used to:

- claim that a tool backend is safe or unsafe based only on metadata;
- execute third-party tools without independent review;
- infer proprietary or private tool behavior;
- deploy attacks against real systems.

## Limitations

- Some records originate from API or benchmark sources and may describe operations rather than directly executable local tools.
- Output schemas and return descriptions are not available for all sources.
- `function_profile` fields are generated or refined metadata and should be treated as analysis fields, not ground-truth tool behavior.
- The dataset focuses on model-visible declarations, not tool implementation code.

## Languages

Most tool declarations are in English.

## Maintenance

Future versions may add additional source families, stronger schema validation, richer output descriptions, and task-level annotations for tool-use experiments.

