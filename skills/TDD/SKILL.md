---
name: TDD
description: Test-driven development — RED/GREEN/REFACTOR cycle, Prove-It Pattern for bugs, test pyramid, coverage strategy. USE WHEN writing tests, TDD, test strategy, prove-it pattern, test pyramid, bug fix testing, test coverage, test-first, write tests, add tests, test plan, testing approach, regression test, coverage checklist.
---

# TDD

Test-driven development skill. Ensures code is written test-first with proper coverage strategy, structured test patterns, and the Prove-It Pattern for bug fixes.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/TDD/`

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WORKFLOWNAME in TDD to ACTION"}' \
  > /dev/null 2>&1 &
```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **TestFirst** | "write tests", "TDD", "test-first", "add tests" | `Workflows/TestFirst.md` |
| **ProveIt** | "prove-it", "bug fix test", "regression test", "reproduce bug" | `Workflows/ProveIt.md` |
| **TestStrategy** | "test plan", "test strategy", "coverage plan", "test pyramid" | `Workflows/TestStrategy.md` |
| **APITesting** | "API testing", "Hurl", "httpx", "endpoint testing", "API assertions", "probe endpoints" | `APITesting/SKILL.md` |

## Quick Reference

**The Cycle:** RED (write failing test) → GREEN (minimal code to pass) → REFACTOR (clean up, tests stay green)

**The Pyramid:** ~80% unit, ~15% integration, ~5% e2e

**The Prove-It Pattern:** For bugs — write a failing test that proves the bug exists, then fix it. The test is your proof.

**The Rule:** "A codebase with good tests is an AI agent's superpower; a codebase without tests is a liability."

## Core Principles

- **Test behavior, not implementation** — assert on outcomes, not internal state
- **Each test verifies one concept** — if it fails, you know exactly what broke
- **Tests must be independent** — no shared mutable state between tests
- **Mock only at system boundaries** — databases, networks, external APIs. Not internal modules.
- **A test that never fails is as useless as one that always fails**

## Test Structure: Arrange-Act-Assert

```typescript
test('should mark task complete when toggled', () => {
  // Arrange — set up preconditions
  const task = createTask({ title: 'Buy groceries', done: false });

  // Act — perform the action
  const result = toggleTask(task);

  // Assert — verify the outcome
  expect(result.done).toBe(true);
});
```

## Test Naming

Names should read like specifications:

```
"[unit] [expected behavior] [condition]"

✓ "toggleTask marks task as done when currently undone"
✓ "parseDate throws on invalid ISO string"
✓ "fetchUser returns null when user not found"

✗ "test1"
✗ "it works"
✗ "toggleTask test"
```

## Coverage Checklist

For every function/component, ensure tests cover:

- [ ] **Happy path** — normal expected usage
- [ ] **Empty/null inputs** — edge case handling
- [ ] **Boundary conditions** — min/max values, off-by-one
- [ ] **Error handling** — what happens when things fail
- [ ] **Concurrency** (if applicable) — race conditions, parallel execution

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Breaks on refactor even when behavior unchanged | Assert on outputs and side effects |
| Snapshot overuse | Tests pass with `--update` without review | Use targeted assertions |
| Shared mutable state | Tests interfere with each other | Fresh setup per test |
| Mocking everything | Tests pass but production breaks | Mock only at system boundaries |
| Testing framework code | Wastes time verifying third-party library | Test YOUR logic only |
| `test.skip` permanently | Hidden debt that never gets addressed | Fix or delete, don't skip |

## Examples

**Example 1: New feature with TDD**
```
User: "Add email validation to the signup form"
→ Invokes TestFirst workflow
→ Write failing tests for valid/invalid emails
→ Implement validation until tests pass
→ Refactor for clarity
```

**Example 2: Bug fix with Prove-It**
```
User: "Users can submit empty titles — fix it"
→ Invokes ProveIt workflow
→ Write test: submit with empty title → expect rejection
→ Verify test fails (confirming the bug)
→ Add validation → verify test passes
```

**Example 3: Test strategy for a new module**
```
User: "Plan the testing approach for the auth module"
→ Invokes TestStrategy workflow
→ Analyze module boundaries, external deps, critical paths
→ Produce test plan with pyramid ratios and priorities
```
