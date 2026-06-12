# Field Dictionary

Each JSONL line is one UTSR-ToolMeta record. The dataset keeps UTSR as the central normalized representation and adds dataset-level metadata, source metadata, functional profile fields, and provenance fields around it.

## Top-Level Fields

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `record_id` | string | no | Stable unique identifier for the normalized record. The prefix reflects the dataset/source split, such as `UTSR-MCP-000001`. |
| `dataset_meta` | object | no | Dataset management metadata, including dataset name, schema version, split, language, and construction date. |
| `source_meta` | object | no | Upstream source metadata, including source family, source identifier, URL, version, license, and collection method. |
| `function_profile` | object | no | Generated functional profile used for grouping, filtering, and experiment construction. |
| `utsr` | object | no | Unified Tool Semantic Representation, the normalized core representation of model-visible tool declarations. |
| `provenance` | object | no | Parsing and traceability metadata for reproducing how the record was constructed. |

## `dataset_meta`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `dataset_name` | string | no | Dataset name, expected to be `UTSR-ToolMeta`. |
| `schema_version` | string | no | Version of the dataset schema. |
| `created_at` | string | no | Date when the record version was created. |
| `language` | string | no | Primary language of the tool declaration. |
| `split` | string | no | Source split or source-family label used in record identifiers. |
| `source_record_uid` | string | no | Stable hash or identifier for the parsed source record. |

## `source_meta`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `source_family` | string | no | High-level source family, such as `mcp`, `openapi`, `framework_tool`, `tool_benchmark`, or `function_calling_dataset`. |
| `source_id` | string | no | Internal identifier of the upstream source. |
| `source_url` | string | yes | URL of the upstream source when available. |
| `source_version` | string | yes | Snapshot date, commit, release, or version identifier. |
| `license` | string | yes | Upstream license string when available. |
| `framework` | string | yes | Framework or protocol environment associated with the source. |
| `priority` | string | yes | Internal priority level used during source selection. |
| `collection_method` | string | yes | Method used to collect the upstream data, such as repository clone, dataset import, or API specification import. |

## `function_profile`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `domain` | string | no | Coarse functional domain, such as `information_retrieval`, `financial`, `developer_tools`, or `data_management`. |
| `subdomain` | string | no | Fine-grained functional category within the domain. |
| `function_type` | string | no | Operation type, such as `retrieve`, `search_or_list`, `create_or_write`, `modify`, or `delete_or_destructive`. |
| `task_intent` | string | no | Concise natural-language description of the task the tool is intended to support. |
| `semantic_tags` | array[string] | no | Lightweight semantic tags for filtering and grouping. |
| `profile_origin` | string | no | Origin of the functional profile, such as rule-generated or rule-generated with assisted refinement. |

## `utsr.source`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `framework` | string | yes | Framework or protocol into which the tool declaration can be loaded. |
| `upstream_type` | string | yes | Type of upstream semantic carrier, such as MCP tool, OpenAPI operation, function declaration, or framework tool. |
| `upstream_channel` | string | yes | Collection channel or upstream representation category. |
| `usage_context` | string | yes | Expected use context in an agent system, such as runtime tool, benchmark tool, or API-operation candidate. |
| `field_origin_map` | object | no | Mapping from UTSR fields to original fields or generated sources. |

## `utsr.identity`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `name` | string | no | Model-visible tool or function name. |
| `namespace` | string | yes | Namespace, plugin, package, MCP server, or tool collection name. |

## `utsr.capability`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `description` | string | no | Natural-language description of the tool capability, usage scenario, and capability boundary. |
| `summary` | string | yes | Short capability summary when available or generated. |
| `return_description` | string | yes | Natural-language description of the expected return value or output. |

## `utsr.interface`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `input_schema` | object | yes | Structured input schema when available. |
| `parameters` | array[object] | no | Normalized list of input parameters. |
| `output_schema` | object | yes | Structured output schema when available. |
| `output_type` | string | yes | Coarse output type, such as `object`, `array`, `string`, `number`, `boolean`, `file`, `image`, or `text`. |

## `utsr.interface.parameters[]`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `name` | string | no | Parameter name. |
| `type` | string | yes | Parameter type. |
| `required` | boolean | yes | Whether the parameter is required. |
| `description` | string | yes | Natural-language parameter description. |
| `default` | any | yes | Default value when available. |
| `enum` | array | yes | Enumerated values when available. |

## `utsr.binding`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `executor_ref` | string | yes | Stable reference to the executable entity, such as function signature, MCP server and tool name, endpoint, or plugin function path. |
| `serializer_target` | string | yes | Target framework or protocol format for serialization. |
| `raw_descriptor_ref` | string | yes | Reference to the raw upstream descriptor used for normalization. |

## `provenance`

| Field | Type | Nullable | Description |
|---|---|---:|---|
| `raw_dir` | string | yes | Local raw source directory used during construction. |
| `raw_descriptor_ref` | string | yes | Raw descriptor reference. |
| `parser` | string | yes | Parser class or parser module that produced the record. |
| `parser_version` | string | yes | Parser version. |
| `parse_time_utc` | string | yes | UTC timestamp of parsing. |
| `candidate` | object | yes | Intermediate parsed candidate used to construct the UTSR record. |

