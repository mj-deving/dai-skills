1. Require plan path and explicit target repo path (`-r`) for cross-repo safety.
2. Run `codex-plan-review.sh -p <plan.md> -r <repo>`.
3. If user requests machine use, rerun with `-j` via `codex-call.sh` and validate with `jq`.
4. Never auto-enable `--auto` unless user explicitly asks for autonomous execution.
5. For large plans, require findings-first output and tell Codex to stop after enough evidence instead of reading the whole repo.
