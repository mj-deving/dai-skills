---
name: beads
description: Beads operating system for repo and machine workflow. USE WHEN Beads, beads bootstrap, beads upgrade, beads hooks, beads topology, beads formulas, beads recovery, beads research, or making Beads foolproof across sessions and repos.
---

# Beads

Use this as the default Beads skill.

Current doctrine is version-aware for `bd 1.0.x`:
- use `bd bootstrap --dry-run` / `bd bootstrap --yes` to adopt or repair existing shared repo state
- do not use `bd init --force` for shared-repo recovery; inspect `bd init-safety` instead
- use explicit `bd dolt pull` / `bd dolt push`; there is no current `bd sync` command
- use `bd comment` for concurrent observations and `bd note` for consolidated issue summaries
- use `bd batch` for scripted multi-bead mutations

The other Beads skills are implementation details:
- `Bootstrap/SKILL.md` for repo-local adoption and alignment
- `UpgradePath/SKILL.md` for tier/doctrine upgrades in repos that already use Beads
- `HookAudit/SKILL.md` for machine-level Claude hook repair
- `VersionAudit/SKILL.md` for live backend/remotes/hooks/drift inspection
- `TopologyPlanner/SKILL.md` for choosing the right collaboration topology
- `FormulaBuilder/SKILL.md` for recurring workflow templates and formulas
- `EvidenceTriage/SKILL.md` for evidence-first issue creation
- `RecoveryAudit/SKILL.md` for backup/sync/lock recovery rehearsal
- `Research/SKILL.md` for source-grounded doctrine and current-versus-historical guidance
- `Workflows/MigrateRepo.md` for applying current Beads doctrine to one repo
- `Tools/AuditRepos.sh` for scanning many repos before rollout

Outcome rule:
- using this skill should leave the relevant repo or machine Beads-clean when safe, not make the user remember which Beads sub-skill to invoke
- choose the smallest combination of bootstrap, upgrade, and hook repair that reaches doctrine hygiene directly
- leave manual follow-up only when blocked by permissions, credentials, or a genuinely risky coordination window
- when repo-local doctrine is in scope, make sure issue creation defaults produce self-contained beads at creation time: description for what/why, `--context` for execution details, and `--notes` for source provenance
- when a bead is clearly an epic or multi-step work package, default to immediate child decomposition with explicit dependencies rather than leaving the execution plan implied in prose
- prefer evidence-first beads over vague reminders: repro, observed behavior, likely fix surface, and acceptance criteria beat generic TODO phrasing
- treat stale epics and disproven theories as first-class cleanup work: close or supersede them explicitly instead of letting the queue rot

## Routing

Start with a quick audit of the current repo and, when relevant, machine hook state.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Repo bootstrap, Beads adoption, Beads alignment, initialize Beads in a repo | `Bootstrap/SKILL.md` |
| Tier upgrade, T1 to T2, T2 to T3, repo Beads model evolution | `UpgradePath/SKILL.md` |
| Claude hooks, SessionStart, PreCompact, hook repair, machine Beads behavior | `HookAudit/SKILL.md` |
| Backend drift, remotes, legacy JSONL, current Beads posture audit | `VersionAudit/SKILL.md` |
| Embedded versus server mode, clone strategy, collaboration topology | `TopologyPlanner/SKILL.md` |
| Workflow formulas, rollout templates, reusable Beads graphs | `FormulaBuilder/SKILL.md` |
| Evidence-first bug beads, repro capture, issue quality | `EvidenceTriage/SKILL.md` |
| Backup, restore, sync rehearsal, lock recovery, failure drills | `RecoveryAudit/SKILL.md` |
| Current docs, mixed-era drift, senior-user doctrine, source-grounded research | `Research/SKILL.md` |
| Migrate this repo to current Beads doctrine, apply Beads SOTA to another repo | `Workflows/MigrateRepo.md` |
| Audit many repos, fleet rollout, batch repo scan, Beads migration inventory | `Tools/AuditRepos.sh` |

### Route to `Bootstrap`

Use when:
- `.beads/` is missing
- repo-local `AGENTS.md` / `CLAUDE.md` are missing or clearly drifted
- the repo needs initial Beads adoption or canonical workflow alignment

### Route to `UpgradePath`

Use when:
- the repo already uses Beads
- the main question is tier/doctrine fit rather than initial setup
- the repo likely belongs in `T2` or `T3` and current docs underfit that

### Route to `HookAudit`

Use when:
- the user mentions hooks, global defaults, Claude startup behavior, or machine-level Beads behavior
- repo-local doctrine depends on healthy Claude hook behavior
- the user wants Beads made foolproof across sessions, not just inside one repo

### Combined default

If the request is generic, use this order:
1. fix repo-local hygiene first
2. repair machine hooks if they are in scope or clearly undermining repo doctrine
3. apply tier/doctrine upgrades if the repo already uses Beads but is on the wrong operating model

Default scope rules:
- `make Beads work in this repo` => repo-local only unless machine drift is clearly in the way
- `make Beads foolproof` or `standardize my Beads workflow` => repo-local plus machine hook audit
- `upgrade this repo's Beads workflow` => repo-local upgrade, not machine changes, unless hook drift blocks the target behavior
- repo-local hygiene includes creation-time bead quality; do not leave repos on a workflow where `bd create` produces hollow tasks that need a later enrichment pass

## Minimal audit

Use only what is needed to route correctly:

```bash
pwd
git rev-parse --show-toplevel
test -d .beads && echo ".beads exists" || echo ".beads missing"
bd version
bd context --json || true
bd bootstrap --dry-run || true
find . \
  -path './.git' -prune -o \
  -path './.claude/worktrees' -prune -o \
  \( -name AGENTS.md -o -name CLAUDE.md \) -print
bd ready --json || true
sed -n '1,220p' ${AGENT_HOME}/settings.json 2>/dev/null || true
```

Then choose the minimum justified route and do the work directly.

If repo-local doctrine is changed or aligned, verify it mechanically with:

```bash
python3 ${PAI_EXTENSIONS_DIR}/skills/Beads/Bootstrap/scripts/check_beads_doctrine.py --path .
```

When restructuring an epic into child beads, use this default sequence:
1. create the parent epic with full description, context, acceptance, and provenance
2. create child beads immediately when the execution steps are already clear
3. give each child bead its own description, execution context, acceptance criteria, and provenance notes
4. wire dependencies explicitly with `bd dep` instead of leaving order only in prose
5. leave a decomposition note on the parent listing the child IDs and intended sequence
6. run `bd dolt push` after the bead-tree restructure so the new plan is shared durably

## Verification

Verify only the surfaces touched:
- repo-local changes: `bd ready --json`, `git diff --check`, relevant `AGENTS.md` / `CLAUDE.md`
- hook changes: `bd setup claude --check`, `grep` or `sed` over `${AGENT_HOME}/settings.json` and referenced hook files
- shared repo setup: `bd dolt remote list`, `bd dolt pull || true`, `bd dolt push`

Report:
- which sub-skill logic was used
- what was changed
- what was deliberately left alone
- any residual manual step and why it could not be automated safely
