#!/usr/bin/env bash
set -euo pipefail

schema=""
repo="${PWD}"
prompt=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s) schema="${2:?}"; shift 2 ;;
    -C|-r|--repo) repo="${2:?}"; shift 2 ;;
    *) prompt+="${prompt:+ }$1"; shift ;;
  esac
done

[[ -n "${schema}" ]] || { echo "Schema required: -s <name>" >&2; exit 1; }
[[ -n "${prompt}" ]] || { echo "Prompt required." >&2; exit 1; }

out="$(bash ${SKILLS_HOME}/Utilities/CodexBridge/Tools/codex-call.sh -j -C "${repo}" "${prompt}")"
echo "${out}" | jq . >/dev/null
echo "${out}"
