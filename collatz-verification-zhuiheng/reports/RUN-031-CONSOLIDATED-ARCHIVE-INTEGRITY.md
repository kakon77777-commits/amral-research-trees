# RUN-031 — the consolidated archive: 964 files open at nine levels, 47 entries are byte-identical to what the sweep verified, and a checksum manifest certifies only the half that cannot change

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Collatz_OT_Series_Paper.zip` (source item 49) — a 17.5 MB consolidated archive of the source folder itself, 50 entries.
**Tools:** [`src49_archive_integrity.py`](../code/src49_archive_integrity.py) · [`src49_drill.py`](../code/src49_drill.py) · [`src49_emit_report_block.py`](../code/src49_emit_report_block.py)
**Logs:** [`src49-archive.json`](../data/gate-logs/src49-archive.json) · [`src49-drill.json`](../data/gate-logs/src49-drill.json)

**Result: the archive is faithful. Every one of its 47 entries that has a standalone counterpart is byte-identical to the item this sweep already verified, nothing has drifted, and all 964 files open at every one of nine nesting levels. Three findings, none of them about the Collatz work: it omits one item 33 seconds older than itself; half of it by volume is Riemann-zeta material that exists nowhere else in the source folder; and the integrity manifest those packs ship verifies perfectly while covering none of the files that actually changed between two shipped versions.**

---

## A third kind of object, and a third kind of check

Items 1–47 asserted mathematics, and the question was whether it held. Item 48
asserted what the other documents say, and the question was fidelity. This one
asserts nothing at all — it is a **container**.

So the failure modes are different, and none of them is mathematical:

- an entry that has **drifted** from the standalone item the sweep verified;
- an item the archive **silently omits**;
- content that exists **only inside it**, which an item-by-item sweep would never
  meet;
- a nested structure that cannot be **opened all the way down**;
- and an integrity manifest that **verifies perfectly while covering the wrong
  half** of what it ships.

The last one is what this archive does, and it is the finding worth keeping.

## Nothing has drifted, and everything opens

Of 50 entries, **47** have a standalone counterpart in the source folder, and
every one of them is **byte-identical** — checked against both the hash this tree
recorded when it swept the item and the file on disk now, because those answer
different questions. **Zero** differ.

The archive is nine levels deep in places. Following every nested zip to the
bottom reaches **964 files** through **49** nested archives, and **none** failed
to open. For a hand-assembled 17.5 MB container that is worth stating plainly,
because the alternative — a truncated inner zip nobody ever opened — is exactly
the kind of thing that stays invisible until someone needs the file.

## Finding 1 — a checksum manifest that certifies only what cannot change

Two entries ship their own `SHA256SUMS.txt`. That is an integrity claim the
artifact makes about itself, so the right response is to compute the hashes
independently and compare.

**All 16 listed hashes verify. Zero mismatches.** The manifest is telling the
truth about everything it mentions.

What it mentions is the problem. It lists **8 files of 16** in one pack and
**8 of 18** in the other, and the eight are the third-party PDFs — papers by other
authors, which by construction will never change. The uncovered remainder is the
part that is actually the work: `scripts/reproduce_constants.py`,
`scripts/ceiling_law256_constants.py`, `sources.json`, and four sets of notes.

The measurement that turns "incomplete" into a finding is this. Between the two
shipped versions of the same pack, **3 files differ** — two added
(`notes/04_Reconstructing_68_185_Ceiling.md`,
`scripts/ceiling_law256_constants.py`) and one changed (`README.md`) — and the
manifest covers **none** of them. It is **byte-identical across both versions**:
the pack was revised and its integrity manifest was not.

So the manifest verifies forever, and would have verified just as perfectly if
every script in the pack had been replaced. **An integrity claim that only ever
certifies the immutable files is a checksum on the part nobody would doubt** —
the same shape as RUN-028's guard that could not fail, wearing a hash.

A second pack takes it further: it nests its own predecessor **nine levels deep**,
v11 inside v10 inside v9 down to v3, **83 files** reachable only by opening every
one in turn — and **no level ships a manifest at all**.

## Finding 2 — half the archive is a different research line

**50.0%** of the archive by uncompressed bytes — 8.9 MB in 3 entries — is `CPL_`
material: Riemann-zeta pair-correlation research packs, containing papers on
Montgomery's theorem, zeta zeros on the critical line, and proportions of simple
zeros. It is not Collatz work, and it **exists nowhere else in the source folder**.

That matters procedurally rather than mathematically. This sweep walks the folder
one standalone item at a time; three entries are reachable only by opening the
consolidated archive. Had this item been treated as "a container of things
already checked", they would never have been seen at all.

**They are not verified here, and this run does not pretend otherwise.** They
belong to a different line and a different literature; what was checked is their
integrity, not their content.

## Finding 3 — the archive omits an item 33 seconds older than itself

Of **48** source items older than the archive, it contains **47**. The one it
leaves out is `Hard_Zeta_Collatz_New_Chat_Handoff_v1.0.zip` — item 48, the
bootstrap document RUN-030 examined — written **33 seconds** before the archive
was built.

Thirty-three seconds is the sort of gap that reads as a race rather than a
decision, and the consequence is small but specific: a reader who takes this
archive as the state of the folder gets everything except the document that tells
a new conversation how to start.

## What the archive shares with this tree's own copy

RUN-002 archived the OT Series byte-exact as `collatz-ot-series-neok/`, in its
SSSP-Repaired edition. This archive carries the working documents. Of its 8
markdown entries, **3 are byte-identical** to files in that archive and 5 are not
— which is what a repaired edition should look like, and is reported as a
measurement rather than as a defect.

---

<!-- BEGIN GENERATED measured block: python code/src49_emit_report_block.py -->

**What the shipped manifests cover.** Each pack's own `SHA256SUMS.txt`, verified by recomputing the hashes rather than by running whatever produced the list:

| pack | files | listed | verified | mismatched | uncovered |
| --- | --- | --- | --- | --- | --- |
| `67_25_Research_Pack` | `16` | `8` | `8` | `0` | `7` |
| `67_25_Research_Pack_v2` | `18` | `8` | `8` | `0` | `9` |

Both manifests share one sha256 (`fa25b9d3fa1409ae`) — the pack was revised and the manifest was not. Between the two versions `3` files differ (`notes/04_Reconstructing_68_185_Ceiling.md`, `scripts/ceiling_law256_constants.py`, `README.md`), and `0` of them are covered.

| what | measured against | value |
| --- | --- | --- |
| archive entries | the top level of the container | `50` |
| …byte-identical to the standalone item the sweep verified | the recorded hash **and** the file on disk | `47` |
| …**that have drifted** | must be zero | `0` |
| …with no standalone counterpart anywhere in the folder | reachable only by opening this archive | `3` |
| source items older than the archive | of which present: 47 | `48` |
| …omitted | named below if any | `1` |
| files reachable through every nesting level | 49 nested archives, deepest nesting 9 | `964` |
| …**that could not be opened** | must be zero | `0` |
| shipped checksum entries verified | of 16 listed, across 2 packs | `16` |
| …**mismatched** | must be zero | `0` |
| …files present but not covered by any manifest | the scripts, notes and sources | `16` |
| version-chain depth | each version nesting its predecessor | `9` |
| …levels shipping a manifest | of 9 | `0` |
| …files reachable only through that chain |  | `83` |
| share of the archive that is `CPL_` material | 3 entries, 8913130 of 17812870 uncompressed bytes | `50.0%` |
| markdown entries byte-identical to this tree's own OT archive | of 8, against 57 archived files | `3` |
| defects planted / caught by the check named for each | 2 of the entries are robustness properties; 0 malformed | `14 / 14` |

**Omitted.** `Hard_Zeta_Collatz_New_Chat_Handoff_v1.0.zip`, written `2026-08-13T14:08:51` — `33` seconds before the archive was built.

Every figure above is emitted by `code/src49_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

