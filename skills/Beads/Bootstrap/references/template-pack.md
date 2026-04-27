# Template pack

These are starter shapes for repo-local workflow files.

They are intentionally concise. Adapt them to the repo instead of copying blindly.

## Default template shape (`T2`)

### Root `CLAUDE.md`

Use when:
- the repo is active and another agent session could plausibly join
- multiple agents may work in the same repo over time
- repo needs stronger startup reconstruction
- architecture and package authority should be explicit

Suggested content:

```md
# <repo-name>

Brief repo identity and architecture.

## Session Bootstrap

Read `AGENTS.md` after this file.

- Beads is the task ledger and durable shared memory.
- Use `main` (or equivalent) for merged code truth.
- Local memory/handoff files are convenience only unless explicitly stated otherwise.
- If Claude hooks are installed, let `bd prime` inject current Beads context automatically.

## Beads Conventions

- Beads is the task authority for this repo.
- Create self-contained beads at creation time.
- Use `bd create --description` for what/why, `--context` for execution detail, and `--notes` for `SOURCES:` plus `kn entry:`.
```

### Root `AGENTS.md`

Suggested content:

```md
# AGENTS.md

## Read Order

1. `CLAUDE.md`
2. `AGENTS.md`
3. nearer nested `AGENTS.md` if relevant
4. relevant docs
5. `bd dolt pull || true` when the repo uses a Dolt remote
6. `bd ready --json`
7. open PRs if overlap is likely

## Workflow

- `bd ready --json` before choosing work
- `bd show <id> --json` before implementation
- `bd update <id> --claim --json` before starting
- `bd comment <id> "..." --json` for concurrent observations
- `bd note <id> "..." --json` for consolidated durable summaries
- `bd create --title="..." --description="what and why" --context="file paths, commands, current state" --notes="SOURCES: <url or internal origin>. kn entry: <filename or none>" --json` for follow-up work
- decompose clearly multi-step epics into child beads immediately, with explicit `bd dep` links and a parent decomposition note
- `bd remember "..." --key <name> --json` for durable repo facts
- `bd close <id> --reason "..." --json` only on real completion
- `bd dolt pull || true` at session start when the repo uses a Dolt remote
- `bd dolt push` before ending the session unless the repo is intentionally in stealth / no-git-ops mode
- use `bd dep` for real sequencing
- use `bd gate` for real waits
- use worktrees for concurrent agents when file ownership may overlap

## Optional but useful

- `bd blocked` to inspect waits
- `bd worktree create <name>` for parallel execution
- `bd stale`, `bd orphans`, `bd duplicates` for maintenance cadence

## Memory Model

- Beads = task state and durable repo memory
- integration branch = merged truth
- local memory/handoff files = convenience only
```

Default T2 guidance:
- treat concurrent-agent safety as normal repo policy, not an edge case
- keep worktree / gate / sync expectations explicit
- use nested `AGENTS.md` only for real subproject divergence

## Exception template shape (`T1`)

### Root `CLAUDE.md`

Use when:
- the repo is explicitly solo or local-planning-only
- one main working surface exists
- no strong need for nested workflow files yet

Suggested content:

```md
# <repo-name>

Brief architecture and where the real public/package truth lives.

## Session Bootstrap

After reading this file, load `AGENTS.md`.

- Reconstruct current state from Beads, `main`, and open PRs.
- If a nearer nested `AGENTS.md` exists, read that next.
- Local memory/handoff files are non-authoritative convenience only.

## Beads Conventions

- Beads is the task authority for this repo.
- New beads must be self-contained at creation time with `--context` and provenance notes.
```

### Root `AGENTS.md`

Suggested content:

```md
# AGENTS.md

## Read Order

1. `CLAUDE.md`
2. `AGENTS.md`
3. relevant docs
4. `bd ready --json`

## Authority

- Beads = task state and durable shared memory
- `main` = merged truth
- open PRs = in-flight work
- repo docs = workflow rules

## Workflow

- `bd ready --json`
- `bd show <id> --json`
- `bd update <id> --claim --json`
- `bd comment ... --json`
- `bd note ... --json`
- `bd create --title="..." --description="what and why" --context="file paths, commands, current state" --notes="SOURCES: <url or internal origin>. kn entry: <filename or none>" --json`
- if an epic is clearly multi-step, create child beads immediately, wire them with `bd dep`, note the decomposition on the parent, and push the new structure
- `bd remember ... --json`
- `bd close ... --json` on real completion
- `bd dolt pull || true` at session start when the repo uses a Dolt remote
- `bd dolt push` before session end

## Optional but useful

- `bd dep <blocker> --blocks <blocked>` for real sequencing
- `bd blocked` to inspect waits
```

T1 guidance:
- keep it short
- allow `bd dep` even in T1
- do not add heavy multi-agent policy unless the repo explicitly wants it

### Nested `AGENTS.md`

Add only where a subproject has:
- different validation commands
- different public-surface authority
- different docs/read order

## T3 template shape

### Root `CLAUDE.md`

Use when:
- Claude is one surface in a broader crew/orchestrated environment
- repo needs explicit note that local machine behavior is subordinate to repo orchestration rules

Suggested content:

```md
# <repo-name>

Architecture, repo boundaries, and system role.

## Session Bootstrap

Read `AGENTS.md` immediately after this file.

- Beads is the shared task/memory layer.
- `main` and open PRs are code truth surfaces.
- Local Claude memory/handoff is convenience only.
- Machine hooks must not override repo workflow.

## Beads Conventions

- Beads is the shared workflow authority.
- Create self-contained beads at creation time via description + `--context` + provenance notes.
```

### Root `AGENTS.md`

Suggested content:

```md
# AGENTS.md

## Read Order

1. `CLAUDE.md`
2. `AGENTS.md`
3. nearer nested `AGENTS.md`
4. relevant docs
5. `bd ready --json`
6. routing / multi-repo context if relevant
7. open PRs / merge queue

## Operating Model

- Beads is the workflow authority
- use routing / hydration rules explicitly
- define whether repo is contributor/team/server/federated
- define whether molecules/messages/role beads/convoys are in use

## Required Commands

- `bd ready --json`
- `bd show --json`
- `bd update --claim --json`
- `bd dep`
- `bd gate`
- `bd remember --json`
- `bd close --json`
- `bd dolt pull || true`
- `bd dolt push`

## Additional T3 Policy

- routing.mode expectations
- repos.additional expectations
- server/shared-server expectations if applicable
- federation boundaries if applicable
- role/message/convoy usage only where explicitly in use
```

T3 guidance:
- be explicit
- do not assume every advanced Beads feature is active
- name the advanced features that are truly in use

## Upgrade rule

Design `T1` so it upgrades cleanly:
- same issue lifecycle
- same Beads authority model
- same startup discipline
- add coordination layers, do not rewrite fundamentals
