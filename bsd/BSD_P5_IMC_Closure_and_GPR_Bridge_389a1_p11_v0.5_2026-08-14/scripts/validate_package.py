#!/usr/bin/env python3
from pathlib import Path
import json
import hashlib

root = Path(__file__).resolve().parents[1]
canonical = root / "source" / "P5_v0.5_canonical_source.md"
main = root / "BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5.md"
text = canonical.read_text(encoding="utf-8")
assert main.read_text(encoding="utf-8") == text, "main paper must be byte-identical to canonical source"
assert "\\[" not in text and "\\]" not in text and "\\(" not in text and "\\)" not in text
assert "\\u" not in text, "unicode_escape-style source fragment detected"
for glyph in ["∈", "∉", "⊂", "⊆", "⊕", "⊗", "≅", "≤", "≥", "⇒", "⇔", "ℚ", "ℤ"]:
    assert glyph not in text, f"unicode math glyph detected: {glyph}"
assert text.count("$$") % 2 == 0, "unbalanced display-math delimiters"
# Check inline-dollar parity after removing display delimiters line-by-line.
for i, line in enumerate(text.splitlines(), 1):
    stripped = line.replace("$$", "")
    if stripped.count("$") % 2:
        raise AssertionError(f"unbalanced inline $ on line {i}")
# Parse every JSON artifact.
for p in root.rglob("*.json"):
    json.loads(p.read_text(encoding="utf-8"))
# UTF-8 decode all text-like artifacts.
for p in root.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".md", ".py", ".sage", ".json", ".txt"}:
        p.read_text(encoding="utf-8")
print("VALIDATION_OK")
print("canonical_sha256", hashlib.sha256(canonical.read_bytes()).hexdigest())
