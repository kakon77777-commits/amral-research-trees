"""Build the web-chat edition of the handoff: what a browser AI can take.

    python handoff/build_web_edition.py

Produces, in handoff/web/:

  BSD-handoff-digest-<date>.md    ONE file, pasteable: HANDOFF.md as built (with the
                                  README round table), then every round's Result
                                  paragraph in order — the 69 headline findings with
                                  their figures, as each report states them — then
                                  the open-gates table again at the end so it is the
                                  last thing read.
  sandbox-pack-<date>.zip         ~40 KB: the modular-symbols gate (src70) with the
                                  one corpus document it reads, in the relative
                                  layout it expects, plus a README. A chat AI with a
                                  Python sandbox can unzip it and reproduce
                                  δ_{397·991} = 5 (mod 11) in about ten seconds with
                                  the standard library alone. Nothing else in the
                                  tree runs without the census package.

The full bundle (handoff/BSD-verification-handoff-<date>.zip) is the real
handoff; this edition is for a chat window.
"""

from __future__ import annotations

import datetime
import pathlib
import re
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
TREE = HERE.parent
AMRAL = TREE.parent.parent / "amral"
TODAY = datetime.date.today().isoformat()
BUILD = HERE / "build" / f"BSD-verification-handoff-{TODAY}"
WEB = HERE / "web"
NL = chr(10)


def result_paragraphs() -> str:
    out = []
    for f in sorted((TREE / "reports").glob("RUN-*.md")):
        s = f.read_text(encoding="utf-8")
        title = next(l for l in s.splitlines() if l.startswith("# "))
        subj = next((l for l in s.splitlines() if l.startswith("**Subject:**")), "")
        subj = re.sub(r"\]\([^)]*\)", "]", subj)                      # drop link targets
        i = s.find("**Result")
        j = s.find(NL + NL, i)
        para = s[i:j].strip()
        para = re.sub(r"\]\([^)]*\)", "]", para)
        out.append(title + NL + NL + subj + NL + NL + para + NL)
    return (NL + "---" + NL).join(out)


def open_gates_section(handoff: str) -> str:
    i = handoff.index("### 5.2 Open")
    j = handoff.index("## 6.", i)
    return handoff[i:j].rstrip()


def main() -> int:
    WEB.mkdir(parents=True, exist_ok=True)
    handoff = (BUILD / "HANDOFF.md").read_text(encoding="utf-8")
    digest = (handoff.rstrip() + NL + NL + "---" + NL + NL
              + "# Every round's Result paragraph, RUN-001 … RUN-069" + NL + NL
              + "Each is the opening paragraph of that round's report, verbatim (link targets removed); "
              + "every figure in it traces to the gate log named in the report." + NL + NL
              + result_paragraphs() + NL + NL + "---" + NL + NL
              + "# Read last: what is open" + NL + NL + open_gates_section(handoff) + NL)
    dpath = WEB / f"BSD-handoff-digest-{TODAY}.md"
    dpath.write_text(digest, encoding="utf-8")
    # the sandbox pack
    zpath = WEB / f"sandbox-pack-{TODAY}.zip"
    readme = (
        "# Sandbox pack — reproduce the Kurihara number of 389.a1 at 397·991 mod 11" + NL + NL
        + "Python 3.11+ standard library only; no network. From this directory:" + NL + NL
        + "    cd amral-research-trees/bsd-verification-zhuiheng" + NL
        + "    python code/src70_kurihara_modular_symbols.py" + NL + NL
        + "Expected (about ten seconds): the plus-eigenline of Γ₀(389) mod 11 found at 65 → 2 → 1, "
        + "first nonzero coordinate at index 5, eigenvalues −5, −3, −6, 5 at 7, 13, 17, 19, then" + NL + NL
        + "    θ̄_n mod I³: {'const': 0, 'X': 0, 'Y': 0, 'X2': 0, 'Y2': 0, 'XY': 5}; δ = 5; raw product sum 43,605,160" + NL + NL
        + "and exit code 0. The log it writes (data/gate-logs/src70-kurihara-modular-symbols.json) carries the "
        + "eigenline, all forty blocks of the sum and the conventions. The gate reads one corpus document, "
        + "included here at the relative path it expects; everything else is computed. See the digest for what "
        + "the number means and what it does not." + NL
    )
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.md", readme)
        z.write(TREE / "code" / "src70_kurihara_modular_symbols.py",
                "amral-research-trees/bsd-verification-zhuiheng/code/src70_kurihara_modular_symbols.py")
        doc = AMRAL / "public" / "bsd" / "p5" / "files" / "BSD_RUGZPB_P2_P4_389a1_p11_v0.2.md"
        z.write(doc, "amral/public/bsd/p5/files/BSD_RUGZPB_P2_P4_389a1_p11_v0.2.md")
        z.write(TREE / "reports" / "RUN-068-KURIHARA-MODULAR-SYMBOLS.md",
                "amral-research-trees/bsd-verification-zhuiheng/reports/RUN-068-KURIHARA-MODULAR-SYMBOLS.md")
    print(f"digest: {dpath} ({dpath.stat().st_size / 1e3:.0f} KB)")
    print(f"sandbox pack: {zpath} ({zpath.stat().st_size / 1e3:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
