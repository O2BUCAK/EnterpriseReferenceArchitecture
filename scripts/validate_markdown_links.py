#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
errors = []

for path in ROOT.rglob("*.md"):
    if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
        continue
    for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        target = target.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        candidate = (path.parent / target.replace("%20", " ")).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path}: link escapes repository: {target}")
            continue
        if not candidate.exists():
            errors.append(f"{path}: missing link target: {target}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Markdown relative-link validation passed.")
