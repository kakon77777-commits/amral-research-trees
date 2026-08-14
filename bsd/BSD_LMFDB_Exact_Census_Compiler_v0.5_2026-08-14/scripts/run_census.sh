#!/usr/bin/env bash
set -euo pipefail

HOST="${LMFDB_HOST:-devmirror.lmfdb.xyz}"
PORT="${LMFDB_PORT:-5432}"
DB="${LMFDB_DB:-lmfdb}"
USER="${LMFDB_USER:-lmfdb}"

export PGPASSWORD="${LMFDB_PASSWORD:-lmfdb}"

mkdir -p results/raw results/final

psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" \
  -f sql/00_candidate_universe.sql --csv \
  > results/raw/00_candidate_universe.csv

psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" \
  -f sql/01_edixhoven_safe_structural_pool.sql --csv \
  > results/raw/01_structural_pool.csv

psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" \
  -f sql/02_local_rows_for_structural_pool.sql --csv \
  > results/raw/02_local_rows.csv

python scripts/postprocess_witness_network.py \
  --base results/raw/01_structural_pool.csv \
  --local results/raw/02_local_rows.csv \
  --outdir results/final

sha256sum \
  sql/*.sql \
  results/raw/*.csv \
  results/final/* \
  > results/SHA256SUMS.runtime.txt

echo "LMFDB exact census pipeline completed."
