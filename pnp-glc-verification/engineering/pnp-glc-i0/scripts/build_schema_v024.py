from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "run-record.schema.v0.2.3-candidate.json"
TARGET = ROOT / "schemas" / "run-record.schema.v0.2.4-candidate.json"


def replace_version(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("0.2.3", "0.2.4")
    if isinstance(value, list):
        return [replace_version(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_version(item) for key, item in value.items()}
    return value


def main() -> None:
    schema = replace_version(json.loads(SOURCE.read_text(encoding="utf-8")))
    schema["description"] = (
        "Candidate v0.2.4 transport schema: v0.2.3 structural, gate-matrix, "
        "provenance-derivation, role-binding, and canonical-domain interface; "
        "external semantic validation remains mandatory. CLOSURE-EDGE-SCOPE-01 "
        "is closed in the versioned external closure specification because "
        "artifact bytes are outside the run-record transport schema."
    )
    oracle = schema["$defs"]["mechanism"]["properties"]["oracle"]
    oracle["properties"]["oracle_id"] = {
        "type": "string",
        "minLength": 1,
        "pattern": "^[a-z0-9][a-z0-9-]*$",
    }
    oracle["properties"]["entrypoint"] = {
        "type": "string",
        "minLength": 1,
        "pattern": "^[A-Za-z_][A-Za-z0-9_.]*:[A-Za-z_][A-Za-z0-9_]*$",
    }
    oracle["properties"]["obligations"] = {
        "type": "array",
        "minItems": 1,
        "uniqueItems": True,
        "items": {
            "enum": [
                "answer",
                "prefix-invariant",
                "assignment",
                "mutual-implication-paths",
            ]
        },
    }
    for name in ("oracle_id", "entrypoint", "obligations"):
        if name not in oracle["required"]:
            oracle["required"].append(name)
    TARGET.write_text(
        json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
