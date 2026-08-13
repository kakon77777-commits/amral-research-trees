"""Replay the 71-packet closure audit against the archived dataset."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import audit_public_4x6 as audit


TREE_ROOT = Path(__file__).resolve().parent.parent
DATASET = TREE_ROOT / "data" / "public-4x6-packets.v1.json"


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    packets = tuple(
        (tuple(item[0]), tuple(item[1])) for item in payload["packets"]
    )
    assert len(packets) == payload["packet_count"] == 71
    digest = hashlib.sha256(repr(packets).encode("utf-8")).hexdigest()
    assert digest == payload["repr_sha256"], (digest, payload["repr_sha256"])

    # Keep every mathematical check in the original auditor while replacing
    # only its mutable network input with the immutable archived snapshot.
    audit.fetch_packets = lambda: packets
    audit.main()


if __name__ == "__main__":
    main()
