# Refactor: Scan → Triage → Fix → Verify

Lightweight refactoring cycle. Stateless — no persistent scoring, no triage ceremony.

---

## Phase 1: SCAN

Run available tools. Skip any that fail (no config, not installed). Use Bash tool for each.

### knip — dead code and unused exports
```bash
npx knip --reporter json 2>&1
```
**Requires:** `package.json` in project root.
**If missing:** Report `[refactor] knip: no package.json found — skipping. Run \`npm init\` to create one.`
**Output:** JSON with `files`, `exports`, `dependencies`, `devDependencies`, `unlisted` arrays.

### jscpd — code duplication
```bash
npx jscpd --min-lines 5 --reporters json --output ${TMPDIR}/refactor-jscpd/ 2>&1
```
**Requires:** nothing (works on any directory).
**Output:** `${TMPDIR}/refactor-jscpd/jscpd-report.json` with `duplicates` array containing `firstFile`, `secondFile`, `lines`, `tokens`.

### eslint — lint violations
```bash
eslint . --format json 2>&1
```
**Requires:** `.eslintrc.*` or `eslint.config.*` in project.
**If missing:** Report `[refactor] eslint: no config found — skipping. Run \`eslint --init\` to configure.`
**Output:** JSON array of file objects with `messages` array (each has `ruleId`, `severity`, `line`, `message`).

### ast-grep — structural anti-patterns
```bash
# Run from the skill's directory so sgconfig.yml is found
cd ${SKILLS_HOME}/Refactor && sg scan --json <project-root> 2>&1
```
**Requires:** nothing (uses `sgconfig.yml` + `Rules/` shipped with the skill).
**If no matches or error:** Report `[refactor] ast-grep: no structural issues found.`
**Output:** JSON array of matches with `file`, `range`, `message`, `ruleId`.
**Built-in rules:** `no-any-type`, `no-console-log`, `no-empty-catch`, `no-process-exit`

**Note:** If a project has its own `sgconfig.yml`, run `sg scan --json` from the project root instead (project rules take precedence).

### Running Tools

Run all 4 sequentially via Bash. Collect output. If a tool exits non-zero or produces an error message, skip it with a `[refactor]` message and continue to the next tool.

---

## Phase 2: TRIAGE

Parse the JSON output from each tool. Collect findings into a unified list.

### Priority Order

1. **Dead code** (knip: unused files, exports) — safest to delete, no behavior change
2. **Duplication** (jscpd: cloned blocks ≥5 lines) — extract or deduplicate
3. **Structural patterns** (ast-grep: anti-patterns) — refactor
4. **Lint issues** (eslint: violations by severity) — fix
5. **Deprecation warnings** (eslint plugins) — migrate

### Deduplication

Same file + same line range from multiple tools → keep the highest-priority finding only.

### Presentation

If ≤20 findings: show all, grouped by category.

If >20 findings: show top 10 by priority and ask:
```
Found {N} issues ({dead} dead code, {dup} duplication, {struct} structural, {lint} lint).
Showing top 10. Fix these first? Or show all?
```

---

## Phase 3: FIX

Interactive loop for each finding:

```
[{n}/{total}] {tool}: {description} in {file}:{line}
  → {suggestion}
  Fix: {proposed change}. [Apply? y/n/skip]
```

For each finding:
1. **Show** the finding with file, line, context
2. **Read** the relevant code
3. **Propose** the fix
4. **Apply** the fix (Edit tool)
5. **Next** finding

**Skip behavior:** If user says "skip" or the fix is ambiguous, move to next finding.

**Batch behavior:** For similar findings (e.g., 5 unused exports in one file), propose fixing all at once.

---

## Phase 4: VERIFY

After all fixes, rescan with the tools that found issues:

```bash
# Re-run only the tools that had findings
npx knip --reporter json 2>&1          # if knip found issues
npx jscpd --min-lines 5 ... 2>&1      # if jscpd found issues
```

Report delta:
```
Refactoring complete:
  Dead code: {before} → {after} ({fixed} resolved, {skipped} skipped)
  Duplication: {before} → {after} ({fixed} fixed, {skipped} intentional)
  Structural: {before} → {after}
  Lint: {before} → {after} ({fixed} fixed, {remaining} need manual review)
```

If all findings resolved: `Codebase is clean. No issues remaining.`

---

## Graceful Degradation Summary

| Tool | Failure Mode | Behavior |
|------|-------------|----------|
| knip | No package.json | Skip, report |
| knip | Not installed | Skip, report: `npm i -g knip` |
| jscpd | Not installed | Skip, report: `npm i -g jscpd` |
| eslint | No config file | Skip, report: `eslint --init` |
| eslint | Not installed | Skip, report: `npm i -g eslint` |
| ast-grep | Not installed | Skip, report: `npm i -g @ast-grep/cli` |
| ast-grep | No rules match | Report: "no structural issues" |
| Any tool | Timeout >30s | Kill, report partial results |
