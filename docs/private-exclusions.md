# Private / Local Exclusions

These local skill groups were not copied into the first public-ready export.

- `GoogleWorkspace` — workspace/account integrations; review for tenant, credential, and private workflow assumptions.
- `Gsd` — personal/local operating workflow; review before public release.
- `Inbox` — likely personal intake/workflow state; review before public release.
- `Pai` — core local PAI identity/runtime layer; keep private unless a portable public profile is created.
- `Research` — original local skill remains excluded because it is coupled to local PAI memory, local paths, external agents/tools, and cost-heavy workflows. A portable public variant is included at `skills/Research`.
- `Telos` — original local skill remains excluded because it contains personal life/career operating-system assumptions and paths. A project-only public variant is included at `skills/ProjectTelos`.
- `ccgram-messaging` — messaging integration; review for account, token, and private workflow assumptions.
- `Utilities/DistillToTelos` — personal TELOS belief-candidate workflow and local state ledger; excluded from the public export.
- `Utilities/Aphorisms` — personal curated quote/TELOS workflow; excluded from the public export.
- `Frontend/Aesthetics/mj-brand` — personal brand design system; excluded from the public export.

- `Utilities/Fabric` — bundled upstream Fabric prompt patterns; excluded until third-party provenance is verified or replaced with install/sync instructions.

Review and sanitize these manually before adding them to a public repository.
