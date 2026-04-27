# Recommended conventions

These are strong default workflow patterns for Beads-enabled repos.

They are **recommended conventions**, not universal Beads law.

Apply them when:
- the repo is silent
- they fit the repo's actual collaboration model
- no stronger repo-local convention already exists

Default assumption:
- for active repos, another agent session could plausibly join, so `T2` coordination rules are the baseline unless the repo is explicitly solo

Do not apply them blindly if the repo already has different, coherent rules.

## 1. One bead = one branch = one PR

Good default for `T2` and many `T3` repos.

Why:
- clean task boundary
- clean audit trail
- easier merge/review state
- fewer hidden mixed-scope changes

Use as default when:
- PRs are the merge unit
- task scope is reasonably contained

Do not force when:
- repo intentionally uses direct-push
- repo intentionally uses stacked PRs
- work is pure local planning with no code landing yet

## 2. PR-first merge model

Good default for:
- multi-agent repos
- reviewable change boundaries
- merge automation

Pattern:
1. claim bead
2. branch from integration branch
3. make one coherent change
4. run smallest relevant validation
5. open PR
6. inspect review / CI
7. merge

If the repo intentionally uses direct-push instead, keep the same Beads coordination discipline without forcing PRs.

## 3. Integration branch as merged truth

Usually:
- `main`

Use the repo's real integration branch, not assumptions from other repos.

## 4. Startup reconstruction before implementation

Good default:
1. read repo `CLAUDE.md`
2. read repo `AGENTS.md`
3. read nearer nested `AGENTS.md` if relevant
4. read relevant package/docs
5. verify the Dolt remote with `bd dolt remote list` when the repo is shared
6. run `bd dolt pull || true`
7. inspect `bd ready --json`
8. inspect open PRs if overlap is likely

This is a strong default for `T2` and `T3`.

Bootstrap convention for shared repos:
- do not leave a shared repo in local-only Beads mode after `bd init`
- add `bd dolt remote add origin ...` immediately
- verify it before parallel work begins

`CLAUDE.md` prominence rule:
- do not hide Beads doctrine exclusively in `AGENTS.md`
- `CLAUDE.md` should explicitly name Beads as task/memory authority near session bootstrap
- `CLAUDE.md` should carry the creation-time bead contract at a high level; `AGENTS.md` can hold the longer command matrix

## 5. Claim before implementation

Default:

```bash
bd show <id> --json
bd update <id> --claim --json
```

Why:
- prevents duplicate work
- makes active ownership visible

## 6. Context and provenance at creation

Default:
- every new bead should be self-contained at creation time
- use the description for what to do and why
- use `--context` for file paths, commands, current state, and execution detail a future session will need
- use `--notes` for provenance with `SOURCES:` and `kn entry:`
- if there is no external URL or knowledge-note file, say `SOURCES: internal/user request/...` and `kn entry: none`

Why:
- avoids a manual second pass to enrich beads
- keeps future sessions from doing archaeology before they can act
- makes `bd show` enough to understand and execute the task

For investigations and bug work, raise the bar:
- include exact repro commands when known
- include observed evidence, not just suspicions
- name the likely fix surface or files when justified by evidence
- write acceptance criteria that would prove the hypothesis or prove it wrong

This is the strongest pattern from high-signal Beads usage in mature repos.

## 7. Immediate epic decomposition when steps are already clear

Default:
- if a bead is clearly an epic or multi-step work package, decompose it into child beads immediately
- do not keep the real execution sequence only inside a long parent description
- give every child bead description, execution context, acceptance criteria, and provenance notes
- wire child dependencies explicitly with `bd dep`
- leave a decomposition note on the parent that lists the child IDs and sequence
- run `bd dolt push` after restructuring the bead tree

Why:
- turns planning into executable queue state immediately
- prevents the parent epic from becoming a prose backlog that other agents must reinterpret
- keeps sequencing queryable instead of implicit

## 8. Note incomplete work in Beads, not only local memory

Default:
- use `bd comment` for per-agent observations during concurrent work
- use `bd note` for consolidated durable summaries that should appear in `bd show`
- use `bd gate` for real waits
- do not rely only on local handoff files

Why:
- keeps wait state queryable for other agents
- avoids turning every observation into a same-row issue-notes conflict
- lets `bd ready` reflect actual execution order

## 9. Close only on real completion

Default:
- close on merge, real completion, or explicit supersession
- not on commit
- not on session end

Close quality matters too:
- use close reasons that explain why the bead stopped being live
- prefer `superseded`, `invalidated by better evidence`, or `already implemented` over vague closure
- when an umbrella epic goes stale, close it and keep active work on the surviving child beads instead of letting dead planning linger

## 10. Sync at session end

Default:
- run `bd dolt push` before ending the session
- if the repo uses a Dolt remote, prefer `bd dolt pull || true` at session start
- in stealth / no-git-ops mode, do not invent a fake sync command; document the repo-specific no-push behavior explicitly
- do not assume hooks replace explicit pull/push unless the repo has proven automation for it

## 11. Smallest relevant validation first

Default:
- do not run the largest test suite reflexively
- choose the smallest meaningful validation for the touched area
- widen validation when risk justifies it

## 12. Worktree isolation for parallel agents

Default:
- separate worktrees for concurrent agents
- disjoint file ownership where practical
- serialize overlapping hot-file work when needed

This should be the normal assumption for active multi-agent repos, not an exotic escalation.

## 13. Merge-slot only for true hot-file contention

Use when:
- multiple agents would otherwise collide during landing
- a repo has a small set of repeatedly conflicted files

Do not introduce merge-slot policy in repos that do not need it.

## 14. Maintenance cadence

Good default for `T2/T3`:
- run stale/orphan/duplicate checks at natural boundaries
- not necessarily every session

Typical boundaries:
- before clearing session state
- after a merged work cluster
- when the queue feels noisy

For active T2 repos, make this part of normal hygiene rather than an occasional cleanup ritual.

When cleaning:
- reset stale backlog aggressively
- remove contradictory live beads after better evidence arrives
- prefer a smaller, sharper queue over preserving obsolete plans for historical comfort

## 15. Local memory as convenience only

Default:
- Beads = task state and durable shared repo memory
- local handoff or machine memory = pointer/index convenience only

Promote this to a repo rule unless the repo explicitly wants something else.

Corollary:
- do not let tracked repo state fill up with branch-specific reminders or generic "memories" that are not actionable tasks
- if historical `.beads/issues.jsonl` exists, treat it as legacy state that may need validation before migration or reuse
