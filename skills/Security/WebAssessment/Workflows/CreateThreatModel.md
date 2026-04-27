# Create Threat Model Workflow

Generates prioritized attack scenarios and test plans from application understanding using structured threat modeling frameworks (STRIDE, DREAD, PASTA).

## Trigger Conditions

**Automatic — prompt user when detected:**
- New project with external-facing components (web app, API, service)
- Pre-deploy to production for the first time
- New external API integration or third-party service dependency
- Architecture change that modifies trust boundaries

**Manual:**
- "create threat model", "threat model this app"
- "STRIDE analysis", "DREAD scoring", "PASTA threat model"
- "what are the attack scenarios", "how would I attack this"
- "generate attack plan", "prioritize testing"

**Ideal (not yet automated):** When the Security skill detects the above conditions, prompt: "This looks like a good moment for threat modeling. Run STRIDE analysis?" Currently relies on manual invocation or Algorithm phase routing.

## Purpose

After understanding an application, generate a structured threat model that:
1. **STRIDE pass** — systematically enumerate threats per component/boundary
2. **DREAD score** — prioritize threats by risk dimensions
3. Maps threats to OWASP and CWE classifications
4. Creates realistic attack paths (optionally using PASTA for complex systems)
5. Produces a prioritized test plan

## Prerequisites

Run **UnderstandApplication** workflow first, or have equivalent context about:
- Technology stack
- User roles and access levels
- User flows and sensitive data
- Attack surface (inputs, APIs, file uploads, etc.)

## Output Structure

Produce a markdown document with these sections:

```markdown
# Threat Model: [Target]

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Threats | [N] |
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |

**Top Categories:** [List top 3-5 threat categories]

## Attack Paths

### [Attack Path Name]
**Description:** [What attacker achieves]
**Required Access:** [None/Authenticated/Privileged]
**Target Asset:** [What's being attacked]

**Steps:**
1. [First step]
2. [Second step]
...

**Related Threats:** [List threat IDs]

## Prioritized Test Plan

| Priority | Threat | Tests | Tools | Effort |
|----------|--------|-------|-------|--------|
| 1 | [Name] | [Brief test description] | [Tool suggestions] | [quick/medium/extensive] |
| 2 | ... | ... | ... | ... |

## Threat Details

### T1: [Threat Name]
**Category:** [Authentication/Access Control/Injection/etc.]
**OWASP:** [A01-A10 category]
**CWE:** [CWE-XXX]
**Impact:** [low/medium/high/critical]
**Likelihood:** [low/medium/high]
**Risk Score:** [Impact × Likelihood]

[Description of the threat]

**Attack Vector:** [How it's exploited]
**Target Component:** [What part of app]

**Prerequisites:**
- [What's needed to attempt this]

**Test Cases:**
- [Specific test to perform]
- [Another test]

**Mitigations:**
- [How to fix/prevent]
```

## Threat Categories

Apply threats based on attack surface characteristics:

### Authentication (apply when auth exists)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Credential Stuffing | A07 | CWE-307 | High | High |
| Session Hijacking | A07 | CWE-384 | High | Medium |
| JWT Token Manipulation | A07 | CWE-287 | Critical | Medium |
| Password Reset Flaws | A07 | CWE-640 | High | Medium |

### Access Control (apply when multiple roles exist)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Horizontal Privilege Escalation | A01 | CWE-639 | High | High |
| Vertical Privilege Escalation | A01 | CWE-269 | Critical | Medium |
| Forced Browsing | A01 | CWE-425 | Medium | Medium |

### Injection (apply to all web apps)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| SQL Injection | A03 | CWE-89 | Critical | Medium |
| Cross-Site Scripting (XSS) | A03 | CWE-79 | Medium | High |
| Command Injection | A03 | CWE-78 | Critical | Low |
| Server-Side Request Forgery | A10 | CWE-918 | High | Medium |

### Data Exposure (apply when sensitive data exists)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Sensitive Data in Transit | A02 | CWE-319 | High | Medium |
| Information Disclosure | A05 | CWE-200 | Medium | High |

