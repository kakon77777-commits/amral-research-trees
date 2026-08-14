#!/usr/bin/env python3
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
g = json.loads((root/'results'/'p5_gate_status_v0.6.json').read_text(encoding='utf-8'))
assert g['inherited']['P5_IMC11']['status'] == 'CLOSED'
assert g['new']['P5_BOC_NZ11']['status'].startswith('CLOSED')
assert g['new']['P5_uGPR11']['status'] == 'OPEN_MINIMAL_CONCEPTUAL_GATE'
assert g['new']['P5_LAT11']['equivalent_to'] == ['P5_uGPR11']
assert set(g['new']['P5_LAT11']['decomposition']) == {'P5_INT11','P5_PRIM11'}
print('GATE_LOGIC_V06_OK')
