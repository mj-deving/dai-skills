---
name: n8n-mcp-tools-expert
description: Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nodes, validating configurations, accessing templates, managing workflows, managing credentials, auditing instance security, or using any n8n-mcp tool. Provides tool selection guidance, parameter formats, and common patterns. IMPORTANT — Always consult this skill before calling any n8n-mcp tool — it prevents common mistakes like wrong nodeType formats, incorrect parameter structures, and inefficient tool usage. If the user mentions n8n, workflows, nodes, or automation and you have n8n MCP tools available, use this skill first.
---

# n8n MCP Tools Expert

Master guide for using n8n-mcp MCP server tools to build, validate, deploy, and maintain n8n workflows.

Use this skill before calling any n8n MCP tool. The main job is to choose the right tool, use the right node type format, avoid high-token detail modes unless needed, and validate changes before deployment.

## Fast Path

1. For node discovery, read [`SEARCH_GUIDE.md`](SEARCH_GUIDE.md) and [`ToolSelection.md`](ToolSelection.md).
2. Before passing any `nodeType`, read [`NodeTypeFormats.md`](NodeTypeFormats.md).
3. Before or after configuring nodes, read [`VALIDATION_GUIDE.md`](VALIDATION_GUIDE.md).
4. For workflow create/update/deploy operations, read [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md).
5. If an MCP call fails or looks suspicious, read [`CommonMistakes.md`](CommonMistakes.md).

## Most Used Tools

| Tool | Use when |
|---|---|
| `search_nodes` | Finding nodes by keyword |
| `get_node` | Understanding node operations; default to standard detail |
| `validate_node` | Checking node configuration |
| `validate_workflow` | Checking complete workflow structure |
| `n8n_create_workflow` | Creating workflows |
| `n8n_update_partial_workflow` | Editing workflows incrementally |
| `n8n_deploy_template` | Deploying a template workflow |
| `n8n_manage_datatable` | Managing data tables and rows |
| `n8n_manage_credentials` | Credential CRUD and schema discovery |
| `n8n_audit_instance` | Security and configuration audit |
| `n8n_autofix_workflow` | Auto-fixing validation errors |

## Progressive Loading

Read only the file needed for the task:

| Request shape | Read next |
|---|---|
| Choose MCP tools or find the right node | [`ToolSelection.md`](ToolSelection.md), [`SEARCH_GUIDE.md`](SEARCH_GUIDE.md) |
| Convert between search/validation node types and workflow node types | [`NodeTypeFormats.md`](NodeTypeFormats.md) |
| Avoid known failures, bad payloads, wrong parameter names, or inefficient calls | [`CommonMistakes.md`](CommonMistakes.md) |
| Follow common discovery, validation, or workflow-editing loops | [`UsagePatterns.md`](UsagePatterns.md) |
| Templates, data tables, credentials, or security audit | [`TemplatesDataCredentialsSecurity.md`](TemplatesDataCredentialsSecurity.md) |
| Tool docs, AI agent guide, health check, availability, unified tool reference, or performance | [`SelfHelpAndReference.md`](SelfHelpAndReference.md) |
| High-level do/don't rules and summary | [`BestPractices.md`](BestPractices.md) |
| Detailed search guide | [`SEARCH_GUIDE.md`](SEARCH_GUIDE.md) |
| Detailed validation guide | [`VALIDATION_GUIDE.md`](VALIDATION_GUIDE.md) |
| Detailed workflow-management guide | [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) |

## Core Rules

- Use `search_nodes` before guessing node names.
- Use `get_node` with standard detail by default; do not use full detail unless necessary.
- Use short node types such as `nodes-base.slack` for search, docs, and validation tools.
- Use workflow node types such as `n8n-nodes-base.slack` when creating or editing workflow nodes.
- Validate node configs and whole workflows before deployment.
- Prefer `n8n_update_partial_workflow` for edits instead of replacing full workflows.
- Use validation profiles deliberately: `minimal`, `runtime`, `ai-friendly`, or `strict`.
- Do not ignore auto-sanitization behavior after workflow updates.
- For credentials, inspect schemas and required fields before creating or attaching credentials.
- For security work, use `n8n_audit_instance` and report real findings rather than generic advice.
