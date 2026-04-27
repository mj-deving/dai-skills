---
name: n8n-code-mode
description: Code-mode runtime for n8n — sandboxed TypeScript execution that collapses sequential LLM tool calls into one shot. Architecture, sandbox rules, lazy imports, sibling auto-register, LLM gotchas, and benchmark data. USE WHEN code-mode, code mode, utcp, sandbox, n8n sandbox, toolCode, n8n code execution, token savings, tool consolidation, code-mode-tools, code-mode-core, MCP n8n, sibling tools, auto-register, lazy import, isolated-vm, n8n agent optimization, n8n cost reduction.
---

# Code-Mode — Code-First n8n Runtime

Code-mode collapses sequential LLM tool calls into a single sandboxed TypeScript execution. Instead of an AI agent making 5 serial HTTP-request tool calls (5 round trips, 5x context), it writes one TypeScript block that calls all 5 — executed in a V8 isolate sandbox.

**Benchmark result:** 96% token savings on a 5-tool pipeline (4,847 → 202 tokens).

---

## Architecture

```
@utcp/code-mode (upstream)        @code-mode/core (engine)         Wrappers
──────────────────────          ─────────────────────          ──────────
CodeModeUtcpClient              CodeModeEngine                 n8n community node
  - V8 sandbox (isolated-vm)     - Setup caching (FIFO/16)     - supplyData() thin wrapper
  - UTCP tool registration        - Execution tracing           - Sibling auto-register
  - TypeScript compilation         - External tool composition   - MCP presets UI
                                   - Collision-safe bridges
                                   - Security hardening        MCP server (code-mode-tools)
                                                                - Standalone stdio server
                                                                - tools.json config
```

### Package relationships
```
@utcp/code-mode@1.2.11         <- upstream (raw sandbox + UTCP client)
    wraps
@code-mode/core                 <- production engine (caching, tracing, composition)
    consumed by
n8n-nodes-utcp-codemode@2.1.x  <- n8n community node
code-mode-tools@0.2.x          <- CLI + MCP server (any MCP client)
```

---

## Sandbox Rules (CRITICAL)

n8n Code nodes and code-mode both run in sandboxed environments with strict restrictions.

### n8n toolCode sandbox
- **No `fetch`** — not available in sandbox
- **No `require('http')`** — blocked
- **No `require('fs')`** — blocked
- **Only `this.helpers.httpRequest`** works for HTTP calls
- **`query` variable with `specifyInputSchema: true`** — `query` is an object `{query: "..."}`, not a string. Access via `query.query`
- **Sibling tool args** — use `args ?? {}` not `args || {}` (falsy primitives like `0` or `""` are valid)

### code-mode V8 isolate sandbox
- Runs in `isolated-vm` — separate V8 context, no Node.js APIs
- Tool calls go through registered bridges (MCP, HTTP, sibling)
- TypeScript compiled at setup time, cached via FIFO (16 entries)
- Timeout and memory limits configurable per execution

---

## Lazy Imports (CRITICAL for Windows n8n)

All heavy imports in the n8n node MUST be lazy — `await import()` inside `supplyData()`. Eager top-level imports crash n8n on Windows because `isolated-vm` native addon gets loaded at n8n startup.

```typescript
// WRONG — crashes n8n on Windows
import { CodeModeEngine } from '@code-mode/core';
import { Client } from '@utcp/mcp';
import { z } from 'zod';

// CORRECT — lazy import inside supplyData()
async supplyData() {
  const { CodeModeEngine } = await import('@code-mode/core');
  const { Client } = await import('@utcp/mcp');
  const { z } = await import('zod');
  // ...
}
```

---

## Sibling Auto-Register (v2.1+)

The n8n code-mode node automatically discovers sibling tool nodes connected to the same AI Agent and registers them in the sandbox. The AI agent can call both:
- **MCP/manual tools** registered via `toolSources` config
- **Sibling n8n tool nodes** connected via the n8n canvas

```
[HTTP Request Tool] ─┐
[Calculator Tool]  ──┤── AI Agent ── Code-Mode Tool
[Custom Tool]     ───┘       ↑
                     siblingAdapter.ts converts
                     LangChain DynamicTool → ToolLike[] + CallToolFn
```

Engine API for external tools:
```typescript
const result = await engine.execute(code, {
  externalTools: siblingToolDescriptions,
  externalCallToolFn: callSiblingTool,
});
```

---

## LLM Gotchas for n8n AI Agents

### Model selection
- **Never Sonnet for n8n agents** — $10 burned in 8 tool calls once. Use Haiku max ($0.80/$4 per 1M tokens)
- **Gemini 2.0/2.5 Flash + n8n tools = broken** — sends `null` tool arguments in toolCode. Use Claude Haiku instead
- **OpenRouter model IDs:** `anthropic/claude-haiku-4-5` works. `anthropic/claude-3.5-sonnet` is dead

### n8n LLM node config
- **lmChatOpenAi typeVersion 1** — accepts plain string model IDs
- **lmChatOpenAi typeVersion 1.3** — requires `{ mode: 'list', value: 'model-id' }` object
- **Context overflow** — Haiku's 200k context overflows if agent lists all workflows. System prompt must skip listing

### Credential references
- OpenRouter uses `openAiApi` credential type with custom base URL
- Google Gemini uses `googlePalmApi` credential type
- Always get credential ID from `npx --yes n8nac credential list --json`

---

## MCP Server Setup

code-mode-tools exposes `execute_code_chain` and `list_available_tools` as MCP tools:

```json
{
  "mcpServers": {
    "code-mode": {
      "command": "node",
      "args": ["/path/to/code-mode-tools/dist/index.js"],
      "env": { "TOOLS_CONFIG": "/path/to/tools.json" }
    }
  }
}
```

Works with: Claude Desktop, Claude Code, Cursor, Windsurf, any MCP client.

---

## MCP Tool Sources (Known limitation)

MCP tool sources work in the source repo but spawn **Linux child processes**. When n8n runs on Windows and code-mode spawns an MCP server, it fails because the child process is Linux.

**Workaround:** Use n8n-native `toolCode` with `this.helpers.httpRequest` instead of MCP tool sources when n8n runs on Windows.

---

## Engine API Quick Reference

```typescript
const engine = await CodeModeEngine.create();

// Register tool sources
await engine.registerToolSource({
  name: "fs",
  call_template_type: "mcp",
  config: { mcpServers: { filesystem: { transport: "stdio", command: "node", args: [...] } } }
});

// Execute code in sandbox
const result = await engine.execute(code, {
  timeout: 30000,
  memoryLimit: 128,
  enableTrace: true,           // ToolCallRecord[] with timing
  externalTools: [...],        // v2.1: merge additional tools
  externalCallToolFn: fn       // v2.1: route external tool calls
});

// Get LLM-ready tool description
const description = engine.getToolDescription();

engine.close();
```

---

## Build Commands

```bash
# n8n community node (monorepo)
cd n8n-nodes-utcp-codemode && npm run build && npm test  # 78 tests

# code-mode-tools (CLI + MCP server)
cd code-mode-tools && npm run build && npm test  # 44 tests
```

---

## npm Packages

| Package | Description |
|---|---|
| `n8n-nodes-utcp-codemode` | n8n community node |
| `code-mode-tools` | CLI + MCP server |
| `@code-mode/core` | Platform-agnostic engine (internal) |
