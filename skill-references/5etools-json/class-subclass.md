# Class and Subclass Schema

Classes are the most complex content type. This reference covers the core structures.

---

## Top-level arrays for class content

```json
{
  "class": [...],
  "subclass": [...],
  "classFeature": [...],
  "subclassFeature": [...]
}
```

Class features are defined in their own top-level array and referenced from the class definition. This keeps the class object itself manageable.

---

## Class object

### Minimal valid class

```json
{
  "name": "Ember Knight",
  "source": "MySource",
  "page": 0,
  "hd": {"number": 1, "faces": 10},
  "proficiency": ["str", "con"],
  "startingProficiencies": {
    "armor": ["light", "medium", "shields"],
    "weapons": ["simple", "martial"],
    "tools": [],
    "skills": {
      "choose": {
        "from": ["athletics", "intimidation", "perception", "survival"],
        "count": 2
      }
    }
  },
  "startingEquipment": {
    "additionalFromBackground": true,
    "default": ["(a) {@item chain mail|phb} or (b) {@item leather armor|phb}"],
    "goldAlternative": "5d4 × 10"
  },
  "classTableGroups": [...],
  "classFeatures": [...],
  "subclassTitle": "Ember Path",
  "multiclassing": {...}
}
```

### Class fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Class name |
| `source` | string | |
| `page` | number | |
| `hd` | object | Hit die: `{"number": 1, "faces": 10}` |
| `proficiency` | string[] | Saving throw proficiencies: `["str", "con"]` |
| `startingProficiencies` | object | See below |
| `startingEquipment` | object | See below |
| `classTableGroups` | array | Progression table columns |
| `classFeatures` | array | Feature references by level |
| `subclassTitle` | string | What subclasses are called (e.g., "Ember Path") |
| `multiclassing` | object | Multiclassing requirements and gains |
| `spellcastingAbility` | string | `"int"`, `"wis"`, `"cha"` — if spellcaster |
| `casterProgression` | string | `"full"`, `"1/2"`, `"1/3"`, `"pact"` |
| `preparedSpells` | string | Formula: `"classpb+wis"` |
| `cantripProgression` | number[] | Array of cantrips known per level (20 entries) |
| `spellsKnownProgression` | number[] | Array of spells known per level |

### `classFeatures` array

This is an array of feature references or feature strings:

```json
"classFeatures": [
  "Ember Sense|Ember Knight|MySource|1",
  "Fighting Style|Ember Knight|MySource|1",
  "Spellcasting|Ember Knight|MySource|1",
  "Action Surge|Ember Knight|MySource|2",
  {"classFeature": "Action Surge|Ember Knight|MySource|2", "gainSubclassFeature": false},
  "Ember Path|Ember Knight|MySource|3||{\"gainSubclassFeature\":true}",
  "Ability Score Improvement|Ember Knight|MySource|4",
  "Extra Attack|Ember Knight|MySource|5"
]
```

The format is `"Feature Name|Class Name|Source|Level"`.

When a level grants a subclass feature, use the special object form or the `gainSubclassFeature` flag.

### `classTableGroups` array

Defines the columns shown in the class progression table:

```json
"classTableGroups": [
  {
    "colLabels": ["Ember Dice"],
    "rows": [
      [{"type": "dice", "toRoll": [{"number": 1, "faces": 6}]}],
      [{"type": "dice", "toRoll": [{"number": 1, "faces": 8}]}],
      ...
    ]
  },
  {
    "title": "Spell Slots per Spell Level",
    "colLabels": ["1st", "2nd", "3rd", "4th", "5th"],
    "rowsSpellProgression": [
      [2, 0, 0, 0, 0],
      [3, 0, 0, 0, 0],
      [4, 2, 0, 0, 0],
      ...
    ]
  }
]
```

---

## ClassFeature object

```json
{
  "name": "Ember Sense",
  "source": "MySource",
  "page": 0,
  "className": "Ember Knight",
  "classSource": "MySource",
  "level": 1,
  "entries": [
    "At 1st level, you have learned to sense heat and flame. You can detect fire and extreme heat within 60 feet of you, even through solid objects."
  ]
}
```

### ClassFeature required fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Feature name |
| `source` | string | |
| `page` | number | |
| `className` | string | Must exactly match the class `name` |
| `classSource` | string | Must exactly match the class `source` |
| `level` | number | 1–20 |
| `entries` | array | Feature description |

