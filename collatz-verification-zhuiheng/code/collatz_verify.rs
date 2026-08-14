// collatz_verify.rs — local Collatz (3x+1) verification engine
// 數學戰士「墜衡」 / AMRAL Research Lab. Apache-2.0 (repository LICENSE).
//
// No external crates. Build:  rustc -O collatz_verify.rs -o collatz_verify
//
// WHAT THIS PROGRAM PROVES, AND WHAT IT DOES NOT
// ----------------------------------------------
// `verify` establishes, for a stated finite interval and relative to THIS
// implementation, that every n in the interval has a Collatz trajectory that
// eventually falls strictly below n. Combined with the same statement holding
// for every smaller start (i.e. running the interval [2, N] from the bottom),
// strong induction gives "every 1 <= n <= N reaches 1". It gives NOTHING about
// n > N. A completed run is never evidence for the conjecture itself.
//
// A run that hits the overflow guard, the step guard, or any internal
// invariant failure is a FAILED run. It is reported as `"ok": false` and must
// not be read as a negative result about Collatz — it is a result about this
// program.
//
// MAPS
// ----
// Standard map  C(x) = x/2 (x even), 3x+1 (x odd).
// Shortcut map  T(x) = x/2 (x even), (3x+1)/2 (x odd).
// T is used for verification (it is the one with the clean 2^k congruence
// structure). `records` uses C, because the OEIS record sequences this program
// is cross-checked against are defined on C.

use std::collections::HashMap;
use std::env;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Mutex;
use std::time::Instant;

/// Any trajectory value strictly above this aborts the run. Chosen so that
/// `3*x + 1` cannot overflow u128 even at the guard boundary.
const VALUE_GUARD: u128 = 1u128 << 120;
/// Any single descent taking more shortcut steps than this aborts the run.
/// The observed maximum below 2^40 is under 1000; 1 << 20 is not a tuning knob.
const STEP_GUARD: u64 = 1 << 20;

// ---------------------------------------------------------------------------
// k-step congruence tables
// ---------------------------------------------------------------------------
//
// For n = q * 2^k + r with 0 <= r < 2^k, the parity of each of the first k
// shortcut steps depends only on r, and
//
//     T^k(n) = q * 3^a(r) + T^k(r)
//
// where a(r) is the number of odd steps among those k. `pow3[r] = 3^a(r)` and
// `tail[r] = T^k(r)`. Both are derived by simulating r itself — no closed form
// is assumed — so the table is a computation, not a claim.

struct Tables {
    k: u32,
    mask: u64,
    pow3: Vec<u64>,
    tail: Vec<u64>,
    odd_steps: Vec<u8>,
}

fn build_tables(k: u32) -> Tables {
    assert!((1..=26).contains(&k), "sieve exponent k must be in 1..=26");
    let m = 1usize << k;
    let mut pow3 = vec![0u64; m];
    let mut tail = vec![0u64; m];
    let mut odd_steps = vec![0u8; m];
    for r in 0..m {
        let mut x = r as u128;
        let mut a: u32 = 0;
        for _ in 0..k {
            if x & 1 == 0 {
                x >>= 1;
            } else {
                x = (3 * x + 1) >> 1;
                a += 1;
            }
        }
        pow3[r] = 3u64.pow(a);
        assert!(x <= u64::MAX as u128, "k-step tail exceeded u64 at r={r}");
        tail[r] = x as u64;
        odd_steps[r] = a as u8;
    }
    Tables { k, mask: (1u64 << k) - 1, pow3, tail, odd_steps }
}

// ---------------------------------------------------------------------------
// Descent check
// ---------------------------------------------------------------------------

#[derive(Debug)]
enum Failure {
    ValueGuard { n: u64, at: u128 },
    StepGuard { n: u64 },
}

struct Descent {
    steps: u64,
    peak: u128,
}

