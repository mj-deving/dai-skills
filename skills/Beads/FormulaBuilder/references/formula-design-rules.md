# Formula design rules

## 1. Model the real dependency graph

Do not copy the prose runbook line-by-line if the real graph is simpler.

## 2. Put gates where expensive mistakes happen

Good gate points:
- before a batch rollout
- before promotion
- after repro but before patching a speculative fix
- before recovery actions that can destroy evidence

## 3. Keep templates reusable

Parameterize:
- host names
- branch names
- service IDs
- environment-specific URLs

Do not parameterize away the structure.

## 4. Prefer examples that prove the workflow shape

An example should show:
- parent objective
- child sequence
- one or two dependencies
- one explicit gate

## 5. Dry-run first

Any repeatable workflow pack should explain how to validate the graph before real execution.
