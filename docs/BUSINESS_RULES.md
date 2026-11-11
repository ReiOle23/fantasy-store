# Crown & Trade — Business Rules

**Project:** Marketplace
**Last reviewed:** 2026-11-10

Crown & Trade is a fantasy trading and adventure game. Each player has up to three heroes and plays one at a time. A hero travels between fifteen cities, takes contracts, gathers and crafts materials, trades in markets and at the auction house, clears dungeons, fights armies and other heroes, and grows stronger with gear and powers.

## This project's role in the product

This project is **the auction house and the limited-stock marketplace** (section 15). It runs the auctions between heroes: listings, bids and endings. It guarantees that only one bid wins when many arrive at once, and that every finished auction is delivered to the winner and the seller exactly once. Gold and inventories belong to the game; the marketplace only handles the sale itself.

## Game rules

> This section is **identical** in the documents of all Crown & Trade projects.
> When a rule changes, update it everywhere.

### 1. Glossary

| Term | Meaning |
|---|---|
| **Player** | A person with an account. Signs in with an email and password or a Google account. |
| **Game** | One hero's save: its gold, power coins, tutorial progress and its own progress in every city. A player has one game per hero. |
| **Hero** | A character a player controls (up to three per player). Has a class, a level, stats, an inventory and powers. |
| **Gold** | The main currency. Earned by playing and spent on items and services. |
| **Power coins** | A rare in-game currency, earned at milestones and spent to unlock powers. |
| **Conditions** | The hero's stamina, from 0 to 100. Contracts and travel spend it; food restores it. |
| **Contract** | A job from a city's notice board that ends in a fight against an enemy. |
| **Gathering** | Mining, fishing, herboristery (herb gathering) or hunting. Gives materials, no fight. |
| **Dungeon** | A chain of fights in a city, 10 stages deep, with more beyond. |
| **Army** | One of six enemy armies. It can only be fought while it attacks a city. |
| **Mortorius** | A legendary creature that shows up 1 time in 100 after a contract fight or a dungeon stage. |
| **Framan** | A three-headed legendary creature that shows up 1 time in 100 after a contract fight or a dungeon stage, when Mortorius does not. |
| **Gem** | A gemstone crafted at the Alchemist. Set into a weapon or armour piece, it adds one stat. |
| **Potion** | A brew crafted at the Alchemist. Drunk, it boosts one stat (a dark potion also lowers another) for the hero's next battle. |
| **World event** | A 5-day situation in one city: a festival, high taxes, a war, and so on. |
| **Bot** | A hero run by the game itself. Bots fill rankings and tournaments. |

### 2. Players, heroes and cities

- A player can have up to **3 heroes**. Each hero has its **own game**: a game has **one hero**.
- A player's heroes are independent: gold, power coins, tutorial, city progress, inventory, letters and purchases belong to one hero and are never shared or moved between them.
- After signing in, the player chooses which hero to play, or creates a new one while they have fewer than 3. They can switch hero at any time.
- A hero name is **unique** in the whole world. It is also how other players see the hero, for example in auctions.
- Hero classes: **knight**, **lancer** and **ranger**. Gender: male or female.
- A new hero starts in **Dredfort** with the class's base stats, an empty inventory, and a market ready in that city.
- For every city, the game keeps the player's own progress:
  - **City level and city experience.** The first city level needs 1000 experience, and each following level needs 1000 more than the previous one.
  - **Dungeon progress**: the next stage to fight.
  - **The city market stock** this player sees.
- The hero is always in exactly one city.

**Accounts and passwords**
- A password has at least **8 characters**. Players who already have a shorter password can still sign in with it.
- A player who forgot their password can ask for a reset by email. The email holds a link that is valid for **10 minutes** and works **once**.
- An account can receive **one** reset email per day (24 hours from the last one sent).
- Asking for a reset never tells whether an email has an account.
- Changing the password signs the player out everywhere else. The game, hero and progress are not touched.
- A player who signed up with Google can also reset their password. Afterwards they can sign in either with the password or with Google.

**Travelling**
- The hero needs at least the city's **required level**.
- The hero must have cleared the **dungeon the city requires** at least once (see 12).
- Travel costs **5 conditions**.
- Travel time is 18 seconds, shortened by a mount: `18 s / (1 + mount speed %)`.
- Arriving renews the market stock and clears the hero's unaccepted contracts in the city they left.

### 3. Hero progression

**Experience:** the next level needs `50 × level²` experience. When a hero has enough, the player confirms the level-up.

**On level-up:**
- The level goes up by 1, and **the hero keeps half of their experience**.
- Stats are recalculated from the class table below.
- Every level gives `10 × new level` gold.
- Some levels give more:

| Levels | Extra reward |
|---|---|
| 5, 13, 17, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93 | +5 inventory slots |
| 17, 21, 25 … 97 (every 4 levels from 17) | +1 power coin |
| 9 | 3 apple pies |
| 17 | 1 free power |

**Features unlocked by level:**
- Blacksmith: 9.
- Item upgrades: 10.
- Magic cauldron: 17.
- Mounts and stables: 20.
- Blacksmith and alchemy cities: 41.
- Mayor cities: 57.
- The capital: 69.

**Class stats**

| Class | Damage | Defence | Health | Agility | Critical % | + per level |
|---|---|---|---|---|---|---|
| Knight | 20 | 10 | 200 | 8 | 5 | dmg +4, def +2, hp +40, agi +1, crit +0.25 |
| Lancer | 15 | 20 | 200 | 5 | 10 | dmg +3, def +4, hp +50, agi +1, crit +0.25 |
| Ranger | 25 | 0 | 200 | 8 | 10 | dmg +5, def +2, hp +30, agi +1.05, crit +0.25 |

- Knights are balanced, lancers are tanky, and rangers hit hard with no armour of their own.
- **Total hero strength** = class stats + equipped items + collection set bonuses. In battle, items count in proportion to their durability.
- **Weapons by class:**
  - Normal loot: knights get large swords, lancers get lances, rangers get bows.
  - Crossbows, twin swords and lances with shield only come from collection sets.
  - Any hero may equip any weapon type.

