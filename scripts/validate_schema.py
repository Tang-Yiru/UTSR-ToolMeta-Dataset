#!/usr/bin/env python3
"""Validate JSONL records against the UTSR-ToolMeta JSON Schema.

If the optional `jsonschema` package is installed, this script performs full
JSON Schema validation. Otherwise, it falls back to the lightweight integrity
checks implemented in `check_record_integrity.py`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                yield line_no, json.loads(line)


def fallback(paths: list[Path]) -> int:
    script = Path(__file__).with_name("check_record_integrity.py")
    return subprocess.call([sys.executable, str(script), *map(str, paths)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--schema", type=Path, default=Path("schema/utsr_record.schema.json"))
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    try:
        import jsonschema
    except Exception:
        print("jsonschema is not installed; using lightweight integrity checks.")
        raise SystemExit(fallback(args.paths))

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = 0
    records = 0

    for path in args.paths:
        for line_no, record in iter_jsonl(path):
            records += 1
            for error in validator.iter_errors(record):
                if errors < args.max_errors:
                    loc = ".".join(map(str, error.absolute_path))
                    print(f"{path}:{line_no}: {loc}: {error.message}")
                errors += 1

    print(json.dumps({"records": records, "schema_errors": errors}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

