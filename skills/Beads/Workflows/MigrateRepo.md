# MigrateRepo

Use this workflow when the goal is to bring one repo onto the current Beads doctrine with the smallest justified changes.

## Step 1: Establish posture

Run the repo through the Beads posture questions:

```bash
cd /path/to/repo
git rev-parse --show-toplevel
test -d .beads && echo ".beads exists" || echo ".beads missing"
bd ready --json || true
bd dolt remote list || true
bd setup claude --check || true
find .beads -maxdepth 3 \( -name 'issues.jsonl' -o -name '*.jsonl' \) 2>/dev/null | sort
```

Classify the repo:
- `new` if `.beads/` is missing
- `partial` if Beads exists but doctrine/remotes/hooks are weak or drifted
- `mature` if Beads exists, doctrine is coherent, and only minor corrections are needed

## Step 2: Choose the path

- `new` => use `Bootstrap/SKILL.md`
- `partial` or `mature` but underfit => use `UpgradePath/SKILL.md`
- hook drift => add `HookAudit/SKILL.md`
- topology uncertainty => add `TopologyPlanner/SKILL.md`
- migration risk or lock concerns => add `RecoveryAudit/SKILL.md`

Do not assume every repo needs the same route.

## Step 3: Apply the Beads doctrine baseline

For repos that use Beads seriously, the target baseline is:
- `CLAUDE.md` and `AGENTS.md` make Beads the task authority
- shared repos have a Dolt remote and explicit pull/push posture
- new beads are self-contained at creation time
- investigative beads are evidence-first
- epics decompose immediately when the next steps are already clear
- dependencies are explicit with `bd dep`
- stale or contradictory backlog is cleaned aggressively
- close reasons are specific, not vague

## Step 4: Verify

At minimum:

```bash
bd ready --json || true
git diff --check
```

If bootstrap or doctrine files changed:

```bash
python3 ${PAI_EXTENSIONS_DIR}/skills/Beads/Bootstrap/scripts/check_beads_doctrine.py --path .
```

If the repo is shared:

```bash
bd dolt remote list
bd dolt pull || true
bd dolt push
```

## Step 5: Record the result

Document:
- repo classification
- chosen Beads path
- changes applied
- what was intentionally left alone
- whether follow-up work is required

## Anti-patterns

Do not:
- bootstrap every repo identically
- import legacy JSONL blindly
- jump to server mode without a real multi-writer need
- leave hollow tasks that require chat archaeology later
