#!/usr/bin/env python3
from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/'source'/'P5_v0.8_canonical_source.md'
s=p.read_text(encoding='utf-8')
for bad in ['\\[','\\]','\\(','\\)']:
    assert bad not in s, f'forbidden delimiter {bad}'
assert not re.search(r'\\u[0-9a-fA-F]{4}', s), 'unicode_escape marker found'
assert not re.search(r'\\x[0-9a-fA-F]{2}', s), 'hex escape marker found'
assert s.count('$$') % 2 == 0
# reject control chars other than newline/tab/carriage return
assert not any(ord(ch)<32 and ch not in '\n\r\t' for ch in s)
print('VALIDATION_V08_OK')
