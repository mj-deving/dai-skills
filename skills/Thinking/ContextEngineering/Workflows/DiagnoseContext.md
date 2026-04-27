# DiagnoseContext Workflow — Context Problems

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the DiagnoseContext workflow in the ContextEngineering skill to diagnose context issues"}' \
  > /dev/null 2>&1 &
```

Running **DiagnoseContext** in **ContextEngineering**...

---
-->

## When to Use

- Agent is hallucinating (inventing APIs, wrong function signatures)
- Agent lost focus (contradicting itself, forgetting the task)
- Agent producing generic output (ignoring project specifics)
- Agent mixing conventions from different projects
- After context compaction — checking what was lost

## Diagnosis Checklist

### 1. Check for Starvation

| Symptom | Missing Level | Fix |
|---------|--------------|-----|
| Invents APIs that don't exist | L3 — Source | Read the relevant source files |
| Ignores project conventions | L1 — Rules | Ensure CLAUDE.md is loaded |
| Wrong function signatures | L3 — Source | Read types/interfaces |
| Hallucinates file paths | L3 — Source | Run Glob to find actual paths |
| Ignores requirements | L2 — Specs | Load the PRD/spec |

### 2. Check for Flooding

| Symptom | Overloaded Level | Fix |
|---------|-----------------|-----|
| Contradicts earlier reasoning | L5 — History too long | Summarize conversation |
| Forgets task objective | L5 — Too many tangents | Restate objective explicitly |
| Generic output | L3 — Too many files loaded | Focus on relevant files only |
| Slow/unfocused responses | Overall — past 2,000 lines | Compact and restart focus |

### 3. Check for Pollution

| Symptom | Source | Fix |
|---------|-------|-----|
| Wrong project conventions | Mixed L1 rules | Use project-specific CLAUDE.md |
| Applies stale patterns | Old L5 history | /clear between unrelated tasks |
| References deleted code | Outdated L3 | Re-read current file state |

## Recovery Actions

1. **Mild (focus drift):** Restate the objective in the next prompt. "We're doing X. The current sub-task is Y."
2. **Moderate (wrong context):** Load the correct files explicitly. "Read file X before continuing."
3. **Severe (context rot):** Summarize key decisions, /clear, restart with fresh context.