**Conditions (stamina, 0–100)**

| Action | Effect |
|---|---|
| Accept a contract | −2 to −5 (longer contracts cost more). Not allowed at 0. |
| Travel | −5 |
| Eat food | + the food's value, up to 100 |
| Gathering | Free |

A tired hero sees longer mission times: shown time × `(2 − conditions/100)`.

**Hero record:** enemies killed, missions finished, PvP wins and losses, dungeons completed, great enemies defeated (legendary contracts won) and gold earned. The record drives challenges and rankings.

**Challenges**
- A challenge completes automatically. The player then **accepts** the reward, once.

| Challenge | Goal | Gold | XP |
|---|---|---|---|
| First Blood / Slayer's Path / Hundred Blades / Unstoppable Force | kill 1 / 50 / 100 / 500 enemies | 10 / 100 / 250 / 1000 | 50 / 300 / 700 / 3000 |
| Mission Accepted / Veteran Contractor / Mercenary Legend | finish 1 / 25 / 100 missions | 20 / 300 / 1500 | 50 / 800 / 5000 |
| First Victory / Arena Champion / Undefeated Warrior | win 1 / 10 / 50 PvP fights | 50 / 400 / 2000 | 150 / 1200 / 6000 |
| First Descent / Dungeon Crawler / Dungeon Master | clear 1 / 10 / 50 dungeon stages | 75 / 500 / 3000 | 200 / 1500 / 9000 |
| Giant Slayer / Legend Hunter / Monster Bane | defeat 1 / 5 / 20 great enemies | 150 / 800 / 4000 | 500 / 2500 / 12000 |
| Rival's Nemesis | 10 PvP wins and 5 PvP losses | 350 | 1000 |
| Battle-Hardened | 50 dungeon stages and 250 kills | 5000 | 15000 |
| Merchant's Fortune / Itinerant Merchant / Trader's Triumph / Monopoly Master | earn 1k / 10k / 50k / 100k gold | 0 | 100 / 500 / 1000 / 5000 |

**Rankings:** heroes can be ranked by level, gold earned, missions, PvP wins, or dungeon progress in a chosen city. Bots appear in the rankings.

### 4. Items

| Type | Kinds | Properties |
|---|---|---|
| **Weapon** | bow, crossbow, lance, lance with shield, large sword, twin swords | level, rarity, price, durability (0–100%), upgrades, stats, upgrade materials, collection set |
| **Armour** | helmet, shoulders, chest, pants, boots, amulet | same as weapons |
| **Material** | **food** (restores conditions) or **crafting** material; each has a trade (market, mining, fishing, herboristery, hunt) | quantity (same materials stack), price, conditions restored |
| **Potion** | natural, elaborated, dark | rarity, effects, price, quantity; lasts one battle once drunk (see "Potions" below) |
| **Gem** | Ruby, Sapphire, Emerald, Topaz | rarity, stat, value, price, quantity (see "Gems" below) |
| **Mount** | — | travel speed bonus; price in gold or real money |
| **Skin** | hero look (legendary hero or a class skin) or house (inventory background) | price in gold or real money |

**Rarity:**
- Item rarities: **normal**, **rare**, **legendary**.
- Contracts use their own names: casual and unusual give normal items, epic gives rare items, legendary gives legendary items.

**Equipping:**
- One weapon.
- One armour piece per slot, except **two amulets**. A third amulet replaces the oldest.
- The item's level must not be higher than the hero's level.

**Inventory:**
- 30 slots to start, +5 at the level rewards (see 3).
- Each unequipped weapon or armour piece uses one slot. A stack of the same material, or of gems or potions of the same kind and rarity, uses one slot, whatever its quantity. Equipped items, mounts and skins use none.
- Every item keeps its own slot. A new item goes to the first free slot. The player can move an item to another slot; if that slot holds an item, the two swap.
- The player can sort the inventory: every item is put one after the other from the first slot, in its current order, with no empty slot left between them.
- Filtering the inventory leaves every item in its slot and dims the ones that don't match.
- When no slot is free:
  - buying or crafting an item that needs a slot is refused, and nothing is spent;
  - unequipping is refused;
  - a reward item that doesn't fit is **lost**: contract and gathering rewards, dungeon and army loot, Mortorius, auction letters and level rewards. The player is warned before accepting. The rest of the reward (gold, XP, coins, record) is kept.
- A hero with more items than slots keeps them all, but receives nothing that needs a slot until one is free.
- Bots have no slot limit.

**Durability:**
- Item stats count in proportion to durability.
- After every fight against the game's enemies (contracts, dungeons, armies; not PvP):
  - the weapon loses `turns ÷ 2` durability, at most 10;
  - each armour piece loses `share of life lost × 10`.
- The blacksmith repairs one weapon or armour piece, equipped or in the backpack, for `(missing durability %) × price ÷ 2` gold. An intact item (100%) can't be repaired, and nothing is spent without enough gold.
- **Repair all** repairs every equipped item and costs the sum of their repairs.

**Upgrades (blacksmith, from level 10)**
- Maximum upgrades: normal 3, rare 4, legendary 5.
- Upgrade number *n* uses *n* units of **each** material listed on the item.
- Each upgrade adds **one new random bonus stat** the item does not have yet.

**Gem slots (blacksmith, in the blacksmith cities and the capital)**
- The Blacksmith of the blacksmith cities (Grimwald, Ashen City, Darkhelm) and the capital has a third section, gem slots, next to repair and upgrade.
- A weapon or armour piece (amulets included), equipped or not, can get **one** gem slot for **2500 gold**. New items have none.
- Buying is refused, and nothing is spent, when the item already has its gem slot or the hero has less than 2500 gold.
- The gem slot stays with the item: equipping, unequipping, selling and auctioning keep it.

