---
name: CodeReview
description: Structured code review methodology — 5-axis evaluation, severity classification, named simplification patterns. USE WHEN code review, review code, review PR, review changes, review diff, review this, quality review, review before merge, review my code, pull request review, change review, shellcheck, shell lint, bash lint, script analysis.
---

# CodeReview

Structured methodology for evaluating code changes. Provides the framework that /simplify agents and human reviewers use to assess quality.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/CodeReview/`

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running WORKFLOWNAME in CodeReview to ACTION"}' \
  > /dev/null 2>&1 &
```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Review** | "review code", "review PR", "review changes", "review this diff" | `Workflows/Review.md` |
| **TwoStageReview** | "two-stage review", "review against spec", "spec compliance review", "6-axis review" | `Workflows/TwoStageReview.md` |
| **Desloppify** | "desloppify", "health scan", "technical debt", "health score", "cleanup plan" | `Desloppify/SKILL.md` |
| **Refactor** | "refactor", "scan for duplication", "dead code", "unused exports", "refactoring pass" | `Refactor/SKILL.md` |

## The 5-Axis Review Framework

Every code review evaluates across five dimensions:

### 1. Correctness
- Does the code match the requirements/spec?
- Are edge cases handled (empty, null, boundary, concurrent)?
- Do tests cover the new behavior?
- Are error paths handled, not just happy path?

### 2. Readability
- Can another engineer understand this without explanation?
- Are names descriptive (not `data`, `temp`, `result`, `x`)?
- Is the logic flow obvious or does it require mental gymnastics?
- Are complex sections commented with WHY, not WHAT?

### 3. Architecture
- Does it fit the existing patterns in this codebase?
- Are module boundaries respected?
- Are abstractions appropriate (not premature, not missing)?
- Would this scale to 10x usage without redesign?

### 4. Security
- Are external inputs validated at the boundary?
- Are secrets kept out of code and logs?
- Is authentication/authorization checked where needed?
- Could this introduce XSS, injection, or CSRF?

### 5. Performance
- Any N+1 queries or unbounded fetches?
- Any unnecessary synchronous operations that could be async?
- Any memory leaks (uncleaned listeners, intervals, refs)?
- Would this degrade under load?

## Severity Classification

Every finding gets exactly one label:

| Label | Meaning | Action |
|-------|---------|--------|
| **Critical** | Blocks merge — security flaw, data loss, crash | Must fix before merge |
| **Important** | Should fix — missing test, design issue, bug risk | Fix in this PR |
| **Nit** | Optional — style, naming preference, minor cleanup | Author decides |
| **FYI** | No action needed — context, explanation, praise | Informational only |

**Rule:** No more than 1-2 Critical per review. If you're finding 5+ Criticals, the change needs a design discussion, not a code review.

## Named Simplification Patterns

When suggesting improvements, use named patterns so the author knows exactly what you mean:

| Pattern | Before | After |
|---------|--------|-------|
| **Guard clause** | Deep nested if/else | Early return for edge cases |
| **Extract function** | Long function doing 3 things | 3 focused functions |
| **Rename for clarity** | `data`, `val`, `x` | `userProfile`, `maxRetries`, `connectionTimeout` |
| **Inline trivial variable** | `const x = foo(); return x;` | `return foo();` |
| **Replace conditional with polymorphism** | Switch on type string | Type-specific classes/functions |
| **Consolidate duplicate** | Same 5 lines in 3 places | Extracted shared function |

## Approval Philosophy

> "Approve when it definitely improves overall code health, even if it isn't perfect."

The goal is continuous improvement, not perfection. Don't block a merge for Nits. Don't request a rewrite when the change is directionally correct. "I'll fix it later" is a valid response to a Nit — "I'll fix it later" is NOT valid for Critical or Important.

## Examples

**Example 1: Review a PR**
```
User: "Review the changes in the last commit"
→ Invokes Review workflow
→ git diff → read tests first → walk 5 axes → classify findings
→ Output: summary with Critical/Important/Nit labels
```

**Example 2: Pre-merge quality check**
```
User: "Is this ready to merge?"
→ Invokes Review workflow
→ 0 Critical + 0 Important = Approve
→ 2 Nits noted as optional improvements
```

**Example 3: Architecture concern**
```
User: "Review this refactor for design issues"
→ Invokes Review workflow with focus on axis 3 (Architecture)
→ Checks pattern consistency, module boundaries, abstraction level
```

## ShellCheck — Shell Script Analysis

Static analysis for shell scripts. Catches common bugs, portability issues, and style problems.

```bash
# Lint shell scripts
shellcheck script.sh

# JSON output for programmatic analysis
shellcheck -f json *.sh

# Check all shell scripts in project
find . -name "*.sh" -exec shellcheck {} +

# Specific severity
shellcheck --severity=warning script.sh
```

**When to use:**
- Code review includes shell scripts — run ShellCheck as part of the review
- CI/CD pipeline scripts — these often have subtle bugs (unquoted variables, missing error handling)
- Dockerfiles with RUN blocks — extract the shell commands and lint them
- Any `.sh`, `.bash`, or shebang-detected scripts in the changeset

**Common findings:**
- **SC2086** — unquoted variable expansion (word splitting / globbing risk)
- **SC2046** — unquoted command substitution
- **SC2034** — unused variable
- **SC2155** — declare and assign separately to avoid masking return values
- **SC2164** — `cd` without `|| exit` (failure to change directory silently continues)

**Integration with 5-axis review:** ShellCheck findings map to axis 1 (Correctness) and axis 4 (Security). Unquoted variables are both correctness bugs and potential injection vectors.

## Integration

**Works with:**
- **/simplify** — invokes 3 review agents. This skill provides the framework they should follow.
- **Algorithm VERIFY** — code-producing runs invoke /simplify. This skill can be selected as a capability for deeper reviews.
- **Refactor** — automated tool-based scanning. Different from CodeReview (judgment-based evaluation).
- **Security:SecureCoding** — handles axis 4 (security) in depth. CodeReview does a quick security check; SecureCoding does a thorough one.
- **TDD** — handles test quality. CodeReview checks "are there tests?"; TDD ensures they're well-structured.
