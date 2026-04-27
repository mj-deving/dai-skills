# Postmortem

Generate a blameless postmortem from incident data.

## Steps

### 1. Gather Incident Data

Ask the user for (or pull from conversation context):
- Incident title and date
- Duration of impact
- Severity level
- Who was involved in response
- Timeline of events (what happened when)
- What the root cause was (or best understanding)
- What went well during response
- What went poorly

### 2. Run 5 Whys Analysis

Walk through the causal chain:

1. **Why did [symptom occur]?** → Because [cause 1]
2. **Why did [cause 1]?** → Because [cause 2]
3. **Why did [cause 2]?** → Because [cause 3]
4. **Why did [cause 3]?** → Because [cause 4]
5. **Why did [cause 4]?** → **Root cause: [systemic issue]**

The goal is to reach a systemic/process root cause, not blame an individual.

### 3. Generate Action Items

For each finding, produce actionable items:
- **P0:** Must fix before next deploy (prevents recurrence)
- **P1:** Fix within 1 week (reduces risk)
- **P2:** Fix within 1 month (improves resilience)

Each action item needs: description, owner, priority, due date.

### 4. Produce Postmortem Document

```markdown
## Postmortem: [Incident Title]
**Date:** [Date] | **Duration:** [X hours Y min] | **Severity:** SEV[X]
**Authors:** [Names] | **Status:** Draft

### Summary
[2-3 sentence plain-language summary. What happened, how long, who was affected.]

### Impact
- **Users affected:** [number or scope]
- **Duration of impact:** [time]
- **Business impact:** [revenue, SLA, reputation — quantify if possible]

### Timeline (UTC)
| Time | Event |
|------|-------|
| [HH:MM] | [Detection — how was it noticed?] |
| [HH:MM] | [Triage — severity assessed] |
| [HH:MM] | [Key actions taken] |
| [HH:MM] | [Mitigation applied] |
| [HH:MM] | [Resolution confirmed] |

### Root Cause
[Detailed explanation of the technical root cause. Be specific — "a config change to X caused Y because Z" not "human error".]

### 5 Whys
1. Why did [symptom]? → [Because...]
2. Why did [cause 1]? → [Because...]
3. Why did [cause 2]? → [Because...]
4. Why did [cause 3]? → [Because...]
5. Why did [cause 4]? → **[Root cause]**

### What Went Well
- [Things that worked — detection, response, communication]

### What Went Poorly
- [Things that didn't work — delayed detection, missing runbooks, unclear ownership]

### Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Specific action] | [Person] | P0 | [Date] |
| [Specific action] | [Person] | P1 | [Date] |
| [Specific action] | [Person] | P2 | [Date] |

### Lessons Learned
[2-3 key takeaways that apply beyond this specific incident]
```

### Rules

- **Blameless:** Focus on systems and processes, never individuals. "The deploy pipeline lacked a canary step" not "Alice deployed without checking"
- **Specific:** "Error rate hit 45% for 23 minutes" not "there were some errors"
- **Actionable:** Every action item must be specific, owned, and dated
- **Forward-looking:** The goal is to prevent recurrence, not assign blame
