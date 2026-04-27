# Publication Checklist

Before creating a public GitHub repository:

- [x] Choose an explicit license and replace `LICENSE.md`.
- [x] Run `python3 scripts/audit_skills.py` and review all findings.
- [x] Fix missing relative links or remove references to unavailable bundled assets.
- [x] Replace hardcoded local paths with portable placeholders where possible.
- [x] Review copied skills for private project names, account-specific assumptions, and operational secrets.
- [ ] Keep original `Research` and `Telos` private unless their local-memory and personal-context assumptions are fully removed.
- [x] Document third-party content provenance and license compatibility notes.
- [ ] Decide whether large skills should be split into smaller references for progressive disclosure.
- [x] Add examples showing how to symlink only selected skills.
- [ ] Create a release tag only after a clean audit.

Recommended GitHub creation command after review:

```bash
gh repo create pai-skills --public --source=. --remote=origin --push
```
