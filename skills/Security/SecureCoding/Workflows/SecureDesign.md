# SecureDesign Workflow

## Input
- **Feature**: description of feature being designed
- **Context**: optional architecture notes or constraints

## Steps

### Step 1: Load All Domain Context
Read all 6 context files — design review needs full coverage.
- `${CLAUDE_SKILL_DIR}/AccessControl.md`
- `${CLAUDE_SKILL_DIR}/ClientSide.md`
- `${CLAUDE_SKILL_DIR}/ServerSide.md`
- `${CLAUDE_SKILL_DIR}/AuthSessions.md`
- `${CLAUDE_SKILL_DIR}/ApiSecurity.md`
- `${CLAUDE_SKILL_DIR}/BypassTechniques.md`

### Step 2: Identify Attack Surfaces
For each domain, assess whether the feature creates attack surface:
- Does it accept user input? -> ClientSide.md, ServerSide.md
- Does it make external requests? -> ServerSide.md (SSRF)
- Does it handle auth/sessions? -> AuthSessions.md
- Does it expose an API? -> ApiSecurity.md
- Does it handle files? -> ServerSide.md (uploads)
- Does it have authorization? -> AccessControl.md

### Step 3: Threat Model
For each identified attack surface:
1. What can an attacker do? (use bypass techniques)
2. What controls are needed? (use prevention checklists)
3. What's the impact if the control fails?

### Step 4: Output Design Recommendations
```markdown
## Secure Design: [feature]

### Attack Surface Analysis
| Surface | Domain | Risk | Recommended Control |
|---------|--------|------|-------------------|
| User input in search | SQLi | HIGH | Parameterized queries |
| Webhook URL | SSRF | HIGH | URL allowlist + DNS validation |

### Required Security Controls
1. [Control with implementation guidance]
2. [Control with implementation guidance]

### VibeSec Patterns to Apply
- [Specific bypass technique to defend against]
- [Specific checklist items to implement]
```
