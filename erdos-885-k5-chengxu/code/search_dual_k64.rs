use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;

#[derive(Clone)]
struct Row {
    n: u64,
    factors: Vec<(u64, u32)>,
}

fn sieve_spf(limit: usize) -> Vec<u32> {
    let mut spf = vec![0u32; limit + 1];
    if limit >= 1 {
        spf[1] = 1;
    }
    for i in 2..=limit {
        if spf[i] == 0 {
            spf[i] = i as u32;
            if i <= limit / i {
                let mut j = i * i;
                while j <= limit {
                    if spf[j] == 0 {
                        spf[j] = i as u32;
                    }
                    j += i;
                }
            }
        }
    }
    spf
}

fn add_factorization(mut n: u64, spf: &[u32], out: &mut BTreeMap<u64, u32>) {
    while n > 1 {
        let p = spf[n as usize] as u64;
        let mut e = 0u32;
        while n % p == 0 {
            n /= p;
            e += 1;
        }
        *out.entry(p).or_insert(0) += e;
    }
}

fn product_factorization(x: u64, y: u64, spf: &[u32]) -> Vec<(u64, u32)> {
    let mut map = BTreeMap::new();
    add_factorization(x, spf, &mut map);
    add_factorization(y, spf, &mut map);
    map.into_iter().collect()
}

fn divisors(factors: &[(u64, u32)]) -> Vec<u64> {
    let mut ds = vec![1u64];
    for &(p, e) in factors {
        let base_len = ds.len();
        let mut pow = 1u64;
        for _ in 0..e {
            pow = pow.checked_mul(p).expect("divisor overflow");
            for i in 0..base_len {
                ds.push(ds[i].checked_mul(pow).expect("divisor overflow"));
            }
        }
    }
    ds
}

fn isqrt(n: u64) -> u64 {
    if n < 2 {
        return n;
    }
    let mut x = (n as f64).sqrt() as u64;
    while (x + 1) <= n / (x + 1) {
        x += 1;
    }
    while x > n / x {
        x -= 1;
    }
    x
}

fn isqrt_u128(n: u128) -> u128 {
    if n < 2 {
        return n;
    }
    let bits = 128u32 - n.leading_zeros();
    let mut x = 1u128 << ((bits + 1) / 2);
    loop {
        let y = (x + n / x) / 2;
        if y >= x {
            return x;
        }
        x = y;
    }
}

fn pair_fiber(p: u64, q: u64, spf: &[u32]) -> Vec<Row> {
    let left = q - p;
    let right = q + p;
    let g = left * right;
    let gf = product_factorization(left, right, spf);
    let mut rows = Vec::new();
    let mut seen = HashSet::new();
    for u in divisors(&gf) {
        let v = g / u;
        if u >= v || ((u ^ v) & 1) != 0 {
            continue;
        }
        let sp = (v - u) / 2;
        let sq = (v + u) / 2;
        if sp <= p || sq <= q || ((sp ^ p) & 1) != 0 || ((sq ^ q) & 1) != 0 {
            continue;
        }
        let a = (sp - p) / 2;
        let b = (sp + p) / 2;
        if a == 0 || a > spf.len() as u64 - 1 || b > spf.len() as u64 - 1 {
            panic!("SPF bound failure at p={}, q={}, a={}, b={}", p, q, a, b);
        }
        let n = a * b;
        assert_eq!(sp * sp, p * p + 4 * n);
        assert_eq!(sq * sq, q * q + 4 * n);
        assert!(seen.insert(n), "duplicate pair-fiber row");
        rows.push(Row {
            n,
            factors: product_factorization(a, b, spf),
        });
    }
    rows.sort_by_key(|r| r.n);
    rows
}

fn support_groups(rows: &[Row], q: u64, row_target: usize) -> Vec<(u64, Vec<u16>)> {
    assert!(rows.len() <= u16::MAX as usize, "pair fiber exceeds u16 index capacity");
    let mut by_difference: HashMap<u64, Vec<u16>> = HashMap::new();
    for (idx, row) in rows.iter().enumerate() {
        for a in divisors(&row.factors) {
            if a > row.n / a {
                continue;
            }
            let d = row.n / a - a;
            if d > q {
                by_difference.entry(d).or_default().push(idx as u16);
            }
        }
    }
    let mut retained: Vec<_> = by_difference
        .into_iter()
        .filter(|(_, indices)| indices.len() >= row_target)
        .collect();
    retained.sort_by_key(|(d, _)| *d);
    retained
}

