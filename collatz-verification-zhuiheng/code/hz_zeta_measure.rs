//! Measure the Hard-Zeta frontier Z_k(s) on a finite range.
//!
//! 數學戰士「墜衡」 / AMRAL Research Lab.
//! Subject: Neo.K, *Faithful Global Quantifier Compression* v0.1 §15–§16.
//!
//! The paper's §16 defines, for the shortcut map T and
//! sigma(n) = inf{ j >= 1 : T^j(n) < n },
//!
//!     E_k = { n >= 2 : sigma(n) > k },      Z_k(s) = sum_{n in E_k} n^{-s},
//!
//! and proves Collatz <=> Z_k(s) -> 0 for any fixed s > 1. The equivalence is a
//! theorem about an infinite sum. This program computes the part of that sum
//! lying in [2, N], which is not the same thing and is not claimed to be:
//!
//!     Z_k^[2,N](s)  <=  Z_k(s)  <=  Z_k^[2,N](s) + sum_{n > N} n^{-s}
//!
//! The right-hand tail is bounded rigorously by the caller. What comes out is a
//! two-sided bracket on a quantity nobody has yet written down numerically, plus
//! an explicit statement of the depth at which the bracket stops saying anything.
//!
//! Deliberately a SEPARATE implementation from `collatz_verify.rs`, with its own
//! walk, so the two can disagree. Its sigma is cross-checked against that engine
//! and against `collatz_ref.py`.
//!
//! Summation is Kahan-compensated. The terms arrive in decreasing order, which is
//! the order in which naive f64 accumulation loses the most, so the compensation
//! is doing real work here rather than decorating the code.
//!
//! Build:  rustc -O --edition 2021 code/hz_zeta_measure.rs -o build/hz_zeta_measure.exe
//! Usage:  hz_zeta_measure --to N --ks 1,2,4,... --s 2,3,4 [--threads T]
//!         hz_zeta_measure --self-test

use std::collections::BTreeMap;
use std::sync::mpsc;
use std::thread;

/// Values cannot legitimately reach here for the ranges this program is run on;
/// crossing it means the walk is wrong, not that the number is interesting.
const VALUE_GUARD: u128 = 1u128 << 120;

/// One shortcut-map step: T(n) = n/2 for even n, (3n+1)/2 for odd n.
#[inline(always)]
fn step(x: u128) -> u128 {
    if x & 1 == 0 {
        x >> 1
    } else {
        (3 * x + 1) >> 1
    }
}

/// sigma(n), capped: returns min(sigma(n), cap + 1).
///
/// A capped value of `cap + 1` means only "sigma(n) > cap", which is all the
/// caller needs — every k it asks about is <= cap.
fn sigma_capped(n: u128, cap: u64) -> u64 {
    let mut x = n;
    for j in 1..=cap {
        x = step(x);
        if x >= VALUE_GUARD {
            panic!("value guard tripped at n = {n}, step {j}");
        }
        if x < n {
            return j;
        }
    }
    cap + 1
}

/// Least j with 3^u < 2^j, for u = 0..=umax, exactly.
///
/// 3^u leaves u128 at u = 81, and comparing `3^u < 2^j` in a fixed width was the
/// first version's bug: the comparison was silently skipped past j = 127, so
/// tau_c was never found for the very starts that make this measurement
/// interesting. Base-2^32 limbs cost twenty lines and remove the ceiling.
fn crossing_table(umax: usize) -> Vec<u64> {
    let mut out = Vec::with_capacity(umax + 1);
    let mut limbs: Vec<u64> = vec![1];              // 3^u, base 2^32
    for _ in 0..=umax {
        let bits = {
            let top = limbs.len() - 1;
            (top as u64) * 32 + (64 - (limbs[top] as u64).leading_zeros() as u64)
        };
        out.push(bits);                              // 3^u < 2^bits, minimally
        let mut carry: u64 = 0;
        for l in limbs.iter_mut() {
            let v = *l * 3 + carry;
            *l = v & 0xFFFF_FFFF;
            carry = v >> 32;
        }
        if carry > 0 {
            limbs.push(carry);
        }
    }
    out
}

