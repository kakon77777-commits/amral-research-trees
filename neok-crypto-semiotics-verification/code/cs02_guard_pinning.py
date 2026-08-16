"""How much of source item 38's Ω-wrapper is actually pinned by its own tests?

數學戰士「墜衡」 / AMRAL Research Lab.

The v0.8 report says "7/7 executable tests passed". That is a statement about the
tests, and it is worth exactly what the tests can detect. So each guard the
module implements is removed in turn and two questions are asked separately,
because they have very different answers:

  1. does any of THEIR tests go red?
  2. does the module's BEHAVIOUR change — does it now accept an input the
     undamaged module refuses?

A guard that fails (1) but not (2) is **redundant**: something underneath, here
the `cryptography` library, re-catches it. Defence in depth, not a hole.

A guard that fails both is an **unpinned guard**: real work that nothing checks,
so a later edit removes it silently and the suite stays green.

Reporting those two as one number would be wrong in both directions, so this
tool reports them apart. Nothing is written into the package; every mutation
happens on a copy under a temporary directory.

Usage:  python code/cs02_guard_pinning.py
Env:    CS_SOURCE_ZIP
"""

from __future__ import annotations

import base64
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

DEFAULT_ZIP = (pathlib.Path(r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新"
                            r"\Collatz_OT_Series_Paper")
               / "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip")
SRC_ZIP = pathlib.Path(os.environ.get("CS_SOURCE_ZIP", str(DEFAULT_ZIP)))
TOP = "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8"
V8 = "12_obligation_execution_v0.8"
SUB, MOD, TEST = "01_omega_wrapper", "omega_wrapper.py", "test_omega_wrapper.py"

GUARDS = [
    ("G1_visible_only_copy_keeps_the_hidden_state",
     '    return Carrier(carrier.profile, carrier.visible, "")',
     '    return Carrier(carrier.profile, carrier.visible, carrier.state)'),
    ("G2_recover_stops_checking_the_carrier_profile",
     '    if carrier.profile != PROFILE or carrier.visible != VISIBLE_GLYPH:\n'
     '        raise CarrierError("wrong carrier profile")',
     '    if False:\n        raise CarrierError("wrong carrier profile")'),
    ("G3_decode_packet_drops_the_canonicality_check",
     '    if encode_packet(obj) != state:\n        raise CarrierError("non-canonical state")',
     '    if False:\n        raise CarrierError("non-canonical state")'),
    ("G4_decode_packet_stops_pinning_the_packet_shape",
     '    if set(obj) != {"v", "nonce", "ct"} or obj["v"] != 1:\n'
     '        raise CarrierError("unsupported packet")',
     '    if False:\n        raise CarrierError("unsupported packet")'),
    ("G5_the_aad_is_not_bound_into_the_ciphertext",
     '    ct = AESGCM(key).encrypt(nonce, plaintext, aad)',
     '    ct = AESGCM(key).encrypt(nonce, plaintext, b"")'),
    # NOT `aad if aad else b""` — that is identical to `aad` for every input.
    # The first run of this probe used it and reported an unpinned guard where
    # nothing had been changed at all.
    ("G6_recover_ignores_the_aad_it_was_given",
     '    return AESGCM(key).decrypt(nonce, ct, aad)',
     '    return AESGCM(key).decrypt(nonce, ct, b"")'),
    ("G7_the_nonce_length_is_no_longer_enforced_on_recover",
     '    if len(nonce) != 12:\n        raise CarrierError("invalid nonce length")',
     '    if False:\n        raise CarrierError("invalid nonce length")'),
    ("G8_the_key_length_check_is_removed_from_encrypt",
     '    if len(key) != 32:\n        raise ValueError("AES-256 key must be 32 bytes")\n'
     '    nonce = nonce if nonce is not None else os_random_nonce()',
     '    if False:\n        raise ValueError("AES-256 key must be 32 bytes")\n'
     '    nonce = nonce if nonce is not None else os_random_nonce()'),
    ("G9_the_packet_carries_the_plaintext_beside_the_ciphertext",
     '    packet = {"v": 1, "nonce": _b64e(nonce), "ct": _b64e(ct)}',
     '    packet = {"v": 1, "nonce": _b64e(nonce), "ct": _b64e(ct + plaintext)}'),
]

_seq = [0]


def load(src: str):
    _seq[0] += 1
    name = f"_omega_probe_{_seq[0]}"
    d = pathlib.Path(tempfile.mkdtemp())
    f = d / f"{name}.py"
    f.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, f)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m               # frozen dataclasses need this
    spec.loader.exec_module(m)
    return m


