#!/usr/bin/env python3
"""Check the file map, catalog links, and application naming."""

import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    names = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=ROOT,
    ).decode().split('\0')
    files = sorted({ROOT / name for name in names if name and (ROOT / name).is_file()})
    errors = []
    seen = {}
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        previous = seen.setdefault(relative.casefold(), relative)
        if previous != relative:
            errors.append(f'Case conflict: {previous} and {relative}')

    mapping = json.loads((ROOT / 'docs/file-map.json').read_text())
    for old, new in mapping['moves'].items():
        target = (ROOT / new).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f'File map destination missing: {old} -> {new}')
    for old in mapping['removed_scaffolding']:
        if (ROOT / old).exists():
            errors.append(f'Removed scaffold still present: {old}')

    links = 0
    for path in files:
        if path.suffix != '.md':
            continue
        for match in re.finditer(r'\]\(([^\n]+?)\)', path.read_text()):
            href = match.group(1).strip('<>')
            url = urlsplit(href)
            if url.scheme or url.netloc or href.startswith('#'):
                continue
            target = (path.parent / unquote(url.path)).resolve()
            links += 1
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing link {href}')
            elif target.is_dir() and not any(p.is_relative_to(target) for p in files):
                errors.append(f'{path.relative_to(ROOT)}: empty linked directory {href}')

    graphs = 0
    for path in files:
        if path.suffix != '.grc':
            continue
        text = path.read_text()
        if text.lstrip().startswith('<?xml'):
            continue
        match = re.search(r'^    id: (\w+)$', text, re.M)
        graphs += 1
        if not match or match[1] != path.stem:
            errors.append(f'{path.relative_to(ROOT)}: graph ID must match filename')

    for error in errors:
        print(error, file=sys.stderr)
    print(f'Checked {len(mapping["moves"])} moved paths, {links} local links, and {graphs} application IDs.')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
