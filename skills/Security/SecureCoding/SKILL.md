---
name: SecureCoding
description: Proactive secure coding — vulnerability patterns, bypass techniques, defense-in-depth for TypeScript and Cloudflare Workers. USE WHEN secure code, code security, vulnerability prevention, secure coding review, defense in depth, XSS prevention, SQL injection prevention, SSRF prevention, JWT security, access control patterns, API security patterns, secure design, security review code, prototype pollution.
---

# SecureCoding

Proactive security guidance adapted from VibeSec-Skill. Bug bounty hunter perspective —
teaches attack patterns so you build defenses that actually work.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/SecureCoding/`

<!-- ## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the SecureCoding skill to ACTION", "voice_id": "fTtv3eikoepIosk8dTZ5"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **SecureCoding** skill to ACTION...
   ```

**Full documentation:** `${PAI_HOME}/THENOTIFICATIONSYSTEM.md`
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CodeReview** | "security review", "check for vulnerabilities", "secure code review" | `Workflows/CodeReview.md` |
| **SecureDesign** | "secure design", "threat model feature", "security architecture" | `Workflows/SecureDesign.md` |
| **SecretAudit** | "secret audit", "scan for secrets", "find leaked keys", "git history secrets", "secret discovery" | `SecretAudit.md` |

## Quick Reference

**Approach:** Bug bounty perspective — think like an attacker, not just a defender
**Coverage:** Access control, client-side, server-side, auth/JWT, API security
**Focus:** TypeScript/Node.js, Cloudflare Workers (framework-specific)

## 3-Tier Security Decision Framework

Quick triage for any security-relevant code change:

**Always Do (no exceptions):**
- Validate all external input at system boundary (Zod/schema validation)
- Parameterize database queries (no string concatenation)
- Encode output to prevent XSS
- Hash passwords with bcrypt/scrypt/argon2
- Set security headers (CSP, HSTS, X-Frame-Options)
- Use httpOnly + secure + sameSite cookies for sessions
- Rate limit authentication endpoints

**Ask First (requires approval):**
- Authentication/authorization logic changes
- New sensitive data storage
- External service integrations
- CORS modifications
- File upload handling
- Permission model changes

**Never Do:**
- Commit secrets to version control
- Log sensitive data (passwords, tokens, PII)
- Rely on client-side validation for security
- Disable security headers
- Use `eval()` with user data
- Expose stack traces to users in production

## Dependency Auditing

Run periodically and before releases:

```bash
npm audit                    # Check for known vulnerabilities
npm audit --production       # Production deps only
```

**Triage by reachability:** A critical vulnerability in a dev-only dependency is lower priority than a moderate one in a production request handler. Focus on: (1) Is the vulnerable code path reachable? (2) Can an attacker trigger it? (3) What's the blast radius?

**Domain Context Files (loaded on demand):**
- `${CLAUDE_SKILL_DIR}/AccessControl.md` — IDOR, privilege escalation, mass assignment, multi-tenant
- `${CLAUDE_SKILL_DIR}/ClientSide.md` — XSS, CSRF, open redirects, secret exposure, prototype pollution
- `${CLAUDE_SKILL_DIR}/ServerSide.md` — SSRF, file uploads, SQLi, XXE, path traversal
- `${CLAUDE_SKILL_DIR}/AuthSessions.md` — JWT attacks, password storage, token management
- `${CLAUDE_SKILL_DIR}/ApiSecurity.md` — Mass assignment, GraphQL depth/complexity, introspection
- `${CLAUDE_SKILL_DIR}/BypassTechniques.md` — Consolidated bypass catalogs across all domains
- `${CLAUDE_SKILL_DIR}/SecretAudit.md` — Secret detection in git history, rotation workflow

## Examples

**Example 1: Security review of code changes**
```
User: "security review the changes in packages/api"
-> Invokes CodeReview workflow
-> Loads relevant domain context based on code content
-> Returns structured findings with severity, location, fix
```

**Example 2: Secure design for new feature**
```
User: "secure design for the webhook endpoint"
-> Invokes SecureDesign workflow
-> Loads all domain context files
-> Returns attack surfaces, recommended controls
```

## Known Gaps

- Template injection (Handlebars, EJS — not in current stack)
- LDAP injection (no LDAP in PAI projects)
- Insecure deserialization (JSON.parse is safe for JS)
- Business logic flaws (requires human review)
- Compliance frameworks (PCI DSS, HIPAA)
- Infrastructure/network security beyond SSRF

**Cross-references:**
- Supply chain security → `../SupplyChain.md`
- Secret auditing → `${CLAUDE_SKILL_DIR}/SecretAudit.md`
