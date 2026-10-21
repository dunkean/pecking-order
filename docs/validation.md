# Validation — Rust 0.2.0

Vérifié sous Windows avec Rust 1.99, le 21 octobre 2026.

- `cargo fmt --check` : réussi.
- `cargo clippy --all-targets -- -D warnings` : réussi.
- `cargo test` : 17 tests réussis. Ils parcourent les 16 214 combinaisons système/thème,
  tous les systèmes à cinq tailles, ainsi que les 9 680 combinaisons système/structure/
  autorité. Les tests vérifient aussi les graphes après filtre, les alias usuels,
  les pouvoirs bilingues, les exemples livrés et les cas demandés par l’utilisateur.
- `cargo run -- validate` : 242 systèmes, 67 thèmes, 1 713 rôles, 6 124 entrées
  de titres et couverture des 41 cultures de Magna Urbis.
- `cargo check --lib --target wasm32-unknown-unknown` : réussi.
- `cargo build --release` : réussi ; exécutable Windows d’environ 3,3 Mo.
- Binaire copié et lancé hors du dépôt : validation complète réussie, sans fichier
  de données ni installation Python à proximité.

Les parcours navigateur couvrent le changement culturel Est/Ouest sur la même nation,
le village tswana, la cellule de quatre personnes, la famille indivise, le lexique
entier, FR/EN, les filtres, l’import/export JSON et un viewport de 390 px.
Commande : `npm run test:browser`, après lancement du studio. Les captures sont
dans `output/screenshots/` ; la capture de bureau livrée avec le README est examinée
visuellement.

`npm run test:glossary` vérifie les 4 484 termes, l’affichage intégral, les variantes,
les filtres culture/fonction, les quatre sections, les définitions et liens vers les
structures, la restauration de l’URL, les exports CSV/JSON, FR/EN et le mobile.
Deux tests Rust contrôlent que chaque titre et variante de chaque culture ainsi
que les 1 713 rôles fonctionnels sont présents, sans doublon de libellé exact.
Les captures `glossary-fr.png` et `glossary-mobile.png` ont été examinées visuellement.

Les tests établissent que le contenu est disponible et que sa composition fonctionne.
Les thèmes constituent du lore de worldbuilding. L’affectation de personnes, les
successions calculées, les dynamiques historiques et l’expansion récursive des
organisations ne font pas partie de ce moteur de titres et de fonctions.
