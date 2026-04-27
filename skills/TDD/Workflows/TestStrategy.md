# TestStrategy Workflow — Test Planning

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the TestStrategy workflow in the TDD skill to plan test coverage"}' \
  > /dev/null 2>&1 &
```

Running **TestStrategy** in **TDD**...

---
-->

## The Test Pyramid

Target distribution for a healthy test suite:

```
        /  E2E  \        ~5%  — Critical user flows only
       /----------\
      / Integration \    ~15% — Cross-boundary behavior
     /----------------\
    /    Unit Tests     \  ~80% — Pure logic, fast, isolated
   /____________________\
```

### Unit Tests (~80%)
- Pure functions, business logic, transformations
- Fast (ms), no I/O, no network
- Mock nothing — if you need mocks, it's not a unit test
- Run on every save

### Integration Tests (~15%)
- Database queries, API handlers, middleware chains
- Test real boundaries (DB, filesystem, HTTP)
- Mock only external services you don't control
- Run on every commit

### E2E Tests (~5%)
- Critical user flows: signup, purchase, core workflow
- Real browser (Playwright), real API, real DB
- Expensive — only for paths where failure = revenue loss
- Run in CI, not on every save

## Planning Process

### Step 1: Map the Module

1. **Identify boundaries** — where does this module talk to external systems?
2. **List public API** — what functions/endpoints does it expose?
3. **Find edge cases** — empty inputs, max values, error states, concurrent access
4. **Check existing coverage** — what's already tested? What's not?

### Step 2: Prioritize

| Priority | What to Test | Why |
|----------|-------------|-----|
| **P0** | Happy path for each public API | Must work or nothing works |
| **P1** | Error handling + boundary conditions | Most bugs live here |
| **P2** | Edge cases (empty, null, max, concurrent) | Prevents subtle regressions |
| **P3** | Performance characteristics | Only if SLAs exist |

### Step 3: Produce Test Plan

```markdown
## Test Plan: [Module Name]

### Unit Tests
- [ ] [function]: happy path — [expected behavior]
- [ ] [function]: empty input — [expected behavior]
- [ ] [function]: boundary — [expected behavior]

### Integration Tests
- [ ] [endpoint/handler]: success response shape
- [ ] [endpoint/handler]: error response on invalid input
- [ ] [query]: returns correct data with filters

### E2E Tests (if critical flow)
- [ ] [user flow]: completes end-to-end
```

## Anti-Patterns to Flag

- **Inverted pyramid** (more e2e than unit) → slow CI, flaky tests
- **No integration tests** (unit + e2e only) → boundary bugs slip through
- **100% coverage target** → tests that assert `true === true` for numbers
- **Snapshot-heavy** → tests that pass with `--update` without review
