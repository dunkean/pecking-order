# Pecking Order

**Un système. Une culture. Tous les rôles.**

Moteur **Rust** de contenu institutionnel pour les générateurs de mondes : choisir
un royaume, une nation, une ville, une guilde, une famille organisée, une religion
ou une cellule secrète, puis appliquer un thème culturel et récupérer les titres,
fonctions, responsabilités, niveaux d’autorité et importance de chaque rôle.

[English](README.en.md) · [Contrat d’API](docs/API.fr.md) · [Catalogue](docs/CATALOG.md) · [Révision de cohérence](docs/COHERENCE.fr.md)

![Explorateur des titres et rôles](docs/images/demo.png)

**242 systèmes**, **67 thèmes**, **1 731 rôles définis**, **6 124 entrées de titres
FR/EN**. Les **41 cultures de Magna Urbis** sont toutes reprises avec leurs
identifiants. Le catalogue ne se limite pas aux exemples de l’interface : tous les
systèmes sont combinables avec tous les thèmes.

## Lancer

Rust 1.88 ou ultérieur. Sous Windows : double-cliquer sur **`demo.cmd`**.

```powershell
cargo run --release -- studio
```

Ouvrir **http://127.0.0.1:8773**. Le premier lancement compile le programme.
L’exécutable embarque le moteur, les données et l’interface : après compilation,
`target/release/pecking-order.exe` fonctionne seul. Pas de Python, de LLM, de clé
d’API ou de dépôt voisin nécessaire à l’exécution.

Dans l’interface : **système → taille / structure / pouvoir → culture**. Les filtres
par titre, niveau et importance permettent d’explorer le résultat. Le lexique
culturel montre également toutes les entrées d’un thème, indépendamment du système.
Titres français, anglais et formes locales restent consultables côte à côte.

Le **[glossaire complet](http://127.0.0.1:8773/glossary)** expose les **4 959 termes
distincts**, variantes comprises, sans choisir d’abord un système. Recherche,
index A–Z, filtres par culture et fonction, responsabilités et liens vers toutes
les organisations concernées ; choisir **Tout afficher** pour parcourir la liste
entière. Il comprend aussi les 609 types de rôles, les 242 organisations et les
316 pouvoirs. Export de la sélection en CSV et du glossaire complet en JSON.

## Requête minimale

```json
{"system":"kingdom","theme":"russian-kremlin"}
```

```json
{
  "system": "nation",
  "theme": "russian-kremlin",
  "authority": "aristocratic",
  "locale": "fr"
}
```

Exemples directs :

| Système | Thème | Titres dans le résultat |
|---|---|---|
| Nation aristocratique | Europe de l’Est | Tsar, Kniaz, Boiar, Voïvode, Namestnik… |
| Même système | Europe de l’Ouest | King / roi, Duke / duc, Count / comte, Baron / baron… |
| Village | Tswana | Kgosi, Mothusa kgosi, Kgotla, anciens… |
| Famille indivise | Inde | Kulapati, Karta, responsables de branches et du patrimoine… |
| Guilde artisanale | Naine | Maître des forges, maîtres, compagnons, apprentis… |
| Cellule cultuelle, 4 membres | Drow ou culte chthonien | Responsable, officiant, gardien et adepte avec leurs fonctions propres |

```powershell
cargo run -- resolve examples/nation-east.json
cargo run -- resolve examples/secret-cell.json
cargo run -- lexicon chinese
cargo run -- catalog
cargo run -- glossary
```

HTTP : **`POST /api/resolve`**, `GET /api/catalog`, `GET /api/themes/{id}` et
`GET /api/schema/query`. Les requêtes et résultats s’exportent aussi depuis l’interface.

## Ce que renvoie un rôle

```json
{
  "id": "sovereign",
  "function": "aristocratic_sovereignty",
  "title_key": "king",
  "title": {"fr":"Tsar","en":"Tsar","native":"царь","variants":[]},
  "level": 0,
  "importance": 100,
  "scope": "realm",
  "reports_to": [],
  "duties": {"fr":"Édicte lois et chartes, nomme les grands officiers…","en":"Issues law and charters, appoints senior officers…"}
}
```

Le niveau **0** est le sommet de l’organisation ; un niveau croissant descend dans
ses échelons. L’importance **0–100** exprime le poids du rôle dans ce système,
indépendamment de sa position : un oracle ou un trésorier peut être très important
sans commander les autres. Un conseil peut être un organe collectif.

La structure fonctionnelle est séparée du lexique. Changer de culture change les
titulatures, sans mélanger les identifiants des fonctions. Les thèmes sont du lore
librement composable : pas de blocage pour combiner un système et une culture.

## Contenu

- Gouvernements, empires, monarchies, républiques, fédérations, nations et échelons locaux.
- Religions, temples, clergés, monastères, ordres, oracles, confréries, rites et cultes secrets.
- Guildes, ateliers, métiers, compagnies, coopératives, marchés, banques et caravanes.
- Armées et échelons du groupe d’armées à l’escouade, marines, équipages et services secrets.
- Maisons nobles, familles à patrimoine commun, lignages, clans et dynasties.
- Justice, enseignement, services publics, associations, spectacles et organisations criminelles.
- Cours et collèges fantastiques, sociétés magiques, colonies et groupes non humains.

Les cultures comprennent tous les thèmes de Magna Urbis ainsi que des variantes
supplémentaires : tswana, asante, oromo, sumérien, égyptien, hellénique, polynésien,
démocratique moderne, cultes animiste, solaire, ancestral, chthonien, astral, etc.
La [liste complète](docs/CATALOG.md) est générée depuis les données réellement embarquées.

## Intégrer et enrichir

```rust
use pecking_order::{Engine, Query};

let engine = Engine::embedded()?;
let query: Query = serde_json::from_str(
    r#"{"system":"craft_guild","theme":"dwarven"}"#
)?;
let organization = engine.resolve(query)?;
```

Le cœur Rust ne dépend ni de l’interface ni du serveur HTTP. Il compile également
pour `wasm32-unknown-unknown`. Les systèmes sont définis dans `data/systems*.json`,
les thèmes dans `data/themes*.json`. Une entrée nouvelle n’exige pas de modifier
le moteur. Les données sont embarquées à la compilation ; le catalogue externe
peut aussi être chargé via `Engine::from_json`.

Namebench peut nommer les titulaires ; Lineage Lab peut les affecter aux charges ;
Magna Urbis peut placer les organisations. Ces intégrations n’imposent aucune
dépendance entre dépôts. Voir [le contrat et les règles de composition](docs/API.fr.md).

```powershell
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
cargo run -- validate
cargo check --lib --target wasm32-unknown-unknown
```

La validation résout les **16 214 combinaisons système × thème**, pas seulement un
jeu d’exemples. Tests navigateur facultatifs : `npm ci`, démarrer le studio, puis
`npm run test:browser` et `npm run test:glossary`. `STUDIO_BROWSER` choisit le binaire Chromium/Edge.

Cette version remplace le prototype Python initial. Le contrat actuel est **API 2.0**.
