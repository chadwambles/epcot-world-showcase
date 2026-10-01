# Data dictionary

Six files in `data/`. Every one is derived; nothing here is hand-edited after
collection except `pavilions.csv`, which is noted below.

The eleven pavilions, used as the key throughout: Mexico, Norway, China,
Germany, Italy, The American Adventure, Japan, Morocco, France, United
Kingdom, Canada.

---

## rankings.csv

11 rows, one per pavilion. The output of `build_matrix.py`.

| column | type | description |
|---|---|---|
| `pavilion` | text | Pavilion name, the key across every file |
| `things_to_do_rank` | number | Rank on guest-consumable minutes. 1 is most. Ties share the average rank |
| `food_rank` | number | Rank averaged over venue count, menu breadth and signature dining count |
| `authenticity_rank` | number | Rank averaged over native menu share, entertainment specificity and building references. Blank for The American Adventure, which is excluded |
| `ride_film_min` | number | Total runtime of rides and films, in minutes |
| `live_guest_min` | number | One set of each live act, each discounted by the share of sampled dates it ran on |
| `guest_min` | number | `ride_film_min` + `live_guest_min`. What one visitor can consume. This is what things_to_do_rank sorts on |
| `live_min_day` | number | The pavilion's scheduled live performance output per day, averaged over sampled dates. Reported for context, does not rank |
| `exhibits` | integer | Galleries and walkthroughs. Reported, does not rank: self-paced spaces have no runtime and the count takes only three values |
| `venues` | integer | Open permanent food and drink locations |
| `menu_items` | integer | Distinct published menu items across the pavilion |
| `signature` | integer | Disney Signature Dining rooms. Only three exist in World Showcase |
| `menu_native_share` | number 0-1 | Share of coded items native to that country's cuisine. UNCLEAR items are left out of the denominator |
| `ent_specific_share` | number 0-1 | Share of live entertainment minutes performed in that country's own tradition. Blank where the pavilion has no scheduled entertainment, which is not the same as having generic entertainment |
| `arch_refs` | integer | Named real buildings the pavilion reproduces, counted from `architecture.csv` |
| `arch_coherence` | text | `coherent` where references come from one city or region, `pastiche` where they span distant regions. Reported, does not rank |
| `menu_items_unclear` | integer | Items that could not be coded either way, excluded from the native share |

---

## pavilions.csv

11 rows. Static facts assembled from `docs/inventory.md`. The one file in
`data/` entered by hand rather than derived, so it carries its own notes.

| column | type | description |
|---|---|---|
| `pavilion` | text | Pavilion name |
| `ride_film_min` | number | Total ride and film runtime |
| `ride_film_note` | text | Why the number is what it is, including the two disputed runtimes |
| `permanent_shops` | integer | Retail count. **Not used in any ranking.** Both available sources are unreliable, see the README |
| `exhibits` | integer | Galleries and walkthroughs |
| `arch_refs` | integer | Superseded by the count derived from `architecture.csv`. Kept for reference |
| `arch_coherence` | text | `coherent` or `pastiche` |

---

## dining.csv

1,513 rows, one per menu item per venue. Collected 24 to 30 September 2026.

| column | type | description |
|---|---|---|
| `pavilion` | text | Pavilion name |
| `venue` | text | Restaurant, kiosk or lounge name |
| `service_type` | text | `table service`, `quick service`, `lounge`, `kiosk` |
| `signature` | text | `yes` where Disney classifies it as Signature Dining |
| `price_tier` | text | Disney's own `$` to `$$$$` |
| `status` | text | `open` or `closed`. Closed venues are excluded from venue counts |
| `item` | text | Menu item name. Blank where a venue's menu could not be obtained, with the reason in `note` |
| `section` | text | `appetizer`, `entree`, `dessert`, `beverage` |
| `price` | text | As published, including the currency symbol |
| `cuisine_code` | text | `NATIVE`, `ADAPTED`, `GENERIC` or `UNCLEAR`. See below |
| `note` | text | Coding rationale, menu gaps, and whether an item is a festival offering at a permanent venue |