**Gems (Alchemist, from level 41)**
- The Alchemist workshop is in the alchemy cities (Shadowmere, Nightfall Citadel) and the capital. It has three tabs: create potion, create gem and socket gem.
- Crafting a gem takes 1 of each of its three materials and no gold. Its rarity is rolled:

  | Rarity | normal | rare | epic | legendary | divine |
  |---|---|---|---|---|---|
  | Chance | 35% | 30% | 20% | 10% | 5% |
  | Tier | 1 | 2 | 3 | 4 | 5 |
  | Price | 100 | 200 | 300 | 400 | 1000 |

  | Gem | Colour | Materials | Stat |
  |---|---|---|---|
  | Ruby | red | garnet, lapis lazuli, coral | damage, tier × 45 |
  | Sapphire | blue | amethyst, lapis lazuli, pearl | defence, tier × 45 |
  | Emerald | green | emerald, obsidian, jet | health, tier × 45 |
  | Topaz | yellow | tourmaline, obsidian, amber | critical, tier × 15 % |

- A gem's value depends only on its rarity, never on the hero's level.
- Crafting is refused, and nothing is spent, when a material is missing or no inventory slot is free.
- Any gem can be set into any weapon or armour piece (amulets included) that has its **gem slot** (see Gem slots), equipped or not, for free. An item without a gem slot cannot hold a gem. An item holds one gem: setting a new one **destroys** the old one.
- The gem's stat counts with the item's other stats, in proportion to its durability.
- Gems can be sold (half price, like any item) and auctioned. An auctioned item keeps its gem.

**Potions (Alchemist, from level 41)**
- Potions are crafted in the Alchemist's create potion tab, from the ingredients below and no gold. They are only crafted: they never drop and markets don't sell them.
- The rarity is rolled when crafting: normal 94% (×1), rare 5% (×1.5), legendary 1% (×2). Rarity multiplies the boost only, never the malus of a dark potion nor the price.

  | Potion | Tier | Effect (normal) | Ingredients | Price |
  |---|---|---|---|---|
  | Orchard Tonic | natural | health +5% | 3 apple, 2 orange, 1 salmon | 120 |
  | Barkskin Brew | natural | defence +5% | 2 wood, 2 bone | 120 |
  | Hunter's Broth | natural | damage +5% | 1 wild boar, 2 deer meat | 120 |
  | Hawkeye Draught | natural | critical +5% | 3 feather, 2 pike | 120 |
  | Salmon Elixir | elaborated | health +10% | 1 glass, 2 salmon, 1 apple pie | 432 |
  | Ironbark Elixir | elaborated | defence +10% | 1 glass, 2 walnut wood, 1 steel | 444 |
  | Bloodfire Elixir | elaborated | damage +10% | 1 glass, 2 wild boar, 1 bronze | 444 |
  | Silver Eye Elixir | elaborated | critical +10% | 1 glass, 2 feather, 1 silver ingot | 468 |
  | Wrath of Obsidian | dark | damage +20%, defence −10% | 1 glass, 1 obsidian, 1 garnet, 2 bone | 648 |
  | Shroud of Jet | dark | defence +20%, damage −10% | 1 glass, 1 obsidian, 1 jet, 1 leather | 732 |
  | Pearl of the Drowned | dark | health +20%, critical −10% | 1 glass, 1 obsidian, 1 pearl, 2 salmon | 696 |
  | Amber Madness | dark | critical +20%, health −10% | 1 glass, 1 obsidian, 1 amber, 3 feather | 648 |

- Price = 1.2 × the value of the ingredients, whatever the rarity. Potions sell at half price, like any item, and cannot be auctioned.
- Crafting is refused, and nothing is spent, when an ingredient is missing or no inventory slot is free (a potion that joins its stack needs no new slot).
- The hero can drink a potion anywhere; it uses one of the stack. Its % multiplies the hero's total strength (class stats, items and sets), for example +10% damage = damage × 1.10, critical included (10% → 11%).
- **A potion lasts one battle:** the hero's next contract fight (and Mortorius or Framan after it), dungeon stage run or army run, won or lost. Afterwards every active potion is gone. PvP fights and tournaments neither use nor remove them.
- One active potion per stat: a potion that boosts a stat already boosted by an active potion is refused. A dark potion only takes up the stat it boosts. Effects on the same stat add up.

**Item stats**

| Group | Stats |
|---|---|
| Attack | damage; critical chance; true damage (ignores defence); bonus damage vs heroes; bonus damage in dungeons; bonus true damage vs heroes; bonus true damage in dungeons; fire damage; bonus vs stunned enemies; bonus vs frozen enemies; bonus vs disoriented enemies; ranged damage; melee damage |
| Defence | health; defence; stun resistance; bonus health vs heroes; bonus health in dungeons; bonus defence vs heroes; bonus defence in dungeons; fire, frozen, disorientation, ranged and melee protection |
| General | dodge; agility (decides who strikes first); mission time reduction |

Everything except damage, true damage, health, defence and agility is a percentage.

### 5. How items are generated

**Rarity chance by source**

| Source | Normal | Rare | Legendary |
|---|---|---|---|
| Most drops and missions | 94% | 5% | 1% |
| Market | 93% | 5% | 2% |
| Dungeon reward | — | 70% | 30% |

Contracts and armies have their own rarity rules (see 9 and 13).

**Stat roll**

For an item of level **L**:

```
rarity step = 1 (normal) | 1.5 (rare) | 2 (legendary)
range       = [ low base + (low growth + step) × L ,  high base + (high growth + step) × L ]
value       = random value in the range × rarity power (normal 1 | rare 1.3 | legendary 1.8)
weapon critical chance = between max(1, 0.8 L − 15) and max(2, L − 10), × rarity power
```

| Item | Base | Growth per level | Stats |
|---|---|---|---|
| Weapon | damage 5–10 | damage 3–4 | damage, critical, 1 bonus |
| Helmet, chest, pants | defence 2–12, health 20–28 | defence 4–8, health 4–8 | health, defence, 1 bonus |
| Boots, shoulders | defence 2–8, health 8–12 | defence 2–6, health 2–6 | health, defence, 1 bonus |
| Amulet | damage 4–8, health 8–12 | damage 1–2, health 2–6 | health, damage, 1 bonus |

