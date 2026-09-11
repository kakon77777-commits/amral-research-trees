#!/usr/bin/env bash
# Run the mutation drill as N parallel shards, then merge them into
# data/gate-logs/src11-gate-drill.json.
#
#   bash code/run_sharded_drill.sh 8 /tmp/drill-logs
#
# Each shard takes every N-th planted defect and control, runs its own
# baseline and its own restored-state check, and writes a partial log; the
# merge reassembles them in index order and refuses an incomplete or
# inconsistent set. One pass over the 97 checks is ~35 s single-process; a
# full drill (294 defects, 60 controls) is ~45 min on 8 shards of a laptop.
set -u
N="${1:-8}"
LOGDIR="${2:-./drill-logs}"
TREE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$TREE" || exit 2
mkdir -p "$LOGDIR"
start=$(date +%s)
pids=()
for ((k=0; k<N; k++)); do
  python -X utf8 -u code/src11_gate_drill.py --shard "$k/$N" --out "$LOGDIR/shard$k.json" > "$LOGDIR/shard$k.log" 2>&1 &
  pids+=($!)
done
fail=0
for pid in "${pids[@]}"; do
  wait "$pid" || fail=1
done
mid=$(date +%s)
echo "shards finished in $((mid-start)) s, any shard non-zero: $fail"
for ((k=0; k<N; k++)); do
  printf '  shard %d: ' "$k"; tail -1 "$LOGDIR/shard$k.log"
done
parts=()
for ((k=0; k<N; k++)); do parts+=("$LOGDIR/shard$k.json"); done
python -X utf8 code/src11_gate_drill.py --merge "${parts[@]}" > "$LOGDIR/merge.log" 2>&1
rc=$?
end=$(date +%s)
echo "merge exit=$rc, total $((end-start)) s"
tail -9 "$LOGDIR/merge.log"
exit $rc
