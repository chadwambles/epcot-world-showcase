# Tableau walkthrough: EPCOT World Showcase

Four sheets and a dashboard, built from four isolated CSVs. Every number is
precomputed, so there are no calculated fields anywhere in this workbook.

Part 8 is a list of traps indexed by the symptom you will actually see. If
something goes wrong, look there first rather than re-reading the step.

---

## Part 0. Build the sources

```
py build_tableau.py --isolate --clean
```

That writes `tableau/` with one subfolder per file:

```
tableau/
  rank_long/rank_long.csv     32 rows   the slope chart
  scatter/scatter.csv         10 rows   the quadrant chart
  menu_mix/menu_mix.csv       33 rows   the menu composition bar
  minutes/minutes.csv         22 rows   the things-to-do bar
  notes.md                              the figures the text blocks quote
```

**The subfolders are not tidiness, they are load-bearing.** Tableau's text
file connector is folder scoped. Point it at a folder holding four
differently-shaped CSVs and it tries to union them, then fails with
`F3ADC07B`. One file per folder means it can only ever see one shape.

Open `tableau/notes.md` now and keep it to hand. Every figure quoted in the
dashboard's text comes from there, so if the workbook and the notes disagree,
the workbook is stale.

---

## Part 1. Connect

Four separate connections. Do them one at a time.

**1.1** Open Tableau Desktop. Connect, To a File, Text file.

**1.2** Navigate **into** `tableau/rank_long/` and pick `rank_long.csv`.
Not the `tableau/` folder. Into the subfolder, then the file.

**1.3** On the Data Source tab, check the field types:

| field | type |
|---|---|
| `pavilion` | Abc, string |
| `ranking` | Abc, string |
| `ranking_order` | # number, will be used as a sort key |
| `rank` | # number |
| `rank_label` | Abc, string |
| `emphasis` | Abc, string |
| `is_highlighted` | Abc, string |

If `rank_label` came in as a number, click its type icon and change it to
String. It holds values like `3.5` and you want the text, not the arithmetic.

**1.4** Repeat for the other three. Data menu, New Data Source, Text file,
then into `scatter/`, `menu_mix/`, `minutes/` in turn.

You should end with four data sources listed in the Data pane. Each sheet uses
exactly one of them.

---

## Part 2. Sheet 1, the slope chart

The hero. Eleven pavilions tracked across the three rankings, so the crossing
lines show the disagreement without a word of explanation.

**2.1** New worksheet. Rename it `Three rankings`. Select the **rank_long**
data source.

**2.2** Drag `ranking` to **Columns**.

**2.3** Drag `rank` to **Rows**. It will arrive as `SUM(rank)`. Click the
pill, Measure, **Average**. It should read `AVG(rank)`.

**2.4** Marks card, change the mark type dropdown from Automatic to **Line**.

**2.5** Drag `pavilion` to **Detail** on the Marks card. You now have eleven
lines instead of one.

**2.6** Sort the columns. Right-click the `ranking` pill, **Sort**. Sort By:
Field. Order: Ascending. Field Name: `ranking_order`. Aggregation: Minimum.
OK.

The order should now read Things to do, Food and drink, Authenticity.

**2.7** Reverse the rank axis, because rank 1 belongs at the top. Right-click
the vertical axis, **Edit Axis**, tick **Reversed**. Close.

**2.8** Drag `emphasis` to **Color**.

**2.9** Click Color, **Edit Colors**. Select each item on the left and click
the colour square, then paste the hex into the dialog:

| member | hex |
|---|---|
| Good at all three | `2A78D6` |
| Last on all three | `E34948` |
| Ninth in things to do, first in authenticity | `7A4FBF` |
| The other eight | `898781` |

These three identity colours were checked with a colourblindness validator
rather than chosen by eye. The worst adjacent pair separates at 21.4 under
protanopia, which is comfortably clear. Do not substitute a green: green
against this red collapses to 7.3 and becomes a coin flip for about one man
in twelve.

**2.10** Drag `is_highlighted` to **Size**. Click Size, and drag the slider so
the range is noticeable but not silly. The three highlighted pavilions should
read as foreground, the other eight as background.