**Price**

Price = a random value in a level range (same formula as stats), × rarity price factor (normal 1, rare 2, legendary 3).

| Item | Base | Growth per level |
|---|---|---|
| Weapon | 4–8 | 4–8 |
| Helmet, chest, pants | 5–8 | 5–10 |
| Shoulders, boots, amulet | 3–6 | 4–8 |

**Bonus stat** (one at creation, one more per upgrade)

A random stat from the pool, worth `small random base + random growth × L × rarity step`.

- **Weapon pool:** true damage, bonuses vs heroes and in dungeons, fire / stun / frozen / disorientation / ranged / melee damage, dodge, agility.
- **Armour pool:** stun resistance, bonus health and defence vs heroes and in dungeons, the five protections, dodge, agility, mission time reduction.
- Most bonuses grow about 0.1–0.3 per level.

**Upgrade materials:**
- Each item gets one random recipe for its rarity, for example steel, walnut wood, feather, gold ingot and obsidian for a legendary weapon.
- Legendary armour needs obsidian; legendary amulets need gems.

**Examples at level 10**

| Item | Damage | Defence | Health | Critical | Price |
|---|---|---|---|---|---|
| Normal sword | 45–60 | — | — | 1–2% | 54–98 |
| Legendary sword | 99–126 | — | — | 2–4% | 192–324 |
| Normal helmet | — | 52–102 | 70–118 | — | 64–118 |

**Collection sets**
- Sets are legendary items with fixed names, one set per army.
- Wearing several pieces of the same set gives extra stats (value × item level).

| Set | Pieces | Bonuses |
|---|---|---|
| Centaur | shoulders, chest, pants, boots | 2 pieces: defence · 3: melee damage · 4: melee protection |
| Wizard | two amulets | 1 piece: bonus vs disoriented · 2: disorientation protection |
| Merfolk | helmet, shoulders, chest, pants | 2: bonus vs frozen · 3: frozen protection · 4: better legendary drops (not active yet) |
| Imp | twin swords, crossbow, lance, two amulets | 2: bonus vs stunned · 3: stun resistance |
| Lizardfolk | large sword, lance, crossbow, helmet, boots | 2: agility · 3: dodge |
| Ravens of the Sanctuary | large sword, crossbow, lance, chest, pants | 2: health · 3: true damage |

### 6. Materials, gathering and crafting

**What each trade yields** (price per unit; food shows conditions restored)

| Trade | Materials |
|---|---|
| Mining | stone 5, copper 20, tin 25, iron 15, silver ore 30, gold ore 40, gems 200, obsidian 60, emerald 200, jet 200, amethyst 200, lapis lazuli 200, garnet 200, tourmaline 200 |
| Fishing | herring 5 (+1), cod 10 (+2), pike 20 (+3), salmon 50 (+5), silica 40, gems 200, pearl 200, coral 200 |
| Herboristery | orange 10 (+1), apple 10 (+1), wood 20, bone 30, walnut wood 40, thread 40, gems 200, amber 200 |
| Hunt | wild boar 40 (+8), skins 25, deer meat 30 (+6), feather 20, bone 15 |
| Market | rye bread 50 (+5), apple pie 40 (+5), roast poultry 50 (+7), feather 30, steel 30, fabric 30, leather 30, silk 30 |
| Contract rewards | sunflower seeds 5, wheat 5, peas and beans 10, barley 8, wild boar 40 (+8), apple pie 40 (+5), cod 10 (+2) |

- Cheap materials are common. Gems, obsidian and the gem materials (emerald, jet, amethyst, lapis lazuli, garnet, tourmaline, pearl, coral, amber) are rare: each gem material is at most as likely as gems.

**Gathering trips**

| Trip length | City experience |
|---|---|
| short (12 s) | +15 |
| medium (24 s) | +30 |
| long (48 s) | +60 |

How a trip works:
1. The trip yields `1 + city level` kinds of material, 1–3 units each. During **Abundance Day** it yields double.
2. When the trip ends, the hero plays a collection mini-game.
3. The hero keeps what they pick, up to `3–10 units (more for longer trips) + city level`.

**Crafting**

| Result (value) | Ingredients |
|---|---|
| refined wood (60) | 3 wood |
| stone slabs (12) | 2 stone |
| steel (70) | 4 iron |
| fabric (130) | 4 feather |
| leather (130) | 4 skins |
| gold ingot (220) | 3 gold ore |
| bronze (70) | 2 copper + 1 tin |
| silver ingot (130) | 3 silver ore |
| glass (220) | 4 silica |
| beans soup (35, food) | 3 peas and beans |
| apple pie (40, food) | 3 apples |
| bread (30, food) | 4 wheat |

### 7. Cities

| City | Kind | Trade | Required level | Own dungeon | Dungeon that must be cleared first | Governor | Contract levels |
|---|---|---|---|---|---|---|---|
| **Dredfort** (start) | settlement | hunt | 1 | Goblinoid Lair | — | Cassian | 1–30 |
| Grimshire | settlement | fishing | 1 | Wilderness Refuge | — | Alaric | 1–30 |
| Bleakmoor | settlement | mining | 1 | Duluk Caverns | — | Drogo | 1–30 |
| Blackthorn | settlement | herboristery | 9 | Snowy Caves | Goblinoid Lair | Honora | 9–38 |
| Haunted Hollow | settlement | fishing | 9 | Beast's Grotto | Wilderness Refuge | Svend | 9–38 |
| Bleakshore | settlement | hunt | 9 | Witches' Forest | Duluk Caverns | Morcant | 9–38 |
| Slabehaven | village | fishing | 21 | Crypts of Oblivion | Snowy Caves | Fiora | 21–50 |
| Duskshire | village | herboristery | 21 | Tomb of Skeletons | Beast's Grotto | Jeremiah | 21–50 |
| Emberbrook | village | mining | 21 | Ancient Wandering Castle | Witches' Forest | Hamlin | 21–50 |
| Grimwald | village | blacksmith | 41 | Labyrinth of Despair | Crypts of Oblivion | Brenna | 41–70 |
| Shadowmere | village | alchemy | 41 | Abomination Trench | Tomb of Skeletons | Orvyn | 41–70 |
| Ashen City | mayor city | blacksmith | 57 | Ancient Dwarven Kingdom | Ancient Wandering Castle | Godfrey | 57–79 |
| Nightfall Citadel | mayor city | alchemy | 57 | Fortress of the Cursed Warriors | Labyrinth of Despair | Regina | 57–79 |
| Darkhelm | mayor city | blacksmith | 57 | Khael Pit | Abomination Trench | Kenric | 57–79 |
| **Nythralen** (capital) | capital | all | 69 | Cauldron of Lost Souls | Ancient Dwarven Kingdom | King Nythar III | 69–100 |

