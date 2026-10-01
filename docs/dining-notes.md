# EPCOT World Showcase dining: venues, menus, cuisine coding

Collected 2026-09-30. Companion file: `dining.csv` (one row per menu item).

## Sources and why

Disney's own dining pages at disneyworld.disney.go.com render their menus in
JavaScript, so a fetch returns an empty document. Direct HTTP to
disneyworld.disney.go.com, allears.net and touringplans.com was refused by this
session's egress policy (403 on CONNECT), so I could not work around it.

Everything in the CSV therefore comes from two aggregators that publish
server-rendered menus and date-stamp them:

- **touringplans.com** (primary). Most pages carried "last updated" dates of
  24 to 30 September 2026.
- **ropedropplanner.com** (primary/cross-check). Nearly every page carried
  "Last Updated: September 30, 2026".

Where both were available they agreed on items and prices. Two sources were
checked and rejected as stale:

- **wdwinfo.com** is years out of date. Its San Angel Inn page still lists
  Chuleta de Puerco and Capirotada and prices guacamole at $13; the current
  menu has neither dish and prices guacamole at $16.
- **allears.net**'s La Hacienda menu is roughly 2019 vintage (snapper $27.95,
  guacamole $8.50 against a current $16.00).

Disney's published price tiers ($ to $$$$) come from Disney's own EPCOT dining
index page, which did return its venue list. Signature Dining status was
confirmed separately: at World Showcase it is **Le Cellier Steakhouse,
Monsieur Paul and Takumi-Tei**, and nothing else.

## Status findings worth flagging

- **Germany is under construction** (began 13 July 2026, still active in
  September). It has closed *shops*, not restaurants: Volkskunst is mostly
  closed, Stein Haus is behind scrims, and the pavilion restrooms are sealed.
  Biergarten, Sommerfest and Karamell-Kuche are all fully open. Weinkeller is
  open but its exterior entrance is closed, so the only way in is through
  Stein Haus. A temporary beverage pickup window has opened next to Sommerfest.
- **Restaurant Marrakesh (Morocco) is closed** and has not operated as a dining
  location since 2020. No reopening date. I list it as a venue with status
  `closed` and exclude it from Morocco's venue count.
- **Tangierine Cafe (Morocco) no longer runs a standing menu.** It now operates
  as a festival booth under the name "Flavors of the Medina", serving a rotating
  menu tied to whichever festival is running. Everything I could capture for it
  is festival-period, and the CSV marks those rows.
- **Refreshment Port (Canada) closed 12 January 2026** and was replaced by
  **La Poutinerie**, which opened 1 July 2026. Dole Whip and chicken fingers
  went; poutine and Canadian beverages came in. Refreshment Port is not listed.
- Akershus is running as Princess Storybook prix fixe dining ($69 / $46).

## Venue list

Counts below exclude closed venues. Service type follows the four categories
asked for; `kiosk/cart` covers walk-up windows and outdoor stands with no
seating of their own.

