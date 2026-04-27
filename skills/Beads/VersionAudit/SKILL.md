---
name: beads-version-audit
description: Audit a repo's live Beads posture before migration or coordination work. USE WHEN verify backend mode, remotes, hooks, legacy drift, or whether a repo is safe to upgrade, share, or recover.
---

# Beads Version Audit

Use this skill before bootstrap, migration, server-mode decisions, or recovery planning.

Outcome rule:
- produce a mechanical audit first
- then explain the operational meaning
- point to the smallest justified remediation path

## Quick start

Run:

```bash
${PAI_EXTENSIONS_DIR}/skills/Beads/VersionAudit/scripts/audit_beads_env.sh
bd version
bd context --json || true
bd bootstrap --dry-run || true
bd config drift --json || true
```

Then use [references/remediation-matrix.md](references/remediation-matrix.md) to interpret the result.

## What to check

- `bd` is installed and responds
- the repo has `.beads/` state
- current ready output is readable
- Dolt remotes exist or do not exist by design
- `bd bootstrap --dry-run` would adopt existing remote state rather than minting a shadow database
- Claude hook posture is healthy when relevant
- legacy JSONL or other historical markers are still present
- lock/process anomalies are visible

## Report shape

Keep the result compact:
- current posture
- drift or risk found
- immediate remediation
- what not to change yet

## Escalation rule

If the audit shows real uncertainty about current architecture, route the user to `beads-research` and cite the current README/docs before making migration claims.
