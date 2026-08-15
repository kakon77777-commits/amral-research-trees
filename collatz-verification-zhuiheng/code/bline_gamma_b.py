"""Emit the B-line's Gamma_B record for the extremal first-crossing words.

數學戰士「墜衡」 / AMRAL Research Lab.

`Hard_Zeta_B_Line_Handoff_v0.1.md` §25 asks that the next line keep, for each
first-crossing word,

    Gamma_B(w) = (k, u, Delta_w, b_w, r_w, nu(w), m_w, Lambda(w))

and §26's Round B-01 Steps 1-4 ask for the enumeration, the exact quantities, and
the extremal structure. This script emits that for the two extremal words at each
length — the minimum integer slack and the maximum correction ratio — so the B
line starts from data rather than regenerating it.

**This is an emitter, not a check.** It asserts nothing. Everything it prints is
computed by `hz_chart_algebra.py`, whose slack layer is drilled by `src14_drill.py`;
the checks that grade these quantities live in
`src14_hardzeta_bline_aline_closure_recheck.py`.

Usage:  python code/bline_gamma_b.py [maxlen] > data/b-line-gamma-b.json
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import hz_chart_algebra as C  # noqa: E402


def gamma_b(w: "C.Chart") -> dict:
    """§25's record, in the handoff's own order."""
    return {
        "word": w.word, "k": w.k, "u": w.u,
        "delta_w": C.delta_of(w.k, w.u), "b_w": w.b, "r_w": w.r,
        "nu_w": C.nu(w), "m_w": w.m,
        "lambda_w": C.correction_slack(w),
        "ratio_R": str(C.normalized_correction_ratio(w)),
        "ratio_R_float": float(C.normalized_correction_ratio(w)),
    }


def main() -> int:
    maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    words = C.first_crossing_words(maxlen)

    per: dict[int, list] = {}
    for w in words:
        per.setdefault(w.k, []).append(w)

    lengths = []
    for k in sorted(per):
        fam = per[k]
        lengths.append({
            "length": k,
            "words": len(fam),
            "min_slack": gamma_b(min(fam, key=C.correction_slack)),
            "max_ratio": gamma_b(max(fam, key=C.normalized_correction_ratio)),
        })

    global_min = min(words, key=C.correction_slack)
    global_max = max(words, key=C.normalized_correction_ratio)

    out = {
        "tool": "bline_gamma_b.py",
        "_what_this_is": (
            "Gamma_B records for the extremal first-crossing words, as asked for "
            "by Hard_Zeta_B_Line_Handoff_v0.1.md §25 and §26 Round B-01. An "
            "emitter, not a check: it asserts nothing."),
        "enumeration": {
            "max_word_length": maxlen,
            "first_crossing_words": len(words),
            "note": ("W_fc is pruned by its own defining condition — a word is "
                     "extended only while still uniformly expanding — so this is "
                     "the complete set to this length, not a sample."),
        },
        "terras_form": (
            "Terras coefficient-stopping equality on W_fc is exactly "
            "Lambda(w) >= 1 for every first-crossing word (handoff §13)."),
        "global_extremals": {
            "min_slack": gamma_b(global_min),
            "max_ratio": gamma_b(global_max),
        },
        "by_length": lengths,
        "observations_for_round_B01": [
            f"minimum slack over all {len(words)} words is "
            f"{C.correction_slack(global_min)}, at {global_min.word or '(root)'}",
            f"supremum of R(w) is "
            f"{C.normalized_correction_ratio(global_max)} at {global_max.word}, "
            f"of length {global_max.k}",
            "no length beyond the argmax comes within a factor of ten of it, but "
            "the post-argmax maximum does NOT decay — it oscillates, and its "
            "largest value sits at the longest length examined, so there is no "
            "evidence here for max R -> 0",
        ],
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
