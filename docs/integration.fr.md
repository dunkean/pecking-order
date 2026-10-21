# Intégration avec les générateurs

## Échanges

Pecking Order possède les identifiants des modèles et des charges ; le monde
consommateur possède les identifiants de ses organisations, lieux et personnes.
Ne pas faire porter à un titre traduit un rôle de clé étrangère.

```json
{
  "organization_id": "world:organization:42",
  "place_id": "world:settlement:7",
  "institution_reference": {
    "kb_version": "0.1.0",
    "kb_digest": "sha256-from-resolution",
    "culture": "tswana_bogosi_contemporary",
    "kind": "village_council"
  },
  "office_holders": [
    {"role_id": "head", "person_ids": ["world:person:123"], "from_year": 2026},
    {"role_id": "assembly", "collective_id": "world:body:18", "from_year": 2026}
  ]
}
```

Cet objet illustre un **adaptateur du monde**, pas un nouvel endpoint ni une
réponse du résolveur. L’historique des occupations, les dates, les raisons d’entrée
ou de sortie et les membres des collèges appartiennent au consommateur.

## Lineage Lab

1. Résoudre le contexte institutionnel du monde ou du groupe.
2. Conserver la requête, la réponse ou son archive et le condensat de la base.
3. Ouvrir les charges ; traiter les minima et maxima comme contraintes d’occupation,
   sans les interpréter comme des distributions statistiques.
4. Interpréter seulement les méthodes de recrutement connues de l’adaptateur.
   Si une règle reste narrative ou inconnue, demander une règle de scénario ou
   conserver la charge vacante et signaler le manque.
5. Affecter des personnes existantes et tracer l’occupation dans le temps.

Une personne peut cumuler plusieurs charges si les règles du scénario le permettent.
Le modèle n’impose pas de personne différente par charge. Un conseil est un organe
collectif dont les personnes membres restent explicites. Les liens père/enfant,
l’âge, les décès et les héritiers calculés restent dans Lineage Lab.

Les règles de ménage ordinaires ne sont pas remplacées. Les familles institutionnelles
ajoutent seulement un objet maison/lignage/patrimoine et ses charges particulières.

## Magna Urbis

Le territoire et le peuplement déterminent quels groupes sont plausibles :
administration, communauté d’irrigation, guilde, temple, tribunal, milice, marché,
maison notable. Pecking Order ne déduit pas leur existence à partir d’une carte.
L’intégrateur choisit le type, l’échelle et le contexte, puis place l’organisation
et affiche ses titres selon la langue du lecteur.

Les sous-unités sont des références de types. Elles ne déclenchent pas d’expansion
automatique infinie : un budget de profondeur et d’effectifs doit appartenir au
générateur du monde. Une administration impériale peut contenir des provinces,
mais ne crée pas automatiquement des milliers de postes.

Pour un client Rust/WASM, utiliser les schémas pour générer des types ou écrire un
adaptateur JSON. Le serveur local est une option de développement, pas une
dépendance du moteur. Une intégration binaire directe Rust n’est pas livrée ici.

## Namebench et TTRPG generator

Le nom d’un titulaire reste un nom de personne. Le titre reste une référence à la
charge. Conserver les deux séparément permet de changer de langue sans renommer
la personne et de conserver une titulature historique lors d’un changement de charge.

Le générateur TTRPG peut utiliser la structure et les sources comme contraintes
d’écriture : le LLM rédige les biographies et conflits, mais n’a pas à redéfinir
arbitrairement les compétences des charges. Une proposition du LLM hors catalogue
doit être présentée comme adaptation et validée avant intégration.

## Rejeu et mises à jour

Conserver le JSON de requête normalisé et le `kb_digest`. Une version nouvelle du
corpus peut changer une traduction ou corriger une structure tout en conservant
le contrat 1.0. Pour un monde déjà publié, archiver la réponse résolue ou le pack
exact. Ne pas rafraîchir silencieusement une ancienne institution vers une nouvelle
interprétation historique.
