# Enrichir la base

## Procédure éditoriale

1. Chercher une fonction et un modèle déjà disponibles avant d’en créer un nouveau.
2. Délimiter le contexte : lieu, intervalle, institution, communauté et niveau.
3. Consulter des sources primaires, institutionnelles ou des travaux scientifiques
   précis. Une page qui atteste un titre ne suffit pas à attester tous ses pouvoirs.
4. Ajouter la source avec URL, éditeur, emplacement, affirmations étayées et limites.
5. Écrire les titres, descriptions, règles et limites en français et en anglais.
6. Créer la déclinaison : remplacer une charge entière ou ajouter/retirer explicitement
   des charges. Déclarer les exceptions et les relations modifiées.
7. Attacher une preuve à chaque titre, pouvoir, relation et règle ; garder le
   générique comme générique lorsqu’il n’est pas documenté.
8. Régénérer, valider, tester les cas compatibles et incompatibles, puis examiner
   le résultat dans l’explorateur.

Le source éditorial v1 est `tools/build_catalog.py`. Les helpers composent des
fonctions génériques ; le JSON matérialisé ne dépend pas de ces helpers à l’exécution.
Une nouvelle source n’exige aucune modification du résolveur.

```powershell
python tools/build_catalog.py
python tools/export_schemas.py
python -m pecking_order validate
python -m pytest
```

Un pack alternatif doit être un `Dataset` complet : `version`, `templates`,
`cultures`, `sources`, `broad_aliases`. Charger avec `KnowledgeBase(path)` ou
`pecking-order --data path/catalog.json studio`. La v1 ne charge pas de plugins
Python ni de scripts embarqués et n’assemble pas implicitement plusieurs packs.

## Déclinaisons

`Binding.roles` remplace les charges de même ID et ajoute les autres. Ce sont des
objets complets, sans fusion récursive de champs. `remove_roles` retire explicitement
des charges existantes. Les relations génériques touchant une charge retirée sont
supprimées. `replace_relations: true` remplace tout le graphe de relations ; sinon
les relations supplémentaires sont ajoutées. Les règles du binding s’ajoutent aux
règles du modèle : pour remplacer un système contradictoire, choisir un modèle
générique adapté ou créer une variante au lieu d’empiler des textes incompatibles.

Les ID des charges sont locaux au modèle ; `function` est l’identifiant réutilisable
pour la requête. Les appellations culturelles vont dans `title`, jamais dans l’ID.
Les fonctions génériques du catalogue restent consultables dans le JSON. Si une
fonction manque, l’ajouter au modèle et documenter sa sémantique.

Le schéma autorise les catégories de règles sélection, succession, mandat,
révocation, éligibilité, appartenance, héritage, résidence, mariage, décision,
incompatibilité et vacance. Les méthodes sont des ID stables, interprétés uniquement
par les consommateurs qui les connaissent. Les paramètres acceptent chaînes,
entiers, booléens et listes de chaînes ; ni code ni prédicat exécutable.

## Multilingue

Tous les textes d’usage ont `labels.fr` et `labels.en`. Ajouter d’autres clés ne
modifie pas les identifiants. `title.native` et `title.language` sont renseignés
ensemble. Une langue non précisée dans la source peut être signalée par `und` ;
ne pas inventer une attribution linguistique précise.

Les formes facultatives sont regroupées par langue : `forms.fr.feminine`,
`forms.en.plural`, etc. Les noms de formes sont des conventions éditoriales
extensibles, pas des règles de flexion exécutées. Les titres invariables, le pluriel,
la titulature complète et la formule d’adresse doivent rester distincts quand la
documentation l’exige. Aucun genre de titulaire n’est déduit du libellé français.

`translation` vaut `equivalent`, `gloss` ou `loanword`. Ce champ indique un choix
de traduction, pas une équivalence de souveraineté, de prestige ou de grade.

## Critères avant publication

- Aucune source inconnue, charge dupliquée, relation orpheline ou boucle `reports_to`.
- Pas d’extension tacite d’un titre d’empire à un village, ou d’une institution
  contemporaine à toute une période médiévale.
- Titres sourcés et pouvoirs génériques visibles séparément.
- Les contrôles réciproques et organes collectifs restent représentables.
- Les absences restent diagnostiquées et la matrice de couverture est régénérée.
- Une source contradictoire appelle une variante ou une note de portée, pas un
  vote majoritaire silencieux entre sources.

Pour l’intégration démographique, compléter les règles de recrutement et leurs
paramètres avant d’affecter des personnes. La présence d’une charge n’autorise pas
à inventer automatiquement sa règle d’accès.
