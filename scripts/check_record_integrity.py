#!/usr/bin/env python3
"""Check basic integrity of UTSR-ToolMeta JSONL records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_TOP_KEYS = {
    "record_id",
    "dataset_meta",
    "source_meta",
    "function_profile",
    "utsr",
    "provenance",
}

REQUIRED_UTSR_KEYS = {"source", "identity", "capability", "interface", "binding"}


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc


def check_record(line_no: int, record: dict[str, Any]) -> list[str]:
    errors = []
    top_keys = set(record)
    missing = REQUIRED_TOP_KEYS - top_keys
    extra = top_keys - REQUIRED_TOP_KEYS
    if missing:
        errors.append(f"line {line_no}: missing top-level keys {sorted(missing)}")
    if extra:
        errors.append(f"line {line_no}: unexpected top-level keys {sorted(extra)}")

    utsr = record.get("utsr")
    if not isinstance(utsr, dict):
        errors.append(f"line {line_no}: utsr is not an object")
        return errors
    missing_utsr = REQUIRED_UTSR_KEYS - set(utsr)
    if missing_utsr:
        errors.append(f"line {line_no}: missing utsr keys {sorted(missing_utsr)}")

    name = (((utsr.get("identity") or {}).get("name")) or "").strip()
    desc = (((utsr.get("capability") or {}).get("description")) or "").strip()
    if not name:
        errors.append(f"line {line_no}: empty utsr.identity.name")
    if not desc:
        errors.append(f"line {line_no}: empty utsr.capability.description")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    total = 0
    error_count = 0
    summaries = []

    for path in args.paths:
        file_total = 0
        duplicate_count = 0
        families = Counter()
        seen_ids = set()
        for line_no, record in load_jsonl(path):
            file_total += 1
            total += 1
            record_id = record.get("record_id")
            if record_id in seen_ids:
                duplicate_count += 1
                if error_count < args.max_errors:
                    print(f"{path}:{line_no}: duplicate record_id {record_id}")
                error_count += 1
            seen_ids.add(record_id)

            families[record.get("source_meta", {}).get("source_family", "unknown")] += 1
            errors = check_record(line_no, record)
            for error in errors:
                if error_count < args.max_errors:
                    print(f"{path}:{error}")
                error_count += 1
        summaries.append({
            "path": str(path),
            "records": file_total,
            "unique_record_ids": len(seen_ids),
            "duplicates_within_file": duplicate_count,
            "source_families": dict(families),
        })

    print(json.dumps({
        "records_checked": total,
        "errors": error_count,
        "files": summaries,
    }, indent=2, ensure_ascii=False))

    if error_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
