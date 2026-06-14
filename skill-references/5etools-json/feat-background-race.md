# Feats, Backgrounds, and Races Schema

---

# FEATS

## Minimal valid feat

```json
{
  "name": "Iron Focus",
  "source": "MySource",
  "page": 0,
  "entries": ["You have trained your mind to resist distraction, gaining the following benefits:"]
}
```

## Full feat field reference

### Required

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Feat name |
| `source` | string | Must match `_meta.sources[].json` |
| `page` | number | 0 for homebrew |
| `entries` | array | Feat description |

### Optional

| Field | Type | Notes |
|-------|------|-------|
| `prerequisite` | array | Prerequisite conditions (see below) |
| `ability` | array | Ability score improvements: `[{"str": 1}]` or `[{"choose": {"from": ["str","dex"], "count": 1}}]` |
| `skillProficiencies` | array | Skill proficiency grants |
| `languageProficiencies` | array | Language proficiency grants |
| `toolProficiencies` | array | Tool proficiency grants |
| `weaponProficiencies` | array | Weapon proficiency grants |
| `armorProficiencies` | array | Armor proficiency grants |
| `additionalSpells` | array | Spells granted |
| `resist` | array | Damage resistance grants |
| `expertise` | array | Expertise grants |
| `senses` | array | Sense grants |
| `savingThrowProficiencies` | array | Saving throw proficiencies |

### `prerequisite` structure

```json
"prerequisite": [
  {"level": {"level": 4}},
  {"ability": [{"str": 13}]},
  {"proficiency": [{"armor": "medium"}]},
  {"spellcasting": true},
  {"spellcastingFeature": true},
  {"spellcastingPrepared": true},
  {"race": [{"name": "Dwarf"}]},
  {"background": [{"name": "Soldier"}]},
  {"feat": ["alert|phb"]},
  {"other": "You must be able to see."},
  {"otherSummary": {"entry": "You must be able to see.", "entrySummary": "Can see"}}
]
```

Multiple entries in the outer array are AND conditions. The inner objects are the condition type.

### `skillProficiencies` structure

```json
"skillProficiencies": [
  {"perception": true, "stealth": true}
]
```

For choose-one:
```json
"skillProficiencies": [
  {"choose": {"from": ["arcana", "history", "nature", "religion"], "count": 1}}
]
```

### `additionalSpells` structure

```json
"additionalSpells": [
  {
    "ability": "cha",
    "known": {
      "1": ["detect magic#c"]
    },
    "innate": {
      "_": {
        "daily": {
          "1e": ["charm person"]
        }
      }
    }
  }
]
```

The `#c` suffix means the spell is a cantrip for this purpose. Keys under `innate._` can be `"daily"`, `"rest"`, etc.

### Full example feat

```json
{
  "name": "Arcane Deflection",
  "source": "MySource",
  "page": 0,
  "prerequisite": [{"spellcasting": true}],
  "entries": [
    "You have learned to weave your magic into a protective barrier, gaining the following benefits:",
    {
      "type": "list",
      "items": [
        "When you are hit by an attack, you can use your reaction to gain a +2 bonus to AC against that attack, potentially causing it to miss.",
        "When you fail a saving throw, you can use your reaction to reroll it, and you must use the new result.",
        "If you use either of these features, you can only cast cantrips until the end of your next turn."
      ]
    }
  ]
}
```

---

# BACKGROUNDS

## Minimal valid background

```json
{
  "name": "Ember Warden",
  "source": "MySource",
  "page": 0,
  "skillProficiencies": [{"athletics": true, "survival": true}],
  "entries": [
    {"type": "entries", "name": "Feature: Flame Kinship", "entries": ["You can always find shelter near fire..."]}
  ]
}
```

## Full background field reference

### Required

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Background name |
| `source` | string | Must match `_meta.sources[].json` |
| `page` | number | |
| `skillProficiencies` | array | At least one skill proficiency object |
| `entries` | array | Background description and feature |

### Optional

| Field | Type | Notes |
|-------|------|-------|
| `languageProficiencies` | array | Language grants |
| `toolProficiencies` | array | Tool grants |
| `startingEquipment` | array | Starting equipment |
| `additionalSpells` | array | Spells (rare for backgrounds) |
| `feats` | array | Starting feat (new in 2024) |
| `skillToolLanguageProficiencies` | array | Combined flexible proficiencies |
| `fromFeature` | object | Link to a feature entry |

### `languageProficiencies` structure

```json
"languageProficiencies": [
  {"anyStandard": 2}
]
"languageProficiencies": [
  {"elvish": true, "anyStandard": 1}
]
```

### `toolProficiencies` structure

```json
"toolProficiencies": [
  {"thieves' tools": true}
]
"toolProficiencies": [
  {"choose": {"from": ["herbalism kit", "poisoner's kit"], "count": 1}}
]
```

