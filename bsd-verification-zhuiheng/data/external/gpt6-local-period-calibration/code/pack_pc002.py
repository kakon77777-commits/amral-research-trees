"""Build the deterministic PC-002 review handoff from tracked research payloads."""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
FILES={
    "README.md":"handoff/README.md",
    "PC-002-RELATIVE-REGULATOR.md":"reports/PC-002-RELATIVE-REGULATOR.md",
    "INPUTS.json":"data/pc002-inputs.json",
    "code/relative_regulator.py":"code/relative_regulator.py",
    "code/cup_normalization.py":"code/cup_normalization.py",
    "result.json":"data/pc002-relative-regulator.json",
    "cup-result.json":"data/pc002-cup-normalization.json",
}


def main():
    payload={name:(ROOT/source).read_bytes() for name,source in FILES.items()}
    manifest={"round":"PC-002","schema_version":1,
              "files":{name:{"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
                       for name,data in sorted(payload.items())},
              "speaker_label":"unresolved","BSD_proved":False}
    payload["MANIFEST.json"]=(json.dumps(manifest,indent=2)+"\n").encode()
    target=ROOT/"handoff"/"PC-002-relative-regulator.zip"
    with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,data in sorted(payload.items()):
            info=zipfile.ZipInfo(name,(2026,9,13,0,0,0))
            info.create_system=3
            info.external_attr=0o100644 << 16
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ArithmeticError("ZIP integrity failure")
        for name,entry in manifest["files"].items():
            if hashlib.sha256(archive.read(name)).hexdigest()!=entry["sha256"]:
                raise ArithmeticError(name)
    print(json.dumps({"file":target.name,"members":len(payload),"bytes":target.stat().st_size,
                      "sha256":hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))


if __name__=="__main__":
    main()
