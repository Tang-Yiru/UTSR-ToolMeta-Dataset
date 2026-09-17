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
    primary_action = Counter()
    supported_actions = Counter()
    action_mode = Counter()
    effect_class = Counter()
    cardinality = Counter()
    task_intents = set()

    for record in records:
        source_family[record["source_meta"].get("source_family", "unknown")] += 1
        profile = record["function_profile"]
        domain[profile.get("primary_domain", "unknown")] += 1
        subdomain[profile.get("primary_subdomain") or "__null__"] += 1
        primary_action[profile.get("primary_action") or "__null__"] += 1
        supported_actions.update(profile.get("supported_actions", ["unknown"]))
        action_mode[profile.get("action_mode", "unknown")] += 1
        effect_class[profile.get("effect_class", "unknown")] += 1
        cardinality[profile.get("cardinality", "unknown")] += 1
        intent = profile.get("task_intent")
        if intent:
            task_intents.add(json.dumps(intent, sort_keys=True, ensure_ascii=False))

    return {
        "records": len(records),
        "source_family": dict(source_family.most_common()),
        "domain_unique": len(domain),
        "subdomain_unique": len(subdomain),
        "task_intent_unique": len(task_intents),
        "top_domains": dict(domain.most_common(20)),
        "primary_domain_counts": dict(domain.most_common()),
        "primary_subdomain_counts": dict(subdomain.most_common()),
        "primary_action_counts": dict(primary_action.most_common()),
        "supported_action_counts": dict(supported_actions.most_common()),
        "action_mode_counts": dict(action_mode.most_common()),
        "effect_class_counts": dict(effect_class.most_common()),
        "cardinality_counts": dict(cardinality.most_common()),
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

    for field in ("source_family", "primary_domain", "primary_subdomain", "primary_action",
                  "supported_action", "action_mode", "effect_class", "cardinality"):
        values = summary[field if field == "source_family" else field + "_counts"]
        write_counter_csv(args.out / f"{field}_distribution.csv", field, Counter(values))

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
