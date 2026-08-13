from __future__ import annotations

import ast
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts-v0.2.6" / "acceptance-runtime-closure.v0.2.6.json"
PACKAGE_ROOT = ROOT / "src" / "pnp_glc_i0"

OFFICIAL_COMMANDS = [
    {
        "name": "runtime-closure-self-check",
        "args": ["-I", "-B", "scripts/verify_runtime_closure_v026.py", "."],
    },
    {
        "name": "closure-reproducer",
        "args": ["-I", "-B", "scripts/reproduce_closure_class_v026.py", "."],
    },
    {
        "name": "advice-reproducer",
        "args": ["-I", "-B", "scripts/reproduce_advice_decl_ledger_v026.py", "."],
    },
    {
        "name": "oracle-reproducer",
        "args": ["-I", "-B", "scripts/reproduce_oracle_decl_family_v026.py", "."],
    },
    {
        "name": "live-report-scope-reproducer",
        "args": ["-I", "-B", "scripts/reproduce_live_report_scope_v026.py", "."],
    },
    {
        "name": "minimal-cli-legit",
        "args": ["-I", "-B", "scripts/validate_fixture_v026.py", ".", "legit"],
    },
]

PYTHON_ENTRYPOINTS = [
    "scripts/build_artifacts_v026.py",
    "scripts/build_isolation_report_v026.py",
    "scripts/build_runtime_closure_spec_v026.py",
    "scripts/build_schema_v026.py",
    "scripts/generate_fixtures_v026.py",
    "scripts/make_checksums_v026.py",
    "scripts/reproduce_advice_decl_ledger_v026.py",
    "scripts/reproduce_closure_class_v026.py",
    "scripts/reproduce_live_report_scope_v026.py",
    "scripts/reproduce_oracle_decl_family_v026.py",
    "scripts/run_experiment_v026.py",
    "scripts/validate_fixture_v026.py",
    "scripts/verify_runtime_closure_v026.py",
    "tests_v026/test_semantic_validator_v026.py",
]

PARENT_BUILD_INPUTS = [
    "SHA256SUMS-v0.2.5-candidate.txt",
    "schemas/run-record.schema.v0.2.5-candidate.json",
    *[
        f"artifacts-v0.2.5/{name}"
        for name in (
            "artifact-closure-spec.v0.2.5.json",
            "candidate-projection-spec.v0.2.5.json",
            "capability-sandbox.v0.2.5.json",
            "contract-2sat.v0.2.5.json",
            "contract-parity.v0.2.5.json",
            "evidence-role-spec.v0.2.5.json",
            "fairness.v0.2.5.json",
            "maximal-run.v0.2.5.json",
            "negative-malformed-role-edge.json",
            "negative-missing-envelope-spec-id.json",
            "parity-invariant.v0.2.5.json",
            "run-robust.v0.2.5.json",
            "run-standard.v0.2.5.json",
            "trace-public-key.v0.2.5.json",
        )
    ],
    *[
        f"fixtures-v0.2.5/{name}.json"
        for name in (
            "legit",
            "cheat",
            "robust-legit",
            "neutral-legit",
            "robust-neutral-legit",
            "2sat-sat",
            "2sat-unsat",
        )
    ],
    *[
        f"artifacts-v0.2.5/traces/{name}.trace.json"
        for name in (
            "legit",
            "cheat",
            "robust-legit",
            "neutral-legit",
            "robust-neutral-legit",
            "2sat-sat",
            "2sat-unsat",
        )
    ],
]


def module_paths(module: str, aliases: Iterable[str] = ()) -> set[str]:
    if module == "pnp_glc_i0":
        paths = {"src/pnp_glc_i0/__init__.py"}
        for alias in aliases:
            candidate = PACKAGE_ROOT / f"{alias}.py"
            if candidate.is_file():
                paths.add(candidate.relative_to(ROOT).as_posix())
        return paths
    if not module.startswith("pnp_glc_i0."):
        return set()
    relative = module.removeprefix("pnp_glc_i0.").replace(".", "/")
    candidate = PACKAGE_ROOT / f"{relative}.py"
    if not candidate.is_file():
        raise ValueError(f"unresolved local module {module}")
    return {
        "src/pnp_glc_i0/__init__.py",
        candidate.relative_to(ROOT).as_posix(),
    }


def local_imports(relative: str) -> set[str]:
    path = ROOT / relative
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
    results: set[str] = set()
    package_module = None
    if relative.startswith("src/pnp_glc_i0/"):
        package_module = "pnp_glc_i0." + Path(relative).stem
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                results.update(module_paths(alias.name))
        elif isinstance(node, ast.ImportFrom):
            aliases = [alias.name for alias in node.names]
            if node.level and package_module:
                package_parts = package_module.split(".")[:-node.level]
                module_parts = node.module.split(".") if node.module else []
                module = ".".join(package_parts + module_parts)
                if node.module is None:
                    results.update(module_paths(module, aliases))
                else:
                    results.update(module_paths(module))
            elif node.module:
                results.update(module_paths(node.module, aliases))
    return results


