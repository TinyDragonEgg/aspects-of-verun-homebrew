# Spell Schema

## Minimal valid spell

```json
{
  "name": "Ember Bolt",
  "source": "MySource",
  "page": 0,
  "level": 1,
  "school": "V",
  "time": [{"number": 1, "unit": "action"}],
  "range": {"type": "point", "distance": {"type": "feet", "amount": 60}},
  "components": {"v": true, "s": true},
  "duration": [{"type": "instant"}],
  "entries": ["You hurl a bolt of smoldering flame at a creature or object within range."]
}
```

---

## Full spell field reference

### Required fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Spell name |
| `source` | string | Must match `_meta.sources[].json` |
| `page` | number | Page number, `0` for homebrew |
| `level` | number | 0–9 integer. 0 = cantrip. |
| `school` | string | Single capital letter. See enums. |
| `time` | array | Array of casting time objects |
| `range` | object | Range object |
| `components` | object | Components object |
| `duration` | array | Array of duration objects |
| `entries` | array | Spell description entries |

---

### `time` — casting time (array, REQUIRED)

```json
"time": [{"number": 1, "unit": "action"}]
"time": [{"number": 1, "unit": "bonus"}]
"time": [{"number": 1, "unit": "reaction", "condition": "which you take when you take damage"}]
"time": [{"number": 1, "unit": "minute"}]
"time": [{"number": 8, "unit": "hour"}]
"time": [{"number": 1, "unit": "action"}, {"number": 1, "unit": "minute"}]
```

For reactions, `condition` describes the trigger. Multiple entries mean the spell can be cast in multiple ways.

**Never:** `"time": "1 action"` (wrong — must be an array of objects)

---

### `range` — spell range (object, REQUIRED)

**Point (targeted):**
```json
{"type": "point", "distance": {"type": "feet", "amount": 60}}
{"type": "point", "distance": {"type": "miles", "amount": 1}}
{"type": "point", "distance": {"type": "touch"}}
{"type": "point", "distance": {"type": "self"}}
{"type": "point", "distance": {"type": "sight"}}
{"type": "point", "distance": {"type": "unlimited"}}
```

**Self (area of effect):**
```json
{"type": "radius", "distance": {"type": "feet", "amount": 30}}
{"type": "line", "distance": {"type": "feet", "amount": 60}}
{"type": "cone", "distance": {"type": "feet", "amount": 60}}
{"type": "cube", "distance": {"type": "feet", "amount": 15}}
{"type": "sphere", "distance": {"type": "feet", "amount": 30}}
{"type": "hemisphere", "distance": {"type": "feet", "amount": 10}}
```

**Special:**
```json
{"type": "special"}
```

**Never:** `"range": "60 feet"` or `"range": 60` (wrong — must be an object)

---

### `components` (object, REQUIRED)

```json
{"v": true}
{"v": true, "s": true}
{"v": true, "s": true, "m": "a pinch of sulfur"}
{"v": true, "s": true, "m": {"text": "a diamond worth at least 300 gp, which the spell consumes", "cost": 30000, "consume": true}}
{"r": true}
```

- `v`: verbal (boolean)
- `s`: somatic (boolean)
- `m`: material — plain string, or object for cost/consumption
  - `text`: description of the material
  - `cost`: cost in copper pieces (300 gp = 30000 cp)
  - `consume`: `true` if consumed, `"optional"` if optionally consumed
- `r`: royalty (from some sources)

---

### `duration` — spell duration (array, REQUIRED)

**Instantaneous:**
```json
[{"type": "instant"}]
```

**Timed:**
```json
[{"type": "timed", "duration": {"type": "round", "amount": 1}}]
[{"type": "timed", "duration": {"type": "minute", "amount": 1}}]
[{"type": "timed", "duration": {"type": "hour", "amount": 1}}]
[{"type": "timed", "duration": {"type": "day", "amount": 1}}]
```

**Concentration:**
```json
[{"type": "timed", "duration": {"type": "minute", "amount": 1}, "concentration": true}]
```

**Until dispelled:**
```json
[{"type": "permanent", "ends": ["dispel"]}]
[{"type": "permanent", "ends": ["dispel", "trigger"]}]
```

**Special:**
```json
[{"type": "special"}]
```

