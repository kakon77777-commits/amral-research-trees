#!/usr/bin/env python3
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parents[1]
main = base / "BSD_P5_Anomalous_Norm_Localization_389a1_p11_v1.1.md"
canon = base / "source" / "P5_v1.1_canonical_source.md"
assert main.read_bytes() == canon.read_bytes(), "canonical source differs from main"
text = canon.read_text(encoding="utf-8")
assert "\\(" not in text and "\\)" not in text and "\\[" not in text and "\\]" not in text
assert text.count("$$") % 2 == 0
# Reject C0 controls except LF/TAB.
for i, ch in enumerate(text):
    if ord(ch) < 32 and ch not in "\n\t":
        raise AssertionError(f"control character U+{ord(ch):04X} at {i}")
subprocess.run([sys.executable, str(base / "scripts" / "replay_anomalous_norm_localization.py")], check=True)
cert = json.loads((base / "results" / "anomalous_norm_localization_certificate.json").read_text(encoding="utf-8"))
assert cert["localization_det_mod11"] == 2
assert cert["mw_mod11_to_two_norm_quotients"] == "ISOMORPHISM"
assert cert["full_reduction"]["surjective"] is True
assert cert["full_reduction"]["cokernel_order_J_S"] == 1
print("VALIDATION_V11_OK")
print("canonical_sha256", hashlib.sha256(canon.read_bytes()).hexdigest())
