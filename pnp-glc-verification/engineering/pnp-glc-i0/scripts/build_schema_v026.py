from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "schemas" / "run-record.schema.v0.2.5-candidate.json"
OUTPUT = ROOT / "schemas" / "run-record.schema.v0.2.6-candidate.json"


def version_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: version_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [version_value(item) for item in value]
    if isinstance(value, str):
        return value.replace("0.2.5", "0.2.6")
    return value


def main() -> None:
    schema = version_value(json.loads(PARENT.read_text(encoding="utf-8")))
    schema["description"] = (
        "v0.2.6 candidate transport schema. It preserves v0.2.5 typed advice "
        "constraints; cross-field evidence truth remains the external validator's job."
    )
    OUTPUT.write_text(
        json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
