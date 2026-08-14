-- 01_edixhoven_safe_structural_pool.sql
--
-- Strict structural pool:
--   * cheap rank-zero parity gates
--   * at least one fixed odd additive prime
--   * ALL fixed odd additive primes are in the conservative Edixhoven-safe
--     pool: p>=11 and Kodaira code not II/III/IV = 2/3/4
--   * at least two odd multiplicative primes
--   * at least one nonsplit multiplicative prime
--   * every fixed multiplicative prime has a distinct residual-ramification
--     witness (leave-one-out)
--   * every fixed odd additive prime has a nonsplit H3 witness
--   * no odd nonmaximal residual prime (clean first pool)
--   * singleton rational isogeny class (clean optimality/period pool)
--
-- Still NOT checked here:
--   BSD(E,2), local FW-H2 at additive primes.

WITH base AS (
    SELECT
        c.lmfdb_label,
        c.lmfdb_iso,
        c.conductor,
        c.ainvs,
        c.bad_primes,
        c.rank,
        c.analytic_rank,
        c.torsion,
        c.class_size,
        c.optimality,
        c.manin_constant,
        c.signD,
        c.nonmax_primes,
        c.isogeny_degrees,
        m.sha_an,
        m.tamagawa_product,
        m.real_period,
        m.special_value
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

      -- Clean first pool: all odd residual images maximal.
      AND NOT EXISTS (
          SELECT 1
          FROM unnest(COALESCE(c.nonmax_primes, '{}'::smallint[])) AS r(p)
          WHERE r.p > 2
      )

      -- At least one odd additive prime.
      AND EXISTS (
          SELECT 1
          FROM ec_localdata AS a
          WHERE a.lmfdb_label = c.lmfdb_label
            AND a.prime > 2
            AND a.reduction_type = 0
      )

      -- Every odd additive prime is conservatively Edixhoven-safe:
      -- p >= 11 and not unstarred II/III/IV (LMFDB codes 2,3,4).
      AND NOT EXISTS (
          SELECT 1
          FROM ec_localdata AS a
          WHERE a.lmfdb_label = c.lmfdb_label
            AND a.prime > 2
            AND a.reduction_type = 0
            AND (
                a.prime < 11
                OR a.kodaira_symbol IN (2,3,4)
            )
      )

      -- Need at least two odd multiplicative bad primes.
      AND (
          SELECT COUNT(*)
          FROM ec_localdata AS mloc
          WHERE mloc.lmfdb_label = c.lmfdb_label
            AND mloc.prime > 2
            AND mloc.reduction_type IN (-1,1)
      ) >= 2

      -- Need a nonsplit multiplicative reservoir for Fouquet-Wan H3.
      AND EXISTS (
          SELECT 1
          FROM ec_localdata AS ns
          WHERE ns.lmfdb_label = c.lmfdb_label
            AND ns.prime > 2
            AND ns.reduction_type = -1
      )

      -- Fixed multiplicative leave-one-out graph:
      -- every multiplicative p has another multiplicative ell != p
      -- with p ∤ v_ell(Delta).
      AND NOT EXISTS (
          SELECT 1
          FROM ec_localdata AS pbad
          WHERE pbad.lmfdb_label = c.lmfdb_label
            AND pbad.prime > 2
            AND pbad.reduction_type IN (-1,1)
            AND NOT EXISTS (
                SELECT 1
                FROM ec_localdata AS wit
                WHERE wit.lmfdb_label = c.lmfdb_label
                  AND wit.prime > 2
                  AND wit.reduction_type IN (-1,1)
                  AND wit.prime <> pbad.prime
                  AND MOD(wit.discriminant_valuation, pbad.prime) <> 0
            )
      )

      -- Every fixed odd additive p gets at least one nonsplit H3 witness ell
      -- with p ∤ v_ell(Delta).
      AND NOT EXISTS (
          SELECT 1
          FROM ec_localdata AS abad
          WHERE abad.lmfdb_label = c.lmfdb_label
            AND abad.prime > 2
            AND abad.reduction_type = 0
            AND NOT EXISTS (
                SELECT 1
                FROM ec_localdata AS ns
                WHERE ns.lmfdb_label = c.lmfdb_label
                  AND ns.prime > 2
                  AND ns.reduction_type = -1
                  AND MOD(ns.discriminant_valuation, abad.prime) <> 0
            )
      )
)
SELECT *
FROM base
ORDER BY conductor, lmfdb_label;
