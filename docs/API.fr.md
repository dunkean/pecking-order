# API 2.0 — systèmes, rôles et titres

## Entrée

Le système décrit **ce qu’est l’organisation**. Le thème fournit **le vocabulaire
des titres**. Les filtres facultatifs décrivent sa taille et la répartition du pouvoir.
Le moteur renvoie tous les rôles correspondants ; aucun rôle précis n’est requis
dans la question.

```json
{
  "system": "nation",
  "theme": "russian-kremlin",
  "authority": "aristocratic",
  "structure": "hierarchical",
  "locale": "fr"
}
```

| Champ | Sens | Défaut |
|---|---|---|
| `system` | ID ou alias du système, p. ex. `kingdom`, `empire`, `nation`, `village`, `craft_guild`, `joint_family`, `cult_cell` | obligatoire |
| `theme` | ID ou alias culturel, y compris les 41 IDs de Magna Urbis | `generic` |
| `size` | Complexité de l’organisation : `tiny`, `small`, `medium`, `large`, `vast`, `full` | `full` |
| `members` | Effectif positif du groupe ; détermine la complexité à la place de `size` | absent |
| `structure` | `hierarchical`, `horizontal`, `network`, `cellular` | valeur du système |
| `authority` | `hereditary`, `aristocratic`, `authoritarian`, `democratic`, `theocratic`, `military`, `bureaucratic`, `meritocratic`, `consensual`, `personal` | valeur du système |
| `locale` | Langue de présentation : FR et EN disponibles ; autres clés extensibles | `fr` |
| `filter` | Sélection facultative des rôles | aucun |
| `api_version` | Version du contrat | `2.0` |

L’effectif sélectionne une complexité : 1–5 `tiny`, 6–30 `small`, 31–300 `medium`,
301–10 000 `large`, au-delà `vast`. Il ne génère pas de personnes et ne promet
pas une personne différente par fonction. Un groupe de quatre personnes peut
cumuler plusieurs charges ; le système spécialisé `cult_cell` expose précisément
quatre fonctions de base. `full` retourne tous les échelons disponibles.

Le type et la taille sont indépendants : un petit royaume reste un royaume.
Réduire la complexité conserve ses offices de base, puis écarte les spécialisations
et échelons secondaires. Aucune conversion implicite en village.

```json
{
  "system":"empire",
  "theme":"chinese",
  "filter":{
    "max_level":3,
    "min_importance":70,
    "functions":["sovereignty","government"],
    "scopes":["realm","province"]
  }
}
```

`filter.text` recherche également dans les titres FR/EN, la forme locale, l’ID et
la fonction. Les critères d’un filtre se cumulent avec **ET** ; les valeurs d’une
même liste sont alternatives. Les identifiants de fonctions et de portées se lisent
dans les données/résultats, sans être traduits.

Les alias français/anglais et les IDs sont normalisés pour la casse, les accents,
les espaces, tirets et underscores. Un ID canonique a priorité sur un alias.

## Sortie

```json
{
  "api_version":"2.0",
  "content_version":"0.2.0",
  "system":{"id":"aristocratic_nation","label":{"fr":"Nation aristocratique","en":"Aristocratic nation"}},
  "theme":{"id":"eastern-europe","label":{"fr":"Principautés de la Rus’","en":"Rus principalities"}},
  "size":"full",
  "structure":"hierarchical",
  "authority":"aristocratic",
  "roles":[
    {
      "id":"sovereign",
      "function":"aristocratic_sovereignty",
      "title_key":"king",
      "title":{"fr":"Tsar","en":"Tsar","native":"царь","variants":[]},
      "display_title":"Tsar",
      "level":0,
      "importance":100,
      "scope":"realm",
      "reports_to":[],
      "duties":{"fr":"Édicte lois et chartes, nomme les grands officiers…","en":"Issues law and charters, appoints senior officers…"},
      "powers":[{"id":"appoint","label":{"fr":"nommer","en":"appoint"}}],
      "collective":false,
      "optional":false,
      "selection":{"fr":"Choix parmi les maisons, familles ou ordres privilégiés.","en":"Selection among privileged houses, families or estates."},
      "title_theme":"eastern-europe"
    }
  ]
}
```

Extrait abrégé : la vraie réponse inclut aussi la requête normalisée, la description,
le nombre de rôles disponibles avant filtre, les systèmes associés et les notes.

### Les concepts qui restent stables

**`id`** identifie une charge à l’intérieur d’un système. **`function`** décrit son
travail sémantique. **`title_key`** sélectionne son vocabulaire. **`title`** est la
réalisation culturelle bilingue de cette fonction. Aucune personne ni aucun nom
propre ne se trouve dans ces objets.

**`level`** mesure l’échelon local : 0 au sommet, valeurs croissantes vers les
échelons subordonnés. Plusieurs organes peuvent partager un niveau. En structure
horizontale, tous les rôles ont le niveau 0 et aucune subordination de commandement.

**`importance`** va de 0 à 100 et mesure le poids institutionnel du rôle, pas son
rang mécanique ni sa proportion dans la population. Un gardien de rites peut
être indispensable sans être le supérieur du commandant. Cette mesure est locale
au système ; elle ne classe pas un maire au-dessus d’un empereur.

