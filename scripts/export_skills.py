#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

SOURCE = Path('${PAI_EXTENSIONS_DIR}/skills')
DEST = Path(__file__).resolve().parents[1] / 'skills'
DOCS = Path(__file__).resolve().parents[1] / 'docs'

# Conservative first public cut. Excluded skills can be added after manual privacy/provenance review.
EXCLUDED_TOP = {
    'Pai',            # machine/persona-specific operating system
    'Telos',          # private original; portable project variant lives in skills/ProjectTelos
    'Inbox',          # local inbox behavior
    'GoogleWorkspace',# account/workspace-specific integration risk
    'ccgram-messaging', # local inter-agent messaging setup
    'Gsd',            # personal operating workflow
}
EXCLUDED_SUBPATHS = {
    'Frontend/Aesthetics/mj-brand', # personal brand design system
    'Utilities/Aphorisms', # personal curated quote database workflow
    'Utilities/DistillToTelos', # personal TELOS belief-candidate workflow
    'Utilities/Fabric', # third-party upstream pattern library; use install/sync docs instead
}
EXCLUDED_PATHS = {
    # Keep private original out; portable public variant lives in skills/Research.
    'Research',
}
PUBLIC_VARIANTS = {
    'Research': 'Portable public variant included at skills/Research.',
    'Telos': 'Project-only public variant included at skills/ProjectTelos.',
}
IGNORE_NAMES = {'__pycache__', '.DS_Store', '.git', 'node_modules', 'dist', 'build'}


def parse_skill(path: Path) -> dict:
    text = path.read_text(errors='ignore')
    fm = {}
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if match:
        for line in match.group(1).splitlines():
            if ':' in line and not line.startswith(' '):
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip().strip('"')
    return {
        'name': fm.get('name'),
        'description': fm.get('description'),
        'lines': len(text.splitlines()),
    }


def ignore(dirpath: str, names: list[str]) -> set[str]:
    ignored = {name for name in names if name in IGNORE_NAMES}
    ignored |= {name for name in names if name.endswith('.pyc') or name.endswith('.log')}
    current = Path(dirpath)
    try:
        rel_dir = current.relative_to(SOURCE).as_posix()
    except ValueError:
        rel_dir = ''
    for subpath in EXCLUDED_SUBPATHS:
        parent, leaf = subpath.rsplit('/', 1)
        if rel_dir == parent and leaf in names:
            ignored.add(leaf)
    return ignored


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    copied = []
    excluded = []
    for child in sorted(SOURCE.iterdir()):
        if not child.is_dir():
            continue
        reason = None
        if child.name in EXCLUDED_TOP or child.name in EXCLUDED_PATHS:
            reason = PUBLIC_VARIANTS.get(child.name, 'private/local review required before public release')
        if reason:
            excluded.append({'path': child.name, 'reason': reason})
            continue
        target = DEST / child.name
        if target.exists() or target.is_symlink():
            shutil.rmtree(target)
        shutil.copytree(child, target, ignore=ignore, symlinks=False, ignore_dangling_symlinks=True)
        for skill in target.rglob('SKILL.md'):
            meta = parse_skill(skill)
            copied.append({
                'path': str(skill.relative_to(DEST).parent),
                **meta,
            })

    (DOCS / 'export-manifest.json').write_text(json.dumps({
        'source': str(SOURCE),
        'destination': str(DEST),
        'copied_count': len(copied),
        'copied': copied,
        'excluded': excluded,
        'public_variants': PUBLIC_VARIANTS,
    }, indent=2) + '\n')

    lines = ['# Private / Local Exclusions', '', 'These local skill groups were not copied into the first public-ready export.', '']
    for item in excluded:
        lines.append(f"- `{item['path']}` — {item['reason']}")
    lines.extend(['', 'Review and sanitize these manually before adding them to a public repository.'])
    (DOCS / 'private-exclusions.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'copied_count': len(copied), 'excluded': excluded}, indent=2))


if __name__ == '__main__':
    main()
