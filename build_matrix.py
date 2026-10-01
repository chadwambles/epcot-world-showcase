#!/usr/bin/env python3
"""
build_matrix.py

Ranks the eleven EPCOT World Showcase pavilions on separate families of
evidence, and reports where those families disagree. There is deliberately no
composite score. Averaging the families would need weights, and any weighting
is a choice presented as arithmetic.

Within a family: rank on each sub-measure, 1 is best, ties share the average
rank, then average the ranks. Ranking rather than normalising avoids having to
decide how a minute compares to a menu item.

THINGS TO DO
  guest_minutes        what one visitor can actually consume: ride and film
                       runtimes, plus ONE set of each live act, each act
                       discounted by how often it runs.
  Exhibits are reported but do not rank. A gallery is self paced and has no
  runtime, and the count only takes three values across eleven pavilions, so
  ranking on it gave a coarse count the same weight as measured minutes and
  pushed the two pavilions with the most to see down the table.

  An earlier version ranked ride runtime against entertainment minutes per
  day. Those are different units. A film's runtime is what one guest sees; a
  mariachi group's 175 minutes a day is the pavilion's output, of which a
  guest consumes one 25 minute set. Mixing them ranked France ninth while it
  holds the largest attraction lineup in World Showcase. Daily output is
  still reported, as context, but it does not rank.

  Shop counts are NOT here. Two sources were tried and both are wrong in
  opposite directions. A 2023 secondary list carries shops that have since
  closed. Disney's own rendered directory returns 33 park-wide and assigns
  zero to China, which visibly has a large shop. Neither is an inventory, so
  the measure is dropped rather than caveated.

FOOD AND DRINK
  venues               open permanent food and drink locations
  menu_items           distinct published items, a choice proxy
  signature            count of Disney Signature Dining rooms

AUTHENTICITY
  menu_native_share    share of items native to that country's cuisine
  ent_specific_share   share of live entertainment minutes in that country's
                       own tradition, coded from each act's own description
  arch_refs            named real buildings the pavilion reproduces, counted
                       from architecture.csv rather than copied into a second
                       file. A row counts only where a source names a
                       specific real structure, and a competing attribution
                       of an element already counted does not count twice.

  The American Adventure is excluded from this family. Coding items as native
  to the cuisine is meaningless when the country is the United States and the
  baseline "generic theme park food" is that country's food. It still ranks
  on the other families.
"""

import csv
import collections
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data") + os.sep

P = ["Mexico", "Norway", "China", "Germany", "Italy", "The American Adventure",
     "Japan", "Morocco", "France", "United Kingdom", "Canada"]

# Counted as a show under things-to-do, so not also live entertainment.
NOT_LIVE = {("The American Adventure", "The American Adventure")}

# Roving acts, excluded from pavilion totals. TouringPlans lists the EPCOT
# Pianist under the United Kingdom and its own page says "currently found in
# the Rose & Crown Pub", but the same page records it playing the American
# Adventure, the World Showplace building, and through Summer 2025 The
# Odyssey, which is not in World Showcase at all. An act documented in four
# buildings is not a property of one pavilion. It carried 20 of the UK's 45.7
# guest minutes and its first place, so --with-roving reports the other way.
ROVING = {("United Kingdom", "EPCOT Pianist")}

# Native-cuisine coding is not comparable for the USA pavilion.
NO_AUTHENTICITY = {"The American Adventure"}


def read(p):
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def rank(values, higher_is_better=True):
    scored = [(k, v) for k, v in values.items() if v is not None]
    scored.sort(key=lambda kv: kv[1], reverse=higher_is_better)
    out, i = {}, 0
    while i < len(scored):
        j = i
        while j + 1 < len(scored) and scored[j + 1][1] == scored[i][1]:
            j += 1
        for k in range(i, j + 1):
            out[scored[k][0]] = (i + j) / 2.0 + 1
        i = j + 1
    return out