fn factor_difference_member(n: u128, d: u128) -> bool {
    let z = d * d + 4 * n;
    let x = isqrt_u128(z);
    x * x == z
}

fn self_test() {
    let spf = sieve_spf(1_000_000);
    let rows_1 = pair_fiber(330, 870, &spf);
    assert_eq!(rows_1.len(), 26);
    let ds_1 = [330, 870, 2445, 4155, 10482];
    let selected_1: Vec<u64> = rows_1
        .iter()
        .filter(|r| ds_1.iter().all(|&d| factor_difference_member(r.n as u128, d)))
        .map(|r| r.n)
        .collect();
    assert_eq!(selected_1, vec![189000, 3992800, 11282544]);

    let rows_2 = pair_fiber(36, 468, &spf);
    assert_eq!(rows_2.len(), 23);
    let ds_2 = [36, 468, 692, 1028];
    let selected_2: Vec<u64> = rows_2
        .iter()
        .filter(|r| ds_2.iter().all(|&d| factor_difference_member(r.n as u128, d)))
        .map(|r| r.n)
        .collect();
    assert_eq!(selected_2, vec![79200, 227205, 1258560]);
    assert!(selected_2
        .iter()
        .all(|&n| !factor_difference_member(n as u128, 1029)));
    println!("SELF_TEST=PASS");
}

