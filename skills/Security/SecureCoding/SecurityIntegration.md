# VibeSec Security Integration — Reference Documentation

**Version:** 1.0 | **Date:** 2026-03-23 | **Status:** Phase 1 (warn-only)

## Overview

Three-layer defense-in-depth integration of VibeSec-Skill security knowledge into PAI:

| Layer | Mechanism | Location | Purpose |
|-------|-----------|----------|---------|
| 1 | Knowledge Injection | `${SKILLS_HOME}/Security/SecureCoding/` | LLM generates secure code because security context is in prompt |
| 2 | Skill Workflows | `SecureCoding/Workflows/` | Human/Algorithm invokes structured security review |
| 3 | Active Enforcement | `${AGENT_HOME}/hooks/SecurityValidator.hook.ts` | Hook catches vulnerable patterns before disk write |

**Source:** [BehiSecc/VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) (Apache 2.0, ~25KB)

---

## Layer 1: Knowledge Injection

### Architecture

SecureCoding is a sub-skill under the Security umbrella (`${SKILLS_HOME}/Security/`). It uses PAI's dynamic loading pattern — minimal SKILL.md with domain-specific context files loaded on demand.

```
${SKILLS_HOME}/Security/SecureCoding/
├── SKILL.md                  # Routing + frontmatter (3.6KB)
├── AccessControl.md          # IDOR, privilege escalation, mass assignment (3.8KB)
├── ClientSide.md             # XSS, CSRF, open redirects, prototype pollution (5.8KB)
├── ServerSide.md             # SSRF, file uploads, SQLi, XXE, path traversal (7.3KB)
├── AuthSessions.md           # JWT attacks, password storage, timing attacks (5.6KB)
├── ApiSecurity.md            # Mass assignment, GraphQL, rate limiting (5.3KB)
├── BypassTechniques.md       # 38+ consolidated bypass techniques (6.0KB)
├── SecurityIntegration.md    # This document
├── SecretAudit.md            # Secret detection in git history + codebases
├── Tools/                    # Empty (convention)
└── Workflows/
    ├── CodeReview.md         # 5-step security review (1.9KB)
    └── SecureDesign.md       # 4-step threat modeling (1.7KB)
```

### Content Mapping

VibeSec content is included **in full** — all languages, all examples, all tables:
- **Included verbatim:** All VibeSec content — Java, Python, PHP, Node.js, .NET examples
- **Added as `## PAI Extensions`:** Cloudflare Workers patterns (D1, KV, Hono middleware) appended at the end of each domain file
- **Added (beyond VibeSec):** Prototype pollution, rate limiting, timing attacks, ReDoS

| Domain File | VibeSec Source Sections | PAI Extensions |
|------------|----------------------|----------------|
| AccessControl.md | Access Control Issues | D1 tenant isolation, Hono middleware |
| ClientSide.md | XSS, CSRF, Secret Keys, Open Redirect, Password | Prototype pollution |
| ServerSide.md | SSRF, File Upload, SQLi, XXE, Path Traversal | D1 parameterized queries, ReDoS |
| AuthSessions.md | JWT Security, Password Security | Timing attacks (timingSafeEqual), token revocation |
| ApiSecurity.md | API Security (Mass Assignment, GraphQL) | Rate limiting with KV, security headers |
| BypassTechniques.md | All bypass sections consolidated | Defense guidance per technique |

### How It Works

When security context is relevant (user says "secure code", "security review", etc.), PAI's skill system activates SecureCoding. The SKILL.md loads, and workflows reference domain context files on demand — only loading what's needed.

The Security umbrella routes to SecureCoding via:
```
| Secure coding, vulnerability prevention, defense patterns, security review code | `SecureCoding/SKILL.md` |
```

**Boundary with WebAssessment:** SecureCoding = writing secure code (proactive). WebAssessment = testing existing apps (reactive). The USE WHEN triggers intentionally exclude "OWASP" to avoid routing ambiguity.

---

## Layer 2: Skill Workflows

### CodeReview Workflow

**Trigger:** "security review", "check for vulnerabilities", "secure code review"

**5-step process:**
1. **Gather Code** — Read file, directory, or git diff
2. **Detect Relevant Domains** — Scan for SQL, JWT, innerHTML, fetch, upload, role/permission patterns → load matching context files
3. **Review Against Patterns** — Check code against prevention checklists and known vulnerable patterns
4. **Output Findings** — Structured table: severity, domain, location, issue, fix
5. **Offer Fixes** — Optionally apply fixes with user confirmation

