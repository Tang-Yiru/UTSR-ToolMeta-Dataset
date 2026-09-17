# UTSR-ToolMeta v0.2 Field Dictionary

Use `releases/v0.2/schema/utsr_record.schema.json` for the public record schema.

## Record Fields

| Field | Meaning |
|---|---|
| `record_id` | Stable record identifier. |
| `dataset_meta` | Original dataset name, creation date, language, split, schema metadata, and source UID. |
| `source_meta` | Upstream source family, ID, URL, version, license metadata, framework, and collection metadata. |
| `function_profile` | Derived semantic labels, described below. |
| `utsr` | Normalized declaration, described below. |
| `provenance.raw_descriptor_ref` | Upstream descriptor reference; the raw files are not bundled. |

Original per-record metadata are retained; package `VERSION.json` identifies the public distribution. Construction-only parser candidates and local work traces are not included.

## Functional Profile

| Field | Type | Meaning |
|---|---|---|
| `primary_domain` | string | Primary L1 domain from the 37-value vocabulary, including `unknown`. |
| `primary_subdomain` | string or null | Lower-snake-case descriptive subdomain, not a closed vocabulary. |
| `secondary_domains` | array of strings | Additional supported domains; unique, without `unknown` or the primary domain. |
| `supported_actions` | array of strings | Nonempty unique direct actions. `unknown` may occur only alone. |
| `primary_action` | string or null | Main supported action when evidence establishes one. |
| `action_mode` | string | `single`, `multi`, or `unknown`. |
| `effect_class` | string | `read_only`, `compute_only`, `state_creating`, `state_modifying`, `state_deleting`, `external_side_effect`, `mixed`, or `unknown`. |
| `resource_object` | string or null | Logical object acted upon or produced. |
| `cardinality` | string | `single`, `collection`, `batch`, or `unknown`. |
| `task_intent` | object | `actions`, `object`, `qualifiers`, and nullable `canonical_text`. |

The action vocabulary is `search`, `list`, `retrieve`, `create`, `update`, `delete`, `execute`, `transform`, `communicate`, `transfer`, `interact`, and `unknown`. Intent actions and object match the profile's supported actions and resource object.

AI-assisted derived profiles contain only these ten semantic fields. They are not original declarations, human gold, or verified backend behavior. Do not pass them to evaluated agents as tool metadata.

## UTSR Declaration

| Group | Fields |
|---|---|
| `source` | Framework, upstream type/channel, and usage context. |
| `identity` | Name and optional namespace. |
| `capability` | Primary description, optional summary, and return description. |
| `interface` | Input schema, flat parameters, output schema, and output type. |
| `binding` | Executor reference, serializer target, and raw descriptor reference. |

`input_schema` is the authoritative structured interface when trustworthy. Flat `parameters` preserve compatibility and source inspection; they must not be interpreted as an equivalent second invocation schema. Parameter names, types, requiredness, descriptions, defaults, and enums are preserved, including existing primitive/null type unions.

Missing optional information remains null or empty rather than being invented. A non-null input schema is not proof of validated execution compatibility. Bindings are references, not bundled implementations or credentials. Source text may contain illustrative values; those are not authorization to access a service.