**Cuisine codes.** `NATIVE` is a dish that belongs to that country's cuisine.
`ADAPTED` is recognisably influenced by it but altered or invented for the
park. `GENERIC` is standard American theme park food with no connection to the
country. `UNCLEAR` is a genuine ambiguity, recorded rather than forced.

Soft drinks and domestic beer code `GENERIC`; a beer or wine from the country
codes `NATIVE`. The coding describes provenance only and makes no judgment
about quality. Every borderline call is written out in `docs/dining-notes.md`.

The American Adventure was coded on a different basis, because "generic
American theme park food" is that country's food. Its share is not comparable
to the other ten and it is excluded from the authenticity ranking.

---

## entertainment.csv

81 rows, one per act per sampled date. Seven dates between June 2025 and
September 2026, across four festivals and one non-festival day.

| column | type | description |
|---|---|---|
| `date` | date | Sampled date, YYYY-MM-DD |
| `pavilion` | text | Pavilion name, or a non-pavilion venue such as America Gardens Theatre, World Showcase Lagoon or park-wide |
| `act` | text | Act name as TouringPlans lists it |
| `performances` | integer | Sets scheduled that day |
| `set_minutes` | number | Published duration of one set |
| `daily_minutes` | number | `performances`  x  `set_minutes` |
| `specificity` | text | `specific` where the act's own published description names a tradition and an origin, `generic` where it does not |
| `evidence_quote` | text | The phrase from the source that establishes the specificity coding |
| `source_url` | url | The act's TouringPlans page |

Festival concert series at America Gardens Theatre, the nighttime lagoon show
and park-wide roving acts are kept in this file but excluded from pavilion
totals. They are not pavilion entertainment.

The American Adventure's 29-minute theater show appears here but is counted as
a show under things-to-do, not as live entertainment, so it is not double
counted.

---

## architecture.csv

40 rows, one per documented reference.

| column | type | description |
|---|---|---|
| `pavilion` | text | Pavilion name |
| `pavilion_element` | text | The structure at EPCOT |
| `real_structure` | text | The real building it reproduces |
| `real_location` | text | That building's city or region |
| `source_url` | url | Primary source for the connection |
| `source_tier` | text | T1 Disney official, T2 reference or published guidebook, T3 established fan reference, T4 individual blog |
| `disputed` | text | `yes` where sources disagree about which real building is the model |
| `counted` | text | `yes` where the row counts toward `arch_refs` |
| `not_counted_reason` | text | Why a row does not count |

**Counting rule.** A row counts only where a source names a specific real
structure. Style references such as "Bavarian village" or "Tudor", towns with
no named building, landscape features, and objects that are not buildings
(telephone boxes, totem poles, gondolas) are recorded in
`docs/architecture-notes.md` but not counted. A competing attribution of an
element already counted does not count a second time, which is why Mexico's
contested pyramid counts once.

Claims appearing only at T4 are excluded from the counted totals.

---

## shops.csv

32 rows. A snapshot of Disney's own shop directory, rendered in a browser
because the page builds its list client side and a plain fetch returns an
empty document.

| column | type | description |
|---|---|---|
| `shop` | text | Shop name as the directory lists it |
| `area` | text | Which part of EPCOT it sits in |
| `in_world_showcase` | text | `yes` only for the eleven country pavilions. The World Showcase entrance plaza, the African Outpost and the International Gateway are `no` |
| `pavilion` | text | Pavilion, where applicable |
| `note` | text | Why a shop is excluded, or its listed status |

**This file is a record, not an inventory, and no ranking uses it.** The
directory assigns zero shops to China, which visibly has a large one. It is
published so the shop measure's absence is checkable rather than asserted.
