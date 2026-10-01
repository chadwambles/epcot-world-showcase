# EPCOT World Showcase pavilion live-entertainment minutes per day

Source: TouringPlans EPCOT date-addressable showtimes pages (default sort is by land) plus each act's own TouringPlans attraction page for set length, location and description.

## Method and caveats

- **TouringPlans does NOT group World Showcase by pavilion.** The `?sort=land` view (which is the default, no query param) groups only into the park's four neighborhoods: World Celebration, World Discovery, World Nature, World Showcase. Every pavilion act lands in one undifferentiated "World Showcase" list, sorted alphabetically. Pavilion attribution here comes from each act's own TouringPlans attraction page, which states the pavilion.
- `?sort=land` as a literal query string is not a valid value on the site. It falls back to alphabetical-by-show. The land-grouped view is the bare date URL.
- Set lengths are the `Duration` fact-box value on each act's TouringPlans attraction page.
- Dates sampled are all in the past, so their schedules are actual rather than unreleased. Future dates (checked 2026-10-01 and 2026-08-03) return partial or unreleased schedules and were excluded.
- **The American Adventure** is included in the pavilion tables because TouringPlans lists it as a World Showcase show, but it is an audio-animatronic theater attraction, not live performers. A second table excludes it.
- **EPCOT Pianist is attributed to the United Kingdom but does not always sit there.** Its act page says: "Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion. During festivals that use the large World Showplace building behind the Canada and UK Pavilions, the pianist has sometimes performed there. During Summer 2025, the EPCOT Pianist is performing in The Odyssey building between the Test Track and Mexico Pavilions." So the 120-140 min/day it contributes to the UK total is the single least secure pavilion attribution in this dataset, and on 2025-06-10 it was probably not in the UK pavilion at all.
- Overlap is not deduplicated: 'daily minutes' is stage-time supplied, not wall-clock coverage. Some acts overlap each other in time.

## Dates sampled

| Date | Festival | Park hours |
|---|---|---|
| 2025-06-10 | none listed | 9:00am-9:00pm |
| 2025-11-11 | EPCOT International Food & Wine Festival | 9:00am-9:00pm |
| 2026-01-26 | EPCOT International Festival of the Arts | 9:00am-9:00pm |
| 2026-03-16 | EPCOT International Flower & Garden Festival | 9:00am-9:00pm |
| 2026-09-08 | EPCOT International Food & Wine Festival | 9:00am-9:00pm |
| 2026-09-29 | EPCOT International Food & Wine Festival | 9:00am-9:00pm |
| 2026-09-30 | EPCOT International Food & Wine Festival | 9:00am-9:00pm |

### Pavilion daily performance minutes (as TouringPlans lists them, incl. The American Adventure theater show)

| Pavilion | 2025-06-10 | 2025-11-11 | 2026-01-26 | 2026-03-16 | 2026-09-08 | 2026-09-29 | 2026-09-30 | Average |
|---|---|---|---|---|---|---|---|---|
| Mexico | 175 | 175 | 175 | 175 | 175 | 175 | 175 | **175.0** |
| Norway | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| China | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| Germany | 120 | 120 | 120 | 120 | 120 | 120 | 0 | **102.9** |
| Italy | 140 | 140 | 0 | 0 | 140 | 140 | 140 | **100.0** |
| The American Adventure | 381 | 394 | 381 | 381 | 381 | 381 | 381 | **382.9** |
| Japan | 0 | 105 | 105 | 105 | 0 | 0 | 0 | **45.0** |
| Morocco | 0 | 0 | 0 | 105 | 0 | 0 | 105 | **30.0** |
| France | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| United Kingdom | 290 | 270 | 270 | 270 | 270 | 270 | 120 | **251.4** |
| Canada | 0 | 0 | 0 | 0 | 0 | 0 | 125 | **17.9** |

### Pavilion daily LIVE-performer minutes only (The American Adventure theater show removed)

