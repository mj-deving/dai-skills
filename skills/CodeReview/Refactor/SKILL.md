---
name: Refactor
description: Lightweight batch refactoring using jscpd, knip, eslint, ast-grep. USE WHEN refactor, scan for duplication, find dead code, unused exports, cleanup session, refactoring pass.
---

# Refactor

Lightweight, transparent, stateless batch refactoring. Four CLI tools you own.

> /refactor is stretching after exercise — quick, transparent, stateless.
> Desloppify is an annual physical — comprehensive, scored, persistent.

## When to Use

| Say This | Gets You |
|----------|----------|
| `/refactor` | Full scan→triage→fix→verify cycle |
| "find dead code" / "unused exports" | knip-focused scan |
| "scan for duplication" | jscpd-focused scan |
| "cleanup session" / "refactoring pass" | Full cycle |

## When NOT to Use

- **Health score / debt audit** → use Desloppify
- **Review a diff** → use /simplify
- **Security scan** → use /security

## Tool Inventory

| Tool | What It Finds | Command |
|------|--------------|---------|
| **knip** 6.1.1 | Dead code, unused exports, unused deps | `npx knip --reporter json` |
| **jscpd** 4.0.8 | Code duplication (cloned blocks) | `npx jscpd --min-lines 5 --reporters json --output .refactor/` |
| **eslint** | Lint violations, deprecation warnings | `eslint . --format json` |
| **ast-grep** 0.42.0 | Structural anti-patterns (AST-level) | `sg scan --rule <rules-dir> --json` |

## Workflow

Route to the scan workflow:

→ `Workflows/Scan.md` — the scan→triage→fix→verify cycle