def acceptances(m) -> list[str]:
    """Adversarial inputs the module ACCEPTS that the undamaged one refuses."""
    bad, key = [], b"K" * 32
    c = m.encrypt_then_project(key, b"secret", b"aad")
    pkt = json.loads(base64.urlsafe_b64decode(c.state + "=" * ((4 - len(c.state) % 4) % 4)))

    def carrier(raw: bytes):
        return m.Carrier(m.PROFILE, m.VISIBLE_GLYPH,
                         base64.urlsafe_b64encode(raw).decode().rstrip("="))

    try:
        m.recover(key, m.Carrier("other-profile", "X", c.state), b"aad")
        bad.append("accepts a carrier with a foreign profile and glyph")
    except Exception:
        pass
    try:
        m.recover(key, carrier(json.dumps({"ct": pkt["ct"], "nonce": pkt["nonce"],
                                           "v": 1}).encode()), b"aad")
        bad.append("accepts a non-canonical re-encoding of the same packet")
    except Exception:
        pass
    try:
        m.recover(key, carrier(json.dumps({**pkt, "extra": "x"}, sort_keys=True,
                                          separators=(",", ":")).encode()), b"aad")
        bad.append("accepts a packet carrying undeclared extra fields")
    except Exception:
        pass
    try:
        if m.recover(key, c, b"a-totally-different-aad") == b"secret":
            bad.append("recovers plaintext under the wrong aad")
    except Exception:
        pass
    try:
        m.encrypt_then_project(b"short", b"x")
        bad.append("encrypts with a key that is not 32 bytes")
    except Exception:
        pass
    # the legitimate path must still work, or the mutation broke the module
    # rather than loosening a guard
    try:
        if m.recover(key, c, b"aad") != b"secret":
            bad.append("BROKEN: cannot recover its own ciphertext")
    except Exception:
        bad.append("BROKEN: raises on its own ciphertext")
    return bad


def main() -> int:
    rep = {"tool": "cs02_guard_pinning.py",
           "subject": "the Ω-wrapper of source item 38 and its own pytest suite",
           "guards": {}, "counts": {}}

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="cs38_guard_"))
    try:
        with zipfile.ZipFile(SRC_ZIP) as z:
            z.extractall(tmp)
        base = tmp / TOP / V8
        src = (base / SUB / MOD).read_text(encoding="utf-8")

        def suite(root: pathlib.Path) -> int:
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", TEST],
                               cwd=str(root / SUB), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=900,
                               env={**os.environ, "PYTHONUTF8": "1",
                                    "PYTHONDONTWRITEBYTECODE": "1"})
            return p.returncode

        if suite(base) != 0:
            print(json.dumps({"error": "their suite is not green to begin with"}))
            return 2
        ref = acceptances(load(src))
        rep["reference_module_unexpected_acceptances"] = ref
        if ref:
            print(json.dumps({"error": "the undamaged module already accepts "
                                       "adversarial input; probe is unsound",
                              "acceptances": ref}, indent=2, ensure_ascii=False))
            return 3

        for name, old, new in GUARDS:
            if src.count(old) != 1:
                rep["guards"][name] = {"anchor_matches": src.count(old),
                                       "note": "anchor absent or ambiguous"}
                continue
            mutated = src.replace(old, new, 1)
            work = tmp / f"w_{name}"
            shutil.copytree(base, work, ignore=shutil.ignore_patterns(
                "__pycache__", ".pytest_cache", "*.pyc"))
            (work / SUB / MOD).write_text(mutated, encoding="utf-8")
            caught = suite(work) != 0
            shutil.rmtree(work, ignore_errors=True)
            behaves = acceptances(load(mutated))
            rep["guards"][name] = {
                "their_suite_catches_it": caught,
                "behaviour_change": behaves,
                "verdict": ("pinned" if caught else
                            "unpinned guard" if behaves else "redundant guard"),
            }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    v = [g.get("verdict") for g in rep["guards"].values()]
    rep["counts"] = {"guards_probed": len(rep["guards"]),
                     "pinned_by_their_suite": v.count("pinned"),
                     "unpinned_guards": v.count("unpinned guard"),
                     "redundant_guards": v.count("redundant guard")}
    rep["unpinned"] = sorted(k for k, g in rep["guards"].items()
                             if g.get("verdict") == "unpinned guard")
    # This tool REPORTS; it does not grade the package. `ok` means the probe ran
    # soundly — reference clean, every anchor found — not that nothing was found.
    rep["ok"] = (not rep["reference_module_unexpected_acceptances"]
                 and all("verdict" in g for g in rep["guards"].values()))
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