### `startingEquipment` structure

```json
"startingEquipment": [
  {
    "a": [
      {"item": "traveler's clothes|phb"},
      {"item": "dagger|phb"},
      {"value": 1000}
    ],
    "b": [
      {"value": 5000}
    ]
  }
]
```
`value` is in copper pieces. Players choose option A or B.

### Background feature (the special class feature)

Feature entries go inside the main `entries` array as a named `"entries"` type object:

```json
"entries": [
  "You spent years...",
  {
    "type": "entries",
    "name": "Feature: Eyes of the Flame",
    "entries": [
      "You can always tell where a fire has been within the last hour within 1 mile of your current location..."
    ]
  }
]
```

### Full example background

```json
{
  "name": "Runescribe",
  "source": "MySource",
  "page": 0,
  "skillProficiencies": [{"arcana": true, "history": true}],
  "languageProficiencies": [{"anyStandard": 2}],
  "toolProficiencies": [{"calligrapher's supplies": true}],
  "startingEquipment": [
    {
      "a": [
        {"item": "calligrapher's supplies|phb"},
        {"item": "ink pen|phb"},
        {"quantity": 5, "item": "ink (1 ounce bottle)|phb"},
        {"value": 1000}
      ],
      "b": [{"value": 5000}]
    }
  ],
  "entries": [
    "You have dedicated years to the study of magical script and the art of runic inscription.",
    {
      "type": "entries",
      "name": "Feature: Runic Archive",
      "entries": [
        "You have memorized a vast collection of magical sigils and their meanings. When you encounter a written magical text, inscription, or runic marking, you can usually determine its general purpose and magical school (though not its exact contents) with a few minutes of study."
      ]
    }
  ]
}
```

---

# RACES

## Minimal valid race

```json
{
  "name": "Emberkin",
  "source": "MySource",
  "page": 0,
  "size": ["M"],
  "speed": 30,
  "entries": ["The emberkin are descended from mortals touched by elemental fire."]
}
```

## Full race field reference

### Required

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Race name |
| `source` | string | |
| `page` | number | |
| `size` | string[] | Array of size codes |
| `speed` | number or object | Walk speed or speed object |
| `entries` | array | Race description and traits |

### Optional

| Field | Type | Notes |
|-------|------|-------|
| `ability` | array | Ability score improvements |
| `languageProficiencies` | array | Starting languages |
| `skillProficiencies` | array | Skill proficiencies |
| `toolProficiencies` | array | Tool proficiencies |
| `weaponProficiencies` | array | Weapon proficiencies |
| `armorProficiencies` | array | Armor proficiencies |
| `darkvision` | number | Darkvision range in feet |
| `resist` | array | Damage resistances |
| `immune` | array | Damage immunities |
| `additionalSpells` | array | Innate spellcasting |
| `traitTags` | string[] | Tags for filtering |
| `lineage` | string or boolean | `"VRGR"` or `true` for lineage races |
| `creatureTypes` | string[] | `["humanoid"]` — what type this race is |
| `age` | object | `{"mature": 20, "max": 350}` |
| `heightAndWeight` | object | Height/weight table |

### `ability` (ASI) structure

```json
"ability": [{"str": 2, "dex": 1}]
"ability": [{"choose": {"from": ["str", "dex", "con", "int", "wis", "cha"], "count": 2, "amount": 1}}]
"ability": [{"str": 2}, {"choose": {"from": ["str", "dex", "con", "int", "wis", "cha"], "count": 1, "amount": 1}}]
```

For the Tasha's/2024 floating ASI:
```json
"ability": [{"choose": {"from": ["str", "dex", "con", "int", "wis", "cha"], "count": 3, "amount": 1}}]
```

### Race entries and traits

Traits go inside `entries` as named objects. Standard format:

```json
"entries": [
  "Ember paragraphs...",
  {
    "type": "entries",
    "name": "Age",
    "entries": ["Emberkin mature at the same rate as humans and live about 100 years."]
  },
  {
    "type": "entries",
    "name": "Ember Resistance",
    "entries": ["You have resistance to fire damage."]
  },
  {
    "type": "entries",
    "name": "Born of Flame",
    "entries": ["You know the {@spell produce flame} cantrip. Constitution is your spellcasting ability for it."]
  }
]
```

---

# SUBRACES

Subraces are separate top-level entries in the `"subrace"` array:

```json
"subrace": [
  {
    "name": "Ashborn",
    "source": "MySource",
    "page": 0,
    "raceName": "Emberkin",
    "raceSource": "MySource",
    "ability": [{"wis": 1}],
    "entries": [
      {
        "type": "entries",
        "name": "Cinder Sight",
        "entries": ["You can see through smoke and ash without penalty."]
      }
    ]
  }
]
```

`raceName` and `raceSource` must match the parent race's `name` and `source` exactly.
