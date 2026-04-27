#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

echo "== baseline =="
printf 'repo: %s\n' "$repo_root"

echo
echo "== ready =="
(bd ready --json 2>/dev/null || true)

echo
echo "== dolt remotes =="
(bd dolt remote list 2>/dev/null || true)

echo
echo "== beads files =="
(find .beads -maxdepth 2 -type f 2>/dev/null | sort || true)

echo
echo "== claude hooks =="
(bd setup claude --check 2>/dev/null || true)

echo
echo "== candidate lock processes =="
(ps -eo pid,comm,args | rg '(^|/)(bd|dolt)( |$)' || true)
