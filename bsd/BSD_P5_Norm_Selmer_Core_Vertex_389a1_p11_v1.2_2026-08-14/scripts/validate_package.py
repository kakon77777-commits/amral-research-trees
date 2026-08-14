#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path
base=Path(__file__).resolve().parents[1]
main=base/'BSD_P5_Norm_Selmer_Core_Vertex_389a1_p11_v1.2.md'
canon=base/'source/P5_v1.2_canonical_source.md'
assert main.read_bytes()==canon.read_bytes()
text=canon.read_text(encoding='utf-8')
assert '\\(' not in text and '\\)' not in text and '\\[' not in text and '\\]' not in text
assert text.count('$$')%2==0
for i,ch in enumerate(text):
    if ord(ch)<32 and ch not in '\n\t':
        raise AssertionError((i,ord(ch)))
subprocess.run([sys.executable,str(base/'scripts/replay_norm_selmer_cube.py')],check=True)
cert=json.loads((base/'results/norm_selmer_core_vertex_certificate.json').read_text(encoding='utf-8'))
assert cert['selmer_dimension']==2
assert cert['norm_selmer']['397']['dimension']==1
assert cert['norm_selmer']['991']['dimension']==1
assert cert['norm_selmer']['397_991']['dimension']==0
assert cert['transversality']['wedge_coefficient_mod11']==2
print('VALIDATION_V12_OK')
print('canonical_sha256',hashlib.sha256(canon.read_bytes()).hexdigest())
