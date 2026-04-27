# NonReproducible Workflow — Flaky & Intermittent Bugs

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the NonReproducible workflow in the Debugging skill to investigate a flaky bug"}' \
  > /dev/null 2>&1 &
```

Running **NonReproducible** in **Debugging**...

---
-->

## When to Use

- Bug doesn't reproduce reliably
- "Works on my machine"
- Flaky tests that pass/fail randomly
- User-reported issue you can't trigger locally

## Stop-the-Line Rule

If you've tried to reproduce **twice** and failed both times → **STOP.**

Don't loop. Instead:
1. Document what you tried and what happened
2. Escalate to {PRINCIPAL.NAME} with your observations
3. Ask for more context: environment, timing, sequence of actions

Infinite reproduction loops waste time and produce no evidence.

## Investigation Playbook

When reproduction fails, investigate indirectly:

### 1. Static Analysis
- Read the code path the bug reportedly follows
- Look for race conditions, shared mutable state, unguarded async operations
- Check for missing null/undefined guards on optional data
- Look for timing-dependent logic (timeouts, debounce, animation frames)

### 2. Recent Changes
```bash
# What changed recently in the affected area?
git log --oneline -20 -- path/to/affected/
git diff HEAD~5 -- path/to/affected/
```

A recent change near the bug location is the most likely cause.

### 3. Environment Differences
- Node/Bun version mismatch?
- Different OS (Linux vs macOS vs WSL2)?
- Different env vars or config?
- Database state (stale data, missing migration)?
- Clock skew or timezone difference?

### 4. Add Targeted Logging
```typescript
// Add temporary logging at the suspect boundary
console.log('[DEBUG] value at checkpoint:', JSON.stringify(value));
```

Deploy with logging, wait for the bug to recur, read the logs. Remove logging after diagnosis.

### 5. Stress Testing
```bash
# Run the flaky test 50 times to find the pattern
for i in $(seq 1 50); do bun test --filter "flaky-test" 2>&1 | tail -1; done
```

If it fails 3/50 times, you have a race condition. If 0/50, the bug is environment-dependent.

## Common Causes of Non-Reproducible Bugs

| Pattern | Symptom | Likely Cause |
|---------|---------|-------------|
| Passes locally, fails in CI | Environment difference | Missing env var, different Node version, no DB |
| Fails every ~5th run | Race condition | Unguarded async, shared state between tests |
| Fails only on first run | Initialization timing | Missing await, lazy init not handling cold start |
| Fails after midnight | Timezone/date logic | Hardcoded dates, timezone-naive comparisons |
| Fails under load | Resource contention | Connection pool exhaustion, file descriptor limits |