**Example invocation:**
```
User: "security review packages/api/src/routes/items.ts"
→ Detects SQL patterns → loads ServerSide.md
→ Detects auth patterns → loads AccessControl.md
→ Returns findings table
```

### SecureDesign Workflow

**Trigger:** "secure design", "threat model feature", "security architecture"

**4-step process:**
1. **Load All Domain Context** — Design review needs full coverage
2. **Identify Attack Surfaces** — Map feature to vulnerability domains
3. **Threat Model** — For each surface: what can attacker do? what controls needed?
4. **Output Recommendations** — Attack surface table + required controls + VibeSec patterns

### Algorithm Integration

SecureCoding is a selectable capability in Algorithm's OBSERVE phase. Auto-selected when:
- Task involves API endpoints, authentication, or data handling
- Project has security-sensitive data
- Task modifies auth middleware, database queries, or external integrations

---

## Layer 3: Active Enforcement

### Architecture

Extends `SecurityValidator.hook.ts` with a new scanner alongside the existing secret scanner:

```
handleFileWrite()
├── scanContentForSecrets()           ← existing (blocks API keys, credentials)
├── scanContentForVulnerabilities()   ← NEW (warns/blocks code patterns)
└── validatePath()                    ← existing (path access control)
```

### Patterns

**7 BLOCK patterns** (high confidence — always dangerous):

| Pattern | Name | What It Catches |
|---------|------|----------------|
| `eval(req.body...)` | eval-user-input | eval() with user-controlled input |
| `db.query(\`...${}\`)` | sql-template-literal | SQL template literal injection (DB prefix required) |
| `db.query("..." + req.body)` | sql-string-concat | SQL string concatenation with user input |
| `algorithms: ['none']` | jwt-alg-none | JWT algorithm "none" acceptance |
| `exec("..." + req.body)` | command-injection | exec() with user input (single-line constraint) |
| `new Function(req.body)` | function-constructor-injection | Function constructor with user input |
| `['__proto__'] =` | prototype-pollution | Prototype pollution via assignment (not comparison) |

**7 WARN patterns** (context-dependent — may be intentional):

| Pattern | Name | What It Catches |
|---------|------|----------------|
| `dangerouslySetInnerHTML` | dangerous-inner-html | Any dangerouslySetInnerHTML usage |
| `.innerHTML =` | inner-html-assignment | Any innerHTML assignment |
| `rejectUnauthorized: false` | tls-verification-disabled | TLS cert verification disabled |
| `cors = '*'` | cors-wildcard | CORS wildcard origin |
| `jwt...verify: false` | crypto-verification-disabled | JWT/crypto verification disabled |
| `console.log(env.KEY)` | env-var-exposure | Env var in logs/response (both orders) |
| `obj[req.body.key] =` | dynamic-property-assignment | Dynamic property with user input |

### Design Decisions

**DB prefix requirement (C1 fix):** SQL patterns require `db.`, `stmt.`, `pool.`, `D1.` etc. before `query()`/`run()`. Without this, `test.run(\`suite ${name}\`)` would false-positive.

**Assignment context for __proto__ (H2 fix):** Pattern requires `['__proto__'] =` or `__proto__:` (assignment), not `=== '__proto__'` (comparison). Defensive code checking for prototype pollution is NOT blocked.

**Both-order env check (H3 fix):** Checks `console.log(env.KEY)` AND `env.KEY...res.json()` — the most common pattern has the output method first.

**endsWith for exemptions (C2 fix):** Extension-based exemptions use `endsWith()` not `includes()`. A path containing `.md` in a directory name (e.g., `.mdx-components/evil.ts`) is NOT exempt.

### Exempt Paths

| Type | Exemptions | Method |
|------|-----------|--------|
| Extensions | `.test.ts`, `.test.js`, `.spec.ts`, `.spec.js`, `.example`, `.sample`, `.md` | `endsWith()` |
| Directories | `/.claude/hooks/`, `/.claude/skills/`, `/migrations/`, `/node_modules/` | `includes()` |
| Specific | *(removed — VibeSecSource retired)* | — |

**Asymmetry with SECRET_SCAN_EXEMPT_PATHS is intentional:** Secrets in migration files SHOULD be caught (a DB password in a migration is a leak). Vuln patterns in migrations should NOT (SQL in migrations is expected).

### Phased Rollout

Controlled by `VULN_ENFORCEMENT_PHASE` constant in SecurityValidator.hook.ts:

