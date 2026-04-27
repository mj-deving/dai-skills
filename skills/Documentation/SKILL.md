---
name: Documentation
description: Documentation practices — comment guidelines, ADR conventions, API documentation, inline docs philosophy, doc health scanning and maintenance. USE WHEN documentation, write docs, comment guidelines, ADR, architecture decision, API docs, JSDoc, OpenAPI, document code, when to comment, how to document, self-documenting code, README, doc health, doc drift, stale docs, fix docs, doc maintenance, check docs.
---

# Documentation

Documentation explains WHY, not WHAT. Code shows what was built; documentation explains why it was built that way.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Documentation/`

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WORKFLOWNAME in Documentation to ACTION"}' \
  > /dev/null 2>&1 &
```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **WriteADR** | "write ADR", "document decision", "architecture decision" | `Workflows/WriteADR.md` |
| **DocHealth** | "doc health", "check docs", "fix doc drift", "doc maintenance", "stale docs" | `Workflows/DocHealth.md` |
| **CodebaseToCourse** | "codebase to course", "interactive tutorial", "teach code", "code walkthrough" | `CodebaseToCourse/SKILL.md` |

## Comment Guidelines

### When to Comment

- **Non-obvious intent** — why this approach was chosen over the obvious one
- **Known gotchas** — "this looks wrong but it's intentional because..."
- **Business rules** — logic that comes from domain requirements, not technical necessity
- **Workarounds** — temporary fixes with references to the real issue

### When NOT to Comment

- **Restating code** — `// increment counter` above `counter++` adds nothing
- **Commented-out code** — git has history. Delete it.
- **TODO without a ticket** — either create a Beads issue / ADR or don't write the TODO
- **Obvious types** — `// string` above a `name: string` declaration

### The Self-Documenting Code Myth

> "Self-documenting code" is only self-documenting for its author, briefly.

Good names and clear structure reduce the need for comments, but they can't explain:
- Why this algorithm was chosen over a simpler one
- What business rule drives this branching logic
- Why this seemingly redundant check exists
- What happens if you remove this "unnecessary" code

## Architecture Decision Records (ADRs)

**Convention:** See `${PAI_HOME}/RULES/adr-convention.md` for full details.

**Quick reference:**
- Format: `NNNN-kebab-title.md`
- Sections: Status, Date, Context, Decision, Alternatives Considered, Consequences
- **Never delete old ADRs** — supersede with Status: Superseded by ADR-XXXX
- Two levels: global (PAI-wide in `~/projects/Pai-Exploration/docs/decisions/`) and per-project (`docs/decisions/`)
- Algorithm LEARN phase checks if session warrants an ADR

## API Documentation

### TypeScript (JSDoc)

```typescript
/**
 * Validates an email address against format rules and MX records.
 *
 * @param email - The email address to validate
 * @returns Validation result with error message if invalid
 *
 * @example
 * const result = await validateEmail('user@example.com');
 * if (!result.valid) console.error(result.error);
 */
export async function validateEmail(email: string): Promise<ValidationResult> {
```

**When to use JSDoc:**
- Public API functions (exported from a module)
- Complex parameters that aren't obvious from types alone
- Functions with non-obvious side effects
- Anything other developers (or agents) will call

### REST/HTTP APIs (OpenAPI)

For HTTP endpoints, maintain OpenAPI/Swagger spec alongside the code:
- Request/response schemas with examples
- Error response shapes
- Authentication requirements
- Rate limiting information

## Project Documentation Checklist

- [ ] README with quick start and architecture overview
- [ ] ADRs for major technical decisions
- [ ] CLAUDE.md with project conventions for AI agents
- [ ] API documentation (JSDoc for functions, OpenAPI for HTTP)
- [ ] Inline comments for non-obvious intent and gotchas

## Examples

**Example 1: Document a technical decision**
```
User: "We chose SQLite over PostgreSQL — document why"
→ Invokes WriteADR workflow
→ Creates ADR with context, decision, alternatives, consequences
→ Saves to docs/decisions/NNNN-sqlite-over-postgres.md
```

**Example 2: Comment guidelines question**
```
User: "Should I comment this function?"
→ Checks against comment guidelines
→ If non-obvious intent or business rule: yes, explain WHY
→ If code is clear from names and types: no comment needed
```

**Example 3: API documentation**
```
User: "Document the webhook endpoint"
→ References JSDoc/OpenAPI patterns
→ Adds parameter descriptions, return types, examples, error shapes
```

## Integration

**Works with:**
- **ADR convention rule** — this skill references and extends it
- **Algorithm LEARN** — LEARN phase triggers ADR creation for architectural decisions
- **CodeReview** — reviews check for documentation quality (axis 2: readability)
- **GitWorkflow** — commit messages are documentation (explain WHY)
