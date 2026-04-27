---
name: beads-bootstrap
description: Audit or initialize repo Beads workflow and files. USE WHEN bootstrap Beads, adopt Beads, standardize Beads workflow, initialize a new repo onto Beads, or verify whether a repo already has mature Beads doctrine.
---

# Beads Bootstrap

Use this skill to bootstrap or align Beads deterministically.

The job is to:
- prove what the repo already uses
- avoid overwriting mature workflow
- initialize only what is missing
- create the right repo-local files
- choose the justified Beads tier and setup mode, defaulting to `T2` when another agent session could plausibly join the repo
- prefer upstream non-interactive defaults so setup is fast and foolproof

Outcome rule:
- using this skill should result in repo-local Beads doctrine hygiene, not a leftover checklist of `bd` commands for another agent to remember
- perform the needed bootstrap/alignment work and verification directly whenever the environment permits it
- only leave manual follow-up steps when blocked by missing permissions, missing credentials, or a genuinely risky coordination window
- adopt high-signal issue doctrine for repos that use Beads seriously: evidence-first task bodies, explicit supersession/closure reasons, and aggressive stale-backlog cleanup

Global doctrine lives in `${HOME}/.claude/PAI/BEADS_ADOPTION.md`, but repo-local workflow always wins.

Use these references:
- [references/tiers.md](references/tiers.md)
- [references/command-matrix.md](references/command-matrix.md)
- [references/repo-templates.md](references/repo-templates.md)
- [references/template-pack.md](references/template-pack.md)
- [references/recommended-conventions.md](references/recommended-conventions.md)
- [scripts/check_beads_doctrine.py](scripts/check_beads_doctrine.py)

## Quick start

First prove repo identity and current state:

```bash
pwd
git rev-parse --show-toplevel
find . \
  -path './.git' -prune -o \
  -path './.claude/worktrees' -prune -o \
  \( -name AGENTS.md -o -name CLAUDE.md \) -print
ls ${AGENT_HOME}/projects/*/memory/* 2>/dev/null | head -3
test -d .beads && echo ".beads exists" || echo ".beads missing"
bd version
bd context --json || true
bd bootstrap --dry-run || true
bd config drift --json || true
bd ready --json || true
gh pr list --state open || true
```

Classify the repo as:
- `mature`
- `partial`
- `new`

Memory classification rules:
- Claude project auto-memory found under `${AGENT_HOME}/projects/*/memory/`: valid memory source, but machine-local and not repo-portable
- no machine-local memory found: treat the repo as having no memory source

Then map it to `T1`, `T2`, or `T3` using the tier reference.

## Contamination guard

Do not trust startup memory until the repo proves itself.

Before making workflow claims:
- prove repo root
- list actual repo `AGENTS.md` / `CLAUDE.md`
- check whether Claude project auto-memory exists under `${AGENT_HOME}/projects/*/memory/`
- inspect `.beads/` and live `bd ready --json`
- infer PR model from repo docs, not from memory

If you mention foreign project names or foreign docs, stop and redo the audit. Claude auto-memory is valid context, but it is never authority over repo-local workflow.

## Ask only the minimum questions

Ask only if the repo is silent and the answer would materially change setup.

Prefer upstream defaults without asking:
- use `bd bootstrap --yes` first when an existing repo or remote may already have Beads data
- initialize with `bd init --quiet` only when intentionally minting a new Beads identity
- use Beads hooks via `bd setup claude` / `bd setup codex`
- treat `bd bootstrap --dry-run` plus `bd context --json` as the primary safety check; use `bd setup ... --check` to verify or repair integration drift
- for active or shared repos, treat bootstrap as incomplete until `bd dolt remote list`, `bd dolt pull`, and a known issue lookup prove the shared ledger is visible
- use `--json` for agent-facing `bd` commands

Use at most these four:
1. Which operating tier is intended: `T1`, `T2`, or `T3`?
2. Which agent surfaces matter here: `Claude hook-enabled`, `Codex/AGENTS`, or `mixed`?
3. Should landing be `PR-first` or `direct push`?
4. Do you want machine-level Claude hook changes too, or only repo-local setup?

## Workflow

### 1. Audit

Determine:
- whether `.beads/` exists
- whether root / nested `AGENTS.md` exist
- whether `CLAUDE.md` exists
- whether Claude project auto-memory exists
- whether machine-local memory exists
- whether workflow is PR-first or direct-push
- whether external memory is being treated as authority

### 2. Choose the mode

Use the tier model and command matrix.

Rules:
- do not reinitialize mature repos
- prefer embedded mode first
- default to `T2` for active repos where another Codex/Claude/agent session could plausibly join
- reserve `T1` for explicitly solo or local-planning-only repos
- choose `T3` only when routing/orchestration/federation is actually needed
- for `T2+` or otherwise shared repos, adopt existing remote state with `bd bootstrap --yes` when present; configure a Dolt remote only when there is no existing shared remote

### 3. Create or align repo-local files

Usually create or update:
- root `CLAUDE.md`
- root `AGENTS.md`
- nested `AGENTS.md` only where a subproject truly diverges

Use the template pack and repo templates instead of inventing file structure from scratch.

If the repo is silent on workflow shape, use the recommended conventions reference as the default pattern set, not as immutable law.

