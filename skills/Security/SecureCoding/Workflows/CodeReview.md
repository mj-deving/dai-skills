# CodeReview Workflow

## Input
- **Target**: file path, directory, or "current changes" (defaults to `git diff --cached`)
- **Scope**: "full" (all domains) or specific domain ("auth", "api", "client", etc.)

## Steps

### Step 1: Gather Code
- If file path: Read the file
- If directory: Glob for *.ts, *.tsx, *.js files, read each
- If "current changes": Run `git diff --cached` or `git diff`

### Step 2: Detect Relevant Domains
Scan code content for domain indicators:
| Pattern in Code | Load Context File |
|----------------|-------------------|
| SQL, query, D1, .prepare( | ServerSide.md |
| JWT, token, sign, verify | AuthSessions.md |
| innerHTML, dangerouslySet, CSP | ClientSide.md |
| fetch(url), webhook, proxy | ServerSide.md (SSRF) |
| upload, file, multer, formData | ServerSide.md (uploads) |
| role, admin, permission, authorize | AccessControl.md |
| GraphQL, mutation, introspection | ApiSecurity.md |
| (always load) | BypassTechniques.md |

### Step 3: Review Against Patterns
For each relevant domain context file:
1. Read the context file via `${CLAUDE_SKILL_DIR}/[FileName].md`
2. Check code against each prevention checklist item
3. Check for known vulnerable patterns
4. Cross-reference bypass techniques

### Step 4: Output Findings
```markdown
## Security Review: [target]

### Findings

| # | Severity | Domain | Location | Issue | Fix |
|---|----------|--------|----------|-------|-----|
| 1 | HIGH | SQLi | api/routes/items.ts:42 | String concatenation in query | Use parameterized query |
| 2 | MEDIUM | CSRF | api/middleware/auth.ts:15 | No CSRF token on POST | Add SameSite=Strict cookie |

### Summary
- **Critical/High:** N findings
- **Medium/Low:** N findings
- **Domains checked:** [list]
- **Clean domains:** [list with no findings]
```

### Step 5: Offer Fixes
If findings exist, offer to apply fixes with user confirmation.
