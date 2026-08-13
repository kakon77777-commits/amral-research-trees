from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "run-record.schema.v0.2.4-candidate.json"
TARGET = ROOT / "schemas" / "run-record.schema.v0.2.5-candidate.json"


def replace_version(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("0.2.4", "0.2.5")
    if isinstance(value, list):
        return [replace_version(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_version(item) for key, item in value.items()}
    return value


def main() -> None:
    schema = replace_version(json.loads(SOURCE.read_text(encoding="utf-8")))
    schema["description"] = (
        "Candidate v0.2.5 transport schema: frozen v0.2.4 structural, "
        "gate-matrix, provenance-derivation, role-binding, canonical-domain, "
        "and family-bound oracle interface; external semantic validation "
        "remains mandatory. The free-text admissibility advice declaration is "
        "replaced by typed advice_mode with fail-closed internal consistency."
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

    admissibility = schema["$defs"]["mechanism"]["properties"]["admissibility"]
    admissibility["properties"].pop("advice", None)
    admissibility["properties"]["advice_mode"] = {
        "enum": ["none", "per-input-length-truth-table"]
    }
    admissibility["required"] = [
        "advice_mode" if name == "advice" else name
        for name in admissibility["required"]
    ]
    admissibility.setdefault("allOf", []).extend(
        [
            {
                "if": {
                    "properties": {"advice_mode": {"const": "none"}},
                    "required": ["advice_mode"],
                },
                "then": {
                    "properties": {
                        "uniform": {"const": True},
                        "program_quantifiers": {
                            "const": "exists-one-program-for-all-input-lengths"
                        },
                        "advice_generator_ref": {"type": "null"},
                        "declared_answer_access": {"const": "none"},
                    }
                },
            },
            {
                "if": {
                    "properties": {
                        "advice_mode": {
                            "const": "per-input-length-truth-table"
                        }
                    },
                    "required": ["advice_mode"],
                },
                "then": {
                    "properties": {
                        "uniform": {"const": False},
                        "program_quantifiers": {
                            "const": "for-all-lengths-exists-program"
                        },
                        "advice_generator_ref": {"$ref": "#/$defs/hash"},
                        "declared_answer_access": {"const": "truth-table"},
                    }
                },
            },
        ]
    )

    def advice_mode_condition(mode: str) -> dict[str, Any]:
        return {
            "properties": {
                "mechanism": {
                    "properties": {
                        "admissibility": {
                            "properties": {
                                "advice_mode": {"const": mode}
                            },
                            "required": ["advice_mode"],
                        }
                    },
                    "required": ["admissibility"],
                }
            },
            "required": ["mechanism"],
        }

    schema.setdefault("allOf", []).extend(
        [
            {
                "if": advice_mode_condition("none"),
                "then": {
                    "properties": {
                        "ledger": {
                            "properties": {
                                "description_bytes": {
                                    "properties": {
                                        "advice": {"const": 0},
                                        "generated_tables": {"const": 0},
                                    }
                                },
                                "admission_costs": {
                                    "properties": {
                                        "advice_generation": {
                                            "properties": {
                                                "time_ns": {"const": 0},
                                                "peak_space_bytes": {"const": 0},
                                                "peak_output_bytes": {"const": 0},
                                            }
                                        }
                                    }
                                },
                            }
                        },
                        "validation_receipt": {
                            "properties": {
                                "observed_answer_access": {"const": "none"}
                            }
                        },
                    }
                },
            },
            {
                "if": advice_mode_condition("per-input-length-truth-table"),
                "then": {
                    "properties": {
                        "ledger": {
                            "properties": {
                                "description_bytes": {
                                    "properties": {
                                        "advice": {"minimum": 1},
                                        "generated_tables": {"minimum": 1},
                                    }
                                },
                                "admission_costs": {
                                    "properties": {
                                        "advice_generation": {
                                            "properties": {
                                                "time_ns": {"minimum": 1},
                                                "peak_space_bytes": {"minimum": 1},
                                                "peak_output_bytes": {"minimum": 1},
                                            }
                                        }
                                    }
                                },
                            }
                        },
                        "validation_receipt": {
                            "properties": {
                                "observed_answer_access": {
                                    "const": "truth-table"
                                }
                            }
                        },
                    }
                },
            },
        ]
    )
    TARGET.write_text(
        json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
