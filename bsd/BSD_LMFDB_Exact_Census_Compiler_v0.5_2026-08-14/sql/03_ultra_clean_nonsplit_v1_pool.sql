-- 03_ultra_clean_nonsplit_v1_pool.sql
--
-- Optional ultra-clean first theorem pool:
-- require a nonsplit multiplicative prime ell with v_ell(Delta)=1.
--
-- This kills the generic FW-H3 exceptional-prime set completely.
-- It is intentionally stronger than the general witness-network theorem.

WITH structural AS (
    -- Paste / materialize the result of 01_edixhoven_safe_structural_pool.sql
    -- into a temporary table if desired.  In a read-only workflow, use this
    -- query by joining the same base conditions or by passing labels from
    -- the exported CSV to 04_by_label.sql.
    SELECT DISTINCT c.lmfdb_label, c.conductor
    FROM ec_curvedata c
    JOIN ec_mwbsd m ON m.lmfdb_label=c.lmfdb_label
    WHERE c.rank=0
      AND c.analytic_rank=0
      AND c.torsion=1
      AND c.optimality=1
      AND c.semistable=FALSE
      AND c.class_size=1
      AND c.manin_constant IS NOT NULL
      AND MOD(c.manin_constant,2)=1
      AND c.sha=1
      AND m.sha_an=1::numeric
      AND MOD(m.tamagawa_product,2)=1
      AND NOT EXISTS (
          SELECT 1 FROM unnest(COALESCE(c.nonmax_primes,'{}'::smallint[])) r(p)
          WHERE r.p>2
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
)
SELECT s.*
FROM structural s
WHERE EXISTS (
    SELECT 1
    FROM ec_localdata ns
    WHERE ns.lmfdb_label=s.lmfdb_label
      AND ns.prime>2
      AND ns.reduction_type=-1
      AND ns.discriminant_valuation=1
)
ORDER BY s.conductor,s.lmfdb_label;
