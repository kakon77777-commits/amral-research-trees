# `data/raw-logs/` — original run streams

One `.out.log` and one `.err.log` per chunk, exactly as the engine wrote them.
Each `.out.log` holds a single JSON object describing one closed interval.

Naming: `<tag>_chunk<NN>.{out,err}.log`. The `t40` tag is the run covering
`[3, 2^40]`.

These logs are the evidence. `../../code/verify_run_logs.py` reads *only* this
directory — it never re-runs the engine — and refuses to state a conclusion
about `[3, N]` unless the intervals tile it with no gap and no overlap, every
chunk exited clean, every companion `.err.log` is empty, and each chunk's count
of odd starts matches what its interval actually contains.

A non-empty `.err.log`, a missing chunk, or an interval boundary that does not
meet its neighbour is a defect in the run, and the aggregator is written to say
so rather than to average over it. Superseded or interrupted chunks, if any,
are kept and labelled rather than deleted.
