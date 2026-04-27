# TestFirst Workflow

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the TestFirst workflow in the TDD skill to write tests first"}' \
  > /dev/null 2>&1 &
```

Running **TestFirst** in **TDD**...

---
-->

## Process: RED → GREEN → REFACTOR

### Step 1: RED — Write Failing Tests

Before writing any implementation:

1. **Analyze the feature/change** — what behavior needs to exist?
2. **Write tests that assert on that behavior** — these MUST fail initially
3. **Run the tests** — confirm they fail for the right reason (not syntax error)

```bash
# Run tests — expect failures
bun test        # or npm test, pytest, go test, etc.
```

If tests pass immediately, they're not testing anything new. Rewrite.

### Step 2: GREEN — Minimal Implementation

Write the **minimum code** to make failing tests pass:

- Don't write code the tests don't require
- Don't optimize yet
- Don't add "nice to have" features
- Just make the red tests turn green

```bash
# Run tests — expect all green
bun test
```

### Step 3: REFACTOR — Clean Up

With tests green, improve the code:

- Extract duplicated logic
- Improve naming
- Simplify conditionals
- **Run tests after every change** — if anything breaks, revert the last refactor

```bash
# After each refactor step
bun test
```

### Step 4: Commit

Tests green + code clean = commit.

---

## Test Quality Checks

Before moving on, verify:

- [ ] Each test asserts on behavior, not implementation
- [ ] Each test verifies one concept
- [ ] Test names read like specifications
- [ ] Arrange-Act-Assert structure is clear
- [ ] No shared mutable state between tests
- [ ] Mocks only at system boundaries (DB, network, external API)
