#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: codex-plan-review.sh -p <plan.md> [-r <repo>]" >&2
  echo "   or: codex-plan-review.sh <plan.md> [repo]  # legacy positional form" >&2
  exit 1
}

plan=""
repo="${PWD}"
confirm_risk=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--plan)
      plan="${2:?}"
      shift 2
      ;;
    -r|--repo|-C)
      repo="${2:?}"
      shift 2
      ;;
    --confirm-risk)
      confirm_risk=1
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      if [[ -z "${plan}" ]]; then
        plan="$1"
      elif [[ "${repo}" == "${PWD}" ]]; then
        repo="$1"
      else
        usage
      fi
      shift
      ;;
  esac
done

[[ -n "${plan}" ]] || usage

[[ -f "${plan}" ]] || { echo "Plan not found: ${plan}" >&2; exit 1; }
[[ -d "${repo}" ]] || { echo "Repo/dir not found: ${repo}" >&2; exit 1; }

cmd=(bash ${SKILLS_HOME}/Utilities/CodexBridge/Tools/codex-call.sh -r "${repo}")
[[ "${confirm_risk}" -eq 1 ]] && cmd+=(--confirm-risk)
cmd+=("Review this implementation plan for bugs, regressions, missing tests, sequencing risks, and unclear assumptions.
Output findings first, ordered by severity, then open questions, then brief summary.

PLAN:
$(cat "${plan}")")

"${cmd[@]}"
