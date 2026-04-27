# Testing Pyramid Decision Framework

Reference for test strategy decisions. Loaded by Desloppify when test-related issues are found.

## Ratio Targets

Adapt to project size — these are starting points, not dogma.

| Layer | Target | Speed | What It Tests |
|-------|--------|-------|---------------|
| Unit | 60-70% | Fast (<10ms) | Isolated logic, pure functions, edge cases |
| Integration | 20-30% | Medium (<1s) | System boundaries, real DB/API, data flow |
| E2E | 5-10% | Slow (seconds) | Critical user paths, full-stack flows |

**Small projects (<5 files):** Shift toward 40/40/20 — integration tests give more confidence per test when the codebase is small enough that unit tests over-mock.

**AI/LLM projects:** Add an evaluation layer alongside unit tests — test output quality, not just function signatures.

## Tool Selection (TypeScript/Bun)

| Layer | Recommended | Alternative |
|-------|------------|-------------|
| Unit | `bun:test` | vitest |
| Integration | `bun:test` + real deps (SQLite, API calls) | vitest + testcontainers |
| E2E | Playwright | Cypress |
| Property-based | fast-check | — |

## Decision Tree

When deciding what type of test to write:

```
Is this pure logic with no side effects?
  → Unit test

Does it cross a system boundary (DB, API, file system, network)?
  → Integration test

Is it a critical user workflow that must work end-to-end?
  → E2E test

Are you testing implementation details (private methods, internal state)?
  → Don't test — refactor to expose behavior instead

Are you testing third-party library behavior?
  → Don't test — trust the library, test your usage of it

Does the input space have subtle edge cases (parsing, encoding, math)?
  → Property-based test with fast-check
```

## Coverage Targets

| Zone | Target | Rationale |
|------|--------|-----------|
| Critical business logic | 90%+ | Bugs here are expensive |
| API endpoints | 80%+ | Contract matters |
| Utilities/helpers | 70%+ | Usually well-isolated |
| UI components | 60%+ | Visual testing supplements |
| Generated/config | Skip | Not your code |

**Do not chase 100%.** Diminishing returns hit hard past 80% overall. The last 20% costs 5x and tests implementation details.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Inverted pyramid** | All E2E, few unit tests | Write unit tests for logic, keep E2E for happy paths |
| **Over-mocking** | Mocks pass, production fails | Use real dependencies in integration tests |
| **Testing implementation** | Tests break on every refactor | Test behavior (inputs → outputs), not internals |
| **100% coverage worship** | Trivial tests, false confidence | Target meaningful coverage, not line count |
| **Flaky E2E** | Tests pass/fail randomly | Add explicit waits, reduce test coupling, use test IDs |
| **No integration tests** | Unit pass, deploy fails | Test the seams — DB queries, API contracts, file I/O |
| **Snapshot overuse** | Approve-all culture, stale snapshots | Use for stable structures only, review diffs carefully |