/// tau_c(n) = inf{ j >= 1 : 3^(u_j) < 2^j }, the coefficient stopping time.
///
/// Uses the crossing table: 3^u < 2^j exactly when j >= K[u].
fn tau_c(n: u128, kt: &[u64]) -> u64 {
    let mut x = n;
    let mut u: usize = 0;
    for j in 1..=1024u64 {
        if x & 1 == 1 {
            u += 1;
        }
        x = step(x);
        if x >= VALUE_GUARD {
            panic!("value guard tripped in tau_c at n = {n}, step {j}");
        }
        if j >= kt[u] {
            return j;
        }
    }
    panic!("tau_c({n}) exceeded 1024 steps");
}

/// Kahan-compensated accumulator.
#[derive(Clone, Copy)]
struct Kahan {
    sum: f64,
    c: f64,
}

impl Kahan {
    fn new() -> Self {
        Kahan { sum: 0.0, c: 0.0 }
    }
    #[inline(always)]
    fn add(&mut self, v: f64) {
        let y = v - self.c;
        let t = self.sum + y;
        self.c = (t - self.sum) - y;
        self.sum = t;
    }
    fn merge(&mut self, o: &Kahan) {
        self.add(o.sum);
        self.add(-o.c);
    }
}

struct Acc {
    ks: Vec<u64>,
    ss: Vec<f64>,
    /// count of n in E_k, per k
    counts: Vec<u64>,
    /// smallest n in E_k, per k (0 = none seen)
    mins: Vec<u64>,
    /// Z_k^[2,N](s), indexed [k][s]
    z: Vec<Vec<Kahan>>,
    max_sigma: u64,
    max_sigma_at: u64,
    scanned: u64,
}

impl Acc {
    fn new(ks: &[u64], ss: &[f64]) -> Self {
        Acc {
            ks: ks.to_vec(),
            ss: ss.to_vec(),
            counts: vec![0; ks.len()],
            mins: vec![0; ks.len()],
            z: vec![vec![Kahan::new(); ss.len()]; ks.len()],
            max_sigma: 0,
            max_sigma_at: 0,
            scanned: 0,
        }
    }

    #[inline]
    fn offer(&mut self, n: u64, sigma: u64) {
        self.scanned += 1;
        if self.max_sigma_at == 0 || sigma > self.max_sigma {
            self.max_sigma = sigma;
            self.max_sigma_at = n;
        }
        // sigma > k for the listed k, in increasing k, so once it fails it fails
        // for every larger k and the loop can stop.
        let nf = n as f64;
        for (i, &k) in self.ks.iter().enumerate() {
            if sigma <= k {
                break;
            }
            self.counts[i] += 1;
            if self.mins[i] == 0 {
                self.mins[i] = n;
            }
            for (j, &s) in self.ss.iter().enumerate() {
                self.z[i][j].add(nf.powf(-s));
            }
        }
    }

    fn merge(&mut self, o: &Acc) {
        self.scanned += o.scanned;
        if o.max_sigma_at != 0 && (self.max_sigma_at == 0 || o.max_sigma > self.max_sigma) {
            self.max_sigma = o.max_sigma;
            self.max_sigma_at = o.max_sigma_at;
        }
        for i in 0..self.ks.len() {
            self.counts[i] += o.counts[i];
            if o.mins[i] != 0 && (self.mins[i] == 0 || o.mins[i] < self.mins[i]) {
                self.mins[i] = o.mins[i];
            }
            for j in 0..self.ss.len() {
                let other = o.z[i][j];
                self.z[i][j].merge(&other);
            }
        }
    }
}

