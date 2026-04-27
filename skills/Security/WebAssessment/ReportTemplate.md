# Security Assessment Report Template

Standardized format for documenting security findings from assessments, pentests, and code reviews.

---

## Finding Format

Each finding should use this structure:

### [SEVERITY] Finding Title

| Field | Value |
|-------|-------|
| **Severity** | Critical / High / Medium / Low / Info |
| **CVSS Score** | X.X (vector string) |
| **CWE** | CWE-XXX: Name |
| **OWASP** | A0X:20XX Category |
| **Location** | URL/file path/endpoint |
| **Status** | Open / Remediated / Accepted Risk |

**Description:** What the vulnerability is and how it was discovered.

**Evidence:** Steps to reproduce, screenshots, request/response pairs, code snippets.

**Impact:** What an attacker could achieve by exploiting this.

**Remediation:** Specific fix recommendations with code examples where applicable.

**References:** Links to CWE, OWASP, vendor advisories, or related documentation.

---

## Severity Definitions

| Severity | CVSS Range | Description | Example |
|----------|-----------|-------------|---------|
| Critical | 9.0-10.0 | Remote code execution, auth bypass, data breach | Unauthenticated SQLi on login |
| High | 7.0-8.9 | Significant data access, privilege escalation | Stored XSS in admin panel |
| Medium | 4.0-6.9 | Limited impact, requires interaction | CSRF on profile update |
| Low | 0.1-3.9 | Minimal direct impact | Verbose error messages |
| Info | 0.0 | Best practice recommendations | Missing security headers |

---

## SLA Timelines

Remediation deadlines by severity:

| Severity | SLA | Escalation |
|----------|-----|------------|
| Critical | 24 hours | Immediate exec notification |
| High | 7 days | Team lead notification |
| Medium | 30 days | Sprint planning |
| Low | 90 days | Backlog |
| Info | No SLA | Optional improvement |

---

## Report Summary Template

```markdown
# Security Assessment Report

## Executive Summary
- **Target:** [Application/system name and version]
- **Scope:** [What was tested — URLs, APIs, source code paths]
- **Date Range:** [Assessment period]
- **Methodology:** [OWASP Testing Guide, custom, etc.]
- **Overall Risk:** [Critical / High / Medium / Low]

## Findings Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| Info | X |

## Top 3 Priority Findings
1. [Most critical finding — one line]
2. [Second — one line]
3. [Third — one line]

## Positive Findings
- [Security controls that ARE working well]
- [Good practices observed]

## Detailed Findings
[Individual findings using the format above]

## Appendix
- Tools used
- Testing accounts and access levels
- Out-of-scope items
```

---

## Integration Note

For threat modeling output format, see `CreateThreatModel.md` in WebAssessment/Workflows/. This template is for assessment reporting, not threat modeling — they complement each other but serve different purposes.