**What a city changes**
- **Contract levels:** most contracts sit near the low end of the city's range. Only the capital goes above level 79.
- **Market materials:**
  - A gathering city sells market goods and its own trade's materials.
  - Blacksmith, alchemy and capital cities sell materials of any trade.
- **Selling:** each city pays **full price for one trade's materials**. Everything else sells at **half price**.

  | City trade | Pays full price for |
  |---|---|
  | fishing | mining materials |
  | hunt | herboristery materials |
  | mining | hunt materials |
  | herboristery | fishing materials |
  | blacksmith, alchemy, capital | nothing |

  Best trade loop: gather in one city and sell where that trade is valued. For example, mine in Bleakmoor and sell the ore in Grimshire.
- **City level** (raised by missions done in that city):
  - +1 market item per level;
  - +1 material kind per gathering trip;
  - +1 unit in the collection mini-game.
- **Auction house and stable** exist only in cities with a required level of 20 or more.
- **Alchemist** exists only in the alchemy cities and the capital, for heroes of level 41 or more (see 4, Gems and Potions).
- **Gem slots** are sold at the Blacksmith only in the blacksmith cities and the capital (see 4, Gem slots).
- **World map:** every city shows how many heroes are in it right now, bots included. Only the number is shown, never who they are.

**Market**
- Stock: `5 + city level` items.
  - 20% weapons (one level below the hero).
  - 40% armour (hero level).
  - 40% materials.
- Restocking early costs `hero level + 5` gold. Arriving in a city restocks it for free.

### 8. World events

- Every **5 days**, each event type is placed on **one random city**. No city gets two events, and the other cities have none.
- An event lasts 5 days.
- Every player receives a letter announcing each event.

| Event | Effect | Verdict |
|---|---|---|
| **Town Festival** | Market prices −30% | 🟢 **Best place to buy** |
| **Abundance Day** | Gathering yields ×2 | 🟢 **Best place to gather** |
| **Great Tournament** | One hour after it starts, every hero in the city enters a knockout PvP bracket. Odd heroes get a random free pass, and bots join. The champion wins **200 gold × number of entrants + 1 power coin**, collected by accepting a letter. | 🟡 **Big prize for strong heroes**; no stamina or durability cost |
| **Great War** | One of the 6 armies attacks the city. An army can **only** be fought during a war and only from the attacked city. | 🟡 **The only chance to farm that army's loot and set** |
| **King Penalty** | The contract board drops to a third (50 → 16) | 🔴 **Bad**: fewer contracts, less XP and gold |
| **Higher Taxes** | Buying +50%, selling −40% | 🔴 **Worst for trading**: avoid buying or selling here |

### 9. Missions

**Contract board**
- Each city has **one board shared by all players**. It holds 50 contracts, or 16 under King Penalty.
- The board refills every 5 minutes. The first hero to accept a contract takes it.
- **Starting city:** after every refill, Dredfort's board holds at least 10–20 contracts of level 1–2 (a new random number each time, at most the board size). If it has fewer, higher contracts are swapped for beginner ones.
- **Contract types:**

  | Chance | Type | Reward |
  |---|---|---|
  | 70% | **casual** or **unusual** (half and half) | casual gives materials; unusual gives normal equipment |
  | 25% | **epic** | rare equipment |
  | 5% | **legendary** | legendary equipment and a "great enemy" kill |

  - Equipment is made for the hero who accepts the contract, at the contract's level.
- **Contract length** decides the rewards:

  | Length | Gold multiplier | XP share | City experience | Stamina cost |
  |---|---|---|---|---|
  | short | ×1.3 | 50–80% | 17–23 | 2–3 |
  | medium | ×1.6 | 70–100% | 27–33 | 3–4 |
  | long | ×1.9 | 90–130% | 33–40 | 4–5 |

  - Base gold = random between `4 + 2 × level` and `10 + 6 × level`, × the length multiplier.
  - Base XP = the XP share of `50 × level² ÷ (1 + level^0.6)`, so a hero levels up in about `1 + level^0.6` contracts (2 at level 1, 9 at level 30, 17 at level 100).
  - Epic contracts pay ×1.3 gold and XP; legendary contracts pay ×1.8.
- **To accept a contract:**
  - stamina above 0;
  - no other mission in progress;
  - the hero is within **10 levels** of the contract;
  - the contract is still on the board.
- **How it plays out:**
  - The fight is decided the moment the contract is accepted. The hero comes back a few seconds later from a casual or unusual contract, 30–60 seconds later from an epic one and 3–5 minutes later from a legendary one.
  - **Win:** gold, XP, item and record updates.
  - **Loss:** no rewards.
  - Either way: a report letter and the city experience.
- **Contract enemies:**
  - Contract enemies get stronger with the contract's level and type. Legendary enemies are much tougher than casual ones.
  - Below level 6 they are half as strong.
  - They are 3 levels below the contract.
- **Mortorius, the legendary creature:**
  - 1 time in 100, after a **won** contract fight, the hero must also fight Mortorius. It never shows up in gathering trips, army runs or PvP.
  - It is at the contract enemy's level and as strong as a legendary contract enemy.
  - Its power is **black attack** (see 11).
  - **Killing it gives +5 power coins** and 1 legendary weapon or armour piece at the hero's level (a weapon one time in three). This comes on top of the contract's rewards.
  - Losing to it gives none of its rewards; the contract's rewards are kept.
  - The fight has its own report letter.