fn scan(lo: u64, hi: u64, ks: &[u64], ss: &[f64], cap: u64) -> Acc {
    let mut acc = Acc::new(ks, ss);
    for n in lo..hi {
        let s = sigma_capped(n as u128, cap);
        acc.offer(n, s);
    }
    acc
}

fn self_test() -> i32 {
    let mut bad = 0;
    // sigma by hand, from the definition, on values checkable by eye
    // 2 -> 1                      sigma = 1
    // 3 -> 5 -> 8 -> 4 -> 2       sigma = 4   (first value below 3 is 2)
    // 4 -> 2                      sigma = 1
    // 7 -> 11 -> 17 -> 26 -> 13 -> 20 -> 10 -> 5   sigma = 7
    for &(n, want) in &[(2u128, 1u64), (3, 4), (4, 1), (7, 7), (27, 59)] {
        let got = sigma_capped(n, 1000);
        if got != want {
            eprintln!("self-test: sigma({n}) = {got}, expected {want}");
            bad += 1;
        }
    }
    // the cap must report "greater than", never a wrong finite value.
    // This is the property whose misuse produced a meaningless `max_sigma` in
    // the first version: `cap + 1` is a bound, not a measurement, and nothing
    // downstream may present it as one.
    if sigma_capped(27, 10) != 11 {
        eprintln!("self-test: capped sigma(27) at cap 10 should be 11");
        bad += 1;
    }
    if sigma_capped(27, 59) != 59 {
        eprintln!("self-test: cap exactly at sigma should return sigma");
        bad += 1;
    }
    // the crossing table, against values checkable by hand
    let kt = crossing_table(200);
    for &(u, want) in &[(0usize, 1u64), (1, 2), (2, 4), (3, 5), (4, 7), (5, 8),
                        (6, 10), (7, 12), (8, 13)] {
        if kt[u] != want {
            eprintln!("self-test: crossing_table[{u}] = {}, expected {want}", kt[u]);
            bad += 1;
        }
    }
    // and past where 3^u leaves u128, where the first version stopped working
    if kt[81] != 129 || kt[100] != 159 || kt[200] != 317 {
        eprintln!("self-test: crossing table wrong past u128: {} {} {}",
                  kt[81], kt[100], kt[200]);
        bad += 1;
    }
    // Kahan must beat naive summation on a case built to break naive summation
    let mut k = Kahan::new();
    let mut naive = 0.0f64;
    k.add(1.0);
    naive += 1.0;
    for _ in 0..10_000_000 {
        k.add(1e-9);
        naive += 1e-9;
    }
    let exact = 1.0 + 10_000_000.0 * 1e-9;
    if (k.sum - exact).abs() >= (naive - exact).abs() {
        eprintln!(
            "self-test: Kahan ({}) did not beat naive ({}) against exact {}",
            k.sum, naive, exact
        );
        bad += 1;
    }
    if bad == 0 {
        println!("{{\"self_test\":\"ok\",\"cases\":19}}");
        0
    } else {
        println!("{{\"self_test\":\"FAILED\",\"failures\":{bad}}}");
        1
    }
}