| Pavilion | 2025-06-10 | 2025-11-11 | 2026-01-26 | 2026-03-16 | 2026-09-08 | 2026-09-29 | 2026-09-30 | Average |
|---|---|---|---|---|---|---|---|---|
| Mexico | 175 | 175 | 175 | 175 | 175 | 175 | 175 | **175.0** |
| Norway | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| China | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| Germany | 120 | 120 | 120 | 120 | 120 | 120 | 0 | **102.9** |
| Italy | 140 | 140 | 0 | 0 | 140 | 140 | 140 | **100.0** |
| The American Adventure | 91 | 104 | 91 | 91 | 91 | 91 | 91 | **92.9** |
| Japan | 0 | 105 | 105 | 105 | 0 | 0 | 0 | **45.0** |
| Morocco | 0 | 0 | 0 | 105 | 0 | 0 | 105 | **30.0** |
| France | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0.0** |
| United Kingdom | 290 | 270 | 270 | 270 | 270 | 270 | 120 | **251.4** |
| Canada | 0 | 0 | 0 | 0 | 0 | 0 | 125 | **17.9** |

## Per date, per pavilion detail


### 2025-06-10 ,  none listed

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  140 min total

- *Sergio* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:50am, 12:35pm, 1:20pm, 2:15pm, 3:10pm, 3:55pm, 4:40pm
  - Specificity: **generic** ,  evidence: "An entertaining juggling act that involves the crowd watching the show. Performs in the Italy Pavilion in World Showcase."
  - Source: https://touringplans.com/epcot/attractions/sergio

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  no scheduled acts.

**Morocco** ,  no scheduled acts.

**France** ,  no scheduled acts.

**United Kingdom** ,  290 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:30pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:30am, 12:30pm, 1:30pm, 2:30pm, 3:30pm, 4:30pm, 5:30pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *JAMMitors* (roving, Park-wide (roving)) ,  6 x 10 min = **60 min**; showtimes 9:30am, 10:30am, 11:30am, 12:55pm, 1:55pm, 2:55pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2025-11-11 ,  EPCOT International Food & Wine Festival

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  140 min total

- *Sergio* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:50am, 12:35pm, 1:20pm, 2:15pm, 3:10pm, 3:55pm, 4:40pm
  - Specificity: **generic** ,  evidence: "An entertaining juggling act that involves the crowd watching the show. Performs in the Italy Pavilion in World Showcase."
  - Source: https://touringplans.com/epcot/attractions/sergio

**The American Adventure** ,  394 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  8 performances x 13 min = **104 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 4:00pm, 5:00pm, 6:00pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  105 min total

- *Matsuriza* ,  7 performances x 15 min = **105 min**
  - Showtimes: 11:00am, 12:00pm, 1:00pm, 2:00pm, 3:00pm, 4:00pm, 4:45pm
  - Specificity: **specific** ,  evidence: "Matsuriza is a Japanese Taiko drum show that performs in the Japan pavilion."
  - Source: https://touringplans.com/epcot/attractions/matsuriza

**Morocco** ,  no scheduled acts.

**France** ,  no scheduled acts.

**United Kingdom** ,  270 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:30pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Eat to the Beat Concert Series* (festival_concert, America Gardens Theatre) ,  3 x 35 min = **105 min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "World Showcase at EPCOT, specifically the America Gardens Theatre on the lagoon opposite the American Adventure Pavilion" ,  https://touringplans.com/epcot/attractions/eat-to-the-beat-concerts
- *JAMMitors* (roving, Park-wide (roving)) ,  6 x 10 min = **60 min**; showtimes 9:30am, 10:30am, 11:30am, 12:55pm, 1:55pm, 2:55pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2026-01-26 ,  EPCOT International Festival of the Arts

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  no scheduled acts.

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  105 min total

- *Matsuriza* ,  7 performances x 15 min = **105 min**
  - Showtimes: 11:00am, 12:00pm, 1:00pm, 2:00pm, 3:00pm, 4:00pm, 4:45pm
  - Specificity: **specific** ,  evidence: "Matsuriza is a Japanese Taiko drum show that performs in the Japan pavilion."
  - Source: https://touringplans.com/epcot/attractions/matsuriza

**Morocco** ,  no scheduled acts.

**France** ,  no scheduled acts.

**United Kingdom** ,  270 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:30pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Disney on Broadway Concert Series* (festival_concert, America Gardens Theatre) ,  3 x unknown min = **unknown min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "Live Broadway Performers (showtimes listing description; no act page duration found)" ,  https://c.touringplans.com/epcot/showtimes/date/2026-01-26
- *JAMMitors* (roving, Park-wide (roving)) ,  6 x 10 min = **60 min**; showtimes 9:30am, 10:30am, 11:30am, 12:55pm, 1:55pm, 2:55pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2026-03-16 ,  EPCOT International Flower & Garden Festival

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  no scheduled acts.

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  105 min total

