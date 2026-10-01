#!/usr/bin/env python3
"""
pavilion_anchors.py

Builds the pavilion attribution dictionary.

Parks have unambiguous names. Pavilions are named after countries people
actually travel to, so "we loved Japan" is the pavilion in a trip report and
Tokyo in a travel post. Attribution therefore runs on venue and attraction
names first, which nobody uses about the real country, and falls back to the
bare country name only inside an EPCOT context.

TIER 1  unambiguous. A match attributes the paragraph on its own.
TIER 2  ambiguous. Only counts when the post or a nearby paragraph already
        establishes EPCOT, and never on its own against a tier 1 match for a
        different pavilion.

Most of tier 1 is generated from the collected inventory rather than typed
out, so rebuilding the inventory rebuilds the dictionary.

Usage:
    py pavilion_anchors.py --raw ../raw --out anchors.json
"""

import argparse
import csv
import json
import os
import re

PAVILIONS = ["Mexico", "Norway", "China", "Germany", "Italy",
             "The American Adventure", "Japan", "Morocco", "France",
             "United Kingdom", "Canada"]

# Attractions, films, galleries and the shorthand people actually type.
# Anything here is unambiguous in a theme park conversation.
TIER1_EXTRA = {
    "Mexico": ["Gran Fiesta Tour", "Three Caballeros", "San Angel",
               "Plaza de los Amigos", "La Cava", "Choza de Margarita",
               "Mexico pavilion", "the pyramid"],
    "Norway": ["Frozen Ever After", "Maelstrom", "Stave Church",
               "Akershus", "Kringla", "school bread", "Norway pavilion",
               "Anna and Elsa", "Royal Sommerhus"],
    "China": ["Reflections of China", "Wondrous China", "Nine Dragons",
              "Lotus Blossom", "House of Good Fortune",
              "House of the Whispering Willows", "Temple of Heaven",
              "Jeweled Dragon Acrobats", "China pavilion"],
    "Germany": ["Biergarten", "Sommerfest", "Karamell", "Weinkeller",
                "Volkskunst", "Stein Haus", "Die Weihnachts Ecke",
                "Germany pavilion", "Oktoberfest Musikanten",
                "the model train"],
    "Italy": ["Via Napoli", "Tutto Italia", "Tutto Gusto", "Gelateria Toscana",
              "Il Bel Cristallo", "Enoteca Castello", "Italy pavilion",
              "Ziti Sisters", "Sergio the juggler"],
    "The American Adventure": ["American Adventure", "Voices of Liberty",
                               "Regal Eagle", "Fife & Drum", "Fife and Drum",
                               "Block & Hans", "Block and Hans",
                               "American Heritage Gallery",
                               "Spirit of America"],
    "Japan": ["Teppan Edo", "Tokyo Dining", "Takumi-Tei", "Takumi Tei",
              "Katsura Grill", "Kabuki Cafe", "Shiki-Sai", "Mitsukoshi",
              "Bijutsu-kan", "Matsuriza", "Japan pavilion", "the pagoda",
              "Miyuki"],
    "Morocco": ["Restaurant Marrakesh", "Spice Road", "Tangierine",
                "Oasis Sweets", "Souk-Al-Magreb", "Souk Al Magreb",
                "Marketplace in the Medina", "Koutoubia", "Fez House",
                "Morocco pavilion", "Mo'Rockin", "MoRockin", "Atlas Fusion",
                "Gallery of Arts and History"],
    "France": ["Remy's Ratatouille", "Ratatouille Adventure",
               "Impressions de France", "Beauty and the Beast Sing",
               "Chefs de France", "Monsieur Paul", "Les Halles",
               "La Creperie", "L'Artisan des Glaces", "Artisan des Glaces",
               "Plume et Palette", "France pavilion", "Serveur Amusant",
               "the grey stuff"],
    "United Kingdom": ["Rose & Crown", "Rose and Crown", "Yorkshire County",
                       "The Tea Caddy", "Crown & Crest", "Crown and Crest",
                       "Sportsman's Shoppe", "Queen's Table",
                       "UK pavilion", "British Revolution",
                       "British Invasion", "Command Performance"],
    "Canada": ["Le Cellier", "Canada Far and Wide", "O Canada",
               "La Poutinerie", "Trading Post", "Victoria Gardens",
               "Hotel du Canada", "Canada pavilion", "Off Kilter",
               "the totem pole"],
}

# Ambiguous on their own. Require EPCOT context.
TIER2 = {
    "Mexico": ["Mexico", "Mexican"],
    "Norway": ["Norway", "Norwegian"],
    "China": ["China", "Chinese"],
    "Germany": ["Germany", "German"],
    "Italy": ["Italy", "Italian"],
    "The American Adventure": ["America", "American", "the USA pavilion"],
    "Japan": ["Japan", "Japanese"],
    "Morocco": ["Morocco", "Moroccan"],
    "France": ["France", "French", "Eiffel Tower"],
    "United Kingdom": ["UK", "United Kingdom", "Britain", "British",
                       "England", "English"],
    "Canada": ["Canada", "Canadian"],
}