**2.11** Label the line ends. Click **Label** on the Marks card.
- Tick **Show mark labels**
- Marks to Label: **Line Ends**
- Untick **Label start of line**, leave **Label end of line** ticked
- Click the Text `...` box and set the font to 10pt

**2.12** Drag `pavilion` to **Label** as well, so the label says the pavilion
name rather than the rank number.

**2.13** The American Adventure has no authenticity rank, so its line stops at
Food and drink and its label lands mid-chart. That is correct and worth
leaving. If it overlaps another line, click Label and tick **Allow labels to
overlap other marks**, which lets Tableau draw it rather than suppressing it.

**2.14** Tidy the axes.
- Right-click the vertical axis, Edit Axis, Title: `Rank, 1 is best`
- Right-click the horizontal axis header, **Hide Field Labels for Columns**
- Right-click in the view, **Format**, Lines, and set Grid Lines to a light
  grey. Zero Lines: None.

**2.15** Tooltip. Click Tooltip and replace the contents with:

```
<pavilion>
<ranking>: rank <rank_label>
<emphasis>
```

**2.16** Title: `The same eleven pavilions, asked three different questions`

---

## Part 3. Sheet 2, the quadrant scatter

**3.1** New worksheet, name it `No tradeoff`. Select the **scatter** data
source.

**3.2** Drag `things_to_do_rank` to **Columns**, `authenticity_rank` to
**Rows**. Set both pills to **Average** via the pill menu, Measure, Average.

**3.3** Drag `pavilion` to **Detail**. Eleven points become ten, because The
American Adventure is excluded from the authenticity ranking and so has no
coordinates. That exclusion is in the data, not something you need to filter.

**3.4** Marks type: **Circle**. Click Size and enlarge to roughly the
three-quarter mark.

**3.5** Drag `emphasis` to **Color** and apply the same four hexes from step
2.9. Using one colour system across both sheets is what lets a reader connect
them.

**3.6** Reverse both axes. Right-click each, Edit Axis, tick **Reversed**.
Rank 1 then sits top left, which is the "best" corner and the one people look
at first.

**3.7** Fix both axis ranges so the quadrant lines land in the middle.
Right-click each axis, Edit Axis, Range: **Fixed**, start `0.5`, end `11.5`.

**3.8** Add the quadrant lines. Right-click the horizontal axis, **Add
Reference Line**. Line, Scope: Entire Table, Value: **Constant** `6`,
Label: None, Formatting: a light grey, 1pt. Repeat on the vertical axis.

**3.9** Label every point. Click Label, tick Show mark labels, drag `pavilion`
to Label, set 10pt, and set Alignment to top centre so the names sit above
the dots rather than on them.

**3.10** Axis titles: `Things to do rank, 1 is most` and
`Authenticity rank, 1 is most`.

**3.11** Tooltip:

```
<pavilion>
Things to do: rank <AVG(things_to_do_rank)>
Authenticity: rank <AVG(authenticity_rank)>
Food: rank <AVG(food_rank)>

<AVG(guest_min)> minutes a visitor can consume
<AVG(menu_native_pct)>% of the menu is native to the cuisine
<AVG(arch_refs)> real buildings reproduced, <arch_coherence>
```

**3.12** Title: `No tradeoff, just uneven investment`

---

## Part 4. Sheet 3, the menu composition

**4.1** New worksheet, `Menu mix`. Select the **menu_mix** data source.

**4.2** Drag `pavilion` to **Rows**, `share` to **Columns**. Set the share
pill to **Sum**.

**4.3** Drag `cuisine_code` to **Color**. You get a stacked bar.

**4.4** Sort the rows by native share. Right-click the `pavilion` pill, Sort,
Sort By: Field, Order: Ascending, Field Name: `pavilion_sort`, Aggregation:
Minimum.

**4.5** Sort the stack segments. Right-click `cuisine_code` on the Colour
card, Sort, Sort By: Field, Ascending, Field Name: `code_order`,
Aggregation: Minimum. Native should sit at the left of each bar.

**4.6** Edit Colors with the sequential ramp:

