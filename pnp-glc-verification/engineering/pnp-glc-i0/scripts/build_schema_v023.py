from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json"
TARGET = ROOT / "schemas" / "run-record.schema.v0.2.3-candidate.json"


def replace_version(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("0.2.2", "0.2.3")
    if isinstance(value, list):
        return [replace_version(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_version(item) for key, item in value.items()}
    return value


def main() -> None:
    schema = replace_version(json.loads(SOURCE.read_text(encoding="utf-8")))
    schema["description"] = (
        "Candidate v0.2.3 transport schema: v0.2.2 structural, gate-matrix, "
        "provenance-derivation, role-binding, and canonical-domain interface; "
        "external semantic validation remains mandatory. CLOSURE-CLASS-01 is "
        "closed in the external validator because artifact bytes are outside "
        "the run-record transport schema."
    )
    TARGET.write_text(
        json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
