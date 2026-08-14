#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "results" / "p5_gate_status_v0.5.json").read_text(encoding="utf-8"))
g = data["gates"]
closed = {"CLOSED", "CLOSED_IMPORTED", "CLOSED_EXTERNAL_THEOREM", "CLOSED_UP_TO_Z11_UNIT"}
for key in ["P4_SHA11", "P5_GOOD_ORD11", "P5_RESIDUAL_IRR11", "P5_BCS_IM", "P5_IMC11", "P5_BKS_HYP11"]:
    assert g[key]["status"] in closed, (key, g[key])
assert g["P5_GPR11"]["status"] == "OPEN_CONCEPTUAL_GATE"
assert g["P5_BOC_NZ11"]["status"] == "PENDING_LOCAL_SAGE_REPLAY"
assert g["P5_LAT11"]["status"] == "BLOCKED"
assert set(g["P5_LAT11"]["requires"]) == {"P5_BOC_NZ11", "P5_GPR11"}
assert g["FULL_BSD"]["status"] == "NOT_CLAIMED"
print("GATE_LOGIC_OK")
