from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Iterable


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_python_closure(
    root: Path, entrypoints: Iterable[str]
) -> tuple[list[str], list[dict[str, str]]]:
    package_root = root / "src" / "pnp_glc_i0"

    def module_paths(module: str, aliases: Iterable[str] = ()) -> set[str]:
        if module == "pnp_glc_i0":
            paths = {"src/pnp_glc_i0/__init__.py"}
            for alias in aliases:
                candidate = package_root / f"{alias}.py"
                if candidate.is_file():
                    paths.add(candidate.relative_to(root).as_posix())
            return paths
        if not module.startswith("pnp_glc_i0."):
            return set()
        relative = module.removeprefix("pnp_glc_i0.").replace(".", "/")
        candidate = package_root / f"{relative}.py"
        if not candidate.is_file():
            raise ValueError(f"unresolved local module {module}")
        return {
            "src/pnp_glc_i0/__init__.py",
            candidate.relative_to(root).as_posix(),
        }

    def local_imports(relative: str) -> set[str]:
        tree = ast.parse(
            (root / relative).read_text(encoding="utf-8"), filename=relative
        )
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
                    results.update(
                        module_paths(module, aliases if node.module is None else ())
                    )
                elif node.module:
                    results.update(module_paths(node.module, aliases))
        return results

    queue = list(entrypoints)
    seen: set[str] = set()
    edges: set[tuple[str, str]] = set()
    while queue:
        source = queue.pop(0)
        if source in seen:
            continue
        if not (root / source).is_file():
            raise FileNotFoundError(source)
        seen.add(source)
        for target in sorted(local_imports(source)):
            edges.add((source, target))
            if target not in seen:
                queue.append(target)
    return sorted(seen), [
        {"from": source, "to": target} for source, target in sorted(edges)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    descriptor_path = (
        root
        / "artifacts-v0.2.6"
        / "acceptance-runtime-closure.v0.2.6.json"
    )
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    required = descriptor["required_paths"]
    derived_sources, derived_edges = derive_python_closure(
        root, descriptor["python_entrypoints"]
    )
    checks = {
        "all-required-paths-present": all((root / path).is_file() for path in required),
        "required-paths-unique": len(required) == len(set(required)),
        "python-source-closure-exact": (
            derived_sources == descriptor["python_source_closure"]
        ),
        "local-import-edges-exact": (
            derived_edges == descriptor["local_import_edges"]
        ),
        "python-source-closure-required": set(derived_sources).issubset(required),
        "resolved-content-evidence-required": set(
            descriptor["resolved_content_evidence_paths"]
        ).issubset(required),
        "official-commands-use-isolated-no-bytecode": all(
            command["args"][:2] == ["-I", "-B"]
            for command in descriptor["official_acceptance_commands"]
        ),
        "external-distribution-versions-match": all(
            importlib.metadata.version(name) == version
            for name, version in descriptor["external_python_distributions"].items()
        ),
    }
    sys.path.insert(0, str(root / "src"))
    from pnp_glc_i0 import semantic_validator_v026 as validator

    evidence = descriptor["operational_evidence_files"]
    checks.update(
        {
            "schema-pin-matches": (
                sha256(root / "schemas/run-record.schema.v0.2.6-candidate.json")
                == validator.PINNED_SCHEMA_HASH
            ),
            "closure-spec-pin-matches": (
                sha256(root / "artifacts-v0.2.6/artifact-closure-spec.v0.2.6.json")
                == validator.PINNED_CLOSURE_SPEC_HASH
            ),
            "oracle-pin-matches": (
                sha256(root / evidence["oracle"]) == validator.PINNED_ORACLE_HASH
            ),
            "parity-transition-pin-matches": (
                sha256(root / evidence["parity-transition"])
                == validator.PINNED_PARITY_RULE_HASH
            ),
            "two-sat-transition-pin-matches": (
                sha256(root / evidence["two-sat-transition"])
                == validator.PINNED_TWO_SAT_RULE_HASH
            ),
            "generator-does-not-import-legacy-generator": (
                "generate_fixtures_v021"
                not in (root / "scripts/generate_fixtures_v026.py").read_text(
                    encoding="utf-8"
                )
            ),
        }
    )
    unexpected = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "all_conformant": not unexpected,
                "checks": checks,
                "classification": "Acceptance runtime/evidence closure check",
                "derived_local_import_edge_count": len(derived_edges),
                "derived_python_source_count": len(derived_sources),
                "official_command_count": len(
                    descriptor["official_acceptance_commands"]
                ),
                "required_path_count": len(required),
                "unexpected": unexpected,
                "version": descriptor["version"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
