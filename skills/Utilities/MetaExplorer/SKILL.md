---
name: MetaExplorer
description: PAI-wide meta knowledge system — fast capture, federated search, TELOS alignment, weekly digest, reminders. CLI-first via `mx`. USE WHEN mx, capture idea, dump URL, what's my status, check alignment, does this align with goals, what happened this week, weekly digest, remind me, set reminder, ideas inbox, check goals, telos, mission check, what should I work on, am I on track, side-task check, open ideas.
---

# MetaExplorer (mx)

PAI's unified capture + federated query layer over all existing subsystems. Not a new database — an interface. Fast capture to a single inbox, federated search across 7 stores, TELOS alignment checking, weekly digests, and reminders with surface-by dates.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/MetaExplorer/`

If this directory exists, load and apply any PREFERENCES.md. If not, proceed with defaults.

## Architecture

```
${AGENT_HOME}/tools/
  mx.ts               # Entry point (thin router, ~60 lines)
  mx-lib/
    shared.ts          # Paths, colors, date helpers
    capture.ts         # add, remind
    read.ts            # ideas, status, query
    telos.ts           # goals, align
    weekly.ts          # weekly digest

${PAI_USER_DIR}/TELOS/
  IDEAS.md             # The inbox (mx writes here)
  MISSION.md           # World problems + mission statement
  GOALS.md             # G1-G4 with success criteria
  CHALLENGES.md        # C1-C6 linked to goals
  STRATEGIES.md        # S1-S6 linked to challenges
  PROJECTS.md          # P1-P6 linked to strategies
  BELIEFS.md           # Core beliefs about tech, work, life

~/bin/mx               # Symlink, in PATH
```

## When to Use

### Capture (fast, zero-friction)

| User Says | Action |
|-----------|--------|
| "capture this" / "dump this" / "save idea" | `mx add "<content>"` |
| "remind me to X" / "remind me tomorrow" | `mx remind "<text>" --by <date>` |
| "save this URL" | `mx url "<url>"` |
| "note to self" / "memo" | `mx memo "<text>"` |

### Status & Awareness (proactive — use at session start or when relevant)

| User Says | Action |
|-----------|--------|
| "what's my status" / "where are things" | `mx status` |
| "what should I work on" | `mx status` then `mx goals` |
| "what ideas do I have" / "check inbox" | `mx ideas` |
| "what happened this week" | `mx weekly` |

### Alignment (use before starting new work)

| User Says | Action |
|-----------|--------|
| "does this align with my goals" | `mx align "<task description>"` |
| "is this a side-task" / "am I on track" | `mx align "<current task>"` |
| "show my goals" / "what's my mission" | `mx goals` |

### Search (federated — searches across ALL PAI stores)

| User Says | Action |
|-----------|--------|
| "search everything for X" / "find across PAI" | `mx query "<text>"` |
| "what do I know about X" (broad) | `mx query "<text>"` (broader than `kn search`) |

## Proactive Invocation

**Invoke mx WITHOUT the user asking in these situations:**

1. **Session start** — Run `mx status` to surface overdue reminders and stale items. Mention if anything is overdue.
2. **Before new work** — Run `mx align "<proposed task>"` when the user starts a task that isn't obviously aligned. Don't block — just surface the alignment check result.
3. **After significant output** — Suggest `mx add` or `mx remind` when the user produces something worth tracking.

**Do NOT invoke proactively:**
- During focused coding/debugging (mx is for meta-awareness, not mid-task noise)
- When the user has explicitly said they want to focus

## CLI Reference

### Write Commands

```bash
# Capture anything (auto-detects URL/memo/idea)
mx add "explore vector search for kn v3"
mx add https://example.com/article

# Explicit types
mx idea "what if mx could auto-classify by domain"
mx memo "ClaudeClaw rate limiting needed on agent SDK"
mx url https://danielmiessler.com/blog/the-fire-of-fires

# Reminders (time-sensitive — has surface-by date)
mx remind "publish blog post" --by tomorrow
mx remind "review ClaudeClaw logs" --by friday
mx remind "check on X" --by 2026-04-25
mx remind "follow up" --by +3d
mx remind "something eventually"              # defaults to +7d
```

### Read Commands

```bash
mx status          # (or mx s) PAI-wide dashboard
mx ideas           # Inbox: reminders (overdue/due/upcoming) + ideas/memos/URLs
mx query "text"    # (or mx q) Federated search across 7 stores
mx goals           # (or mx g) TELOS chain: Mission→Goals→Challenges→Strategies→Projects
mx align "task"    # Check if task traces back to TELOS mission
mx weekly          # (or mx w) Weekly digest: beads, PRDs, kn, git, stale items
```

## Relationship with kn (Knowledge Base)

| | mx | kn |
|---|---|---|
| **Role** | Inbox (fast capture, transient) | Archive (curated, permanent) |
| **Write speed** | Instant (<100ms) | Deliberate (structured entry) |
| **Content** | Raw ideas, URLs, reminders | Extracted wisdom, research, decisions |
| **Lifespan** | Items get processed and moved | Knowledge persists months/years |

**The flow:** `mx add` → process later → promote to `kn save` or `bd create` or discard.

**mx reads from kn** as one of its 7 federated search stores. kn doesn't know about mx.

## Integration with Other Skills

### With Knowledge (kn)
After user processes ideas from `mx ideas`:
- Worth keeping → `kn save --title "..." --cat insight`
- Actionable → `bd create` or `mx remind`
- Not valuable → delete from IDEAS.md

### With Research
After extensive research completes:
```
mx add "Research on [topic] complete — review findings in WORK dir"
```

### With extract_wisdom
After running extract_wisdom on content:
```
"Want me to save this to kn and add a reminder to review it?"
→ kn save + mx remind "review [topic] wisdom" --by +3d
```

### With TELOS (Telos skill)
MetaExplorer reads TELOS files for `mx goals` and `mx align`. The Telos skill handles CRUD operations on TELOS files (update goals, add beliefs, etc.). MetaExplorer is read-only on TELOS — it displays and checks alignment but never modifies.

### With Beads (bd)
`mx status` reads open beads count. `mx weekly` shows beads closed this week. `mx query` searches beads via `bd search`. But mx never creates or closes beads — that's `bd`'s job.

## Daemon Integration

**TelosRefreshNudge.hook.ts** (Stop event):
- Checks for stale TELOS files (>14 days since update)
- Checks for overdue reminders
- Warns on stderr — non-blocking, <5s timeout