| member | hex |
|---|---|
| Native to the cuisine | `1A4F8F` |
| Adapted for the park | `6F9FD8` |
| Generic theme park food | `C9CCD1` |

This one is a single hue going light to dark on purpose. Native, adapted and
generic are degrees of the same thing, not three unrelated categories, and a
three-colour rainbow here would imply they are unrelated.

**4.7** Drag `share_label` to **Label**. It is prebuilt text that is blank for
any segment under 9%, so small slivers do not collect unreadable labels.

**4.8** Label colour has to differ by segment and Tableau will not do that for
you. Set the label font to white, then accept that the two pale segments need
dark text: click Label, Font, and set the colour to **Match Mark Color**,
then click Label again and set it to Automatic. If the pale segments are
unreadable, set the label font to a dark grey for all segments; white on
`6F9FD8` only reaches 2.75:1 and fails, while dark ink on it is fine.

**4.9** Format the axis as a percentage. Right-click the horizontal axis,
Format, Axis tab, Numbers: **Percentage**, 0 decimal places.

**4.10** Set the axis range Fixed, 0 to 1, so every bar is full width and the
comparison is between compositions rather than lengths.

**4.11** Tooltip:

```
<pavilion>
<cuisine_code>: <SUM(items)> items, <share_label> of the menu
```

**4.12** Title: `How much of each pavilion's menu is actually that country's
food`

**4.13** Add a caption. Worksheet menu, Show Caption, then double-click it and
type:

```
The American Adventure is coded on a different basis and is not comparable:
generic American theme park food is that country's food.
```

---

## Part 5. Sheet 4, the minutes

**5.1** New worksheet, `Guest minutes`. Select the **minutes** data source.

**5.2** `pavilion` to **Rows**, `minutes` to **Columns** as **Sum**.

**5.3** `component` to **Color**.

**5.4** Sort rows: right-click `pavilion`, Sort, By Field, Ascending,
`pavilion_sort`, Minimum.

**5.5** Sort the stack: right-click `component` on Colour, Sort, By Field,
Ascending, `component_order`, Minimum.

**5.6** Edit Colors:

| member | hex |
|---|---|
| Rides and films | `3D5A73` |
| Live entertainment, one set | `9BB0C1` |

A second single-hue ramp, in a different hue from the menu chart so the two
sheets are not read as related.

**5.7** `minutes_label` to **Label**. Blank under 4 minutes, so the slivers
stay clean.

**5.8** Axis title: `Minutes one visitor can consume`. Leave the range
automatic here; the lengths are the point.

**5.9** Tooltip:

```
<pavilion>
<component>: <SUM(minutes)> minutes
Total one visitor can consume: <AVG(guest_min_total)> minutes
```

**5.10** Title: `What the things-to-do ranking is actually made of`

**5.11** Caption:

```
A film's runtime is what one guest sees. A pavilion's daily entertainment
output is not, so each act counts once here, discounted by how often it runs.
```

---

## Part 6. The dashboard

**6.1** New Dashboard.

**6.2** Size, bottom left of the Dashboard pane. Change from Automatic to
**Fixed size**, then Custom, and type **1000 x 1900**.

Do not leave it on Automatic. Automatic lets every object fight for space and
the result is different on Tableau Public than on your screen. Fixed means
what you see is what gets published.

**6.3** Drag a **Text** object to the top. Type:

```
EPCOT World Showcase: three rankings that disagree

Eleven country pavilions, ranked on how much there is to do, on food and
drink, and on how authentic each one is. There is no overall score, because
combining the three would need weights and any weighting is a choice presented
as arithmetic.
```

Select the first line and set it to 18pt bold. Leave the rest at 11pt.

**6.4** Drag `Three rankings` below it.

**6.5** Drag `No tradeoff` below that.

**6.6** Drag a **Text** object below the scatter:

```
Spearman between the rankings runs +0.25 to +0.45. On ten or eleven points you
need about 0.65 for significance at p = 0.05, so none of these is
distinguishable from zero. The honest reading is that the three questions have
unrelated answers, not that there is a weak positive relationship.
```

**6.7** Drag `Menu mix`, then `Guest minutes`.

**6.8** Drag a final **Text** object:

