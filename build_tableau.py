#!/usr/bin/env python3
"""
build_tableau.py

Reshapes the published CSVs into the long, Tableau-shaped files the workbook
needs, and precomputes everything so the workbook needs no calculated fields.

WHY --isolate EXISTS
Tableau's text-file connector is FOLDER scoped, not file scoped. Point it at a
folder and it tries to union every text file in it, which on a folder of
differently-shaped CSVs fails with "There was a problem connecting to the data
source" and error code F3ADC07B. --isolate writes each CSV into a subfolder of
its own so the connector only ever sees one file.

WHAT IT WRITES
    rank_long.csv    pavilion x ranking, the slope chart
    scatter.csv      one row per pavilion, the quadrant chart
    menu_mix.csv     pavilion x cuisine code, the stacked menu bar
    minutes.csv      pavilion x component, the things-to-do bar
    notes.md         the figures the dashboard's text blocks quote

Usage:
    py build_tableau.py --isolate
"""

import argparse
import collections
import csv
import os
import shutil

SRC_DEFAULT = "data"

# The three pavilions the charts highlight, and why. Everything else is grey,
# because eleven categorical colours is not a palette, it is a crayon box.
EMPHASIS = {
    "France": "Good at all three",
    "Norway": "Last on all three",
    "Japan": "Ninth in things to do, first in authenticity",
}
OTHER = "The other eight"

RANKINGS = [("things_to_do_rank", "Things to do", 1),
            ("food_rank", "Food and drink", 2),
            ("authenticity_rank", "Authenticity", 3)]

CODES = [("NATIVE", "Native to the cuisine", 1),
         ("ADAPTED", "Adapted for the park", 2),
         ("GENERIC", "Generic theme park food", 3)]

# Coding native cuisine is meaningless when the country is the United States,
# so its menu mix is not comparable with the other ten.
NOT_COMPARABLE = {"The American Adventure"}


def read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write(rows, cols, out, name, isolate):
    folder = os.path.join(out, os.path.splitext(name)[0]) if isolate else out
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("  %-46s %4d rows  %2d cols" % (path, len(rows), len(cols)))
    return path


def emphasis(p):
    return EMPHASIS.get(p, OTHER)


def build_rank_long(rank, out, isolate):
    """One row per pavilion per ranking. The slope chart reads this."""
    rows = []
    for r in rank:
        for key, label, order in RANKINGS:
            if not r[key]:
                continue
            rows.append({
                "pavilion": r["pavilion"],
                "ranking": label,
                "ranking_order": order,
                "rank": float(r[key]),
                "rank_label": ("%g" % float(r[key])),
                "emphasis": emphasis(r["pavilion"]),
                "is_highlighted": "Yes" if r["pavilion"] in EMPHASIS else "No",
            })
    cols = ["pavilion", "ranking", "ranking_order", "rank", "rank_label",
            "emphasis", "is_highlighted"]
    return write(rows, cols, out, "rank_long.csv", isolate)


def build_scatter(rank, out, isolate):
    """One row per pavilion. The quadrant chart reads this."""
    rows = []
    for r in rank:
        if not r["authenticity_rank"]:
            continue          # excluded from authenticity, so no point to plot
        rows.append({
            "pavilion": r["pavilion"],
            "things_to_do_rank": float(r["things_to_do_rank"]),
            "authenticity_rank": float(r["authenticity_rank"]),
            "food_rank": float(r["food_rank"]),
            "guest_min": float(r["guest_min"]),
            "menu_native_pct": round(100 * float(r["menu_native_share"]), 1),
            "arch_refs": int(r["arch_refs"]),
            "arch_coherence": r["arch_coherence"],
            "emphasis": emphasis(r["pavilion"]),
            "is_highlighted": "Yes" if r["pavilion"] in EMPHASIS else "No",
        })
    cols = ["pavilion", "things_to_do_rank", "authenticity_rank", "food_rank",
            "guest_min", "menu_native_pct", "arch_refs", "arch_coherence",
            "emphasis", "is_highlighted"]
    return write(rows, cols, out, "scatter.csv", isolate)


