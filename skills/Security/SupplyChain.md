# Supply Chain Security

Detect malicious, compromised, or risky dependencies before they enter your project.

---

## When to Use

- Adding new dependencies to a project
- Periodic dependency audit (monthly or before releases)
- Investigating suspicious package behavior
- Pre-deploy verification

---

## Audit Commands by Ecosystem

| Ecosystem | Audit Command | Catches | Misses |
|-----------|---------------|---------|--------|
| npm/Bun | `npm audit` / `bun audit` (if available, else `npm audit`) | Known CVEs in npm advisory DB | Zero-days, malicious packages without CVEs, typosquats |
| pip | `pip-audit` or `safety check` | Known CVEs in PyPI | Malicious PyPI packages, namespace confusion |
| Go | `govulncheck ./...` | Known vulns in Go vuln DB | Malicious modules, typosquats |
| Rust | `cargo audit` | RustSec advisories | Supply chain attacks not in RustSec |
| Ruby | `bundle audit` | Ruby advisory DB | Gem squatting, malicious gems |

**Key insight:** Audit tools only catch *known* vulnerabilities with assigned CVEs. They are necessary but not sufficient. The behavioral indicators below cover what audit tools miss.

---

## Behavioral Indicators Beyond CVE Databases

These are red flags that audit tools will never catch:

### Maintainer Transfer
Package ownership changed recently. Check with:
```bash
npm info <pkg> maintainers
```
A package that changed hands in the last 90 days warrants extra scrutiny — especially if the new maintainer has no other packages.

### Sudden Version Bumps
Major version jump with minimal changelog. A jump from 1.2.3 to 4.0.0 with a one-line changelog is suspicious — legitimate major bumps come with migration guides and detailed notes.

### Undocumented Install Scripts
Check `preinstall`, `postinstall`, and `prepare` scripts in package.json:
```bash
npm show <pkg> scripts
```
Legitimate install scripts compile native addons. Illegitimate ones download and execute remote code.

### Network Requests During Install
Monitor with `strace` or network tools during install:
```bash
strace -f -e trace=network npm install <pkg> 2>&1 | grep connect
```
No package should be phoning home during installation.

### Typosquatting
Similar names to popular packages. Examples:
- `lodahs` vs `lodash`
- `coler` vs `color`
- `crossenv` vs `cross-env`

Always double-check spelling before installing.

### Unpinned Dependencies
`"*"` or `"latest"` in package.json — pins should be exact or range-limited. Unpinned deps mean any future publish (including malicious ones) will be pulled automatically.

### Minified-Only Source
npm package contains only minified JS with no readable source. Legitimate packages publish readable code. Minified-only packages are hiding something.

### Zero-Star / New Publisher
First-time publisher with no history, no other packages, no GitHub presence. Not inherently malicious, but combined with other signals it is a strong indicator.

### Publish Date vs Commit Date Mismatch
Package published from code much newer or older than the linked repo. Check with:
```bash
npm view <pkg> time
```
If the published version doesn't correspond to any tagged commit in the repo, the published code may differ from the repo code.

---

## Manual Verification Steps

1. **Compare scripts in npm vs GitHub repo:**
   ```bash
   npm show <pkg> scripts
   ```
   Then check the same `package.json` on the GitHub repo. Differences in `preinstall`/`postinstall` are a critical red flag.

2. **Check if published tarball matches repo code:**
   ```bash
   npm pack <pkg>
   tar -xzf <pkg>-<version>.tgz
   # diff against cloned repo
   ```

3. **Review install scripts:**
   ```bash
   npm show <pkg> scripts
   ```

4. **Check publish history:**
   ```bash
   npm view <pkg> time
   ```
   Look for irregular publish cadence — a package dormant for 2 years that suddenly publishes 3 versions in a day.

5. **Look at download trends:**
   Check npmjs.com or bundlephobia. Sudden spikes on unknown packages are suspicious — may indicate a dependency injection attack upstream.

6. **Verify GitHub repo link:**
   Confirm the `repository` field in package.json actually exists and the code matches what is published to npm.

---

## When to Be Suspicious

Quick-reference checklist:

- [ ] Package has < 100 weekly downloads but claims broad utility
- [ ] Publisher account created recently (< 30 days)
- [ ] Package name is one character off from a popular package
- [ ] No GitHub/source repo linked
- [ ] Install scripts make network requests
- [ ] Dependencies pull in unexpected native modules
- [ ] README is copy-pasted from another package

If **two or more** of these are true, do not install without thorough manual verification.

---

## Lockfile Hygiene

- **Always commit lockfiles** — `package-lock.json`, `bun.lockb`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`, etc.
- **Review lockfile diffs in PRs** — unexpected dependency changes (new transitive deps, version jumps you didn't request) are a signal worth investigating.
- **Use `npm ci` (not `npm install`) in CI** — this ensures the lockfile is authoritative and CI builds are reproducible. `npm install` can silently update the lockfile.
