#!/usr/bin/env python3
"""
score_sentiment.py

Turns the labels into the fourth ranking, and writes a publishable file that
carries no post text.

Sub-measures, matching the four codes:
    feel_score     share of characterising paragraphs that read transporting
                   rather than themed retail
    driver_net     net positive minus negative driver mentions, per paragraph
    dwell_score    share of dwell statements that are lingered
    (missing_entertainment is counted and reported, but does not rank. It is
     a rare code and skews toward long time visitors. A handful of people
     saying they miss an act is a good paragraph in the write up and a bad
     statistic.)

A pavilion under the floor keeps its number and its count but is not ranked,
the same treatment the park study gave thin cells.

Each sub-measure carries its own floor as well, because the paragraph count
is not the denominator. feel_score only counts paragraphs that characterise
the pavilion one way or the other, and most do not. An earlier run printed
Germany at a perfect 1.00 off a single characterising paragraph, which looks
like a finding and is one observation.
"""

import argparse
import collections
import csv
import json

FLOOR = 30          # attributed paragraphs per pavilion
SUB_FLOOR = 15      # paragraphs that actually carry each sub-measure


def rank(values):
    s = sorted(((k, v) for k, v in values.items() if v is not None),
               key=lambda kv: kv[1], reverse=True)
    out, i = {}, 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1][1] == s[i][1]:
            j += 1
        for k in range(i, j + 1):
            out[s[k][0]] = (i + j) / 2.0 + 1
        i = j + 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="data/labels_raw.jsonl")
    ap.add_argument("--out", default="sentiment_ranking.csv")
    ap.add_argument("--floor", type=int, default=FLOOR)
    ap.add_argument("--sub-floor", type=int, default=SUB_FLOOR)
    args = ap.parse_args()

    n = collections.Counter()
    feel = collections.defaultdict(collections.Counter)
    drv = collections.defaultdict(collections.Counter)
    dwell = collections.defaultdict(collections.Counter)
    miss = collections.Counter()
    posts = collections.defaultdict(set)

    for line in open(args.labels, encoding="utf-8"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        p = r.get("pavilion")
        if not p:
            continue
        n[p] += 1
        posts[p].add(r.get("post_id"))
        feel[p][r.get("feel", "not_stated")] += 1
        dwell[p][r.get("dwell", "not_stated")] += 1
        if r.get("missing_entertainment"):
            miss[p] += 1
        for d in r.get("drivers") or []:
            if isinstance(d, dict) and d.get("aspect"):
                drv[p][(d["aspect"], d.get("direction"))] += 1

    pav = sorted(n)
    fs, dn, ds = {}, {}, {}
    den = {}
    for p in pav:
        t = feel[p]["transporting"]
        r_ = feel[p]["themed_retail"]
        li = dwell[p]["lingered"]
        wt = dwell[p]["walked_through"]
        ndrv = sum(v for (a, d), v in drv[p].items())
        den[p] = (t + r_, ndrv, li + wt)
        # A ratio off one or two observations is noise wearing a decimal
        # point. Report the count, withhold the score.
        fs[p] = t / float(t + r_) if (t + r_) >= args.sub_floor else None
        pos = sum(v for (a, d), v in drv[p].items() if d == "positive")
        neg = sum(v for (a, d), v in drv[p].items() if d == "negative")
        dn[p] = ((pos - neg) / float(n[p])
                 if ndrv >= args.sub_floor and n[p] else None)
        ds[p] = (li / float(li + wt)
                 if (li + wt) >= args.sub_floor else None)

    # A pavilion needs the paragraph floor and at least one usable
    # sub-measure. Averaging a rank over zero sub-measures ranks nothing.
    ranked = [p for p in pav if n[p] >= args.floor
              and any(m[p] is not None for m in (fs, dn, ds))]
    sub = [rank({p: v for p, v in m.items() if p in ranked})
           for m in (fs, dn, ds)]
    avg = {}
    for p in ranked:
        got = [r[p] for r in sub if p in r]
        avg[p] = sum(got) / len(got) if got else None
    final = rank({p: -v for p, v in avg.items() if v is not None})

    print("=" * 76)
    print("GUEST SENTIMENT          floor %d paragraphs" % args.floor)
    print("=" * 76)
    print("%-22s %5s %5s %12s %12s %12s %5s %5s"
          % ("pavilion", "paras", "posts", "feel (n)", "drivers (n)",
             "dwell (n)", "miss", "rank"))

    def cell(v, d, fmt="%.2f"):
        if v is None:
            return "%s (%d)" % ("--", d)
        return "%s (%d)" % (fmt % v, d)

    for p in sorted(pav, key=lambda p: final.get(p, 99)):
        print("%-22s %5d %5d %12s %12s %12s %5d %5s"
              % (p, n[p], len(posts[p]),
                 cell(fs[p], den[p][0]),
                 cell(dn[p], den[p][1], "%+.2f"),
                 cell(ds[p], den[p][2]),
                 miss[p],
                 "%.1f" % final[p] if p in final else "--"))
    print()
    print("  (n) is the number of paragraphs the measure actually rests on,")
    print("  not the pavilion's paragraph count. A score is withheld below")
    print("  %d, because a ratio off a handful of observations is noise."
          % args.sub_floor)

    unranked = [p for p in pav if p not in final]
    if unranked:
        print("\n  not ranked: %s" % ", ".join(sorted(unranked)))
    if len(final) < 3:
        print()
        print("  Fewer than three pavilions could be ranked. The corpus does")
        print("  not carry enough evaluative writing to support this measure.")
        print("  Add comments or a second subreddit, or drop the lens. Do not")
        print("  lower the floors to make a table appear.")

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["pavilion", "paragraphs", "posts", "feel_score",
                    "driver_net", "dwell_score", "missing_entertainment",
                    "sentiment_rank"])
        for p in pav:
            w.writerow([p, n[p], len(posts[p]),
                        "" if fs[p] is None else round(fs[p], 4),
                        "" if dn[p] is None else round(dn[p], 4),
                        "" if ds[p] is None else round(ds[p], 4),
                        miss[p], final.get(p, "")])
    print("\nwrote %s  (no post text, safe to publish)" % args.out)


if __name__ == "__main__":
    main()
