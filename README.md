# UTSR-ToolMeta Dataset

**Current version: v0.2.** UTSR-ToolMeta represents heterogeneous LLM-agent tool declarations in a Unified Tool Semantic Representation (UTSR).

## Dataset

| File | Records | Description |
|---|---:|---|
| [release_valid](releases/v0.2/data/utsr_records.release_valid.jsonl) | 7,593 | Full valid dataset. |
| [high_confidence](releases/v0.2/data/utsr_records.high_confidence.jsonl) | 4,408 | Subset inherited from declaration-quality screening. |
| [core_balanced](releases/v0.2/data/utsr_records.core_balanced.jsonl) | 2,000 | Balanced subset with 400 records per source family. |

The subsets overlap; do not concatenate them as independent samples. Sources include MCP declarations, OpenAPI operations, framework-integrated tools, tool benchmarks, and function-calling datasets. See [source overview](docs/source_overview.md).

Each record contains a stable `record_id`, `dataset_meta`, `source_meta`, `function_profile`, `utsr`, and a source descriptor reference under `provenance`. The UTSR object contains source information, tool identity, capability text, input/output interfaces, and binding references. Missing source information remains missing. Tool implementation code and service credentials are not distributed.

## Functional Profiles

Profiles contain exactly ten semantic fields:

`primary_domain`, `primary_subdomain`, `secondary_domains`, `supported_actions`, `primary_action`, `action_mode`, `effect_class`, `resource_object`, `cardinality`, and structured `task_intent`.

Functional profiles are derived labels produced with rule-based pre-annotation and per-record AI-assisted semantic review, including conflict review. AI participation is declared here at dataset level; records contain no added model, confidence, evidence, or review-status fields. These labels are not human gold or verified tool execution behavior. `unknown` means the declaration provides insufficient evidence. Sixteen records with known declaration parsing gaps have abstaining profiles. Declaration-quality subset names do not imply profile accuracy.

Profiles are for analysis and must not be supplied to an evaluated agent as tool-owned declarations. Before any execution experiment, independently verify the behavior of selected tools. See the [field dictionary](schema/field_dictionary.md) and [dataset card](DATASET_CARD.md).

## Usage

Python 3.10 or newer is required. Reading, statistics, and file-hash verification use only the standard library. Full schema validation additionally requires `jsonschema`.

```bash
pip install -r requirements.txt
python examples/read_dataset.py releases/v0.2/data/utsr_records.core_balanced.jsonl --limit 3
python scripts/verify_release.py releases/v0.2
python scripts/validate_schema.py releases/v0.2/data/utsr_records.release_valid.jsonl
python scripts/summarize_dataset.py releases/v0.2/data/utsr_records.release_valid.jsonl --out stats/v0.2
```

Use [the version-local record schema](releases/v0.2/schema/utsr_record.schema.json). Original per-record schema-version metadata is preserved for traceability; package-level `VERSION.json` identifies the current distribution.

## Repository Layout

```text
releases/v0.2/data/    The three current JSONL subsets.
releases/v0.2/schema/  Record and functional-profile schemas.
releases/v0.2/         Version, statistics, README, and SHA-256 manifest.
schema/               Field documentation.
docs/                 Source, subset, quality, and responsible-use notes.
scripts/              Dataset-reading support, validation, and statistics.
examples/             Minimal reading example.
tests/                Public utility tests.
```

The public edition omits construction-only metadata, private work files, and internal review assets. Source identities, normalized tool semantics, record IDs, subset ordering, and functional labels are retained. It contains neither attack algorithms nor experiment configurations. Previous repository versions remain available in Git history.

## Citation and Terms

Cite this repository and specify dataset version v0.2; see [CITATION.cff](CITATION.cff). No accompanying paper citation or archival DOI is claimed yet.

Code and documentation use the license in [LICENSE](LICENSE). Upstream-derived data remain subject to their respective terms; see [DATA_LICENSE.md](DATA_LICENSE.md) and [NOTICE.md](NOTICE.md). A source license marked unknown is not permission for unrestricted redistribution. Use only in authorized research environments. Report corrections with a record ID and source reference.
