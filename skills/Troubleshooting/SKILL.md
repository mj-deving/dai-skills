---
name: Troubleshooting
description: Debugging and incident management — 6-step triage, Stop-the-Line, competing hypotheses for dev-time bugs plus incident detection, response, and blameless postmortems for production issues. USE WHEN debugging, fix bug, error recovery, troubleshooting, reproduce bug, root cause, stack trace, test failing, build broken, incident, outage, SEV1, SEV2, postmortem, blameless review, incident response, 5 whys.
---

# Troubleshooting

Unified skill for when things break — in development or in production.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Debugging, fix bug, error recovery, troubleshooting, reproduce bug, root cause, stack trace, test failing, build broken | `Debugging/SKILL.md` |
| Incident, outage, SEV1, SEV2, postmortem, blameless review, incident response, war room, 5 whys, incident timeline | `Incident/SKILL.md` |

## Examples

**Example 1: Debug a failing test**
```
User: "This test is failing intermittently"
→ Routes to Debugging
→ Non-reproducible bug playbook: isolate, instrument, competing hypotheses
```

**Example 2: Production incident**
```
User: "The API is returning 500s in production"
→ Routes to Incident
→ New incident workflow: triage, mitigate, communicate, resolve
```

**Example 3: Post-incident review**
```
User: "Write a postmortem for yesterday's outage"
→ Routes to Incident/Postmortem
→ Blameless review: timeline, contributing factors, action items
```
