# Beads command matrix

This file is the self-contained command and feature reference for `beads-bootstrap`.

Use it when bootstrapping a repo so you do not need to keep consulting the upstream Beads repo for normal adoption decisions.

## Core model

Beads has three practical operating tiers:
- `T1` standalone agent / local planning
- `T2` coordinated multi-agent repo
- `T3` crew / multi-repo / federated orchestration

Default to `T2` for active repos if another agent session could plausibly join. Use `T1` only for explicitly solo or local-planning contexts. Use `T3` only when routing/orchestration/federation is actually needed.

## Storage / init modes

### `bd bootstrap --yes`

Use for:
- fresh clones of repos that may already have Beads state
- moved machines
- repair after an empty or shadow local database appears
- existing repos where git origin may already carry `refs/dolt/data`

What it implies:
- non-destructive adoption or repair
- auto-detection of `sync.remote`, git-origin Dolt data, JSONL backup, legacy JSONL, or a new empty database when no state exists
- safer default than `bd init --force` for agents

Shared-repo rule:
- run `bd bootstrap --dry-run` first when the current state is unclear
- after bootstrap, verify with `bd context --json`, `bd dolt remote list`, `bd dolt pull`, and `bd show <known-id> --json` when a known bead exists

### `bd init --quiet`

Use for:
- genuinely new repos where no shared Beads identity exists
- explicitly local-only `T1` repos
- first creation of a shared repo before the initial `bd dolt push`

What it implies:
- minting a new Beads identity unless a remote is auto-adopted
- local embedded Dolt backend by default
- no external Dolt server required

Shared-repo rule:
- after first init in a shared repo, run `bd dolt push` before other clones bootstrap
- do not use `bd init --force` / `--reinit-local` to recover a shared repo; inspect `bd init-safety` and prefer `bd bootstrap`

### `bd init --quiet --stealth`

Use for:
- private/local planning on shared repos
- repos where git side effects should be minimized
- non-git or git-light usage
- many `T1` setups

What it implies:
- Beads is local and quiet
- avoid assuming hooks / AGENTS automation should be installed

### `bd init --quiet --contributor`

Use for:
- OSS contributor workflows
- planning that must stay out of upstream PRs
- contributor/maintainer split
- some `T3` setups

Typical companion config:
- `routing.mode=auto`
- contributor planning repo separate from source repo

### `bd init --quiet --team`

Use for:
- shared team planning in a repo or shared planning context
- teams with common work ledger
- some `T3` setups

### `bd init --quiet --server`

Use for:
- true concurrent multi-writer access
- intentionally shared Dolt server infrastructure
- advanced `T3` environments only

Do not use just because it sounds more powerful.

## `T2` command set (default for active repos)

Best for:
- multi-agent work in one repo
- active repos where another agent session could plausibly join
- PR-first workflows
- worktree parallelism
- durable shared repo memory

### Required base commands

```bash
bd bootstrap --dry-run
bd context --json
bd dolt remote list
bd dolt pull || true
bd ready --json
bd show <id> --json
bd update <id> --claim --json
bd comment <id> "progress observation" --json
bd note <id> "durable issue summary" --json
bd create --title="..." --description="what and why" --context="file paths, commands, current state" --notes="SOURCES: <url or internal origin>. kn entry: <filename or none>" --json
bd remember "fact" --key <name> --json
bd memories --json
bd close <id> --reason "completed" --json
bd dolt push
bd batch
bd dep <blocker> --blocks <blocked>
bd blocked
bd gate list
bd gate check
bd worktree create <name>
bd history <id>
bd diff <from-ref> <to-ref>
bd stale
bd orphans
bd duplicates
```

### Situational commands

```bash
bd merge-slot acquire
bd merge-slot release
bd swarm
```

Use these only if the repo actually has:
- hot files / serialized landing risk
- clearly parallelizable epics

### T2 operating defaults

- `embedded mode` first
- adopt or configure a Dolt remote during bootstrap, not later
- repo-local `CLAUDE.md` + strong `AGENTS.md`
- nested `AGENTS.md` only where a subproject diverges
- `bd dep` for real sequencing
- `bd gate` for real async waits
- worktree isolation for concurrent agents
- use `bd comment` for high-frequency cross-agent observations; reserve `bd note` for consolidated issue-level state because it edits the issue row
- explicit session-close sync discipline
- PR-first lifecycle unless the repo clearly defines direct-push
- self-contained issue creation: description for what/why, `--context` for execution detail, `--notes` for provenance

### Usually avoid in T2

- `bd init --quiet --server` unless true multi-writer access is needed
- `bd init --quiet --contributor` / `--team` unless repo structure demands it
- `repos.additional`
- federation
- `bd mail`
- `agent` / `role` / `convoy` issue types unless there is real orchestration

## `T1` command set (exception case)

Best for:
- explicitly solo Claude
- explicitly solo Codex
- one agent at a time by policy, not just by current accident
- local durable task memory

Important:
- `T1` is not "simple mode"
- `T1` can and often should use dependencies when they clarify real sequencing
- the main thing `T1` lacks is repo-wide multi-agent coordination policy

### Required commands

```bash
bd bootstrap --dry-run
bd context --json
bd dolt remote list
bd dolt pull || true
bd ready --json
bd show <id> --json
bd update <id> --claim --json
bd comment <id> "progress observation" --json
bd note <id> "durable issue summary" --json
bd create --title="..." --description="what and why" --context="file paths, commands, current state" --notes="SOURCES: <url or internal origin>. kn entry: <filename or none>" --json
bd remember "fact" --key <name> --json
bd memories --json
bd close <id> --reason "completed" --json
bd dolt push
```

### Common setup commands

