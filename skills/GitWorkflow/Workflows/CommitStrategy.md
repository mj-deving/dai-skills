# CommitStrategy Workflow

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running CommitStrategy in GitWorkflow to plan commits"}' \
  > /dev/null 2>&1 &
```
-->

Running **CommitStrategy** in **GitWorkflow**...

---

## When to Use

- Finished a chunk of work and need to commit properly
- Staged changes span multiple concerns
- Need to split a large change into atomic commits
- Unsure whether to commit now or keep going

## Process

### Step 1: Review What Changed

```bash
git diff --stat          # what files changed
git diff                 # what actually changed
```

### Step 2: Identify Logical Units

Group changes by concern:
- **Type changes** (interfaces, schemas) → one commit
- **Implementation** (handlers, logic) → one commit per feature
- **Tests** → commit with the code they test (same logical unit)
- **Refactoring** (renames, extractions) → separate commit from features
- **Config/infra** (CI, deps, config) → separate commit

### Step 3: Stage Intentionally

```bash
git add -p              # interactive: review each hunk
# Stage only the hunks that belong to this logical unit
```

**Never `git add -A`** without reviewing what's staged. Especially with AI-generated changes — you may have exploratory code that shouldn't be committed.

### Step 4: Summarize the Diff

Before writing the commit message, use the `summarize_git_diff` Fabric pattern to generate an intelligent summary of staged changes.

**If `fabric` CLI is installed:**
```bash
git diff --cached | fabric -p summarize_git_diff
```

**Otherwise, summarize the staged diff directly:**
> Use the `summarize_git_diff` pattern on my staged changes

Both produce a structured summary of what changed, why it matters, and potential impacts. Use this as the basis for your commit message — it catches details you might miss in a manual review.

**When to use:** Every commit benefits, but especially valuable for:
- Multi-file changes where the full scope isn't obvious
- Refactoring where the "what" is clear but the "why" needs articulation
- Changes touching unfamiliar code where the diff summary provides context

### Step 5: Write the Message

Follow the convention in SKILL.md:
```
<type>: <what> (imperative)

<why — 1-3 sentences>
<excluded — what was deliberately left out>
```

Use the `summarize_git_diff` output to inform the "why" section.

### Step 6: Verify Before Push

```bash
bun test                # tests still pass
git log --oneline -5    # commits tell a coherent story
git diff --stat HEAD~3  # scope matches intent
```