- **Framan, the three-headed legendary creature:**
  - 1 time in 100, after a **won** contract fight in which Mortorius did not appear, the hero must also fight Framan. At most one legendary creature follows a contract. It never shows up in gathering trips, army runs or PvP.
  - It is at the contract enemy's level and as strong as a legendary contract enemy.
  - Its power is **withering wail** (see 11).
  - **Killing it gives +5 power coins** and 1 legendary weapon or armour piece at the hero's level (a weapon one time in three). This comes on top of the contract's rewards.
  - Losing to it gives none of its rewards; the contract's rewards are kept.
  - The fight has its own report letter.

**Gathering trips:** see 6. **Travel:** see 2.

### 10. Battles

- A fight is **decided instantly and in full by the game**. The player then watches it as a turn-by-turn replay.
- The player never influences a fight while it runs. Strength comes from level, gear and the chosen power.

**Kinds of fights**

| Fight | Opponent | Situational bonuses that apply | Wears items | Counts as |
|---|---|---|---|---|
| Contract | contract enemy | none | yes | kill and mission |
| PvP (direct attack or tournament) | another hero | "vs heroes" bonuses | no | PvP win or loss |
| Dungeon | a chain of dungeon enemies | "in dungeons" bonuses | yes | dungeon stage |
| Army run | random army soldiers | "in dungeons" bonuses | yes | dungeon stage, at 10 kills |

**Before the first turn**
1. Each side's strength is set: class stats, gear (by durability) and set bonuses. Against the game's enemies, the hero's active potions then multiply it (see 4, Potions).
2. Situational health and defence bonuses apply.
3. Always-on powers apply, for example +30% defence.
4. **Initiative:** the side with more agility acts first. The hero wins ties.
5. "Opening" powers resolve, for example a stun on the first turn, or both sides losing half their life.

**Each turn of a side** (turns repeat until one side has no health left):
1. Turn-start effects: regeneration, stacking buffs, the hellfire aura, ….
2. **Bleeding** drains % of max life (up to 3 wounds, 3 turns each).
3. **Death curse** counts down from 5; at 0 the cursed side dies.
4. Status:
   - **Stunned:** loses the turn.
   - **Disoriented:** hits itself.
   - **Silenced:** cannot use its active power this turn.
5. If its **active power** is due this turn, it uses it. A power marked "every N turns" fires on turns 1, N+1, 2N+1, ….
6. Otherwise it makes a **normal attack**.
7. The defender may **counter-attack** (counter thrust).
8. A **burning** defender loses 5% of (health + defence), reduced by fire protection.
9. Revival: a side that just died may come back, for example *reassemble* at X% life, or *cursed oath* staying at 1 health.
10. Temporary buffs and debuffs count down and wear off.

**A normal attack, step by step**
1. **Dodge:** the defender may dodge (at most 30% chance).
2. **Critical:** chance equal to critical %. A critical multiplies damage by a random 1.1 to 2.0.
3. Conditional boosts, for example berserker below half life.
4. + "vs heroes" damage in PvP, or + "in dungeons" damage in dungeons and army runs.
5. **Ranged or melee:**
   - The fight is **ranged** if either side is a ranger.
   - It is **melee** only if both are knights or lancers, which only happens in PvP.
   - Otherwise neither applies. Ranged or melee damage bonuses apply when they match.
6. + bonus vs a stunned, frozen or disoriented defender.
7. − the defender's matching protections.
8. − flat damage reduction (for example *battle hardened*), − shield charges (*bone shield*).
9. An evading or ethereal defender takes nothing.
10. **Defence works like a shield:** damage removes defence first, then health.
11. **True damage** then goes straight to health.
12. **Fire damage** adds an extra burn share of the hit, reduced by fire protection.

**Power hits:**
- Use their own multiplier, for example 150%, 3×, or ⅓.
- A critical always doubles them.
- **Magic damage** ignores defence and is the only damage that hits an ethereal target.

**States:**
- stunned (blocked by stun resistance, at most 30%);
- disoriented;
- burning;
- frozen;
- bleeding;
- silenced;
- evading (absorbs one hit);
- ethereal;
- death curse.
- Immunity powers block negative states and debuffs.

**Limits:**
- dodge 30%, stun resistance 30%;
- fire, ranged and melee protection 80%; frozen and disorientation protection 50%;
- situational health and defence bonuses 20%;
- mission time reduction 50%;
- critical chance 100%.

**After the fight**
- The hero wins if they have health left.
- Gear wears down, except in PvP.
- PvP updates both heroes' records and sends both a letter.
- Dungeon and army XP = `50 × (last enemy level)² ÷ 10`, a tenth of a level at that enemy's level.

### 11. Powers

- A hero **unlocks** powers with **power coins** and **equips one**.
- A power is **active** (used on a schedule) or **passive** (always on, or triggered by events such as being stunned or landing a critical).
- Each class has its own tree. **Generic** powers are open to every class.
- Heroic powers (★) are the strongest of each class.
- Some passives are designed with three strength levels; only the first is in play today.

**Power tree:**
- Powers are arranged in rows by cost.
- A row opens when one power of the row above is unlocked.
- A row with a single power needs the whole row above.

**Where power coins come from:**
- every 4 levels from level 17;
- each dungeon stage cleared;
- each full army run (10 kills);
- winning a tournament;
- killing Mortorius or Framan (+5, see 9 and 12).

