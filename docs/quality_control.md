# Quality Control

The construction pipeline uses a quality gate to separate hard-invalid records from valid tool-semantic records.

## Quality Decisions

| Decision | Meaning | Included in `release_valid` | Included in `high_confidence` |
|---|---|---:|---:|
| `keep` | Strong record with no hard defects or major review warnings. | yes | yes |
| `review` | Valid tool-semantic record with minor quality weaknesses. | yes | no |
| `exclude` | Hard-invalid or low-value record. | no | no |

## Exclusion Criteria

Records may be excluded for reasons such as:

- test, mock, dummy, sample, or simulator records;
- low-value API validation or ping-like endpoints;
- missing core semantics, such as missing name or unusably short description;
- non-tool-like names.

## Review Criteria

Records may be marked for review when they are still valid but imperfect:

- missing or empty parameter list;
- incomplete parameter descriptions;
- very long descriptions;
- benchmark or API records that are useful for analysis but differ from runtime tools;
- generic task intent;
- operation records without explicit schema.

## Release Policy

`release_valid` removes only `exclude` records. It retains `keep` and `review` because both still contain usable tool semantics. `high_confidence` contains only `keep` and is intended for precision-sensitive experiments.

The quality gate is not part of the public record schema for the three release subsets. It is documented here as a construction and audit mechanism.

