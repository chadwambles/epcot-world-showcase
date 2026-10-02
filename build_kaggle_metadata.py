#!/usr/bin/env python3
"""
build_kaggle_metadata.py

Builds kaggle_upload/: the six curated CSVs plus dataset-metadata.json.

WHY A SEPARATE FOLDER
The first version uploaded straight out of data/, which is also where the
sentiment pipeline writes its working files. Kaggle uploads a folder, so
anything sitting in it goes public. Staging into a folder this script creates
means a stray file cannot reach Kaggle by being in the wrong place, and the
preflight is checking a folder whose contents are known rather than whatever
happens to be on disk.

kaggle_upload/ is a build artifact. Delete it any time; this rebuilds it.

THREE THINGS LEARNED THE HARD WAY ON THE LAST DATASET, ALL STILL TRUE

1. Keywords are validated against a controlled vocabulary and one bad tag
   rejects the ENTIRE payload, descriptions included. The error does name it:
   'The following keywords are invalid: "tourism and travel"'. Only tags
   already accepted on a live dataset go in KEYWORDS. Add discovery tags in
   the web UI instead, where Kaggle autocompletes from the valid list.

2. The Data Card body is not optional. kaggle's dataset_metadata_update
   builds a fresh settings object and sends the lot:
       update_settings.description = metadata.get("description") or ""
   There is no patch semantics. Metadata with no description does not leave
   the Data Card alone, it replaces it with an empty string. Omitting it is
   the one thing that looks cautious and is actually destructive.

3. Column descriptions do not go through the API. Kaggle accepts a resources
   block, returns no error and stores nothing. They are entered by hand in
   the web UI, behind the "Edit file description" pencil on each file. The
   resources block is still written here so the text is under version
   control and can be pasted rather than composed at the keyboard.

Usage:
    py build_kaggle_metadata.py
    py build_kaggle_metadata.py --id chadwambles/epcot-world-showcase
"""

import argparse
import csv
import json
import os
import shutil
import sys

ID = "chadwambles/epcot-world-showcase"
# Kaggle enforces these and the API error arrives only after you have typed
# yes to a create. Checked here instead.
TITLE_MIN, TITLE_MAX = 6, 50
SUBTITLE_MIN, SUBTITLE_MAX = 20, 80

TITLE = "EPCOT World Showcase: 11 Pavilions Measured"
SUBTITLE = "Eleven country pavilions ranked three ways, menus coded by cuisine"
LICENSE = "CC-BY-NC-SA-4.0"

# Known good. Both are already accepted on a live dataset of this account.
# Do not add a plausible sounding tag here without pushing it and reading the
# response. Use the web UI for anything else; it autocompletes valid tags.
KEYWORDS = [
    "exploratory data analysis",
    "data analytics",
]

FILE_DESCRIPTIONS = {
    "rankings.csv":
        "The result. One row per pavilion, with all three rankings and every "
        "sub-measure that feeds them, so the weighting can be disagreed with "
        "and rebuilt. authenticity_rank is blank for The American Adventure, "
        "which is excluded from that family.",
    "dining.csv":
        "Every published menu item at all 44 operating food and drink "
        "locations in World Showcase, 1,513 rows, each coded NATIVE, ADAPTED, "
        "GENERIC or UNCLEAR by whether the dish belongs to that country's "
        "cuisine. Collected 24 to 30 September 2026.",
    "entertainment.csv":
        "Live entertainment across seven sampled dates spanning two years and "
        "four festivals. Each act carries its set length, performances that "
        "day, whether it performs in that country's own tradition, and the "
        "quoted source phrase establishing that coding.",
    "architecture.csv":
        "40 documented references from a pavilion structure to the real "
        "building it reproduces, with the real location, the source, a source "
        "reliability tier, and whether the reference counts toward the "
        "pavilion's total.",
    "pavilions.csv":
        "Static per pavilion facts: ride and film runtime, gallery count, and "
        "whether the architectural references are regionally coherent or a "
        "national pastiche.",
    "shops.csv":
        "A snapshot of Disney's own shop directory, rendered in a browser "
        "because the page builds its list client side. Published so the "
        "absence of a shop measure is checkable rather than asserted: the "
        "directory assigns zero shops to China, which visibly has one.",
}

