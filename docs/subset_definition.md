# Subset Definition

UTSR-ToolMeta provides three public release subsets.

## `release_valid`

`release_valid` is the main release set. It is constructed by removing hard-invalid `exclude` records from the parsed candidate pool while retaining both `keep` and `review` records.

Use this subset when broad source coverage is important.

## `high_confidence`

`high_confidence` contains only records that passed the quality gate as `keep`.

Use this subset when precision and metadata completeness matter more than broad coverage.

## `core_balanced`

`core_balanced` is sampled from `release_valid`. It contains 2,000 records, with 400 records from each source family:

- `mcp`;
- `openapi`;
- `framework_tool`;
- `tool_benchmark`;
- `function_calling_dataset`.

Use this subset for experiments where source balance is important.

## Relationship

```text
parsed candidates
  -> quality-labeled candidates
  -> release_valid = keep + review
  -> high_confidence = keep
  -> core_balanced = balanced sample from release_valid
```

