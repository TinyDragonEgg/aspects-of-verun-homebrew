# Top-Level Structure & `_meta`

## Top-level file structure

Every 5etools homebrew JSON file must have a `_meta` block and one or more content arrays:

```json
{
  "_meta": { ... },
  "monster": [ ... ],
  "spell": [ ... ],
  "item": [ ... ],
  "feat": [ ... ],
  "background": [ ... ],
  "race": [ ... ],
  "subrace": [ ... ],
  "class": [ ... ],
  "subclass": [ ... ],
  "classFeature": [ ... ],
  "subclassFeature": [ ... ],
  "optionalfeature": [ ... ],
  "table": [ ... ],
  "tableGroup": [ ... ],
  "legendaryGroup": [ ... ],
  "trap": [ ... ],
  "hazard": [ ... ],
  "reward": [ ... ],
  "vehicle": [ ... ],
  "variantrule": [ ... ],
  "condition": [ ... ],
  "disease": [ ... ],
  "action": [ ... ]
}
```

Only include the arrays you actually have content for. All arrays are optional except `_meta`.

---

## `_meta` block (REQUIRED)

```json
{
  "_meta": {
    "sources": [
      {
        "json": "MyBrewSource",
        "abbreviation": "MBS",
        "full": "My Homebrew Source Full Name",
        "url": "https://example.com",
        "authors": ["Author Name"],
        "convertedBy": ["Converter Name"],
        "version": "1.0.0",
        "color": "ff0000"
      }
    ],
    "dateAdded": 1700000000,
    "dateLastModified": 1700000000,
    "optionalFeatureTypes": {
      "AI": "Artificer Infusion",
      "EI": "Eldritch Invocation"
    }
  }
}
```

### `_meta` field rules

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `sources` | array | YES | At least one source object required |
| `sources[].json` | string | YES | Short identifier, no spaces. Must match every `source` field in content. Case-sensitive. |
| `sources[].abbreviation` | string | YES | 2-6 chars, shown in UI |
| `sources[].full` | string | YES | Full display name |
| `sources[].authors` | string[] | no | List of author names |
| `sources[].convertedBy` | string[] | no | Who converted to JSON |
| `sources[].version` | string | no | Semver or any string |
| `sources[].url` | string | no | Link to source |
| `sources[].color` | string | no | Hex color WITHOUT `#`, e.g. `"a03232"` |
| `dateAdded` | number | no | Unix timestamp (seconds) |
| `dateLastModified` | number | no | Unix timestamp (seconds) |
| `optionalFeatureTypes` | object | no | Required if you have custom `optionalfeature` types |

**Critical:** Every single content entry's `"source"` field must exactly equal one of the `sources[].json` values. If they don't match, the entry will not appear in Plutonium.

---

## Entry types (used inside `entries` arrays everywhere)

Entries arrays can contain:
- Plain strings (rendered as paragraphs)
- Entry objects with a `type` field

### Common entry object types

**`entries`** — named section with sub-entries:
```json
{
  "type": "entries",
  "name": "Section Title",
  "entries": ["Text here.", "More text."]
}
```

**`list`** — bulleted list:
```json
{
  "type": "list",
  "items": ["First item", "Second item"]
}
```
With list style:
```json
{
  "type": "list",
  "style": "list-hang-notitle",
  "items": [
    {"type": "item", "name": "Bold Label.", "entry": "Description text."}
  ]
}
```

**`table`** — a data table:
```json
{
  "type": "table",
  "caption": "Optional Table Title",
  "colLabels": ["d6", "Result"],
  "colStyles": ["col-2 text-center", "col-10"],
  "rows": [
    ["1", "First result"],
    ["2", "Second result"]
  ]
}
```

**`inset`** — boxed aside:
```json
{
  "type": "inset",
  "name": "Box Title",
  "entries": ["Boxed content."]
}
```

**`quote`** — flavor quote:
```json
{
  "type": "quote",
  "entries": ["The words spoken."],
  "by": "Speaker Name",
  "from": "Source Work"
}
```

**`inline`** / **`inlineBlock`** — inline content grouping (rare).

**`abilityDc`** — spell save DC line:
```json
{"type": "abilityDc", "name": "Spell", "attributes": ["int"]}
```

**`abilityAttackMod`** — attack bonus line:
```json
{"type": "abilityAttackMod", "name": "Spell", "attributes": ["int"]}
```

**`dice`** — a rollable dice expression:
```json
{"type": "dice", "toRoll": [{"number": 2, "faces": 6}], "rollable": true}
```

---

## Inline formatting (inside strings)

5etools uses `{@tag text}` syntax inside strings for linking and formatting:

| Tag | Example | Result |
|-----|---------|--------|
| `{@b text}` | `{@b Bold}` | **Bold** |
| `{@i text}` | `{@i Italic}` | *Italic* |
| `{@creature name}` | `{@creature goblin}` | linked creature |
| `{@spell name}` | `{@spell fireball}` | linked spell |
| `{@item name}` | `{@item longsword}` | linked item |
| `{@condition name}` | `{@condition poisoned}` | linked condition |
| `{@damage Xd6}` | `{@damage 2d6}` | rollable damage |
| `{@dice Xd6}` | `{@dice 1d20+5}` | rollable dice |
| `{@hit X}` | `{@hit 5}` | attack roll bonus (`+` is rendered automatically — do NOT include it) |
| `{@dc X}` | `{@dc 15}` | save DC |
| `{@chance X}` | `{@chance 50}` | percentage |
| `{@scaledice ...}` | (complex) | scaling dice |
| `{@atk mw}` | `{@atk mw}` | melee weapon attack |
| `{@atk rw}` | `{@atk rw}` | ranged weapon attack |
| `{@atk ms}` | `{@atk ms}` | melee spell attack |
| `{@atk rs}` | `{@atk rs}` | ranged spell attack |
| `{@recharge X}` | `{@recharge 5}` | recharge notation |
| `{@filter text\|...}` | | filtered link |
| `{@sense darkvision}` | | sense link |
| `{@skill Perception}` | | skill link |
| `{@action Dash}` | | action link |
| `{@feat Alert}` | | feat link |

Custom homebrew cross-links: `{@creature MyMonster|MySource}` — add `|SourceJson` to link to homebrew entries.

---

## Common mistakes checklist

Before finalizing any JSON, check these:

1. **`_meta` present and `sources[].json` matches every `source` field in content?**
2. **`size` is an array of single-letter codes**, not a plain string. `["M"]` not `"Medium"`.
3. **`cr` is a string**, not a number. `"1/2"` not `0.5`, `"1"` not `1`.
4. **`ac` is an array of objects** `[{"ac": 15}]`, not a plain number `15`.
5. **`hp` is an object** `{"average": 45, "formula": "7d8+14"}`, not a number.
6. **`speed` is an object** `{"walk": 30}`, not a number.
7. **`alignment` is an array** of alignment codes, not a string.
8. **Spell `time` is an array** of objects, not a string.
9. **Spell `duration` is an array** of objects, not a string.
10. **Spell `range` is an object** with `type` and `distance`, not a string like `"60 feet"`.
11. **`rarity` values are all lowercase** with spaces: `"very rare"` not `"Very Rare"`.
12. **Entry objects have a `type` field**. Objects without `type` inside `entries` arrays will break rendering.
13. **`dateAdded`/`dateLastModified` are Unix timestamps** (integers, seconds since epoch), not date strings.
14. **`passive` (passive perception) is required** on monsters and is a plain integer.
15. **`page` is required** on all entries. Use `0` for pure homebrew with no physical book page.
