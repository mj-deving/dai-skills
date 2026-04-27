# Review Workflow — Structured Code Review

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the Review workflow in the CodeReview skill to evaluate code changes"}' \
  > /dev/null 2>&1 &
```

Running **Review** in **CodeReview**...

---
-->

## Process

### Step 1: Understand the Change

Before reviewing, understand context:

```bash
# What changed?
git diff --stat HEAD~1
git log --oneline -3

# What was the intent?
# Read the PR description, commit message, or ask the author
```

### Step 2: Review Tests First

Tests reveal intent. Read them before the implementation:

- What behavior do the tests assert?
- What edge cases are covered?
- What's NOT tested (gaps)?

If there are no tests for new behavior → **Important** finding.

### Step 3: Walk Through the 5 Axes

For each changed file, evaluate:

1. **Correctness** — Does it do what the tests/spec say?
2. **Readability** — Can I understand it without the author explaining?
3. **Architecture** — Does it fit the patterns here?
4. **Security** — Any untrusted input handling?
5. **Performance** — Any obvious bottlenecks?

### Step 4: Classify Findings

For each issue found:

```markdown
**[SEVERITY]** file.ts:42 — Description
Suggestion: [what to do instead]
```

Example:
```markdown
**[Critical]** auth.ts:15 — Password compared with === instead of timing-safe comparison
Suggestion: Use `crypto.timingSafeEqual()` to prevent timing attacks

**[Important]** api.ts:88 — Missing validation on user input before DB query
Suggestion: Add Zod schema validation at the handler boundary

**[Nit]** utils.ts:23 — Variable name `d` is unclear
Suggestion: Rename to `dateOffset` or `daysDelta`

**[FYI]** Nice use of the discriminated union pattern in types.ts:50-65
```

### Step 5: Summarize

```markdown
## Review Summary

**Verdict:** [Approve / Request Changes / Needs Discussion]

**Critical:** [count] — [brief list]
**Important:** [count] — [brief list]
**Nit:** [count]

**Positive:** [what's done well — always include this]
```

---

## When NOT to Review

- Don't review auto-generated code (lock files, build output)
- Don't review formatting-only changes (trust the formatter)
- Don't review import reordering unless it changes behavior
- Don't block on style preferences that aren't in the project's conventions
