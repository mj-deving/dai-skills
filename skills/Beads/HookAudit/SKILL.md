---
name: beads-hook-audit
description: Audit and repair Claude-side Beads hook behavior on the local machine. USE WHEN Beads hooks, SessionStart, PreCompact, Stop, PostToolUse, hook doctrine, auto-close risk, or machine-level Beads alignment.
---

# Beads Hook Audit

Use this skill for machine-level Claude hook behavior, not repo-local workflow files.

Outcome rule:
- using this skill should result in machine-level Beads hook hygiene, not a residual checklist of hook commands for another agent to run later
- audit, repair, and verify directly whenever the environment permits it
- only leave manual follow-up when blocked by permissions or by an explicit user decision to defer repair

Doctrine source:
- `${HOME}/.claude/PAI/BEADS_ADOPTION.md`
- [references/hook-policy.md](references/hook-policy.md)

## Scope

Audit and repair:
- `${AGENT_HOME}/settings.json`
- hook files referenced there
- Beads-related `SessionStart`, `PreCompact`, `Stop`, and `PostToolUse` behavior

Do not rewrite repo `CLAUDE.md` / `AGENTS.md` unless explicitly asked.

## Quick start

```bash
sed -n '1,260p' ${AGENT_HOME}/settings.json
grep -nE 'SessionStart|PreCompact|Stop|PostToolUse|bd prime|Beads|handoff|MEMORY' ${AGENT_HOME}/settings.json
sed -n '1,240p' ${AGENT_HOME}/hooks/BeadsAutoClose.hook.ts
sed -n '1,260p' ${AGENT_HOME}/hooks/LoadContext.hook.ts
```

If the machine uses different hook files, inspect those instead.

## Ask only if needed

At most:
1. `audit only` or `audit + repair`?
2. Should local continuity files remain as convenience, or be minimized aggressively?

## Workflow

### 1. Enumerate hook points

Check whether the machine uses:
- `SessionStart`
- `PreCompact`
- `Stop`
- `PostToolUse`

Look for:
- `bd prime`
- context-loading hooks
- auto-close hooks
- handoff / memory injection
- wrapup helpers

### 2. Classify behavior

Use the hook policy reference and label each relevant behavior:
- `good`
- `acceptable but noisy`
- `risky`
- `forbidden`

### 3. Repair only what violates doctrine

Good defaults:
- `SessionStart`: `bd prime`
- `PreCompact`: `bd prime --stealth`
- local continuity loading only as convenience

Forbidden:
- auto-close on commit
- auto-close on session end
- local next-step queues injected as authoritative startup context
- repo-specific workflow assumptions encoded globally

Prefer weakening risky hooks into reminders instead of deleting useful behavior blindly.

## Validation

```bash
grep -nE 'SessionStart|PreCompact|Stop|PostToolUse|bd prime|Beads|handoff|MEMORY' ${AGENT_HOME}/settings.json
sed -n '1,240p' ${AGENT_HOME}/hooks/BeadsAutoClose.hook.ts
grep -nE 'Next steps|Handoff|Local handoff' ${AGENT_HOME}/hooks/LoadContext.hook.ts
```

Confirm:
- `SessionStart` and `PreCompact` still refresh Beads context
- `SessionStart` uses full `bd prime` unless the machine is intentionally configured for a quieter variant
- no hook auto-closes on commit or session end
- local `next_steps` are not injected as authoritative startup context
- local handoff remains clearly non-authoritative

Report:
- hook points found
- files inspected
- risky behaviors found
- exact repairs made
- residual risks if any
