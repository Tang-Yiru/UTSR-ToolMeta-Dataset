# Dataset Card: UTSR-ToolMeta v0.2

UTSR-ToolMeta normalizes LLM-agent tool declarations into UTSR for metadata analysis and tool-use research.

| Subset | Records |
|---|---:|
| release_valid | 7,593 |
| high_confidence | 4,408 |
| core_balanced | 2,000 |

Current files and schemas are in `releases/v0.2/`. Subsets overlap. The balanced core has 400 records per source family. Families are MCP, OpenAPI, framework tools, tool benchmarks, and function-calling datasets.

Each record preserves source identity and a normalized UTSR declaration alongside a ten-field derived functional profile. Profiles cover domain, actions, direct effects, resource, cardinality, and intent. Rule-based annotation and AI-assisted per-record review were used; profiles are not human gold or proof of backend behavior. Unknown labels represent insufficient evidence. Known parsing-gap records retain abstaining profiles. AI involvement is declared at dataset level only.

Use for declaration analysis and controlled tool-use research. Do not expose profiles to evaluated agents as tool-owned declarations, infer backend safety from metadata, or execute third-party services without authorization and independent checks. This public edition excludes internal construction traces, reviews, and experiment methods.

See [DATASHEET.md](DATASHEET.md), [the field dictionary](schema/field_dictionary.md), and [DATA_LICENSE.md](DATA_LICENSE.md). Source-derived rights remain with upstream providers; unknown licensing is not unrestricted permission. Paper and archival citation metadata will be added when available.
