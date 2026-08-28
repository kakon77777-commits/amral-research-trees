#!/usr/bin/env python3
"""Recheck of Hard-Zeta Phase II Round A-U.2d.6 (source item 52).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Farey-Order Entropy Collision* (v0.1, 2026-08-13).
21 numbered results across 19 sections; ships a checker, its report, a constants
frontier, a source-validation record and a stdout transcript.

## What is decidable here, and it is a lot

Three parts of this round are pure arithmetic or pure combinatorics, and none of
them mentions a surviving orbit:

**Section 3 — the binary bridge.** `C(d(w)) = B_w` is an identity between a
functional on a binary word and the accelerated affine numerator, and
`B_uv = 3^|v| B_u + 2^p B_v` is its concatenation law. The normalized correction
`c(w) = B_w/3^g = (1/3) sum 2^(P_j)/3^j` is **rational**, so it is compared as a
Fraction and not as a float.

**Section 5 — the capacity count.** `#W_{p,g} = binom(p-1,g-1)/g = binom(p,g)/p`
for coprime `p, g` is a closed form for a set that can simply be **enumerated**.
Formula against enumeration is the most decisive check available anywhere in this
sweep: it needs no tolerance and no sampling.

**Section 6 — the B-to-B class.** Given a destination `z = 3 (mod 4)`, the source
class tightens from item 51's `2^(p+1)` to `2^(p+2)`, and the separation from
`2*3^g` to `4*3^g`. That is one extra bit, and one extra bit is exactly the kind
of claim that is either right or off by a factor of two.

## Both directions, again

RUN-033 established that a residue-class claim needs members drawn from the class
**at which the code was never observed** to realize it, or the check passes on a
class twice too large. That matters more here than there, because the whole point
of section 6 is a factor of two.

## The continued fractions the report publishes

The checker prints 30 partial quotients of `beta` and of `theta`. The first 16 of
`beta` are the terms RUN-029 certified by integer comparison alone. `theta` is
**not** `1/beta` -- the round defines `theta = beta - 1` at section 9 -- so its CF
must be `[0] + beta_cf[1:]`, which is checked rather than assumed. Reading the
definition is what stopped that becoming a finding against correct arithmetic.

Usage:
  python code/src52_farey_entropy.py --bundle DIR [--limit N] [--trials N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
import sys
from fractions import Fraction

PAPER = "Hard_Zeta_Phase_II_Round_AU2d6_Farey_Order_Entropy_Collision_v0.1.md"
CONSTANTS = "Hard_Zeta_AU2d6_constants_frontier.json"
CHECKER_REPORT = "Hard_Zeta_AU2d6_checker_report.json"
CHECKER_STDOUT = "checker_stdout.txt"
VALIDATION = "SOURCE_VALIDATION_AU2d6.json"

#: the partial quotients of log_2 3 certified at RUN-029 by comparing 2^A with
#: 3^B and nothing else. Sixteen is where that certification stopped, measured.
CERTIFIED_BETA_CF = (1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def run_code(x: int, g: int) -> tuple[tuple[int, ...], int]:
    code, y = [], x
    for _ in range(g):
        t = 3 * y + 1
        a = v2(t)
        code.append(a)
        y = t >> a
    return tuple(code), y


def numerator_of(code: tuple[int, ...]) -> tuple[int, int]:
    """(B_w, p) for an accelerated exponent code."""
    g = len(code)
    b, partial = 0, 0
    for j in range(g):
        b += 3 ** (g - 1 - j) * (1 << partial)
        partial += code[j]
    return b, partial


def binary_word(code: tuple[int, ...]) -> list[int]:
    """d(w): length p, ones at positions P_{j-1}+1 (1-indexed)."""
    b, p = numerator_of(code)
    word = [0] * p
    partial = 0
    for a in code:
        word[partial] = 1
        partial += a
    return word


def functional(word: list[int]) -> int:
    """C(d) = sum over ones at position i of 2^(i-1) * 3^(ones strictly right)."""
    total = 0
    ones_right = sum(word)
    for i, bit in enumerate(word, start=1):
        if bit:
            ones_right -= 1
            total += (1 << (i - 1)) * 3 ** ones_right
    return total


def normalized(code: tuple[int, ...]) -> Fraction:
    """c(w) = (1/3) sum_{j<g} 2^(P_j)/3^j, exactly."""
    total = Fraction(0)
    partial = 0
    for j in range(len(code)):
        total += Fraction(1 << partial, 3 ** j)
        partial += code[j]
    return total / 3


# ---------------------------------------------------------------------------

def check_exact_bridge(trials: int, seed: int) -> dict:
    rng = random.Random(seed)
    bridge_bad = concat_bad = normal_bad = concat_c_bad = 0
    checked = 0
    for _ in range(trials):
        g = rng.randint(1, 8)
        code = tuple(rng.randint(1, 6) for _ in range(g))
        b, p = numerator_of(code)
        checked += 1
        if functional(binary_word(code)) != b:                     # Theorem 3.2
            bridge_bad += 1
        if normalized(code) != Fraction(b, 3 ** g):                # Corollary 3.3
            normal_bad += 1
        h = rng.randint(1, 6)
        second = tuple(rng.randint(1, 6) for _ in range(h))
        bv, _ = numerator_of(second)
        buv, _ = numerator_of(code + second)
        if buv != 3 ** h * b + (1 << p) * bv:                      # Theorem 3.4
            concat_bad += 1
        # c(uv) = c(u) + 2^(-A(u)) c(v), and 2^(-A(u)) = 2^p / 3^g exactly
        if normalized(code + second) != normalized(code) + Fraction(1 << p, 3 ** g) * normalized(second):
            concat_c_bad += 1
    return {
        "trials": checked,
        "bridge_violations_C_of_d_equals_B": bridge_bad,
        "normalized_correction_violations": normal_bad,
        "concatenation_violations_on_B": concat_bad,
        "concatenation_violations_on_c": concat_c_bad,
    }


def enumerate_capacity(p: int, g: int) -> int:
    """|W_{p,g}| by brute force: positive compositions with P_j <= j*p/g."""
    count = 0

    def walk(j: int, used: int, partial: int) -> None:
        nonlocal count
        if j == g:
            if used == p:
                count += 1
            return
        remaining = g - j
        for a in range(1, p - used - (remaining - 1) + 1):
            nxt = partial + a
            if j + 1 < g and nxt * g > (j + 1) * p:
                break
            walk(j + 1, used + a, nxt)

    walk(0, 0, 0)
    return count


def check_capacity(report: dict) -> dict:
    beta = Fraction(1584962500721156, 10 ** 15)      # a rational just under log2 3
    rows, formula_bad, enum_bad = [], [], []
    # The window has to reach the pairs the shipped report uses. Stopping at
    # g = 8 capped the largest enumerated class at 30, which is too small to
    # separate binom(p,g)/p from anything else it might have been.
    for g in range(2, 14):
        for p in range(g + 1, 23):
            if math.gcd(p, g) != 1 or Fraction(p, g) >= beta:
                continue
            a = math.comb(p - 1, g - 1)
            b = math.comb(p, g)
            if a % g or b % p:
                formula_bad.append({"p": p, "g": g, "reason": "not divisible"})
                continue
            f1, f2 = a // g, b // p
            if f1 != f2:
                formula_bad.append({"p": p, "g": g, "binom_p1_g1_over_g": f1,
                                    "binom_p_g_over_p": f2})
            actual = enumerate_capacity(p, g)
            rows.append({"p": p, "g": g, "enumerated": actual, "formula": f1})
            if actual != f1:
                enum_bad.append(rows[-1])

    shipped, shipped_bad = [], []
    for ex in report.get("fixed_layer_capacity_examples", []):
        p, g = ex["p"], ex["g"]
        want = math.comb(p, g) // p
        ok = str(want) == str(ex["count"]) and math.comb(p, g) % p == 0
        shipped.append({"p": p, "g": g, "agrees": ok})
        if not ok:
            shipped_bad.append({"p": p, "g": g, "theirs": ex["count"],
                                "mine": str(want)})
    return {
        "pairs_enumerated": len(rows),
        "largest_pair": max(((r["p"], r["g"]) for r in rows), default=None),
        "largest_count": max((r["enumerated"] for r in rows), default=0),
        "formula_disagreements_between_the_two_forms": formula_bad,
        "enumeration_disagreements": enum_bad,
        "shipped_examples_checked": len(shipped),
        "shipped_examples_disagreeing": shipped_bad,
        "rows": rows[:12],
    }


def check_b2b(trials: int, seed: int) -> dict:
    """Theorem 6.1 and Corollary 6.2, in both directions."""
    rng = random.Random(seed + 7)
    class_bad = reverse_bad = sep_source_bad = sep_dest_bad = 0
    checked = reverse_checked = pairs = 0
    sharper_than_item51 = 0
    for _ in range(trials):
        x = 4 * rng.randrange(1, 2_000_000) + 3      # a B source: 3 mod 4
        g = rng.randint(1, 7)
        code, z = run_code(x, g)
        if z % 4 != 3:                                # the theorem's hypothesis
            continue
        b, p = numerator_of(code)
        checked += 1
        modulus = 1 << (p + 2)
        want = (pow(3, -g, modulus) * (3 * (1 << p) - b)) % modulus
        if x % modulus != want:
            class_bad += 1

        # both directions: members of the class the code was never seen at
        for step in (1, 2, 3):
            other = x + step * modulus
            reverse_checked += 1
            code2, z2 = run_code(other, g)
            if code2 != code or z2 % 4 != 3:
                reverse_bad += 1
        # separation, and that it is one bit sharper than item 51's 2^(p+1)
        m = rng.randint(1, 4)
        x2 = x + m * modulus
        code2, z2 = run_code(x2, g)
        if code2 == code and z2 % 4 == 3:
            pairs += 1
            if abs(x2 - x) < modulus:
                sep_source_bad += 1
            if abs(z2 - z) < 4 * 3 ** g or (z2 - z) % (4 * 3 ** g):
                sep_dest_bad += 1
            if modulus == 2 * (1 << (p + 1)):
                sharper_than_item51 += 1
    return {
        "codes_with_a_B_destination": checked,
        "class_violations": class_bad,
        "class_members_checked_in_reverse": reverse_checked,
        "class_members_failing_the_code_or_the_residue": reverse_bad,
        "repeated_code_pairs": pairs,
        "source_gap_below_2^(p+2)": sep_source_bad,
        "destination_gap_not_a_multiple_of_4*3^g": sep_dest_bad,
        "pairs_where_the_modulus_is_exactly_twice_item_51's": sharper_than_item51,
    }


def check_continued_fractions(report: dict) -> dict:
    beta_cf = report.get("beta_continued_fraction_first_30", [])
    theta_cf = report.get("theta_continued_fraction_first_30", [])
    certified = list(CERTIFIED_BETA_CF)
    expected_theta = [0] + beta_cf[1:len(theta_cf)] if beta_cf else []

    def value(cf: list[int], n: int) -> Fraction:
        v = Fraction(cf[n - 1])
        for a in reversed(cf[:n - 1]):
            v = a + 1 / v
        return v

    beta_v = value(beta_cf, 20) if len(beta_cf) >= 20 else None
    theta_v = value(theta_cf, 20) if len(theta_cf) >= 20 else None
    return {
        "beta_terms_published": len(beta_cf),
        "beta_first_16_match_the_certified_terms": beta_cf[:16] == certified,
        "certified_terms": certified,
        "theta_is_defined_as_beta_minus_one_in_the_round": True,
        "theta_cf_equals_zero_then_beta_cf_shifted": theta_cf == expected_theta,
        "theta_plus_one_equals_beta_as_rationals":
            (beta_v is not None and theta_v is not None
             and theta_v + 1 == beta_v),
        "theta_is_not_one_over_beta":
            (beta_v is not None and theta_v is not None and theta_v != 1 / beta_v),
    }


def check_orbit_carryover(limit: int) -> dict:
    """Item 51's `y = 3 (mod 4)`, which section 6 builds on. Re-verified here."""
    sources = violations = 0
    for start in range(3, limit + 1, 2):
        y, values, word = start, [start], []
        while y != 1 and len(word) < 4000:
            t = 3 * y + 1
            a = v2(t)
            word.append(a)
            y = t >> a
            values.append(y)
        K, run = [0], 0
        for q in word:
            run += q
            K.append(run)
        n = len(word)
        out: list[int | None] = [None] * (n + 1)
        stack: list[int] = []
        for u in range(n + 1):
            while stack and Fraction(3) ** (u - stack[-1]) < Fraction(2) ** (K[u] - K[stack[-1]]):
                out[stack.pop()] = u
            stack.append(u)
        for s, end in enumerate(out):
            if end is None or s >= n or end - s < 2:
                continue
            sources += 1
            if values[s] % 4 != 3:
                violations += 1
    return {"sources_with_L_at_least_2": sources, "not_3_mod_4": violations}


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    if "artifact_sha256_before_manifest" in validation:
        listed = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
    elif isinstance(validation.get("files"), list):
        listed = {rec["file"]: rec for rec in validation["files"]}
        shape = "list of file records (items 51, 52)"
    else:
        listed, shape = {}, "UNRECOGNISED"
    present = {p.name for p in bundle.iterdir() if p.is_file()}
    verified, mismatched, absent = 0, [], []
    for name, rec in sorted(listed.items()):
        path = bundle / name
        if not path.exists():
            absent.append(name)
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:
            verified += 1
        else:
            mismatched.append(name)
    report = (bundle / CHECKER_REPORT).read_bytes()
    stdout = (bundle / CHECKER_STDOUT).read_bytes()
    return {
        "validation_record_shape": shape,
        "files_listed": len(listed), "verified": verified,
        "mismatched": mismatched, "listed_but_absent": absent,
        "present_but_not_covered": sorted(present - set(listed)),
        "the_only_uncovered_file_is_the_record_itself":
            sorted(present - set(listed)) == [VALIDATION],
        "checker_exit_code": validation.get("checker_exit_code"),
        "validation_passed": validation.get("validation_passed"),
        "errors_listed": len(validation.get("errors", [])),
        "report_and_stdout_byte_identical": report == stdout,
        "stdout_is_the_report_plus": (stdout[len(report):].decode("utf-8", "replace")
                                      if stdout.startswith(report) else None),
    }


