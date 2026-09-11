"""Where the Phase 1 census package lives.

Eight gates read `BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12` — the
package the corpus's Phase 1 line archived (inputs/, results/, sources/). Until
RUN-069 its location was one absolute path on the machine the line ran on.
This module resolves it in order:

  1. the environment variable BSD_CENSUS_PKG, if set — the package's root directory;
  2. the original location, D:/我的研究/學術討論/論文/數學/BSD/<NAME>;
  3. `<handoff bundle>/census/<NAME>`, i.e. three directories above this file —
     the layout `handoff/build_handoff.py` produces.

The first that exists wins; if none does, the last candidate is returned so
that the gate's own error names a path rather than a None.
"""

from __future__ import annotations

import os
import pathlib

NAME = "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12"
_HERE = pathlib.Path(__file__).resolve()


def candidates() -> list[pathlib.Path]:
    out = []
    env = os.environ.get("BSD_CENSUS_PKG")
    if env:
        out.append(pathlib.Path(env))
    out.append(pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD") / NAME)
    out.append(_HERE.parents[3] / "census" / NAME)          # <bundle>/census/<NAME>
    return out


def root() -> pathlib.Path:
    for c in candidates():
        if c.exists():
            return c
    return candidates()[-1]


PKG = root()
