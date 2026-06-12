# Quality Summary

The construction pipeline parsed 7,697 candidate records and assigned a quality decision to each candidate:

| Decision | Records | Meaning |
|---|---:|---|
| `keep` | 4,408 | High-quality records with no major quality warnings. |
| `review` | 3,185 | Valid records with minor quality weaknesses. |
| `exclude` | 104 | Hard-invalid or low-value records removed from public release. |

After removing 104 `exclude` records, the main release set contains 7,593 records.

## Exclude Reasons

Some records may have multiple reasons.

| Reason | Count |
|---|---:|
| `test_or_mock_record` | 103 |
| `toolbench_operation_without_schema` | 41 |
| `no_parameters_or_input_schema` | 35 |
| `parameter_descriptions_incomplete` | 18 |
| `long_description` | 7 |
| `function_calling_model_api` | 7 |
| `low_value_api_validation` | 1 |

## Review Reasons

Some records may have multiple reasons.

| Reason | Count |
|---|---:|
| `no_parameters_or_input_schema` | 1,550 |
| `parameter_descriptions_incomplete` | 1,283 |
| `toolbench_operation_without_schema` | 1,262 |
| `function_calling_model_api` | 741 |
| `long_description` | 56 |

