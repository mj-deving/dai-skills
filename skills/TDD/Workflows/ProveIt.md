# ProveIt Workflow — Bug Fix Testing

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the ProveIt workflow in the TDD skill to prove and fix a bug"}' \
  > /dev/null 2>&1 &
```

Running **ProveIt** in **TDD**...

---
-->

## The Prove-It Pattern

For bug fixes: **prove the bug exists with a test BEFORE fixing it.**

The test is your evidence — it fails before the fix (proving the bug is real) and passes after (proving the fix works). No test = no proof.

### Step 1: Write a Failing Test That Reproduces the Bug

```typescript
test('should reject empty title on submission', () => {
  // This test should FAIL right now — that's the bug
  const result = submitTask({ title: '' });
  expect(result.error).toBe('Title is required');
});
```

### Step 2: Run the Test — Verify It Fails

```bash
bun test --filter "empty title"
```

**If the test passes:** The bug is either already fixed, or your test doesn't reproduce it. Investigate further — don't just move on.

**If the test fails:** Good. You've proven the bug exists. Proceed.

### Step 3: Fix the Bug

Apply the minimal fix. Don't refactor, don't "improve" surrounding code.

### Step 4: Run the Test — Verify It Passes

```bash
bun test --filter "empty title"
```

The test that failed in Step 2 must now pass.

### Step 5: Run Full Test Suite — No Regressions

```bash
bun test
```

All existing tests must still pass. If anything broke, your fix has side effects — investigate before proceeding.

### Step 6: Commit

The commit includes both the test AND the fix. They're one logical unit.

---

## When to Use

- Bug reports from users
- Regressions discovered during development
- Flaky behavior that needs to be pinned down
- Any defect where "it works on my machine" is the current state
