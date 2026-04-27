---
name: Incident
description: Incident management from detection through postmortem. USE WHEN incident, outage, SEV1, SEV2, production down, postmortem, blameless review, incident response, war room, incident update, status page, root cause analysis, 5 whys, incident timeline, on-call.
---

# Incident

Manage incidents across 4 phases: Triage → Communicate → Mitigate → Postmortem.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Incident/`

If this directory exists, load and apply:
- `PREFERENCES.md` - Severity thresholds, escalation contacts, communication templates
- Additional files specific to the skill

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **New** | "new incident", "production down", "SEV1" | `Workflows/New.md` |
| **Update** | "incident update", "status update" | `Workflows/Update.md` |
| **Postmortem** | "postmortem", "blameless review", "root cause" | `Workflows/Postmortem.md` |

## Examples

**Example 1: Start a new incident**
```
User: "Production API is returning 500s for all users"
→ Invokes New workflow
→ Assesses severity, identifies affected systems
→ Produces triage summary + status update + communication draft
```

**Example 2: Post a status update**
```
User: "Update the incident — we identified the cause, it's a bad deploy"
→ Invokes Update workflow
→ Structures update with current status, actions taken, next steps
→ Outputs formatted status update ready to post
```

**Example 3: Write postmortem**
```
User: "Write the postmortem for yesterday's outage"
→ Invokes Postmortem workflow
→ Reconstructs timeline, runs 5 Whys analysis
→ Produces blameless postmortem with action items
```

## Quick Reference

**Severity Levels:**
| Level | Criteria | Response Time |
|-------|----------|---------------|
| SEV1 | Total outage, all users affected | Immediate, all-hands |
| SEV2 | Major degradation, many users affected | < 15 min, on-call team |
| SEV3 | Partial degradation, some users affected | < 1 hour, assigned team |
| SEV4 | Minor issue, workaround available | Next business day |

**Phases:**
1. **Triage** — Severity, impact, roles (IC, comms, responders)
2. **Communicate** — Internal update, customer comms, war room cadence
3. **Mitigate** — Steps taken, timeline tracking, resolution confirmation
4. **Postmortem** — Blameless review, 5 Whys, action items with owners
