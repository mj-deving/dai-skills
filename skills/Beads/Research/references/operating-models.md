# Operating models

## Main finding

Beads is in a documentation transition era.

Current docs and README emphasize a Dolt-backed model with embedded and server modes. Older public docs still describe SQLite, JSONL sync, and related concepts. That means migration, recovery, and topology advice must be version-aware.

## Operational implications

### 1. Storage/backend posture is first-class

Do not assume "Beads" means one architecture.

For real work, first identify:
- whether the repo is using current Dolt-backed Beads
- whether it is embedded or server mode
- whether a Dolt remote is configured
- whether legacy `.beads/issues.jsonl` or other historical state still exists
- whether `bd bootstrap --dry-run` would adopt existing remote state or mint fresh local state

### 2. Topology choice matters as much as task doctrine

The key topologies seen in current docs and DoltHub posts are:
- embedded single clone, single writer
- embedded with shared remote across multiple clones
- embedded with separate remote per clone
- server mode for true multi-writer access
- git worktrees sharing one local embedded database through git common-directory discovery

This is not a minor implementation detail. It changes conflict handling, visibility, and recovery expectations.

### 3. CLI plus hooks is usually the fast path

Older docs explicitly note that MCP has higher context overhead than shell access plus hooks. For power users with local shell access, the efficient path is usually:
- `bd bootstrap --dry-run` / `bd context --json` when identity is uncertain
- `bd prime` at session start
- direct CLI operations during work
- explicit `bd dolt pull` / `bd dolt push` at session boundaries

There is no `bd sync` command in the current installed CLI. If older docs or local skills mention it, translate that guidance to explicit Dolt pull/push.

### 4. Formulas and gates are underused leverage

The formulas docs show the right direction: repeatable workflows should become templates with clear gates, not ad hoc prose runbooks. The most valuable uses are recurring operational flows and bug investigation patterns.

### 5. Comments reduce same-row note conflicts

For concurrent agents, use `bd comment <id> ...` for per-agent observations and reserve `bd note <id> ...` for consolidated issue-level summaries. `bd note` appends to the issue notes field, so multiple remote writers touching the same issue can still create row-level merge conflicts even though IDs are hash-based.

### 6. Recovery should be rehearsed

Because current usage mixes embedded state, Dolt remotes, hooks, and potential legacy remnants, recovery cannot be trusted just because a happy path works once. Disposable-clone rehearsal is part of real production readiness.
