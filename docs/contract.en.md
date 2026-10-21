# Query contract 1.0

The same object is accepted by Python, the CLI and `POST /api/resolve`.
[JSON schemas](../schemas/) are generated from the runtime models. Unknown fields
and implicit type coercion are rejected. Identifiers are language-independent.

```json
{
  "culture": "tswana_bogosi_contemporary",
  "organization": {"kind": "village_council", "scale": "local"},
  "role": "executive",
  "locale": "en"
}
```

| Field | Meaning | Default |
|---|---|---|
| `schema_version` | Exactly `1.0` | `1.0` |
| `culture` | Bounded profile ID, known alias, or `*` for generic mode | required |
| `organization.kind` | Catalogue institution ID | required |
| `organization.scale` | Institutional reach, independently of headcount | required |
| `organization.traits` | Required positive traits; filters, not mutations | `[]` |
| `role` | Local role ID or canonical function; absent means all | `null` |
| `as_of` | Integer year, −10000 to 10000, negative for BCE | `null` |
| `mode` | `historical`, `inspired` or `generic` | `historical` |
| `locale` | Presentation language tag | `fr` |
| `fallback_locale` | Explicit fallback language | `en` |
| `adaptations` | Explicit fictional transformations | `[]` |

Scales: `household`, `local`, `district`, `regional`, `polity`, `imperial`,
`transregional`. An army corps is a kind; regional reach is a scale.
The catalogue supplies valid combinations. Profiles already contain regional,
period and institutional context; a broad religion or continent remains ambiguous.
An absent year uses the profile interval with a diagnostic, never the machine date.

`historical` requires a researched cultural binding but still labels remaining
generic fields individually. It does not promise a complete historical reconstruction.
`inspired` uses available bindings and explicitly falls back to the generic model
when necessary. `generic` requires `culture: "*"`.

## Fictional adaptations

```json
{
  "culture": "vijayanagara_krishnadevaraya",
  "organization": {"kind": "hereditary_monarchy", "scale": "polity"},
  "mode": "inspired",
  "adaptations": [{"kind": "authoritarian", "target_role": "sovereign"}],
  "locale": "en"
}
```

The referenced Raya title remains sourced; the fictional concentration of power is
`adapted`. This makes no claim about Vijayanagara's actual historical regime.

- `authoritarian`: adds unilateral internal decision power and removes `checks`
  relations targeting the office. Advisory relations can remain.
- `elective_succession`: replaces selection/succession rules at blueprint and target
  office level with election. The electorate and eligibility remain unspecified.
- `hereditary_succession`: replaces them with dynastic selection without inventing
  primogeniture, a sex preference or a specific descent system.

Targets must be individual executive offices with at most one holder. Adaptations
are rejected in historical mode. Two succession transformations on the same office
conflict. More elaborate transformations belong in an authored knowledge pack.

## Response and evidence

Every response includes the normalized request, wire version, corpus version,
SHA-256 digest of the canonical dataset, status and localized diagnostics.

| Status | Meaning |
|---|---|
| `resolved` | Compatible blueprint available |
| `needs_context` | Choose among explicit cultural candidates |
| `unsupported` | Unknown kind/culture, date outside coverage or missing binding |
| `conflict` | Incompatible scale, traits, mode or adaptation |
| `role_not_found` | Blueprint available but requested office/function absent |

`blueprint` preserves the whole institutional graph; `selected_roles` identifies
matching offices. One function may match several offices. No global total ranking
is assumed. `culture` contains profile context, not all its other bindings.

Roles separate ID, function, title, optional rank, holder kind, cardinality, duties,
powers and rules. `person` can be vacant; `collective` is one body whose membership
can be represented by separate roles and `member_of` edges. Null maximum means no
specified cap. Bounds are not population targets.

Powers distinguish action, domain, scope, limits and basis: `de_jure`, `de_facto`,
`ritual`, `advisory`. Institutional authority does not imply legality under an
external state. Relations distinguish command, advice, appointment, removal,
election, representation, oversight and ritual legitimacy. Only `reports_to` is
required to be acyclic. Child units reference kinds without recursive expansion.

Rules contain category, method, parameters and bilingual descriptions. They are
**declarative**: v1 does not calculate heirs, votes, marriages or person eligibility.
Consumers must explicitly support each method they interpret; unknown methods
remain unsupported. No rule text or arbitrary script is executed. Runtime behavior
is limited to resolution, filters and the three documented adaptations.

Evidence is attached separately to titles, powers, rules and relations:
`generic_model`, `source_supported`, `adapted`. Sources include publisher, URL,
access date, locator, supported claims and limitations. Blueprint-level evidence
never overrides field-level evidence. Only used sources are expanded in the response.

## Languages

Authored label maps require `fr` and `en`, accepting additional language tags without
schema changes. Tags use a syntactic subset of BCP 47; the IANA registry is not checked.
Native spellings and their language are separate from translations. Translated
glosses do not establish rank or protocol equivalence between societies.

`display` projects titles and duties using exact locale, base language, explicit
fallback, its base language, then English. `translation_fallbacks` reports affected
paths. All original translations remain present. Grammatical forms are only
available when explicitly authored; no automatic translation or gender inference.

## Transport

HTTP accepts one JSON object, at most 32,768 bytes, with `application/json`.
Syntax/schema errors return 400, invalid size 413, unsupported media 415, foreign
Origin 403 and unknown routes 404. Semantic failures return 200 with explicit
status. The explorer is loopback-only, without production authentication or open CORS.
CLI input errors exit 2; inspect semantic status even when the process exits 0.

Identical requests against an identical KB digest resolve identically. Resolution
uses no randomness, machine clock, network service or sibling project.
