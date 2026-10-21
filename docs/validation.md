# Validation — 2026-10-21

Environnement local : Windows, Python 3.12.13. Application autonome installée dans
son propre environnement ; aucun import d’un dépôt voisin.

## Contrat et résolution

`python -m pytest -q` : **173 tests réussis**.

Les contrôles couvrent les 85 modèles génériques et les 18 déclinaisons culturelles,
les profils ambigus, les périodes et échelles incompatibles, les titres FR/EN et
les replis linguistiques, les fonctions collectives, la séparation charge/grade,
les adaptations fictives et leurs conflits, le rejeu concurrent, les références
invalides, les cycles de commandement, les 15 exemples, les schémas JSON et leurs
références OpenAPI. Les tests HTTP vérifient les assets, les erreurs JSON, la taille
et le type des requêtes ainsi que le refus des origines étrangères. La CLI est
vérifiée en UTF-8, y compris avec une sortie Windows configurée en encodage hérité.

`ruff check src tests tools` : réussi.

`python -m pecking_order validate` : base valide, 85 modèles, 12 profils, 18
déclinaisons et 12 sources. Le catalogue, les schémas et la documentation de
couverture sont reproductibles depuis les sources éditoriales du dépôt.

## Navigateur

`python tools/check_browser.py` : réussi avec Playwright 1.64 et Microsoft Edge.
Parcours FR/EN, Kgosi/Karta, Grand Conseil, commandement militaire, Japon d’Edo,
adaptation autoritaire, ambiguïté de « africain », choix d’un contexte, roi/king,
export/import JSON, affichage à 390 px et absence d’erreurs de console.

Les captures complètes sont dans le répertoire local ignoré `output/screenshots/`.
La capture [demo.png](images/demo.png) est livrée avec le README. Le rendu de bureau
a été examiné visuellement. Les contrôles mobiles vérifient également l’absence de
débordement horizontal.

## Distribution

`python -m build` produit une archive source et une wheel. Les assets web et le
catalogue sont embarqués dans la wheel. L’archive source comprend également les
documents, schémas, exemples, outils éditoriaux et tests.

Une installation de la wheel dans un environnement distinct, hors du checkout,
vérifie l’import, la validation, une résolution bilingue avec titre d’origine et
le service des assets par le serveur HTTP installé.

## Limites de la preuve

Ces contrôles établissent le fonctionnement logiciel et la cohérence du pack,
pas l’exhaustivité ni l’exactitude historique de chaque modèle. Les sources
étayent les affirmations délimitées dans les données ; les autres restent des
modèles génériques. Les règles de succession et d’éligibilité restent déclaratives.
Les intégrations aux projets voisins sont documentées, sans modification de ces
projets ni validation de bout en bout dans leurs moteurs.

Un workflow GitHub Actions est fourni pour Python 3.12 sous Linux et Windows.
Son exécution distante est distincte des vérifications locales rapportées ici.