### Optional ClassFeature fields

| Field | Type | Notes |
|-------|------|-------|
| `isClassFeatureVariant` | boolean | For optional class features (TCE variants) |
| `header` | number | Display level in UI (defaults to `level`) |
| `type` | string | `"inset"` for variant/optional features |

---

## Subclass object

```json
{
  "name": "Path of Cinders",
  "shortName": "Cinders",
  "source": "MySource",
  "page": 0,
  "className": "Ember Knight",
  "classSource": "MySource",
  "subclassTitle": "Ember Path",
  "subclassFeatures": [
    "Cinder Step|Ember Knight|MySource|Path of Cinders|MySource|3",
    "Ash Shield|Ember Knight|MySource|Path of Cinders|MySource|7",
    "Blazing Aura|Ember Knight|MySource|Path of Cinders|MySource|15",
    "Eternal Flame|Ember Knight|MySource|Path of Cinders|MySource|20"
  ]
}
```

### Subclass required fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Full subclass name |
| `shortName` | string | Short name for display (e.g., "Cinders") |
| `source` | string | |
| `page` | number | |
| `className` | string | Must match parent class `name` exactly |
| `classSource` | string | Must match parent class `source` exactly |
| `subclassTitle` | string | Should match class's `subclassTitle` |
| `subclassFeatures` | array | Feature references |

`subclassFeatures` format: `"Feature Name|Class Name|Class Source|Subclass Name|Subclass Source|Level"`

---

## SubclassFeature object

```json
{
  "name": "Cinder Step",
  "source": "MySource",
  "page": 0,
  "className": "Ember Knight",
  "classSource": "MySource",
  "subclassShortName": "Cinders",
  "subclassSource": "MySource",
  "level": 3,
  "entries": [
    "Starting at 3rd level when you choose this path, you can dash through flame without harm.",
    "When you move through a space affected by fire damage (such as a {@spell wall of fire} or standing in a bonfire), you take no fire damage from passing through."
  ]
}
```

### SubclassFeature required fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Feature name |
| `source` | string | |
| `page` | number | |
| `className` | string | Parent class name |
| `classSource` | string | Parent class source |
| `subclassShortName` | string | Must match subclass `shortName` exactly |
| `subclassSource` | string | Must match subclass `source` exactly |
| `level` | number | 1–20 |
| `entries` | array | Feature description |

---

## Optional features (`optionalfeature`)

Used for things like Eldritch Invocations, Arcane Shots, Fighting Styles, Maneuvers, etc.:

```json
{
  "name": "Cinder Strike",
  "source": "MySource",
  "page": 0,
  "featureType": ["EK:EB"],
  "prerequisite": [{"level": {"level": 5, "class": {"name": "Ember Knight", "source": "MySource"}}}],
  "entries": ["When you hit a creature with an attack, you can expend one Ember Die to deal extra fire damage equal to the die roll."]
}
```

`featureType` must match a key defined in `_meta.optionalFeatureTypes`. Built-in types include:
- `"EI"` — Eldritch Invocation
- `"MM"` — Metamagic Option
- `"FS:F"` — Fighting Style (Fighter)
- `"FS:P"` — Fighting Style (Paladin)
- `"FS:R"` — Fighting Style (Ranger)
- `"MV:B"` — Maneuver (Battle Master)
- `"AS:F20"` — Arcane Shot (Fighter 20)
- `"OTH"` — Other

Custom types must be registered in `_meta.optionalFeatureTypes`:
```json
"_meta": {
  "optionalFeatureTypes": {"EK:EB": "Ember Knight: Ember Burst"}
}
```

---

## Common class/subclass mistakes

1. **`className` and `classSource` mismatch** — if the class feature's `className` doesn't exactly match the class object's `name`, it won't associate. Case-sensitive, space-sensitive.
2. **`subclassShortName` vs `subclassName`** — SubclassFeature uses `subclassShortName` (the short name), not the full subclass name.
3. **`subclassFeatures` format** — must be `"Feature|ClassName|ClassSource|SubclassName|SubclassSource|Level"` with 5 pipes, not 3.
4. **Missing `classFeature` / `subclassFeature` entries** — the class references features by name, but if the classFeature object doesn't exist in the top-level `classFeature` array, it silently fails to display.
5. **`featureType` on optionalfeature not in `_meta.optionalFeatureTypes`** — custom types need to be registered.
