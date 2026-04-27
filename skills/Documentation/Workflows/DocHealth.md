# DocHealth Workflow

Documentation health scanning, auto-fixing, and maintenance for any repo.

## Tool Location

`${PAI_HOME}/Tools/doc-health-check.ts`

Runs on whatever repo directory is passed (defaults to cwd). Each repo can have its own `.doc-health-ignore` file for suppression patterns.

## Commands

### Scan

Detect doc drift. Show findings grouped by file.

```bash
bun ${PAI_HOME}/Tools/doc-health-check.ts [--counts] [--dates] [--json] [--files f1,f2] [dir]
```

- Default: checks file paths and symbols
- `--counts`: also check numeric claims ("23 skills" vs actual)
- `--dates`: also check front-matter dates vs git modification dates
- `--files`: scope to specific files (for wrapup integration)
- `--json`: machine-readable output

### Fix

Auto-fix deterministic findings. Show before→after for each fix.

```bash
bun ${PAI_HOME}/Tools/doc-health-check.ts --fix [--counts] [--dates] [dir]
```

Fixes three categories:
1. **Renamed paths** — finds the actual file by name, updates the reference
2. **Stale dates** — updates front-matter date to git last-modified date
3. **Stale counts** — replaces number with actual count

**Limitation:** Count fixer uses repo-wide globs. Scope-specific counts (e.g. "38 GSD workflows" vs 95 total) will be incorrectly replaced. Review count fixes before committing. Path and date fixes are safe.

### Baseline

Save/compare finding snapshots for delta tracking.

```bash
# Save current state
bun ${PAI_HOME}/Tools/doc-health-check.ts --baseline [dir]

# Subsequent runs show delta
bun ${PAI_HOME}/Tools/doc-health-check.ts [dir]
# → "Doc health: 193 findings (baseline: 193, delta: +0)"
```

Baseline saved to `MEMORY/STATE/doc-health-baseline.json` in the target repo.

### Report

Generate a persisted fix list for working through remaining findings.

```bash
bun ${PAI_HOME}/Tools/doc-health-check.ts --json [dir] | \
  bun -e '[generate markdown checklist from JSON output]'
```

Output: `docs/doc-health-fix-list.md` with checkboxes per finding, grouped by file.

## Maintain Pipeline

The full maintenance workflow, run by the agent when invoked:

1. **Scan** — run with `--counts --dates`, capture findings
2. **Fix paths** — run with `--fix`, apply safe path renames
3. **Review** — show diff of what was fixed, ask user to confirm
4. **Fix counts** — only for repo-wide counts (skills, hooks, patterns). Skip scope-specific counts.
5. **Baseline** — save new baseline after fixes
6. **Report remaining** — for findings that need human judgment (stale sections, removed features):
   - Generate fix list
   - Optionally delegate to a background agent for non-deterministic cleanup
7. **Summary** — N fixed, M remaining, K suppressed

### Agent Delegation for Non-Deterministic Fixes

When findings require judgment (stale sections referencing removed features, misleading descriptions), delegate to a background agent:

```
Agent({
  description: "Fix doc drift findings",
  prompt: "You're in [repo]. Here are [N] documentation findings that need human judgment to fix.
    [paste findings]
    For each: read the doc, check what actually exists, update or remove the stale reference.
    Do NOT modify files outside this list: [scoped file list]",
  run_in_background: true,
})
```

This uses whatever model the current session runs on. No specific provider dependency.

## Session-end Integration

At session end (e.g., during the `session-wrapup` harness), run a scoped scan on session-changed `.md` files:

```bash
# Get changed docs
changed=$(git diff --name-only HEAD~1 -- '*.md' | tr '\n' ',')
# Scoped scan
bun ${PAI_HOME}/Tools/doc-health-check.ts --files "$changed" [dir]
```

Surface only new drift introduced in the current session. If delta > 0, warn before completing the session.

## Ignore Patterns

Each repo can have a `.doc-health-ignore` file at its root:

```
# Suppress by claim content (matches finding's claim or detail)
NNNN-kebab-title.md
src/foo.ts
USER/

# Suppress entire files
file:PAI/PAI-CAPABILITIES-CHANGELOG.md
file:generated/output.md
```

## Examples

**Example 1: Quick health check**
```
User: "check doc health"
→ Run scan with --counts --dates on cwd
→ Show: "245 findings (baseline: 250, delta: -5). 178 suppressed."
→ Top 5 files by finding count
```

**Example 2: Fix doc drift**
```
User: "fix doc drift"
→ Run --fix, show diff summary
→ "90 paths fixed, 0 dates, 0 counts. Review diff before committing."
→ Show git diff --stat
```

**Example 3: Full maintenance**
```
User: "doc maintenance" or "maintain docs"
→ Run maintain pipeline (scan → fix → baseline → report)
→ "Fixed 12 paths. 45 remaining findings. Fix list at docs/doc-health-fix-list.md"
→ "Want me to delegate remaining findings to a background agent?"
```
