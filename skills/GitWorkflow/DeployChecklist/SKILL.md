---
name: DeployChecklist
description: Pre-deployment verification checklists customized to your stack. USE WHEN deploy checklist, pre-deploy, ready to ship, deploy verification, release checklist, go-no-go, deploy readiness, before deploying, ship it, production deploy, rollback plan, sops, secrets check, encrypted config, pre-deploy secrets.
---

# DeployChecklist

Generate customized pre-deployment checklists based on your stack and release type.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/DeployChecklist/`

If this directory exists, load and apply:
- `PREFERENCES.md` - Default stack, CI/CD pipeline, rollback thresholds, team contacts
- Additional files specific to the skill

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Generate** | "deploy checklist", "ready to ship", "pre-deploy" | `Workflows/Generate.md` |
| **Verify** | "verify deploy", "go-no-go", "check deploy status" | `Workflows/Verify.md` |

## Examples

**Example 1: Standard deploy**
```
User: "Generate a deploy checklist for the auth service"
→ Invokes Generate workflow
→ Produces pre-deploy, deploy, post-deploy checklist
→ Includes rollback triggers with default thresholds
```

**Example 2: Deploy with migration**
```
User: "Deploy checklist — this one includes a database migration"
→ Invokes Generate workflow
→ Adds migration-specific checks (backup, test migration, rollback SQL)
→ Flags higher-risk deploy with additional verification steps
```

**Example 3: Verify readiness**
```
User: "Are we ready to deploy? Check CI and PRs"
→ Invokes Verify workflow
→ Checks git status, recent commits, CI if accessible
→ Produces go/no-go recommendation
```

## Quick Reference

**Checklist phases:** Pre-Deploy → Deploy → Post-Deploy
**Risk modifiers:** database migration, breaking API change, feature flags, first deploy of new service
**Rollback triggers:** error rate, latency, critical user flow failure

## sops — Pre-Deploy Secrets Verification

Verify secrets are properly encrypted before deploying. Add to every pre-deploy checklist: **"Verify secrets are encrypted (no plaintext in repo)"**.

### Verify encrypted secrets can be decrypted

```bash
sops --decrypt --output-type json secrets.enc.yaml | jq 'keys'
```

### Check for plaintext secrets in repo

```bash
grep -r "password\|secret\|api_key\|token" --include="*.yaml" --include="*.json" --include="*.env" . | grep -v ".enc." | grep -v node_modules
```

### Rotate encryption key

```bash
sops rotate -i secrets.enc.yaml
```

### Pre-deploy secrets checklist item

- [ ] All secrets files use `.enc.` naming convention
- [ ] `sops --decrypt` succeeds (encryption keys accessible)
- [ ] No plaintext secrets found in repo (grep check passes clean)
- [ ] Encryption keys rotated if any team member departed recently