| Pavilion | Venue | Service | Signature | Tier | Status |
|---|---|---|---|---|---|
| Mexico | San Angel Inn Restaurante | table service | no | $$ | open |
| Mexico | La Hacienda de San Angel | table service | no | $$ | open |
| Mexico | La Cantina de San Angel | quick service | no | $ | open |
| Mexico | La Cava del Tequila | lounge/bar | no | $ | open |
| Mexico | Choza de Margarita | lounge/bar | no | $ | open (outdoor walk-up stand) |
| Norway | Akershus Royal Banquet Hall | table service | no | $$$$ | open |
| Norway | Kringla Bakeri og Kafe | quick service | no | $ | open |
| China | Nine Dragons Restaurant | table service | no | $$ | open |
| China | Lotus Blossom Cafe | quick service | no | $ | open |
| China | Joy of Tea | kiosk/cart | no | $ | open |
| Germany | Biergarten Restaurant | table service | no | $$$ | open (buffet) |
| Germany | Sommerfest | quick service | no | $ | open |
| Germany | Karamell-Kuche | kiosk/cart | no | $ | open |
| Germany | Weinkeller | lounge/bar | no | not published | open, access via Stein Haus only |
| Italy | Tutto Italia Ristorante | table service | no | $$ | open |
| Italy | Via Napoli Ristorante e Pizzeria | table service | no | $$ | open |
| Italy | Tutto Gusto Wine Cellar | lounge/bar | no | $ | open |
| Italy | Gelateria Toscana | kiosk/cart | no | $ | open |
| Italy | Pizza al Taglio | kiosk/cart | no | varies | open, limited hours |
| The American Adventure | Regal Eagle Smokehouse | quick service | no | $ | open |
| The American Adventure | Fife & Drum Tavern | kiosk/cart | no | $ | open |
| The American Adventure | Block & Hans | kiosk/cart | no | $ | open |
| The American Adventure | Funnel Cake | kiosk/cart | no | $ | open |
| Japan | Takumi-Tei | table service | **yes** | $$$$ | open (prix fixe) |
| Japan | Teppan Edo | table service | no | $$ | open |
| Japan | Shiki-Sai: Sushi Izakaya | table service | no | $$ | open |
| Japan | Katsura Grill | quick service | no | $ | open |
| Japan | Kabuki Cafe | kiosk/cart | no | $ | open |
| Morocco | Spice Road Table | table service | no | $$ | open |
| Morocco | Tangierine Cafe: Flavors of the Medina | quick service | no | $ | open, festival menus only |
| Morocco | Oasis Sweets & Sips | kiosk/cart | no | $ | open |
| Morocco | Restaurant Marrakesh | table service | no | n/a | **closed** |
| France | Monsieur Paul | table service | **yes** | $$$$ | open (prix fixe) |
| France | Chefs de France | table service | no | $$ | open |
| France | La Creperie de Paris | table service | no | $$ | open |
| France | Les Halles Boulangerie-Patisserie | quick service | no | $ | open |
| France | Crepes A Emporter | kiosk/cart | no | $ | open |
| France | L'Artisan des Glaces | kiosk/cart | no | $ | open |
| France | Les Vins des Chefs de France | kiosk/cart | no | $ | open |
| United Kingdom | Rose & Crown Dining Room | table service | no | $$ | open |
| United Kingdom | Rose & Crown Pub | lounge/bar | no | $ | open |
| United Kingdom | Yorkshire County Fish Shop | quick service | no | $ | open |
| Canada | Le Cellier Steakhouse | table service | **yes** | $$$ | open |
| Canada | La Poutinerie | quick service | no | $ | open (new 1 July 2026) |
| Canada | Canada Popcorn Cart | kiosk/cart | no | $ | open |

Festival marketplace booths are excluded entirely, as asked. Kiosks that sit
inside a pavilion year round (Joy of Tea, Kabuki Cafe, Fife & Drum, Block &
Hans, Funnel Cake, the Canada popcorn cart, Gelateria Toscana, the two France
carts) are permanent and are included.

## Sections used

The brief named appetizer / entree / dessert / beverage. I added **side**,
because several venues publish a separate sides or contorni section and folding
those into entrees would misstate how much of a menu is main dishes. Five
values appear in the `section` column: appetizer, entree, side, dessert,
beverage.

## Cuisine coding rules, as actually applied

Provenance of the dish only. No quality judgement anywhere.

- **NATIVE**: the dish genuinely belongs to that country's cuisine, or the drink
  is actually produced there. Schnitzel and spaetzle in Germany, tagine and
  bastilla in Morocco, poutine in Canada, kakigori and okonomiyaki in Japan. All
  German wines at Biergarten, all Italian wines at Tutto Italia, all Japanese
  sake at Takumi-Tei, all French wines at Chefs de France code NATIVE.
- **ADAPTED**: recognisably influenced by the cuisine but altered or invented
  for the park, or a native ingredient in a foreign format. Pretzel bread
  pudding, churro sundae, maple creme brulee, frozen mint tea, plant-based
  kjottkaker, California roll.
- **GENERIC**: standard American park food or a product with no link to the
  country. Cheeseburger, chicken tenders, mac and cheese, fountain drinks,
  bottled water, and any wine or beer from a third country (Californian wine in
  Norway, Spanish wine in Morocco).
- **UNCLEAR**: used where the call is genuinely undecidable, not where it is
  merely awkward. 41 of 1,509 items.

