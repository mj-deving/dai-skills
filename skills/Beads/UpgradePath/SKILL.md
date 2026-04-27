---
name: beads-upgrade-path
description: Audit and safely upgrade a repo's Beads operating tier. USE WHEN evolve Beads workflow, move T1 to T2, move T2 to T3, add multi-agent coordination, add routing or orchestration, or confirm that no upgrade is justified.
---

# Beads Upgrade Path

Use this skill when a repo already has Beads workflow and the question is whether it should stay put or move up a tier.

Outcome rule:
- using this skill should result in tier/doctrine hygiene for the repo, not just a narrated upgrade plan
- if the upgrade is justified and safe, apply the smallest necessary repo-local changes directly and verify them
- only stop at a recommendation when the repo should intentionally stay put, or when permissions/coordination risk make direct application unsafe

References:
- `${HOME}/.claude/PAI/BEADS_ADOPTION.md`
- `${PAI_EXTENSIONS_DIR}/skills/Beads/Bootstrap/references/tiers.md`
- [references/upgrade-checklist.md](references/upgrade-checklist.md)

## Core rule

Do not upgrade just because advanced features exist.

Upgrade only when the current operating model has a real mismatch.

## Quick start

```bash
pwd
git rev-parse --show-toplevel
find . \
  -path './.git' -prune -o \
  -path './.claude/worktrees' -prune -o \
  \( -name AGENTS.md -o -name CLAUDE.md \) -print
test -d .beads && echo ".beads exists" || echo ".beads missing"
bd version
bd context --json || true
bd bootstrap --dry-run || true
bd ready --json || true
gh pr list --state open || true
```

Then read the repo workflow files and determine the current tier.

## Ask only if needed

At most:
1. Are multiple agents expected to work concurrently here?
2. Are multi-repo routing, orchestration, or federation actually needed?
3. Should the upgrade include machine-level Claude hook changes, or repo-local workflow only?

## Upgrade logic

### `T1 -> T2`

Upgrade when:
- multiple agents are active or expected
- PR-first workflow exists or should exist
- sequencing and waits should become repo policy instead of operator habit

Typical changes:
- strengthen root `AGENTS.md`
- clarify `CLAUDE.md` session bootstrap
- introduce explicit `bd dep` and `bd gate` rules
- document worktree policy
- document merge-slot policy if hot files exist
- add maintenance cadence

Do not add unless needed:
- routing
- federation
- crew/orchestration features
- server mode

### `T2 -> T3`

Upgrade when:
- contributor vs maintainer routing is needed
- multiple repos should hydrate into one working view
- orchestration features are real, not hypothetical
- repeated workflows justify molecules/wisps
- independent workspaces or orgs truly need federation

Typical changes:
- add explicit routing/storage/orchestration sections to `AGENTS.md`
- document which advanced features are truly in use
- choose the smallest needed set:
  - routing
  - `repos.additional`
  - `--contributor` / `--team`
  - molecules/swarm
  - message/role/convoy patterns
  - federation peers

Avoid:
- `bd init --quiet --server` without true multi-writer need
- federation because it sounds advanced
- role/message/convoy beads without a real control plane

## Upgrade invariants

Across all tiers, keep stable:
- Beads is task authority
- local memory is non-authoritative unless repo says otherwise
- close tasks only on real completion / merge / supersession
- `bd bootstrap --dry-run` for uncertain identity, `bd ready --json`, `bd show --json`, `bd update --claim --json`, `bd comment --json`, `bd note --json`, `bd remember --json`, `bd close --json`, plus explicit `bd dolt pull` / `bd dolt push` remain core
- `bd note` is for durable consolidated state; `bd comment` is safer for concurrent per-agent observations
- `bd batch` is the preferred primitive for scripted multi-bead create/update/close/dep operations

Upgrade by adding layers, not rewriting fundamentals.

## Validation

```bash
find . \
  -path './.git' -prune -o \
  -path './.claude/worktrees' -prune -o \
  \( -name AGENTS.md -o -name CLAUDE.md \) -print
bd ready --json || true
gh pr list --state open || true
git diff --check
```

Then report:
- current tier
- recommended tier
- whether upgrade is justified
- exact files or rules to change
- advanced features added
- advanced features deliberately left out
- why this is the smallest justified upgrade
