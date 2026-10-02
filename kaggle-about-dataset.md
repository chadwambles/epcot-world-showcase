Eleven country pavilions ring the lagoon at EPCOT's World Showcase. This is a
structured record of what is actually in each one, assembled in September 2026,
and three separate rankings built from it.

There is deliberately no overall score. Combining the rankings would need
weights, and any weighting is a choice presented as arithmetic.

## What is here

**1,513 menu rows**, every published item at all 44 operating food and drink
locations, each coded for whether the dish is native to that country's cuisine,
adapted for the park, or generic theme park food.

**Entertainment schedules** across seven sampled dates spanning two years and
four festivals, with each act coded for whether it performs in that country's
own tradition, and the quoted source phrase that establishes the coding.

**40 architectural references**, each naming the real building a pavilion
structure reproduces, its real city, the source, and a source reliability tier.

**The rankings themselves**, with every sub-measure exposed so you can
disagree with the weighting and rebuild it.

## The finding

Things to do, food, and authenticity give three unrelated answers.

France is the only pavilion good at all three. Norway is last on all three.
Japan is ninth in things to do and first in authenticity. Morocco is last on
two measures while carrying five documented real-building references and
entertainment entirely in its own tradition.

Spearman between the rankings runs +0.25 to +0.45. On eleven points you need
about 0.65 for significance, so none of these is distinguishable from zero.
The honest reading is that the three questions have three different answers,
not that there is a weak relationship.

## How authenticity is measured

Nothing here scores a culture. Every measure scores Disney's choices against
an external reference.

A menu item is native, adapted or generic by whether the dish belongs to that
cuisine. An act is specific or generic by whether its own published
description names a tradition and an origin. A building reference counts only
where a source names a specific real structure, which is why "Bavarian village
architecture" does not count and Burg Eltz does.

The American Adventure is excluded from the authenticity ranking. Coding items
as native is meaningless when the country is the United States and the
baseline "generic theme park food" is that country's food.

## Known limits

Eleven pavilions is eleven data points. Everything here is descriptive.

Menu coding has judgment in it, and every borderline call is written out in
the repository's dining notes. Buffet and prix fixe venues under-report on
item count because a buffet publishes as eight stations.

Shop counts are deliberately absent. Two sources were tried and both are wrong
in opposite directions: a 2023 secondary list carries closed shops, and
Disney's own directory assigns zero shops to China, which visibly has a large
one. `shops.csv` records the official directory as a snapshot so the absence is
checkable rather than asserted.

Some of this will age quickly. Germany has been under unannounced construction
since July 2026. Morocco's Restaurant Marrakesh has not served food since 2020
and Tangierine Cafe now runs as a rotating festival booth. Wondrous China was
announced in 2019 and never opened.

## A fourth ranking that did not work

A guest sentiment lens was attempted using r/epcot via the Arctic Shift
archive. 5,465 posts produced 807 pavilion-attributed segments, of which 788
said nothing evaluative at all. France had 153 attributed paragraphs and zero
that characterised the pavilion either way.

The labels were correct. r/epcot is a photo-and-questions subreddit and the
corpus does not contain the writing the measure needed. The full pipeline is
published in the repository, including the attribution dictionary and the
audit tooling, because it ran and the reason it failed is a real fact about
the source.

No post text, titles, usernames or links appear in this dataset.

## Sources

Dining and entertainment from TouringPlans, cross-checked against
RopeDropPlanner, collected 24 to 30 September 2026. Shop directory rendered
from disneyworld.disney.go.com. Architectural provenance primarily from D23,
with source tiers and disagreements recorded. Reddit via Arctic Shift.

Code, methodology notes and a full data dictionary:
https://github.com/chadwambles/epcot-world-showcase
