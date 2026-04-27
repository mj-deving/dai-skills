# Generate Deploy Checklist

Produce a customized pre-deployment checklist.

## Steps

### 1. Determine Context

Ask the user (or infer from their message):
- **What** is being deployed? (service name, version, description)
- **Who** is deploying? (deployer name)
- **Risk modifiers** — check if any apply:
  - Database migration included?
  - Breaking API change?
  - Feature flags involved?
  - First deploy of a new service?
  - Infrastructure/config change?

### 2. Check Git Status (if in a repo)

```bash
git log --oneline -5    # Recent commits
git status              # Uncommitted changes
git branch --show-current  # Current branch
```

Use this to pre-fill the checklist with actual context.

### 3. Generate Checklist

```markdown
## Deploy Checklist: [Service/Release]
**Date:** [Date] | **Deployer:** [Name] | **Risk:** Standard | Elevated | High

### Pre-Deploy
- [ ] All tests passing in CI
- [ ] Code reviewed and approved
- [ ] No known critical bugs in release
- [ ] Rollback plan documented
- [ ] On-call team notified
```

**If database migration:**
```markdown
- [ ] Migration tested on staging with production-like data
- [ ] Migration is reversible (down migration exists)
- [ ] Database backup taken before deploy
- [ ] Migration estimated time: [X minutes]
- [ ] Read replica lag acceptable during migration
```

**If breaking API change:**
```markdown
- [ ] All consumers notified of breaking change
- [ ] Deprecation period observed (if applicable)
- [ ] API versioning in place
- [ ] Consumer migration guide published
```

**If feature flags:**
```markdown
- [ ] Feature flags configured in [flag service]
- [ ] Flags set to OFF by default
- [ ] Kill switch tested
- [ ] Rollout plan defined (%, cohorts, timing)
```

Continue with deploy and post-deploy:

```markdown
### Deploy
- [ ] Deploy to staging and verify
- [ ] Run smoke tests on staging
- [ ] Deploy to production (canary if available)
- [ ] Monitor error rates and latency for 15 min
- [ ] Verify key user flows work end-to-end

### Post-Deploy
- [ ] Confirm metrics are nominal (error rate, latency, throughput)
- [ ] Update release notes / changelog
- [ ] Notify stakeholders of successful deploy
- [ ] Close related tickets/issues

### Rollback Triggers
Deploy must be rolled back if ANY of:
- Error rate exceeds [X]% (baseline: [current]%)
- P50 latency exceeds [X]ms (baseline: [current]ms)
- [Critical user flow] fails end-to-end test
- Any SEV1/SEV2 incident opened within 30 min of deploy
```

### 4. Adapt to User's Stack

If the user mentions their stack, customize:
- **Cloudflare Pages:** Add "Verify preview deployment URL" and "Check Cloudflare dashboard"
- **Docker/K8s:** Add "Verify image tagged and pushed" and "Check pod rollout status"
- **Serverless:** Add "Check cold start times" and "Verify function memory limits"
- **npm publish:** Add "Verify package contents with `npm pack --dry-run`" and "Check `npm whoami`"
