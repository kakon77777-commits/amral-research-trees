# `data/external/` — third-party snapshots

Byte-exact copies of four OEIS b-files, downloaded 2026-08-14. They are the
external half of this tree's verification: they were computed by other people,
by other methods, and are not derived from anything in this repository.

| File | Sequence | Content |
|---|---|---|
| `b006877.txt` | A006877 | starting values setting a new record for the number of `C`-steps to reach 1 |
| `b006878.txt` | A006878 | the corresponding record step counts |
| `b006884.txt` | A006884 | starting values setting a new record for the highest point of the `C`-trajectory |
| `b006885.txt` | A006885 | the corresponding record high points |

Source URLs are recorded in `../../code/anchors.py`, which also prints the
SHA-256 of each file on every run, so a silently swapped snapshot shows up in
the run report rather than in the conclusion.

## A known inconsistency in the upstream data

As snapshotted, **A006884 carries 98 terms while its companion A006885 carries
97**. The pair is maintained separately upstream and was not extended in step.
`anchors.py` uses only the paired prefix and reports the term counts it
actually used; it does not let `zip()` absorb the difference silently. The
unpaired 98th term of A006884 (`2358909599867980429759`) is far above any bound
reached locally, so it does not affect the comparisons performed here.

A006877/A006878 are paired and consistent at 148 terms each.

These files are third-party data included for verification purposes. They are
not covered by this repository's own licence grant; see OEIS's terms.
