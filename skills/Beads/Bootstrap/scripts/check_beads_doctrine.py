#!/usr/bin/env python3
"""Heuristic checker for core repo-local Beads doctrine."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def first_match_line(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return None
    return text.count("\n", 0, match.start()) + 1


def has_all(text: str, snippets: list[str]) -> bool:
    return all(snippet in text for snippet in snippets)


def add_result(results: list[dict[str, str]], code: str, status: str, message: str, details: str = "") -> None:
    results.append(
        {
            "code": code,
            "status": status,
            "message": message,
            "details": details,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check root CLAUDE.md and AGENTS.md for core Beads doctrine.")
    parser.add_argument("--path", default=".", help="Repo root to inspect")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--prominence-lines",
        type=int,
        default=160,
        help="Warn if the first Beads mention in CLAUDE.md appears after this line number",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    claude_path = root / "CLAUDE.md"
    agents_path = root / "AGENTS.md"
    claude_text = read_text(claude_path)
    agents_text = read_text(agents_path)

    results: list[dict[str, str]] = []

    if claude_text:
        add_result(results, "claude_exists", "pass", "Root CLAUDE.md exists", str(claude_path))
    else:
        add_result(results, "claude_exists", "fail", "Root CLAUDE.md is missing", str(claude_path))

    if agents_text:
        add_result(results, "agents_exists", "pass", "Root AGENTS.md exists", str(agents_path))
    else:
        add_result(results, "agents_exists", "fail", "Root AGENTS.md is missing", str(agents_path))

    if claude_text:
        beads_line = first_match_line(claude_text, r"(?im)^(#+\s+.*beads.*|.*beads.*)$")
        if beads_line is None:
            add_result(
                results,
                "claude_mentions_beads",
                "fail",
                "CLAUDE.md does not mention Beads explicitly",
                "Add a visible Beads section or equivalent doctrine near session bootstrap.",
            )
        else:
            status = "pass" if beads_line <= args.prominence_lines else "warn"
            message = "CLAUDE.md mentions Beads prominently" if status == "pass" else "Beads appears late in CLAUDE.md"
            add_result(results, "claude_mentions_beads", status, message, f"First Beads mention at line {beads_line}")

        if "AGENTS.md" in claude_text:
            add_result(results, "claude_points_to_agents", "pass", "CLAUDE.md points readers to AGENTS.md")
        else:
            add_result(
                results,
                "claude_points_to_agents",
                "fail",
                "CLAUDE.md does not point readers to AGENTS.md",
                "Add an explicit bootstrap instruction to read AGENTS.md.",
            )

        if has_all(claude_text, ["bd create", "--context", "SOURCES:", "kn entry"]):
            add_result(
                results,
                "claude_creation_contract",
                "pass",
                "CLAUDE.md encodes the self-contained bead creation contract",
            )
        else:
            add_result(
                results,
                "claude_creation_contract",
                "fail",
                "CLAUDE.md is missing the creation-time context/provenance contract",
                "Expected a bd create example or rule using --context plus SOURCES/kn entry notes.",
            )

    if agents_text:
        read_order_ok = (
            re.search(r"(?m)^1\.\s+`?CLAUDE\.md`?", agents_text) is not None
            and re.search(r"(?m)^2\.\s+`?AGENTS\.md`?", agents_text) is not None
        )
        if read_order_ok:
            add_result(results, "agents_read_order", "pass", "AGENTS.md read order starts with CLAUDE.md then AGENTS.md")
        else:
            add_result(
                results,
                "agents_read_order",
                "fail",
                "AGENTS.md read order does not start with CLAUDE.md then AGENTS.md",
            )

        required = [
            "bd ready --json",
            "bd show <id> --json",
            "bd update <id> --claim --json",
            "bd note",
            "bd remember",
            "bd close",
            "bd dolt push",
        ]
        missing = [snippet for snippet in required if snippet not in agents_text]
        if missing:
            add_result(
                results,
                "agents_core_commands",
                "fail",
                "AGENTS.md is missing core Beads lifecycle commands",
                ", ".join(missing),
            )
        else:
            add_result(results, "agents_core_commands", "pass", "AGENTS.md includes the core Beads lifecycle commands")

    failures = sum(1 for result in results if result["status"] == "fail")
    warnings = sum(1 for result in results if result["status"] == "warn")
    payload = {
        "path": str(root),
        "ok": failures == 0,
        "failures": failures,
        "warnings": warnings,
        "results": results,
        "note": "This checker validates only mechanically provable workflow surfaces.",
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Beads doctrine check: {'PASS' if payload['ok'] else 'FAIL'}")
        print(f"Repo: {root}")
        for result in results:
            print(f"[{result['status'].upper()}] {result['code']}: {result['message']}")
            if result["details"]:
                print(f"  {result['details']}")
        if failures or warnings:
            print(f"Summary: {failures} fail, {warnings} warn")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