- *Matsuriza* ,  7 performances x 15 min = **105 min**
  - Showtimes: 11:00am, 12:00pm, 1:00pm, 2:00pm, 3:00pm, 4:00pm, 4:45pm
  - Specificity: **specific** ,  evidence: "Matsuriza is a Japanese Taiko drum show that performs in the Japan pavilion."
  - Source: https://touringplans.com/epcot/attractions/matsuriza

**Morocco** ,  105 min total

- *Atlas Fusion* ,  7 performances x 15 min = **105 min**
  - Showtimes: 12:35pm, 1:20pm, 2:20pm, 3:20pm, 5:00pm, 6:00pm, 7:10pm
  - Specificity: **specific** ,  evidence: "Traditional Gnawa and Moroccan music on the World Showcase Promenade outside the Morocco Pavilion."
  - Source: https://touringplans.com/epcot/attractions/atlas-fusion

**France** ,  no scheduled acts.

**United Kingdom** ,  270 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:30pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Garden Rocks Concert Series* (festival_concert, America Gardens Theatre) ,  3 x 30 min = **90 min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "Musical acts from the past perform in Garden Rocks Concerts that take place in America Gardens Theatre daily during EPCOT's International Flower & Garden Festival each year." ,  https://touringplans.com/epcot/attractions/garden-rocks-concert-series
- *JAMMitors* (roving, Park-wide (roving)) ,  6 x 10 min = **60 min**; showtimes 9:30am, 10:30am, 11:30am, 12:55pm, 1:55pm, 2:55pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2026-09-08 ,  EPCOT International Food & Wine Festival

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  140 min total

- *Sergio* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:50am, 12:35pm, 1:20pm, 2:15pm, 3:10pm, 3:55pm, 4:40pm
  - Specificity: **generic** ,  evidence: "An entertaining juggling act that involves the crowd watching the show. Performs in the Italy Pavilion in World Showcase."
  - Source: https://touringplans.com/epcot/attractions/sergio

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  no scheduled acts.

**Morocco** ,  no scheduled acts.

**France** ,  no scheduled acts.

**United Kingdom** ,  270 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:30pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Eat to the Beat Concert Series* (festival_concert, America Gardens Theatre) ,  3 x 35 min = **105 min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "World Showcase at EPCOT, specifically the America Gardens Theatre on the lagoon opposite the American Adventure Pavilion" ,  https://touringplans.com/epcot/attractions/eat-to-the-beat-concerts
- *JAMMitors* (roving, Park-wide (roving)) ,  7 x 10 min = **70 min**; showtimes 8:30am, 9:30am, 10:30am, 11:30am, 1:00pm, 2:00pm, 3:00pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *Max & Aydar - Amazing Masters of Variety* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:15am, 10:15am, 11:15am, 12:15pm, 1:15pm, 2:15pm
  - Specificity: **generic** ,  evidence: "Entertaining duo that juggles, balances, and generally entertains." ,  https://touringplans.com/epcot/attractions/max-aydar
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2026-09-29 ,  EPCOT International Food & Wine Festival

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  120 min total

- *Entertainment at Germany Gazebo* ,  6 performances x 20 min = **120 min**
  - Showtimes: 12:40pm, 1:30pm, 2:35pm, 3:55pm, 5:00pm, 6:05pm
  - Specificity: **specific** ,  evidence: "See German (mostly musical) performers in the Germany Gazebo, just east of the main Germany Pavilion buildings."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-germany-gazebo

**Italy** ,  140 min total

- *Sergio* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:50am, 12:35pm, 1:20pm, 2:15pm, 3:10pm, 3:55pm, 4:40pm
  - Specificity: **generic** ,  evidence: "An entertaining juggling act that involves the crowd watching the show. Performs in the Italy Pavilion in World Showcase."
  - Source: https://touringplans.com/epcot/attractions/sergio

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  no scheduled acts.

**Morocco** ,  no scheduled acts.

**France** ,  no scheduled acts.

**United Kingdom** ,  270 min total

