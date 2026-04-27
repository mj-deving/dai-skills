# Repo templates

Use these as minimal structure guides, not verbatim boilerplate.

## Root `CLAUDE.md`

Should cover:
- repo identity and architecture
- where the public/package truth lives
- `Session Bootstrap` pointer
- statement that repo `AGENTS.md` defines workflow
- visible Beads conventions near session bootstrap, not buried only in `AGENTS.md`
- the creation-time bead contract: description for what/why, `--context` for execution detail, `--notes` for provenance
- local memory is non-authoritative unless explicitly stated otherwise
- note that upstream Beads hooks can provide `bd prime` context automatically for Claude

Keep it short. Do not turn it into a second workflow manual.

## Root `AGENTS.md`

Should cover:
- read order: `CLAUDE.md`, `AGENTS.md`, nearer nested `AGENTS.md`, relevant docs, `bd ready --json`, open PRs if overlap is likely
- authority model by domain
- Beads commands and lifecycle rules
- issue creation contract: description for what/why, `--context` for execution detail, `--notes` for provenance
- epic decomposition contract: complete child beads, explicit `bd dep` links, parent decomposition note, and post-restructure `bd dolt push`
- branch/PR discipline
- merge/review discipline
- worktree / merge-slot / gate policy as the normal T2 baseline for active repos
- validation ladder

This is the main workflow contract.

## Nested `AGENTS.md`

Create only when a subproject needs local instructions such as:
- different validation commands
- different public-surface authority
- package-local documentation routing

Do not create many nested files unless there is a real instruction boundary.

## Startup model to encode

Safe default:

```text
1. Read CLAUDE.md
2. Read AGENTS.md
3. Read nearer nested AGENTS.md if relevant
4. Read relevant package docs
5. Inspect bd ready --json
6. Inspect open PRs if overlap is likely
```

For active repos, treat this as a `T2` startup model by default, not a special case.

## Memory model to encode

Safe default:
- Beads = task state and durable shared repo memory
- integration branch + open PRs = code truth
- local MEMORY/handoff files = pointer/index convenience only

## Lifecycle model to encode

Safe default:
- claim before implementation
- note during execution
- create follow-up tasks when scope expands, and make them self-contained at creation time
- when an epic is clearly multi-step, decompose it immediately into child beads with explicit dependency structure
- close only on real completion, merge, or supersession
- sync at session end unless the repo is intentionally in stealth / no-git-ops mode
- use `bd gate` for real waits instead of leaving blockers implicit
- prefer worktree isolation when concurrent agents may touch the repo