**Drill 14/14 by the check named for each, both controls clean, no malformed
mutations in the final pass.**

An archive check is awkward to drill for a reason worth naming: **almost every
branch that would report a defect is one no real input reaches.** Nothing has
drifted, so the `differing` list is always empty; nothing is unreadable, so
`unreadable` is always empty. Loosening a branch that never fires is invisible —
the item-43 lesson — so the defects here break the **subject** instead: the hash
function, the recorded-item lookup, the recursion, the manifest parse. Each makes
an empty branch fill.

The other half is non-vacuity. A check that reads nothing reports a clean
archive, so the gate now fails when the recursive walk does not descend, when no
shipped manifest is verified, when the two pack versions come back
indistinguishable, when the composition prefix matches nothing, and when the
coverage set is not the archive's own contents. **Six of the fourteen defects aim
at those guards rather than at the checks.**

**Two defects were re-aimed after the pre-flight named them.** Parsing the
manifest on one space instead of two changes nothing — the extra space lands at
the front of the filename and `.strip()` removes it — so the same slip was planted
as a column swap instead. And flipping the coverage comparison from `<` to `>`
still yields 24 items, comfortably past a size threshold; the guard now asks
whether the archive *contains* the set it selected rather than how large that set
is. **A size threshold does not know whether it is measuring the right set.**
Fourth item running that the pre-flight has paid for itself.

## Route map

Item 49 is a container, not a round. Item 50 returns to the numbered line with
`A-U.2d.4 — Renewal Congestion Rigidity`, which is the round the handoff in item
48 was written to launch.

## What this run does not claim

1. That the CPL research packs are correct, or that their Riemann-zeta content
   has been reviewed. It has not. Only their integrity was checked.
2. That the archive's entries are correct — only that they are **the same bytes**
   as the standalone items, which RUN-002 through RUN-030 examined individually.
3. That 964 files were read. They were opened and counted; their contents were
   not examined except where a manifest made a claim about them.
4. That the omission of item 48 was accidental. The 33-second gap is measured; the
   intent is not.
