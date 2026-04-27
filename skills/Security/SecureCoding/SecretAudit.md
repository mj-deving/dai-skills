# Secret Audit

Find secrets already committed to git history or existing in codebases. Supplementary to SecurityValidator's real-time blocking.

---

## When to Use

- **New repo onboarding** — scan history before trusting a codebase
- **Pre-deploy audit** — verify no secrets ship to production
- **Post-incident (suspected key leak)** — find what was exposed and when
- **Periodic hygiene check** — scheduled sweeps to catch drift

---

## Limitations

> **READ THIS FIRST** — understand what this document can and cannot do.

- **This is supplementary** — use TruffleHog, Gitleaks, or GitGuardian as primary tools. They have entropy analysis, ML models, and maintained pattern databases that far exceed manual regex.
- **Regex catches ~40-60% of secrets.** Entropy-based detection adds another 20-30%. The remainder requires manual review or specialized tooling.
- **Does NOT detect:**
  - Custom keys without standard prefixes
  - Base64-encoded secrets
  - Concatenated or split strings (`"sk_" + "live_" + token`)
  - Secrets in binary files (compiled code, images with steganography, database dumps)
- **SecurityValidator.hook.ts already runs 35+ patterns on every write** — this document is for historical/audit scanning of code that predates the hook or was committed elsewhere.

---

## Common Secret Patterns

| Pattern Name | Example Format | Regex |
|---|---|---|
| AWS Access Key | `EXAMPLE_AKIAIOSFODNN7EXAMPLE` | `AKIA[0-9A-Z]{16}` |
| AWS Secret Key | `EXAMPLE_wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` | `[A-Za-z0-9/+=]{40}` (near `aws_secret`, `AWS_SECRET`, or `secret_access_key`) |
| GitHub Token (PAT) | `ghp_EXAMPLE01234567890abcdefghijklmnopqr` | `gh[pousr]_[A-Za-z0-9]{36}` |
| GitHub Token (other) | `gho_EXAMPLE…`, `ghs_EXAMPLE…`, `ghu_EXAMPLE…` | Same pattern — `gho_`, `ghs_`, `ghu_` prefixes |
| Slack Token | `xoxb-EXAMPLE-0000000000-abcdefghijklmn` | `xox[bpras]-[0-9a-zA-Z-]+` |
| Stripe Secret Key | `sk_live_<redacted>` | `sk_live_[0-9a-zA-Z]{24,}` |
| Stripe Publishable Key | `pk_live_<redacted>` | `pk_live_[0-9a-zA-Z]{24,}` |
| Google API Key | `AIza<redacted>` | `AIza[0-9A-Za-z\-_]{35}` |
| Private Key Header | `-----BEGIN <KEY TYPE> PRIVATE KEY-----` | `-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----` |
| Generic High-Entropy | (random 32+ char strings) | Use entropy-based tools — not feasible with regex alone |

---

## Git History Scanning

### Basic pattern search across all history

```bash
git log --all --full-history -p | grep -nE 'AKIA[0-9A-Z]{16}'
```

Replace the pattern with any regex from the table above.

### Find deleted sensitive files

```bash
git log --all --diff-filter=D -- '*.env' '*.key' '*.pem'
```

### Search all commits for a pattern

```bash
git rev-list --all | xargs git grep -l 'AKIA[0-9A-Z]{16}'
```

### Performance note

These commands are **slow on large repos** (10k+ commits). For repos with significant history, use TruffleHog (`trufflehog git file://./ --only-verified`) which is purpose-built for speed and accuracy on git history scanning.

---

## .gitignore Coverage Verification

### Required .gitignore entries

Verify your `.gitignore` includes these patterns:

```
.env*
*.pem
*.key
*.p12
*.pfx
credentials.json
service-account*.json
```

### Find tracked sensitive files

```bash
git ls-files --cached | grep -iE '\.(env|pem|key|p12|pfx)$'
```

Any output means sensitive files are **already tracked** — they need to be removed from git (see Secret Rotation Workflow below).

### Verify .gitignore entries exist

```bash
for pattern in '.env*' '*.pem' '*.key' '*.p12' '*.pfx' 'credentials.json' 'service-account*.json'; do
  grep -q "$pattern" .gitignore 2>/dev/null && echo "OK: $pattern" || echo "MISSING: $pattern"
done
```

---

## Secret Rotation Workflow

When a leaked key is found, follow these steps **in order**:

1. **Revoke the exposed credential immediately.** Do not wait for cleanup — revoke first. Every minute of delay is exposure.
2. **Generate a new credential** from the provider's console/API.
3. **Update all systems** using the credential (CI/CD, environment variables, secrets managers, deployed services).
4. **Remove from git history** using one of:
   - `git filter-repo --path-glob '*.env' --invert-paths` (recommended)
   - BFG Repo-Cleaner: `bfg --delete-files '*.env'`
5. **Force push cleaned history** — coordinate with the team first (`git push --force-with-lease --all`).
6. **Audit access logs** for unauthorized use during the exposure window. Check the provider's audit/access logs for the compromised credential.
7. **Document the incident** — what was exposed, when, duration of exposure, whether unauthorized access occurred, and what was done to remediate.

---

## Recommended Tools

| Tool | Approach | Best For |
|---|---|---|
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | Entropy + regex, git history aware, verified-only mode | Deep git history scanning; `--only-verified` reduces false positives |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Regex with TOML config, fast | CI/CD pipelines; pre-commit hooks |
| [GitGuardian](https://www.gitguardian.com/) | SaaS, real-time monitoring, ML-based | Org-wide monitoring; public leak detection |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | Baseline approach (Yelp) | Incremental adoption; tracks known secrets to reduce noise |
