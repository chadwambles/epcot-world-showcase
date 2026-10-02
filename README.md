# EPCOT World Showcase

Three separate rankings of the eleven country pavilions, and what happens when
you compare them.

There is deliberately no overall score. Combining the three would need weights,
and any weighting is a choice presented as arithmetic.

## The result

| pavilion | things to do | food | authenticity |
|---|---|---|---|
| The American Adventure | 1 | 6 | n/a |
| France | 2 | 1 | 2 |
| Mexico | 3 | 3.5 | 7 |
| United Kingdom | 4 | 8 | 5 |
| Germany | 5 | 9 | 3 |
| Canada | 6 | 5 | 8 |
| Italy | 7 | 3.5 | 4 |
| China | 8 | 7 | 9 |
| Japan | 9 | 2 | 1 |
| Norway | 10 | 10 | 10 |
| Morocco | 11 | 11 | 6 |

Spearman between the three: things and authenticity +0.25, things and food
+0.45, food and authenticity +0.41. On ten or eleven points you need about
0.65 for significance at p = 0.05, so **none of these is distinguishable from
zero.** The honest reading is that the three questions have three unrelated
answers, not that there is a weak positive relationship.

**Two pavilions are consistent.** France is 2nd, 1st and 2nd, the only one
good at everything, with the highest native menu share in the park at 76%.
Norway is 10th, 10th and 10th: a Frozen ride, a 22% native menu, two
architectural references and no scheduled live entertainment on any sampled
date.

**Everything between them depends which question you ask.** Japan is 9th in
things to do and 1st in authenticity. Germany is 3rd in authenticity and 9th
in food. Morocco is last on two measures: five documented real-building
references, entertainment entirely in its own tradition, one shop left, and
that shop now sells Disney merchandise.

## What each ranking measures

Within a family, every pavilion is ranked on each sub-measure, ties share the
average rank, and the ranks are averaged. Ranking rather than normalising
avoids having to decide how a minute compares to a menu item.

**Things to do.** Minutes of programmed content one visitor can actually
consume: ride and film runtimes, plus one set of each live act, each act
discounted by how often it runs. Not minutes per day. A film's runtime is what
a guest sees; 175 minutes a day of mariachi is the pavilion's output, of which
a guest catches one 25 minute set. Daily output is reported alongside but does
not rank.

**Food and drink.** Venue count by service type, menu breadth, and count of
Disney Signature Dining rooms. There are exactly three in World Showcase: Le
Cellier, Monsieur Paul and Takumi-Tei.

**Authenticity.** Share of menu items native to that country's cuisine, share
of live entertainment minutes performed in that country's own tradition, and
the count of named real buildings the pavilion reproduces.

Quantity belongs to things-to-do and character belongs to authenticity. A
pavilion's entertainment minutes count in one and its entertainment tradition
in the other. Counting the same fact in both would make the two rankings agree
by construction.

## Measurement rules worth knowing

**Nothing here scores a culture.** Every authenticity measure scores Disney's
choices against an external reference. A menu item is native, adapted or
generic by whether the dish belongs to that cuisine. An act is specific or
generic by whether its own published description names a tradition and an
origin. A building reference counts only where a source names a specific real
structure.

**The American Adventure is excluded from authenticity.** Coding items as
native to the cuisine is meaningless when the country is the United States and
the baseline "generic theme park food" is that country's food. It still ranks
on the other two.

**Shop counts are not used.** Two sources were tried and both are wrong in
opposite directions. A 2023 secondary list carries shops that have since
closed. Disney's own rendered directory returns 33 park-wide and assigns zero
to China, which visibly has a large shop. `data/shops.csv` records the
official directory as a snapshot; neither source is an inventory, so the
measure was dropped rather than caveated.

**One roving act is excluded.** TouringPlans lists the EPCOT Pianist under the
United Kingdom and its own page says it is currently in the Rose & Crown Pub,
but the same page records it playing the American Adventure, the World
Showplace building, and through Summer 2025 The Odyssey, which is not in World
Showcase at all. It carried 20 of the UK's 45.7 guest minutes and its first
place. `py build_matrix.py --with-roving` reports the other way.

## Repository

