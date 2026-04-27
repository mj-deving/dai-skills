# Remediation matrix

Map the audit output to a concrete next step.

## Common outcomes

### `bd` missing

Meaning:
- no reliable Beads operations are possible yet

Next step:
- install or repair Beads before touching repo doctrine

### `.beads/` missing

Meaning:
- repo is not initialized for Beads
- or this checkout has not adopted an existing remote Beads database yet

Next step:
- run `bd bootstrap --dry-run`
- for an existing/shared repo, use `bd bootstrap --yes` and verify `bd context --json`, `bd dolt remote list`, and a known issue lookup
- use `beads-bootstrap`, not migration or destructive reinit workflow

### `.beads/` exists, no Dolt remote, solo repo

Meaning:
- local-only mode may be fine

Next step:
- leave it alone unless multi-agent or multi-machine work is expected

### `.beads/` exists, no Dolt remote, shared repo

Meaning:
- coordination state is not durably shared

Next step:
- run `bd bootstrap --dry-run` to see whether a Git-origin Dolt database can be adopted
- add and verify a remote only if bootstrap cannot adopt existing shared state
- prove the fix with `bd dolt pull`, `bd dolt push`, and a known issue lookup

### legacy `.beads/issues.jsonl` present

Meaning:
- historical state may need validation before import or migration

Next step:
- archive first, then validate against the installed Beads version

### hook check fails

Meaning:
- session-start and sync behavior may be inconsistent

Next step:
- use `beads-hook-audit` or repo-local doctrine cleanup depending on scope
- use `bd config drift --json` for current drift evidence before editing hooks

### lingering `bd` or `dolt` processes, lock symptoms

Meaning:
- embedded mode or local process cleanup may be unhealthy

Next step:
- serialize writes, rehearse recovery, and avoid parallel mutations until the posture is understood

### `bd init --force` suggested by old docs or tooling

Meaning:
- the advice predates the current init-safety contract or is too generic for shared repos

Next step:
- do not run it in a shared repo
- run `bd init-safety` to inspect the contract
- use `bd bootstrap --yes` to adopt remote state when that is the intent

### repeated note conflicts on the same bead

Meaning:
- multiple agents are appending to the issue notes field from different clones before synchronizing

Next step:
- use `bd comment <id> ... --json` for concurrent observations
- have one owner periodically consolidate durable state into `bd note`
- pull/push before and after consolidation
