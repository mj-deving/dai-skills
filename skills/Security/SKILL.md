---
name: Security
description: Security assessment — network recon, web app testing, prompt injection testing, security news, and vulnerability scanning. USE WHEN recon, port scan, subdomain, DNS, WHOIS, pentest, threat model, OWASP, prompt injection, LLM security, security news, trivy, CVE, vulnerability scan, sops, encrypt secrets.
---

# Security

Unified skill for security assessment and intelligence workflows.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Recon, reconnaissance, port scan, subdomain, DNS, WHOIS, ASN | `Recon/SKILL.md` |
| Web assessment, OWASP, pentest, ffuf, app security, threat modeling, STRIDE, DREAD, PASTA, threat model | `WebAssessment/SKILL.md` |
| Prompt injection, jailbreak, LLM security, guardrail bypass | `PromptInjection/SKILL.md` |
| Security news, sec updates, breaches, tldrsec, security research | `SECUpdates/SKILL.md` |
| Annual reports, security trends, threat landscape, vendor reports | `AnnualReports/SKILL.md` |
| Secure coding, vulnerability prevention, defense patterns, security review code | `SecureCoding/SKILL.md` |
| Supply chain, dependency audit, package security, new dependency check | `SupplyChain.md` |
| Secret audit, scan for secrets, find leaked keys, git history secrets | `SecureCoding/SKILL.md` |
| Trivy, vulnerability scan, CVE, container scan, IaC scan | See **Trivy Vulnerability Scanning** below |
| sops, encrypt secrets, decrypt secrets | See **sops Secrets Management** below |

## Trivy Vulnerability Scanning

Scan projects, containers, and infrastructure-as-code for known vulnerabilities.

```bash
# Scan project directory for CVEs
trivy fs --format json . | jq '.Results[] | select(.Vulnerabilities) | .Vulnerabilities[] | select(.Severity == "CRITICAL")'

# Scan container image
trivy image --format json myapp:latest

# Scan IaC (Terraform, CloudFormation)
trivy config --format json ./infrastructure/

# CI gate — fail on critical
trivy fs --exit-code 1 --severity CRITICAL .
```

**When to use:**
- Before deploying — scan the project for known CVEs
- Container builds — scan images before pushing to registry
- IaC review — catch misconfigurations in Terraform/CloudFormation before apply
- CI pipelines — add `--exit-code 1` to fail the build on critical findings

**Triage approach:**
1. Run `trivy fs --format json .` to get full results
2. Filter to CRITICAL and HIGH severity first
3. Check if vulnerable code paths are actually reachable
4. Update dependencies where possible, document accepted risks where not

## sops Secrets Management

Encrypt and decrypt secrets files using Mozilla sops with age keys.

```bash
# Encrypt a file with age key
sops --encrypt --age age1... secrets.yaml > secrets.enc.yaml

# Decrypt
sops --decrypt secrets.enc.yaml

# Edit encrypted file in place
sops secrets.enc.yaml
```

**When to use:**
- Storing secrets in git — encrypt with sops so they can be version-controlled safely
- Sharing secrets across team/agents — encrypted files can be committed and shared
- Rotating secrets — edit in place with `sops secrets.enc.yaml`

**Rules:**
- Never commit unencrypted secrets files
- Use age keys (not PGP) for new setups — simpler key management
- Store the age key outside the repo (e.g., `~/.config/sops/age/keys.txt`)

## Examples

**Example 1:** `User: "[typical request]"` → Routes to appropriate sub-skill workflow

**Example 2:** `User: "[another request]"` → Routes to different sub-skill workflow