### De-duplication rules I applied

These materially affect counts, so they are stated rather than buried.

1. **Allergy-friendly duplicates dropped.** Regal Eagle, Le Cellier, Spice Road
   Table and Rose & Crown republish their whole menu once per allergen. The
   BBQ Burger appeared seven times on Regal Eagle's page. I kept one row per
   dish. Without this, Regal Eagle alone would have contributed about 200 rows.
2. **Wine by the glass and by the bottle collapsed to one row**, with both
   prices in the `price` field. One wine is one menu item.
3. **Pizza sizes collapsed.** Via Napoli sells six speciality pizzas in three
   sizes each. Counting 18 rows would have overstated Italy's choice, so each
   pizza is one row with all three prices.
4. **Kakigori sizes collapsed** at Kabuki Cafe: regular and large were listed at
   identical prices.
5. **Lunch and dinner price variants kept as separate rows** where the source
   published both (Nine Dragons pot stickers at $9 and $12, Teppan Edo's lunch
   entrees, Le Cellier's lunch-only dishes). The `note` column marks which menu
   each came from. This is the one place where the item count runs slightly
   ahead of the distinct-dish count.
6. **Souvenir stein versions of Sommerfest beers kept**, since Disney prices
   them as separate line items, but the note marks them as packaging variants.
7. **Festival items at permanent venues kept and flagged** in the note as
   limited-time. Sommerfest's Zwiebelkuchen, Regal Eagle's Blackberry Buckle,
   Funnel Cake's three festival flavours, and all of Tangierine Cafe. Filter on
   the note if you want only the standing menu.

### Borderline calls I had to make

These are the ones where a different analyst could reasonably differ.

- **The American Adventure breaks the GENERIC rule.** The brief defines GENERIC
  as "standard American theme park food with no connection to the country", but
  for this pavilion the country *is* America, so the two categories collide.
  The brief also says domestic beer codes GENERIC, which would have coded every
  beer in the USA pavilion GENERIC. I overrode both: named regional American
  barbecue (Kansas City chicken, North Carolina pork, Texas brisket), cornbread,
  coleslaw, banana pudding, s'mores, funnel cake, hot dogs, root beer floats and
  American breweries all code NATIVE. Undifferentiated park food (fountain
  drinks, chicken strips, PB&J, Mickey pretzels, popcorn, turkey legs) codes
  GENERIC. This pavilion's 46% NATIVE share is therefore not measured on the
  same basis as the other ten and should not be ranked against them without a
  caveat.
- **Caesar salad** is coded three different ways on purpose. It was invented in
  Tijuana by an Italian immigrant. At San Angel Inn (Mexico) I coded it UNCLEAR,
  because the origin claim is real but the dish is not part of Mexican culinary
  tradition. At Tutto Italia and Via Napoli (Italy) I coded it GENERIC, because
  it is not Italian by any reading.
- **Chicken tikka masala at Rose & Crown is NATIVE.** It was created in Britain,
  most likely Glasgow. Coding it GENERIC or ADAPTED would misread British
  cuisine as excluding its own inventions.
- **Irish products in the UK pavilion are UNCLEAR, not NATIVE.** Guinness, Harp,
  Sullivan's and the Irish Whiskey Flight are Irish, not British, but they are a
  normal part of a British pub's range. This is the single largest source of
  UNCLEAR calls (10 of the UK's 101 items). If you treat "British Isles" as the
  unit rather than "United Kingdom", the UK's NATIVE share rises materially.
- **Nordic-but-not-Norwegian drinks at Akershus are UNCLEAR**: Einstok is
  Icelandic, Rekorderlig is Swedish. Kringla's "Nordic Draft Beer" is UNCLEAR
  because no brewery or country is published.
- **Disney house-brand beers with themed names are UNCLEAR**: Dragon Blossom,
  Lucky Foo Pale Ale and Honey Jasmine Lager in China, Moroccan Blonde Ale and
  "Mediterranean Beer" in Morocco. The names imply provenance; the brewery is
  not published, and these are generally US-brewed.
- **Teppanyaki is split.** At Teppan Edo, items named in Japanese for Japanese
  ingredients (Tori, Yasai, Ebi, Hotate, wagyu) code NATIVE. Western steak cuts
  cooked on the same griddle (NY Cut Steak, Julienne Steak, Filet Mignon,
  Lobster Tail) code ADAPTED, as do the district-named combination plates.
- **Sushi rolls are split** at Shiki-Sai and Kabuki Cafe. Nigiri and sashimi
  code NATIVE. American sushi-bar inventions code ADAPTED: California, Spicy
  Tuna, Philadelphia, Rainbow, Dragon, Volcano, Shrimp Tempura, Avocado.
- **Osso buco appears on both Mexican menus** (Osso Buco con Mole Negro, Osso
  Buco a la Mexicana). Italian cut, Mexican sauce, so ADAPTED both times.
- **Monsieur Paul's scallop course is ADAPTED**, the only non-NATIVE item on
  that menu, because it is finished with maple syrup. Its "Main Course: Where
  East Meets West" at Takumi-Tei is ADAPTED on the same logic, using Disney's
  own wording.
- **Nachos at La Cantina are ADAPTED.** Nachos were genuinely invented in
  Piedras Negras, Mexico, but the park version is built on Tex-Mex nacho cheese
  sauce rather than the original melted cheese.
- **Werther's Original items at Karamell-Kuche.** Werther's is a German
  confectionery brand, which is the pavilion's whole premise, but a caramel
  pecan cluster or a snickerdoodle is not German food. I coded the plain caramel
  squares ADAPTED (German brand, German confection) and the American bakery
  formats GENERIC. This is the shakiest block in the file and it drags Germany's
  GENERIC share up by itself.
- **Fabrizia limoncello at Tutto Gusto is ADAPTED**, not NATIVE. Fabrizia is a
  US producer making an Italian-style product.
- **Le Cellier is a steakhouse first.** Most of its menu is American steakhouse
  cuts with no Canadian content, which is why Canada shows only 25% NATIVE
  despite the pavilion's two genuinely Canadian venues. Bison, Chinook salmon,
  cheddar soup, poutine, butter tart, Canadian breweries, icewine and the Bloody
  Caesar code NATIVE; the cuts, the Napa wines and the sides do not.
- **Prix fixe courses count as items.** Akershus, Biergarten, Takumi-Tei,
  Monsieur Paul and the Chefs de France Menu Francais publish named courses
  rather than priced dishes. Each named course or buffet station is one row with
  price "Included". This is a judgement that affects the food ranking: Biergarten
  shows 26 items because a buffet is published as eight stations, which is not
  comparable to an a la carte menu of 26 dishes. Treat buffet and prix fixe
  venues separately in any choice measure.

## Gaps

Four venues have a row in the CSV with a blank `item` and the reason in `note`:

1. **Weinkeller (Germany)**: no itemised wine list published anywhere
   accessible. The touringplans page for it was last updated May 2023 and
   carries only prose. The venue is open.
2. **Pizza al Taglio (Italy)**: no itemised menu published. Disney lists the
   window with price "Varies". Its permanence is not confirmed.
3. **Canada Popcorn Cart**: no itemised menu published.
4. **Restaurant Marrakesh (Morocco)**: closed, so no menu exists.

Partial menus, flagged in the CSV:

- **La Cava del Tequila** has only 8 speciality cocktails itemised. Its
  advertised 100-plus tequilas, its tequila flights and its Mexican beers are
  not published as priced line items. Its true item count is far higher than 8,
  so do not use it as-is in a choice measure.
- **Tangierine Cafe** has festival items only, because that is all it now
  serves.
- **Shiki-Sai: Sushi Izakaya**: the source page ended with "menu incomplete in
  source document". Food is captured in full; its sake, beer and cocktail list
  is missing. Real item count is higher than 78.
- **Kringla Bakeri og Kafe**: the venue description mentions sandwiches, but the
  published menu has only a "Norwegian Treats" section and drinks. If sandwiches
  are still sold they are not in the CSV.
- **Nine Dragons**: I captured the dinner menu in full plus the lunch-priced
  duplicates the page carried. I did not separately pull the standalone lunch
  menu, so a lunch-only dish, if one exists, could be missing.
