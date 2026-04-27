#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  AuditRepos.sh /path/to/repo [/path/to/repo ...]
  AuditRepos.sh --from-file repos.txt

Reports baseline Beads posture for each repo:
- git root
- .beads presence
- bd availability
- bd ready status
- Dolt remote presence
- Claude hook check status
- legacy JSONL markers

This is a fleet triage tool, not a mutator.
EOF
}

repo_paths=()

if [ "$#" -eq 0 ]; then
  usage
  exit 1
fi

if [ "$1" = "--from-file" ]; then
  if [ "$#" -ne 2 ]; then
    usage
    exit 1
  fi
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    repo_paths+=("$line")
  done <"$2"
else
  repo_paths=("$@")
fi

if command -v bd >/dev/null 2>&1; then
  bd_available=yes
else
  bd_available=no
fi

for repo in "${repo_paths[@]}"; do
  echo "== $repo =="

  if [ ! -d "$repo" ]; then
    echo "exists: no"
    echo
    continue
  fi

  if ! git_root="$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)"; then
    echo "git_repo: no"
    echo
    continue
  fi

  echo "git_root: $git_root"

  if [ -d "$git_root/.beads" ]; then
    echo "beads_dir: yes"
  else
    echo "beads_dir: no"
  fi

  echo "bd_available: $bd_available"

  if [ "$bd_available" = yes ] && [ -d "$git_root/.beads" ]; then
    if (cd "$git_root" && bd ready --json >${TMPDIR}/beads-ready.json 2>/dev/null); then
      echo "ready: yes"
    else
      echo "ready: no"
    fi

    if (cd "$git_root" && bd dolt remote list >${TMPDIR}/beads-remotes.txt 2>/dev/null); then
      if [ -s ${TMPDIR}/beads-remotes.txt ]; then
        echo "dolt_remote: yes"
      else
        echo "dolt_remote: no"
      fi
    else
      echo "dolt_remote: unknown"
    fi

    if (cd "$git_root" && bd setup claude --check >${TMPDIR}/beads-hooks.txt 2>/dev/null); then
      echo "hook_check: yes"
    else
      echo "hook_check: no"
    fi
  else
    echo "ready: skipped"
    echo "dolt_remote: skipped"
    echo "hook_check: skipped"
  fi

  legacy_markers="$(find "$git_root/.beads" -maxdepth 3 \( -name 'issues.jsonl' -o -name '*.jsonl' \) 2>/dev/null | sort || true)"
  if [ -n "$legacy_markers" ]; then
    echo "legacy_jsonl: yes"
    printf '%s\n' "$legacy_markers"
  else
    echo "legacy_jsonl: no"
  fi

  echo
done