COLUMN_DESCRIPTIONS = {
 "rankings.csv": {
  "pavilion": "Pavilion name. The key across every file in this dataset",
  "things_to_do_rank": "Rank on minutes of programmed content one visitor can consume. 1 is most. Ties share the average rank",
  "food_rank": "Rank averaged over venue count, menu breadth and signature dining count",
  "authenticity_rank": "Rank averaged over native menu share, entertainment specificity and building references. Blank for The American Adventure, which is excluded",
  "ride_film_min": "Total runtime of rides and films in the pavilion, in minutes",
  "live_guest_min": "One set of each live act, each discounted by the share of sampled dates it actually ran on",
  "guest_min": "ride_film_min plus live_guest_min. What one visitor can consume. things_to_do_rank sorts on this",
  "live_min_day": "The pavilion's scheduled live performance output per day, averaged over sampled dates. Context only, does not rank",
  "exhibits": "Galleries and walkthroughs. Reported but not ranked: a self paced space has no runtime and the count takes only three values",
  "venues": "Open permanent food and drink locations",
  "menu_items": "Distinct published menu items across the whole pavilion",
  "signature": "Disney Signature Dining rooms. Only three exist in World Showcase",
  "menu_native_share": "Share of coded items native to that country's cuisine, 0 to 1. UNCLEAR items are left out of the denominator",
  "ent_specific_share": "Share of live entertainment minutes performed in that country's own tradition, 0 to 1. Blank where the pavilion has no scheduled entertainment, which is not the same as having generic entertainment",
  "arch_refs": "Count of named real buildings the pavilion reproduces, derived from architecture.csv",
  "arch_coherence": "coherent where references come from one city or region, pastiche where they span distant regions. Reported, does not rank",
  "menu_items_unclear": "Items that could not be coded either way and are excluded from the native share",
 },
 "dining.csv": {
  "pavilion": "Pavilion name",
  "venue": "Restaurant, kiosk or lounge name",
  "service_type": "table service, quick service, lounge or kiosk",
  "signature": "yes where Disney classifies the venue as Signature Dining",
  "price_tier": "Disney's own price tier, $ to $$$$",
  "status": "open or closed. Closed venues are excluded from venue counts",
  "item": "Menu item name. Blank where a venue's menu could not be obtained, with the reason in note",
  "section": "appetizer, entree, dessert or beverage",
  "price": "Price as published, including the currency symbol",
  "cuisine_code": "NATIVE for a dish belonging to that country's cuisine, ADAPTED for one influenced by it but altered for the park, GENERIC for standard theme park food, UNCLEAR for a genuine ambiguity recorded rather than forced",
  "note": "Coding rationale, menu gaps, and whether an item is a festival offering at a permanent venue",
 },
 "entertainment.csv": {
  "date": "Sampled date, YYYY-MM-DD",
  "pavilion": "Pavilion name, or a non pavilion venue such as America Gardens Theatre, World Showcase Lagoon or park-wide",
  "act": "Act name as the source lists it",
  "performances": "Sets scheduled that day",
  "set_minutes": "Published duration of a single set",
  "daily_minutes": "performances multiplied by set_minutes",
  "specificity": "specific where the act's own published description names a tradition and an origin, generic where it does not",
  "evidence_quote": "The phrase from the source that establishes the specificity coding",
  "source_url": "The act's source page",
 },
 "architecture.csv": {
  "pavilion": "Pavilion name",
  "pavilion_element": "The structure at EPCOT",
  "real_structure": "The real building it reproduces",
  "real_location": "That real building's city or region",
  "source_url": "Primary source establishing the connection",
  "source_tier": "T1 Disney official, T2 reference or published guidebook, T3 established fan reference, T4 individual blog. T4 only claims are excluded from counted totals",
  "disputed": "yes where sources disagree about which real building is the model",
  "counted": "yes where the row counts toward the pavilion's arch_refs total",
  "not_counted_reason": "Why a row does not count, such as a source naming no specific structure, or a competing attribution of an element already counted",
 },
 "pavilions.csv": {
  "pavilion": "Pavilion name",
  "ride_film_min": "Total ride and film runtime in minutes",
  "ride_film_note": "Why the number is what it is, including the two runtimes that sources dispute",
  "permanent_shops": "Retail count. Not used in any ranking, because both available sources are unreliable",
  "exhibits": "Galleries and walkthroughs",
  "arch_refs": "Superseded by the count derived from architecture.csv. Kept for reference",
  "arch_coherence": "coherent or pastiche",
 },
 "shops.csv": {
  "shop": "Shop name as Disney's directory lists it",
  "area": "Which part of EPCOT the shop sits in",
  "in_world_showcase": "yes only for the eleven country pavilions. The entrance plaza, the African Outpost and the International Gateway are no",
  "pavilion": "Pavilion, where the shop belongs to one",
  "note": "Why a shop is excluded, or its listed status",
 },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="kaggle_upload")
    ap.add_argument("--id", default=ID)
    ap.add_argument("--title", default=TITLE)
    ap.add_argument("--subtitle", default=SUBTITLE)
    ap.add_argument("--license", default=LICENSE)
    ap.add_argument("--description-file", default="kaggle-about-dataset.md")
    args = ap.parse_args()

    if not TITLE_MIN <= len(args.title) <= TITLE_MAX:
        raise SystemExit(
            "Title is %d characters. Kaggle requires %d to %d.\n  %r"
            % (len(args.title), TITLE_MIN, TITLE_MAX, args.title))
    if not SUBTITLE_MIN <= len(args.subtitle) <= SUBTITLE_MAX:
        raise SystemExit(
            "Subtitle is %d characters. Kaggle requires %d to %d.\n  %r"
            % (len(args.subtitle), SUBTITLE_MIN, SUBTITLE_MAX, args.subtitle))

    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, args.data)
    out = os.path.join(here, args.out)

    # Only the files that have a description. A CSV nobody documented is not
    # part of the dataset, whatever it is doing in data/.
    files = sorted(FILE_DESCRIPTIONS)
    missing = [f for f in files if not os.path.exists(os.path.join(data, f))]
    if missing:
        raise SystemExit("Missing from %s: %s" % (data, ", ".join(missing)))

    problems = []
    resources = []
    ncols = 0
    for name in files:
        res = {"path": name}
        fd = FILE_DESCRIPTIONS.get(name)
        if fd:
            res["description"] = fd
        else:
            problems.append("%s has no file description." % name)

        with open(os.path.join(data, name), newline="",
                  encoding="utf-8") as fh:
            header = next(csv.reader(fh))
        cols = COLUMN_DESCRIPTIONS.get(name, {})
        fields = []
        for c in header:
            d = cols.get(c)
            if not d:
                problems.append("%s column %r has no description." % (name, c))
                d = ""
            # The column description goes in "title". Kaggle's own importer
            # reads it from there, and text put in "description" does not
            # surface anywhere in the UI.
            fields.append({"name": c, "title": d})
            ncols += 1
        res["schema"] = {"fields": fields}
        resources.append(res)

    desc_path = os.path.join(here, args.description_file)
    if not os.path.exists(desc_path):
        raise SystemExit(
            "No Data Card body at %s.\n\n"
            "This is required. The metadata update call replaces the entire\n"
            "settings object, so metadata without a description blanks the\n"
            "live Data Card rather than leaving it alone."
            % desc_path)
    description = open(desc_path, encoding="utf-8").read().strip()

    meta = {
        "id": args.id,
        "title": args.title,
        "subtitle": args.subtitle,
        "description": description,
        "licenses": [{"name": args.license}],
        "keywords": KEYWORDS,
        "resources": resources,
    }

    # Rebuild the staging folder from scratch so a file removed from the
    # dataset does not linger from a previous run and upload again.
    if os.path.isdir(out):
        for f in os.listdir(out):
            os.remove(os.path.join(out, f))
    else:
        os.makedirs(out)
    for name in files:
        shutil.copyfile(os.path.join(data, name), os.path.join(out, name))

    meta_path = os.path.join(out, "dataset-metadata.json")
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)

    print("=" * 66)
    print("KAGGLE METADATA")
    print("=" * 66)
    print("  id            %s" % args.id)
    print("  title         %s  (%d/%d)"
          % (args.title, len(args.title), TITLE_MAX))
    print("  subtitle      %s" % args.subtitle)
    print("                (%d/%d)" % (len(args.subtitle), SUBTITLE_MAX))
    print("  Data Card     %d words from %s"
          % (len(description.split()), args.description_file))
    print("  license       %s" % args.license)
    print("  keywords      %s" % ", ".join(KEYWORDS))
    print("  files         %d" % len(files))
    print("  columns       %d" % ncols)
    print()
    if problems:
        print("  PROBLEMS")
        for p in problems:
            print("    %s" % p)
        print()
        return 1
    print("  staged %d files into %s/" % (len(files), args.out))
    print("  wrote %s" % meta_path)
    print()
    print("  Column descriptions do not apply through the API. After the")
    print("  version uploads, open each file on Kaggle and use the pencil")
    print("  next to 'Edit file description' to paste them in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
