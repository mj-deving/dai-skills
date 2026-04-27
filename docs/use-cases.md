# Practical Use Guide

Use skills as task-specific operating manuals for AI agents.

## Routing Pattern

1. If the request is broad, start with a category router skill such as `Utilities`, `Frontend`, `Beads`, `Security`, or `ContentAnalysis`.
2. If the request is concrete, use the leaf skill directly, such as `Browser`, `beads-version-audit`, `n8n-expression-syntax`, or `Desloppify`.
3. Load only the references needed for the current task.
4. Prefer scripts bundled with a skill when deterministic behavior matters.

## Common Workflows

- **New repo workflow setup:** `beads` → `beads-bootstrap` → `beads-version-audit`.
- **Multi-agent repo coordination:** `beads-topology-planner` → `beads-upgrade-path` → `beads-hook-audit`.
- **Frontend build or redesign:** `FrontendDesign` → relevant `Frontend/Impeccable/*` or aesthetics skill → `Browser` for visual verification.
- **Code health pass:** `CodeReview` for review, `Refactor` for lightweight cleanup, `Desloppify` for full code-health scoring.
- **n8n workflow build:** `n8n-workflow-patterns` → `n8n-node-configuration` → `n8n-expression-syntax` → `n8n-validation-expert`.
- **Web extraction:** `Scraping` router → provider skill such as `Apify`, `BrightData`, `Crawl4AI`, `JinaReader`, or `Spider`.
- **Research/reporting:** `research` for source-grounded research, `ContentAnalysis` for extraction/summarization, `Investigation` for OSINT, then `VisualExplainer` for shareable output.
- **Project context mapping:** `project-telos` to turn project docs, repos, notes, and public sources into a context pack, dependency map, or executive brief.

## Public vs Local Use

This export intentionally excludes clearly personal/local skill groups listed in `private-exclusions.md`. Additional hardcoded local paths may still exist in copied skills; run `scripts/audit_skills.py` before publishing.
