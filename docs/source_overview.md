# Source Overview

UTSR-ToolMeta covers five source families.

## MCP

MCP records describe tools exposed by Model Context Protocol servers or MCP tool catalogs. These records commonly include a tool name, description, and JSON input schema.

## OpenAPI

OpenAPI records describe API operations that can be converted into agent-callable tools. These records are operation-level tool candidates rather than tool libraries by themselves. They are included because OpenAPI specifications are a common upstream carrier for tool registration.

## Framework Tools

Framework-tool records come from agent frameworks, integrations, or tool libraries. They represent tools that are already close to agent runtime usage.

## Tool Benchmarks

Tool benchmark records come from datasets built for tool-use or API-use evaluation. They often contain tool or operation descriptions, parameters, and usage metadata.

## Function-Calling Datasets

Function-calling records contain model-visible function declarations used for function-call generation research. They are included as a related form of tool declaration metadata.

## Why Multiple Sources

Using multiple source families reduces the risk that the dataset reflects only one tool ecosystem. It also enables source-aware analysis, cross-source generalization experiments, and construction of balanced subsets.

