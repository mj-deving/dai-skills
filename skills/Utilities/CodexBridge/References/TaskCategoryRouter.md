# Task Category Router

Use this table to classify a user request before invoking Codex. Pick one primary category.

## Categories

| Category | Trigger Vocabulary | Required Response Shape |
|---|---|---|
| Plan | plan, architecture, design, strategy, sequence | milestones, risks, dependencies, acceptance criteria |
| Build/Implement | build, implement, create, develop | code changes, tests, verification commands |
| Debug | debug, investigate, root cause, why failing | reproduction, root cause, fix candidates |
| Fix/Bug | bugfix, patch, hotfix, broken | minimal patch, regression tests |
| Refactor | refactor, cleanup, simplify, restructure | behavior-preserving diff + rationale |
| Review | review, audit, critique | findings first, severity ordering, file refs |
| Test Engineering | tests, coverage, test gaps | test matrix + added test cases |
| Performance | optimize, perf, latency, memory | bottlenecks, measurements, optimization plan |
| Security | security, auth, token, secret, harden | vulnerabilities, impact, remediations |
| Dependencies | upgrade, dependency, package, lockfile | compatibility risks + upgrade sequence |
| CI/CD | ci, workflow, pipeline, deploy checks | pipeline changes + reliability notes |
| Data/Schema | migration, schema, database, backfill | migration path + rollback strategy |
| API/Contract | api, endpoint, interface, contract | contract diff + compatibility guidance |
| Docs | docs, readme, guide, documentation | doc updates consistent with code behavior |
| Codegen | scaffold, boilerplate, generator | generated files + usage/test stubs |
| Multi-repo | multi repo, cross repo, integration | per-repo deltas + ordered rollout |
| Static Analysis | lint, typecheck, static analysis | categorized issues + safe fixes |
| Release Readiness | release, go/no-go, launch check | blockers, risks, checklist |
| Incident/Production | prod issue, incident, outage | triage, containment, remediation plan |
| Machine JSON | json, machine-readable, schema output | strict JSON only (no markdown) |

## Wrapper Selection

- Use `codex-plan-review.sh -p <plan.md> -r <repo>` for plan-file reviews.
- Use `codex-json.sh -r <repo> -s <schema> "<prompt>"` for machine-readable outputs.
- Use `codex-call.sh -r <repo> "<prompt>"` for all other categories.

## Tie-Break Rule

If multiple categories match:
1. Choose the highest-risk category as primary (security > prod incident > data/schema > others).
2. Include secondary requirements explicitly in the prompt.
3. Keep output contract of the primary category.

