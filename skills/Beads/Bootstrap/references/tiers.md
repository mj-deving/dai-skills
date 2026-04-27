# Beads tier model

Use this file to decide which Beads capabilities are justified for a repo.

The goal is to avoid both underfitting and overengineering.

Default stance:
- for active repos, assume `T2` unless the repo is explicitly solo/local-planning-only

## T2 — Multi-agent repo (default)

Best for:
- multiple agents working in one repo
- active repos where another agent session could plausibly join
- PR-first workflow
- shared durable task memory
- worktree-based parallelism
- repos like `demos-agents`

Typical setup:
- embedded mode is usually enough
- `bd bootstrap --yes` to adopt existing shared state, or preserve a proven existing `.beads/`
- configure or adopt the Dolt remote during bootstrap so shared Beads state is replicated before parallel work begins
- `CLAUDE.md` + strong root `AGENTS.md`
- nested `AGENTS.md` where subprojects diverge

Core features:
- `bd dolt pull || true`
- `bd ready --json`
- `bd show <id> --json`
- `bd update <id> --claim --json`
- `bd comment ... --json` for concurrent observations
- `bd note ... --json` for consolidated durable summaries
- `bd remember ... --json`
- `bd memories --json`
- `bd close ... --json`
- `bd dolt push`
- `bd dep` for real sequencing
- `bd gate` for async waits
- worktree guidance
- merge-slot guidance where hot files exist
- maintenance cadence: `bd stale`, `bd orphans`, `bd duplicates`

Use selectively:
- `bd swarm` for clearly parallelizable epics
- molecules only when workflows repeat enough to justify them

Usually avoid:
- federation unless independent workspaces need sync
- server mode unless true concurrent multi-writer access is needed
- crew message infrastructure unless you actually have agent mail/control-plane needs

File guidance:
- `CLAUDE.md` = architecture + session bootstrap pointer
- `AGENTS.md` = workflow authority
- nested `AGENTS.md` = local instruction layer

## T1 — Standalone agent / local planning (exception)

Best for:
- one primary agent at a time by explicit repo intent
- explicitly solo Claude or explicitly solo Codex
- local planning on a shared or external repo
- repos where Beads is mainly task memory, not full orchestration

Important:
- `T1` does **not** mean simplistic
- `T1` may still use dependencies, blocked views, and careful lifecycle discipline
- the difference from `T2` is that parallel multi-agent coordination is not yet a first-class repo concern

Typical setup:
- `bd bootstrap --yes` for existing repos or fresh clones that may already have shared Beads data
- `bd init --quiet` for intentionally new embedded mode
- `bd init --quiet --stealth` when git side effects should be minimized or planning is private
- `bd setup claude` for hook-enabled Claude
- `bd setup codex` or explicit `AGENTS.md` workflow for Codex/hookless agents
- Dolt remote optional only if the repo is intentionally solo/local-only

Core features:
- `bd dolt pull || true`
- `bd ready --json`
- `bd show <id> --json`
- `bd update <id> --claim --json`
- `bd comment ... --json` for concurrent observations
- `bd note ... --json` for consolidated durable summaries
- `bd remember ... --json`
- `bd memories --json`
- `bd close ... --json`
- `bd dolt push`
- optional but often useful: `bd dep`, `bd blocked`, `bd prime`, `bd stale`

Usually avoid:
- federation
- server mode
- contributor/team routing
- messages / role beads / convoys
- molecules unless a repeatable workflow really exists

Easy upgrade path to `T2`:
- keep issue lifecycle the same
- keep Beads as task authority from the start
- add the Dolt remote before parallel/shared work starts
- add `AGENTS.md` depth, worktree policy, `bd gate`, maintenance cadence, and merge-slot rules only when multi-agent coordination becomes real
- avoid local-memory authority patterns that would later need to be removed

File guidance:
- hook-enabled Claude: keep `CLAUDE.md` light, rely on `bd prime`; upstream default hooks are `SessionStart: bd prime` and `PreCompact: bd prime --stealth`
- hookless / mixed: fuller `AGENTS.md`

## T3 — Crew / orchestrated / multi-repo / federated

Best for:
- whole agent crews
- multiple repos with shared or routed work
- independent workspaces or orgs that must sync
- orchestration systems, patrols, surveys, convoys, role beads

Typical setup options:
- `bd init --quiet --contributor` for OSS contributor planning separation
- `bd init --quiet --team` for shared team planning
- `bd init --quiet --server` when multiple concurrent writers truly need direct shared access
- shared-server mode only when you intentionally want one Dolt server serving many projects
- `routing.mode auto|explicit`
- `repos.additional` for multi-repo hydration
- federation peers for cross-workspace or cross-org sync

Advanced features:
- molecules / wisps / bonding for repeatable or long-running workflows
- `message` issue type with `bd mail` and threading
- `agent`, `role`, `convoy`, `gate` issue types for orchestration/state
- role-bead state caching patterns
- contributor/team routing and repo hydration
- federation peers and sovereignty tiers where needed

Warnings:
- do not enable server mode just because it sounds advanced
- do not enable federation unless independent databases really must sync
- do not add messages / role beads / convoys unless there is an orchestrator or real crew control plane

File guidance:
- full explicit `AGENTS.md` for hookless agents and orchestrators
- `CLAUDE.md` remains an overlay, not sole authority
- document routing, storage mode, and multi-repo boundaries explicitly

## Capability selection heuristics

Use the tier and mode that match reality, but default to `T2` for active repos unless the repo is explicitly solo/local-planning-only.

Choose:
- `embedded mode` first
- `server mode` only for true concurrent multi-writer access
- `bd bootstrap --yes` before `bd init` when an existing remote identity may exist
- `--quiet --stealth` when git side effects should be minimized
- `--quiet --contributor` when planning must stay out of upstream PRs
- `--quiet --team` when team planning belongs in the shared repo workflow
- `routing.mode auto` for maintainer vs contributor split
- `repos.additional` when one workspace should see multiple repos
- `federation` when independent workspaces or orgs must sync, not just one repo with multiple worktrees

## Source notes

These recommendations are derived from Beads upstream docs on:
- setup profiles (`docs/SETUP.md`)
- storage modes (`README.md`, `docs/DOLT.md`)
- worktrees (`docs/WORKTREES.md`)
- molecules (`docs/MOLECULES.md`)
- multi-repo routing/hydration (`docs/MULTI_REPO_AGENTS.md`)
- federation (`FEDERATION-SETUP.md`)
- messaging (`docs/messaging.md`)