/// Iterate T from `start` until the value is strictly below `n`.
/// `start` must already be T^j(n) for some j >= 0 whose peak is folded in by
/// the caller, or `n` itself.
fn descend_below(n: u64, start: u128) -> Result<Descent, Failure> {
    let bound = n as u128;
    let mut x = start;
    let mut peak = start;
    let mut steps: u64 = 0;
    while x >= bound {
        if x > VALUE_GUARD {
            return Err(Failure::ValueGuard { n, at: x });
        }
        if steps >= STEP_GUARD {
            return Err(Failure::StepGuard { n });
        }
        x = if x & 1 == 0 { x >> 1 } else { (3 * x + 1) >> 1 };
        if x > peak {
            peak = x;
        }
        steps += 1;
    }
    Ok(Descent { steps, peak })
}

/// All four extremal fields are quantities of the Collatz map alone, with no
/// dependence on the sieve exponent k. That is deliberate: it makes "the
/// answer must not change when k changes" a check the self-test can run, and
/// fail.
struct RangeStats {
    checked: u64,
    sieve_resolved: u64,
    slow_path: u64,
    /// max over the range of sigma(n) = min{ j >= 1 : T^j(n) < n }
    max_sigma: u64,
    max_sigma_at: u64,
    /// the n maximising peak(n)/n, where peak is the largest value seen before
    /// the first descent below n; stored as a fraction to avoid floating point
    max_expansion_peak: u128,
    max_expansion_at: u64,
}

impl RangeStats {
    fn new() -> Self {
        RangeStats {
            checked: 0,
            sieve_resolved: 0,
            slow_path: 0,
            max_sigma: 0,
            max_sigma_at: 0,
            max_expansion_peak: 0,
            max_expansion_at: 0,
        }
    }
    /// Ties are broken towards the smaller n so that the result is independent
    /// of the order chunks happen to be scheduled and finish in.
    fn offer_sigma(&mut self, n: u64, sigma: u64) {
        if self.max_sigma_at == 0
            || sigma > self.max_sigma
            || (sigma == self.max_sigma && n < self.max_sigma_at)
        {
            self.max_sigma = sigma;
            self.max_sigma_at = n;
        }
    }
    fn offer_expansion(&mut self, n: u64, peak: u128) {
        if self.max_expansion_at == 0 {
            self.max_expansion_peak = peak;
            self.max_expansion_at = n;
            return;
        }
        let lhs = peak * self.max_expansion_at as u128;
        let rhs = self.max_expansion_peak * n as u128;
        if lhs > rhs || (lhs == rhs && n < self.max_expansion_at) {
            self.max_expansion_peak = peak;
            self.max_expansion_at = n;
        }
    }
    fn merge(&mut self, o: &RangeStats) {
        self.checked += o.checked;
        self.sieve_resolved += o.sieve_resolved;
        self.slow_path += o.slow_path;
        if o.max_sigma_at != 0 {
            self.offer_sigma(o.max_sigma_at, o.max_sigma);
        }
        if o.max_expansion_at != 0 {
            self.offer_expansion(o.max_expansion_at, o.max_expansion_peak);
        }
    }
}

/// Verify descent for every odd n in [lo, hi]. Even n are excluded on purpose:
/// T(n) = n/2 < n holds for every even n by definition of the map, so they
/// carry no information. This is stated in the report, not hidden here.
///
/// The k-step jump is used ONLY as a filter. Whenever it does not settle the
/// question, the trajectory is re-walked from n itself rather than from the
/// jump: the trajectory may dip below n and rise again inside the first k
/// steps, so counting `k + (steps from the jump)` would not be sigma(n).
fn verify_range(t: &Tables, lo: u64, hi: u64) -> Result<RangeStats, Failure> {
    let mut st = RangeStats::new();
    let mut n = if lo % 2 == 0 { lo + 1 } else { lo };
    if n < 3 {
        n = 3;
    }
    while n <= hi {
        let r = (n & t.mask) as usize;
        let q = (n >> t.k) as u128;
        let jump = q * t.pow3[r] as u128 + t.tail[r] as u128;
        st.checked += 1;
        if jump < n as u128 {
            st.sieve_resolved += 1;
        } else {
            st.slow_path += 1;
            let d = descend_below(n, n as u128)?;
            st.offer_sigma(n, d.steps);
            st.offer_expansion(n, d.peak);
        }
        n += 2;
    }
    Ok(st)
}