Prominence rule:
- Beads conventions should sit visibly in `CLAUDE.md`, not only in `AGENTS.md`
- `CLAUDE.md` should establish Beads as the task/memory authority and encode the creation-time bead contract
- `AGENTS.md` remains the detailed workflow contract, but `CLAUDE.md` should make the repo's Beads model obvious near session bootstrap

### 4. Establish Beads workflow

Unless the repo already defines something stronger, set these defaults:
- `bd bootstrap --dry-run` before destructive-looking init or recovery work
- `bd bootstrap --yes` for fresh clones, moved machines, or shadow/empty database recovery
- `bd init --quiet` only for a genuinely new local Beads identity
- `bd dolt remote list` as part of bootstrap verification for active/shared repos
- `bd dolt pull || true` at session start when the repo uses a Dolt remote
- `bd ready --json`
- `bd show <id> --json`
- `bd update <id> --claim --json`
- `bd comment <id> "progress observation" --json` for concurrent multi-agent observations
- `bd note <id> "durable summary" --json` for consolidated issue-level state that should appear in `bd show`
- `bd create --title "..." --description "what to do and why" --context "file paths, commands, current state" --notes "SOURCES: <url or internal origin>. kn entry: <filename or none>" --json`
- `bd remember "fact" --key <name> --json`
- `bd close <id> --reason "completed" --json` only on real completion / merge / supersession
- `bd dolt push` at session end unless the repo is intentionally in stealth / no-git-ops mode
- `bd batch` for scripted multi-bead create/update/close/dep operations

Add only the coordination layers justified by tier. Use the command matrix instead of restating the full feature split here.

Issue-creation default:
- every new bead should be self-contained at creation time rather than depending on a second enrichment pass
- put task intent and rationale in `--description`
- put execution detail in `--context`
- put provenance in `--notes` with `SOURCES:` and `kn entry:`
- if there is no external source or kn entry, say so explicitly instead of omitting provenance
- when the work is investigative, write the bead like an engineering brief: include repro steps, observed evidence, likely fix area, and what would falsify the current theory
- prefer exact file paths, commands, run artifacts, and observed outputs over general summaries
- make acceptance criteria concrete enough that a later session can prove the work is done without rereading chat history

Backlog-hygiene default:
- close stale umbrella epics once their child work has been split out or the original framing is no longer useful
- use explicit close reasons such as `completed`, `superseded`, `already implemented`, or `invalidated by better evidence`
- when fresh evidence disproves an earlier theory, update or close the old bead instead of keeping contradictory live tasks in parallel
- if the queue drifts into branch-local reminders or generic memories, either convert them into actionable evidence-backed beads or remove them from tracked state

Tracked-state caution:
- if a repo already tracks legacy `.beads/issues.jsonl`, treat it as historical state, not automatically as the best live backend
- validate old JSONL before trying `bd init --from-jsonl`; schema drift can make legacy snapshots unsafe migration inputs
- avoid mixing durable task tracking with noisy branch-specific "memories" in tracked repo state unless the repo explicitly relies on that model

Epic-decomposition default:
- when an epic is clearly multi-step, decompose it into child beads immediately instead of keeping the plan only in the epic body
- every child bead should include description, execution context, acceptance criteria, and provenance notes
- wire the dependency chain with `bd dep` as soon as the child set is known
- leave a parent note recording the child IDs and the intended sequence
- after creating or rewiring the bead tree, run `bd dolt push` so the new structure is shared

Bootstrap rule:
- `T1` explicitly solo/local-only repos may stay local-only by choice
- `T2` and `T3` repos should not stop at `bd init`; they must prove remote adoption and shared visibility before bootstrap is considered complete
- never use `bd init --force` to recover a shared repo; use `bd init-safety` to understand the refusal and `bd bootstrap --yes` to adopt remote state

### 5. Hook policy

If machine-level Claude setup is in scope, prefer:

```bash
bd setup claude
bd setup claude --check
bd setup codex
bd setup codex --check
```

Good hook behavior:
- `SessionStart`: `bd prime`
- `PreCompact`: `bd prime --stealth`
- local continuity only as convenience

Forbidden:
- auto-close on commit
- auto-close on session end
- local next-step queues injected as authoritative startup context

## Validation

After setup, prove the result from the repo:

```bash
pwd
git rev-parse --show-toplevel
find . \
  -path './.git' -prune -o \
  -path './.claude/worktrees' -prune -o \
  \( -name AGENTS.md -o -name CLAUDE.md \) -print
ls ${AGENT_HOME}/projects/*/memory/* 2>/dev/null | head -3
test -d .beads && echo ".beads exists" || echo ".beads missing"
bd context --json || true
bd bootstrap --dry-run || true
bd dolt remote list || true
bd dolt pull || true
bd ready --json || true
gh pr list --state open || true
python3 ${PAI_EXTENSIONS_DIR}/skills/Beads/Bootstrap/scripts/check_beads_doctrine.py --path .
git diff --check
```

Then state:
- repo classification
- operating tier
- setup/init mode chosen
- files created or changed
- advanced features enabled
- advanced features deliberately left out
- doctrine-check result, including any warnings the checker surfaced
- whether any epic decomposition defaults were added or aligned
