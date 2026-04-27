# WriteADR Workflow

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WriteADR in Documentation to document architecture decision"}' \
  > /dev/null 2>&1 &
```
-->

Running **WriteADR** in **Documentation**...

---

## When to Use

- A significant technical choice was made (framework, database, API design, system boundary)
- Choosing technology X over Y with non-obvious reasoning
- Establishing a convention that affects future development
- Algorithm LEARN phase identifies an architectural decision worth recording

## Process

### Step 1: Determine Scope

- **Project ADR** → `docs/decisions/` in the current project
- **Global/PAI-wide ADR** → `~/projects/Pai-Exploration/docs/decisions/` (only when user explicitly requests)

### Step 2: Find Next Number

```bash
ls docs/decisions/ | sort -n | tail -1
# If last is 0010, next is 0011
```

### Step 3: Write the ADR

```markdown
# NNNN — [Title: The Decision Made]

**Status:** Accepted
**Date:** YYYY-MM-DD

## Context

[What prompted this decision? What constraints exist?
What problem are we solving?]

## Decision

[What we decided and why. Be specific — not "use X" but
"use X because Y constraint makes Z the only viable option."]

## Alternatives Considered

[What else was evaluated and why it was rejected.
This is the most valuable section for future readers.]

## Consequences

[What changes as a result. Both positive and negative.
What new constraints does this create?]
```

### Step 4: Verify

- [ ] Title describes the DECISION, not the context
- [ ] Context explains WHY this decision was needed
- [ ] Decision is specific (not "we chose the best option")
- [ ] At least one alternative documented with rejection reason
- [ ] Consequences include both benefits and trade-offs