fn main() {
    let mut args: Vec<String> = env::args().skip(1).collect();
    if args.first().map(String::as_str) == Some("--self-test") {
        self_test();
        return;
    }
    let row_target = if args.first().map(String::as_str) == Some("--rows") {
        assert!(args.len() >= 2, "--rows requires 3 or 4");
        let value: usize = args[1].parse().expect("row target must be 3 or 4");
        args.drain(0..2);
        value
    } else {
        4
    };
    assert!(row_target == 3 || row_target == 4, "row target must be 3 or 4");
    let (q_min, q_max) = match args.as_slice() {
        [] => (1, 300),
        [end] => (1, end.parse().expect("q_max must be an integer")),
        [start, end] => (
            start.parse().expect("q_min must be an integer"),
            end.parse().expect("q_max must be an integer"),
        ),
        _ => panic!("usage: search_dual_k64 [--rows 3|4] [q_max] | [q_min q_max] | --self-test"),
    };
    assert!(q_max >= 2);
    assert!(q_min >= 1 && q_min <= q_max);
    let spf_limit = (q_max * q_max) as usize;
    let spf = sieve_spf(spf_limit);

    let mut anchors = 0u64;
    let mut eligible_fibers = 0u64;
    let mut fiber_entries = 0u64;
    let mut retained_differences = 0u64;
    let mut max_fiber = 0usize;
    let mut max_retained = 0usize;
    let mut max_mask_support = 0u32;
    let mut quad_support_updates = 0u64;
    let mut quartets_with_extra_1 = 0u64;
    let mut quartets_with_extra_2 = 0u64;
    let mut quartets_with_extra_3 = 0u64;
    let mut best_near: Option<(usize, u64, u64, Vec<u64>, Vec<u64>)> = None;

    for q in q_min..=q_max {
        for p in 0..q {
            anchors += 1;
            let rows = pair_fiber(p, q, &spf);
            fiber_entries += rows.len() as u64;
            max_fiber = max_fiber.max(rows.len());
            if rows.len() < row_target {
                continue;
            }
            eligible_fibers += 1;
            let groups = support_groups(&rows, q, row_target);
            retained_differences += groups.len() as u64;
            max_retained = max_retained.max(groups.len());
            for (_, indices) in &groups {
                max_mask_support = max_mask_support.max(indices.len() as u32);
            }
            let mut subset_to_differences: HashMap<Vec<u16>, Vec<u64>> = HashMap::new();
            for (d, indices) in &groups {
                if row_target == 3 {
                    for a in 0..indices.len() {
                        for b in a + 1..indices.len() {
                            for c in b + 1..indices.len() {
                                quad_support_updates += 1;
                                let key = vec![indices[a], indices[b], indices[c]];
                                subset_to_differences.entry(key).or_default().push(*d);
                            }
                        }
                    }
                } else {
                    for a in 0..indices.len() {
                        for b in a + 1..indices.len() {
                            for c in b + 1..indices.len() {
                                for e in c + 1..indices.len() {
                                    quad_support_updates += 1;
                                    let key = vec![indices[a], indices[b], indices[c], indices[e]];
                                    subset_to_differences.entry(key).or_default().push(*d);
                                }
                            }
                        }
                    }
                }
            }
            for (row_indices, ds) in subset_to_differences {
                let selected_rows: Vec<u64> = row_indices
                    .iter()
                    .map(|&i| rows[i as usize].n)
                    .collect();
                match ds.len() {
                    1 => quartets_with_extra_1 += 1,
                    2 => quartets_with_extra_2 += 1,
                    3 => quartets_with_extra_3 += 1,
                    _ => {}
                }
                if best_near.as_ref().map_or(true, |best| ds.len() > best.0) {
                    best_near = Some((ds.len(), p, q, selected_rows.clone(), ds.clone()));
                    eprintln!(
                        "record extra_count={} anchor=[{}, {}] rows={:?} extra={:?}",
                        ds.len(), p, q, selected_rows, ds
                    );
                }
                if ds.len() < 4 {
                    continue;
                }
                let extra: Vec<u64> = ds.into_iter().take(4).collect();
                let mut six_differences = vec![p, q];
                six_differences.extend(extra.iter().copied());
                six_differences.sort_unstable();
                assert_eq!(six_differences.len(), 6);
                assert!(selected_rows.iter().all(|&n| six_differences.iter().all(|&d| factor_difference_member(n as u128, d as u128))));

                println!("FOUND_K6{row_target} p={p} q={q}");
                println!("K6{row_target}_ROWS={selected_rows:?}");
                println!("K6{row_target}_DIFFERENCES={six_differences:?}");

                let base = six_differences[0];
                let transposed_rows: Vec<u128> = six_differences[1..]
                    .iter()
                    .map(|&d| (d as u128) * (d as u128) - (base as u128) * (base as u128))
                    .collect();
                let mut transposed_differences = vec![2 * base];
                for &n in &selected_rows {
                    let x = isqrt(base * base + 4 * n);
                    assert_eq!(x * x, base * base + 4 * n);
                    transposed_differences.push(2 * x);
                }
                transposed_differences.sort_unstable();
                assert!(transposed_rows.iter().all(|&n| transposed_differences.iter().all(|&d| factor_difference_member(n, d as u128))));
                println!("TRANSPOSED_K{}5_ROWS={transposed_rows:?}", row_target + 1);
                println!("TRANSPOSED_K{}5_DIFFERENCES={transposed_differences:?}", row_target + 1);
                println!("STATUS=EXACT_CERTIFICATE");
                return;
            }
        }
        if q % 100 == 0 || q == q_max {
            eprintln!("progress q={q} range=[{q_min},{q_max}] anchors={anchors} eligible={eligible_fibers}");
        }
    }

    println!("STATUS=NO_K6{row_target}_WITH_CANONICAL_SECOND_DIFFERENCE_IN_[{q_min},{q_max}]");
    println!("anchors={anchors}");
    println!("eligible_fibers={eligible_fibers}");
    println!("fiber_entries={fiber_entries}");
    println!("retained_differences={retained_differences}");
    println!("max_fiber={max_fiber}");
    println!("max_retained={max_retained}");
    println!("max_mask_support={max_mask_support}");
    println!("quad_support_updates={quad_support_updates}");
    println!("quartets_with_exactly_1_extra={quartets_with_extra_1}");
    println!("quartets_with_exactly_2_extra={quartets_with_extra_2}");
    println!("quartets_with_exactly_3_extra={quartets_with_extra_3}");
    if let Some((count, p, q, rows, extra)) = best_near {
        println!("best_near_extra_count={count}");
        println!("best_near_anchor=[{p}, {q}]");
        println!("best_near_rows={rows:?}");
        println!("best_near_extra_differences={extra:?}");
    }
}
