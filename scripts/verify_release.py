"""Verify a versioned dataset's exact file hashes, sizes, and file coverage."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def verify(root: Path) -> int:
    root = root.resolve()
    entries = set()
    manifest = root / "MANIFEST.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})\s+(\d+)\s+(.+)", line)
        if not match:
            raise ValueError("Malformed manifest entry")
        expected, size, name = match.groups()
        path = (root / name).resolve()
        if not path.is_relative_to(root) or name in entries or path == manifest:
            raise ValueError("Invalid or duplicate manifest path")
        if not path.is_file() or path.stat().st_size != int(size):
            raise ValueError(f"Missing file or size mismatch: {name}")
        h = hashlib.sha256()
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                h.update(block)
        if h.hexdigest() != expected:
            raise ValueError(f"Hash mismatch: {name}")
        entries.add(name)
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
              if p.is_file() and p != manifest}
    if not entries or entries != actual:
        raise ValueError("Manifest file coverage mismatch")
    return len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release", type=Path)
    args = parser.parse_args()
    try:
        count = verify(args.release)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Verification failed: {exc}\n")
    print(json.dumps({"manifest_entries": count, "verified": True}))


if __name__ == "__main__":
    main()
