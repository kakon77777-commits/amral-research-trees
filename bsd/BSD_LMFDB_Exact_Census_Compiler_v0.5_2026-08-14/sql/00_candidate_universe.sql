-- 00_candidate_universe.sql
-- Cheap rank-zero / 2-adic-parity candidate universe.
--
-- IMPORTANT:
-- This is NOT a proof of BSD(E,2).
-- It only identifies curves whose stored rank-zero BSD quotient has odd
-- 2-adic parity under the strict torsion=1, sha_an=1, Tamagawa odd filter.

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
    c.semistable,
    c.signD,
    c.sha AS sha_integer_field,
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
ORDER BY c.conductor, c.lmfdb_label;
