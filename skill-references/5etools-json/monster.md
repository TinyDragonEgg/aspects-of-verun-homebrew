# Monster Schema

## Minimal valid monster

```json
{
  "name": "Stone Lurker",
  "source": "MySource",
  "page": 0,
  "size": ["M"],
  "type": "monstrosity",
  "alignment": ["U"],
  "ac": [{"ac": 14, "from": ["natural armor"]}],
  "hp": {"average": 45, "formula": "6d8+18"},
  "speed": {"walk": 30},
  "str": 18, "dex": 10, "con": 16, "int": 5, "wis": 12, "cha": 6,
  "passive": 11,
  "cr": "2",
  "entries": []
}
```

---

## Full monster field reference

### Identity fields (all required)

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Display name |
| `source` | string | Must match `_meta.sources[].json` |
| `page` | number | Page number, `0` for homebrew |

### Size, type, alignment (all required)

| Field | Type | Notes |
|-------|------|-------|
| `size` | string[] | Array of size codes. Usually `["M"]`. See enums. |
| `type` | string or object | See below |
| `alignment` | array | Array of alignment codes or special objects. See enums. |

**`type` as plain string:** `"humanoid"`

**`type` as object with tags:** `{"type": "humanoid", "tags": ["elf"]}`

**`type` as object with swarm:** `{"type": "beast", "swarmSize": "T"}` (T = Tiny, S = Small, etc.)

**`type` with multiple types:** `{"type": "fiend", "tags": ["devil"]}`

### Defenses (all required)

| Field | Type | Notes |
|-------|------|-------|
| `ac` | array | Array of AC objects or numbers. See below. |
| `hp` | object | `{"average": N, "formula": "XdY+Z"}` |

**`ac` formats:**
- Simple: `[{"ac": 13}]`
- With source: `[{"ac": 13, "from": ["natural armor"]}]`
- With condition: `[{"ac": 13, "condition": "in lair", "braces": true}]`
- Multiple: `[{"ac": 13}, {"ac": 16, "from": ["shield"], "condition": "with shield"}]`
- Special: `[{"special": "equal to 10 + its Charisma modifier"}]`

**Never:** `"ac": 13` (wrong — not an array, not an object)

**`hp` formats:**
- Standard: `{"average": 45, "formula": "6d8+18"}`
- Special: `{"special": "equal to five times its CR"}` — use when the formula doesn't apply
- No formula (simple fixed): `{"average": 1}` — formula can be omitted but average is required

### Speed (required)

```json
"speed": {"walk": 30}
"speed": {"walk": 30, "fly": 60, "hover": true}
"speed": {"walk": 30, "swim": 20, "climb": 20}
"speed": {"walk": 0, "burrow": 20}
"speed": {"fly": {"number": 30, "condition": "(with wings)"}}
"speed": {"walk": 30, "canHover": true}
```

`hover: true` means levitates (not truly flying, immune to prone). `canHover: true` on the fly speed means it can hover in place.

### Ability scores (all required, plain integers)

`str`, `dex`, `con`, `int`, `wis`, `cha` — all integers, e.g. `"str": 18`

### Saving throws (optional)

```json
"save": {"str": "+5", "dex": "+3"}
```
Values are strings with sign: `"+5"` not `5`.

### Skills (optional)

```json
"skill": {"perception": "+5", "stealth": "+3"}
```
All skill names lowercase with spaces (`"animal handling"`, `"sleight of hand"`). Values are strings with sign.

### Resistances/immunities/vulnerabilities (optional)

```json
"immune": ["fire", "poison"],
"resist": ["bludgeoning", "piercing", "slashing"],
"vulnerable": ["cold"],
"conditionImmune": ["poisoned", "charmed"]
```

All are arrays of lowercase strings. Can also contain objects for conditional immunity:
```json
"immune": [
  "fire",
  {"immune": ["bludgeoning", "piercing", "slashing"], "note": "from nonmagical weapons", "cond": true}
]
```

`preNote` renders **before** the damage list; `note` renders **after**. Both are valid:
```json
{"vulnerable": ["bludgeoning", "thunder"], "preNote": "While in solid form,"}
{"resist": ["piercing", "slashing"], "note": "from nonmagical attacks", "cond": true}
```

### Senses (optional, array of strings)

```json
"senses": ["darkvision 60 ft.", "tremorsense 30 ft."]
```

### Passive perception (REQUIRED)

```json
"passive": 12
```
This is a plain integer. It must always be present. If the creature has no special Perception, calculate: 10 + Wisdom modifier (+ proficiency if proficient).

### Languages (optional, array of strings)

```json
"languages": ["Common", "Draconic"]
```
Use `"--"` for no languages. Use `"any one language (usually Common)"` for humanoid templates.
Telepathy: `"telepathy 60 ft."`

### CR (required)

```json
"cr": "1/2"
"cr": "5"
"cr": "20"
"cr": {"cr": "5", "lair": "6", "coven": "7"}
```

Always a string or an object. Never a number.

### `isNpc` flag (optional)

```json
"isNpc": true
```
Marks this as an NPC rather than a monster. Affects display in some tools.

---

## Traits, actions, reactions, legendary actions

All follow the same entry object structure:

