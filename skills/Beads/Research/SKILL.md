---
name: beads-research
description: Research Beads best practices from primary sources. USE WHEN real Beads documentation, senior-user workflow patterns, architecture drift analysis, or source-grounded Beads doctrine and recommendations are needed.
---

# Beads Research

Use this skill when the task is about understanding how Beads is actually used in the wild, not changing one repo yet.

Outcome rule:
- distinguish current Beads guidance from mixed-era or stale docs
- prefer primary sources over forum-style summaries
- turn research into operational recommendations, not a citation dump

## Quick start

1. Read [references/source-map.md](references/source-map.md).
2. Load only the relevant reference file:
   - architecture/version drift: [references/operating-models.md](references/operating-models.md)
   - senior usage patterns and doctrine: [references/senior-usage-doctrine.md](references/senior-usage-doctrine.md)
3. If the user asked for the latest or to verify, re-browse the current Beads docs/README and the cited DoltHub posts before answering.

## Core rules

- Treat current Beads as version-sensitive. State clearly when a conclusion comes from current docs versus older doc pages.
- When sources disagree, anchor on the current README and current docs, then explain the older model as drift or historical context.
- Focus on operational questions:
  - embedded versus server mode
  - shared remote versus per-clone remote
  - CLI plus hooks versus MCP
  - formulas, gates, and durable handoff
  - recovery and lock/rehearsal posture
- If recommending tooling, tie each proposed tool to a concrete failure mode or workflow bottleneck.

## Deliverable shape

A good answer from this skill usually includes:
- what is current
- what appears mixed-era or stale
- what senior users optimize for
- what skills, workflows, or scripts would reduce risk or toil

Do not overquote sources. Summarize them and include links.
