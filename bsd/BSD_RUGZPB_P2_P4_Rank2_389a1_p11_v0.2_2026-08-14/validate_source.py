#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parent
errors=[]
text_ext={'.md','.py','.sage','.txt','.json'}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='SHA256SUMS.json' or p.suffix.lower() not in text_ext:
        continue
    try:
        s=p.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f'{p.relative_to(ROOT)}: UTF-8 read failed: {e}')
        continue
    if '\x00' in s:
        errors.append(f'{p.relative_to(ROOT)}: NUL byte')
    if p.suffix.lower()=='.md':
        for bad in (r'\\\(', r'\\\)', r'\\\[', r'\\\]'):
            if re.search(bad,s):
                errors.append(f'{p.relative_to(ROOT)}: alternate LaTeX delimiter found: {bad}')
    if p.suffix.lower()=='.json':
        try: json.loads(s)
        except Exception as e: errors.append(f'{p.relative_to(ROOT)}: invalid JSON: {e}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('VALIDATION_OK')
