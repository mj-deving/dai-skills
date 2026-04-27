---
name: beads-recovery-audit
description: Rehearse Beads recovery and drift handling. USE WHEN backup, restore, pull or push, lock cleanup, or mode-transition safety should be audited before trusting Beads operationally.
---

# Beads Recovery Audit

Use this skill when the repo already works well enough on the happy path, but you do not yet trust failure handling.

Outcome rule:
- prefer rehearsal on disposable clones or test repos
- make pass or fail explicit
- leave a short runbook, not hand-wavy reassurance

## Quick start

1. Run:

```bash
${PAI_EXTENSIONS_DIR}/skills/Beads/RecoveryAudit/scripts/recovery_probe.sh
```

2. Read [references/recovery-drill.md](references/recovery-drill.md).
3. Turn the findings into a pass/fail report plus next actions.

## Audit areas

- current repo state capture
- Dolt remote visibility
- backup and restore path
- pull/push behavior
- lock or lingering-process symptoms
- hook posture where relevant
- embedded-versus-server assumptions

## Rule

Do not claim recovery is good because `bd ready` works once. Recovery readiness means the drill is understood and repeatable.
