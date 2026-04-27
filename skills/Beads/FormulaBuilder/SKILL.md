---
name: beads-formula-builder
description: Build repeatable Beads formulas and workflow packs. USE WHEN recurring operational work should become dependency-aware templates with gates, examples, and dry-run validation.
---

# Beads Formula Builder

Use this skill when a workflow repeats often enough that prose runbooks are no longer good enough.

Outcome rule:
- encode the workflow shape, not every transient detail
- make gates explicit
- leave examples that can be poured or adapted later

## Workflow

1. Read [references/formula-design-rules.md](references/formula-design-rules.md).
2. Load [references/workflow-templates.md](references/workflow-templates.md) for the closest pattern.
3. Identify:
   - the parent outcome
   - child work packages
   - dependency edges
   - human or evidence gates
   - dry-run validation points
4. Produce the formula or template plus one concrete example.

## Design bias

- start with epics and bounded child tasks
- use gates at points where bad automation would be expensive
- keep rollout workflows canary-first
- keep investigation workflows evidence-first

## Validation

Prefer to show how the workflow would be exercised with `--dry-run` or equivalent validation rather than claiming the formula is correct by inspection.