**Multiple options:**
```json
[
  {"type": "timed", "duration": {"type": "hour", "amount": 24}},
  {"type": "permanent", "ends": ["dispel"]}
]
```

**Never:** `"duration": "1 minute"` (wrong — must be an array of objects)

---

### `meta` — spell meta flags (optional)

```json
"meta": {"ritual": true}
"meta": {"technomagic": true}
```

---

### `entriesHigherLevel` — upcasting (optional)

```json
"entriesHigherLevel": [
  {
    "type": "entries",
    "name": "At Higher Levels",
    "entries": ["When you cast this spell using a spell slot of 2nd level or higher, the damage increases by {@scaledamage 1d8|2-9|1d8} for each slot level above 1st."]
  }
]
```

---

### Class and subclass lists (optional but important for filtering)

```json
"classes": {
  "fromClassList": [
    {"name": "Wizard", "source": "PHB"},
    {"name": "Sorcerer", "source": "PHB"}
  ],
  "fromSubclassList": [
    {
      "class": {"name": "Cleric", "source": "PHB"},
      "subclass": {"name": "Light", "source": "PHB"}
    }
  ],
  "fromClassListVariant": [
    {"name": "Artificer", "source": "TCE"}
  ]
}
```

---

### Filter tags (optional, help 5etools search)

```json
"damageInflict": ["fire", "radiant"],
"damageResist": ["fire"],
"damageImmune": ["lightning"],
"damageVulnerable": [],
"conditionInflict": ["poisoned", "blinded"],
"conditionImmune": [],
"savingThrow": ["dex", "con"],
"abilityCheck": ["str"],
"spellAttack": ["M", "R"],
"areaTags": ["MT", "ST", "AOE"],
"miscTags": ["SCL", "HL", "SGT", "SMN"]
```

Common `areaTags`: `"MT"` (multiple targets), `"ST"` (single target), `"AOE"` (area of effect)
Common `miscTags`: `"SCL"` (scalable), `"HL"` (higher level), `"SGT"` (requires sight), `"SMN"` (summons)

---

## Full example: concentration spell

```json
{
  "name": "Glacial Shroud",
  "source": "MySource",
  "page": 0,
  "level": 3,
  "school": "A",
  "time": [{"number": 1, "unit": "action"}],
  "range": {"type": "point", "distance": {"type": "self"}},
  "components": {"v": true, "s": true, "m": "a shard of ice"},
  "duration": [{"type": "timed", "duration": {"type": "minute", "amount": 10}, "concentration": true}],
  "classes": {
    "fromClassList": [
      {"name": "Wizard", "source": "PHB"},
      {"name": "Sorcerer", "source": "PHB"}
    ]
  },
  "entries": [
    "You wrap yourself in a shroud of swirling ice. For the duration, you gain the following benefits:",
    {
      "type": "list",
      "items": [
        "You have resistance to cold damage.",
        "When a creature within 5 feet of you hits you with a melee attack, that creature takes {@damage 2d6} cold damage.",
        "You can move across difficult terrain created by ice or snow without spending extra movement."
      ]
    }
  ],
  "entriesHigherLevel": [
    {
      "type": "entries",
      "name": "At Higher Levels",
      "entries": ["When you cast this spell using a spell slot of 4th level or higher, the cold damage increases by {@scaledamage 2d6|3-9|1d6} for each slot level above 3rd."]
    }
  ],
  "damageInflict": ["cold"],
  "savingThrow": [],
  "spellAttack": []
}
```

---

## Cantrip scaling

For cantrips that scale with character level:

```json
"entries": [
  "You hurl a mote of fire at a creature. Make a ranged spell attack. On a hit, the target takes {@scaledamage 1d10|5,11,17|1d10} fire damage.",
  {
    "type": "entries",
    "name": "Cantrip Upgrade",
    "entries": ["The spell's damage increases by {@scaledamage 1d10|5,11,17|1d10} when you reach 5th level ({@scaledamage 1d10|5,11,17|1d10}), 11th level ({@scaledamage 1d10|5,11,17|2d10}), and 17th level ({@scaledamage 1d10|5,11,17|3d10})."]
  }
]
```

The `{@scaledamage base|levels|increment}` tag handles display at different tier breakpoints.
