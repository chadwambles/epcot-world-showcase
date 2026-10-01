#!/usr/bin/env python3
"""
audit_attribution.py

Measures how often the attribution rule puts a paragraph in the right
pavilion, by hand, against the source text.

The park study carried 0.82 precision on 140 hand-judged segments, and that
measurement is what justified cutting two sources that scored 0.12 and 0.38.
Pavilion attribution is harder than park attribution, so this number matters
more here, not less.

Two steps.
    py audit_attribution.py --sample          writes audit_sample.csv
    (open it, fill the verdict column with y or n, save)
    py audit_attribution.py --score           reports precision with intervals

Sampling is stratified by pavilion and by basis, because tier 2 matches on a
bare country name will be wrong far more often than tier 1 matches on a venue
name, and a single pooled number would hide that.

audit_sample.csv quotes paragraph text. Never commit it.
"""

import argparse
import collections
import csv
import json
import math
import random


def wilson(k, n, z=1.96):
    """Wilson score interval. A normal approximation on 20 judgments per
    pavilion would give intervals that run past 1.0."""
    if n == 0:
        return (0.0, 0.0)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4.0 * n * n))
    return ((c - s) / d, (c + s) / d)


def sample(segments, out, per_pavilion, seed):
    rows = [json.loads(l) for l in open(segments, encoding="utf-8")]
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["pavilion"], r["basis"])].append(r)

    rnd = random.Random(seed)
    picked = []
    for pav in sorted({k[0] for k in by}):
        strata = [k for k in by if k[0] == pav]
        # Split the quota across bases, weighted by how common each is.
        total = sum(len(by[k]) for k in strata)
        for k in strata:
            share = len(by[k]) / float(total)
            n = max(1, int(round(per_pavilion * share)))
            picked += rnd.sample(by[k], min(n, len(by[k])))

    rnd.shuffle(picked)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["verdict", "segment_id", "pavilion", "basis", "text"])
        for r in picked:
            w.writerow(["", r["segment_id"], r["pavilion"], r["basis"],
                        r["text"]])
    print("wrote %s  %d rows" % (out, len(picked)))
    print()
    print("Fill the verdict column:")
    print("  y   this paragraph really is about that pavilion")
    print("  n   it is not")
    print("  ?   you cannot tell from the paragraph alone")
    print()
    print("Judge the paragraph as written. Do not open the thread to work out")
    print("what the author meant, because the rule only ever sees the")
    print("paragraph, and grading it on information the rule cannot use")
    print("would report a precision the pipeline does not have.")


def score(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    judged = [r for r in rows if r["verdict"].strip().lower() in ("y", "n")]
    unclear = [r for r in rows if r["verdict"].strip() == "?"]
    if not judged:
        raise SystemExit("No verdicts filled in yet.")

    def block(title, keyfn):
        print("=" * 68)
        print(title)
        print("=" * 68)
        agg = collections.defaultdict(lambda: [0, 0])
        for r in judged:
            a = agg[keyfn(r)]
            a[1] += 1
            if r["verdict"].strip().lower() == "y":
                a[0] += 1
        for k in sorted(agg, key=lambda k: -agg[k][1]):
            good, n = agg[k]
            lo, hi = wilson(good, n)
            mark = "   LOW" if hi < 0.6 else ""
            print("  %-26s %3d/%-3d  %.2f   [%.2f, %.2f]%s"
                  % (k, good, n, good / float(n), lo, hi, mark))
        print()

    block("PRECISION BY PAVILION", lambda r: r["pavilion"])
    block("PRECISION BY BASIS", lambda r: r["basis"])

    good = sum(1 for r in judged if r["verdict"].strip().lower() == "y")
    lo, hi = wilson(good, len(judged))
    print("  overall %.2f on %d judged  [%.2f, %.2f]"
          % (good / float(len(judged)), len(judged), lo, hi))
    if unclear:
        print("  %d marked unclear and excluded from the denominator"
              % len(unclear))
    print()
    print("A pavilion whose interval top sits below 0.6 is not measured, it")
    print("is guessed. Either tighten its anchors and rerun, or report that")
    print("pavilion's sentiment rank as unavailable.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", default="data/segments_local.jsonl")
    ap.add_argument("--file", default="audit_sample.csv")
    ap.add_argument("--per-pavilion", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--score", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sample(args.segments, args.file, args.per_pavilion, args.seed)
    elif args.score:
        score(args.file)
    else:
        ap.error("pass --sample or --score")


if __name__ == "__main__":
    main()
