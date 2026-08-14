-- 02_local_rows_for_structural_pool.sql
-- Materialize ALL bad-local rows for curves passing the strict structural pool.
--
-- Keep this query logically synchronized with 01_edixhoven_safe_structural_pool.sql.

WITH base AS (
    SELECT c.lmfdb_label
    FROM ec_curvedata AS c
    JOIN ec_mwbsd AS m
      ON m.lmfdb_label = c.lmfdb_label
    WHERE c.rank = 0
      AND c.analytic_rank = 0
      AND c.torsion = 1
      AND c.optimality = 1
      AND c.semistable = FALSE
      AND c.manin_constant IS NOT NULL
      AND MOD(c.manin_constant, 2) = 1
      AND c.sha = 1
      AND m.sha_an = 1::numeric
      AND MOD(m.tamagawa_product, 2) = 1
      AND c.class_size = 1
      AND NOT EXISTS (
          SELECT 1
          FROM unnest(COALESCE(c.nonmax_primes, '{}'::smallint[])) AS r(p)
          WHERE r.p > 2
      )
      AND EXISTS (
          SELECT 1 FROM ec_localdata a
          WHERE a.lmfdb_label=c.lmfdb_label
            AND a.prime>2 AND a.reduction_type=0
      )
      AND NOT EXISTS (
          SELECT 1 FROM ec_localdata a
          WHERE a.lmfdb_label=c.lmfdb_label
            AND a.prime>2 AND a.reduction_type=0
            AND (a.prime<11 OR a.kodaira_symbol IN (2,3,4))
      )
      AND (
          SELECT COUNT(*) FROM ec_localdata mm
          WHERE mm.lmfdb_label=c.lmfdb_label
            AND mm.prime>2 AND mm.reduction_type IN (-1,1)
      ) >= 2
      AND EXISTS (
          SELECT 1 FROM ec_localdata ns
          WHERE ns.lmfdb_label=c.lmfdb_label
            AND ns.prime>2 AND ns.reduction_type=-1
      )
      AND NOT EXISTS (
          SELECT 1 FROM ec_localdata pbad
          WHERE pbad.lmfdb_label=c.lmfdb_label
            AND pbad.prime>2 AND pbad.reduction_type IN (-1,1)
            AND NOT EXISTS (
                SELECT 1 FROM ec_localdata wit
                WHERE wit.lmfdb_label=c.lmfdb_label
                  AND wit.prime>2 AND wit.reduction_type IN (-1,1)
                  AND wit.prime<>pbad.prime
                  AND MOD(wit.discriminant_valuation,pbad.prime)<>0
            )
      )
      AND NOT EXISTS (
          SELECT 1 FROM ec_localdata abad
          WHERE abad.lmfdb_label=c.lmfdb_label
            AND abad.prime>2 AND abad.reduction_type=0
            AND NOT EXISTS (
                SELECT 1 FROM ec_localdata ns
                WHERE ns.lmfdb_label=c.lmfdb_label
                  AND ns.prime>2 AND ns.reduction_type=-1
                  AND MOD(ns.discriminant_valuation,abad.prime)<>0
            )
      )
)
SELECT
    ld.lmfdb_label,
    ld.prime,
    ld.conductor_valuation,
    ld.discriminant_valuation,
    ld.j_denominator_valuation,
    ld.kodaira_symbol,
    ld.reduction_type,
    ld.root_number,
    ld.tamagawa_number
FROM ec_localdata AS ld
JOIN base AS b USING (lmfdb_label)
ORDER BY ld.lmfdb_label, ld.prime;