def build_menu_mix(dining, out, isolate):
    """Pavilion x cuisine code, with the share precomputed so the stacked bar
    needs no table calculation."""
    tally = collections.defaultdict(collections.Counter)
    for r in dining:
        if r["status"] == "open" and r["cuisine_code"]:
            tally[r["pavilion"]][r["cuisine_code"]] += 1

    native_share = {}
    for p, c in tally.items():
        denom = sum(c[k] for k, _, _ in CODES)
        native_share[p] = (c["NATIVE"] / denom) if denom else 0.0
    order = sorted(native_share, key=lambda p: -native_share[p])

    rows = []
    for p in order:
        c = tally[p]
        denom = sum(c[k] for k, _, _ in CODES)
        for key, label, code_order in CODES:
            share = (c[key] / denom) if denom else 0.0
            rows.append({
                "pavilion": p,
                "cuisine_code": label,
                "code_order": code_order,
                "items": c[key],
                "share": round(share, 4),
                "share_label": ("%.0f%%" % (100 * share)) if share >= 0.09 else "",
                "pavilion_sort": order.index(p) + 1,
                "comparable": "No" if p in NOT_COMPARABLE else "Yes",
            })
    cols = ["pavilion", "cuisine_code", "code_order", "items", "share",
            "share_label", "pavilion_sort", "comparable"]
    return write(rows, cols, out, "menu_mix.csv", isolate)


def build_minutes(rank, out, isolate):
    """Pavilion x component. Splits the things-to-do measure into the two
    things it is made of, which is the part the single number hides."""
    order = sorted(rank, key=lambda r: -float(r["guest_min"]))
    rows = []
    for i, r in enumerate(order, 1):
        for key, label, comp_order in (
                ("ride_film_min", "Rides and films", 1),
                ("live_guest_min", "Live entertainment, one set", 2)):
            v = float(r[key])
            rows.append({
                "pavilion": r["pavilion"],
                "component": label,
                "component_order": comp_order,
                "minutes": round(v, 1),
                # %g, not %.0f: 28.5 rounds to "28" under banker's rounding,
                # which makes the label disagree with the bar it sits on.
                "minutes_label": ("%g" % round(v, 1)) if v >= 4 else "",
                "guest_min_total": float(r["guest_min"]),
                "pavilion_sort": i,
                "emphasis": emphasis(r["pavilion"]),
            })
    cols = ["pavilion", "component", "component_order", "minutes",
            "minutes_label", "guest_min_total", "pavilion_sort", "emphasis"]
    return write(rows, cols, out, "minutes.csv", isolate)


def spearman(pairs):
    n = len(pairs)
    d2 = sum((a - b) ** 2 for a, b in pairs)
    return 1 - (6 * d2) / (n * (n * n - 1)), n


def build_notes(rank, out):
    """The figures the dashboard's text blocks quote, so the wording in the
    workbook and the numbers in the data cannot drift apart."""
    crit = {10: 0.648, 11: 0.618}
    lines = ["# Figures for the dashboard text blocks", "",
             "Generated by build_tableau.py. If a number in the workbook does "
             "not match one here, the workbook is stale.", ""]

    for ka, kb, label in (
            ("things_to_do_rank", "authenticity_rank", "things to do vs authenticity"),
            ("things_to_do_rank", "food_rank", "things to do vs food"),
            ("food_rank", "authenticity_rank", "food vs authenticity")):
        pairs = [(float(r[ka]), float(r[kb])) for r in rank if r[ka] and r[kb]]
        rho, n = spearman(pairs)
        need = crit[n]
        lines.append("- %s: rho %+.2f on n=%d, needs %.2f for p<0.05, so %s"
                     % (label, rho, n, need,
                        "significant" if abs(rho) >= need
                        else "NOT distinguishable from zero"))
    lines += ["", "Highlighted pavilions:", ""]
    for p, why in EMPHASIS.items():
        r = next(x for x in rank if x["pavilion"] == p)
        lines.append("- %s: %s (things %s, food %s, authenticity %s)"
                     % (p, why.lower(), r["things_to_do_rank"],
                        r["food_rank"], r["authenticity_rank"] or "n/a"))
    path = os.path.join(out, "notes.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("  %-46s" % path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC_DEFAULT)
    ap.add_argument("--out", default="tableau")
    ap.add_argument("--isolate", action="store_true",
                    help="each CSV in its own subfolder, which is what the "
                         "folder-scoped text connector needs")
    ap.add_argument("--clean", action="store_true")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, args.src)
    out = os.path.join(here, args.out)
    if args.clean and os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)

    rank = read(os.path.join(src, "rankings.csv"))
    dining = read(os.path.join(src, "dining.csv"))

    print("=" * 70)
    print("TABLEAU SOURCES   %s" % ("isolated" if args.isolate
                                    else "FLAT, see the warning below"))
    print("=" * 70)
    build_rank_long(rank, out, args.isolate)
    build_scatter(rank, out, args.isolate)
    build_menu_mix(dining, out, args.isolate)
    build_minutes(rank, out, args.isolate)
    build_notes(rank, out)
    print()
    if not args.isolate:
        print("  WARNING: without --isolate every CSV sits in one folder, and")
        print("  Tableau's text connector is folder scoped. Connecting to one")
        print("  file tries to union all of them and fails with F3ADC07B.")
        print("  Rerun with --isolate.")
    else:
        print("  Connect to the CSV inside each subfolder, not to tableau/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
