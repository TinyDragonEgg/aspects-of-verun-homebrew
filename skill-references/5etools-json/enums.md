# Valid Enum Values

## Creature size codes (array of strings)

| Code | Meaning |
|------|---------|
| `"F"` | Fine |
| `"D"` | Diminutive |
| `"T"` | Tiny |
| `"S"` | Small |
| `"M"` | Medium |
| `"L"` | Large |
| `"H"` | Huge |
| `"G"` | Gargantuan |
| `"C"` | Colossal |

`size` is always an **array**: `["M"]`, `["L"]`, `["S", "M"]` (for variable-size creatures).

---

## Alignment codes

`alignment` is an **array** of strings. Law axis and moral axis codes combine:

| Code | Meaning |
|------|---------|
| `"L"` | Lawful |
| `"NX"` | Neutral (law axis only, for "neutral X") |
| `"C"` | Chaotic |
| `"G"` | Good |
| `"NY"` | Neutral (moral axis only, for "X neutral") |
| `"E"` | Evil |
| `"N"` | Neutral (true neutral / unspecified axis) |
| `"U"` | Unaligned |
| `"A"` | Any alignment |

**Examples:**
- Lawful Good: `["L", "G"]`
- Chaotic Evil: `["C", "E"]`
- True Neutral: `["NX", "NY"]`
- Chaotic Neutral: `["C", "NY"]`
- Lawful Neutral: `["L", "NX"]`
- Neutral Good: `["NX", "G"]`
- Neutral Evil: `["NX", "E"]`
- Unaligned: `["U"]`
- Any alignment: `["A"]`
- Any chaotic: `["C", "A"]`
- Any non-good: `[{"special": "any non-good alignment"}]`

Special alignment object: `{"special": "as the souls it has captured"}` — use for narrative descriptions.
Chance-based: `{"chance": 50, "alignment": ["L", "G"]}` — 50% chance of that alignment.

---

## Spell schools

| Code | School |
|------|--------|
| `"A"` | Abjuration |
| `"C"` | Conjuration |
| `"D"` | Divination |
| `"E"` | Enchantment |
| `"V"` | Evocation |
| `"I"` | Illusion |
| `"N"` | Necromancy |
| `"T"` | Transmutation |
| `"P"` | Psionic (unofficial, avoid unless needed) |

---

## Spell time units

Used in `time[].unit`:
`"action"`, `"bonus"`, `"reaction"`, `"minute"`, `"hour"`, `"day"`, `"round"`

---

## Spell duration types and units

`duration[].type`: `"instant"`, `"timed"`, `"permanent"`, `"special"`

`duration[].duration.type` (when timed): `"round"`, `"minute"`, `"hour"`, `"day"`, `"year"`

---

## Spell range types and distance types

`range.type`: `"point"`, `"radius"`, `"line"`, `"cone"`, `"cube"`, `"hemisphere"`, `"sphere"`, `"special"`

`range.distance.type`:
- `"feet"`, `"miles"`
- `"self"` — always paired with range type of `"point"` for self-only, or a shape type for AoE
- `"touch"`
- `"sight"`
- `"unlimited"`
- `"plane"` (planar range)

---

## Damage types

`"acid"`, `"bludgeoning"`, `"cold"`, `"fire"`, `"force"`, `"lightning"`, `"necrotic"`, `"piercing"`, `"poison"`, `"psychic"`, `"radiant"`, `"slashing"`, `"thunder"`

---

## Conditions

`"blinded"`, `"charmed"`, `"deafened"`, `"exhaustion"`, `"frightened"`, `"grappled"`, `"incapacitated"`, `"invisible"`, `"paralyzed"`, `"petrified"`, `"poisoned"`, `"prone"`, `"restrained"`, `"stunned"`, `"unconscious"`

---

## Item type codes

| Code | Meaning |
|------|---------|
| `"A"` | Ammunition |
| `"AF"` | Ammunition (Firearm) |
| `"AT"` | Artisan's Tools |
| `"EM"` | Eldritch Machine |
| `"EXP"` | Explosive |
| `"FD"` | Food and Drink |
| `"G"` | Adventuring Gear |
| `"GS"` | Gaming Set |
| `"HA"` | Heavy Armor |
| `"INS"` | Instrument |
| `"LA"` | Light Armor |
| `"M"` | Melee Weapon |
| `"MA"` | Medium Armor |
| `"MNT"` | Mount |
| `"OTH"` | Other |
| `"P"` | Potion |
| `"R"` | Ranged Weapon |
| `"RD"` | Rod |
| `"RG"` | Ring |
| `"S"` | Shield |
| `"SC"` | Scroll |
| `"SCF"` | Spellcasting Focus |
| `"SHP"` | Waterborne Vehicle |
| `"ST"` | Staff |
| `"T"` | Tools |
| `"TAH"` | Tack and Harness |
| `"TG"` | Trade Goods |
| `"VEH"` | Vehicle (Land) |
| `"AIR"` | Airborne Vehicle |
| `"WD"` | Wand |
| `"$"` | Currency |

---

## Item rarity values (exact lowercase strings)

`"none"`, `"common"`, `"uncommon"`, `"rare"`, `"very rare"`, `"legendary"`, `"artifact"`, `"varies"`, `"unknown"`, `"unknown (magic)"`

