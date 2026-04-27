---
name: ContextEngineering
description: Strategic context management for AI agents — 5-level hierarchy, starvation/flooding diagnosis, brain dump structuring, confusion surfacing. USE WHEN context management, context strategy, too much context, too little context, context window, context budget, brain dump, session context, what context to load, context starvation, context flooding, agent context, prompt engineering context.
---

# ContextEngineering

Strategic structuring of information fed to AI agents. Too little context and the agent hallucinates. Too much and it loses focus. This skill teaches how to find the balance.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/ContextEngineering/`

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WORKFLOWNAME in ContextEngineering to ACTION"}' \
  > /dev/null 2>&1 &
```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **StructureContext** | "structure context", "brain dump", "session setup", "what context to load" | `Workflows/StructureContext.md` |
| **DiagnoseContext** | "context problem", "agent confused", "hallucinating", "losing focus", "context starvation", "context flooding" | `Workflows/DiagnoseContext.md` |

## The 5-Level Context Hierarchy

From most persistent to most transient:

| Level | What | Token Budget | Lifespan | Example |
|-------|------|-------------|----------|---------|
| **L1 — Rules** | CLAUDE.md, steering rules, constitution | ~200-400 | Permanent | Project conventions, behavioral constraints |
| **L2 — Specs** | Feature specs, requirements, design docs | ~500-1500 | Per-project | SPEC.md, PRD.md, ADRs |
| **L3 — Source** | Code files being modified + relevant examples | ~1000-3000 | Per-task | The files you're actually editing |
| **L4 — Errors** | Test failures, build errors, runtime logs | ~200-500 | Per-attempt | Stack traces, failing assertions |
| **L5 — Conversation** | Chat history, prior turns, accumulated reasoning | Grows unbounded | Per-session | Previous questions and answers |

**Key insight:** L1-L2 are compressed and stable. L3-L4 are focused and relevant. L5 grows without bound and is the primary cause of context degradation.

## The 2,000-Line Threshold

Research and practice show agent performance degrades beyond ~2,000 lines of active context per task. When you approach this:

- **Compacted:** Summarize L5 (conversation history) to key decisions and open questions
- **Selective:** Load only L3 source files directly relevant to current task
- **Defer:** Don't load reference docs "just in case" — load when a workflow needs them

## Anti-Patterns

### Context Starvation (too little)

**Symptoms:** Agent invents APIs that don't exist, uses wrong function signatures, ignores project conventions, hallucinates file paths.

**Diagnosis:** Missing L1 (no CLAUDE.md) or L3 (didn't read the relevant code before modifying).

**Fix:** Ensure CLAUDE.md exists with conventions. Read the file before editing. Load relevant types/interfaces.

### Context Flooding (too much)

**Symptoms:** Agent loses focus, contradicts earlier reasoning, forgets task objectives, produces generic output, ignores specific instructions buried in noise.

**Diagnosis:** L5 (conversation) has grown past useful length, or too many L3 files loaded at once.

**Fix:** Summarize conversation at natural breakpoints. Load only files relevant to current sub-task, not entire codebase.

### Context Pollution

**Symptoms:** Agent follows patterns from wrong project, mixes conventions, applies advice from unrelated context.

**Diagnosis:** L2 specs from different projects loaded simultaneously, or stale L5 history from a previous task.

**Fix:** Clear context between projects. Use `/clear` between unrelated tasks. Keep CLAUDE.md per-project, not global.

## Core Principles

- **A well-structured 10-minute rules file prevents hours of correction cycles**
- **Every piece of context has a cost** — token budget, attention dilution, confusion risk
- **Implicit knowledge doesn't exist** — if it's not in context, the agent doesn't know it
- **Surface confusion explicitly** — "I'm assuming X; correct me now" is better than silent wrong assumptions

## Examples

**Example 1: Starting a complex task**
```
User: "Refactor the auth module — here's what I know: [brain dump]"
→ Invokes StructureContext workflow
→ Organizes brain dump into task context (objective, stack, constraints, files, gotchas)
→ Identifies L3 source files to load before starting
```

**Example 2: Agent producing bad output**
```
User: "The agent keeps inventing functions that don't exist"
→ Invokes DiagnoseContext workflow
→ Diagnoses: L3 starvation — agent didn't read source files
→ Fix: Read the relevant types/interfaces before continuing
```

**Example 3: Session getting unfocused**
```
User: "We've been going back and forth and losing track"
→ Invokes DiagnoseContext workflow
→ Diagnoses: L5 flooding — conversation history too long
→ Fix: Summarize key decisions, /clear, restart with fresh context
```

## Integration

**Works with:**
- **CLAUDE.md composition standard** — how to write L1 rules files
- **CONTEXT_ROUTING.md** — lookup table for finding the right context
- **DocsList** — explicit L2 documentation index when a task needs a project docs map
- **context-search** — finding relevant prior work
- **Algorithm OBSERVE** — assumption surfacing step