def family(measures, members):
    per = [rank({k: v for k, v in m.items() if k in members})
           for m in measures]
    avg = {}
    for p in members:
        got = [r[p] for r in per if p in r]
        avg[p] = sum(got) / len(got) if got else None
    return rank({k: -v for k, v in avg.items() if v is not None}), per


def spearman(a, b):
    common = sorted(set(a) & set(b))
    n = len(common)
    d2 = sum((a[p] - b[p]) ** 2 for p in common)
    return 1 - (6 * d2) / (n * (n * n - 1)), n


def load(include_roving=False):
    static = {r["pavilion"]: r for r in read(DATA + "pavilions.csv")}

    arch_n = collections.Counter()
    for r in read(DATA + "architecture.csv"):
        if r["counted"] == "yes":
            arch_n[r["pavilion"]] += 1

    ent_rows = read(DATA + "entertainment.csv")
    dates = sorted({r["date"] for r in ent_rows})
    nd = len(dates)
    tot = collections.defaultdict(float)
    spec = collections.defaultdict(float)
    # One set of each act, discounted by the share of sampled dates it ran on.
    # Acts rotate, so a guest is not guaranteed to catch every act listed.
    seen = collections.defaultdict(set)
    setlen = {}
    for r in ent_rows:
        p = r["pavilion"]
        if p not in P or (p, r["act"]) in NOT_LIVE:
            continue
        if not include_roving and (p, r["act"]) in ROVING:
            continue
        m = float(r["daily_minutes"] or 0)
        tot[p] += m
        if r["specificity"] == "specific":
            spec[p] += m
        if m > 0:
            seen[(p, r["act"])].add(r["date"])
            try:
                setlen[(p, r["act"])] = float(r["set_minutes"])
            except ValueError:
                pass
    live_guest = collections.defaultdict(float)
    for key, ds in seen.items():
        if key in setlen:
            live_guest[key[0]] += setlen[key] * (len(ds) / float(nd))

    din = read(DATA + "dining.csv")
    venues = collections.defaultdict(set)
    sig = collections.defaultdict(set)
    items = collections.Counter()
    code = collections.defaultdict(collections.Counter)
    for r in din:
        p = r["pavilion"]
        if p not in P or r["status"] != "open":
            continue
        venues[p].add(r["venue"])
        if r["signature"] == "yes":
            sig[p].add(r["venue"])
        if r["item"]:
            items[p] += 1
        if r["cuisine_code"]:
            code[p][r["cuisine_code"]] += 1

    d = {}
    for p in P:
        denom = code[p]["NATIVE"] + code[p]["ADAPTED"] + code[p]["GENERIC"]
        d[p] = {
            "ride_film": float(static[p]["ride_film_min"]),
            "guest_min": float(static[p]["ride_film_min"]) + live_guest[p],
            "live_guest": live_guest[p],
            "ent_min": tot[p] / len(dates),
            "exhibits": int(static[p]["exhibits"]),
            "venues": len(venues[p]),
            "items": items[p],
            "signature": len(sig[p]),
            "native": code[p]["NATIVE"] / denom if denom else None,
            "ent_spec": (spec[p] / tot[p]) if tot[p] else None,
            "arch": arch_n[p],
            "coherence": static[p]["arch_coherence"],
            "unclear": code[p]["UNCLEAR"],
        }
    return d, len(dates)


def col(d, key, members=P):
    return {p: d[p][key] for p in members}


