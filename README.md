# PAI Skills

Public-ready skill collection scaffold for Codex/Claude-style AI coding agents.

This repository is staged for public GitHub release. Automated audit hard gates pass; final publication is a maintainer decision.

## What This Contains

- `skills/` — exported skill folders from the local PAI skill workspace
- `docs/catalog.md` — generated catalog grouped by practical use case
- `docs/install-codex.md` — Codex symlink/install guidance
- `docs/install-claude.md` — Claude symlink/install guidance
- `docs/publication-checklist.md` — pre-publication safety and quality checklist
- `scripts/audit_skills.py` — metadata/link/path audit helper

## Practical Use

Skills are loaded by agents as task-specific operating guides. Use broad router skills for vague requests, and leaf skills for concrete workflows.

Examples:

- Use `beads` for repo workflow and issue coordination.
- Use `Browser` for browser automation and visual debugging.
- Use `research` for source-grounded research without local machine assumptions.
- Use `project-telos` for project context maps and executive briefs without personal TELOS state.
- Use `FrontendDesign` or the `Frontend/Impeccable` skills for UI work.
- Use `CodeReview` or `Desloppify` for code-health passes.
- Use `n8n-*` skills for workflow automation and node configuration.

## Publication Status

The automated publication audit now passes hard gates: no metadata errors, broken relative links, hardcoded local paths, or secret-pattern hits. Remaining pre-publication judgment items:

1. optionally split large skills for progressive disclosure
2. decide whether to publish now or do an additional manual line-by-line review

Run:

```bash
python3 scripts/audit_skills.py
```

## Install Sketch

For Codex, symlink selected skill folders into `$CODEX_HOME/skills`:

```bash
ln -sfn "$PWD/skills/Beads" "$CODEX_HOME/skills/beads"
ln -sfn "$PWD/skills/Utilities/Browser" "$CODEX_HOME/skills/browser"
```

For Claude, symlink or copy selected folders into the configured skills directory.

See `docs/install-codex.md` and `docs/install-claude.md`.
