#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OUT = ROOT / "docs" / "skill-tree.html"
REPO_URL = "https://github.com/mj-deving/pai-skills"

CATEGORY_DESCRIPTIONS = {
    "Agents": "Reusable agent roles, contexts, and operating profiles.",
    "Beads": "Task coordination, workflow state, recovery, topology, and durable repo memory.",
    "CodeReview": "Review, refactor, code-health, and quality-improvement workflows.",
    "ContentAnalysis": "Content extraction, synthesis, and media/document analysis.",
    "Data": "Data handling, schema reasoning, and structured analysis workflows.",
    "Documentation": "Docs authoring, codebase-to-course flows, ADRs, and documentation health.",
    "Frontend": "UI engineering, frontend craft, visual design, accessibility, and polish.",
    "GitWorkflow": "Git, branch, PR, release, and repo hygiene workflows.",
    "Investigation": "OSINT-style research, debugging, and structured inquiry workflows.",
    "Media": "Visual, deck, video, image, and artifact generation workflows.",
    "ProjectTelos": "Project-scoped context mapping and executive brief generation.",
    "Research": "Portable source-grounded research workflows.",
    "ScientificDeck": "Scientific and academic deck generation and review.",
    "Scraping": "Web and platform scraping patterns and automation guidance.",
    "Security": "Secure coding, supply-chain, and secret-handling guidance.",
    "TDD": "Test-first, proof-driven, and API testing workflows.",
    "Thinking": "Reasoning frameworks, council review, science loops, and plan synthesis.",
    "Troubleshooting": "Incident, debugging, repro, and diagnostic workflows.",
    "Utilities": "General automation helpers and integration-specific operational skills.",
    "VisualExplainer": "HTML, diagrams, slides, and visual explanation systems.",
    "graphify": "Graph extraction and visualization support.",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}

    out: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_value
        if current_key is not None:
            out[current_key] = " ".join(part.strip() for part in current_value).strip().strip('"')
        current_key = None
        current_value = []

    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            flush()
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip()]
        elif current_key is not None:
            current_value.append(line.strip())
    flush()
    return out


def title_from_path(path: str) -> str:
    return path.split("/")[-1].replace("-", " ").replace("_", " ").title()


def first_markdown_summary(text: str) -> tuple[str | None, str | None]:
    title: str | None = None
    paragraph: list[str] = []
    in_frontmatter = text.startswith("---\n")
    in_code = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if in_frontmatter:
            if line == "---":
                in_frontmatter = False
            continue
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line:
            if paragraph:
                break
            continue
        if title is None and line.startswith("#"):
            title = line.lstrip("#").strip()
            continue
        if line.startswith(("-", "*", "|", ">", "!", "[")):
            if paragraph:
                break
            continue
        paragraph.append(line)

    summary = " ".join(paragraph).strip() or None
    return title, summary


def classify_artifact(rel_path: str) -> str:
    parts = rel_path.split("/")
    lower_parts = [part.lower() for part in parts]
    name = parts[-1].lower()
    if name == "skill.md":
        return "Skill"
    if "workflows" in lower_parts:
        return "Workflow"
    if "references" in lower_parts or "reference" in lower_parts:
        return "Reference"
    if "tools" in lower_parts or "scripts" in lower_parts:
        return "Tool"
    if "agents" in lower_parts:
        return "Agent config"
    if "templates" in lower_parts or name.endswith(".hbs"):
        return "Template"
    if "data" in lower_parts or name.endswith((".json", ".yaml", ".yml", ".csv")):
        return "Data"
    if "examples" in lower_parts or "prompts" in lower_parts:
        return "Example"
    if "tests" in lower_parts or name.startswith("eval."):
        return "Eval"
    if name.endswith((".ts", ".js", ".py", ".sh")):
        return "Tool"
    return "Resource"


def artifact_description(path: Path, rel_path: str, kind: str, parent_name: str) -> tuple[str, str]:
    name = title_from_path(path.stem)
    suffix = path.suffix.lower().lstrip(".") or "file"
    try:
        text = path.read_text(errors="ignore")
    except UnicodeDecodeError:
        return name, f"Binary or non-text {kind.lower()} associated with {parent_name}."

    if path.name == "SKILL.md":
        frontmatter = parse_frontmatter(text)
        return str(frontmatter.get("name") or parent_name), str(frontmatter.get("description") or "Skill instruction entry point.")

    if path.suffix.lower() == ".md":
        heading, summary = first_markdown_summary(text)
        return heading or name, summary or f"{kind} document associated with {parent_name}."

    if path.name in {"package.json", "tsconfig.json"}:
        return path.name, f"{kind} manifest associated with {parent_name}."

    if suffix in {"yaml", "yml", "json", "csv"}:
        return path.name, f"{kind} file associated with {parent_name}."

    if suffix in {"ts", "js", "py", "sh"}:
        return path.name, f"{kind} script associated with {parent_name}."

    return path.name, f"{kind} artifact associated with {parent_name}."


def collect_skills() -> list[dict[str, object]]:
    skills: list[dict[str, object]] = []
    for skill_file in sorted(SKILLS.rglob("SKILL.md")):
        text = skill_file.read_text(errors="ignore")
        frontmatter = parse_frontmatter(text)
        rel_dir = skill_file.parent.relative_to(SKILLS).as_posix()
        parts = rel_dir.split("/")
        category = parts[0]
        name = frontmatter.get("name") or title_from_path(rel_dir)
        description = frontmatter.get("description") or "No public description provided."
        link = f"{REPO_URL}/tree/main/skills/{rel_dir}"
        skills.append(
            {
                "name": name,
                "description": description,
                "path": rel_dir,
                "category": category,
                "depth": len(parts),
                "link": link,
            }
        )
    return skills


