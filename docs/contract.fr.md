# Contrat de requête 1.0

Le même objet sert à Python, à la CLI et à `POST /api/resolve`. Les modèles
[Pydantic](../src/pecking_order/models.py) génèrent les schémas ; les champs inconnus
et les conversions implicites sont refusés. La requête n’est pas du langage naturel.
Un assistant peut traduire une phrase vers ce contrat, mais le résolveur reste
déterministe et autonome.

## Requête minimale

```json
{
  "culture": "tswana_bogosi_contemporary",
  "organization": {"kind": "village_council", "scale": "local"}
}
```

| Champ | Sens | Défaut |
|---|---|---|
| `schema_version` | Version du contrat, exactement `1.0` | `1.0` |
| `culture` | ID de profil contextualisé, alias reconnu, ou `*` en mode générique | obligatoire |
| `organization.kind` | Type institutionnel stable du catalogue | obligatoire |
| `organization.scale` | Portée institutionnelle, indépendante des effectifs | obligatoire |
| `organization.traits` | Exigences positives vérifiées sur le modèle résultant ; ce ne sont pas des modifications | `[]` |
| `role` | ID d’une charge ou fonction canonique ; absent = toutes les charges | `null` |
| `as_of` | Année entière, de −10000 à 10000 ; années avant notre ère négatives | `null` |
| `mode` | `historical`, `inspired`, `generic` | `historical` |
| `locale` | Langue de présentation, clé BCP 47 | `fr` |
| `fallback_locale` | Langue de repli explicite | `en` |
| `adaptations` | Modifications fictives explicites, hors mode historique | `[]` |

Échelles : `household`, `local`, `district`, `regional`, `polity`, `imperial`,
`transregional`. « Corps d’armée » est un **type**, « régional » une **portée**.
« Nation » désigne ici une organisation politique, sans présumer une équivalence
entre peuple, territoire et État.

Une culture est un profil documenté qui porte déjà sa région, sa période et son
contexte institutionnel. Les qualificatifs « hindou », « indien », « africain »,
« chrétien » ou « japonais » restent volontairement trop larges. Le catalogue renvoie
des candidats ; choisir l’ID explicite permet de continuer. L’année filtre les
profils mais n’efface pas une ambiguïté culturelle volontaire.

`as_of` absent utilise l’intervalle du profil, avec diagnostic. Il n’existe pas
d’année « actuelle » implicite. Une source consultée en 2026 ne prouve pas qu’une
institution est restée identique pendant toute sa période de référence.

## Modes et adaptations

| Mode | Comportement |
|---|---|
| `historical` | Exige une déclinaison pour ce couple profil/type. Les champs génériques restants sont étiquetés individuellement. Ce n’est pas une garantie de reconstruction historique complète. |
| `inspired` | Utilise la déclinaison disponible ; si elle manque, conserve explicitement la structure générique. Le résultat est une adaptation. |
| `generic` | Demande `culture: "*"`. N’utilise aucune déclinaison culturelle. |

Exemple pour « une monarchie autoritaire d’inspiration hindoue », après sélection
du contexte de Vijayanagara :

```json
{
  "culture": "vijayanagara_krishnadevaraya",
  "organization": {
    "kind": "hereditary_monarchy",
    "scale": "polity",
    "traits": ["authoritarian"]
  },
  "role": "sovereign",
  "mode": "inspired",
  "adaptations": [{"kind": "authoritarian", "target_role": "sovereign"}],
  "locale": "fr"
}
```

Le titre **Raya** garde sa référence ; la concentration des décisions est marquée
`adapted`. Le moteur ne prétend pas avoir établi le régime historique de
Vijayanagara à partir du seul titre.

Trois adaptations v1 sont exécutées :

- `authoritarian` ajoute un pouvoir de décision interne unilatérale et retire les
  relations génériques `checks` visant la charge. Les avis consultatifs peuvent rester.
- `elective_succession` remplace les règles de sélection/succession du modèle et
  de la charge visée par une élection dont corps électoral et critères restent à définir.
- `hereditary_succession` fait de même avec une sélection dynastique, sans inventer
  une primogéniture, une préférence masculine ou une filiation particulière.

La cible doit être une charge exécutive individuelle avec au plus un titulaire.
Une assemblée ne devient pas un dictateur par une modification implicite. Deux
adaptations de succession sur la même charge sont incompatibles. Les transformations
plus riches se définissent dans un profil éditorial, pas dans une requête arbitraire.

## Réponse

La réponse contient toujours `request`, `schema_version`, `kb_version`, `kb_digest`,
`status`, les diagnostics et leurs champs concernés. Le condensat SHA-256 porte sur
le JSON canonique de la base, indépendamment de sa mise en forme.