| Phase | Constant | Behavior | Promotion Criteria |
|-------|----------|----------|-------------------|
| 1 (current) | `= 1` | All 14 patterns → WARN (stderr only) | 20+ sessions with <5% false positive rate |
| 2 | `= 2` | Top patterns BLOCK, rest WARN | 20 more clean sessions |
| 3 | `= 3` | Full enforcement per pattern severity | Ongoing |

**To promote:** Edit `SecurityValidator.hook.ts`, change `VULN_ENFORCEMENT_PHASE` from `1` to `2` (or `3`).

---

## Testing

### How to Run Tests

```bash
# Run ALL security validator tests (baseline + agent + vuln patterns)
cd ${AGENT_HOME} && bun hooks/tests/security-validator.test.ts

# Expected output: 44 passed, 0 failed
```

### Test Coverage

| Category | Tests | What They Verify |
|----------|-------|-----------------|
| Baseline (B1-B8) | 8 | Existing bash/path security unchanged |
| Agent Policy (P1-P15) | 15 | Per-agent access control unchanged |
| Vuln True Positive (V1-V12) | 12 | Each pattern fires on vulnerable code |
| Vuln False Positive (V13-V17) | 5 | Safe code does NOT trigger patterns |
| Vuln Exempt Paths (V18-V21) | 4 | Exempt paths work, bypass attempts fail |
| **Total** | **44** | |

### Key Test Cases

```
V1:  eval(req.body.code)           → WARN (true positive)
V13: eval('2 + 2')                 → no match (no user input)
V15: test.run(`suite ${name}`)     → no match (no DB prefix)
V16: if (key === '__proto__')      → no match (comparison, not assignment)
V20: .mdx-components/evil.ts       → NOT exempt (endsWith check works)
```

---

## Known Limitations

### Fundamental

1. **Variable indirection bypasses all patterns.** `const cmd = req.body.x; exec(cmd)` is vulnerable but undetectable by regex. Layer 1 (knowledge) and Layer 2 (workflow review) must catch these.

2. **Edit tool partial content.** Edit sends only `new_string` to the hook. A vulnerable pattern split across `old_string` and `new_string` will be missed.

3. **No AST parsing.** Regex cannot understand code structure — it matches text patterns. Context-aware patterns (DB prefix, assignment context) mitigate this but can't eliminate it.

### Coverage Gaps

| Gap | Risk | Mitigation |
|-----|------|------------|
| Template injection (Handlebars, EJS) | MEDIUM | Not in current stack (React/Next.js) |
| Business logic flaws | HIGH | Not automatable — requires human review |
| Supply chain / dependencies | MEDIUM | Use `bun audit` separately |
| Insecure deserialization | LOW | JSON.parse is safe for JS |

---

## How to Add New Patterns

### Adding a BLOCK Pattern

1. Add to `VULN_BLOCK_PATTERNS` array in `SecurityValidator.hook.ts`:
```typescript
{
  pattern: /your-regex-here/,     // NEVER use `g` flag
  name: 'descriptive-name',
  description: 'What it catches — risk description'
},
```

2. Add domain hint in `handleFileWrite`'s `domainHints` map:
```typescript
'descriptive-name': 'RelevantDomain.md',
```

3. Add test cases in `security-validator.test.ts`:
   - True positive: code that SHOULD trigger
   - False positive: safe code that should NOT trigger

4. Run tests: `cd ${AGENT_HOME} && bun hooks/tests/security-validator.test.ts`

### Rules for Pattern Design

- **Never use `g` flag** — causes intermittent false negatives via lastIndex state
- **Use `[^\n]*` not `.*`** — constrains to single line, prevents cross-line false matches
- **Require context** — prefix with user-input indicators (`req.`, `ctx.`, `body.`) to avoid matching safe code
- **Avoid nested quantifiers** — risk of ReDoS in the security tool itself
- **Test both directions** — verify true positive AND false positive resistance

### Adding Knowledge Content

Add or update domain context files in `${SKILLS_HOME}/Security/SecureCoding/`. Follow the format:
```markdown
# Domain Name
## Vulnerability Overview
## Attack Vectors
## Bypass Techniques (tables)
## Prevention Checklist
## Code Examples (TypeScript/Node.js only)
```

---

## History

| Date | Change | Review |
|------|--------|--------|
| 2026-03-23 | Initial implementation — 3 layers, 14 patterns, Phase 1 | Dual-reviewed by Intern + Codex agents |
| | Intern review: 16 fixes (critical regex bug, prototype pollution, exempt paths) | |
| | Codex review: 19 fixes (DB prefix, endsWith, Phase 1 logic, env-var order) | |
