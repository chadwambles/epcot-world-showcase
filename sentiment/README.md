# Guest sentiment pipeline, EPCOT pavilion study

The fourth ranking. Everything here runs on your machine, because the
container this was built in cannot reach Arctic Shift or the API.

Pure standard library. No numpy, no requests, no SDK.

## Before you start

Add these to `.gitignore` before the first run. All three carry post text.

```
data/segments_local.jsonl
data/labels_raw.jsonl
audit_sample.csv
labels_qa.csv
```

`ANTHROPIC_API_KEY` must already be in your shell. Do not put it on a command
line and do not write it into a file.

## Order

Commands below are the whole line. Nothing after them is part of the
command, which is how the first run picked up `posts per year` as arguments.

### 1. Census before you commit

```
py fetch_repcot.py --census
```

Posts per year for r/epcot. You picked the source with the best attribution
precision and the least text, then split it across eleven pavilions. If the
early years are thin, you will know now rather than after labeling.

### 2. Pull

```
py fetch_repcot.py --from 2015-01-01 --to 2026-09-30
```

Writes `data/epcot_posts.jsonl`. It refuses to append to an existing file, so
a half finished run can never be silently merged into a new one.

Add `--comments` only if posts alone come back thin. Comments multiply volume
and add noise in roughly equal measure.

### 3. The anchor dictionary

`anchors.json` ships with this pipeline already built. 167 tier 1 anchors.
**You do not need to run `pavilion_anchors.py`, and running it without the
collected inventory alongside will make the dictionary worse.**

It is included so the dictionary is reproducible rather than a magic file. It
now refuses to run when it cannot find the inventory CSVs, instead of quietly
falling back to the curated list alone, which is what cut the first run from
167 anchors to 117 and roughly halved attribution.

To rebuild it, keep `epcot-dining.csv` and `epcot-entertainment.csv` in the
same folder and run:

```
py pavilion_anchors.py
```

Tier 1 is unambiguous. Nobody says "Le Cellier" about the country Canada.
Tier 2 is bare country names and only counts inside EPCOT context.

### 4. Segment and attribute

```
py segment_attribute.py --posts data/epcot_posts.jsonl --assume-epcot
```

**`--assume-epcot` is required for r/epcot.** Every post there is about EPCOT,
so also demanding a context word inside the text threw away 1,148 segments on
the first run. Leave the flag off for a general subreddit such as
r/WaltDisneyWorld, where a post really can be about a trip to Japan.

Titles are segmented in their own right, with a five word floor. 72 percent of
r/epcot posts have no body at all and the median title is nine words, so a
body-only pass discarded two thirds of the corpus.

On your 5,465 posts this gives 807 attributed segments and no pavilion under
30. The thinnest are China and Germany at 41.

Writes `segment_index.csv`, which is publishable, and `segments_local.jsonl`,
which is not.

### 5. Audit the attribution before labeling anything

```
py audit_attribution.py --sample
```

220 rows, 20 per pavilion. Open `audit_sample.csv`, fill the verdict column with y, n or `?`, save.

```
py audit_attribution.py --score
```

Precision by pavilion and by basis, with Wilson intervals. Stratified,
because tier 2 matches on a bare country name will be wrong more often than
tier 1 matches on a venue name, and a pooled number would hide it.

Do this before labeling. Labeling paragraphs that are attributed to the wrong
pavilion costs money and produces a confidently wrong ranking.

### 6. Label

```
py label_pavilions.py --limit 50     # look at the output first
py label_pavilions.py
```

Two paragraphs per request. **Do not raise `BATCH`.** On the park study,
packing eight held overall agreement at 93% while losing 41% of queue
detections and 29% of price detections. The losses were one sided and the
aggregate metric hid them.

Resumable. If it dies, rerun the same command and it picks up.

### 7. Score

```
py score_sentiment.py
```

Writes `sentiment_ranking.csv`, which carries no post text. Pavilions under
the 30 paragraph floor keep their number and their count but are not ranked,
the same treatment the park study gave thin cells.

## The four codes

| code | what it captures |
|---|---|
| `feel` | transporting, themed retail, mixed, not stated |
| `drivers` | which aspects the author credits or blames, and which way |
| `missing_entertainment` | they say an act or show is gone |
| `dwell` | lingered, walked through, not stated |

Three of the four rank. `missing_entertainment` is counted and reported but
does not rank: it is rare and skews toward long time visitors. A handful of
people saying they miss the taiko drummers is a good paragraph in the write
up and a bad statistic.

## What is deliberately not here

The model is never asked to score a pavilion, rank anything, or judge
authenticity. It reads a paragraph and reports what it says. Pavilion
attribution happens in code, in `segment_attribute.py`, where it can be
audited. Authenticity is measured separately from menus, acts and
architecture, and must stay separate: a property and a perception are
different variables, and merging them is the standard way this kind of
analysis goes wrong.

## Known attribution quirk

America Gardens Theatre physically stands at the American Adventure but hosts
the festival concert series, so a post about Eat to the Beat would otherwise
read as the USA pavilion. The phrase is stripped before matching. If the audit
turns up others of this kind, add them to `NOT_PAVILION` in
`segment_attribute.py` and rerun.

## Tested

The segmentation, attribution, audit and scoring steps were run end to end
against synthetic posts covering every branch: tier 1, tier 2 with and
without EPCOT context, multi-pavilion at both tiers, and no anchor. The
scoring recovered a planted signal correctly.

Segmentation and attribution were then tuned against your actual 5,465 post
pull, and a sample of tier 2 attributions was read by hand before shipping.

The label step could not be tested, because the build environment cannot
reach the API. Run it with `--limit 50` first and read the output.
