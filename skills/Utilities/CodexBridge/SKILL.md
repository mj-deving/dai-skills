---
name: CodexBridge
description: Invoke Codex CLI from Claude in a controlled way for plan review, repo audit, codegen, and strict JSON contracts. USE WHEN ask codex, consult codex, codex review, codex json output, run codex, codex plan review, codex audit.
---

# CodexBridge

Routes Claude -> Codex CLI through safe wrappers.

## Default Policy

- Default mode is **safe** (no `--full-auto`).
- `--auto` is required to enable `--full-auto`, and only on explicit user request.
- High-impact execution intent requires `--confirm-risk`.
- JSON mode must validate with `jq` before returning.
- Prompts should bias toward findings-first output and graceful partial results under token pressure.

## Diff Preparation (Mandatory Pre-Flight)

Before sending any diff or code review to Codex:

1. **Check line count.** If the diff or file content exceeds 300 lines, STOP — do not send it as-is.
2. **Split by concern area.** Create focused chunks by directory or logical boundary:
   - `git diff -- src/types/` → types-diff.txt
   - `git diff -- scripts/` → scripts-diff.txt
   - Each chunk should be 200-300 lines max (Codex sweet spot)
3. **Write a prompt file** with an explicit findings-first output contract (see PromptTemplates.md)
4. **Concatenate prompt + focused diff** into a single file:
   ```bash
   cat review-prompt.md types-diff.txt > full-prompt.md
   ```
5. **Pass via `-f`:** `codex-call.sh -C <repo> -f full-prompt.md "Review types changes. Findings-first."`
6. **Run in parallel** — one review per concern area, then merge findings.

**Why this matters:** A 1900-line diff sent as-is causes Codex to exhaust tokens exploring the codebase without producing ANY findings. Focused 200-300 line chunks with explicit output contracts produce severity-ordered tables with file:line refs every time.

## Route Triggers

Route here when user says any of:
- "ask codex"
- "consult codex"
- "codex review"
- "codex json output"
- "run this through codex"

## Task Category Router (Mandatory)

Before invoking Codex, classify the request into one primary category and enforce the matching response contract.

| Category | Typical Trigger Terms | Preferred Wrapper | Response Contract |
|---|---|---|---|
| Plan | plan, design, architecture, strategy | `codex-plan-review.sh` for existing plans, else `codex-call.sh` | Phases, risks, dependencies, acceptance criteria |
| Build/Implement | build, implement, create feature | `codex-call.sh` | Concrete code changes, tests, run/verify steps |
| Debug | debug, investigate failure, root cause | `codex-call.sh` | Repro, root cause, fix options, validation |
| Fix/Bug | fix bug, patch, hotfix | `codex-call.sh` | Minimal safe patch, regression protection |
| Refactor | refactor, clean up, restructure | `codex-call.sh` | Behavior-preserving changes, migration notes |
| Review | review PR, review code, review plan | `codex-plan-review.sh` for plan files, else `codex-call.sh` | Findings first, severity-ordered, refs |
| Test Engineering | add tests, coverage, test gaps | `codex-call.sh` | Test matrix, missing cases, test patches |
| Performance | optimize, speed up, memory, latency | `codex-call.sh` | Bottlenecks, benchmark plan, optimizations |
| Security | security review, harden, secrets/auth risk | `codex-call.sh` | Vulnerabilities, exploitability, prioritized remediations |
| Dependencies | upgrade deps, package update | `codex-call.sh` | Compatibility risks, upgrade order, lockfile impact |
| CI/CD | pipeline, workflow, deployment checks | `codex-call.sh` | CI edits, cache/reliability improvements |
| Data/Schema | migration, schema change, DB | `codex-call.sh` | Migration plan, rollback, compatibility checks |
| API/Contract | endpoint, interface, breaking change | `codex-call.sh` | Contract diffs, compatibility notes, examples |
| Docs | README, guide, docs sync | `codex-call.sh` | Docs patch aligned with real behavior |
| Codegen | scaffold, boilerplate, generate | `codex-call.sh` | Generated structure + usage and test stubs |
| Multi-repo | cross-repo, integration sweep | `codex-call.sh` per repo (or sweep workflow) | Repo-by-repo deltas, ordering, combined summary |
| Static Analysis | lint, type errors, quality sweep | `codex-call.sh` | Categorized findings, safe fix set |
| Release Readiness | release check, go/no-go | `codex-call.sh` | Blockers, risk register, readiness checklist |
| Incident/Production | outage, production issue, incident | `codex-call.sh` | Triage, containment, follow-up actions |
| Machine JSON | json output, structured report | `codex-json.sh` | Valid schema-conformant JSON only |

If multiple categories match, choose the highest-risk category as primary and include secondary category requirements in the prompt.

## Workflows

- Plan review: `Workflows/ReviewPlan.md`
- Repo audit: `Workflows/RepoAudit.md`
- Codegen task: `Workflows/CodegenTask.md`
- JSON contract output: `Workflows/JsonContract.md`
- Multi-repo sweep: `Workflows/MultiRepoSweep.md`


## References

- Prompt templates: `References/PromptTemplates.md`
  Use for consistent review/audit/codegen prompts.
- Task category router: `References/TaskCategoryRouter.md`
  Use for full trigger vocabulary and per-category output expectations.
- Output schemas: `References/OutputSchemas.md`
  Use when `-j` mode is required.
- Failure modes: `References/FailureModes.md`
  Use to recover from invalid JSON, scope drift, and weak prompts.
- Escalation rules: `References/EscalationRules.md`
  Use to decide when to stay safe vs enable `--auto` / `--confirm-risk`.

## Canonical Commands

- Generic call:
  `bash ${CLAUDE_SKILL_DIR}/Tools/codex-call.sh -r <repo> [flags]`

- Plan review:
  `bash ${CLAUDE_SKILL_DIR}/Tools/codex-plan-review.sh -p <plan.md> -r <repo>`

- JSON mode:
  `bash ${CLAUDE_SKILL_DIR}/Tools/codex-json.sh -r <repo> -s <schema-name> "<prompt>"`

## Flags Contract

- `-r, --repo, -C <repo>` target repo (default `PWD`)
- `-f <prompt_file>` append file content to prompt
- `-m <model>` model override
- `-j` strict JSON mode
- `--auto` opt-in full-auto execution
- `-S, --scope <files>` comma-separated list of files Codex may modify (recommended with --auto)
- `--confirm-risk` required for high-impact execution intent

## High-Impact Intent (gate)

The gate looks for explicit execution or exposure intent, for example:
- `git push`, `push this branch`
- `deploy this`, `release this`
- `rm -rf`, `git reset`, `git rebase`
- `migrate database`, `db migrate`
- `print token`, `share secret`, `production deploy`

If detected and `--confirm-risk` is absent:
- Fail with clear message.