| Tree | Power | Kind | Cost | Effect |
|---|---|---|---|---|
| Generic | iron resolve | passive | 5 | when stunned, +15% defence |
| Generic | dazzling strike | passive | 10 | 10% chance to disorient on each attack |
| Generic | momentum | passive | 5 | +2% damage every turn |
| Generic | frostbite | passive | 10 | all damage dealt is frozen damage |
| Generic | opportunist | passive | 5 | after stunning the enemy, +10% critical for the rest of the fight |
| Generic | arcane edge | passive | 10 | all damage becomes magic damage |
| Knight | sword in blood | passive | 10 | ignores enemy defence (opening) |
| Knight | sharp needles | passive | 5 | ignores enemy defence |
| Knight | vampire blade | passive | 5 | heals a fifth of own damage before attacking |
| Knight | emberward | passive | 8 | 25% fire protection |
| Knight | battle hardened | passive | 8 | −5% damage taken |
| Knight | last stand | passive | 8 | below 25% life, immune to negative states |
| Knight | berserker ★ | passive | 15 | at half life or less, +50% damage |
| Knight | holy smite | active | 5 | magic hit ignoring defence, every 3 turns |
| Knight | whirlwind | active | 10 | two hits, every 3 turns |
| Knight | execute | active | 10 | triple damage if the enemy is below 30% life, every 2 turns |
| Knight | double swords | active | 15 | two hits for 5% of own life, every 3 turns |
| Knight | winning horse ★ | active | 10 | +20% damage and disorients, every 3 turns |
| Knight | suicide knife ★ | active | 15 | both sides lose half their life, enemy stunned (opening) |
| Lancer | lance and shield | passive | 8 | +30% defence |
| Lancer | phalanx stance | passive | 5 | +5% defence stacking each turn |
| Lancer | counter thrust | passive | 10 | 15% chance to counter a melee hit |
| Lancer | unbreakable | passive | 8 | immune to negative states for the first 2 turns |
| Lancer | protector shield ★ | passive | 15 | immune to all negative states |
| Lancer | cleric's blessing ★ | passive | 15 | +50% life |
| Lancer | impenetrable wall ★ | passive | 10 | +20% damage and +20% defence |
| Lancer | shield strike | active | 5 | stun, every 3 turns |
| Lancer | large lance | active | 10 | 20% stun chance every turn |
| Lancer | phalanx formation | active | 15 | +50% defence and reflects 30% for 3 turns |
| Lancer | spear throw | active | 10 | ranged hit ignoring half the defence, every 2 turns |
| Lancer | crusader's charge | active | 10 | 150% hit with 40% stun chance, every 4 turns |
| Ranger | ember veil | passive | 8 | 25% frozen protection |
| Ranger | sigilo | passive | 5 | +10% dodge |
| Ranger | eagle eye | passive | 5 | +10% critical |
| Ranger | hunter's mark | passive | 10 | after a hit, +10% damage on the next one |
| Ranger | wind walker | passive | 8 | 5% chance to act twice |
| Ranger | quick draw | passive | 15 | first attack is always critical |
| Ranger | double arrow | active | 8 | two hits (second one a third as strong), every 3 turns |
| Ranger | arrow in fire | active | 8 | sets the enemy on fire (opening) |
| Ranger | Harid's camouflage | active | 5 | evades the next hit, every 3 turns |
| Ranger | imperial crossbow ★ | active | 15 | three hits (full, ⅓, ⅕), every 3 turns |
| Ranger | arrow of the death ★ | active | 20 | the enemy dies in 5 turns (opening) |
| Ranger | large bow ★ | active | 15 | +100% critical, every 2 turns |

**Enemy-only powers:**
- Enemies and army soldiers have their own powers, for example dirty trick, war cry, bloodlust, skull crusher, orcish rage, troll regeneration, avalanche, rending claws, pack howl, corpse feast, paralyzing touch, hex, cauldron brew, reassemble, bone shield, stone skin, earthquake, lost in the maze, escalating fury, unstable mutation, galvanic shock, dragon breath, dragon scales, cursed oath, disarm, hellfire aura, infernal pact, soul drain and ethereal form.
- Players cannot unlock them.
- **Black attack** (Mortorius only): on its first turn the enemy's current life drops to half, rounded down and never below 1. Once per fight. Immunity powers do not block it.
- **Withering wail** (Framan only, passive): each time the hero attacks Framan, the hero's next turn deals 50% less damage, every hit of it, normal attack or power. It never stacks (always −50%). Immunity powers block it.

### 12. Dungeons

- Each city has one dungeon of **10 stages**, each with 2–4 enemies and a boss.
- Enemy strength depends on its race and level. Races, roughly weakest to strongest: goblin, savage, orc, troll, beast, ghoul, witch, skeleton, stone creature, minotaur, abomination and mage, dragon, human, hell creature, lost soul.
- **Entry fee:** `100 × stage` gold.
- **Past stage 10:** the stage-10 enemies come back 1 level higher and 25% stronger for every extra stage.
- **The run:**
  - Enemies are fought one after another. Health and defence **carry over**; states and buffs reset.
  - The run stops at the first defeat.
- **Clearing a stage gives:**
  - 1 weapon or armour piece at the hero's level (70% rare, 30% legendary);
  - the next stage unlocked;
  - +1 power coin;
  - XP.
- **Mortorius:** 1 time in 100 it waits after the stage boss, at the boss's level, with health and defence carried over. The stage is cleared by the stage enemies alone. Killing it gives the same rewards as after a contract (see 9) on top of the stage rewards.
- **Framan:** when Mortorius does not wait after the boss, Framan does 1 time in 100, in the same way and with the same rewards (see 9). At most one legendary creature per run.
- **City unlocks:** a city requires another city's dungeon to have been cleared at least once (see 7).

| Dungeon | City | Enemies | Enemy levels |
|---|---|---|---|
| Goblinoid Lair | Dredfort | goblins | 3–50 |
| Wilderness Refuge | Grimshire | savages | 4–53 |
| Duluk Caverns | Bleakmoor | orcs | 5–63 |
| Snowy Caves | Blackthorn | trolls | 9–69 |
| Beast's Grotto | Haunted Hollow | beasts | 11–72 |
| Witches' Forest | Bleakshore | witches | 21–80 |
| Crypts of Oblivion | Slabehaven | ghouls | 11–72 |
| Tomb of Skeletons | Duskshire | skeletons | 21–78 |
| Ancient Wandering Castle | Emberbrook | stone creatures | 22–82 |
| Labyrinth of Despair | Grimwald | minotaurs | 46–98 |
| Abomination Trench | Shadowmere | abominations, mages | 41–98 |
| Ancient Dwarven Kingdom | Ashen City | dragons | 60–105 |
| Fortress of the Cursed Warriors | Nightfall Citadel | cursed humans | 57–114 |
| Khael Pit | Darkhelm | hell creatures | 58–122 |
| Cauldron of Lost Souls | Nythralen | lost souls | 70–132 |

