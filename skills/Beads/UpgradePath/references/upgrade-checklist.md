# Upgrade checklist

Use this to decide whether an upgrade is justified.

Default assumption:
- active repos belong in `T2` unless they are explicitly solo/local-planning-only

## T1 -> T2 triggers

Upgrade if any of these is materially true:
- more than one agent works in the repo
- another agent session could plausibly join the repo at any time
- PRs are the merge unit
- tasks overlap in time
- waits/blockers should be explicit
- worktrees are in use or should be
- repo needs a strong shared workflow contract

Typical additions:
- stronger root `AGENTS.md`
- `CLAUDE.md` session bootstrap pointer
- `bd dep`
- `bd gate`
- worktree guidance
- merge-slot guidance if needed
- maintenance cadence

## T2 -> T3 triggers

Upgrade if several of these are true:
- contributor vs maintainer routing matters
- multiple repos should appear in one working view
- repeated workflow graphs justify molecules/swarm
- orchestrator-level message/role/state patterns are real
- independent workspaces or orgs must sync

Typical additions:
- routing config
- repos.additional hydration
- contributor/team/server setup where justified
- molecules/wisps
- messaging / role / convoy only if real
- federation only if truly needed

## Non-triggers

Do not upgrade just because:
- Beads has more features
- the repo is important
- one person wants "future proofing"
- federation sounds advanced
- server mode sounds faster
