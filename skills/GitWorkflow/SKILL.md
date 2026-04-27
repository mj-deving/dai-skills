---
name: GitWorkflow
description: Git workflow and versioning — atomic commits, save point pattern, worktrees for parallel agents, commit conventions, change summaries. USE WHEN git workflow, commit strategy, branching, git conventions, commit message, worktree, parallel work, save point, git bisect, version control, how to commit, when to commit, split commits, act, local actions, test workflow, git-cliff, changelog, release notes.
---

# GitWorkflow

Disciplined version control for AI-assisted development. Rapid AI-generated changes need more git discipline, not less.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/GitWorkflow/`

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WORKFLOWNAME in GitWorkflow to ACTION"}' \
  > /dev/null 2>&1 &
```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CommitStrategy** | "how to commit", "commit strategy", "split commits", "when to commit" | `Workflows/CommitStrategy.md` |
| **DeployChecklist** | "deploy checklist", "pre-deploy", "ready to ship", "deploy verification", "release checklist" | `DeployChecklist/SKILL.md` |

## Atomic Commits

Every commit does ONE logical thing. Size follows from scope — 5 lines or 400 lines, doesn't matter. If a commit does two unrelated things, split it.

**The 5 Principles:**
1. **Commit frequently** — each working increment gets its own commit
2. **Keep commits atomic** — one logical change per commit
3. **Write descriptive messages** — explain WHY, not just WHAT
4. **Separate concerns** — refactoring, formatting, and features are distinct commits
5. **Each commit independently revertable** — reverting one shouldn't break others

## Save Point Pattern

Treat commits as checkpoints:

```bash
# After implementing a piece:
bun test              # or your test command

# If tests pass → commit (save point)
git add -p            # stage intentionally, not -A
git commit -m "feat: add email validation to signup form

Validates format + checks MX record. Rejects disposable domains.
Closes #42."

# If tests fail → investigate or revert
git stash             # or git reset --hard if exploratory
```

**Never commit broken state.** Every commit on main should be a working checkpoint.

## Commit Messages

```
<type>: <what changed> (imperative mood)

<why this change was needed — 1-3 sentences>
<what was intentionally excluded, if anything>

[optional: Closes #issue]
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`

**Good:**
```
fix: prevent duplicate form submission on slow connections

Double-click on submit was creating two entries. Added debounce
on the handler + disabled button during async operation.
Not fixing the retry-on-network-error case — separate issue.
```

**Bad:** `fix stuff`, `update`, `wip`, `changes`

## Worktrees for Parallel Agent Work

When multiple agents need to work on the same repo simultaneously:

```bash
# Create isolated worktree for each agent
git worktree add ../project-agent-1 -b agent/feature-1
git worktree add ../project-agent-2 -b agent/feature-2

# Each agent works in its own directory — no file conflicts
# Merge back to main when done
git worktree remove ../project-agent-1
```

**Rule:** 2+ writing agents on the same repo → worktree isolation. Read-only agents can share.

## Change Summaries

After completing a logical chunk of work, document scope:

```markdown
## Changes
- Added email validation to signup form
- Added MX record checking via dns.resolveMx()

## Intentionally Excluded
- Disposable email blocking (separate feature, needs list maintenance)
- Email verification flow (blocked on SMTP service setup)

## Potential Concerns
- MX lookup adds ~200ms to form submission — acceptable for signup, would be too slow for login
```

## Git Bisect for Bug Hunting

When a regression exists but you don't know which commit caused it:

```bash
git bisect start
git bisect bad                    # current commit is broken
git bisect good v1.2.0            # this version worked
# Git checks out a middle commit — test it
bun test --filter "the-bug"
git bisect good                   # or git bisect bad
# Repeat until bisect finds the breaking commit
git bisect reset
```

Pairs with Debugging:Triage step 2 (Localize).

## Examples

**Example 1: Finishing a feature**
```
User: "I'm done with the auth feature, how should I commit?"
→ Invokes CommitStrategy workflow
→ Reviews staged changes
→ Suggests splitting into: types commit, handler commit, test commit
```

**Example 2: Parallel agent work**
```
User: "I need two agents working on different features"
→ References worktree pattern
→ Creates isolated branches for each agent
→ Merge back when complete
```

**Example 3: Finding a regression**
```
User: "This test was passing last week, now it fails"
→ References git bisect section
→ Binary search through commits to find the breaker
```

## Integration

## Local GitHub Actions Testing (act)

Test GitHub Actions workflows locally before pushing to CI.

```bash
# List available workflows
act -l

# Run default workflow
act

# Run specific workflow
act -W .github/workflows/ci.yml

# Run specific job
act -j test

# Dry run (show what would happen)
act -n
```

**When to use:**
- Before pushing CI changes — validate workflow syntax and logic locally
- Debugging CI failures — reproduce the failure without waiting for GitHub
- New workflow development — iterate fast without push-wait-check cycles

**Tips:**
- Use `-n` (dry run) first to verify job selection before running
- Use `--secret-file .env.ci` to provide secrets for local runs
- `act` uses Docker — ensure Docker is running before invoking

## Automated Changelog (git-cliff)

Generate changelogs from conventional commit history.

```bash
# Generate changelog
git-cliff -o CHANGELOG.md

# Generate for unreleased changes only
git-cliff --unreleased

# Generate with custom config
git-cliff --config cliff.toml -o CHANGELOG.md

# Prepend to existing changelog
git-cliff --unreleased --prepend CHANGELOG.md
```

**When to use:**
- Release prep — generate changelog for the release
- PR descriptions — `git-cliff --unreleased` gives a summary of what changed since last tag
- Ongoing maintenance — prepend unreleased changes to existing CHANGELOG.md

**Pairs with commit conventions:** git-cliff parses conventional commit prefixes (`feat:`, `fix:`, `refactor:`, etc.) — the same format this skill prescribes. Good commit messages produce good changelogs automatically.

## Integration

**Works with:**
- **TDD** — save point pattern: test green → commit
- **Debugging** — git bisect pairs with Triage step 2 (Localize)
- **CodeReview** — reviews evaluate commits, not just code
- **Utilities:Delegation** — worktree isolation for parallel agents
