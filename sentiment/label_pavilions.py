#!/usr/bin/env python3
"""
label_pavilions.py

Labels attributed paragraphs with the four codes.

TWO PARAGRAPHS PER REQUEST, AND NOT MORE. On the park study, packing eight
held overall agreement at 93% while losing 41% of queue detections and 29% of
price detections. Cram several paragraphs into one prompt and the model
reports what each is mainly about, dropping the passing mentions. The losses
were one sided and the aggregate metric hid them. Do not raise BATCH to save
money.

The model extracts, the code decides. It is never asked to score a pavilion,
rank anything, or judge authenticity. It answers what a paragraph says.
Pavilion attribution already happened in segment_attribute.py.

Reads ANTHROPIC_API_KEY from the environment. Never pass a key on the command
line and never paste one into a file.

Output is labels_raw.jsonl, which quotes paragraph text for auditing. That
file, like audit_sample.csv and labels_qa.csv, must never be committed or
uploaded.

Usage:
    py label_pavilions.py --limit 50        # try it on 50 first
    py label_pavilions.py
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"
BATCH = 2          # see the module docstring before changing this
MAX_TOKENS = 1400

SCHEMA = """For each paragraph return one object with exactly these keys:

"id"      the paragraph id given to you.

"feel"    how the author portrays the pavilion as a place.
          "transporting"  they describe it as convincing, immersive, like
                          being somewhere else, beautiful, well themed
          "themed_retail" they describe it as a shop, a facade, thin, empty,
                          a place with nothing in it, a gift shop
          "mixed"         both, clearly
          "not_stated"    they do not characterise it either way

"drivers" a list, possibly empty, of what the author credits or blames.
          Each entry is {"aspect": one of
          "food","architecture","staff","entertainment","atmosphere",
          "shopping","crowds","price",
          "direction": "positive" or "negative"}.
          Only include an aspect the author actually comments on.

"missing_entertainment"  true only if the author says a show, act or
          performer is gone, cancelled, no longer there, or that they miss
          one. Not true for merely mentioning an act.

"dwell"   "lingered"       they stayed, spent time, sat, went back
          "walked_through" they passed through, skipped it, nothing to do
          "not_stated"

Return a JSON array, one object per paragraph, nothing else. No prose, no
code fence. If a paragraph is not about an EPCOT pavilion at all, return
"feel":"not_stated", empty drivers, false, "not_stated"."""

SYSTEM = ("You read short passages from theme park discussion and report what "
          "they say. You never rate, rank or score anything, and you never "
          "infer beyond the text. If something is not stated, say it is not "
          "stated.\n\n" + SCHEMA)


def call(key, paras, tries=5):
    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": "\n\n".join(
            "[%s]\n%s" % (p["segment_id"], p["text"]) for p in paras)}],
    }
    data = json.dumps(body).encode("utf-8")
    for i in range(tries):
        req = urllib.request.Request(URL, data=data, headers={
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode("utf-8"))
            txt = "".join(c.get("text", "") for c in out.get("content", []))
            txt = txt.strip()
            if txt.startswith("```"):
                txt = txt.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(txt)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and i < tries - 1:
                wait = 5 * (i + 1)
                print("    http %d, waiting %ds" % (e.code, wait))
                time.sleep(wait)
                continue
            raise
        except (ValueError, urllib.error.URLError) as e:
            if i < tries - 1:
                print("    %s, retrying" % e)
                time.sleep(4 * (i + 1))
                continue
            raise
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", default="data/segments_local.jsonl")
    ap.add_argument("--out", default="data/labels_raw.jsonl")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY is not set in this shell.")

    segs = [json.loads(l) for l in open(args.segments, encoding="utf-8")]
    done = set()
    if os.path.exists(args.out):
        for l in open(args.out, encoding="utf-8"):
            try:
                done.add(json.loads(l)["segment_id"])
            except (ValueError, KeyError):
                pass
        print("resuming, %d already labeled" % len(done))
    todo = [s for s in segs if s["segment_id"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print("%d to label, %d per request" % (len(todo), BATCH))

    t0 = time.time()
    with open(args.out, "a", encoding="utf-8") as fh:
        for i in range(0, len(todo), BATCH):
            chunk = todo[i:i + BATCH]
            try:
                res = call(key, chunk)
            except Exception as e:
                print("  FAILED at %d: %s" % (i, e))
                print("  rerun the same command, it resumes from here")
                break
            by = {r.get("id"): r for r in res if isinstance(r, dict)}
            for s in chunk:
                r = by.get(s["segment_id"])
                if r is None:
                    print("    no label returned for %s" % s["segment_id"])
                    continue
                r["segment_id"] = s["segment_id"]
                r["post_id"] = s["post_id"]
                r["pavilion"] = s["pavilion"]
                r["text"] = s["text"]      # kept for the audit, never published
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            n = i + len(chunk)
            if n % 50 < BATCH:
                rate = n / max(1e-9, time.time() - t0)
                left = (len(todo) - n) / max(rate, 1e-9) / 60
                print("  %d / %d   %.1f/s   about %.0f min left"
                      % (n, len(todo), rate, left))

    print("wrote %s" % args.out)
    print("Do not commit that file. It contains post text.")


if __name__ == "__main__":
    sys.exit(main())
