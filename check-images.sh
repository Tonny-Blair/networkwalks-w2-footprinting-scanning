#!/usr/bin/env bash
# Run from the repository root: bash check-images.sh
# Checks local Markdown image links and HTML <img src="..."> paths in README.md.
set -euo pipefail

python3 - <<'PY'
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

readme = Path('README.md')
if not readme.is_file():
    print('ERROR    README.md not found. Run this script from the repository root.')
    sys.exit(2)

source = readme.read_text(encoding='utf-8')
refs = []
refs.extend(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', source))
refs.extend(re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', source, flags=re.I))

bad = False
seen = set()
for raw in refs:
    target = raw.strip().split()[0].strip('<>')
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith('//') or not parsed.path:
        continue
    path_text = unquote(parsed.path)
    path = Path(path_text)
    if path_text.startswith('/'):
        print(f'WARNING  {target} is an absolute path; use a repository-relative path')
        bad = True
        continue
    if not path.is_file():
        print(f'MISSING  {target}')
        bad = True
    else:
        print(f'OK       {target}')
    if target in seen:
        continue
    seen.add(target)

if not refs:
    print('WARNING  No Markdown or HTML image references found in README.md')
    bad = True

if bad:
    print('\nCheck failed. Fix the missing or invalid image paths above.')
    sys.exit(1)

print('\nAll local README image references were found.')
PY