### 13. Armies

- The six armies are **Centaurs**, **Wizards**, **Merfolk**, **Lizardfolk**, **Imps** and **Ravens of the Sanctuary**. Each has 8–12 named soldiers, each with a power.
- **When an army can be fought:** only during a **Great War**, only from the attacked city, and once every **30 minutes**.
- **Rank 1–4**, chosen by the player, multiplies the soldiers' damage, health and defence. Soldiers match the hero's level.
- **The run:** random soldiers one after another, with health and defence carried over. It ends when the hero falls or after **10 kills**.
- **Loot for every kill:**

  | Rank | Normal | Rare | Legendary | Rare material |
  |---|---|---|---|---|
  | 1 | 30% | 40% | 15% | 15% |
  | 2 | 20% | 40% | 25% | 15% |
  | 3 | 5% | 45% | 35% | 15% |
  | 4 | — | 25% | 55% | 20% |

  - A legendary drop has a **1% chance** to be a piece of that army's **collection set**.
  - A drop is a weapon one time in three, armour otherwise.
- **Rewards:** loot is kept even if the hero falls. A full run of 10 kills also gives +1 power coin, a dungeon stage on the record, and XP.

### 14. Economy

**Earning gold:**
- contracts;
- selling (half price, or full price for the valued trade, then event modifiers);
- level-ups;
- challenges;
- tournaments;
- auction sales.

**Spending gold:**
- buying;
- restocking the market;
- repairs;
- gem slots (2500 each);
- dungeon entry;
- gold mounts and skins;
- auction bids.

**Power coins** are earned at milestones (see 11) and spent on powers.

**Bots:**
- A new bot hero appears every 4 hours.
- Bots gain levels, gold, gear (better rarity at higher levels), a power from level 20, and dungeon progress over time, at a pace similar to a player doing contracts.

**Gold cosmetics:**

| Mount | Speed | Gold |
|---|---|---|
| Donkey | +10% | 2000 |
| Horse | +25% | 4000 |
| White Horse | +40% | 6000 |
| Imperial Horse | +50% | 10000 |

- Skin: Bourgeois House, 15000 gold.

**Real-money cosmetics (euros):**

| Item | Effect | Price |
|---|---|---|
| Legendary Hero skin | hero look | 4.99 |
| Samurai skin | knight hero look | 2.95 |
| Arhem skin | lancer hero look | 2.95 |
| Almogavar skin | ranger hero look | 2.95 |
| Noble House | house skin | 2.99 |
| King House | house skin | 4.99 |
| Horror of the night, Unicorn, Thunderbird | +100% speed | 2.99 each |
| Great Fenix, Griffin, Pegasus | +150% speed | 4.99 each |

- A class hero skin (Samurai, Arhem, Almogavar) is only sold to and worn by heroes of its class, and it shows in the hero's gender.
- A hero wears one hero look at a time: the classic look, the Legendary Hero or a class skin.
- A purchase belongs to the hero who made it and is delivered **once** after the payment is confirmed. Cancelled or expired payments deliver nothing.
- Real money only buys cosmetics and travel speed, never power.

### 15. Auctions

- Heroes sell weapons, armour, materials and gems to each other at the **auction house**.
- **Listing an item:**
  - The seller picks a duration (24 hours by default) and an optional starting price (otherwise the item's price).
  - The item leaves the seller's inventory while the auction runs.
- **Bidding:**
  - A bid must be **higher than the current bid**, affordable, and placed before the auction ends.
  - The bid amount is **taken from the bidder's gold right away**.
  - When outbid, the previous bidder receives a letter that **returns their gold** when accepted.
  - Raising your own bid refunds your previous bid at once.
- **Many bids at the same moment:** only one is accepted. The others are told the price changed and can bid again.
- **When the auction ends:**
  - The **winner** gets a letter that delivers the item.
  - The **seller** gets a letter that pays the gold, or that returns the item if nobody bid.
  - Each auction produces these letters exactly once.
- The auction list updates live for everyone watching it.
- The marketplace also has **unique items in limited quantity**. When stock runs out, nobody else can buy that item.

### 16. Letters

- Heroes receive letters for: contract reports, PvP fights, tournament results, world events, auctions and rewards.
- Letters are deleted after **3 days**, except a tournament prize that has not been collected yet.

### 17. Open questions: rules not yet enforced or not built

Each item is either a bug or a decision still to be made. None of them is a rule.

1. **Unlocking a power** does not check that the player has enough power coins or that the power's row is open.
2. **Restocking the market** does not check the price the player pays.
3. **Ownership is not always checked.** A player could buy an item that is not in their city's market, list an item they do not own, or repair someone else's gear.
4. **Dungeon stages:** a player can choose any stage, not only the next one, and every clear counts as progress.
5. **City unlocks:** the "dungeon cleared first" requirement is only shown, not enforced.
6. **Army rank 4** is always available, with no progression to reach it.
7. **PvP has no limits:** any hero can attack any other hero, at any level, at any time.
8. **Hero stats on level-up** come out slightly off, and agility keeps adding up every level instead of following the table.
9. **City experience:** after a city level-up, the extra experience is not counted correctly.
10. **Not active yet:** mission time reduction, the Merfolk legendary-drop bonus and the free power from level 17.
11. **Abundance Day** doubles the trip's yield, but the collection mini-game ignores the double.
12. **Endless fights:** if neither side can hurt the other, a fight has no turn limit.
13. **Powers with no effect yet:** *wind walker* (double turn) and *quick draw* (guaranteed first critical). *Hunter's mark* currently gives its bonus on every attack.
