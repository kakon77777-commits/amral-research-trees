#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, json
root = Path(__file__).resolve().parents[1]
main = root/'BSD_P5_uGPR_Minimal_Gate_389a1_p11_v0.6.md'
canon = root/'source'/'P5_v0.6_canonical_source.md'
a = main.read_bytes(); b = canon.read_bytes()
assert a == b, 'main and canonical source differ'
s = a.decode('utf-8')
assert '\\(' not in s and '\\)' not in s and '\\[' not in s and '\\]' not in s, 'noncanonical math delimiters found'
assert s.count('$$') % 2 == 0, 'unbalanced display math delimiter'
# Remove display blocks before checking inline dollar parity.
t = re.sub(r'\$\$.*?\$\$', '', s, flags=re.S)
# Ignore dollars inside fenced code for this lightweight source validator.
t = re.sub(r'```.*?```', '', t, flags=re.S)
assert t.count('$') % 2 == 0, 'unbalanced inline math delimiter'
# Source should use LaTeX commands rather than Unicode mathematical letter substitutions.
for ch in ['ℤ','ℚ','ℝ','ℂ','∞','∈','∉','⇒','⇔','≠','≤','≥']:
    assert ch not in s, f'Unicode math glyph found in canonical source: {ch}'
print('VALIDATION_V06_OK')
print('canonical_sha256', hashlib.sha256(b).hexdigest())
