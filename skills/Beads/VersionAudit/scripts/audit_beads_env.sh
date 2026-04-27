#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

echo "== repo =="
printf '%s\n' "$repo_root"

echo
echo "== bd availability =="
if command -v bd >/dev/null 2>&1; then
  echo "bd: installed"
  (bd version 2>/dev/null || bd --version 2>/dev/null || true)
else
  echo "bd: missing"
fi

echo
echo "== beads state =="
if [ -d .beads ]; then
  echo ".beads: present"
  find .beads -maxdepth 2 -type f | sort
else
  echo ".beads: missing"
fi

echo
echo "== legacy markers =="
find .beads -maxdepth 3 \( -name 'issues.jsonl' -o -name '*.jsonl' \) 2>/dev/null | sort || true

echo
echo "== ready =="
(bd ready --json 2>/dev/null || true)

echo
echo "== dolt remotes =="
(bd dolt remote list 2>/dev/null || true)

echo
echo "== claude hooks =="
(bd setup claude --check 2>/dev/null || true)

echo
echo "== live processes =="
(ps -eo pid,comm,args | rg '(^|/)(bd|dolt)( |$)' || true)
