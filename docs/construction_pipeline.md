# Construction Pipeline

The UTSR-ToolMeta construction pipeline transforms heterogeneous tool metadata into a unified JSONL dataset.

## Stage 1: Source Selection

Sources were selected to cover multiple kinds of model-visible tool declarations:

- MCP tools and MCP server catalogs;
- OpenAPI operation specifications;
- framework-integrated tools and tool libraries;
- tool-use benchmark data;
- function-calling datasets.

The goal is to avoid over-reliance on a single ecosystem and to support cross-source comparison.

## Stage 2: Raw Collection

Raw data was collected into source-specific directories in the local construction workspace. Raw data is not included in this release repository. Instead, this repository contains normalized records, source metadata, and provenance references.

## Stage 3: Source-Specific Parsing

Different sources expose tool semantics in different structures. Source-specific parsers extract candidate fields such as:

- tool or function name;
- namespace or package;
- description and summary;
- input schema;
- parameter names, types, required flags, and descriptions;
- return description or output schema when available;
- raw descriptor references and source identifiers.

## Stage 4: UTSR Mapping

Candidate records are normalized into the UTSR schema:

- `source`: framework, upstream type, upstream channel, usage context, and field-origin map;
- `identity`: model-visible name and namespace;
- `capability`: description, summary, and return description;
- `interface`: input schema, parameters, output schema, and output type;
- `binding`: executor reference, serializer target, and raw descriptor reference.

## Stage 5: Functional Profiling

Each record receives a generated functional profile:

- `domain`;
- `subdomain`;
- `function_type`;
- `task_intent`;
- `semantic_tags`.

Functional profiles are used for grouping and constructing semantically competitive tool environments.

## Stage 6: Quality Gate

Parsed candidates are labeled as `keep`, `review`, or `exclude`. Hard-invalid records are excluded from the public `release_valid` subset. See `docs/quality_control.md`.

## Stage 7: Subset Construction

Three release subsets are produced:

- `release_valid`: valid records after removing `exclude`;
- `high_confidence`: only `keep` records;
- `core_balanced`: source-balanced subset sampled from `release_valid`.