fn main() {
    let argv: Vec<String> = std::env::args().collect();
    let mut opts: BTreeMap<String, String> = BTreeMap::new();
    let mut i = 1;
    while i < argv.len() {
        if let Some(name) = argv[i].strip_prefix("--") {
            if i + 1 < argv.len() && !argv[i + 1].starts_with("--") {
                opts.insert(name.to_string(), argv[i + 1].clone());
                i += 2;
            } else {
                opts.insert(name.to_string(), "1".to_string());
                i += 1;
            }
        } else {
            i += 1;
        }
    }

    if opts.contains_key("self-test") {
        std::process::exit(self_test());
    }

    if opts.contains_key("tau-records") {
        // Round 03-A §28-§30: m_k = min { n >= 2 : tau_c(n) > k }, the minimum
        // surviving coefficient anchor. It is determined entirely by the
        // tau_c RECORD holders, since m_k is the first n whose tau_c exceeds k
        // and any later n with a smaller tau_c can never be that first one.
        let to: u64 = opts.get("to").and_then(|v| v.parse().ok()).unwrap_or(1 << 32);
        let kt = crossing_table(1200);
        let mut best: u64 = 0;
        print!("{{\"tool\":\"hz_tau_records\",\"domain_hi\":{to},\"records\":[");
        let mut first = true;
        for n in 2..to {
            let t = tau_c(n as u128, &kt);
            if t > best {
                best = t;
                if !first {
                    print!(",");
                }
                first = false;
                print!("{{\"n\":{n},\"tau_c\":{t}}}");
            }
        }
        println!("]}}");
        return;
    }

    let to: u64 = opts
        .get("to")
        .and_then(|v| v.parse().ok())
        .unwrap_or(1u64 << 24);
    let ks: Vec<u64> = opts
        .get("ks")
        .map(|v| v.split(',').filter_map(|x| x.trim().parse().ok()).collect())
        .unwrap_or_else(|| vec![1, 2, 4, 8, 16, 32, 64]);
    let ss: Vec<f64> = opts
        .get("s")
        .map(|v| v.split(',').filter_map(|x| x.trim().parse().ok()).collect())
        .unwrap_or_else(|| vec![2.0, 3.0, 4.0]);
    let threads: u64 = opts
        .get("threads")
        .and_then(|v| v.parse().ok())
        .unwrap_or(16);

    let mut ks = ks;
    ks.sort_unstable();
    ks.dedup();
    // The walk cap must NOT be tied to max(ks). It was, in the first version, and
    // `max_sigma` then reported max(ks) + 1 for any range containing a harder
    // start — a number that says only "greater than the cap" while looking like a
    // measurement. Early exit is on descent, not on the cap, so a generous cap
    // costs almost nothing: it only extends the walk for the rare hard n.
    let cap: u64 = opts
        .get("sigma-cap")
        .and_then(|v| v.parse().ok())
        .unwrap_or_else(|| (*ks.last().unwrap() + 1).max(4096));
    if cap <= *ks.last().unwrap() {
        eprintln!("--sigma-cap must exceed the largest k, or E_k is undercounted");
        std::process::exit(2);
    }

    // domain is [2, to), matching the paper's n >= 2
    let lo = 2u64;
    let span = to.saturating_sub(lo);
    let chunk = (span + threads - 1) / threads.max(1);

    let (tx, rx) = mpsc::channel();
    let mut handles = Vec::new();
    for t in 0..threads {
        let a = lo + t * chunk;
        let b = (a + chunk).min(to);
        if a >= b {
            continue;
        }
        let ks = ks.clone();
        let ss = ss.clone();
        let tx = tx.clone();
        handles.push(thread::spawn(move || {
            let acc = scan(a, b, &ks, &ss, cap);
            tx.send(acc).expect("send");
        }));
    }
    drop(tx);

    let mut total = Acc::new(&ks, &ss);
    for acc in rx {
        total.merge(&acc);
    }
    for h in handles {
        h.join().expect("join");
    }

    print!(
        "{{\"tool\":\"hz_zeta_measure\",\"domain_lo\":{},\"domain_hi\":{},\"scanned\":{},\
\"max_sigma\":{},\"max_sigma_at\":{},\"sigma_cap\":{},\"rows\":[",
        lo, to, total.scanned, total.max_sigma, total.max_sigma_at, cap
    );
    for (i, &k) in ks.iter().enumerate() {
        if i > 0 {
            print!(",");
        }
        print!(
            "{{\"k\":{},\"count_E_k\":{},\"min_E_k\":{},\"z\":{{",
            k, total.counts[i], total.mins[i]
        );
        for (j, &s) in ss.iter().enumerate() {
            if j > 0 {
                print!(",");
            }
            print!("\"{}\":{:.17e}", s, total.z[i][j].sum);
        }
        print!("}}}}");
    }
    println!("]}}");
}
