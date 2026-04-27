---
name: Knowledge
description: Persistent knowledge base — save, search, and retrieve curated content across sessions. CLI-first via `kn`. USE WHEN save this, remember this content, save to knowledge, store this, search knowledge, what do I know about, recall, find in knowledge, kn, knowledge base, save digest, save wisdom, save research, what was that insight about, look up prior.
---

# Knowledge

PAI's persistent knowledge base. Stores curated content as flat markdown files with YAML frontmatter in `${AGENT_HOME}/knowledge/entries/`. Grep-based search. No database. Zero context footprint until invoked — content lives outside the conversation entirely.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Knowledge/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. If the directory does not exist, proceed with skill defaults.

## Architecture

```
${AGENT_HOME}/knowledge/
  INDEX.md          # Auto-maintained index (one line per entry)
  entries/          # Flat markdown files with YAML frontmatter
    2026-04-18-my-note.md
    2026-02-28-pai-v4-upgrade.md
  kn.ts             # CLI tool (Bun/TypeScript, single file)

~/.local/bin/kn     # Symlink, in PATH
```

No database. No MCP server. No running process. Files are greppable, human-readable, and git-trackable. `context-search` (Source I) searches this directory automatically.

### Entry Format

```yaml
---
title: "Descriptive title"
category: insight              # insight | decision | reference | pattern | session-summary
tags: [tag1, tag2, tag3]
project: project-name           # optional — which project this relates to
created: 2026-04-18
---

Freeform markdown content here.
```

## When to Use

### Save (manual — user asks or you recommend)

| User Says | Action |
|-----------|--------|
| "save this" / "remember this" | Save the most recent output to knowledge base |
| "save to knowledge" | Same as above |
| "store this as a pattern" | Save with category `pattern` |
| "save that research" | Save with category `reference` |

### Save (proactive — after producing these outputs, ASK if user wants to save)

| After Producing | Suggest Category |
|-----------------|-----------------|
| ExtractWisdom output | `insight` |
| Research results | `reference` |
| Follow-builders digest | `reference` |
| Architecture decision | `decision` |
| Reusable approach or technique | `pattern` |
| Important insight or analysis | `insight` |

**Do NOT auto-save without asking.** Say: "Want me to save this to the knowledge base?" If the user previously said "always save digests" etc., honor that.

### Search (when context would help)

| User Says | Action |
|-----------|--------|
| "what do I know about X" | `kn search "X"` |
| "recall / find / look up" | `kn search` with relevant terms |
| "search knowledge for X" | `kn search "X"` |
| "what was that insight about Y" | `kn search "Y"` |

### Proactive Search (search BEFORE answering when these conditions are met)

- User asks about a topic that sounds like it was discussed before
- User references "that digest" or "that research" without specifics
- A new task overlaps with previously saved content

## CLI Reference

### Save

```bash
# From content string
kn save --title "Title" --cat <category> --tags "tag1,tag2" --project "project-name" --content "..."

# From stdin pipe (for large content)
echo "content" | kn save --title "Title" --cat <category> --tags "tag1,tag2"
```

**Categories:** `insight`, `decision`, `reference`, `pattern`, `session-summary`

### Search

```bash
kn search "natural language query"              # Full-text grep search
kn search --cat decision "deployment"           # Category-filtered
kn search --tags security "API"                 # Tag-filtered
kn search --limit 5 "agents"                    # Limit results
```

Returns filename, title, category, tags, and a content snippet around the match.

### Browse & Retrieve

```bash
kn list                       # All entries (title + category + date)
kn list --cat pattern         # Filtered by category
kn get <filename>             # Full content (supports partial name match)
kn recent [N]                 # Last N entries (default 10)
kn categories                 # List categories with counts
kn stats                      # Entry count, size, date range
kn delete <filename>          # Remove entry and update INDEX.md
```

## Saving Guidelines

### Title
Descriptive, searchable. Encode the *what* — future-you searches by topic, not date.
- Good: "Why we chose Bun over Node for ClaudeClaw"
- Good: "Exfiltration guard regex false positive patterns"
- Bad: "Digest" or "Research results"

### Tags
Comma-separated, lowercase. Include people, concepts, projects mentioned.
- Good: `bun,runtime,decision,claudeclaw`
- Bad: `interesting,good,important`

### Category Selection

| Category | When to use | Example |
|----------|-------------|---------|
| `insight` | Aha moments, learnings, things to remember | "SHA-256 with salt is insufficient for short PINs" |
| `decision` | Why X was chosen over Y, with rationale | "Chose Grammy over Telegraf because..." |
| `reference` | Procedures, commands, how-tos, digests | "How to deploy ClaudeClaw to VPS" |
| `pattern` | Reusable approaches, techniques | "Per-chat FIFO queue pattern for Telegram bots" |
| `session-summary` | Session wrapup summaries | "PAI v4.0.1 Upgrade Completion" |

### Content
Save the *distilled* version, not raw transcripts. Write for future reference — include the **why**, not just the what. Context and rationale outlast bare facts.

### Project Tag
Use `--project` when the knowledge is specific to a project (e.g., `claudeclaw`, `cortex`, `pai`). Omit for cross-cutting knowledge.

## Integration with Other Skills

### After ExtractWisdom
```
"Want me to save this to the knowledge base?"
→ kn save --title "Wisdom: [source]" --cat insight --tags "..." --project "..."
```

### After Research
```
"Want me to save these findings?"
→ kn save --title "[research topic]" --cat reference --tags "..." --project "..."
```

### After follow-builders
```
"Want me to save today's digest?"
→ kn save --title "AI Builders Digest [date]" --cat reference --tags "..." 
```

### Before a New Task
When a user starts work on something that might overlap with saved knowledge:
```bash
kn search "relevant terms"
```
Surface any relevant prior content before diving in.

### With context-search
Knowledge entries are automatically searched by `/cs` and `/context-search` (Source I). No manual integration needed — when a user searches for prior work, knowledge base entries surface alongside PRDs, commits, and conversation history.
