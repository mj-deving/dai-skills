# Triage Workflow — 6-Step Bug Fixing

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the Triage workflow in the Debugging skill to systematically fix a bug"}' \
  > /dev/null 2>&1 &
```

Running **Triage** in **Debugging**...

---
-->

## The 6 Steps

### Step 1: Reproduce

**Goal:** Create a reliable way to trigger the bug.

- Write a minimal test case or command that triggers the issue
- If the bug came from a user report, translate it to a reproducible scenario
- If you can't reproduce → switch to NonReproducible workflow

**Evidence required:** "Running X produces Y, expected Z"

### Step 2: Localize

**Goal:** Narrow from "something is broken" to "this specific file/function is wrong."

Techniques:
- **Binary search:** Comment out half the code. Still broken? It's in the remaining half.
- **Stack trace analysis:** Read the FULL trace, not just the top line. The root cause is often in the middle.
- **Git bisect:** If it worked before, `git bisect` to find the breaking commit.
- **Print/log debugging:** Add targeted logging at suspect boundaries.

**Evidence required:** "The bug is in `file.ts:functionName` at line N"

### Step 3: Reduce

**Goal:** Simplify the reproducer to the minimum code that triggers the bug.

- Remove everything that isn't needed to trigger the bug
- This often reveals the actual cause — the bug becomes obvious in a 5-line reproducer
- If the bug disappears when you simplify, the interaction between removed parts is the cause

### Step 4: Fix

**Goal:** Surgical correction of the root cause.

- Fix the **root cause**, not a symptom (see Surface Fix vs Root Cause in SKILL.md)
- Make the **smallest possible change** that fixes the issue
- Don't refactor, don't "improve" surrounding code — that's a separate task

### Step 5: Guard

**Goal:** Ensure this exact bug can never return.

- Write a regression test that fails WITHOUT the fix and passes WITH it
- This is the TDD:ProveIt pattern — invoke `Skill("TDD", "prove-it")` if needed
- The test name should describe the bug: `"should reject empty title on submission"`

### Step 6: Verify

**Goal:** Confirm the fix works and hasn't broken anything else.

```bash
# Run the specific regression test
bun test --filter "the-bug-test"

# Run the full test suite
bun test

# If UI: verify visually
# If API: curl the endpoint
# If CLI: run with the original failing input
```

**Stop-the-Line:** If full test suite has NEW failures after your fix, your fix has side effects. Investigate before committing.
