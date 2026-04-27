# Escalation Rules

## Default Mode

- Use safe mode first (no `--full-auto`)
- Ask for explicit auto mode request before enabling `--auto`

## High-Impact Gate

`codex-call.sh` blocks explicit high-impact execution intent unless `--confirm-risk` is present.

Examples:
- `git push`, `push this branch`
- `deploy this`, `release this`
- `rm -rf`, `git reset`, `git rebase`
- `migrate database`, `db migrate`
- `print token`, `share secret`, `production deploy`

## Recommended Escalation Ladder

1. Analysis only (safe mode)
2. Structured output (`-j` + schema)
3. Autonomous execution (`--auto --scope 'files'`) for low-risk tasks with explicit file scope
4. High-impact execution (`--auto --confirm-risk`) only on explicit user intent

## Collaboration Rule

When Claude delegates to Codex:
- include concrete objective
- include constraints
- require evidence-backed findings
- return output in deterministic format (JSON when possible)
