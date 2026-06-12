#!/usr/bin/env python3
"""Generate summary statistics for a UTSR-ToolMeta JSONL file."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_counter_csv(path: Path, name: str, counter: Counter[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, "count"])
        for key, value in counter.most_common():
            writer.writerow([key, value])


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    source_family = Counter()
    domain = Counter()
    subdomain = Counter()
    function_type = Counter()
    profile_origin = Counter()
    task_intents = set()

    for record in records:
        source_family[record["source_meta"].get("source_family", "unknown")] += 1
        profile = record["function_profile"]
        domain[profile.get("domain", "unknown")] += 1
        subdomain[profile.get("subdomain", "unknown")] += 1
        function_type[profile.get("function_type", "unknown")] += 1
        profile_origin[profile.get("profile_origin", "unknown")] += 1
        intent = profile.get("task_intent")
        if intent:
            task_intents.add(intent)

    return {
        "records": len(records),
        "source_family": dict(source_family.most_common()),
        "domain_unique": len(domain),
        "subdomain_unique": len(subdomain),
        "function_type_unique": len(function_type),
        "task_intent_unique": len(task_intents),
        "top_domains": dict(domain.most_common(20)),
        "function_type": dict(function_type.most_common()),
        "profile_origin": dict(profile_origin.most_common()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--out", type=Path, default=Path("stats"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    records = list(iter_jsonl(args.path))
    summary = summarize(records)

    (args.out / "dataset_statistics.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    source_family = Counter(r["source_meta"].get("source_family", "unknown") for r in records)
    domain = Counter(r["function_profile"].get("domain", "unknown") for r in records)
    subdomain = Counter(r["function_profile"].get("subdomain", "unknown") for r in records)
    function_type = Counter(r["function_profile"].get("function_type", "unknown") for r in records)

    write_counter_csv(args.out / "source_distribution.csv", "source_family", source_family)
    write_counter_csv(args.out / "domain_distribution.csv", "domain", domain)
    write_counter_csv(args.out / "subdomain_distribution.csv", "subdomain", subdomain)
    write_counter_csv(args.out / "function_type_distribution.csv", "function_type", function_type)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

