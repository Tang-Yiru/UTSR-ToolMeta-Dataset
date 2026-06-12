# UTSR-ToolMeta Dataset

Status: internal research draft, version 0.1.0. This repository is currently prepared for research-group discussion. Citation metadata, final paper information, and data licensing notes may be revised before public archival release.

UTSR-ToolMeta is a dataset of LLM-Agent tool declarations normalized into the Unified Tool Semantic Representation (UTSR). It is designed for research on tool metadata modeling, tool retrieval, tool selection, invocation planning, parameter generation, and security analysis of tool-using agents.

The dataset unifies tool descriptions from multiple source families, including MCP tool catalogs, OpenAPI operations, framework-integrated tools, tool-use benchmarks, and function-calling datasets. Each record contains a normalized UTSR object plus dataset metadata, source metadata, functional profiling fields, and provenance information.

## Dataset Files

| File | Records | Description |
|---|---:|---|
| `data/utsr_records.release_valid.jsonl` | 7,593 | Main release set after removing hard-invalid records. |
| `data/utsr_records.high_confidence.jsonl` | 4,408 | High-confidence subset containing only records that passed all quality gates. |
| `data/utsr_records.core_balanced.jsonl` | 2,000 | Balanced core subset sampled from `release_valid`, with 400 records per source family. |

The full construction pipeline produced 7,697 parsed candidate records. A quality gate was applied to label records as `keep`, `review`, or `exclude`. The public release set removes 104 `exclude` records while retaining `keep` and `review` records as valid tool-semantic samples.

## Source Families

The main release set covers five source families:

| Source family | Description |
|---|---|
| `mcp` | Tool declarations exposed by MCP servers or MCP tool catalogs. |
| `openapi` | OpenAPI operations that can be converted into agent-callable tools. |
| `framework_tool` | Tools integrated in agent frameworks or tool libraries. |
| `tool_benchmark` | Tool-use benchmark records with tool or API operation descriptions. |
| `function_calling_dataset` | Function-calling datasets that contain model-visible function declarations. |

## Record Format

Each JSONL line is one UTSR-ToolMeta record:

```json
{
  "record_id": "...",
  "dataset_meta": { "...": "..." },
  "source_meta": { "...": "..." },
  "function_profile": { "...": "..." },
  "utsr": {
    "source": { "...": "..." },
    "identity": { "...": "..." },
    "capability": { "...": "..." },
    "interface": { "...": "..." },
    "binding": { "...": "..." }
  },
  "provenance": { "...": "..." }
}
```

See [`schema/field_dictionary.md`](schema/field_dictionary.md) for field definitions and [`schema/utsr_record.schema.json`](schema/utsr_record.schema.json) for the machine-readable schema.

## Functional Profiles

In addition to UTSR fields, each record includes a `function_profile` used for dataset analysis and experimental environment construction:

- `domain`: coarse functional domain.
- `subdomain`: fine-grained functional category.
- `function_type`: operation type, such as retrieve, search/list, create/write, modify, or delete/destructive.
- `task_intent`: concise natural-language intent summary.
- `semantic_tags`: lightweight tags for semantic grouping.

These fields are intended for grouping, filtering, retrieval, and competition-pool construction. They are not assumed to be visible to the tested agent.

## Intended Uses

UTSR-ToolMeta can support:

- cross-framework tool metadata analysis;
- tool retrieval and candidate tool recall experiments;
- tool selection and invocation planning evaluation;
- parameter generation analysis;
- construction of semantically competitive tool environments;
- security research on model-visible tool metadata perturbations.

## Quick Start

Read a dataset file:

```bash
python examples/read_dataset.py data/utsr_records.core_balanced.jsonl --limit 3
```

Validate basic record integrity:

```bash
python scripts/check_record_integrity.py data/utsr_records.release_valid.jsonl
```

Generate statistics:

```bash
python scripts/summarize_dataset.py data/utsr_records.release_valid.jsonl --out stats
```

Build a simple competition pool:

```bash
python examples/build_competition_pool.py data/utsr_records.core_balanced.jsonl --record-id UTSR-MCP-000001 --top-k 8
```

## Repository Layout

```text
data/       Final release dataset files.
schema/     JSON Schema and field dictionary.
docs/       Construction, quality control, source, subset, and ethics notes.
stats/      Dataset statistics and quality summaries.
examples/   Minimal usage examples.
scripts/    Validation and summarization utilities.
```

## Citation

For the current internal draft, cite this repository. A final paper citation will be added when publication metadata is available. A `CITATION.cff` file is provided for GitHub citation metadata.

## Notice

This dataset contains normalized tool declaration metadata derived from public or research-oriented sources. It does not include raw construction files, tool backend code, private user data, or private execution credentials. Users are responsible for complying with applicable upstream licenses and terms of use. See [`DATA_LICENSE.md`](DATA_LICENSE.md) and [`NOTICE.md`](NOTICE.md).