```
Data and method: github.com/chadwambles/epcot-world-showcase
Dataset: kaggle.com/datasets/chadwambles/epcot-world-showcase

Collected 24 to 30 September 2026. Shop counts are deliberately absent: two
sources were tried and both are wrong in opposite directions.
```

**6.9** Now set every height explicitly. Click each object, then in the
Layout pane type its height. They must sum to 1900:

| object | height |
|---|---|
| title text | 150 |
| Three rankings | 520 |
| No tradeoff | 560 |
| correlation text | 130 |
| Menu mix | 300 |
| Guest minutes | 300 |
| footer text | 140 |

Typing the heights is the step people skip. Dragging dividers gets you close
and then one object quietly takes the remainder, which is what makes a
dashboard look fine in Desktop and broken on Public.

**6.10** Hide the legends you no longer need. The emphasis legend appears
twice, once per sheet. Delete one of them. Click the legend's dropdown and
Remove from Dashboard.

**6.11** Float the remaining emphasis legend into the empty space at the top
right of the slope chart rather than letting it sit in its own column, which
squeezes the chart. Hold Shift while dragging to float it.

---

## Part 7. Publish

**7.1** Server menu, Tableau Public, **Save to Tableau Public**. Sign in.

**7.2** You will get **Data Extract Required**. Tableau Public cannot host a
live connection to files on your machine, so it needs an extract. Click
**Create Extract** and let it run. All four sources are tiny, so it is quick.

If you do not see "Save to Tableau Public" under the Server menu, you are
signed into Tableau Server or Online. Sign out first, then the Tableau Public
option appears.

**7.3** Name it `EPCOT World Showcase: Three Rankings That Disagree`.

**7.4** When the browser opens, scroll down and **untick** "Show sheets",
so visitors land on the dashboard rather than on a tab strip of four
worksheets.

**7.5** Set the thumbnail to the dashboard, not whichever sheet was last
active.

---

## Part 8. Traps, indexed by the symptom

**"There was a problem connecting to the data source" / `F3ADC07B`**
You connected to the `tableau/` folder, or to a file in a folder holding other
CSVs. The text connector is folder scoped and tried to union four different
shapes. Reconnect to the file inside its own subfolder. If you ran
`build_tableau.py` without `--isolate`, rerun it with the flag.

**All eleven lines are one colour**
`emphasis` is not on Colour, or `pavilion` landed on Colour instead of Detail.
Pavilion belongs on Detail; eleven categorical colours is not a palette.

**The three rankings are in the wrong order along the bottom**
Step 2.6. Alphabetical order puts Authenticity first. Sort the `ranking` pill
by `ranking_order`, Minimum.

**Rank 11 is at the top**
You missed the Reversed tick in Edit Axis. Steps 2.7 and 3.6.

**A label is missing from a short bar**
Not annotation overlap, which is the obvious guess. Tableau suppresses a label
that does not fit inside its mark. Click Label and tick **Allow labels to
overlap other marks**.

**You cannot drag a card in the Marks pane**
Marks cards are not draggable. If a field is on the wrong card, drag the field
off and drop it on the right one.

**The stacked segments are in the wrong order**
Sorting the colour legend by hand does nothing. Right-click the dimension on
the Colour card, Sort, By Field, using the `_order` column.

**A dual axis chart draws the wrong series on top**
Layer order follows pill order on Columns or Rows, and the LEFT pill draws on
top. Swap the pills, do not look for a bring-to-front option. There is no
dual axis in this workbook, but you will hit it next time.

**A dual axis has two different scales**
Right-click the second axis and tick **Synchronize Axis**. Without it the two
series are drawn on different scales and the chart is a lie.

**The dashboard looks fine in Desktop and wrong on Tableau Public**
Size is still Automatic, or the heights were dragged rather than typed. Steps
6.2 and 6.9.

**"Data Extract Required" on publish**
Expected. Tableau Public cannot reach files on your machine. Create the
extract.

**A number in the dashboard does not match the data**
Check it against `tableau/notes.md`. That file is generated from the same CSVs
the sheets read, so if they disagree, the text block was typed from an older
run and needs updating.
