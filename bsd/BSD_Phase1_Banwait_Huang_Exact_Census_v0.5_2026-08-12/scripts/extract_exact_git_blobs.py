#!/usr/bin/env python3
"""Materialize selected Git blobs byte-for-byte, bypassing core.autocrlf."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


OLD = "1a0489c3c3099dd0c248624e6621df73ae8f0d43"
NEW = "31fae20c8df3f1f0383f41112b914d4995d5809d"
GENERATOR = "72867942accf94b9513857a2c0bae3895af8e9bc"
PREFIX = "ants_xvii/infinite_bsd"

TARGETS = [
    (OLD, f"{PREFIX}/output/ec_labels_500k.txt", "inputs/old/ec_labels_500k.txt"),
    (
        OLD,
        f"{PREFIX}/output/twists_of_ec_labels_500k.json",
        "inputs/old/twists_of_ec_labels_500k.json",
    ),
    (NEW, f"{PREFIX}/output/ec_labels_500k.txt", "inputs/new/ec_labels_500k.txt"),
    (
        NEW,
        f"{PREFIX}/output/twists_of_ec_labels_500k.json",
        "inputs/new/twists_of_ec_labels_500k.json",
    ),
    (OLD, f"{PREFIX}/Algorithm1.py", "sources/old/Algorithm1.py"),
    (OLD, f"{PREFIX}/Algorithm2.py", "sources/old/Algorithm2.py"),
    (NEW, f"{PREFIX}/Algorithm1.py", "sources/new/Algorithm1.py"),
    (NEW, f"{PREFIX}/Algorithm2.py", "sources/new/Algorithm2.py"),
    (GENERATOR, f"{PREFIX}/Algorithm1.py", "sources/generator_7286794/Algorithm1.py"),
    (GENERATOR, f"{PREFIX}/Algorithm2.py", "sources/generator_7286794/Algorithm2.py"),
    (
        GENERATOR,
        f"{PREFIX}/output/ec_labels_500k.txt",
        "sources/generator_7286794/ec_labels_500k.txt",
    ),
]


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    root = args.root.resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"not a Git checkout: {repo}")

    records = []
    for commit, source, relative_destination in TARGETS:
        object_id = git(repo, "rev-parse", f"{commit}:{source}").decode("ascii").strip()
        content = git(repo, "cat-file", "blob", object_id)
        destination = root / relative_destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        records.append(
            {
                "commit": commit,
                "source": source,
                "destination": relative_destination,
                "git_blob_sha1": object_id,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )

    print(json.dumps({"materialized": records}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
