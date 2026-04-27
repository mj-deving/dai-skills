# Two-Stage Review Workflow

Spec-compliant code review: verify the implementation matches requirements BEFORE evaluating code quality. Prevents wasting review cycles on non-compliant code.

**Source:** Adapted from obra/superpowers two-stage review pattern (MIT)

## When to Use

- Algorithm-produced work with a PRD/spec/ISC criteria
- Any implementation where "does it do what was asked?" is a real question
- Reviews where scope creep or misinterpretation risk is high

For ad-hoc changes without a spec, use the standard `Review.md` workflow instead.

## Inputs

1. **Changeset** — git diff, file list, or user-specified files
2. **Spec/Requirements** — PRD, ISC criteria, task description, or user request (check MEMORY/WORK/ if not provided)

## Stage 1: Spec Compliance

Before touching code quality, answer one question: **does this implementation do what was asked?**

### What to Check

1. **Completeness** — Does the implementation address ALL requirements from the spec? List each requirement and mark it covered or missing.
2. **Scope Creep** — Are there unrequested features, unnecessary abstractions, or over-engineering beyond what was specified?
3. **Interpretation** — Did the implementer misunderstand any requirement? Correct code solving the wrong problem is still wrong.
4. **ISC Coverage** — If ISC criteria exist, does every criterion have corresponding implementation?

### Stage 1 Output

```
## Stage 1: Spec Compliance

**Spec Source:** [where the requirements came from]

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | [requirement text] | Covered / Missing / Partial | [file:line or explanation] |
| 2 | ... | ... | ... |

**Scope Creep:** [None / List of unrequested additions]
**Misinterpretations:** [None / List with explanation]

**Verdict:** ✅ Spec Compliant | ❌ Spec Issues Found
```

### If Spec Issues Found

Stop here. Report the gaps. Do NOT proceed to Stage 2 — polishing non-compliant code wastes everyone's time. The implementer should fix spec compliance first, then request a re-review.

## Stage 2: Code Quality (6-Axis)

Only runs after Stage 1 passes. Evaluates across six dimensions:

### Axis 0: Spec Alignment
- Does the code match documented requirements without unjustified deviations?
- Are there implicit requirements the spec didn't state but the domain demands?
- If the implementation deviates from spec, is the deviation justified and documented?

### Axis 1: Correctness
- Are edge cases handled (empty, null, boundary, concurrent)?
- Do tests cover the new behavior?
- Are error paths handled, not just happy path?

### Axis 2: Readability
- Can another engineer understand this without explanation?
- Are names descriptive (not `data`, `temp`, `result`, `x`)?
- Is the logic flow obvious or does it require mental gymnastics?
- Are complex sections commented with WHY, not WHAT?

### Axis 3: Architecture
- Does it fit the existing patterns in this codebase?
- Are module boundaries respected?
- Are abstractions appropriate (not premature, not missing)?
- Would this scale to 10x usage without redesign?

### Axis 4: Security
- Are external inputs validated at the boundary?
- Are secrets kept out of code and logs?
- Is authentication/authorization checked where needed?
- Could this introduce XSS, injection, or CSRF?

### Axis 5: Performance
- Any N+1 queries or unbounded fetches?
- Any unnecessary synchronous operations that could be async?
- Any memory leaks (uncleaned listeners, intervals, refs)?
- Would this degrade under load?

### Severity Classification

Every finding gets exactly one label:

| Label | Meaning | Action |
|-------|---------|--------|
| **Critical** | Blocks merge — security flaw, data loss, crash | Must fix before merge |
| **Important** | Should fix — missing test, design issue, bug risk | Fix in this PR |
| **Nit** | Optional — style, naming preference, minor cleanup | Author decides |
| **FYI** | No action needed — context, explanation, praise | Informational only |

### Stage 2 Output

```
## Stage 2: Code Quality (6-Axis Review)

### Findings

| # | Axis | Severity | File:Line | Finding |
|---|------|----------|-----------|---------|
| 1 | Correctness | Important | src/foo.ts:42 | Missing null check on user input |
| 2 | Security | Critical | src/auth.ts:15 | Token logged to stdout |
| ... | ... | ... | ... | ... |

### Summary
- Critical: N
- Important: N
- Nit: N
- FYI: N

### Merge Recommendation
- ✅ Approve — [reason]
- ⚠️ Approve with fixes — [list required fixes]
- ❌ Request changes — [blocking issues]
```

## Full Workflow Steps

1. **Identify the changeset** — `git diff`, file list, or user-specified scope
2. **Locate the spec** — PRD in MEMORY/WORK/, ISC criteria via TaskGet, or user-provided requirements
3. **Run Stage 1** — Spec compliance check (completeness, scope creep, interpretation)
4. **If Stage 1 fails** — Report gaps with specific missing requirements. Stop.
5. **Run Stage 2** — 6-axis quality review on compliant code
6. **Classify findings** — Apply severity labels to every finding
7. **Provide merge recommendation** — Based on severity distribution

## Subagent Dispatch (Optional)

For large changesets, Stage 1 can be dispatched to a dedicated spec compliance reviewer. See `SpecReviewerPrompt.md` for the subagent prompt template. This lets the primary reviewer focus on Stage 2 while a parallel agent handles spec verification.