def derive_python_closure(entrypoints: Iterable[str]) -> tuple[list[str], list[dict[str, str]]]:
    queue = list(entrypoints)
    seen: set[str] = set()
    edges: set[tuple[str, str]] = set()
    while queue:
        source = queue.pop(0)
        if source in seen:
            continue
        path = ROOT / source
        if not path.is_file():
            raise FileNotFoundError(source)
        seen.add(source)
        for target in sorted(local_imports(source)):
            edges.add((source, target))
            if target not in seen:
                queue.append(target)
    return sorted(seen), [
        {"from": source, "to": target} for source, target in sorted(edges)
    ]


def derive_content_evidence_paths() -> tuple[list[str], list[str]]:
    sys.path.insert(0, str(ROOT / "src"))
    from pnp_glc_i0 import semantic_validator_v026 as validator

    store = validator.ArtifactIndex(ROOT)
    references: set[str] = set()

    def collect(direct: dict[str, str]) -> None:
        closure = validator._artifact_closure(direct, store)
        references.update(closure.references)

    for path in sorted((ROOT / "fixtures-v0.2.6").glob("*.json")):
        if path.name == "manifest.json":
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(record, dict) and isinstance(
                record.get("validation_receipt"), dict
            ):
                collect(validator._direct_receipt_reference_map(record))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            # Raw-domain and intentionally malformed negatives are allowed to
            # stop before they expose a complete direct reference map.
            continue

    classification_root = ROOT / "artifacts-v0.2.6" / "closure-classification"
    for path in sorted(classification_root.glob("*.json")):
        if path.name != "manifest.json":
            collect({"run-spec": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()})
    run_standard = ROOT / "artifacts-v0.2.6" / "run-standard.v0.2.6.json"
    collect({"run-spec": "sha256:" + hashlib.sha256(run_standard.read_bytes()).hexdigest()})

    resolved: set[str] = set()
    unresolved: list[str] = []
    for reference in sorted(references):
        snapshots = store.resolve(reference)
        candidates = [
            path.relative_to(ROOT).as_posix()
            for path, _ in snapshots
            if path.is_relative_to(ROOT)
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        ]
        if not candidates:
            unresolved.append(reference)
            continue

        def rank(relative: str) -> tuple[int, int, str]:
            if relative.startswith("src/pnp_glc_i0/"):
                priority = 0
            elif relative.startswith("schemas/"):
                priority = 1
            elif "v0.2.6" in relative:
                priority = 2
            elif relative.startswith("artifacts/"):
                priority = 3
            else:
                priority = 4
            return priority, len(relative), relative

        resolved.add(min(candidates, key=rank))
    return sorted(resolved), unresolved


def main() -> None:
    python_closure, import_edges = derive_python_closure(PYTHON_ENTRYPOINTS)
    evidence_paths, unresolved_negative_hashes = derive_content_evidence_paths()
    artifacts = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "artifacts-v0.2.6").rglob("*")
        if path.is_file() and path != OUTPUT
    )
    fixtures = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "fixtures-v0.2.6").rglob("*")
        if path.is_file()
    )
    required_paths = sorted(
        set(
            python_closure
            + PARENT_BUILD_INPUTS
            + evidence_paths
            + artifacts
            + fixtures
            + [
                OUTPUT.relative_to(ROOT).as_posix(),
                "i0-run-report.v0.2.6-candidate.json",
                "requirements-v0.2.6-candidate.txt",
                "schemas/run-record.schema.v0.2.6-candidate.json",
            ]
        )
    )
    payload = {
        "artifact_envelope": {
            "artifact_type": "acceptance-runtime-closure",
            "edges": [],
            "spec_id": "urn:evemisslab:pnp-glc:acceptance-runtime-closure:0.2.6",
            "version": "0.2.6",
        },
        "build_inputs": PARENT_BUILD_INPUTS,
        "external_capabilities": [
            {
                "capability": "non-production Ed25519 fixture signing key",
                "manifest_status": "excluded secret input",
                "scope": "fixture regeneration only; not used by acceptance commands",
            }
        ],
        "external_python_distributions": {
            "cryptography": importlib.metadata.version("cryptography"),
            "jsonschema": importlib.metadata.version("jsonschema"),
        },
        "forbidden_environment_dependencies": [
            "PYTHONHOME",
            "PYTHONPATH",
            "PYTHONSTARTUP",
            "PYTHONUSERBASE",
            "sitecustomize",
            "usercustomize",
        ],
        "local_import_edges": import_edges,
        "official_acceptance_commands": OFFICIAL_COMMANDS,
        "operational_evidence_files": {
            "oracle": "src/pnp_glc_i0/oracles.py",
            "parity-transition": "src/pnp_glc_i0/parity.py",
            "two-sat-transition": "src/pnp_glc_i0/two_sat.py",
        },
        "resolved_content_evidence_paths": evidence_paths,
        "unresolved_negative_evidence_hashes": unresolved_negative_hashes,
        "policy": (
            "Each official command must run with python -I -B in a fresh snapshot "
            "containing only top-level SHA256 manifest paths. Local Python imports "
            "are derived from AST and must equal python_source_closure."
        ),
        "python_entrypoints": PYTHON_ENTRYPOINTS,
        "python_source_closure": python_closure,
        "required_paths": required_paths,
        "status": "Definition / executable acceptance interface candidate",
        "version": "0.2.6",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
