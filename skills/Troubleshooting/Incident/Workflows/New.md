# New Incident

Start a new incident from initial detection.

## Steps

### 1. Gather Context

Ask the user (or infer from their message):
- What is happening? (symptoms)
- When did it start?
- Who/what is affected?
- What changed recently? (deploys, config changes)

### 2. Assess Severity

| Level | Criteria |
|-------|----------|
| **SEV1** | Total outage, all users affected, revenue impact |
| **SEV2** | Major degradation, many users affected |
| **SEV3** | Partial degradation, some users, workaround exists |
| **SEV4** | Minor issue, workaround available, low impact |

### 3. Assign Roles

- **Incident Commander (IC):** Coordinates response, makes decisions
- **Communications Lead:** Posts updates internally and externally
- **Responders:** Engineers working on mitigation

If the user hasn't specified, ask who is filling these roles.

### 4. Produce Output

Generate a structured incident record:

```markdown
## Incident: [Title — short, descriptive]
**Severity:** SEV[1-4] | **Status:** Investigating
**Started:** [Timestamp] | **IC:** [Name] | **Comms:** [Name]

### Impact
- **Users affected:** [scope]
- **Services affected:** [list]
- **Business impact:** [revenue, reputation, compliance]

### What We Know
- [Symptom 1]
- [Symptom 2]
- [Recent changes that may be related]

### Immediate Actions
1. [First action to take]
2. [Second action]
3. [Escalation if needed]

### Communication Plan
- **Internal:** Post to [#incident channel] every [15/30] min
- **External:** [Status page update / customer email / none yet]
- **War room:** [Link or location]

### Rollback Plan
- [How to roll back if mitigation fails]
```

### 5. Draft First Status Update

Also produce a concise status update suitable for posting:

```markdown
**[SEV-X] [Title]**
**Status:** Investigating
**Impact:** [One sentence]
**What we know:** [2-3 sentences]
**Next update:** [Time]
```