// ---------------------------------------------------------------------------
// Records mode — standard map C, full trajectory to 1
// ---------------------------------------------------------------------------

fn full_trajectory(n: u64) -> Result<(u64, u128), Failure> {
    let mut x = n as u128;
    let mut steps: u64 = 0;
    let mut peak = x;
    while x != 1 {
        if x > VALUE_GUARD {
            return Err(Failure::ValueGuard { n, at: x });
        }
        if steps >= STEP_GUARD {
            return Err(Failure::StepGuard { n });
        }
        x = if x & 1 == 0 { x >> 1 } else { 3 * x + 1 };
        if x > peak {
            peak = x;
        }
        steps += 1;
    }
    Ok((steps, peak))
}

// ---------------------------------------------------------------------------
// Self-test
// ---------------------------------------------------------------------------

fn self_test() -> Result<(), String> {
    // 1. Hand-checkable trajectories under the standard map.
    //    n=27 has delay 111 and peak 9232; n=1 has delay 0.
    for &(n, delay, peak) in &[
        (1u64, 0u64, 1u128),
        (2, 1, 2),
        (3, 7, 16),
        (6, 8, 16),
        (7, 16, 52),
        (27, 111, 9232),
        (97, 118, 9232),
        (871, 178, 190996),
        (6171, 261, 975400),
    ] {
        let (d, p) = full_trajectory(n).map_err(|e| format!("{:?}", e))?;
        if d != delay || p != peak {
            return Err(format!(
                "trajectory mismatch at n={n}: got (delay={d}, peak={p}), want (delay={delay}, peak={peak})"
            ));
        }
    }

    // 2. Table identity: T^k(q*2^k + r) == q*3^a(r) + T^k(r), checked against a
    //    direct k-step simulation of the full number. This is the only place
    //    the congruence structure is trusted, so it is tested directly.
    for k in [1u32, 4, 9, 13] {
        let t = build_tables(k);
        for n in [1u64, 2, 3, 27, 255, 4096, 100003, 987654321, u32::MAX as u64] {
            let mut x = n as u128;
            let mut a = 0u32;
            for _ in 0..k {
                if x & 1 == 0 {
                    x >>= 1;
                } else {
                    x = (3 * x + 1) >> 1;
                    a += 1;
                }
            }
            let r = (n & t.mask) as usize;
            let predicted = (n >> k) as u128 * t.pow3[r] as u128 + t.tail[r] as u128;
            if predicted != x {
                return Err(format!(
                    "k-step identity failed: k={k} n={n} predicted={predicted} direct={x}"
                ));
            }
            if t.odd_steps[r] as u32 != a {
                return Err(format!(
                    "odd-step count failed: k={k} n={n} table={} direct={a}",
                    t.odd_steps[r]
                ));
            }
        }
    }

    // 3. Sieve independence. Every reported quantity is a property of the
    //    Collatz map, so changing k may change only HOW MUCH WORK is done, and
    //    never WHAT IS REPORTED. k=1 is effectively no sieve at all, so this
    //    also pins the fast path against a near-naive walk.
    let mut baseline: Option<(u64, u64, u64, u128, u64)> = None;
    for k in [1u32, 3, 7, 11, 16] {
        let t = build_tables(k);
        let st = verify_range(&t, 3, 300_000).map_err(|e| format!("k={k}: {:?}", e))?;
        if st.sieve_resolved + st.slow_path != st.checked {
            return Err(format!("k={k}: sieve/slow accounting does not sum to checked"));
        }
        let got = (
            st.checked,
            st.max_sigma,
            st.max_sigma_at,
            st.max_expansion_peak,
            st.max_expansion_at,
        );
        match baseline {
            None => baseline = Some(got),
            Some(b) => {
                if b != got {
                    return Err(format!(
                        "sieve k={k} changed a reported quantity: {:?} vs baseline {:?}",
                        got, b
                    ));
                }
            }
        }
    }
    // The 300000 range must actually exercise the slow path at every k tested,
    // otherwise check 3 above compares nothing.
    {
        let t = build_tables(16);
        let st = verify_range(&t, 3, 300_000).map_err(|e| format!("{:?}", e))?;
        if st.slow_path == 0 {
            return Err("self-test range never reached the iterative path".to_string());
        }
        // sigma(27) = 59 under the shortcut map; 27 is the classic small start
        // whose descent is long, and it lies inside the tested range.
        let d = descend_below(27, 27).map_err(|e| format!("{:?}", e))?;
        if d.steps != 59 || d.peak != 4616 {
            return Err(format!(
                "shortcut-map descent of 27 is (steps={}, peak={}), expected (59, 4616)",
                d.steps, d.peak
            ));
        }
    }

    // 4. The guards must actually be reachable. A guard that cannot trip is
    //    not a guard. `descend_below` is called with a start above VALUE_GUARD.
    match descend_below(3, VALUE_GUARD + 1) {
        Err(Failure::ValueGuard { .. }) => {}
        other => return Err(format!("VALUE_GUARD did not trip: {:?}", other.map(|d| d.steps))),
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

fn arg_u64(args: &HashMap<String, String>, key: &str, default: u64) -> u64 {
    args.get(key)
        .map(|v| v.replace('_', "").parse::<u64>().unwrap_or_else(|_| panic!("bad --{key}")))
        .unwrap_or(default)
}

fn main() {
    let argv: Vec<String> = env::args().collect();
    let mut flags: Vec<String> = Vec::new();
    let mut kv: HashMap<String, String> = HashMap::new();
    let mut i = 1;
    while i < argv.len() {
        let a = &argv[i];
        if let Some(name) = a.strip_prefix("--") {
            if i + 1 < argv.len() && !argv[i + 1].starts_with("--") {
                kv.insert(name.to_string(), argv[i + 1].clone());
                i += 2;
                continue;
            }
            flags.push(name.to_string());
        }
        i += 1;
    }

    if flags.iter().any(|f| f == "self-test") {
        match self_test() {
            Ok(()) => {
                println!("{{\"mode\":\"self-test\",\"ok\":true}}");
            }
            Err(e) => {
                println!("{{\"mode\":\"self-test\",\"ok\":false,\"error\":{:?}}}", e);
                std::process::exit(1);
            }
        }
        return;
    }

    if kv.contains_key("trace") {
        let n = arg_u64(&kv, "trace", 1);
        match full_trajectory(n) {
            Ok((d, p)) => println!(
                "{{\"mode\":\"trace\",\"ok\":true,\"n\":{n},\"delay\":{d},\"peak\":{p}}}"
            ),
            Err(e) => {
                println!("{{\"mode\":\"trace\",\"ok\":false,\"n\":{n},\"error\":\"{:?}\"}}", e);
                std::process::exit(1);
            }
        }
        return;
    }

    if kv.contains_key("records") {
        let hi = arg_u64(&kv, "records", 1_000_000);
        let threads = arg_u64(&kv, "threads", 16).max(1) as usize;
        run_records(hi, threads);
        return;
    }

    let from = arg_u64(&kv, "from", 3);
    let to = arg_u64(&kv, "to", 1_000_000);
    let k = arg_u64(&kv, "sieve", 20) as u32;
    let threads = arg_u64(&kv, "threads", 16).max(1) as usize;
    run_verify(from, to, k, threads);
}

fn run_verify(from: u64, to: u64, k: u32, threads: usize) {
    let t0 = Instant::now();
    let build0 = Instant::now();
    let tables = build_tables(k);
    let build_ms = build0.elapsed().as_millis();
    let survivors = (0..(1usize << k))
        .filter(|&r| tables.pow3[r] as u128 >= (1u128 << k))
        .count();

    let chunk: u64 = 1 << 22;
    let next = AtomicU64::new(from);
    let out: Mutex<(RangeStats, Vec<String>)> = Mutex::new((RangeStats::new(), Vec::new()));

    std::thread::scope(|s| {
        for _ in 0..threads {
            s.spawn(|| {
                let mut local = RangeStats::new();
                let mut errs: Vec<String> = Vec::new();
                loop {
                    let lo = next.fetch_add(chunk, Ordering::Relaxed);
                    if lo > to {
                        break;
                    }
                    let hi = (lo + chunk - 1).min(to);
                    match verify_range(&tables, lo, hi) {
                        Ok(st) => local.merge(&st),
                        Err(e) => errs.push(format!("{:?}", e)),
                    }
                }
                let mut g = out.lock().unwrap();
                g.0.merge(&local);
                g.1.extend(errs);
            });
        }
    });

    let (st, errs) = out.into_inner().unwrap();
    let secs = t0.elapsed().as_secs_f64();
    let ok = errs.is_empty();
    println!(
        "{{\"mode\":\"verify\",\"ok\":{ok},\"from\":{from},\"to\":{to},\"sieve_k\":{k},\
\"threads\":{threads},\"table_build_ms\":{build_ms},\"sieve_survivor_residues\":{survivors},\
\"odd_starts_checked\":{},\"resolved_by_one_k_step_jump\":{},\"needed_iteration\":{},\
\"max_sigma\":{},\"max_sigma_at\":{},\"max_expansion_peak\":{},\"max_expansion_at\":{},\
\"elapsed_s\":{:.3},\"failures\":{:?}}}",
        st.checked,
        st.sieve_resolved,
        st.slow_path,
        st.max_sigma,
        st.max_sigma_at,
        st.max_expansion_peak,
        st.max_expansion_at,
        secs,
        errs
    );
    if !ok {
        std::process::exit(1);
    }
}

fn run_records(hi: u64, threads: usize) {
    let t0 = Instant::now();
    let chunk: u64 = 1 << 20;
    let next = AtomicU64::new(1);
    // (n, delay, peak) that are records within their own chunk
    let out: Mutex<(Vec<(u64, u64, u128)>, Vec<String>)> = Mutex::new((Vec::new(), Vec::new()));

    std::thread::scope(|s| {
        for _ in 0..threads {
            s.spawn(|| {
                let mut cand: Vec<(u64, u64, u128)> = Vec::new();
                let mut errs: Vec<String> = Vec::new();
                loop {
                    let lo = next.fetch_add(chunk, Ordering::Relaxed);
                    if lo > hi {
                        break;
                    }
                    let end = (lo + chunk - 1).min(hi);
                    let (mut bd, mut bp) = (0u64, 0u128);
                    for n in lo..=end {
                        match full_trajectory(n) {
                            Ok((d, p)) => {
                                // chunk-local record in either statistic; the
                                // serial pass below applies the global filter.
                                if d > bd || p > bp {
                                    cand.push((n, d, p));
                                    if d > bd {
                                        bd = d;
                                    }
                                    if p > bp {
                                        bp = p;
                                    }
                                }
                            }
                            Err(e) => errs.push(format!("{:?}", e)),
                        }
                    }
                }
                let mut g = out.lock().unwrap();
                g.0.extend(cand);
                g.1.extend(errs);
            });
        }
    });

    let (mut cand, errs) = out.into_inner().unwrap();
    cand.sort_by_key(|c| c.0);
    let mut delay_records: Vec<(u64, u64)> = Vec::new();
    let mut peak_records: Vec<(u64, u128)> = Vec::new();
    let (mut bd, mut bp) = (0u64, 0u128);
    let mut first = true;
    for (n, d, p) in cand {
        if first || d > bd {
            delay_records.push((n, d));
            bd = d;
        }
        if first || p > bp {
            peak_records.push((n, p));
            bp = p;
        }
        first = false;
    }
    let ok = errs.is_empty();
    let fmt2 = |v: &Vec<(u64, u64)>| {
        v.iter().map(|(a, b)| format!("[{a},{b}]")).collect::<Vec<_>>().join(",")
    };
    let fmt2b = |v: &Vec<(u64, u128)>| {
        v.iter().map(|(a, b)| format!("[{a},{b}]")).collect::<Vec<_>>().join(",")
    };
    println!(
        "{{\"mode\":\"records\",\"ok\":{ok},\"to\":{hi},\"elapsed_s\":{:.3},\
\"delay_records\":[{}],\"peak_records\":[{}],\"failures\":{:?}}}",
        t0.elapsed().as_secs_f64(),
        fmt2(&delay_records),
        fmt2b(&peak_records),
        errs
    );
    if !ok {
        std::process::exit(1);
    }
}
