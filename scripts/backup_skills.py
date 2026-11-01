#!/usr/bin/env python3
"""Snapshot installed skill directories and verify their copied bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
from datetime import datetime, timezone


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--destination', type=Path, default=Path.home() / '.backup_skills')
    args = parser.parse_args()
    roots = [args.home / '.codex/skills', args.home / '.codex/plugins', args.home / '.agents/skills']
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    snapshot = args.destination / stamp
    snapshot.mkdir(parents=True, mode=0o700)
    entries = []
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for folder, dirs, files in os.walk(root, followlinks=True):
            dirs[:] = sorted(d for d in dirs if d not in {'.git', '__pycache__', 'node_modules'})
            source = Path(folder)
            identity = source.stat().st_dev, source.stat().st_ino
            if identity in seen:
                dirs[:] = []
                continue
            seen.add(identity)
            if 'SKILL.md' not in files:
                continue
            relative = source.relative_to(args.home)
            target = snapshot / 'files' / relative
            shutil.copytree(source, target, symlinks=False)
            for copied in sorted(target.rglob('*')):
                if not copied.is_file():
                    continue
                original = source / copied.relative_to(target)
                checksum = digest(copied)
                if checksum != digest(original):
                    raise RuntimeError(f'Backup mismatch: {original}')
                entries.append({'source': str(original), 'backup': str(copied.relative_to(snapshot)), 'sha256': checksum})
            dirs[:] = []
    if not entries:
        raise RuntimeError('No skill files found; backup is incomplete')
    manifest = {'created_utc': stamp, 'files': entries}
    (snapshot / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'snapshot': str(snapshot), 'files_verified': len(entries)}))


if __name__ == '__main__':
    main()
