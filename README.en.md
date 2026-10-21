# Pecking Order

**Who holds the title? Who holds the power?** A standalone institutional knowledge
base for worldbuilders, with French, English and original-language titles.

[Français](README.md) · [Query contract](docs/contract.en.md) · [Coverage](docs/coverage.md)

Pecking Order supplies institutional blueprints for Lineage Lab populations and
Magna Urbis settlements. Namebench supplies names for office holders. These are
independent projects: integration uses JSON and stable identifiers.

![Local explorer in French](docs/images/demo.png)

The initial release contains **85 generic blueprints**, **12 bounded cultural
profiles**, **18 cultural bindings** and **12 sources**. This is a broad institutional
taxonomy and an initial historical reference corpus, not an exhaustive history of
every culture. Unsupported contexts remain explicit.

## Run

Python 3.12+. On Windows, double-click `demo.cmd`, then open
**http://127.0.0.1:8773**. Alternatively:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pecking_order studio
```

On Linux/macOS use `.venv/bin/python`. The loopback-only explorer needs no LLM,
account, API key, external database or sibling repository. Switch FR/EN, inspect
offices, powers and sources, and import/export JSON requests and results.

## Query

```python
from pecking_order import KnowledgeBase

result = KnowledgeBase().resolve({
    "culture": "tswana",
    "organization": {"kind": "village_council", "scale": "local"},
    "role": "executive",
    "locale": "en",
})
print(result.display["head.title"])  # Kgosi (chief)
```

```powershell
pecking-order resolve examples/tswana-village.json
pecking-order catalog
pecking-order validate
```

HTTP: `GET /api/catalog`, `GET /api/sources`, `POST /api/resolve`.
[JSON Schema](schemas/) and [OpenAPI](schemas/openapi.json) describe the same contract.

An office, its cultural title, a rank and a person are different things. Structures
can contain collective bodies and multiple sources of authority. A sourced title
does not turn an authored power into a historical claim: evidence is attached to
individual titles, powers, relations and rules.

`historical` requires a researched binding; `inspired` permits an explicit
worldbuilding adaptation; `generic` requires `culture: "*"`. Broad contexts such as
“Hindu” or “African” return `needs_context`, never a supposedly universal title.
Only institutional kinship is included: joint estates, corporate lineages, noble
houses, clans, dynasties and inter-house alliances. Trivial parent/child structures
are outside scope.

[Authoritarian Raya example](examples/authoritarian-raya.json): explicitly turn a
fictional office into an authoritarian executive while keeping the referenced title.
This is rejected in historical mode and labelled as an adaptation.

## Validate

```powershell
python -m pytest
ruff check src tests tools
python -m pecking_order validate
python -m build
```

Optional browser checks: install `.[browser]`, start the studio, then run
`python tools/check_browser.py`. `STUDIO_BROWSER` selects a Chromium executable;
`PECKING_ORDER_URL` selects another local URL. Screenshots go to ignored `output/`.

The packaged [catalogue](src/pecking_order/data/catalog.json) is generated from
[the authored source](tools/build_catalog.py). Use `KnowledgeBase(path)` or
`pecking-order --data catalog.json …` for a complete custom knowledge pack.
See [provenance](PROVENANCE.md), [design](docs/design.fr.md),
[authoring](docs/authoring.fr.md) and [integration](docs/integration.fr.md).