# Establishes that a paragraph is about the park rather than the country.
EPCOT_CONTEXT = [
    "epcot", "world showcase", "walt disney world", "wdw", "disney world",
    "the parks", "park hopper", "genie", "lightning lane", "magic kingdom",
    "animal kingdom", "hollywood studios", "food and wine", "food & wine",
    "flower and garden", "festival of the arts", "drinking around the world",
    "drink around the world", "the promenade", "international gateway",
]


def clean(s):
    s = s.strip()
    # Venue names carry service suffixes that nobody types in a post.
    s = re.sub(r":\s.*$", "", s)
    s = re.sub(r"\s+(Restaurante?|Ristorante e Pizzeria|Steakhouse|"
               r"Department Store|Royal Banquet Hall|Dining Room|"
               r"Bakeri og Kafe|Wine Cellar|Boulangerie-Patisserie)$",
               "", s, flags=re.I)
    return s.strip()


def from_inventory(raw):
    """Venue, shop and act names collected for the ranking work."""
    out = {p: set() for p in PAVILIONS}

    def add(p, name):
        if p in out and name:
            out[p].add(name)
            c = clean(name)
            if c and c.lower() != name.lower() and len(c) > 4:
                out[p].add(c)

    def find(*names):
        for d in (raw, "."):
            for n in names:
                q = os.path.join(d, n)
                if os.path.exists(q):
                    return q
        return None

    found = []

    q = find("dining.csv", "epcot-dining.csv")
    if q:
        found.append(q)
        for r in csv.DictReader(open(q, newline="", encoding="utf-8")):
            add(r["pavilion"], r["venue"])

    q = find("shops_official.csv", "epcot-shops.csv")
    if q:
        found.append(q)
        for r in csv.DictReader(open(q, newline="", encoding="utf-8")):
            if r.get("in_world_showcase") == "yes":
                add(r["pavilion"], r["shop"])

    q = find("entertainment.csv", "epcot-entertainment.csv")
    if q:
        found.append(q)
        for r in csv.DictReader(open(q, newline="", encoding="utf-8")):
            add(r["pavilion"], r["act"])

    # Falling back to the curated list alone drops roughly a third of the
    # anchors and quietly halves attribution. Better to stop than to build a
    # worse dictionary that still looks like it worked.
    if not found:
        raise SystemExit(
            "Found none of dining.csv, entertainment.csv or "
            "shops_official.csv in %r or the current directory.\n"
            "Without them this builds a much weaker dictionary. Point --raw "
            "at the folder holding the collected inventory, or just use the "
            "anchors.json that shipped with this pipeline." % raw)
    print("  built from: %s" % ", ".join(os.path.basename(f) for f in found))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../raw")
    ap.add_argument("--out", default="anchors.json")
    args = ap.parse_args()

    auto = from_inventory(args.raw)
    tier1 = {}
    for p in PAVILIONS:
        s = set(auto[p]) | set(TIER1_EXTRA.get(p, []))
        # Drop anything so short or so common it would fire on ordinary prose.
        s = {a for a in s if len(a) >= 5}
        tier1[p] = sorted(s, key=lambda a: (-len(a), a.lower()))

    # A string that names two pavilions is useless for attribution.
    seen = {}
    for p in PAVILIONS:
        for a in tier1[p]:
            seen.setdefault(a.lower(), []).append(p)
    clashes = {a: ps for a, ps in seen.items() if len(ps) > 1}
    for a in clashes:
        for p in PAVILIONS:
            tier1[p] = [x for x in tier1[p] if x.lower() != a]

    doc = {
        "pavilions": PAVILIONS,
        "tier1": tier1,
        "tier2": TIER2,
        "epcot_context": EPCOT_CONTEXT,
        "dropped_as_ambiguous": {a: ps for a, ps in clashes.items()},
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)

    print("=" * 62)
    print("PAVILION ANCHORS")
    print("=" * 62)
    for p in PAVILIONS:
        print("  %-24s %3d tier 1   %2d tier 2"
              % (p, len(tier1[p]), len(TIER2[p])))
    print("  %-24s %3d" % ("total tier 1", sum(len(v) for v in tier1.values())))
    if clashes:
        print("\n  dropped for naming two pavilions:")
        for a, ps in sorted(clashes.items()):
            print("    %-30s %s" % (a, ", ".join(ps)))
    print("\nwrote %s" % args.out)


if __name__ == "__main__":
    main()
