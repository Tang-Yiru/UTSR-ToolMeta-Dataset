#!/usr/bin/env python3
"""Build a simple semantically competitive tool pool.

This example uses functional-profile fields for coarse filtering and a
lightweight lexical score for ranking. It is intentionally dependency-free.
For experiments, replace the scoring function with an embedding model or a
stronger semantic reranker.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str | None) -> set[str]:
    if not text:
        return set()
    return {t.lower() for t in TOKEN_RE.findall(text)}


def record_text(record: dict[str, Any]) -> str:
    utsr = record["utsr"]
    params = utsr["interface"].get("parameters") or []
    param_text = " ".join(
        " ".join(str(p.get(k) or "") for k in ("name", "type", "description"))
        for p in params
    )
    return " ".join(
        [
            str(utsr["identity"].get("name") or ""),
            str(utsr["capability"].get("summary") or ""),
            str(utsr["capability"].get("description") or ""),
            param_text,
        ]
    )


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_records(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--record-id", required=True)
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args()

    records = load_records(args.path)
    by_id = {r["record_id"]: r for r in records}
    target = by_id[args.record_id]
    target_profile = target["function_profile"]
    target_tokens = tokenize(record_text(target))

    candidates = []
    for record in records:
        if record["record_id"] == target["record_id"]:
            continue
        profile = record["function_profile"]
        coarse_score = 0
        if profile.get("domain") == target_profile.get("domain"):
            coarse_score += 3
        if profile.get("subdomain") == target_profile.get("subdomain"):
            coarse_score += 3
        if profile.get("function_type") == target_profile.get("function_type"):
            coarse_score += 2
        lexical_score = jaccard(target_tokens, tokenize(record_text(record)))
        score = coarse_score + lexical_score
        if coarse_score > 0:
            candidates.append((score, lexical_score, record))

    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)

    result = {
        "target": {
            "record_id": target["record_id"],
            "name": target["utsr"]["identity"].get("name"),
            "profile": target_profile,
        },
        "competitors": [
            {
                "record_id": r["record_id"],
                "name": r["utsr"]["identity"].get("name"),
                "source_family": r["source_meta"].get("source_family"),
                "profile": r["function_profile"],
                "score": round(score, 4),
            }
            for score, _, r in candidates[: args.top_k]
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

