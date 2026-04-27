# Incident Status Update

Post a structured status update for an ongoing incident.

## Steps

### 1. Gather Current State

Ask the user (or infer):
- What's the current status? (Investigating / Identified / Monitoring / Resolved)
- What actions have been taken since last update?
- What are the next steps?
- Any new information about root cause?

### 2. Produce Status Update

```markdown
## Incident Update: [Title]
**Severity:** SEV[1-4] | **Status:** Investigating | Identified | Monitoring | Resolved
**Impact:** [Who/what is affected]
**Last Updated:** [Timestamp]

### Current Status
[What we know now — 2-3 factual sentences]

### Actions Taken
- [Action 1 — with who and when]
- [Action 2]

### Next Steps
- [What's happening next and ETA]
- [Escalation plans if current approach fails]

### Timeline
| Time | Event |
|------|-------|
| [HH:MM] | [Initial detection] |
| [HH:MM] | [Action taken] |
| [HH:MM] | [This update] |
```

### 3. Communication Guidance

**Internal:** Post full update to incident channel
**External (if SEV1/SEV2):** Produce a shorter customer-facing version:

```markdown
**[Service Name] — [Status]**
We are experiencing [brief description of impact].
Our team is actively working on resolution.
Next update at [time].
```

### Rules

- **Keep updates factual** — What we know, what we've done, what's next. No speculation.
- **Always include next update time** — Even if it's "in 30 minutes"
- **Maintain the timeline** — Append new events, never rewrite history
