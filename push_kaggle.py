#!/usr/bin/env python3
"""
push_kaggle.py

Pushes the dataset from kaggle_upload/, calling the kaggle library directly
rather than the `kaggle` console script.

Upload from the staging folder build_kaggle_metadata.py creates, never from
data/. Kaggle uploads a whole folder, and data/ is also where the sentiment
pipeline writes its working files. Staging means a stray file cannot go
public by sitting in the wrong directory.

WHY NOT THE CLI
On Windows, pip puts kaggle.exe in a per user Scripts folder that is often
not on PATH, so `kaggle datasets version` fails with "not recognized as the
name of a cmdlet" even though the package installed fine. Importing the
library sidesteps it: if py can run this file, it can push.

WHAT IT CHECKS FIRST
A dataset version is public the moment it lands and there is no quiet undo,
so this refuses to upload unless data/ looks right. It checks that the
metadata exists and parses, that every file it names is present, that no
file carries a cell long enough to be prose, and that none of the
text bearing working files got in. Then it prints what it is about to do and
waits for you to type yes.

TWO CALLS, NOT ONE
Uploading a version and applying settings are separate operations.
dataset_create_version uploads the files and ignores title, subtitle, Data
Card and keywords. dataset_metadata_update applies those. Run the version
first, then --metadata-only.

Column descriptions go through neither. Kaggle accepts the resources block,
returns no error and stores nothing. They are hand entered in the web UI
behind the pencil on each file. The text is in data/dataset-metadata.json
ready to paste.

Usage:
    py push_kaggle.py --dry-run
    py push_kaggle.py -m "First version"
    py push_kaggle.py --metadata-only
"""

import argparse
import csv
import json
import os
import sys

# Working files that quote post text. Named in .gitignore, and named again
# here, because the one thing worse than a leak is a leak nobody checked for
# at the last gate.
NEVER_UPLOAD = {
    "audit_sample.csv",
    "labels_qa.csv",
    "labels_raw.jsonl",
    "segments_local.jsonl",
    "epcot_posts.jsonl",
    "segment_index.csv",
}

# The longest legitimate cell in this dataset is a 290 character methodology
# note about an unobtainable wine list. Anything past this is prose that
# should not be here, most likely a quoted post.
MAX_CELL = 500


def preflight(data):
    problems = []
    meta_path = os.path.join(data, "dataset-metadata.json")

    if not os.path.exists(meta_path):
        return ["No dataset-metadata.json in %s. Run "
                "build_kaggle_metadata.py first." % data], None
    try:
        meta = json.load(open(meta_path, encoding="utf-8"))
    except ValueError as e:
        return ["dataset-metadata.json does not parse: %s" % e], None

    if not (meta.get("description") or "").strip():
        problems.append(
            "No Data Card body in the metadata. A --metadata-only run would "
            "BLANK the live Data Card, because the update call replaces the "
            "whole settings object rather than patching it.")

    present = set(os.listdir(data))

    for bad in sorted(NEVER_UPLOAD & present):
        problems.append("%s is in the upload folder and carries post text. "
                        "Move it out." % bad)

    named = [r["path"] for r in meta.get("resources", [])]
    for n in named:
        if n not in present:
            problems.append("Metadata names %s but it is not in %s"
                            % (n, data))

    strays = [f for f in sorted(present)
              if f.endswith(".csv") and f not in named]
    for s in strays:
        problems.append("%s is in %s but not described in the metadata. "
                        "It would upload with no description." % (s, data))

    for f in sorted(present):
        if not f.endswith(".csv"):
            continue
        with open(os.path.join(data, f), newline="", encoding="utf-8") as fh:
            for i, row in enumerate(csv.reader(fh), 1):
                for cell in row:
                    if len(cell) > MAX_CELL:
                        problems.append(
                            "%s line %d has a %d character cell. The longest "
                            "legitimate one here is 290. Check it is not post "
                            "text: %r" % (f, i, len(cell), cell[:90]))
                        break
                else:
                    continue
                break
    return problems, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="kaggle_upload")
    ap.add_argument("-m", "--message", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--metadata-only", action="store_true")
    ap.add_argument("--new", action="store_true",
                    help="create the dataset instead of versioning it")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, args.data)

    if not os.path.isdir(data):
        print("No %s/. Run build_kaggle_metadata.py first." % args.data)
        return 1
    problems, meta = preflight(data)
    print("=" * 68)
    print("PREFLIGHT  %s" % data)
    print("=" * 68)
    if problems:
        for p in problems:
            print("  BLOCKED  %s" % p)
        print()
        print("  Nothing was uploaded.")
        return 1

    files = sorted(f for f in os.listdir(data) if f.endswith(".csv"))
    total = sum(os.path.getsize(os.path.join(data, f)) for f in files)
    print("  metadata parses, Data Card present (%d words)"
          % len(meta["description"].split()))
    print("  %d files, %.1f KB, none carrying post text" % (len(files),
                                                            total / 1024.0))
    for f in files:
        print("      %-24s %8d bytes" % (f, os.path.getsize(
            os.path.join(data, f))))
    print()

    if args.dry_run:
        print("  Dry run. Nothing uploaded.")
        return 0

    if args.metadata_only:
        action = ("UPDATE SETTINGS on %s\n"
                  "    title, subtitle, Data Card, keywords, license.\n"
                  "    This replaces the live Data Card with the one above."
                  % meta["id"])
    elif args.new:
        action = "CREATE a new public dataset %s" % meta["id"]
    else:
        if not args.message:
            print("  A version needs -m \"what changed\".")
            return 1
        action = ("UPLOAD A NEW VERSION of %s\n    %s"
                  % (meta["id"], args.message))

    print("  About to %s" % action)
    print()
    if input("  Type yes to continue: ").strip().lower() != "yes":
        print("  Stopped.")
        return 1

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("  kaggle is not installed in this interpreter.")
        print("  py -m pip install kaggle")
        return 1

    api = KaggleApi()
    api.authenticate()

    if args.metadata_only:
        r = api.dataset_metadata_update(meta["id"], data)
        print("  %s" % (r or "settings updated"))
    elif args.new:
        # convert_to_csv is set explicitly. Left to its default, kaggle
        # rewrites files on the way up, which silently changes the bytes
        # people download relative to the ones in the repository.
        r = api.dataset_create_new(data, public=True, quiet=False,
                                   convert_to_csv=False, dir_mode="skip")
        print("  %s" % r)
    else:
        r = api.dataset_create_version(data, args.message, quiet=False,
                                       convert_to_csv=False, dir_mode="skip")
        print("  %s" % r)

    print()
    print("  Next: py push_kaggle.py --metadata-only")
    print("  Then open each file on Kaggle and paste its column descriptions")
    print("  from kaggle_upload/dataset-metadata.json. The API will not")
    print("  set them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
