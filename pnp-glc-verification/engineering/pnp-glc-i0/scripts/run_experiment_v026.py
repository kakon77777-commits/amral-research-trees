from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=20260810)
    parser.add_argument("--two-sat-crosscheck-seed", type=int, default=20260809)
    parser.add_argument("--max-parity-n", type=int, default=12)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    from pnp_glc_i0.experiment_v026 import render_report, run_i0

    rendered = render_report(
        run_i0(
            root,
            seed=args.seed,
            two_sat_crosscheck_seed=args.two_sat_crosscheck_seed,
            max_parity_n=args.max_parity_n,
        )
    )
    if args.output:
        output = args.output
        if not output.is_absolute():
            output = root / output
        output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
