#!/usr/bin/env python3
"""
fetch_repcot.py

Pulls r/epcot posts and comments from the Arctic Shift archive.

r/epcot was chosen over r/WaltDisneyWorld because nearly every post is
pavilion relevant, which makes attribution far easier. The cost is volume. Run
--census first: if the thin pavilions are the ones the story needs, add
r/WaltDisneyWorld with an EPCOT filter as a second pass rather than guessing
up front.

Nothing here is published. Post text stays local. Only derived codes ever
leave this machine.

Usage:
    py fetch_repcot.py --census
    py fetch_repcot.py --from 2015-01-01 --to 2026-09-30
"""

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://arctic-shift.photon-reddit.com/api"
UA = "epcot-pavilion-study/1.0 (personal research)"


def epoch(d):
    return int(datetime.strptime(d, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp())


def get(path, params, tries=5):
    url = "%s/%s?%s" % (API, path, urllib.parse.urlencode(params))
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8")).get("data", [])
        except Exception as e:
            if i == tries - 1:
                raise
            # The archive rate limits. Back off rather than hammering it.
            wait = 4 * (i + 1)
            print("    retry %d after %ds (%s)" % (i + 1, wait, e))
            time.sleep(wait)
    return []


def page(kind, sub, start, end, out, limit=100):
    """Walk forward in time. Arctic Shift caps a response, so each page picks
    up from the last item's timestamp."""
    seen = set()
    cur = start
    n = 0
    with open(out, "a", encoding="utf-8") as fh:
        while cur < end:
            rows = get("%s/search" % kind,
                       {"subreddit": sub, "after": cur, "before": end,
                        "limit": limit, "sort": "asc"})
            if not rows:
                break
            newest = cur
            fresh = 0
            for r in rows:
                rid = r.get("id")
                if rid in seen:
                    continue
                seen.add(rid)
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                fresh += 1
                newest = max(newest, int(r.get("created_utc", cur)))
            n += fresh
            print("    %s  %s  +%d  total %d"
                  % (kind, datetime.fromtimestamp(newest, timezone.utc).date(), fresh, n))
            if fresh == 0 or newest <= cur:
                cur += 86400
            else:
                cur = newest + 1
            time.sleep(1.2)
    return n


def census(sub, start, end):
    """Posts per year, so the scope decision is made on counts rather than
    on a hunch about how busy the subreddit was."""
    print("=" * 56)
    print("VOLUME CENSUS  r/%s" % sub)
    print("=" * 56)
    y0 = datetime.fromtimestamp(start, timezone.utc).year
    y1 = datetime.fromtimestamp(end, timezone.utc).year
    for y in range(y0, y1 + 1):
        a = epoch("%d-01-01" % y)
        b = min(epoch("%d-01-01" % (y + 1)), end)
        if b <= a:
            continue
        rows = get("posts/search", {"subreddit": sub, "after": a,
                                    "before": b, "limit": 100, "sort": "asc"})
        print("  %d  at least %d posts%s"
              % (y, len(rows), "  (capped, more exist)" if len(rows) >= 100
                 else ""))
        time.sleep(1.2)
    print("\nA year showing 100 is capped by the page size, not a true count.")
    print("Use it to spot the years that are genuinely thin.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sub", default="epcot")
    ap.add_argument("--from", dest="start", default="2015-01-01")
    ap.add_argument("--to", dest="end", default="2026-09-30")
    ap.add_argument("--out", default="data")
    ap.add_argument("--census", action="store_true")
    ap.add_argument("--comments", action="store_true",
                    help="also pull comments, which multiplies volume")
    args = ap.parse_args()

    s, e = epoch(args.start), epoch(args.end)
    if args.census:
        return census(args.sub, s, e)

    os.makedirs(args.out, exist_ok=True)
    p = os.path.join(args.out, "%s_posts.jsonl" % args.sub)
    if os.path.exists(p):
        raise SystemExit("%s exists. Move or delete it first, so a partial "
                         "run is never silently appended to." % p)
    print("posts %s to %s" % (args.start, args.end))
    n = page("posts", args.sub, s, e, p)
    print("wrote %s  %d posts" % (p, n))

    if args.comments:
        c = os.path.join(args.out, "%s_comments.jsonl" % args.sub)
        if os.path.exists(c):
            raise SystemExit("%s exists." % c)
        m = page("comments", args.sub, s, e, c)
        print("wrote %s  %d comments" % (c, m))


if __name__ == "__main__":
    main()