def check_constants(constants: dict) -> dict:
    import struct
    rho = Fraction("4.1164")
    exact = {
        "old_congestion_power": rho / (rho + 1),
        "disjoint_backbone_power": 1 / (1 + 1 / (rho + 1)),
        "dense_overlap_required_power": 1 - 1 / (1 + 1 / (rho + 1)),
    }
    published = constants["inherited_constants"]

    def bits(x: float) -> int:
        return struct.unpack("<q", struct.pack("<d", x))[0]

    rows, drifted = {}, []
    for name, value in exact.items():
        if name not in published:
            continue
        drift = abs(bits(published[name]) - bits(float(value)))
        rows[name] = {"exact": "%d/%d" % (value.numerator, value.denominator),
                      "published": published[name],
                      "ulps_from_the_nearest_double": drift}
        if drift:
            drifted.append(name)
    return {"rows": rows, "off_by_at_least_one_ulp": drifted,
            "rho_star_agrees": published.get("rho_star") == 4.1164}


def check_their_claims(report: dict, r: dict) -> dict:
    eb, cap, b2b = r["exact_bridge"], r["capacity"], r["b_to_b"]
    mapping = {
        "B_w equals the Fernandez-Ibanez binary functional C(d(w)) exactly":
            eb["bridge_violations_C_of_d_equals_B"] == 0,
        "accelerated correction numerator concatenation identity":
            eb["concatenation_violations_on_B"] == 0
            and eb["concatenation_violations_on_c"] == 0,
        "exact rational-Catalan capacity #W_{p,g}=binom(p,g)/p for tested unit pairs":
            not cap["enumeration_disagreements"]
            and not cap["formula_disagreements_between_the_two_forms"],
        "B-anchor-to-B-anchor residue class modulo 2^(p+2) and repeated-code gaps":
            b2b["class_violations"] == 0
            and b2b["class_members_failing_the_code_or_the_residue"] == 0
            and b2b["source_gap_below_2^(p+2)"] == 0
            and b2b["destination_gap_not_a_multiple_of_4*3^g"] == 0,
    }
    stated = list(report.get("verified_claims", []))
    checked = {c: mapping[c] for c in stated if c in mapping}
    return {
        "claims_the_checker_states": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": [c for c in stated if c not in mapping],
        "the_checker_s_own_not_verified_list": report.get("not_verified", []),
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, type=pathlib.Path)
    ap.add_argument("--limit", type=int, default=2001)
    ap.add_argument("--trials", type=int, default=800)
    ap.add_argument("--seed", type=int, default=20260828)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    bundle = args.bundle
    constants = json.loads((bundle / CONSTANTS).read_text(encoding="utf-8"))
    shipped = json.loads((bundle / CHECKER_REPORT).read_text(encoding="utf-8"))
    paper = (bundle / PAPER).read_text(encoding="utf-8")

    rep: dict = {
        "round": "Hard-Zeta Phase II / Round A-U.2d.6",
        "source_item": 52,
        "exact_bridge": check_exact_bridge(args.trials, args.seed),
        "capacity": check_capacity(shipped),
        "b_to_b": check_b2b(args.trials, args.seed),
        "continued_fractions": check_continued_fractions(shipped),
        "orbit_carryover": check_orbit_carryover(args.limit),
        "constants": check_constants(constants),
        "artifacts": check_artifacts(bundle),
    }
    rep["their_claims"] = check_their_claims(shipped, rep)
    rep["scope_discipline"] = {
        "the round refuses a full contradiction":
            "no full contradiction" in constants.get("status", ""),
        "the checker names what it did not verify":
            len(shipped.get("not_verified", [])) >= 3,
        "the headroom telescope is still forbidden":
            any("rotation headroom" in s for s in constants.get("formal_no_go", [])),
        "the theta definition is in the paper":
            "\\theta=\\beta-1" in paper,
    }

    eb, cap, b2b = rep["exact_bridge"], rep["capacity"], rep["b_to_b"]
    cf, oc, cs = rep["continued_fractions"], rep["orbit_carryover"], rep["constants"]
    ar, tc, sd = rep["artifacts"], rep["their_claims"], rep["scope_discipline"]

    failures = []
    if eb["bridge_violations_C_of_d_equals_B"]:
        failures.append("the binary bridge C(d(w)) = B_w fails")
    if eb["normalized_correction_violations"]:
        failures.append("the normalized correction c(w) = B_w/3^g fails")
    if eb["concatenation_violations_on_B"] or eb["concatenation_violations_on_c"]:
        failures.append("the concatenation identity fails")
    if eb["trials"] < 100:
        failures.append("too few bridge trials to be a test")
    if cap["enumeration_disagreements"]:
        failures.append("the capacity formula disagrees with enumeration: %s"
                        % cap["enumeration_disagreements"])
    if cap["formula_disagreements_between_the_two_forms"]:
        failures.append("the two closed forms of the capacity disagree")
    if cap["pairs_enumerated"] < 10 or cap["largest_count"] < 100:
        failures.append("the capacity enumeration was too small to discriminate")
    if cap["shipped_examples_disagreeing"]:
        failures.append("a shipped capacity example does not recompute")
    if b2b["class_violations"] or b2b["class_members_failing_the_code_or_the_residue"]:
        failures.append("the B-to-B source class modulo 2^(p+2) fails")
    if b2b["class_members_checked_in_reverse"] < b2b["codes_with_a_B_destination"]:
        failures.append("the B-to-B class was not checked in both directions")
    if b2b["source_gap_below_2^(p+2)"] or b2b["destination_gap_not_a_multiple_of_4*3^g"]:
        failures.append("the B-to-B separation fails")
    if b2b["repeated_code_pairs"] < 20 or b2b["codes_with_a_B_destination"] < 50:
        failures.append("too few B-to-B cases to have tested section 6")
    if not cf["beta_first_16_match_the_certified_terms"]:
        failures.append("the published beta continued fraction disagrees with the "
                        "terms RUN-029 certified by integer comparison")
    if not cf["theta_cf_equals_zero_then_beta_cf_shifted"]:
        failures.append("the published theta continued fraction is not beta's "
                        "shifted, which is what theta = beta - 1 requires")
    if not cf["theta_plus_one_equals_beta_as_rationals"]:
        failures.append("theta + 1 != beta on the published expansions")
    if oc["not_3_mod_4"]:
        failures.append("item 51's 3 mod 4 result, which section 6 assumes, fails")
    if oc["sources_with_L_at_least_2"] < 500:
        failures.append("too few sources to have re-verified the 3 mod 4 carryover")
    if ar["validation_record_shape"] == "UNRECOGNISED":
        failures.append("the validation record is in an unknown shape")
    if ar["mismatched"] or ar["listed_but_absent"] or ar["verified"] < 5:
        failures.append("the validation record does not match its files")
    if tc["independently_contradicted"]:
        failures.append("a claim the checker states is contradicted: %s"
                        % tc["independently_contradicted"])
    if tc["independently_confirmed"] < 4:
        failures.append("too few of the checker's claims were independently checked")
    if not all(sd.values()):
        failures.append("scope discipline missing: %s"
                        % sorted(k for k, v in sd.items() if not v))

    findings = []
    if not ar["report_and_stdout_byte_identical"] and ar["stdout_is_the_report_plus"] is not None:
        findings.append(
            "`checker_stdout.txt` is the checker report plus %r and nothing else -- "
            "third bundle shipping the same content twice under two names, and the "
            "first where the two are not byte-identical. Items 50 and 51 shipped "
            "them identical; here one trailing newline separates them, which is "
            "enough to make a byte comparison say they differ and not enough to "
            "make them different documents."
            % ar["stdout_is_the_report_plus"])
    if cs["off_by_at_least_one_ulp"]:
        findings.append(
            "inherited constants drifting from the exact rational's nearest "
            "double: %s." % ", ".join(cs["off_by_at_least_one_ulp"]))
    else:
        findings.append(
            "the three inherited exponents are the **exact** nearest doubles of "
            "their rationals, as item 51's were and item 50's were not (RUN-032 "
            "measured 1 and 2 ulps there). The artifacts have stayed corrected.")

    rep["findings"] = findings
    rep["failures"] = failures
    rep["passed"] = not failures

    text = json.dumps(rep, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
