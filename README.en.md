# Pecking Order

**One system. One culture. Every role.** A Rust content engine for organizational
titles, offices, authority levels, importance, responsibilities and relationships.

[Français](README.md) · [API contract](docs/API.en.md) · [Full catalogue](docs/CATALOG.md)

![Titles and roles explorer](docs/images/demo.png)

**242 systems · 67 themes · 1,731 defined roles · 6,124 bilingual title entries.**
All 41 Magna Urbis culture IDs are supported. Every system combines with every
theme, from an empire to a four-person secret cult cell.

## Run

Rust 1.88+. On Windows double-click `demo.cmd`, or run:

```sh
cargo run --release -- studio
```

Open **http://127.0.0.1:8773**. The compiled executable embeds the engine, content
and UI. It runs independently of Python, a model service, API keys or sibling projects.

Choose **system → size / structure / authority → culture**. Explore all matching
offices or filter by title, level and importance. Switch FR/EN, browse whole cultural
lexicons and import/export JSON requests and responses.

The **[complete glossary](http://127.0.0.1:8773/glossary)** exposes all **4,959 distinct
terms**, including variants, without selecting an organization first. Search FR/EN
and original forms, browse A–Z, filter by culture or role, inspect responsibilities
and open every relevant organization. Select **Show all** to display the entire
list. Separate sections cover 609 role types, 242 organizations and 316 powers.
Export the filtered selection as CSV or download the complete glossary as JSON.
Available through `GET /api/glossary`, `cargo run -- glossary` and `Engine::glossary()`.

```json
{"system":"kingdom","theme":"russian-kremlin"}
```

```json
{"system":"cult_cell","theme":"drow-enclave","members":4,"structure":"cellular"}
```

An Eastern European aristocratic nation uses Tsar, Kniaz, Boiar and Voivode titles;
the same system with a Western European theme uses King, Duke, Count and Baron.
A Tswana village includes Kgosi and Kgotla; an Indian corporate joint family includes
Kulapati and Karta. Themes are freely composable worldbuilding lore.

## Contract

`POST /api/resolve`, `GET /api/catalog`, `GET /api/themes/{id}`, `GET /api/schema/query`.
CLI: `cargo run -- resolve examples/nation-east.json`, `lexicon chinese`, `catalog`.

Each role separates stable ID, semantic function, cultural title, level, importance,
scope, reporting relationships, duties, powers, access to office and optional status.
Titles preserve French, English, original forms and authored variants. Level 0 is
the top tier. Importance 0–100 measures weight inside that system, not a universal
comparison between organizations. Collective bodies are supported.

The Rust library exposes `Engine::embedded()`, `Engine::from_json()` and
`Engine::resolve(Query)`. The core also compiles to `wasm32-unknown-unknown`; the local
HTTP explorer is native. Content lives in `data/systems*.json` and `data/themes*.json`.
No historical-source selection mode or culture-ambiguity gate.

## Check

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
cargo run -- validate
cargo check --lib --target wasm32-unknown-unknown
```

Validation resolves all **16,214 system/theme combinations**. Optional browser checks:
`npm ci`, start the studio, `npm run test:browser`. `STUDIO_BROWSER` selects Chromium/Edge.

This release replaces the original Python prototype with **API 2.0**. Namebench,
Lineage Lab and Magna Urbis can consume stable office IDs and JSON without a
runtime dependency on each other.
