# Sources / data contracts

## LMFDB access options

Official LMFDB database access page:

- API: simple HTTP table queries, at most 10,000 results and 100 per request.
- Direct read-only PostgreSQL mirror is recommended for complex joins.
- SQL mirror connection:
  - host `devmirror.lmfdb.xyz`
  - port `5432`
  - db/user/password `lmfdb`.

The compiler uses the SQL mirror because the census joins curve, MW/BSD and
local-reduction tables and requires correlated witness-graph predicates.

## LMFDB tables used

### `ec_curvedata`

Relevant columns observed in the current LMFDB release include:

```text
lmfdb_label
lmfdb_iso
conductor
ainvs
analytic_rank
rank
torsion
class_size
optimality
manin_constant
semistable
sha
nonmax_primes
isogeny_degrees
bad_primes
signD
```

### `ec_mwbsd`

```text
lmfdb_label
sha_an
tamagawa_product
real_period
special_value
rank_bounds
```

### `ec_localdata`

```text
lmfdb_label
prime
conductor_valuation
discriminant_valuation
j_denominator_valuation
kodaira_symbol
reduction_type
root_number
tamagawa_number
```

Current examples show:
- `reduction_type = 0`: additive;
- `reduction_type = 1`: split multiplicative;
- `reduction_type = -1`: nonsplit multiplicative.

For primes >=5 the local Kodaira integer examples used in this compiler show:
- code `2`: type II;
- code `3`: type III;
- code `4`: type IV;
- code `-1`: type I0*.

The strict SQL therefore excludes additive codes 2/3/4 as a conservative
Edixhoven-safe filter.