- *Command Performance* ,  5 performances x 30 min = **150 min**
  - Showtimes: 3:00pm, 4:15pm, 5:55pm, 7:00pm, 8:00pm
  - Specificity: **specific** ,  evidence: "Cover band that plays classic British rock and roll."
  - Source: https://touringplans.com/epcot/attractions/command-performance
- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  no scheduled acts.

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Eat to the Beat Concert Series* (festival_concert, America Gardens Theatre) ,  3 x 35 min = **105 min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "World Showcase at EPCOT, specifically the America Gardens Theatre on the lagoon opposite the American Adventure Pavilion" ,  https://touringplans.com/epcot/attractions/eat-to-the-beat-concerts
- *JAMMitors* (roving, Park-wide (roving)) ,  7 x 10 min = **70 min**; showtimes 8:30am, 9:30am, 10:30am, 11:30am, 1:00pm, 2:00pm, 3:00pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *Max & Aydar - Amazing Masters of Variety* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:15am, 10:15am, 11:10am, 12:15pm, 1:10pm, 2:10pm
  - Specificity: **generic** ,  evidence: "Entertaining duo that juggles, balances, and generally entertains." ,  https://touringplans.com/epcot/attractions/max-aydar
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


### 2026-09-30 ,  EPCOT International Food & Wine Festival

#### Pavilion acts

**Mexico** ,  175 min total

- *Mariachi Cobre* ,  7 performances x 25 min = **175 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 3:00pm, 3:45pm, 4:30pm
  - Specificity: **specific** ,  evidence: "Mariachi Cobre is a long-standing Mariachi band that performs on the steps of the Mexico Pavilion."
  - Source: https://touringplans.com/epcot/attractions/mariachi-cobre

**Norway** ,  no scheduled acts.

**China** ,  no scheduled acts.

**Germany** ,  no scheduled acts.

**Italy** ,  140 min total

- *Sergio* ,  7 performances x 20 min = **140 min**
  - Showtimes: 11:50am, 12:35pm, 1:20pm, 2:15pm, 3:10pm, 3:55pm, 4:40pm
  - Specificity: **generic** ,  evidence: "An entertaining juggling act that involves the crowd watching the show. Performs in the Italy Pavilion in World Showcase."
  - Source: https://touringplans.com/epcot/attractions/sergio

**The American Adventure** ,  381 min total

- *The American Adventure* ,  10 performances x 29 min = **290 min**
  - Showtimes: 11:45am, 12:30pm, 1:15pm, 2:00pm, 2:45pm, 3:30pm, 4:30pm, 5:30pm, 6:30pm, 7:30pm
  - Specificity: **specific** ,  evidence: "Patriotic mixed-media and audio-animatronic theater presentation on U.S. history"
  - Source: https://touringplans.com/epcot/attractions/american-adventure
- *Voices of Liberty* ,  7 performances x 13 min = **91 min**
  - Showtimes: 11:15am, 12:00pm, 12:45pm, 1:30pm, 2:15pm, 3:00pm, 3:45pm
  - Specificity: **specific** ,  evidence: "Voices of Liberty is a popular a cappella group with a classic Americana repertoire."
  - Source: https://touringplans.com/epcot/attractions/voices-of-liberty

**Japan** ,  no scheduled acts.

**Morocco** ,  105 min total

- *Atlas Fusion* ,  7 performances x 15 min = **105 min**
  - Showtimes: 12:35pm, 1:20pm, 2:20pm, 3:20pm, 5:00pm, 6:00pm, 7:10pm
  - Specificity: **specific** ,  evidence: "Traditional Gnawa and Moroccan music on the World Showcase Promenade outside the Morocco Pavilion."
  - Source: https://touringplans.com/epcot/attractions/atlas-fusion

**France** ,  no scheduled acts.

**United Kingdom** ,  120 min total

- *EPCOT Pianist* ,  6 performances x 20 min = **120 min**
  - Showtimes: 1:30pm, 2:15pm, 4:00pm, 5:00pm, 6:00pm, 7:00pm
  - Specificity: **generic** ,  evidence: "Live music from the resident pianist for EPCOT. Currently found in the Rose & Crowd Pub in the United Kingdom Pavilion, the pianist has also played at the American Adventure Pavilion."
  - Source: https://touringplans.com/epcot/attractions/rose-crown-pub-musician

