#!/usr/bin/env python3
"""Read a UTSR-ToolMeta JSONL file and print a few compact records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    for idx, record in enumerate(iter_jsonl(args.path), start=1):
        utsr = record["utsr"]
        profile = record["function_profile"]
        compact = {
            "record_id": record["record_id"],
            "source_family": record["source_meta"].get("source_family"),
            "name": utsr["identity"].get("name"),
            "namespace": utsr["identity"].get("namespace"),
            "description": utsr["capability"].get("description"),
            "primary_domain": profile.get("primary_domain"),
            "primary_subdomain": profile.get("primary_subdomain"),
            "supported_actions": profile.get("supported_actions"),
            "effect_class": profile.get("effect_class"),
            "cardinality": profile.get("cardinality"),
            "task_intent": profile.get("task_intent"),
        }
        print(json.dumps(compact, ensure_ascii=False, indent=2))
        if idx >= args.limit:
            break


if __name__ == "__main__":
    main()
