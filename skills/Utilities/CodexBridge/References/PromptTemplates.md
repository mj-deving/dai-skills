# Prompt Templates

Use these templates with `codex-call.sh`.

## Findings-First Output Contract (Default for All Reviews)

Every review prompt sent to Codex MUST include this output contract block. Paste it into your prompt file before the diff/content.

```text
## Output Contract (MANDATORY)

Output your findings FIRST as a table. Use this EXACT format:

| # | Severity | Location | Issue | Suggested Fix |
|---|----------|----------|-------|---------------|
| 1 | high     | src/foo.ts:42 | Description | Fix description |
| 2 | medium   | src/bar.ts:15 | Description | Fix description |

Rules:
- Emit the table BEFORE any prose analysis
- Order by severity (high → medium → low)
- Include file:line refs in Location column
- If you run low on tokens, emit the table IMMEDIATELY with what you have
- After the table: open questions, then brief summary
- No findings is a valid result — output an empty table, not prose
```

## Focused Diff Review

Use this template when reviewing a split diff chunk. Write to a file, then concatenate with the diff.

```text
Review the following diff for:
- bugs, regressions, or behavior changes
- security issues
- missing error handling
- test gaps

## Output Contract (MANDATORY)
[paste the contract block above]

## Diff
[diff content is concatenated below this line by the caller]
```

## Plan Review

Review this implementation plan for:
- bugs/regressions
- sequencing risks
- missing tests
- unclear assumptions

Budget discipline:
- review the plan first; only inspect implementation files if strictly needed
- stop once you have enough evidence for the top findings
- if scope is broad, prioritize the highest-risk sections
- if token budget gets tight, return partial findings rather than continuing analysis

Output order:
1. Findings (highest severity first)
2. Open questions
3. Brief summary

PLAN:
{{PLAN_TEXT}}

## Repo Audit

Audit this repository for:
- critical bugs
- security risks
- reliability issues
- testing gaps

Constraints:
- prioritize concrete evidence
- include file/line refs where possible
- keep recommendations actionable
- triage high-risk or explicitly named files first
- prefer diffs and focused checks over full-repo reading
- stop and return findings once evidence is sufficient
- if token budget gets tight, return partial findings with scope noted

Repo focus:
{{FOCUS}}

## Codegen Task

Implement the following change with minimal surface area.

Requirements:
{{REQUIREMENTS}}

Validation:
- run relevant tests/checks
- summarize changed files
- call out risks and follow-ups

Budget discipline:
- inspect only the files needed for the change
- prefer targeted tests before broad suites
- if context grows large, summarize decisions and proceed instead of rereading