### File Upload (apply when upload exists)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Unrestricted File Upload | A04 | CWE-434 | Critical | Medium |
| Path Traversal via Upload | A01 | CWE-22 | High | Medium |

### API Security (apply when APIs exist)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Broken Object Level Authorization | A01 | CWE-639 | High | High |
| Excessive Data Exposure | A01 | CWE-213 | Medium | High |
| Mass Assignment | A08 | CWE-915 | High | Medium |

### WebSocket (apply when websockets exist)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| WebSocket Hijacking | A07 | CWE-346 | High | Medium |
| WebSocket Injection | A03 | CWE-79 | Medium | Medium |

### Business Logic (apply to all web apps)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Business Logic Bypass | A04 | CWE-840 | High | Medium |
| Race Condition Exploitation | A04 | CWE-362 | High | Low |

### Payment Security (apply when payment flows exist)
| Threat | OWASP (2021) | CWE | Impact | Likelihood |
|--------|-------|-----|--------|------------|
| Payment Manipulation | A04 | CWE-472 | Critical | Medium |

## Attack Paths to Consider

Based on threats, generate realistic attack paths:

1. **Account Takeover** - Credential stuffing → session hijacking → account access
2. **Data Exfiltration** - IDOR → API data exposure → sensitive data theft
3. **Privilege Escalation** - Low priv access → role manipulation → admin access
4. **Payment Fraud** - Price manipulation → race conditions → financial theft

## Tool Suggestions by Category

| Category | Tools |
|----------|-------|
| Authentication | Burp Suite, ffuf, Hydra |
| Access Control | Burp Autorize, manual testing |
| Injection | sqlmap, Burp Suite, XSS Hunter |
| Data Exposure | testssl.sh, curl, Burp |
| File Upload | Burp Suite, custom scripts |
| API Security | Postman, Burp, API fuzzer |
| WebSocket | Burp Suite, websocat |
| Business Logic | Manual testing, Burp Repeater |

## Risk Scoring

Calculate risk score: `Impact × Likelihood`

| Impact | Score |
|--------|-------|
| Low | 1 |
| Medium | 2 |
| High | 3 |
| Critical | 4 |

| Likelihood | Score |
|------------|-------|
| Low | 1 |
| Medium | 2 |
| High | 3 |

Risk Score ranges: 1-3 (Low), 4-6 (Medium), 7-9 (High), 10-12 (Critical)

## STRIDE Framework (Mandatory First Pass)

For each component, trust boundary, or data flow in the application, systematically evaluate all six STRIDE categories. Do not skip categories — the value is in forced completeness.

**Identifying targets:** Use the data flow diagram from **UnderstandApplication** output to identify components and trust boundaries. If no DFD exists, enumerate: entry points (user inputs, API endpoints), data stores (DB, files, caches), external services, and the boundaries between them.

| Category | Question | Typical Threats |
|----------|----------|-----------------|
| **S — Spoofing** | Can an attacker impersonate a user, service, or component? | Credential theft, session hijacking, API key abuse, IP spoofing |
| **T — Tampering** | Can data be modified in transit or at rest? | SQL injection, parameter manipulation, MITM, file modification |
| **R — Repudiation** | Can an attacker deny performing an action? | Missing audit logs, unsigned transactions, log injection |
| **I — Information Disclosure** | Can sensitive data leak? | Error messages, directory listing, API over-exposure, timing attacks |
| **D — Denial of Service** | Can service availability be disrupted? | Resource exhaustion, algorithmic complexity, rate limit bypass |
| **E — Elevation of Privilege** | Can an attacker gain higher access? | IDOR, role manipulation, JWT claim tampering, privilege escalation |

### STRIDE Output Format

```markdown
## STRIDE Analysis: [Component/Boundary]

| Category | Applicable? | Threat Description | Severity |
|----------|------------|-------------------|----------|
| Spoofing | Yes/No | [specific threat] | Critical/High/Medium/Low |
| Tampering | Yes/No | [specific threat] | ... |
| Repudiation | Yes/No | [specific threat] | ... |
| Info Disclosure | Yes/No | [specific threat] | ... |
| Denial of Service | Yes/No | [specific threat] | ... |
| Elevation of Privilege | Yes/No | [specific threat] | ... |
```