def main():
    import sys
    include_roving = "--with-roving" in sys.argv
    d, n_dates = load(include_roving)
    auth_members = [p for p in P if p not in NO_AUTHENTICITY]

    todo, _ = family([col(d, "guest_min")], P)
    food, _ = family([col(d, "venues"), col(d, "items"),
                      col(d, "signature")], P)
    auth, _ = family([col(d, "native", auth_members),
                      col(d, "ent_spec", auth_members),
                      col(d, "arch", auth_members)], auth_members)

    def table(title, order, cols, ranks):
        print("=" * 76)
        print(title)
        print("=" * 76)
        head = "%-24s" % "pavilion"
        for label, _, w in cols:
            head += ("%%%ds" % w) % label
        print(head + "   rank")
        for p in order:
            line = "%-24s" % p
            for _, fn, w in cols:
                line += ("%%%ds" % w) % fn(d[p])
            print(line + "   %4.1f" % ranks[p])
        print()

    table("THINGS TO DO        %d dates, roving acts %s" %
          (n_dates, "included" if include_roving else "excluded"),
          sorted(P, key=lambda p: todo[p]),
          [("ride/film", lambda r: "%.1f" % r["ride_film"], 11),
           ("live seen", lambda r: "%.1f" % r["live_guest"], 11),
           ("guest min", lambda r: "%.1f" % r["guest_min"], 11),
           ("exhibits", lambda r: r["exhibits"], 10),
           ("out/day", lambda r: "%.0f" % r["ent_min"], 9)], todo)

    table("FOOD AND DRINK",
          sorted(P, key=lambda p: food[p]),
          [("venues", lambda r: r["venues"], 8),
           ("items", lambda r: r["items"], 8),
           ("signature", lambda r: r["signature"], 11)], food)

    table("AUTHENTICITY        American Adventure excluded, see header",
          sorted(auth_members, key=lambda p: auth[p]),
          [("native", lambda r: "%.0f%%" % (r["native"] * 100), 9),
           ("ent spec", lambda r: ("%.0f%%" % (r["ent_spec"] * 100))
            if r["ent_spec"] is not None else "none", 10),
           ("arch", lambda r: r["arch"], 6),
           ("", lambda r: r["coherence"], 11)], auth)

    print("=" * 76)
    print("THE MATRIX")
    print("=" * 76)
    print("%-24s %8s %8s %8s" % ("pavilion", "things", "food", "authentic"))
    for p in sorted(P, key=lambda p: todo[p]):
        print("%-24s %8.1f %8.1f %8s" %
              (p, todo[p], food[p],
               "%.1f" % auth[p] if p in auth else "n/a"))

    print()
    for a, b, la, lb in ((todo, auth, "things to do", "authenticity"),
                         (todo, food, "things to do", "food"),
                         (food, auth, "food", "authenticity")):
        rho, n = spearman(a, b)
        print("  rho %-14s vs %-14s %+0.3f   (n=%d)" % (la, lb, rho, n))

    with open(DATA + "rankings.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["pavilion", "things_to_do_rank", "food_rank",
                    "authenticity_rank", "ride_film_min", "live_guest_min",
                    "guest_min", "live_min_day", "exhibits", "venues", "menu_items", "signature",
                    "menu_native_share", "ent_specific_share", "arch_refs",
                    "arch_coherence", "menu_items_unclear"])
        for p in P:
            r = d[p]
            w.writerow([p, todo[p], food[p],
                        auth.get(p, ""), r["ride_film"],
                        round(r["live_guest"], 1), round(r["guest_min"], 1),
                        round(r["ent_min"], 1), r["exhibits"], r["venues"],
                        r["items"], r["signature"],
                        "" if r["native"] is None else round(r["native"], 4),
                        "" if r["ent_spec"] is None else round(r["ent_spec"], 4),
                        r["arch"], r["coherence"], r["unclear"]])
    if not include_roving:
        alt, _ = load(True)
        at, _ = family([col(alt, "guest_min")], P)
        print()
        print("  sensitivity, counting the roving pianist as a UK act:")
        print("    United Kingdom things-to-do rank %.1f  (excluded: %.1f)"
              % (at["United Kingdom"], todo["United Kingdom"]))
    print("\nwrote data/rankings.csv")


if __name__ == "__main__":
    main()