```
build_matrix.py          builds all three rankings and prints the matrix
data/
  rankings.csv           the result, with every sub-measure
  pavilions.csv          static per pavilion facts
  dining.csv             1,513 menu rows coded native / adapted / generic
  entertainment.csv      acts by sampled date, with specificity and evidence
  architecture.csv       40 real building references with source and tier
  shops.csv              Disney's own shop directory, as a snapshot
notebooks/
  epcot-world-showcase-starter.ipynb   loads the data, draws the three
                         rankings against each other, and checks whether any
                         of the correlation survives the sample size
docs/
  data-dictionary.md     every column in every file
  inventory.md           attractions, films, galleries, shops per pavilion
  dining-notes.md        venue list, coding rules, every borderline call
  entertainment-notes.md per date, per pavilion, with quoted evidence
  architecture-notes.md  full provenance research, source disagreements noted
sentiment/               a fourth ranking that was attempted and dropped
```

Rebuild:

```
py build_matrix.py
```

Pure standard library. No numpy, no pandas.

## The ranking that was dropped

`sentiment/` holds a complete pipeline for a fourth lens, measuring how
visitors describe each pavilion, built on r/epcot via the Arctic Shift
archive. It is published because it ran, not because it worked.

5,465 posts produced 6,820 segments, of which 807 attributed to a pavilion.
Labeling those returned **788 of 802 saying nothing evaluative at all.** Only
77 segments carried any signal, and the best-served pavilion had ten. France
had 153 attributed paragraphs and zero that characterised the pavilion either
way.

That is not a labeling failure. The labels are correct and r/epcot is a
photo-and-questions subreddit: "The Japan pavilion during a full moon", "Can
you buy the sauces from Regal Eagle?" The corpus does not contain the writing
the measure needed.

The scoring script now withholds a score below fifteen observations rather
than printing a ratio off one, which is what an earlier run did, reporting
Germany at a perfect 1.00 on a single paragraph.

One finding survived. `missing_entertainment`, the code expected to be too
sparse to use, fired 27 times and was the densest of the four. Ten of them are
Norway. People miss Maelstrom.

## Limitations

**Eleven pavilions is eleven data points.** Every correlation here is
underpowered by construction. The rankings are descriptive.

**Menu coding has judgment in it.** The rules and every borderline call are
written out in `docs/dining-notes.md`. Karamell-Kuche is the shakiest block:
Werther's is a German brand and the venue's whole premise, but a snickerdoodle
sandwich is not German food, and that one kiosk moves Germany's generic share
noticeably on its own.

**Prix fixe and buffet venues are not comparable on item count.** A buffet
publishes as eight stations. Biergarten, Akershus, Takumi-Tei and Monsieur
Paul all under-report against an a la carte menu of the same size.

**Entertainment is seven sampled dates.** Acts rotate, with most taking two
days off a week, so a single day would misrepresent any pavilion. Seven dates
across two years and four festivals is better than one and is still a sample.

**Two runtimes are disputed.** Gran Fiesta Tour is given as 5 to 8 minutes
depending on source, Canada Far and Wide as 12 to 15. Midpoints are used and
flagged in `data/pavilions.csv`.

**Some of this will go stale quickly.** Germany has been under unannounced
construction since July 2026. Morocco's Restaurant Marrakesh has not served
food since 2020 and Tangierine Cafe now runs as a rotating festival booth.
Wondrous China was announced in 2019 and never opened.

## Sources

Dining and entertainment from TouringPlans, cross-checked against
RopeDropPlanner, collected 24 to 30 September 2026. Shop directory from
disneyworld.disney.go.com, rendered rather than fetched. Architectural
provenance primarily from D23, with source tiers and disagreements recorded in
`docs/architecture-notes.md`. Reddit posts via the Arctic Shift archive.

No post text, titles, usernames or links are published in this repository.

Kaggle: https://www.kaggle.com/datasets/chadwambles/epcot-world-showcase
Tableau Dashboard: [https://public.tableau.com/views/EPCOTWorldShowcaseThreeRankingsThatDisagree/EPCOTArounttheWorldDashboard](https://public.tableau.com/views/EPCOTWorldShowcaseThreeRankingsThatDisagree/ThreeRankingsThatDisagree?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
