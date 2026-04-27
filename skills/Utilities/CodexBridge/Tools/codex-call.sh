#!/usr/bin/env bash
set -euo pipefail

json_mode=0
auto_mode=0
confirm_risk=0
repo="${PWD}"
model=""
prompt_file=""
prompt=""
scope_files=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -j) json_mode=1; shift ;;
    --auto) auto_mode=1; shift ;;
    --confirm-risk) confirm_risk=1; shift ;;
    -C|-r|--repo) repo="${2:?}"; shift 2 ;;
    -m) model="${2:?}"; shift 2 ;;
    -f) prompt_file="${2:?}"; shift 2 ;;
    -S|--scope) scope_files="${2:?}"; shift 2 ;;
    --) shift; break ;;
    *) prompt+="${prompt:+ }$1"; shift ;;
  esac
done

if [[ -n "${prompt_file}" ]]; then
  [[ -f "${prompt_file}" ]] || { echo "Prompt file not found: ${prompt_file}" >&2; exit 1; }
  prompt="${prompt}"$'\n\n'"$(cat "${prompt_file}")"
fi

# Warn if prompt file exceeds sweet spot
if [[ -n "${prompt_file}" ]] && [[ -f "${prompt_file}" ]]; then
  line_count=$(wc -l < "${prompt_file}")
  if [[ "${line_count}" -gt 400 ]]; then
    echo "WARNING: Prompt file is ${line_count} lines (sweet spot is <300). Consider splitting by concern area. See SKILL.md 'Diff Preparation' section." >&2
  fi
fi

[[ -n "${prompt}" ]] || { echo "No prompt provided." >&2; exit 1; }
[[ -d "${repo}" ]] || { echo "Repo/dir not found: ${repo}" >&2; exit 1; }

budget_contract="$(cat <<'BUDGET_CONTRACT_EOF'
Execution contract:
- Triage before deep reading. Start with the highest-risk or explicitly named files.
- Prefer diffs, focused tests, and short evidence snippets over broad repository sweeps.
- As soon as you have enough evidence to answer, stop exploring and produce the final response.
- If the task scope is broad, explicitly narrow it and state what you prioritized.
- If token budget gets tight, return partial but useful results in the requested format rather than continuing to read.
- Avoid pasting long file bodies or long logs unless they are essential to the answer.
BUDGET_CONTRACT_EOF
)"

scope_contract=""
if [[ -n "${scope_files}" ]]; then
  scope_contract="$(cat <<SCOPE_EOF

File scope constraint (MANDATORY):
- You may ONLY modify these files: ${scope_files}
- Do NOT modify any other files, especially: package-lock.json, package.json, tsconfig.json, catalog.json, .gitignore, .env
- If you believe a file outside this list needs changes, STOP and report it as a finding instead of modifying it.
- This constraint is non-negotiable. Modifying files outside scope is a failure.
SCOPE_EOF
)"
fi

contains_high_impact_intent() {
  local text="${1}"
  local pattern
  local -a high_impact_patterns=(
    '(^|[^[:alnum:]_])git[[:space:]]+push([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])push[[:space:]]+(this|the|that|my|our)[[:space:]]+(branch|changes|commit|commits)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])deploy[[:space:]]+(this|the|that|to|into|on)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])release[[:space:]]+(this|the|that)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])rm[[:space:]]+-[[:alnum:]-]*[rfRF]([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])git[[:space:]]+reset([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])reset[[:space:]]+--hard([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])git[[:space:]]+rebase([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])rebase[[:space:]]+(this|the|that|current|branch)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])(run|apply|execute)[[:space:]].*(db|database|schema)[[:space:]]+migrate([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])(db|database|schema)[[:space:]]+migrate([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])migrate[[:space:]]+(the[[:space:]]+)?(db|database|schema)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])(print|paste|share|reveal|use|set|rotate|export)[[:space:]].*(auth|token|credential|secret)s?([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])(auth|token|credential|secret)s?.*(prod|production)([^[:alnum:]_]|$)'
    '(^|[^[:alnum:]_])(prod|production).*(deploy|release|credential|secret|token|database|db|migrate)([^[:alnum:]_]|$)'
  )

  for pattern in "${high_impact_patterns[@]}"; do
    if printf '%s\n' "${text}" | grep -Eiq "${pattern}"; then
      return 0
    fi
  done

  return 1
}

if contains_high_impact_intent "${prompt}" && [[ "${confirm_risk}" -ne 1 ]]; then
  echo "Blocked: high-impact intent detected. Re-run with --confirm-risk." >&2
  exit 2
fi

if [[ "${auto_mode}" -eq 1 ]] && [[ -z "${scope_files}" ]]; then
  echo "Warning: --auto without --scope — Codex may modify files outside task intent. Consider adding --scope 'file1.ts,file2.ts'" >&2
fi

if [[ "${json_mode}" -eq 1 ]]; then
  prompt="$(cat <<PROMPT_EOF
Return ONLY valid minified JSON. No markdown.
Schema:
{"summary":"string","findings":[{"severity":"high|medium|low","title":"string","details":"string","refs":["path:line"]}],"questions":["string"],"next_steps":["string"]}
If unknown, use empty arrays/strings.

${budget_contract}
${scope_contract}

USER_PROMPT:
${prompt}
PROMPT_EOF
)"
else
  prompt="$(cat <<PROMPT_EOF
${budget_contract}
${scope_contract}

USER_PROMPT:
${prompt}
PROMPT_EOF
)"
fi

if command -v codex >/dev/null 2>&1; then
  codex_runner=(codex)
elif command -v npx >/dev/null 2>&1; then
  codex_runner=(npx -y @openai/codex)
else
  echo "Neither 'codex' nor 'npx' is available on PATH." >&2
  exit 127
fi

cmd=("${codex_runner[@]}" exec --cd "${repo}")
[[ -n "${model}" ]] && cmd+=(--model "${model}")
[[ "${auto_mode}" -eq 1 ]] && cmd+=(--full-auto)
cmd+=("${prompt}")

printf 'Running: %q ' "${cmd[@]}"; echo
"${cmd[@]}"