**`scope`** indique le champ fonctionnel, par exemple royaume, province, ville,
village, maison, unité, cellule ou réseau. **`reports_to`** contient des IDs locaux
de rôles présents dans la réponse. Lors d’un filtrage, le moteur remonte au parent
conservé le plus proche, pour ne pas laisser de référence orpheline.

**`collective`** distingue une assemblée d’une charge individuelle.
**`optional`** signale une spécialisation ou une variante institutionnelle ; ce
marqueur ne génère pas aléatoirement un titulaire. `duties`, `powers` et `selection`
expliquent la fonction. La sélection reste du contenu déclaratif : le moteur ne
calcule pas les héritiers ni les candidats de Lineage Lab.

## Composition

1. Charger le système générique et toutes ses charges.
2. Appliquer l’exercice du pouvoir explicitement demandé. Pour un chef d’État,
   les variantes aristocratique/héréditaire, démocratique, théocratique ou militaire
   changent la clé lexicale correspondante. Les sélections de titulaires suivent
   le mode choisi et la nature du rôle. Le mode autoritaire ajoute le décret et
   concentre le sommet de la chaîne hiérarchique.
3. Appliquer la structure. Le mode horizontal retire le commandement et met les
   fonctions au même niveau ; le réseau retire les subordinations globales ; une
   cellule peut conserver son organisation interne. Le simple défaut horizontal
   d’une maison n’efface pas son titre traditionnel de chef de maison.
4. Sélectionner la complexité puis les filtres de rôles.
5. Choisir les titres dans le lexique culturel : clé du thème, parent éventuel,
   puis lexique générique ; une charge spécialisée peut aussi fournir un titre
   fonctionnel propre si sa clé n’est pas lexicalisée.
6. Réparer les références de parenté hiérarchique après filtre et trier par niveau,
   importance décroissante puis ID.

`title_theme` indique le lexique ayant fourni le titre : thème demandé, parent,
`generic` ou `functional`. Ce n’est pas un statut de preuve et cela ne bloque
jamais une combinaison culturelle.

Les thèmes sont des interprétations de worldbuilding, avec des emprunts et des
extrapolations assumées. Un thème occidental peut donc habiller une guilde naine,
et un thème chinois un système républicain. Le contrat sépare ce choix créatif
des fonctions stables ; il ne s’agit pas d’un moteur d’authentification historique.

## Langues

Les titres ont obligatoirement `fr` et `en`, et éventuellement `native` ainsi que
`variants` pour une autre forme, un féminin, un masculin ou une alternative.
Les objets linguistiques acceptent d’autres clés sans changer les IDs.
`locale` choisit `display_title` et `display_duties` : langue demandée, langue de
base, puis anglais. Aucune traduction automatique n’est exécutée.

Le même titre peut apparaître pour plusieurs charges aux compétences différentes :
le titre ne remplace donc jamais l’ID ou la fonction dans les échanges entre moteurs.

## Transports et intégration

Le glossaire global est disponible dans `/glossary`, via `GET /api/glossary`,
`pecking-order glossary` ou `Engine::glossary()`. La réponse contient `terms`
(libellés `fr`, `en`, `native` et tous leurs `bindings` culture/clé/forme),
`functions` (clé lexicale, libellé et tous les `uses` dans les organisations),
`systems`, `themes`, `powers` et `counts`. Chaque emploi conserve l’ID du système
et du rôle, la fonction, les responsabilités, le niveau, l’importance et les
pouvoirs. Les variantes sont des termes consultables ; `parent` indique leur
titre principal. Les titres identiques sont regroupés par triplet FR/EN/forme
locale, sans supprimer leurs contextes. La réponse livre tout le catalogue
effectif, y compris les titres fonctionnels, sans pagination côté API.

- Rust : `Engine::embedded()?.resolve(query)` ; conserver une instance pour les requêtes en série.
- JSON pur : `pecking_order::resolve_json(request)`.
- CLI : `pecking-order resolve request.json`, ou `resolve -` via l’entrée standard.
- HTTP : `POST /api/resolve`, corps JSON, 65 536 octets maximum ; les choix et le schéma sont disponibles dans `/api/catalog` et `/api/schema/query`.
- Données : `Engine::from_json` accepte un pack complet (`systems`, `themes`, `city_cultures`, `powers`). Les fichiers `data/` sont les sources éditoriales embarquées à la compilation.

Les réponses correctes donnent HTTP 200. Un choix ou un JSON invalide donne 400,
une origine étrangère 403, un corps trop grand 413, un type autre que JSON 415,
une route inconnue 404. Les erreurs de sélection contiennent `code`, `field`,
un `message` bilingue et d’éventuelles `suggestions`. Les erreurs de transport
peuvent se limiter à `code`.

Le studio écoute seulement sur `127.0.0.1`. Le moteur ne fait aucun appel réseau,
ne dépend d’aucun service et n’utilise ni hasard ni date courante. Pour rejouer un
monde, conserver sa requête et sa version de contenu, ou archiver sa réponse.

Lineage Lab reste propriétaire des personnes et occupations des charges. Namebench
reste propriétaire des noms. Magna Urbis reste propriétaire des lieux et effectifs.
Pecking Order fournit les rôles à remplir et les titres à afficher.
