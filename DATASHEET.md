# Datasheet for UTSR-ToolMeta v0.2

## Purpose and Composition

UTSR-ToolMeta supports research on standardized LLM-agent tool declarations. It represents source information, identity, capability descriptions, interfaces, and binding references from five source families. Records are declaration-level metadata, not executable backend implementations.

The main set contains 7,593 records. Its inherited declaration-quality subset contains 4,408 records; its source-balanced subset contains 2,000 records with 400 per family. The subsets overlap and retain stable identifiers. Duplicate declarations are not deleted.

## Annotation

The ten-field `function_profile` is derived using rule-based pre-annotation and AI-assisted per-record semantic review with conflict review. It is not human gold. No per-record AI provenance, confidence, or review metadata is added. `unknown` indicates insufficient declaration evidence; sixteen known parsing-gap records retain abstaining profiles.

Functional labels describe the current call's actions, resource, effects, and cardinality. They must not be presented to an evaluated agent as original tool metadata. Selected tool behaviors require independent verification before execution.

## Distribution

Files are JSONL under `releases/v0.2/data/`, with schemas, statistics, version information, and an integrity manifest in the same version directory. Source metadata and descriptor references are retained; construction traces, parser candidates, internal reviews, private work files, and experiment methods are excluded. Public utilities support reading, validation, and summary statistics, not reconstruction of the private research workspace.

## Limitations and Responsible Use

Some declarations are API operations or benchmark descriptions rather than immediately executable tools. Input and output specifications are incomplete for some sources. Profiles reflect declaration evidence, not measured execution behavior or independently established label accuracy. Subset names refer to declaration quality, not human-gold labels.

No backend code, private service credentials, or private user conversations are included. Upstream example strings can remain in source declarations and should not be used as real credentials. Follow source-specific licenses and terms. Conduct security research only in authorized controlled environments.