| Statut | Signification |
|---|---|
| `resolved` | Structure compatible disponible |
| `needs_context` | Contexte trop large ; `candidates` contient des choix documentés |
| `unsupported` | Type, culture, période ou déclinaison absents |
| `conflict` | Échelle, caractéristiques, mode ou adaptations incompatibles |
| `role_not_found` | Structure disponible, mais charge/fonction demandée absente |

En cas de résolution, `culture` décrit le profil choisi, `blueprint` contient le
graphe institutionnel complet et `selected_roles` les charges correspondant au filtre.
Une fonction peut correspondre à plusieurs charges. Aucun classement total de ces
charges n’est supposé. La réponse ne contient pas toutes les autres déclinaisons
du profil, pour limiter son volume.

Chaque charge porte :

- un ID local stable et une `function` canonique ;
- un titre bilingue, une éventuelle forme d’origine et sa langue, les formes
  grammaticales disponibles et le type de traduction ;
- un `rank` facultatif, séparé de la fonction ;
- un type de titulaire `person` ou `collective`, avec bornes de cardinalité ;
- ses missions, pouvoirs, règles et la provenance du titre.

`min_holders: 0` permet une vacance ; ce n’est pas un objectif démographique.
`max_holders: null` signifie qu’aucun maximum n’est fixé. Une charge `collective`
représente l’organe ; sa composition se décrit par d’autres charges et des relations
`member_of`, pas par une confusion entre nombre de conseils et nombre de conseillers.

Les pouvoirs distinguent domaine, action, portée, limites et fondement : `de_jure`,
`de_facto`, `ritual`, `advisory`. `de_jure` désigne l’autorité reconnue dans le modèle,
sans affirmer sa légalité dans un État extérieur. Le graphe distingue commandement,
conseil, nomination, révocation, représentation, contrôle et légitimation rituelle.
Seules les relations `reports_to` doivent être acycliques ; les contrôles réciproques
sont licites. Les unités associées référencent d’autres types sans expansion récursive.

Les règles ont une catégorie, une méthode, des paramètres JSON bornés et un texte
bilingue. Elles sont **déclaratives** : la v1 ne calcule pas les héritiers, les votes,
les mariages ni la conformité d’un candidat. Aucun texte de règle n’est exécuté.
Le consommateur interprète uniquement les méthodes qu’il prend en charge et doit
refuser ou signaler les autres. La v1 exécute la sélection des modèles, les filtres
et les trois adaptations documentées, pas un simulateur social général.

## Langues et preuves

Les objets `labels` contiennent au minimum `fr` et `en`. Ajouter `de`, `ar`, `ja` ou
`fr-CA` ne change pas le contrat. Les clés sont validées selon un sous-ensemble
syntaxique de BCP 47 ; aucune validation contre le registre IANA n’est effectuée.
Les titres d’origine restent séparés de leur traduction. Un équivalent de fonction
n’est pas nécessairement une équivalence historique ou protocolaire.

`display` fournit les intitulés et missions selon `locale`. Repli : langue exacte,
langue de base, `fallback_locale`, sa langue de base, puis `en`. Les chemins utilisant
un repli sont listés dans `translation_fallbacks`. La réponse conserve toujours
les traductions complètes ; elle ne fait aucune traduction automatique. Les formes
féminines, plurielles ou d’adresse ne sont utilisées que si elles sont renseignées.

Chaque affirmation porte `generic_model`, `source_supported` ou `adapted`. Les
références de sources sont locales à la base. `sources` développe uniquement les
références utilisées, avec URL, éditeur, date de consultation, emplacement, portée
et limites. Le statut du modèle global ne remplace jamais ceux des champs.

## Transport et limites

HTTP accepte un objet JSON de **32 768 octets maximum**, un `Content-Type:
application/json`, sans CORS ouvert. Les erreurs de syntaxe ou de schéma donnent
HTTP 400 ; taille invalide 413 ; type de contenu 415 ; origine étrangère 403 ;
route inconnue 404. Les échecs sémantiques donnent HTTP 200 et un `status` explicite.
Il n’y a pas d’authentification de production : le studio écoute uniquement sur
`127.0.0.1`. La CLI écrit le même résultat JSON ; une entrée invalide sort avec le
code 2. Un statut sémantique doit être inspecté même si la commande sort avec 0.

Le même contrat, la même base et la même requête donnent le même résultat. Aucun
hasard, aucune date machine ni aucun appel réseau n’intervient dans la résolution.
`schema_version` versionne le fil, `kb_version` le corpus, `kb_digest` son contenu.
