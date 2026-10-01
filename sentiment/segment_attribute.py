#!/usr/bin/env python3
"""
segment_attribute.py

Splits posts into paragraphs and attributes each one to a pavilion.

Attribution is done here, in code, not by the labeling model. The model's job
is to read a paragraph and say what it says. Deciding which pavilion the
paragraph is about is a rule, and a rule can be audited.

THE RULE
  1. A tier 1 anchor (a venue, attraction, act or shop name) attributes the
     paragraph outright. Nobody says "Le Cellier" about the country Canada.
  2. A tier 2 anchor (a bare country name) only counts when EPCOT context is
     established, either in the same paragraph or anywhere in the post.
  3. A tier 1 match always beats a tier 2 match for a different pavilion.
  4. A paragraph naming two pavilions at the same tier is marked multi and is
     excluded from the per-pavilion counts. Those are the paragraphs that
     quietly poison a comparison.
  5. Everything else is unattributed.

TITLES ARE SEGMENTS. 72 percent of r/epcot posts have no body at all, and the
median title is nine words, so a body-only pass with a twelve word floor
threw away two thirds of the corpus. Titles carry their own, lower floor.

SUBREDDIT CONTEXT. Every post in r/epcot is about EPCOT, so requiring a
context word inside the text as well discarded 1,148 paragraphs on the first
run. --assume-epcot treats the subreddit itself as the context. Leave it off
for a general subreddit such as r/WaltDisneyWorld, where a post really can be
about a trip to Japan.

Carried forward from the park study: post_id is kept, because it is Reddit's
public base-36 identifier and the analysis needs to cluster on it. No
username, title, permalink or body text is ever written to a published file.

Usage:
    py segment_attribute.py --posts data/epcot_posts.jsonl
"""

import argparse
import csv
import json
import os
import re

# Venues that sit inside a pavilion's footprint but are not that pavilion.
# America Gardens Theatre stands at the American Adventure and hosts the
# festival concert series, so a post about Eat to the Beat would otherwise
# attribute to the USA pavilion. Stripped before matching.
NOT_PAVILION = re.compile(
    r"america[n]?\s+gardens?\s+theat(?:re|er)", re.I)

MIN_WORDS = 12          # body paragraphs; shorter is rarely evaluative
MIN_TITLE_WORDS = 5     # titles say more per word, so they earn a lower bar
MAX_WORDS = 400


def load_anchors(p):
    with open(p, encoding="utf-8") as fh:
        a = json.load(fh)
    def pat(words):
        esc = sorted((re.escape(w) for w in words), key=len, reverse=True)
        return re.compile(r"(?<![\w'])(?:%s)(?![\w'])" % "|".join(esc), re.I)
    t1 = {p_: pat(v) for p_, v in a["tier1"].items() if v}
    t2 = {p_: pat(v) for p_, v in a["tier2"].items() if v}
    ctx = pat(a["epcot_context"])
    return a["pavilions"], t1, t2, ctx


def paragraphs(text, floor=MIN_WORDS):
    for raw in re.split(r"\n\s*\n+", text or ""):
        s = re.sub(r"\s+", " ", raw).strip()
        if not s:
            continue
        n = len(s.split())
        if floor <= n <= MAX_WORDS:
            yield s


def attribute(par, post_ctx, t1, t2, ctx):
    par = NOT_PAVILION.sub(" ", par)
    hits1 = [p for p, r in t1.items() if r.search(par)]
    if len(hits1) == 1:
        return hits1[0], "tier1"
    if len(hits1) > 1:
        return None, "multi_tier1"
    has_ctx = post_ctx or bool(ctx.search(par))
    if not has_ctx:
        return None, "no_epcot_context"
    hits2 = [p for p, r in t2.items() if r.search(par)]
    if len(hits2) == 1:
        return hits2[0], "tier2"
    if len(hits2) > 1:
        return None, "multi_tier2"
    return None, "no_anchor"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts", default="data/epcot_posts.jsonl")
    ap.add_argument("--anchors", default="anchors.json")
    ap.add_argument("--out", default="data")
    ap.add_argument("--assume-epcot", action="store_true",
                    help="treat every post as EPCOT context, correct for "
                         "r/epcot, wrong for a general subreddit")
    ap.add_argument("--no-titles", action="store_true",
                    help="body paragraphs only")
    args = ap.parse_args()

    pavilions, t1, t2, ctx = load_anchors(args.anchors)
    os.makedirs(args.out, exist_ok=True)

    # Holds paragraph text, so it is a working file and never published.
    seg_path = os.path.join(args.out, "segments_local.jsonl")
    idx_path = os.path.join(args.out, "segment_index.csv")

    counts = {p: 0 for p in pavilions}
    reasons = {}
    total = kept = 0

    with open(args.posts, encoding="utf-8") as fin, \
         open(seg_path, "w", encoding="utf-8") as fseg, \
         open(idx_path, "w", newline="", encoding="utf-8") as fidx:
        w = csv.writer(fidx)
        w.writerow(["segment_id", "post_id", "created_utc", "para_index",
                    "pavilion", "basis", "word_count"])
        for line in fin:
            try:
                post = json.loads(line)
            except ValueError:
                continue
            title = (post.get("title") or "").strip()
            self_ = (post.get("selftext") or "").strip()
            if self_ in ("[removed]", "[deleted]"):
                self_ = ""
            whole = "%s\n\n%s" % (title, self_)
            if not whole.strip():
                continue
            post_ctx = args.assume_epcot or bool(ctx.search(whole))
            pid = post.get("id")

            units = []
            if title and not args.no_titles:
                if MIN_TITLE_WORDS <= len(title.split()) <= MAX_WORDS:
                    units.append(re.sub(r"\s+", " ", title))
            units += list(paragraphs(self_))

            for i, par in enumerate(units):
                total += 1
                pav, basis = attribute(par, post_ctx, t1, t2, ctx)
                reasons[basis] = reasons.get(basis, 0) + 1
                if pav is None:
                    continue
                kept += 1
                counts[pav] += 1
                sid = "%s_%d" % (pid, i)
                fseg.write(json.dumps(
                    {"segment_id": sid, "post_id": pid, "pavilion": pav,
                     "basis": basis, "text": par}, ensure_ascii=False) + "\n")
                w.writerow([sid, pid, post.get("created_utc"), i, pav, basis,
                            len(par.split())])

    print("=" * 60)
    print("SEGMENTATION")
    print("=" * 60)
    print("  segments considered     %d" % total)
    print("  attributed              %d  (%.1f%%)"
          % (kept, 100.0 * kept / total if total else 0))
    print()
    for p in pavilions:
        flag = "   THIN" if counts[p] < 30 else ""
        print("  %-24s %5d%s" % (p, counts[p], flag))
    print()
    print("  why the rest were dropped:")
    for r, n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        if r not in ("tier1", "tier2"):
            print("    %-22s %6d" % (r, n))
    print()
    print("  %s   paragraph text, keep local, never commit" % seg_path)
    print("  %s   safe to publish" % idx_path)
    print()
    print("Any pavilion marked THIN will produce a noisy rank. That is the")
    print("signal to add r/WaltDisneyWorld as a second pass, not to publish")
    print("the thin number with a footnote.")


if __name__ == "__main__":
    main()
