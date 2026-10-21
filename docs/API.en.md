# API 2.0 — systems, roles and cultural titles

The system defines **the organization**; the theme defines **its titles**. Optional
size, structure and authority parameters shape the result. Request all matching
offices rather than guessing an office ID first.

```json
{"system":"nation","theme":"russian-kremlin","authority":"aristocratic","locale":"en"}
```

| Field | Meaning | Default |
|---|---|---|
| `system` | System ID or alias | required |
| `theme` | Cultural theme, including all 41 Magna Urbis culture IDs | `generic` |
| `size` | `tiny`, `small`, `medium`, `large`, `vast`, `full` | `full` |
| `members` | Positive group headcount, used instead of size | absent |
| `structure` | `hierarchical`, `horizontal`, `network`, `cellular` | system default |
| `authority` | `hereditary`, `aristocratic`, `authoritarian`, `democratic`, `theocratic`, `military`, `bureaucratic`, `meritocratic`, `consensual`, `personal` | system default |
| `locale` | Presentation language, with FR/EN built in | `fr` |
| `filter` | Role selection | none |
| `api_version` | Contract version | `2.0` |

Headcount selects structural complexity: 1–5 tiny, 6–30 small, 31–300 medium,
301–10,000 large, then vast. It does not create people or imply one distinct holder
per office. `full` includes every available tier. A small kingdom remains a kingdom.

Filters are `text`, `max_level`, `min_importance`, `functions` and `scopes`. Different
criteria combine with AND; values within one list are alternatives. Text matches
French, English and original titles as well as IDs/functions. Aliases normalize
case, accents, spaces, hyphens and underscores. Canonical IDs take precedence.

## Roles

Each role separates:

- `id`: office ID within the system;
- `function`: stable semantic responsibility;
- `title_key`: lexicon selector;
- `title`: French/English title, optional original spelling and authored variants;
- `level`: local tier, 0 at the top;
- `importance`: local institutional weight, 0–100, independently of rank;
- `scope`: realm, province, city, village, organization, unit, household, cell or network;
- `reports_to`: other retained office IDs;
- `duties`, `powers`, `selection`: responsibility, competences and access to office;
- `collective`, `optional`: collective body and optional specialization;
- `title_theme`: lexicon that supplied the title.

The response also contains normalized request, API/content versions, system/theme
context, effective organization settings, available role count, related systems and
notes. Filtering reconnects reporting edges to the nearest retained parent so no
orphan references remain.

The authority override changes state-head title selection and access-to-office
content. Authoritarian organization adds decree power and concentrates the top
hierarchical tier. Horizontal structure flattens tiers and removes command; a
network removes global reporting; cells may retain internal hierarchy. A default
horizontal corporate house retains its traditional house-head title.

Themes inherit a parent lexicon, then generic terms. A niche office may have a
functional title fallback. All combinations are available: these are worldbuilding
interpretations and freely reusable lore, without historical-source gates.

Locale projects `display_title` and `display_duties` using exact language, base
language, then English. The full bilingual content remains present. Additional
language keys are extensible. No automatic translation or gender inference.

## Transports

- Rust: `Engine::embedded()?.resolve(query)`; reuse the engine for batch requests.
- JSON: `pecking_order::resolve_json(request)`.
- CLI: `pecking-order resolve request.json`, or `resolve -` from standard input.
- HTTP: `POST /api/resolve`, JSON up to 65,536 bytes.
- Catalogue: `GET /api/catalog`; lexicon: `GET /api/themes/{id}`.
- Schemas: `/api/schema/query`, `/api/schema/response`, or the checked-in `schemas/`.
- Custom content: `Engine::from_json` takes a full `systems`, `themes`, `city_cultures`, `powers` pack.

Valid responses are 200. Invalid query/selection is 400, foreign origin 403,
oversized body 413, unsupported content type 415, unknown route 404. Selection
errors contain code, field, bilingual message and suggestions. Transport errors
may contain only code. The local explorer binds to loopback only.

Resolution uses no network, randomness, machine clock or sibling repository.
Store request plus content version, or archive the result, for replay. Person
assignment belongs to Lineage Lab, names to Namebench and locations to Magna Urbis.
The schema describes offices, not a succession or population simulator.