**Canada** ,  125 min total

- *Entertainment at Canada Mill Stage* ,  5 performances x 25 min = **125 min**
  - Showtimes: 2:15pm, 3:30pm, 5:00pm, 6:15pm, 7:30pm
  - Specificity: **specific** ,  evidence: "The Canada Mill Stage on the UK side of the pavilion is home to various modern Canadian music acts."
  - Source: https://touringplans.com/epcot/attractions/entertainment-at-canada-mill-stage

#### Non-pavilion acts on this date (excluded from pavilion totals)

- *Eat to the Beat Concert Series* (festival_concert, America Gardens Theatre) ,  3 x 35 min = **105 min**; showtimes 5:30pm, 6:45pm, 8:00pm
  - Specificity: **generic** ,  evidence: "World Showcase at EPCOT, specifically the America Gardens Theatre on the lagoon opposite the American Adventure Pavilion" ,  https://touringplans.com/epcot/attractions/eat-to-the-beat-concerts
- *JAMMitors* (roving, Park-wide (roving)) ,  7 x 10 min = **70 min**; showtimes 8:30am, 9:30am, 10:30am, 11:30am, 1:00pm, 2:00pm, 3:00pm
  - Specificity: **generic** ,  evidence: "STOMP-like musical trash can group that plays and entertains." ,  https://touringplans.com/epcot/attractions/jammitors
- *Luminous The Symphony of Us* (nighttime_spectacular, World Showcase Lagoon) ,  1 x 18 min = **18 min**; showtimes 9:00pm
  - Specificity: **generic** ,  evidence: "Nightly spectacular that involves dazzling lights, fireworks, water effects, lasers, and music in and around World Showcase Lagoon." ,  https://touringplans.com/epcot/attractions/luminous-symphony-us
- *Max & Aydar - Amazing Masters of Variety* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:15am, 10:15am, 11:10am, 12:15pm, 1:10pm, 2:10pm
  - Specificity: **generic** ,  evidence: "Entertaining duo that juggles, balances, and generally entertains." ,  https://touringplans.com/epcot/attractions/max-aydar
- *¡Celebración Encanto!* (non_pavilion_area, World Celebration) ,  6 x 15 min = **90 min**; showtimes 9:45am, 10:45am, 11:45am, 1:30pm, 2:30pm, 3:30pm
  - Specificity: **generic** ,  evidence: "Encanto dance- and sing-a-long show on CommuniCore Plaza stage." ,  https://touringplans.com/epcot/attractions/celebracion-encanto


## Non-pavilion entertainment, summarized (kept out of pavilion totals)

| Act | Venue / kind | Set min | Typical performances/day | Daily min | Appears on |
|---|---|---|---|---|---|
| Eat to the Beat Concert Series | America Gardens Theatre (festival_concert) | 35 | 3 | 105 | 4/7 dates |
| Garden Rocks Concert Series | America Gardens Theatre (festival_concert) | 30 | 3 | 90 | 1/7 dates |
| Disney on Broadway Concert Series | America Gardens Theatre (festival_concert) | unknown | 3 | unknown | 1/7 dates |
| Luminous The Symphony of Us | World Showcase Lagoon (nighttime_spectacular) | 18 | 1 | 18 | 7/7 dates |
| JAMMitors | Park-wide (roving) (roving) | 10 | 6, 7 | 60, 70 | 7/7 dates |
| ¡Celebración Encanto! | World Celebration (non_pavilion_area) | 15 | 6 | 90 | 7/7 dates |
| Max & Aydar - Amazing Masters of Variety | World Celebration (non_pavilion_area) | 15 | 6 | 90 | 3/7 dates |

## Acts never scheduled on any sampled date

Norway, China and France had **zero** scheduled entertainment on all seven sampled dates. Acts that older sources list for these pavilions (Jeweled Dragon Acrobats in China, Serveur Amusant in France, and any Norway act) do not appear on any TouringPlans schedule sampled here and are not counted.


## Unconfirmed set lengths

- **Disney on Broadway Concert Series** (Festival of the Arts, America Gardens Theatre): no Duration found. 3 performances on 2026-01-26. This is a festival concert series, so it does not touch any pavilion total.
- Every act that contributes to a pavilion total has a TouringPlans-published Duration. Zero pavilion minutes rest on a guess.
