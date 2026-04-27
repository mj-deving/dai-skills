# GitHub Release Plan

## Phase 1 — Local Scaffold

- [x] Create local repo scaffold.
- [x] Copy public-candidate skill subset.
- [x] Add portable `research` and project-only `project-telos` variants.
- [x] Generate catalog, install docs, and publication checklist.
- [x] Run publication audit.

## Phase 2 — Sanitize

- [x] Fix missing relative links in `docs/audit-report.md`.
- [x] Replace or parameterize hardcoded local paths.
- [x] Review every secret-pattern hit and remove examples that look credential-like.
- [x] Decide whether to include or permanently exclude remaining personal/local skill groups from `docs/private-exclusions.md`.
- [ ] Optionally split very large skills later.
- [x] Choose a license.

## Phase 3 — Publish

After license/provenance review is complete:

```bash
cd ${REPO_DIR}
git add .
git commit -m "docs: scaffold public PAI skills catalog"
gh repo create pai-skills --public --source=. --remote=origin --push
```

The audit hard gates now pass. Do not publish before license/provenance review is complete.
