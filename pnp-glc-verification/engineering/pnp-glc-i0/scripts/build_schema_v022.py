from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "run-record.schema.v0.2.1-candidate.json"
TARGET = ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json"


def replace_version(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("0.2.1", "0.2.2")
    if isinstance(value, list):
        return [replace_version(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_version(item) for key, item in value.items()}
    return value


def main() -> None:
    schema = replace_version(json.loads(SOURCE.read_text(encoding="utf-8")))
    schema["description"] = (
        "Candidate v0.2.2 transport schema: v0.2.1 provenance derivation plus "
        "role-safe evidence binding and Unicode-scalar fail-closed semantics; "
        "external semantic validation remains mandatory."
    )
    defs = schema["$defs"]
    defs["applicableGateStatus"] = {"enum": ["pass", "fail", "unknown"]}
    receipt = defs["validationReceipt"]
    for name in ("evidence_role_spec_ref", "operational_reference_map_sha256"):
        if name not in receipt["required"]:
            receipt["required"].append(name)
    receipt["properties"]["evidence_role_spec_ref"] = {"$ref": "#/$defs/hash"}
    receipt["properties"]["operational_reference_map_sha256"] = {
        "$ref": "#/$defs/hash"
    }

    universally_applicable = {
        "uniformity_pass",
        "provenance_pass",
        "refs_resolved_pass",
        "builder_execution_pass",
        "advice_budget_pass",
        "answer_access_pass",
        "resource_account_pass",
        "oracle_free_pass",
        "replay_pass",
        "run_class_nonempty",
        "trace_authenticity_pass",
        "transition_execution_pass",
        "resource_derivation_pass",
    }
    gate_properties = receipt["properties"]["gates"]["properties"]
    for gate in universally_applicable:
        gate_properties[gate] = {"$ref": "#/$defs/applicableGateStatus"}

    advice_applicable = {
        "anyOf": [
            {
                "properties": {
                    "mechanism": {
                        "properties": {
                            "admissibility": {
                                "properties": {
                                    "advice_generator_ref": {"$ref": "#/$defs/hash"}
                                },
                                "required": ["advice_generator_ref"],
                            }
                        },
                        "required": ["admissibility"],
                    }
                },
                "required": ["mechanism"],
            },
            {
                "properties": {
                    "ledger": {
                        "properties": {
                            "description_bytes": {
                                "anyOf": [
                                    {"properties": {"advice": {"minimum": 1}}},
                                    {
                                        "properties": {
                                            "generated_tables": {"minimum": 1}
                                        }
                                    },
                                ]
                            }
                        },
                        "required": ["description_bytes"],
                    }
                },
                "required": ["ledger"],
            },
        ]
    }
    proof_applicable = {
        "anyOf": [
            {
                "properties": {
                    "mechanism": {
                        "properties": {
                            "admissibility": {
                                "properties": {
                                    "local_invariant_ref": {"$ref": "#/$defs/hash"}
                                },
                                "required": ["local_invariant_ref"],
                            }
                        },
                        "required": ["admissibility"],
                    }
                },
                "required": ["mechanism"],
            },
            {
                "properties": {
                    "ledger": {
                        "properties": {
                            "description_bytes": {
                                "properties": {"proof": {"minimum": 1}},
                                "required": ["proof"],
                            }
                        },
                        "required": ["description_bytes"],
                    }
                },
                "required": ["ledger"],
            },
        ]
    }
    schema["allOf"].extend(
        [
            {
                "if": advice_applicable,
                "then": {
                    "properties": {
                        "validation_receipt": {
                            "properties": {
                                "gates": {
                                    "properties": {
                                        "advice_generation_pass": {
                                            "$ref": "#/$defs/applicableGateStatus"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "else": {
                    "properties": {
                        "validation_receipt": {
                            "properties": {
                                "gates": {
                                    "properties": {
                                        "advice_generation_pass": {
                                            "const": "not-applicable"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            },
            {
                "if": proof_applicable,
                "then": {
                    "properties": {
                        "validation_receipt": {
                            "properties": {
                                "gates": {
                                    "properties": {
                                        "proof_verification_pass": {
                                            "$ref": "#/$defs/applicableGateStatus"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "else": {
                    "properties": {
                        "validation_receipt": {
                            "properties": {
                                "gates": {
                                    "properties": {
                                        "proof_verification_pass": {
                                            "const": "not-applicable"
                                        }
                                    }
                                }
                            }
                        }
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