def collect_artifacts(skills: list[dict[str, object]]) -> list[dict[str, object]]:
    skill_by_path = {str(skill["path"]): skill for skill in skills}
    skill_paths = sorted(skill_by_path, key=lambda value: value.count("/"), reverse=True)
    text_suffixes = {
        ".md",
        ".yaml",
        ".yml",
        ".json",
        ".csv",
        ".ts",
        ".js",
        ".py",
        ".sh",
        ".hbs",
        ".html",
        ".css",
        ".txt",
    }
    skipped_names = {"bun.lock", "package-lock.json"}
    artifacts: list[dict[str, object]] = []

    for file_path in sorted(SKILLS.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.name == "SKILL.md" or file_path.name in skipped_names:
            continue
        if file_path.suffix.lower() not in text_suffixes:
            continue

        rel_path = file_path.relative_to(SKILLS).as_posix()
        category = rel_path.split("/", 1)[0]
        parent_path = category
        for candidate in skill_paths:
            if rel_path.startswith(f"{candidate}/"):
                parent_path = candidate
                break
        parent = skill_by_path.get(parent_path)
        parent_name = str(parent["name"]) if parent else title_from_path(parent_path)
        kind = classify_artifact(rel_path)
        title, description = artifact_description(file_path, rel_path, kind, parent_name)
        artifacts.append(
            {
                "title": title,
                "description": description,
                "path": rel_path,
                "category": category,
                "kind": kind,
                "parentPath": parent_path,
                "parentName": parent_name,
                "depth": len(rel_path.split("/")),
                "link": f"{REPO_URL}/blob/main/skills/{rel_path}",
            }
        )

    return artifacts


def build_payload(skills: list[dict[str, object]], artifacts: list[dict[str, object]]) -> dict[str, object]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for skill in skills:
        grouped[str(skill["category"])].append(skill)
    artifacts_by_category: dict[str, list[dict[str, object]]] = defaultdict(list)
    for artifact in artifacts:
        artifacts_by_category[str(artifact["category"])].append(artifact)

    categories = []
    for name, items in sorted(grouped.items()):
        root_count = sum(1 for item in items if int(item["depth"]) == 1)
        categories.append(
            {
                "name": name,
                "count": len(items),
                "rootCount": root_count,
                "subskillCount": len(items) - root_count,
                "artifactCount": len(artifacts_by_category.get(name, [])),
                "description": CATEGORY_DESCRIPTIONS.get(name, "Public PAI skill category."),
                "maxDepth": max(int(item["depth"]) for item in items),
            }
        )

    root_skill_count = sum(1 for skill in skills if int(skill["depth"]) == 1)
    return {
        "generatedFrom": "skills/**/SKILL.md",
        "skillCount": len(skills),
        "rootSkillCount": root_skill_count,
        "subskillCount": len(skills) - root_skill_count,
        "categoryCount": len(categories),
        "artifactCount": len(artifacts),
        "repoUrl": REPO_URL,
        "categories": categories,
        "skills": skills,
        "artifacts": artifacts,
    }


def render_html(payload: dict[str, object]) -> str:
    data = json.dumps(payload, ensure_ascii=False)
    escaped_data = html.escape(data, quote=False)
    skill_count = payload["skillCount"]
    subskill_count = payload["subskillCount"]
    category_count = payload["categoryCount"]
    artifact_count = payload["artifactCount"]

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PAI Skills Atlas</title>
  <meta name="description" content="Interactive public skill tree for the PAI skills collection.">
  <style>
    :root {{
      --paper: #f7f7f5;
      --surface: #ffffff;
      --wash: #f0f0ed;
      --ink: #1a1a1a;
      --graphite: #4a4a4a;
      --concrete: #8a8a8a;
      --wire: #e2e2df;
      --teal: #0d9488;
      --teal-hover: #0f766e;
      --teal-muted: #ccfbf1;
      --green: #16a34a;
      --amber: #d97706;
      --red: #dc2626;
      --shadow-card: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
      --shadow-elevated: 0 4px 12px rgba(0,0,0,.08), 0 1px 3px rgba(0,0,0,.04);
      --font-sans: Satoshi, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      --font-mono: "JetBrains Mono", ui-monospace, "Cascadia Code", "Fira Code", monospace;
    }}

    * {{ box-sizing: border-box; }}

    html {{
      scroll-behavior: smooth;
      background: var(--paper);
      color: var(--ink);
    }}

    body {{
      margin: 0;
      font-family: var(--font-sans);
      line-height: 1.65;
      background:
        linear-gradient(90deg, rgba(226,226,223,.55) 1px, transparent 1px),
        linear-gradient(180deg, rgba(226,226,223,.45) 1px, transparent 1px),
        radial-gradient(circle at 82% 8%, rgba(13,148,136,.12), transparent 28rem),
        var(--paper);
      background-size: 48px 48px, 48px 48px, auto, auto;
    }}

    a {{ color: inherit; text-decoration: none; }}
    a:hover {{ color: var(--teal-hover); }}

    .shell {{
      width: min(1200px, calc(100% - clamp(2rem, 6vw, 4rem)));
      margin: 0 auto;
    }}

    .topbar {{
      position: sticky;
      top: 0;
      z-index: 20;
      border-bottom: 1px solid var(--wire);
      background: rgba(255,255,255,.9);
      backdrop-filter: blur(12px);
    }}

    .nav {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 64px;
      gap: 1rem;
    }}

    .brand {{
      font-weight: 700;
      letter-spacing: -.02em;
    }}

    .navlinks {{
      display: flex;
      align-items: center;
      gap: 1rem;
      color: var(--graphite);
      font-size: .875rem;
      font-weight: 500;
    }}

    .button {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 44px;
      border-radius: 6px;
      padding: 10px 20px;
      background: var(--teal);
      color: white;
      font-size: .875rem;
      font-weight: 500;
      letter-spacing: .01em;
      transition: background-color 150ms ease, transform 100ms ease;
    }}

    .button:hover {{
      color: white;
      background: var(--teal-hover);
      transform: translateY(-1px);
    }}

    .hero {{
      min-height: calc(100dvh - 64px);
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(280px, .75fr);
      align-items: center;
      gap: clamp(2rem, 6vw, 5rem);
      padding: clamp(4rem, 8vw, 7rem) 0;
    }}

    .eyebrow, .mono {{
      font-family: var(--font-mono);
      font-size: .75rem;
      letter-spacing: .04em;
      text-transform: uppercase;
      color: var(--teal);
    }}

    h1 {{
      max-width: 11ch;
      margin: .75rem 0 1.25rem;
      font-size: clamp(2.75rem, 6vw, 5.75rem);
      line-height: .95;
      letter-spacing: -.055em;
    }}

    .lede {{
      max-width: 55ch;
      margin: 0;
      color: var(--graphite);
      font-size: clamp(1.05rem, 1.8vw, 1.25rem);
      line-height: 1.7;
    }}

    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: .75rem;
      margin-top: 2rem;
      align-items: center;
    }}

    .text-link {{
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      font-weight: 600;
      color: var(--ink);
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1px;
      margin-top: 2rem;
      border: 1px solid var(--wire);
      background: var(--wire);
    }}

    .metric {{
      background: var(--wash);
      padding: 1rem;
    }}

    .metric strong {{
      display: block;
      font-family: var(--font-mono);
      font-size: clamp(1.45rem, 3vw, 2.25rem);
      line-height: 1.1;
    }}

    .metric span {{
      display: block;
      margin-top: .25rem;
      color: var(--concrete);
      font-size: .75rem;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    .studio-card {{
      position: relative;
      border: 1px solid var(--wire);
      background: var(--surface);
      border-radius: 12px;
      box-shadow: var(--shadow-card);
      padding: 1.25rem;
      overflow: hidden;
    }}

    .studio-card::before {{
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(90deg, rgba(226,226,223,.55) 1px, transparent 1px),
        linear-gradient(180deg, rgba(226,226,223,.45) 1px, transparent 1px);
      background-size: 32px 32px;
      pointer-events: none;
      mask-image: linear-gradient(180deg, black, transparent 70%);
    }}

    .atlas-frame {{
      position: relative;
      min-height: 420px;
    }}

    .atlas-frame::after {{
      content: "";
      position: absolute;
      left: 28%;
      top: 10%;
      bottom: 10%;
      width: 1px;
      background: var(--wire);
    }}

    .node {{
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: .65rem;
      width: 134px;
      min-height: 34px;
      border-radius: 6px;
      border: 1px solid var(--wire);
      background: rgba(255,255,255,.92);
      box-shadow: var(--shadow-card);
      color: var(--ink);
      font-family: var(--font-mono);
      font-size: .68rem;
      line-height: 1.2;
      text-align: left;
      padding: .45rem .55rem;
      transform: translate(-50%, -50%);
      transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    }}

    .node::before {{
      content: "";
      position: absolute;
      left: -44px;
      top: 50%;
      width: 44px;
      height: 1px;
      background: var(--wire);
    }}

    .node.is-center {{
      width: 132px;
      min-height: 132px;
      justify-content: center;
      text-align: center;
      left: 16%;
      top: 50%;
      border-radius: 999px;
      border-color: var(--teal);
      background: var(--teal-muted);
      font-weight: 700;
    }}

    .node.is-center::before {{
      display: none;
    }}

    .node-count {{
      color: var(--teal);
      font-weight: 700;
    }}

    .node:hover, .node.is-active {{
      border-color: var(--teal);
      box-shadow: var(--shadow-elevated);
      transform: translate(-50%, -50%) translateY(-2px);
    }}

    .section {{
      padding: clamp(4rem, 8vw, 7rem) 0;
      border-top: 1px solid var(--wire);
    }}

    .section-head {{
      display: grid;
      grid-template-columns: minmax(0, .8fr) minmax(280px, .7fr);
      gap: 2rem;
      align-items: end;
      margin-bottom: 2rem;
    }}

    h2 {{
      margin: .5rem 0 0;
      font-size: clamp(1.75rem, 3vw, 2.5rem);
      line-height: 1.12;
      letter-spacing: -.03em;
    }}

    .section-copy {{
      color: var(--graphite);
      margin: 0;
      max-width: 64ch;
    }}

    .controls {{
      display: grid;
      grid-template-columns: minmax(220px, .9fr) minmax(0, 1.1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
      align-items: start;
    }}

    .search {{
      width: 100%;
      min-height: 44px;
      padding: .75rem .9rem;
      border: 1px solid var(--wire);
      border-radius: 6px;
      background: var(--surface);
      color: var(--ink);
      font: 1rem/1.4 var(--font-sans);
      box-shadow: var(--shadow-card);
    }}

    .search:focus {{
      outline: 2px solid var(--teal);
      outline-offset: 2px;
      border-color: var(--teal);
    }}

    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: .5rem;
    }}

    .chip {{
      min-height: 36px;
      border: 1px solid var(--wire);
      border-radius: 6px;
      background: var(--surface);
      color: var(--graphite);
      cursor: pointer;
      padding: .45rem .7rem;
      font-family: var(--font-mono);
      font-size: .72rem;
      transition: background-color 150ms ease, border-color 150ms ease, transform 100ms ease;
    }}

    .chip:hover, .chip.is-active {{
      color: var(--teal-hover);
      background: var(--teal-muted);
      border-color: var(--teal);
      transform: translateY(-1px);
    }}

    .category-grid {{
      display: grid;
      grid-template-columns: 1.2fr .72fr .72fr 1fr;
      gap: 1px;
      background: var(--wire);
      border: 1px solid var(--wire);
    }}

    .category-row {{
      display: contents;
    }}

    .category-cell {{
      background: var(--surface);
      padding: 1rem;
    }}

    .category-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      font-weight: 700;
      letter-spacing: -.015em;
    }}

    .count {{
      font-family: var(--font-mono);
      color: var(--teal);
      font-size: .8rem;
    }}

    .bar {{
      height: .5rem;
      border-radius: 999px;
      background: var(--wash);
      overflow: hidden;
      margin-top: .7rem;
    }}

    .bar span {{
      display: block;
      height: 100%;
      border-radius: inherit;
      background: var(--teal);
    }}

    .skill-grid {{
      display: grid;
      grid-template-columns: 1.15fr .85fr;
      gap: 1rem;
      align-items: start;
    }}

    .skill-list {{
      display: grid;
      gap: .75rem;
    }}

    .skill-card {{
      display: block;
      width: 100%;
      border: 1px solid var(--wire);
      border-radius: 8px;
      background: var(--surface);
      padding: 1rem;
      box-shadow: var(--shadow-card);
      transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
      color: inherit;
      cursor: pointer;
      font: inherit;
      text-align: left;
    }}

    .skill-card:hover, .skill-card.is-active {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-elevated);
      border-color: var(--teal);
    }}

    .skill-card h3 {{
      margin: .35rem 0 .35rem;
      font-size: 1rem;
      line-height: 1.3;
      letter-spacing: -.015em;
    }}

    .skill-card p {{
      margin: 0;
      color: var(--graphite);
      font-size: .9rem;
      line-height: 1.55;
    }}

    .skill-path {{
      font-family: var(--font-mono);
      color: var(--concrete);
      font-size: .68rem;
      word-break: break-word;
      margin-top: .6rem;
    }}

    .panel {{
      position: sticky;
      top: 88px;
      border: 1px solid var(--wire);
      border-radius: 12px;
      background: var(--wash);
      padding: 1.25rem;
    }}

    .panel h3 {{
      margin: .5rem 0 .75rem;
      font-size: 1.2rem;
      letter-spacing: -.02em;
    }}

    .panel p {{
      color: var(--graphite);
      margin: 0 0 1rem;
    }}

    .detail-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: .45rem;
      margin: .9rem 0 1rem;
    }}

    .detail-pill {{
      border: 1px solid var(--wire);
      border-radius: 999px;
      background: var(--surface);
      color: var(--graphite);
      font-family: var(--font-mono);
      font-size: .68rem;
      padding: .28rem .55rem;
    }}

    .detail-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: .5rem;
      margin-bottom: 1rem;
    }}

    .detail-link {{
      min-height: 36px;
      display: inline-flex;
      align-items: center;
      border: 1px solid var(--wire);
      border-radius: 6px;
      background: var(--surface);
      color: var(--ink);
      font-size: .82rem;
      font-weight: 700;
      padding: .45rem .7rem;
      cursor: pointer;
      font-family: var(--font-sans);
    }}

    .detail-link:hover {{
      border-color: var(--teal);
      color: var(--teal-hover);
    }}

    .resource-group {{
      margin-top: 1rem;
    }}

    .resource-group h4 {{
      margin: 0 0 .5rem;
      font-family: var(--font-mono);
      color: var(--teal);
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    .resource-list {{
      display: grid;
      gap: .45rem;
    }}

    .resource-button {{
      width: 100%;
      border: 1px solid var(--wire);
      border-radius: 6px;
      background: var(--surface);
      color: var(--ink);
      cursor: pointer;
      padding: .6rem .65rem;
      text-align: left;
      font: inherit;
    }}

    .resource-button:hover, .resource-button.is-active {{
      border-color: var(--teal);
      box-shadow: var(--shadow-card);
    }}

    .resource-button strong {{
      display: block;
      font-size: .85rem;
      line-height: 1.25;
    }}

    .resource-button span {{
      display: block;
      margin-top: .2rem;
      color: var(--concrete);
      font-family: var(--font-mono);
      font-size: .62rem;
      word-break: break-word;
    }}

    .legend {{
      display: grid;
      gap: .75rem;
      margin-top: 1rem;
    }}

    .legend-item {{
      display: grid;
      grid-template-columns: 1rem 1fr;
      gap: .65rem;
      align-items: start;
      color: var(--graphite);
      font-size: .9rem;
    }}

    .mark {{
      width: .8rem;
      height: .8rem;
      margin-top: .45rem;
      border-radius: 999px;
      background: var(--teal);
    }}

    .mark.wire {{ background: var(--wire); border: 1px solid var(--concrete); }}
    .mark.paper {{ background: var(--paper); border: 1px solid var(--wire); }}

    .footer {{
      border-top: 1px solid var(--wire);
      padding: 2rem 0;
      color: var(--graphite);
      font-size: .9rem;
    }}

    .hidden {{ display: none !important; }}

    .system-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1px;
      border: 1px solid var(--wire);
      background: var(--wire);
    }}

    .system-card {{
      background: var(--surface);
      padding: 1.25rem;
    }}

    .system-card strong {{
      display: block;
      margin: .5rem 0;
      font-size: 1.05rem;
      letter-spacing: -.015em;
    }}

    .system-card p {{
      margin: 0;
      color: var(--graphite);
      font-size: .92rem;
    }}

    .note-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-top: 1rem;
    }}

    .note {{
      border: 1px solid var(--wire);
      border-radius: 8px;
      background: var(--wash);
      padding: 1rem;
      color: var(--graphite);
    }}

    @media (max-width: 900px) {{
      .hero, .section-head, .controls, .skill-grid, .system-grid, .note-grid {{
        grid-template-columns: 1fr;
      }}
      .hero {{
        min-height: auto;
      }}
      .category-grid {{
        grid-template-columns: 1fr;
      }}
      .category-row {{
        display: grid;
        grid-template-columns: 1fr;
      }}
      .panel {{
        position: static;
      }}
    }}

    @media (max-width: 640px) {{
      .shell {{
        width: min(100% - 1.5rem, 1200px);
      }}
      .navlinks {{
        display: none;
      }}
      .metrics {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
      .studio-card {{
        padding: .75rem;
        border-radius: 8px;
        overflow: visible;
      }}
      .atlas-frame {{
        min-height: auto;
        display: grid;
        grid-template-columns: 1fr;
        gap: .55rem;
        padding: .25rem;
      }}
      .atlas-frame::after {{
        display: none;
      }}
      .node {{
        position: relative;
        left: auto !important;
        top: auto !important;
        width: 100%;
        min-height: 44px;
        transform: none;
        font-size: .72rem;
        padding: .7rem .85rem;
        white-space: normal;
      }}
      .node::before {{
        display: none;
      }}
      .node.is-center {{
        width: 132px;
        min-height: 132px;
        justify-self: center;
        margin: .25rem 0 .7rem;
        line-height: 1.25;
      }}
      .node:hover, .node.is-active {{
        transform: translateY(-1px);
      }}
      .node-count {{
        flex: 0 0 auto;
        min-width: 2ch;
        text-align: right;
      }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <nav class="shell nav" aria-label="Primary navigation">
      <a class="brand" href="{REPO_URL}">PAI Skills</a>
      <div class="navlinks">
        <a href="#system">System</a>
        <a href="#categories">Categories</a>
        <a href="#skills">Skill Index</a>
        <a href="{REPO_URL}/blob/main/docs/catalog.md">Catalog</a>
      </div>
    </nav>
  </header>

  <main>
    <section class="shell hero" aria-labelledby="page-title">
      <div>
        <div class="eyebrow">Generated skill atlas · MJ brand system</div>
        <h1 id="page-title">Public PAI skill tree.</h1>
        <p class="lede">
          A readable map of the public agent skill collection: router skills, leaf workflows,
          operational tooling, and visualization systems exported without private workspace state.
        </p>
        <div class="hero-actions">
          <a class="button" href="#skills">Browse skills</a>
          <a class="text-link" href="{REPO_URL}">Open repository →</a>
        </div>
        <div class="metrics" aria-label="Skill tree metrics">
          <div class="metric"><strong>{skill_count}</strong><span>Public skills</span></div>
          <div class="metric"><strong>{subskill_count}</strong><span>Subskills</span></div>
          <div class="metric"><strong>{category_count}</strong><span>Categories</span></div>
          <div class="metric"><strong>{artifact_count}</strong><span>Artifacts</span></div>
        </div>
      </div>

      <aside class="studio-card" aria-label="Category constellation">
        <div class="atlas-frame" id="atlas">
          <div class="node is-center">PAI<br>Skills</div>
        </div>
      </aside>
    </section>

    <section class="section" id="system">
      <div class="shell">
        <div class="section-head">
          <div>
            <div class="eyebrow">Progressive disclosure</div>
            <h2>Agents route by metadata, then load only what the task needs.</h2>
          </div>
          <p class="section-copy">
            This atlas embeds all public skill metadata for human browsing. Agent runtimes should not
            eagerly load every skill body. They use the standard skill pattern: metadata for routing,
            activated instructions for execution, and resource files only when needed.
          </p>
        </div>
        <div class="system-grid" aria-label="Skill loading model">
          <div class="system-card">
            <span class="mono">Layer 01</span>
            <strong>Name + description</strong>
            <p>Small frontmatter metadata is available for routing. The description carries the trigger contract.</p>
          </div>
          <div class="system-card">
            <span class="mono">Layer 02</span>
            <strong>Activated SKILL.md</strong>
            <p>The full body loads only after the user request matches a relevant skill description.</p>
          </div>
          <div class="system-card">
            <span class="mono">Layer 03</span>
            <strong>Bundled resources</strong>
            <p>Scripts, references, workflows, and assets are read or executed on demand, not preloaded.</p>
          </div>
        </div>
        <div class="note-grid">
          <div class="note"><span class="mono">Subskill coverage</span><br>Every folder with its own `SKILL.md` is represented below, including nested skills such as Beads audits, Frontend/Impeccable commands, n8n specialists, document tools, and browser attach workflows.</div>
          <div class="note"><span class="mono">Convention status</span><br>Required frontmatter, public links, local-path hygiene, and secret-pattern gates pass. Large-skill warnings remain visible as candidates for future progressive splitting.</div>
        </div>
      </div>
    </section>

    <section class="section" id="categories">
      <div class="shell">
        <div class="section-head">
          <div>
            <div class="eyebrow">Category topology</div>
            <h2>Broad routers first, concrete workflows below.</h2>
          </div>
          <p class="section-copy">
            The tree is intentionally uneven. Root skills act as routers. Subskills are concrete
            operating guides with their own descriptions, paths, and activation triggers.
          </p>
        </div>
        <div class="category-grid" id="category-grid" aria-label="Category table"></div>
      </div>
    </section>

    <section class="section" id="skills">
      <div class="shell">
        <div class="section-head">
          <div>
            <div class="eyebrow">Skill index</div>
            <h2>Filter by category, name, description, or path.</h2>
          </div>
          <p class="section-copy">
            Use this as the practical navigation layer before installing or linking a skill into
            Codex, Claude, or another agent runtime. Click any card for details; searches also
            surface nested workflows, references, tools, prompts, configs, and data files.
          </p>
        </div>

        <div class="controls">
          <label>
            <span class="mono">Search</span>
            <input class="search" id="search" type="search" placeholder="Try: beads, browser, frontend, research">
          </label>
          <div class="chips" id="chips" aria-label="Category filters"></div>
        </div>

        <div class="skill-grid">
          <div class="skill-list" id="skill-list"></div>
          <aside class="panel" aria-label="Selected item details" id="detail-panel">
            <div id="detail-content"></div>
          </aside>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="shell">
      <span class="mono">Generated from {html.escape(str(payload["generatedFrom"]))}</span>
      <span> · Public repository: <a href="{REPO_URL}">{REPO_URL}</a></span>
    </div>
  </footer>

  <script id="skill-data" type="application/json">{escaped_data}</script>
  <script>
    const payload = JSON.parse(document.getElementById('skill-data').textContent);
    const atlas = document.getElementById('atlas');
    const categoryGrid = document.getElementById('category-grid');
    const chips = document.getElementById('chips');
    const skillList = document.getElementById('skill-list');
    const search = document.getElementById('search');
    const detailContent = document.getElementById('detail-content');
    const maxCategoryCount = Math.max(...payload.categories.map(category => category.count));
    let activeCategory = 'All';
    let selectedType = 'category';
    let selectedPath = payload.categories[0]?.name || 'All';

    const skillsByPath = new Map(payload.skills.map(skill => [skill.path, skill]));
    const artifactsByPath = new Map(payload.artifacts.map(artifact => [artifact.path, artifact]));
    const artifactsByParent = payload.artifacts.reduce((groups, artifact) => {{
      if (!groups.has(artifact.parentPath)) groups.set(artifact.parentPath, []);
      groups.get(artifact.parentPath).push(artifact);
      return groups;
    }}, new Map());

    function textIncludes(value, query) {{
      return String(value || '').toLowerCase().includes(query);
    }}

    function escapeHtml(value) {{
      return String(value || '').replace(/[&<>"']/g, char => ({{
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      }}[char]));
    }}

    function filteredSkills() {{
      const query = search.value.trim().toLowerCase();
      return payload.skills.filter(skill => {{
        const inCategory = activeCategory === 'All' || skill.category === activeCategory;
        const matchesQuery = !query ||
          textIncludes(skill.name, query) ||
          textIncludes(skill.description, query) ||
          textIncludes(skill.path, query) ||
          textIncludes(skill.category, query);
        return inCategory && matchesQuery;
      }});
    }}

    function filteredArtifacts() {{
      const query = search.value.trim().toLowerCase();
      if (!query) return [];
      return payload.artifacts.filter(artifact => {{
        const inCategory = activeCategory === 'All' || artifact.category === activeCategory;
        const matchesQuery =
          textIncludes(artifact.title, query) ||
          textIncludes(artifact.description, query) ||
          textIncludes(artifact.path, query) ||
          textIncludes(artifact.kind, query) ||
          textIncludes(artifact.parentName, query) ||
          textIncludes(artifact.category, query);
        return inCategory && matchesQuery;
      }});
    }}

    function selectCategory(name) {{
      selectedType = 'category';
      selectedPath = name;
      renderDetail();
      syncActiveCards();
    }}

    function selectSkill(path) {{
      selectedType = 'skill';
      selectedPath = path;
      renderDetail();
      syncActiveCards();
    }}

    function selectArtifact(path) {{
      selectedType = 'artifact';
      selectedPath = path;
      renderDetail();
      syncActiveCards();
    }}

    function groupedArtifacts(artifacts) {{
      return artifacts.reduce((groups, artifact) => {{
        if (!groups[artifact.kind]) groups[artifact.kind] = [];
        groups[artifact.kind].push(artifact);
        return groups;
      }}, {{}});
    }}

    function renderArtifactGroups(artifacts, emptyText) {{
      if (!artifacts.length) {{
        return `<p>${{escapeHtml(emptyText)}}</p>`;
      }}

      return Object.entries(groupedArtifacts(artifacts)).map(([kind, items]) => `
        <div class="resource-group">
          <h4>${{escapeHtml(kind)}} · ${{items.length}}</h4>
          <div class="resource-list">
            ${{items.map(item => `
              <button class="resource-button" type="button" data-artifact-path="${{escapeHtml(item.path)}}">
                <strong>${{escapeHtml(item.title)}}</strong>
                <span>${{escapeHtml(item.path)}}</span>
              </button>
            `).join('')}}
          </div>
        </div>
      `).join('');
    }}

    function renderDetail() {{
      if (selectedType === 'skill') {{
        const skill = skillsByPath.get(selectedPath) || payload.skills[0];
        const artifacts = artifactsByParent.get(skill.path) || [];
        detailContent.innerHTML = `
          <div class="eyebrow">Skill detail</div>
          <h3>${{escapeHtml(skill.name)}}</h3>
          <p>${{escapeHtml(skill.description)}}</p>
          <div class="detail-meta">
            <span class="detail-pill">${{escapeHtml(skill.category)}}</span>
            <span class="detail-pill">depth ${{skill.depth}}</span>
            <span class="detail-pill">${{artifacts.length}} nested artifacts</span>
          </div>
          <div class="detail-actions">
            <a class="detail-link" href="${{escapeHtml(skill.link)}}">Open source</a>
            <button class="detail-link" type="button" data-category-name="${{escapeHtml(skill.category)}}">Show category</button>
          </div>
          <div class="skill-path">${{escapeHtml(skill.path)}}</div>
          ${{renderArtifactGroups(artifacts, 'No nested workflows or resource files were exported for this skill.')}}
        `;
      }} else if (selectedType === 'artifact') {{
        const artifact = artifactsByPath.get(selectedPath) || payload.artifacts[0];
        const parent = skillsByPath.get(artifact.parentPath);
        detailContent.innerHTML = `
          <div class="eyebrow">${{escapeHtml(artifact.kind)}} detail</div>
          <h3>${{escapeHtml(artifact.title)}}</h3>
          <p>${{escapeHtml(artifact.description)}}</p>
          <div class="detail-meta">
            <span class="detail-pill">${{escapeHtml(artifact.kind)}}</span>
            <span class="detail-pill">${{escapeHtml(artifact.category)}}</span>
            <span class="detail-pill">parent: ${{escapeHtml(artifact.parentName)}}</span>
          </div>
          <div class="detail-actions">
            <a class="detail-link" href="${{escapeHtml(artifact.link)}}">Open source</a>
            ${{parent ? `<button class="detail-link" type="button" data-skill-path="${{escapeHtml(parent.path)}}">Open parent skill</button>` : ''}}
          </div>
          <div class="skill-path">${{escapeHtml(artifact.path)}}</div>
        `;
      }} else {{
        const category = payload.categories.find(item => item.name === selectedPath) || payload.categories[0];
        const skills = payload.skills.filter(skill => skill.category === category.name);
        const artifacts = payload.artifacts.filter(artifact => artifact.category === category.name);
        detailContent.innerHTML = `
          <div class="eyebrow">Category detail</div>
          <h3>${{escapeHtml(category.name)}}</h3>
          <p>${{escapeHtml(category.description)}}</p>
          <div class="detail-meta">
            <span class="detail-pill">${{category.count}} skills</span>
            <span class="detail-pill">${{category.subskillCount}} subskills</span>
            <span class="detail-pill">${{category.artifactCount}} artifacts</span>
          </div>
          <div class="resource-group">
            <h4>Skills · ${{skills.length}}</h4>
            <div class="resource-list">
              ${{skills.map(skill => `
                <button class="resource-button" type="button" data-skill-path="${{escapeHtml(skill.path)}}">
                  <strong>${{escapeHtml(skill.name)}}</strong>
                  <span>${{escapeHtml(skill.path)}}</span>
                </button>
              `).join('')}}
            </div>
          </div>
          ${{renderArtifactGroups(artifacts.slice(0, 30), artifacts.length ? '' : 'No artifacts found for this category.')}}
          ${{artifacts.length > 30 ? `<p><span class="mono">${{artifacts.length - 30}} more artifacts</span><br>Use search to narrow the remaining workflows, tools, references, and config files in this category.</p>` : ''}}
        `;
      }}
    }}

    function renderAtlas() {{
      payload.categories.forEach((category, index) => {{
        const firstColumn = index < Math.ceil(payload.categories.length / 2);
        const columnIndex = firstColumn ? index : index - Math.ceil(payload.categories.length / 2);
        const rows = firstColumn ? Math.ceil(payload.categories.length / 2) : Math.floor(payload.categories.length / 2);
        const x = firstColumn ? 46 : 82;
        const y = 10 + (columnIndex * (80 / Math.max(rows - 1, 1)));
        const node = document.createElement('button');
        node.className = 'node';
        node.type = 'button';
        node.style.left = `${{x}}%`;
        node.style.top = `${{y}}%`;
        node.dataset.category = category.name;
        node.innerHTML = `<span>${{category.name}}</span><span class="node-count">${{category.count}}</span>`;
        node.setAttribute('aria-label', `Filter to ${{category.name}} skills`);
        node.addEventListener('click', () => {{
          setCategory(category.name);
          selectCategory(category.name);
        }});
        atlas.appendChild(node);
      }});
    }}

    function renderCategories() {{
      categoryGrid.innerHTML = '';
      payload.categories.forEach(category => {{
        const row = document.createElement('div');
        row.className = 'category-row';
        row.dataset.category = category.name;
        row.innerHTML = `
          <div class="category-cell">
            <div class="category-title">
              <span>${{category.name}}</span>
              <span class="count">${{category.count}} skills</span>
            </div>
            <div class="bar" aria-hidden="true"><span style="width:${{Math.round((category.count / maxCategoryCount) * 100)}}%"></span></div>
          </div>
          <div class="category-cell"><span class="mono">${{category.subskillCount}} subskills</span></div>
          <div class="category-cell"><span class="mono">${{category.artifactCount}} artifacts</span></div>
          <div class="category-cell">${{category.description}}</div>
        `;
        row.addEventListener('click', () => {{
          setCategory(category.name);
          selectCategory(category.name);
        }});
        categoryGrid.appendChild(row);
      }});
    }}

    function renderChips() {{
      chips.innerHTML = '';
      ['All', ...payload.categories.map(category => category.name)].forEach(name => {{
        const button = document.createElement('button');
        button.className = `chip${{name === activeCategory ? ' is-active' : ''}}`;
        button.type = 'button';
        button.textContent = name;
        button.addEventListener('click', () => setCategory(name));
        chips.appendChild(button);
      }});
    }}

    function renderSkills() {{
      const skills = filteredSkills();
      const artifacts = filteredArtifacts();
      skillList.innerHTML = '';
      if (!skills.length && !artifacts.length) {{
        const empty = document.createElement('div');
        empty.className = 'skill-card';
        empty.innerHTML = '<span class="mono">No matches</span><h3>Adjust the filter.</h3><p>No public skill matched the current category and search query.</p>';
        skillList.appendChild(empty);
        return;
      }}

      skills.forEach(skill => {{
        const card = document.createElement('button');
        card.className = 'skill-card';
        card.type = 'button';
        card.dataset.skillPath = skill.path;
        card.innerHTML = `
          <span class="mono">${{skill.category}}</span>
          <h3>${{skill.name}}</h3>
          <p>${{skill.description}}</p>
          <div class="skill-path">${{skill.path}}</div>
        `;
        card.addEventListener('click', () => selectSkill(skill.path));
        skillList.appendChild(card);
      }});

      artifacts.forEach(artifact => {{
        const card = document.createElement('button');
        card.className = 'skill-card';
        card.type = 'button';
        card.dataset.artifactPath = artifact.path;
        card.innerHTML = `
          <span class="mono">${{artifact.kind}} · ${{artifact.parentName}}</span>
          <h3>${{artifact.title}}</h3>
          <p>${{artifact.description}}</p>
          <div class="skill-path">${{artifact.path}}</div>
        `;
        card.addEventListener('click', () => selectArtifact(artifact.path));
        skillList.appendChild(card);
      }});
      syncActiveCards();
    }}

    function syncActiveNodes() {{
      document.querySelectorAll('.node:not(.is-center)').forEach(node => {{
        node.classList.toggle('is-active', node.dataset.category === activeCategory);
      }});
      document.querySelectorAll('.category-row').forEach(row => {{
        const selected = activeCategory === 'All' || row.dataset.category === activeCategory;
        row.classList.toggle('hidden', !selected && search.value.trim());
      }});
    }}

    function syncActiveCards() {{
      document.querySelectorAll('[data-skill-path]').forEach(card => {{
        card.classList.toggle('is-active', selectedType === 'skill' && card.dataset.skillPath === selectedPath);
      }});
      document.querySelectorAll('[data-artifact-path]').forEach(card => {{
        card.classList.toggle('is-active', selectedType === 'artifact' && card.dataset.artifactPath === selectedPath);
      }});
      document.querySelectorAll('[data-category-name]').forEach(card => {{
        card.classList.toggle('is-active', selectedType === 'category' && card.dataset.categoryName === selectedPath);
      }});
    }}

    function setCategory(name) {{
      activeCategory = name;
      renderChips();
      renderSkills();
      syncActiveNodes();
      if (name !== 'All') selectCategory(name);
    }}

    search.addEventListener('input', () => {{
      renderSkills();
      syncActiveNodes();
    }});

    detailContent.addEventListener('click', (event) => {{
      const skillButton = event.target.closest('[data-skill-path]');
      if (skillButton) {{
        selectSkill(skillButton.dataset.skillPath);
        return;
      }}
      const artifactButton = event.target.closest('[data-artifact-path]');
      if (artifactButton) {{
        selectArtifact(artifactButton.dataset.artifactPath);
        return;
      }}
      const categoryButton = event.target.closest('[data-category-name]');
      if (categoryButton) {{
        setCategory(categoryButton.dataset.categoryName);
      }}
    }});

    renderAtlas();
    renderCategories();
    renderChips();
    renderSkills();
    renderDetail();
  </script>
</body>
</html>
"""


def main() -> int:
    skills = collect_skills()
    artifacts = collect_artifacts(skills)
    payload = build_payload(skills, artifacts)
    OUT.write_text(render_html(payload))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), **{k: payload[k] for k in ("skillCount", "categoryCount", "artifactCount")}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
