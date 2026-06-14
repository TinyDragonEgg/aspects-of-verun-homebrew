# Item Schema

## Minimal valid item

```json
{
  "name": "Ember Ring",
  "source": "MySource",
  "page": 0,
  "type": "RG",
  "rarity": "rare",
  "entries": ["While wearing this ring, you have resistance to fire damage."]
}
```

---

## Full item field reference

### Required fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Display name |
| `source` | string | Must match `_meta.sources[].json` |
| `page` | number | 0 for homebrew |
| `type` | string | Item type code. **Omit for purely wondrous items** — `"wondrous": true` is the type indicator and `type` should not be added. Required for weapons (`M`/`R`), armor (`LA`/`MA`/`HA`), potions (`P`), scrolls (`SC`), rings (`RG`), etc. See enums. |
| `rarity` | string | Exact lowercase rarity string. See enums. |

---

### Common optional fields

| Field | Type | Notes |
|-------|------|-------|
| `reqAttune` | boolean or string | `true` for generic attunement, or a string like `"by a spellcaster"` |
| `weight` | number | Weight in pounds |
| `value` | number | Value in **copper pieces** (1 gp = 100 cp, 1 sp = 10 cp) |
| `entries` | array | Description. Required if the item has any text. |
| `tier` | string | `"minor"` or `"major"` |
| `wondrous` | boolean | `true` for wondrous items |
| `curse` | boolean | `true` if item is cursed |
| `sentient` | boolean | `true` if item is sentient |
| `charges` | number | Number of charges |
| `recharge` | string | `"dawn"`, `"dusk"`, `"midnight"`, `"special"` |
| `rechargeAmount` | string or object | `"1d6+1"` or `{"formula": "1d6+1"}` |
| `focus` | string[] | Spellcasting focus types: `["Arcane Focus", "Druidic Focus"]` |
| `attachedSpells` | string[] | Spell names, for scrolls/wands |
| `lootTables` | string[] | Which loot tables include this item |

---

### Attunement

```json
"reqAttune": true
"reqAttune": "by a wizard"
"reqAttune": "by a creature with the spellcasting trait"
"reqAttune": "by an evil-aligned creature"
```

---

### Weapon-specific fields

Used when `type` is `"M"` (melee weapon) or `"R"` (ranged weapon):

| Field | Type | Notes |
|-------|------|-------|
| `weaponCategory` | string | `"simple"` or `"martial"` |
| `property` | string[] | Property codes. See enums. |
| `dmg1` | string | One-hand damage dice: `"1d8"` |
| `dmg2` | string | Two-hand damage dice (versatile): `"1d10"` |
| `dmgType` | string | Damage type letter: `"S"`, `"P"`, `"B"` |
| `range` | string | Thrown/ranged range: `"20/60"` |
| `reload` | number | Number of shots before reload |

```json
{
  "name": "Burning Blade",
  "source": "MySource",
  "page": 0,
  "type": "M",
  "rarity": "uncommon",
  "reqAttune": true,
  "weaponCategory": "martial",
  "property": ["F"],
  "dmg1": "1d8",
  "dmgType": "S",
  "entries": [
    "This magic longsword's blade is perpetually wreathed in harmless orange flame.",
    "While attuned to this weapon, you deal an extra {@damage 1d4} fire damage on each hit."
  ]
}
```

---

### Armor-specific fields

Used when `type` is `"LA"`, `"MA"`, or `"HA"`:

| Field | Type | Notes |
|-------|------|-------|
| `ac` | number | Base AC of the armor |
| `strength` | number | Strength requirement (heavy armor) |
| `stealth` | boolean | `true` if disadvantage on Stealth |
| `armor` | boolean | `true` — mark as armor for type-specific display |

```json
{
  "name": "Shadowweave Armor",
  "source": "MySource",
  "page": 0,
  "type": "MA",
  "rarity": "rare",
  "reqAttune": true,
  "ac": 14,
  "armor": true,
  "entries": ["While wearing this armor, you have advantage on Dexterity (Stealth) checks."]
}
```

---

### Potion

```json
{
  "name": "Potion of Firebreath",
  "source": "MySource",
  "page": 0,
  "type": "P",
  "rarity": "uncommon",
  "entries": [
    "When you drink this potion, you gain the ability to exhale fire in a 15-foot cone for 1 hour.",
    "Each creature in that area must make a {@dc 13} Dexterity saving throw, taking {@damage 4d6} fire damage on a failed save, or half as much on a success.",
    "The effect ends after you exhale fire three times or when the hour ends."
  ]
}
```

---

### Scroll

```json
{
  "name": "Scroll of Cinder Storm",
  "source": "MySource",
  "page": 0,
  "type": "SC",
  "rarity": "rare",
  "entries": ["A spell scroll bears the words of a single spell, written in a mystical cipher."],
  "attachedSpells": ["Cinder Storm"]
}
```

---

### Staff / Wand / Rod with charges

```json
{
  "name": "Staff of the Emberveil",
  "source": "MySource",
  "page": 0,
  "type": "ST",
  "rarity": "very rare",
  "reqAttune": "by a spellcaster",
  "charges": 10,
  "recharge": "dawn",
  "rechargeAmount": "1d6+4",
  "focus": ["Arcane Focus", "Druidic Focus"],
  "entries": [
    "This staff has 10 charges and regains {@dice 1d6+4} expended charges daily at dawn.",
    {
      "type": "entries",
      "name": "Spells",
      "entries": [
        "While holding this staff, you can use an action to expend 1 or more of its charges to cast one of the following spells from it (save {@dc 16}):",
        {
          "type": "list",
          "items": [
            "{@spell fire bolt} (1 charge)",
            "{@spell scorching ray} (2 charges)",
            "{@spell fireball} (3 charges)"
          ]
        }
      ]
    }
  ],
  "attachedSpells": ["fire bolt", "scorching ray", "fireball"]
}
```

---

### `additionalSources` — additional printing info

```json
"additionalSources": [{"source": "XGE", "page": 141}]
```

---

### Item variants / base items

For magic versions of mundane items, link to the base item:

```json
"baseItem": "longsword|PHB"
```

The format is `"itemName|SOURCE"`.

---

## Common item mistakes

1. **`"rarity": "Very Rare"`** — wrong. Must be `"very rare"` (all lowercase, with space).
2. **`"type": "Wand"`** — wrong. Must be the code `"WD"`.
3. **`"value": 500`** — this is 500 copper (5 gold), not 500 gold. 500 gp = `"value": 50000`.
4. **Missing `reqAttune`** for an item that requires attunement — it just won't show the attunement requirement in Plutonium.
5. **`"charges": 0`** — omit the field if no charges, don't set to 0.
6. **`"wondrous": false`** — omit the field if not wondrous, don't set to false.
7. **`"weaponCategory"` on non-weapons** — only valid when `type` is `"M"` or `"R"`.
8. **Adding `"type": "OTH"` to wondrous items** — don't. If `"wondrous": true` is set and the item has no physical form category (not a ring, rod, wand, staff, etc.), omit `type` entirely.
