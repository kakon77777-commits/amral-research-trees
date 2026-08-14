#!/usr/bin/env bash
# Drive the exhaustive descent verification as disjoint, separately logged
# chunks. Each chunk is an independent claim about its own interval; the union
# is only a claim about [3, N] once verify_run_logs.py has confirmed that the
# intervals tile [3, N] with no gap and no overlap.
#
# Usage: bash code/run_verification.sh <N> <chunks> <sieve_k> <threads> <tag>
set -u

N=${1:-1099511627776}
CHUNKS=${2:-8}
K=${3:-20}
THREADS=${4:-16}
TAG=${5:-main}

BIN=./build/collatz_verify.exe
OUT=data/raw-logs

mkdir -p "$OUT"
WIDTH=$(( (N + CHUNKS - 1) / CHUNKS ))
LO=3
for ((i = 1; i <= CHUNKS; i++)); do
  HI=$(( i * WIDTH ))
  if (( HI > N )); then HI=$N; fi
  if (( LO > N )); then break; fi
  NAME=$(printf "%s_chunk%02d" "$TAG" "$i")
  echo "[$(date -u +%H:%M:%S)] chunk $i/$CHUNKS  [$LO, $HI]"
  "$BIN" --from "$LO" --to "$HI" --sieve "$K" --threads "$THREADS" \
    >"$OUT/${NAME}.out.log" 2>"$OUT/${NAME}.err.log"
  RC=$?
  echo "  rc=$RC $(cat "$OUT/${NAME}.out.log")"
  if (( RC != 0 )); then
    echo "  ABORTING: chunk $i did not exit clean. The partial logs are kept."
    exit "$RC"
  fi
  LO=$(( HI + 1 ))
done
echo "[$(date -u +%H:%M:%S)] all chunks exited clean; now run verify_run_logs.py"
