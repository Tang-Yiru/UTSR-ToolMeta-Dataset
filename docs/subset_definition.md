# Dataset Subsets

All current subsets are in `releases/v0.2/data/`.

| Subset | Records | Meaning |
|---|---:|---|
| `release_valid` | 7,593 | Full valid declaration set. |
| `high_confidence` | 4,408 | Inherited declaration-quality subset. |
| `core_balanced` | 2,000 | Source-balanced subset with 400 records per family. |

The five families are `mcp`, `openapi`, `framework_tool`, `tool_benchmark`, and `function_calling_dataset`. Subsets overlap and are not independent additional records. Stable IDs allow joins to the main set. Identical IDs have identical public records across subsets; each subset retains its own ordering.

Subset membership does not imply human-gold profile accuracy, executable compatibility, or authorization to access a third-party service.
