---
name: n8n
description: Expert n8n workflow development — expression syntax, MCP tools, workflow patterns, node configuration, validation, Code node JS/Python, n8nac code-first development, and code-mode runtime optimization. USE WHEN n8n, n8n workflow, build workflow, n8n node, n8n expression, n8n validation, n8n code node, n8n pattern, n8n MCP, automation workflow, n8n template, webhook workflow, batch processing, n8n agent, n8n javascript, n8n python, workflow architecture, n8nac, n8n-as-code, code-first, workflow.ts, n8nac push, n8nac pull, n8nac init, code-mode, sandbox, token savings, tool consolidation, sibling tools, lazy import.
---

# n8n Workflow Development Skills

7 complementary skills for building production-ready n8n workflows. Sourced from [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) — 525+ nodes, 2,653+ templates analyzed, 10 production patterns.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| n8n expression, curly braces, `$json`, variable syntax, expression error | `n8n-expression-syntax/SKILL.md` |
| n8n MCP, search nodes, validate workflow, manage credentials, audit instance, template library | `n8n-mcp-tools-expert/SKILL.md` |
| Workflow architecture, webhook pattern, batch processing, scheduled task, AI agent workflow, database ops | `n8n-workflow-patterns/SKILL.md` |
| Validate workflow, fix errors, auto-fix, validation profile, error severity | `n8n-validation-expert/SKILL.md` |
| Node configuration, node setup, operation parameters, property dependencies, detail levels | `n8n-node-configuration/SKILL.md` |
| Code node, JavaScript, n8n JS, return format, `$input`, built-in functions, SplitInBatches | `n8n-code-javascript/SKILL.md` |
| Python code node, n8n Python, stdlib only, Python limitations | `n8n-code-python/SKILL.md` |
| n8nac, n8n-as-code, code-first, workflow.ts, push, pull, verify, test, init, GitOps, decorator syntax, Class A/B error | `n8n-n8nac/SKILL.md` |
| code-mode, sandbox, token savings, tool consolidation, isolated-vm, lazy import, sibling tools, MCP runtime, LLM gotchas | `n8n-code-mode/SKILL.md` |

## Recommended Workflow

For building any n8n workflow from scratch:

1. **n8nac Bootstrap** — Read `n8n-n8nac/SKILL.md` for code-first setup (init, GitOps sync)
2. **Pattern** — Read `n8n-workflow-patterns/SKILL.md` to select architecture
3. **Discovery** — Read `n8n-mcp-tools-expert/SKILL.md` for node search + tool usage
4. **Config** — Read `n8n-node-configuration/SKILL.md` for operation-aware setup
5. **Expressions** — Read `n8n-expression-syntax/SKILL.md` for data references
6. **Validate** — Read `n8n-validation-expert/SKILL.md` before deployment
7. **Code Nodes** — Read JS or Python skill only when Code nodes are needed
8. **Code-Mode** — Read `n8n-code-mode/SKILL.md` for sandbox optimization + LLM gotchas

## Critical Gotchas

- **nodeType format**: `nodes-base.slack` (search/validate) vs `n8n-nodes-base.slack` (workflow tools)
- **Webhook body**: `$json.body.name` not `$json.name`
- **Code node return**: Always `[{json: {...}}]` array
- **SplitInBatches**: `main[0]` = once after done, `main[1]` = per batch