```bash
bd bootstrap --yes
bd init --quiet
bd init --quiet --stealth
bd setup claude
bd setup codex
bd setup claude --check
bd setup codex --check
```

Guidance:
- prefer `bd bootstrap --yes` as the primary existing-repo bootstrap path
- use `bd init --quiet` only when intentionally minting new local state
- use `bd setup ... --check` to verify or repair integration drift after bootstrap
- for explicitly solo/local-only repos, a Dolt remote is optional
- for any shared repo, treat missing `bd dolt remote list` output as incomplete bootstrap

### Doctrine checker

After aligning repo-local docs, run:

```bash
python3 ${PAI_EXTENSIONS_DIR}/skills/Beads/Bootstrap/scripts/check_beads_doctrine.py --path .
```

The checker verifies only mechanically provable surfaces:
- root `CLAUDE.md` exists and mentions Beads prominently
- `CLAUDE.md` points readers to `AGENTS.md`
- `CLAUDE.md` encodes creation-time bead context/provenance
- root `AGENTS.md` exists
- `AGENTS.md` read order starts with `CLAUDE.md` then `AGENTS.md`
- `AGENTS.md` includes the core `bd` lifecycle commands

### Useful but optional

```bash
bd dep <blocker> --blocks <blocked>
bd blocked
bd prime
bd stale
bd config drift --json
bd info --json
```

### Usually avoid in T1

- `bd gate`
- worktree / merge-slot policy
- routing
- server mode
- federation
- crew/message features

### Upgrade path from T1 to T2

Keep these stable from the beginning:
- `bd ready --json`
- `bd show --json`
- `bd update --claim --json`
- `bd comment --json` for concurrent observations
- `bd note --json`
- `bd remember --json`
- `bd close --json`
- `bd dolt pull || true`
- `bd dolt push`
- optional `bd dep` where sequencing is real
- self-contained issue creation with `--context` and provenance notes

When upgrading to `T2`, add:
- `bd bootstrap --yes` / remote adoption and verification before shared work starts
- stronger `AGENTS.md`
- PR-first or explicit direct-push coordination rules
- `bd gate`
- worktree policy
- merge-slot policy if needed
- maintenance cadence

## T3 command set

Best for:
- agent crews
- orchestrators
- multi-repo work
- contributor/team routing
- federation or cross-workspace sync

### Routing / multi-repo commands

```bash
bd init --quiet --contributor
bd init --quiet --team
bd config set routing.mode auto
bd config set routing.mode explicit
bd config set routing.maintainer "."
bd config set routing.contributor "~/.beads-planning"
bd config set repos.primary "."
bd config set repos.additional "~/repo1,~/repo2"
bd config get routing.mode
bd info --json
```

### Server / backup / sync commands

```bash
bd init --quiet --server
bd dolt push
bd dolt pull
bd backup init <path>
bd backup sync
bd backup restore --force <path>
bd backup status
```

### Molecule / repeated workflow commands

```bash
bd mol distill <epic-id>
bd mol pour <proto-id>
bd mol wisp <proto-id>
bd mol bond <a> <b>
bd mol squash <id>
bd mol burn <id>
bd swarm
```

### Crew / orchestration commands

```bash
bd mail send <recipient> -s "subject" -m "body"
bd mail inbox
bd mail read <id>
bd mail reply <id> -m "body"
bd state <id> <dimension>
bd state list <id>
bd set-state <id> <dimension>=<value> --reason "why"
```

### Federation commands

```bash
bd federation add-peer <name> <endpoint>
```

Use federation only when:
- independent workspaces or orgs must sync
- one shared repo with worktrees is not enough

### T3 issue types / concepts

Only introduce these when the operating model actually needs them:
- `message`
- `gate`
- `agent`
- `role`
- `convoy`
- `molecule`

## Setup profiles by agent surface

### Hook-enabled Claude

Prefer:
```bash
bd setup claude
bd setup claude --check
```

Guidance:
- keep `CLAUDE.md` lighter
- rely on `bd prime`
- prefer upstream default hooks: `SessionStart` runs `bd prime`, `PreCompact` runs `bd prime --stealth`
- machine-level hooks can inject context
- still keep repo-local files authoritative

### Hookless Codex / AGENTS-based agents

Prefer:
```bash
bd setup codex
bd setup codex --check
```

Guidance:
- put fuller workflow instructions in `AGENTS.md`
- do not assume `bd prime` exists

### Mixed Claude + Codex repo

Preferred pattern:
- `CLAUDE.md` for architecture and bootstrap pointer
- `AGENTS.md` for strong workflow contract
- optional nested `AGENTS.md` for subprojects

## Feature selection cheat sheet

### Use `bd dep` when

- one task truly blocks another
- a hardening sequence has real order
- you want `bd ready` to reflect real execution order

### Use `bd gate` when

- waiting for CI
- waiting for PR merge
- waiting for another bead
- waiting for a human decision

### Use `bd worktree create` when

- multiple agents will work in parallel
- shared Beads state must remain visible

### Use `bd merge-slot` when

- landing conflict-heavy work
- shared hot files create serialization risk

### Use molecules / wisps when

- the workflow repeats often enough to justify structure
- there is a real reusable execution pattern

### Use routing / `repos.additional` when

- one workspace needs visibility into multiple repos
- contributor vs maintainer planning should go to different stores

### Use federation when

- independent databases must sync across towns/orgs/workspaces
- not just because the repo has several agents

## Safe defaults

If uncertain:

- choose `T2` over `T1`
- choose `T2` over `T3`
- choose `bd bootstrap --yes` over `bd init --force` for existing/shared repos
- choose `bd init --quiet` over server mode for new repos
- choose embedded mode over server mode
- choose local repo files over machine-global assumptions
- choose fewer advanced features until the use case proves they are needed
