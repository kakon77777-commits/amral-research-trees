from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_bytes(path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    }


def parse_manifest(root: Path, path: Path) -> tuple[list[str], list[str]]:
    paths: list[str] = []
    issues: list[str] = []
    seen: set[str] = set()
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            issues.append(f"line-{index}-format")
            continue
        if len(expected) != 64 or any(char not in "0123456789abcdefABCDEF" for char in expected):
            issues.append(f"line-{index}-hash")
            continue
        pure = Path(relative)
        if pure.is_absolute() or ".." in pure.parts or relative in seen:
            issues.append(f"line-{index}-path")
            continue
        seen.add(relative)
        source = root / relative
        if not source.is_file():
            issues.append(f"line-{index}-missing")
            continue
        if source.is_symlink() or source.resolve().is_relative_to(root.resolve()) is False:
            issues.append(f"line-{index}-reparse")
            continue
        if sha256_bytes(source.read_bytes()) != expected.upper():
            issues.append(f"line-{index}-mismatch")
            continue
        paths.append(relative)
    return paths, issues


def render_report(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest_paths, manifest_issues = parse_manifest(root, manifest_path)
    descriptor = json.loads(
        (
            root
            / "artifacts-v0.2.6"
            / "acceptance-runtime-closure.v0.2.6.json"
        ).read_text(encoding="utf-8")
    )
    required_missing = sorted(set(descriptor["required_paths"]) - set(manifest_paths))
    path_set_hash = sha256_bytes(
        ("\n".join(sorted(manifest_paths)) + "\n").encode("utf-8")
    )
    with tempfile.TemporaryDirectory(prefix="pnp-glc-v026-isolated-") as directory:
        isolated = Path(directory) / "candidate"
        isolated.mkdir()
        for relative in manifest_paths:
            destination = isolated / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / relative, destination)
        before = snapshot(isolated)

        environment = dict(os.environ)
        for name in (
            "PYTHONHOME",
            "PYTHONPATH",
            "PYTHONSTARTUP",
            "PYTHONUSERBASE",
        ):
            environment.pop(name, None)
        environment.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1",
                "PYTHONUTF8": "1",
            }
        )
        guard_code = (
            "import json,os,sys;print(json.dumps({"
            "'isolated':sys.flags.isolated==1,"
            "'dont_write_bytecode':sys.dont_write_bytecode,"
            "'sitecustomize_absent':'sitecustomize' not in sys.modules,"
            "'usercustomize_absent':'usercustomize' not in sys.modules,"
            "'pythonpath_absent':'PYTHONPATH' not in os.environ},sort_keys=True))"
        )
        guard = subprocess.run(
            [sys.executable, "-I", "-B", "-c", guard_code],
            cwd=isolated,
            env=environment,
            capture_output=True,
            timeout=60,
        )
        guard_payload = json.loads(guard.stdout.decode("utf-8"))

        commands: list[dict[str, Any]] = []
        original_root_bytes = str(root).encode("utf-8")
        for command in descriptor["official_acceptance_commands"]:
            argv = [sys.executable, *command["args"]]
            completed = subprocess.run(
                argv,
                cwd=isolated,
                env=environment,
                capture_output=True,
                timeout=120,
            )
            leaked_root = (
                original_root_bytes in completed.stdout
                or original_root_bytes in completed.stderr
            )
            commands.append(
                {
                    "args": ["python", *command["args"]],
                    "exit_code": completed.returncode,
                    "name": command["name"],
                    "original_root_reference": leaked_root,
                    "passed": completed.returncode == 0 and not leaked_root,
                    "stderr_sha256": sha256_bytes(completed.stderr),
                    "stdout_sha256": sha256_bytes(completed.stdout),
                }
            )
        after = snapshot(isolated)
        extra = sorted(set(after) - set(before))
        missing = sorted(set(before) - set(after))
        changed = sorted(
            path for path in set(before) & set(after) if before[path] != after[path]
        )

    guard_pass = guard.returncode == 0 and all(guard_payload.values())
    all_pass = (
        not manifest_issues
        and not required_missing
        and guard_pass
        and all(item["passed"] for item in commands)
        and not extra
        and not missing
        and not changed
    )
    return {
        "all_pass": all_pass,
        "candidate_root_source_dependency": False,
        "classification": "Manifest-only isolated acceptance replay",
        "commands": commands,
        "guard": guard_payload,
        "guard_pass": guard_pass,
        "manifest_entry_count": len(manifest_paths),
        "manifest_issues": manifest_issues,
        "manifest_path_set_sha256": path_set_hash,
        "required_paths_missing_from_manifest": required_missing,
        "snapshot_changed_files": changed,
        "snapshot_extra_files": extra,
        "snapshot_missing_files": missing,
        "snapshot_policy": (
            "fresh temporary directory; copy exactly top-level manifest paths; "
            "sanitized environment; python -I -B; no original root references"
        ),
        "version": "0.2.6",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    manifest = args.manifest or root / "SHA256SUMS-v0.2.6-candidate.txt"
    report = render_report(root, manifest)
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
