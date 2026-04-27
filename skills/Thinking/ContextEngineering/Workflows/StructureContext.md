# StructureContext Workflow — Brain Dump

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the StructureContext workflow in the ContextEngineering skill to structure session context"}' \
  > /dev/null 2>&1 &
```

Running **StructureContext** in **ContextEngineering**...

---
-->

## When to Use

- Starting a complex task and need to organize what context to load
- User provides a "brain dump" of requirements, constraints, and background
- Agent spawning — structuring context for a subagent prompt
- Session feels unfocused — need to reset what's in context

## Process

### Step 1: Inventory What's Available

Map what context exists at each level:

```
L1 Rules:    [ ] CLAUDE.md   [ ] Steering rules   [ ] Constitution
L2 Specs:    [ ] PRD/spec    [ ] ADRs             [ ] Design docs
L3 Source:   [ ] Files to edit [ ] Types/interfaces [ ] Related code
L4 Errors:   [ ] Test output  [ ] Build errors     [ ] Runtime logs
L5 History:  [ ] Prior turns  [ ] Decisions made   [ ] Open questions
```

### Step 2: Load by Priority

1. **Always load:** L1 rules (CLAUDE.md, project conventions)
2. **Load if task has a spec:** L2 (PRD, requirements, ADRs)
3. **Load before editing:** L3 (the actual files + their imports/types)
4. **Load when debugging:** L4 (the specific error, not all logs)
5. **Summarize, don't accumulate:** L5 (key decisions, not full history)

### Step 3: Brain Dump Structuring

When user provides unstructured context, organize it:

```markdown
## Task Context (structured from brain dump)

**Objective:** [What we're trying to accomplish]
**Tech Stack:** [Languages, frameworks, key dependencies]
**Constraints:** [What we can't change, deadlines, requirements]
**Relevant Files:** [Specific paths to read before starting]
**Known Gotchas:** [Things that have caused problems before]
**Out of Scope:** [What we're NOT doing in this task]
```

### Step 4: Budget Check

Estimate total context load:
- L1+L2: ~500-1500 tokens (stable, always present)
- L3: ~100-300 tokens per source file read
- L4: ~200-500 tokens per error block
- L5: grows ~200-500 tokens per turn

**If approaching 2,000 lines:** Compact L5, defer L3 files not immediately needed.