Note: `"very rare"` has a space and is all lowercase. This is a frequent mistake.

---

## Item tier values

`"minor"`, `"major"`

---

## Item property codes (common)

| Code | Meaning |
|------|---------|
| `"A"` | Ammunition |
| `"AF"` | Ammunition (Firearm) |
| `"BF"` | Burst Fire |
| `"F"` | Finesse |
| `"H"` | Heavy |
| `"L"` | Light |
| `"LD"` | Loading |
| `"R"` | Reach |
| `"RLD"` | Reload |
| `"S"` | Special |
| `"T"` | Thrown |
| `"V"` | Versatile |
| `"2H"` | Two-Handed |

---

## Weapon damage types (for `dmgType`)

Same as damage types above. Common: `"S"` (slashing), `"P"` (piercing), `"B"` (bludgeoning) — NOTE: for `dmgType` field on weapons, use the first letter: `"S"`, `"P"`, `"B"`.

Wait — this is a critical distinction: for `immune`/`resist`/`vulnerable` arrays the full string like `"fire"` is used, but for weapon `dmgType` the single letter codes are used: `"S"` = slashing, `"P"` = piercing, `"B"` = bludgeoning.

---

## Creature type strings (for `type` field on monsters)

Common values: `"aberration"`, `"beast"`, `"celestial"`, `"construct"`, `"dragon"`, `"elemental"`, `"fey"`, `"fiend"`, `"giant"`, `"humanoid"`, `"monstrosity"`, `"ooze"`, `"plant"`, `"undead"`

Can be a plain string, or an object with tags:
```json
{"type": "humanoid", "tags": ["elf", "any race"]}
```
Or with swarm info:
```json
{"type": "beast", "swarmSize": "T"}
```

---

## Challenge rating (CR) values (always strings)

`"0"`, `"1/8"`, `"1/4"`, `"1/2"`, `"1"` through `"30"`

CR can also be an object for creatures with lair/coven ratings:
```json
{"cr": "5", "lair": "6", "coven": "7"}
```

**Never use a number.** `"1"` not `1`, `"0.5"` is wrong — use `"1/2"`.

---

## Ability score keys

`"str"`, `"dex"`, `"con"`, `"int"`, `"wis"`, `"cha"` — always lowercase, always 3 letters.

Used in `save`, `skill`, `ability` (for feats), `check` prerequisite objects, and spellcasting objects.

---

## Skill names (for `skill` field on monsters and proficiency objects)

`"acrobatics"`, `"animal handling"` (with space), `"arcana"`, `"athletics"`, `"deception"`, `"history"`, `"insight"`, `"intimidation"`, `"investigation"`, `"medicine"`, `"nature"`, `"perception"`, `"performance"`, `"persuasion"`, `"religion"`, `"sleight of hand"` (with spaces), `"stealth"`, `"survival"`

All lowercase, spaces where appropriate.

---

## Speed movement types (keys in `speed` object)

`"walk"`, `"fly"`, `"swim"`, `"climb"`, `"burrow"`, `"hover"` (boolean, not a number)

`"hover": true` means the creature hovers (can't go prone, etc.). It accompanies a `"fly"` value.
If a fly speed has a condition: `{"fly": {"number": 30, "condition": "with wings"}}`

---

## Official source abbreviations (common)

| Abbreviation | Book |
|---|---|
| `PHB` | Player's Handbook |
| `MM` | Monster Manual |
| `DMG` | Dungeon Master's Guide |
| `XGE` | Xanathar's Guide to Everything |
| `TCE` | Tasha's Cauldron of Everything |
| `MTF` | Mordenkainen's Tome of Foes |
| `VGM` | Volo's Guide to Monsters |
| `MPMM` | Mordenkainen Presents: Monsters of the Multiverse |
| `FTD` | Fizban's Treasury of Dragons |
| `SCC` | Strixhaven: Curriculum of Chaos |
| `AI` | Acquisitions Incorporated |
| `GGR` | Guildmasters' Guide to Ravnica |
| `ERLW` | Eberron: Rising from the Last War |
| `MOT` | Mythic Odysseys of Theros |
| `IDRotF` | Icewind Dale: Rime of the Frostmaiden |
| `CM` | Candlekeep Mysteries |
| `WBtW` | The Wild Beyond the Witchlight |
| `CRCotN` | Critical Role: Call of the Netherdeep |
| `DSotDQ` | Dragonlance: Shadow of the Dragon Queen |
| `KftGV` | Keys from the Golden Vault |
| `BGG` | Bigby Presents: Glory of the Giants |
| `PAITM` | Planescape: Adventures in the Multiverse |
| `BMT` | The Book of Many Things |
| `HF` | Heroes' Feast |
| `ToA` | Tomb of Annihilation |
| `CoS` | Curse of Strahd |
| `PotA` | Princes of the Apocalypse |
| `OotA` | Out of the Abyss |
| `SKT` | Storm King's Thunder |
| `TftYP` | Tales from the Yawning Portal |
| `HotDQ` | Hoard of the Dragon Queen |
| `RoT` | The Rise of Tiamat |
| `LMoP` | Lost Mine of Phandelver |
| `HBR` | Homebrew (generic, use your own source instead) |
| `UAx` | Unearthed Arcana (various) |
| `SCREEN` | D&D Dungeon Master's Screen |