Repeat for each component or trust boundary. Typical targets: auth boundary, API gateway, database layer, external service integrations, file upload handler, user input processors.

## DREAD Scoring (Prioritization)

After identifying threats via STRIDE, score each for prioritization using DREAD dimensions (1-10 scale each):

| Dimension | Question | Low (1-3) | Medium (4-6) | High (7-10) |
|-----------|----------|-----------|-------------|-------------|
| **D — Damage** | How bad if exploited? | Minor data leak | Partial data breach | Full system compromise |
| **R — Reproducibility** | How easy to reproduce? | Complex conditions | Moderate setup | Trivially reproducible |
| **E — Exploitability** | How easy to exploit? | Requires deep expertise | Moderate skill needed | Script kiddie level |
| **A — Affected Users** | How many users impacted? | Single user | Subset of users | All users |
| **D — Discoverability** | How easy to find? | Requires insider knowledge | Moderate effort | Publicly visible |

**DREAD Score** = (D + R + E + A + D) / 5 → Range 1-10

**Note on Discoverability:** Some practitioners drop this dimension (using DREA scoring) because it can reward security through obscurity. For external-facing applications, consider scoring Discoverability as 10 (assume attackers will find it) to avoid false comfort.

**Note on DREAD vs CVSS:** DREAD is optimized for quick internal prioritization by a solo developer. For external reporting or professional security assessments, map findings to CVSS 3.1 scores instead.

| Score Range | Priority | Action |
|-------------|----------|--------|
| 8-10 | Critical | Fix before deploy |
| 5-7 | High | Fix in current sprint |
| 3-4 | Medium | Schedule for next sprint |
| 1-2 | Low | Track and monitor |

## PASTA Deep Mode (Optional — Complex Systems)

For complex systems with multiple stakeholders, use PASTA (Process for Attack Simulation and Threat Analysis) as a 7-stage deep analysis. Invoke with "PASTA threat model" or when the system has 3+ trust boundaries, handles regulated data (PCI, HIPAA, SOX), or has multi-tenant isolation requirements.

1. **Define objectives** — business goals, compliance requirements, risk appetite
2. **Define technical scope** — system architecture, data flows, trust boundaries
3. **Application decomposition** — DFDs, entry points, assets, privilege levels
4. **Threat analysis** — STRIDE per component (already done above), plus threat intelligence
5. **Vulnerability analysis** — map threats to known CVEs, CWEs, and OWASP categories
6. **Attack modeling** — build attack trees with realistic multi-step scenarios
7. **Risk/impact analysis** — DREAD scoring (already done above), residual risk assessment

PASTA is the full ceremony. Use STRIDE + DREAD for most projects; escalate to PASTA for systems handling financial data, PII at scale, or multi-tenant architectures.

## Workflow Execution

1. **Review application understanding** — Load UnderstandApplication output
2. **Identify applicable threat categories** — Match attack surface to the catalog tables above (known threats)
3. **Run STRIDE per component** — Systematically find threats the catalog misses (mandatory)
4. **Merge and deduplicate** — Combine catalog threats + STRIDE-discovered threats
5. **Score ALL threats with DREAD** — Uniform prioritization across all threats (mandatory)
6. **Generate attack paths** — Create realistic multi-step scenarios
7. **Prioritize test plan** — Order by DREAD score, effort, quick wins
8. **Produce output** — Generate structured markdown document
9. **Optional: PASTA** — If complex system, run full 7-stage analysis

**Which score to use:** DREAD is the primary prioritization score. The Impact x Likelihood matrix in the Threat Details template is a simplified view for executive summaries. When both exist, DREAD score takes precedence for test plan ordering.

## Output Location

Save threat model to:
`../Data/{client}/threat-model.md`

Or return inline for immediate use in testing.

## Integration with PromptInjection Skill

If application uses LLMs/AI:
- Add prompt injection threats
- Reference PromptInjection skill for specialized testing
- Include indirect injection scenarios
