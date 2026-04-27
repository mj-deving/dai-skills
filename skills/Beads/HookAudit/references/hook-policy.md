# Hook policy

Use this to judge Claude-side Beads hook behavior.

## Good patterns

- `SessionStart` runs `bd prime`
- `PreCompact` runs `bd prime --stealth`
- hooks remind Claude to read repo-local `AGENTS.md` / `CLAUDE.md`
- local handoff or memory files are loaded only as convenience
- wrapup hygiene encourages `bd note`, `bd remember`, and `bd dolt push`

## Acceptable but noisy

- startup context includes neutral project summaries
- local handoff notes are shown, but clearly labeled as local/non-authoritative
- extra context is injected that does not compete with Beads or repo docs

## Risky patterns

- startup context includes `next steps` from local files
- hooks infer repo workflow without reading the repo
- hooks treat machine-local memory as stronger than repo files
- hook behavior is strong enough to bias Claude away from `bd ready`

These should usually be softened or relabeled.

## Forbidden patterns

- auto-close Beads on `git commit`
- auto-close Beads on session end
- generate authoritative local backlog state that competes with `bd ready`
- reinitialize Beads automatically in mature repos
- encode one repo's workflow as a machine-global rule

## Preferred repair strategy

When repairing:
- convert auto-close into a reminder
- remove injected local next-step queues
- keep useful `bd prime` behavior
- preserve convenience context only if it is clearly non-authoritative
