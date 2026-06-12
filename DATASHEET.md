# Datasheet for UTSR-ToolMeta

## Motivation

UTSR-ToolMeta was created to support systematic research on model-visible tool declarations in LLM-Agent systems. Existing tool descriptions are distributed across frameworks, protocols, tool libraries, API specifications, and benchmark datasets. This dataset normalizes such heterogeneous metadata into UTSR so that tool semantics can be compared, filtered, perturbed, and evaluated across sources.

## Composition

Each record represents one model-visible tool declaration or tool-like operation. A record contains normalized metadata for source, identity, capability, interface, binding, functional profile, and provenance.

The release contains three subsets:

- `release_valid`: the main valid release set;
- `high_confidence`: a stricter subset containing only high-confidence records;
- `core_balanced`: a source-balanced subset for experiments.

## Collection Process

The construction process contains four stages:

1. Source discovery and raw collection from public tool metadata repositories, framework-integrated tools, MCP catalogs, OpenAPI operation descriptions, and tool-use datasets.
2. Source-specific parsing into candidate tool records.
3. Mapping candidate records into the UTSR schema.
4. Functional profiling, quality gating, and subset construction.

Raw source files are not included in this release repository. The release focuses on normalized dataset records, schema documentation, statistics, and usage scripts.

## Preprocessing and Cleaning

The pipeline removes or excludes records that are likely to be tests, mocks, dummy records, validation-only endpoints, or records missing core semantics. Valid but imperfect records are retained in `release_valid` and documented through quality-control summaries.

## Labeling and Annotation

The dataset includes generated functional profiles:

- `domain`;
- `subdomain`;
- `function_type`;
- `task_intent`;
- `semantic_tags`.

These fields are produced by rule-based extraction and refinement procedures. They are intended to support grouping and experiment construction rather than to serve as authoritative labels of tool behavior.

## Uses

The dataset is suitable for research on:

- unified tool semantic representation;
- candidate tool recall and retrieval;
- tool selection and planning;
- parameter generation;
- robustness and security of tool metadata;
- semantically competitive tool environment construction.

## Distribution

The dataset is distributed as JSONL files. Each line is a single record.

## Ethical Considerations

The dataset can be used for security research on perturbing tool metadata. Researchers should use it in controlled experimental environments and avoid applying perturbation methods to real tool registries or production agent systems without authorization.

## Limitations

The dataset does not include tool backend source code, execution credentials, runtime traces, or private user data. It primarily represents static tool declarations and cannot alone determine actual backend behavior.

