#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'

LOCAL_PATH_PATTERNS = [
    re.compile('/home/' + 'mj'),
    re.compile(r'~/' + r'\.claude'),
    re.compile(r'~/' + r'\.codex'),
    re.compile('/tmp' + '/'),
]
SECRET_PATTERNS = [
    re.compile(r'(?i)api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]{12,}'),
    re.compile(r'(?i)token\s*[:=]\s*[A-Za-z0-9_\-]{16,}'),
    re.compile(r'(?i)secret\s*[:=]\s*[A-Za-z0-9_\-]{12,}'),
    re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        return {}
    out = {}
    for line in match.group(1).splitlines():
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            out[key.strip()] = value.strip().strip('"')
    return out


def iter_md_links(text: str):
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
        target = match.group(1).split('#', 1)[0]
        if not target or target.startswith('#'):
            continue
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('/'):
            continue
        if any(char in target for char in '[]^+*'):
            continue
        yield target


def main() -> int:
    skills = []
    errors = []
    warnings = []
    link_issues = []
    local_refs = []
    secret_hits = []

    for skill_file in sorted(SKILLS.rglob('SKILL.md')):
        rel = skill_file.relative_to(SKILLS)
        text = skill_file.read_text(errors='ignore')
        fm = parse_frontmatter(text)
        name = fm.get('name')
        desc = fm.get('description')
        if not fm:
            errors.append({'path': str(rel), 'kind': 'missing_frontmatter'})
        if not name:
            errors.append({'path': str(rel), 'kind': 'missing_name'})
        if not desc:
            errors.append({'path': str(rel), 'kind': 'missing_description'})
        if len(text.splitlines()) > 500:
            warnings.append({'path': str(rel), 'kind': 'large_skill', 'lines': len(text.splitlines())})
        skills.append({
            'path': str(rel.parent),
            'name': name,
            'description': desc,
            'lines': len(text.splitlines()),
            'category': rel.parts[0] if len(rel.parts) > 1 else rel.parent.name,
        })

    names = [s['name'] for s in skills if s['name']]
    for name, count in Counter(names).items():
        if count > 1:
            errors.append({'name': name, 'kind': 'duplicate_name', 'count': count})

    for file in sorted(SKILLS.rglob('*')):
        if not file.is_file():
            continue
        try:
            text = file.read_text(errors='ignore')
        except UnicodeDecodeError:
            continue
        rel = file.relative_to(SKILLS)
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                local_refs.append({'path': str(rel), 'pattern': pattern.pattern})
                break
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                secret_hits.append({'path': str(rel), 'pattern': pattern.pattern})
        if file.suffix.lower() == '.md' or file.name == 'SKILL.md':
            for target in iter_md_links(text):
                if not (file.parent / target).resolve().exists():
                    link_issues.append({'path': str(rel), 'target': target})

    by_category = defaultdict(list)
    for skill in skills:
        by_category[skill['category']].append(skill)

    report = {
        'ok': not errors and not secret_hits and not link_issues and not local_refs,
        'skill_count': len(skills),
        'category_count': len(by_category),
        'errors': errors,
        'warnings': warnings,
        'missing_relative_links': link_issues,
        'local_path_references': local_refs,
        'secret_pattern_hits': secret_hits,
        'categories': {key: sorted(value, key=lambda item: item['name'] or '') for key, value in sorted(by_category.items())},
    }
    print(json.dumps(report, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
