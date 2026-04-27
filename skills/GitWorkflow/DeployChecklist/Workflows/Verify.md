# Verify Deploy Readiness

Check current state and produce a go/no-go recommendation.

## Steps

### 1. Check Git Status

```bash
git log --oneline -10
git status
git branch --show-current
```

Report:
- Current branch
- Uncommitted changes (if any)
- Recent commits since last tag/release

### 2. Check for Open Issues

If in a GitHub repo:
```bash
gh pr list --state open --base main
gh issue list --label bug --state open
```

Report:
- Open PRs that should be merged first
- Open bugs that might block deploy

### 3. Review Release Diff

Get the diff of what's about to ship and review it for release risk:

```bash
# Get diff since last tag (or last deploy)
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)
git diff $LAST_TAG..HEAD
```

Report:
- **Critical issues** — bugs, security vulns, race conditions found in the diff
- **Important issues** — performance, error handling gaps
- **Minor issues** — readability, style (note but don't block deploy)

If critical issues are found, flag them as **deploy blockers** in the go/no-go.

### 4. Check Build/Tests

```bash
npm test 2>&1 || echo "TESTS FAILED"
npm run build 2>&1 || echo "BUILD FAILED"
```

Report:
- Test results (pass/fail count)
- Build status

### 4. Produce Go/No-Go

```markdown
## Deploy Readiness: [Service]
**Date:** [Date] | **Recommendation:** GO | NO-GO | CAUTION

### Status
| Check | Status | Notes |
|-------|--------|-------|
| Branch | [main/feature] | [clean/dirty] |
| Code Review | [PASS/WARN/FAIL] | [critical/important/minor issues] |
| Tests | [PASS/FAIL] | [X/Y passing] |
| Build | [PASS/FAIL] | |
| Open PRs | [count] | [any blocking?] |
| Open bugs | [count] | [any critical?] |

### Recommendation
**[GO / NO-GO / CAUTION]** — [One sentence reasoning]

### Blockers (if NO-GO)
- [Blocker 1 — what needs to happen first]
- [Blocker 2]

### Risks (if CAUTION)
- [Risk 1 — what to watch for]
- [Risk 2]
```

### Decision Criteria

- **GO:** All tests pass, build succeeds, no critical bugs, branch is clean
- **CAUTION:** Tests pass but open PRs exist, or minor issues present
- **NO-GO:** Tests fail, build fails, critical bugs open, or uncommitted changes on deploy branch
