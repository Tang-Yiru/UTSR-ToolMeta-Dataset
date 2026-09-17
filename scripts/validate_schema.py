#!/usr/bin/env python3
"""Validate JSONL records against the UTSR-ToolMeta JSON Schema.

Requires `jsonschema`; basic integrity checks are available separately.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                yield line_no, json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "releases/v0.2/schema/utsr_record.schema.json")
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    try:
        import jsonschema
    except ImportError:
        print("Install requirements.txt for full schema validation.", file=sys.stderr)
        raise SystemExit(2)

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
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