```json
"trait": [
  {
    "name": "Trait Name",
    "entries": ["Description text with {@damage 1d6} fire damage."]
  }
],
"action": [
  {
    "name": "Multiattack",
    "entries": ["The creature makes two attacks."]
  },
  {
    "name": "Bite",
    "entries": ["{@atk mw} {@hit 5} to hit, reach 5 ft., one target. {@h}{@damage 2d6+3} piercing damage."]
  }
],
"reaction": [
  {
    "name": "Parry",
    "entries": ["The creature adds 2 to its AC against one melee attack that would hit it."]
  }
],
"bonus": [
  {
    "name": "Shadow Step",
    "entries": ["The creature teleports up to 60 feet to an unoccupied space it can see."]
  }
],
"legendary": [
  {
    "name": "Legendary Action Name",
    "entries": ["Description."]
  }
],
"mythic": [
  {
    "name": "Mythic Action Name",
    "entries": ["Description."]
  }
]
```

### Legendary action header and count

```json
"legendaryActions": 3,
"legendaryHeader": [
  "The dragon can take 3 legendary actions, choosing from the options below.",
  "Only one legendary action option can be used at a time and only at the end of another creature's turn.",
  "The dragon regains spent legendary actions at the start of its turn."
]
```

If `legendaryActions` is omitted, defaults to 3. The header is optional but recommended for non-standard legendary action rules.

### Mythic header

```json
"mythicHeader": ["If the creature's Mythic trait is active, it can use the options below..."]
```

### Recharge notation in action names

```json
{"name": "Fire Breath {@recharge 5}", "entries": ["..."]}
```
`{@recharge 5}` renders as "(Recharge 5-6)", `{@recharge 6}` renders as "(Recharge 6)".

### Costs in legendary actions

```json
{
  "name": "Wing Attack (Costs 2 Actions)",
  "entries": ["..."]
}
```

---

## Spellcasting

```json
"spellcasting": [
  {
    "name": "Spellcasting",
    "headerEntries": [
      "The mage is a 9th-level spellcaster. Its spellcasting ability is Intelligence (spell save {@dc 14}, {@hit 6} to hit with spell attacks). The mage has the following wizard spells prepared:"
    ],
    "spells": {
      "0": {"spells": ["{@spell fire bolt}", "{@spell light}"]},
      "1": {"slots": 4, "spells": ["{@spell detect magic}", "{@spell magic missile}"]},
      "2": {"slots": 3, "spells": ["{@spell misty step}"]},
      "3": {"slots": 3, "spells": ["{@spell counterspell}", "{@spell fireball}"]},
      "4": {"slots": 3, "spells": ["{@spell greater invisibility}"]},
      "5": {"slots": 1, "spells": ["{@spell cone of cold}"]}
    },
    "ability": "int",
    "type": "spellcasting"
  }
]
```

For innate spellcasting:
```json
{
  "name": "Innate Spellcasting",
  "headerEntries": [
    "The creature's innate spellcasting ability is Charisma (spell save {@dc 14}). It can innately cast the following spells, requiring no material components:"
  ],
  "will": ["{@spell detect magic}", "{@spell disguise self}"],
  "daily": {
    "3e": ["{@spell charm person}"],
    "1e": ["{@spell dominate person}"]
  },
  "ability": "cha",
  "type": "spellcasting"
}
```

`daily` keys: `"1e"` (1/day each), `"2e"` (2/day each), `"3e"` (3/day each), `"1"` (1/day), etc.

---

## Legendary group (cross-reference)

```json
"legendaryGroup": {
  "name": "Tiamat",
  "source": "FTD"
}
```

Links to a `legendaryGroup` entry for shared lair actions.

---

## Variant and familiar blocks

```json
"variant": [
  {
    "type": "variant",
    "name": "Variant: Familiar",
    "entries": ["Some familiars..."],
    "variantSource": [{"source": "PHB", "page": 347}]
  }
]
```

---

## Tags for filtering

```json
"miscTags": ["MW", "RW", "AOE", "HPR"],
"damageTags": ["A", "C", "F"],
"actionTags": ["Multiattack", "Spellcasting"],
"languageTags": ["C", "DR"],
"senseTags": ["D", "SD", "B"],
"traitTags": ["Legendary Resistances", "Shapechanger"]
```

These are optional but help 5etools search/filter. Don't fabricate tag codes — omit if unsure.

---

## Full example: Medium humanoid monster

```json
{
  "name": "Crimson Blade Duelist",
  "source": "MySource",
  "page": 0,
  "size": ["M"],
  "type": {"type": "humanoid", "tags": ["any race"]},
  "alignment": ["L", "E"],
  "ac": [{"ac": 16, "from": ["studded leather armor"]}],
  "hp": {"average": 78, "formula": "12d8+24"},
  "speed": {"walk": 30},
  "str": 14, "dex": 18, "con": 14, "int": 12, "wis": 11, "cha": 14,
  "save": {"dex": "+7", "wis": "+3"},
  "skill": {"acrobatics": "+7", "perception": "+3"},
  "passive": 13,
  "languages": ["Common", "Thieves' Cant"],
  "cr": "5",
  "trait": [
    {
      "name": "Evasion",
      "entries": ["If the duelist is subjected to an effect that allows it to make a Dexterity saving throw to take only half damage, it instead takes no damage if it succeeds on the saving throw, and only half damage if it fails."]
    }
  ],
  "action": [
    {
      "name": "Multiattack",
      "entries": ["The duelist makes three Rapier attacks."]
    },
    {
      "name": "Rapier",
      "entries": ["{@atk mw} {@hit 7} to hit, reach 5 ft., one target. {@h}{@damage 1d8+4} piercing damage."]
    }
  ],
  "reaction": [
    {
      "name": "Riposte",
      "entries": ["When a creature misses the duelist with a melee attack, the duelist can make one Rapier attack against that creature."]
    }
  ]
}
```
