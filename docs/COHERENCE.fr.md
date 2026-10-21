# Révision de cohérence — contenu 0.3.0

Les 242 systèmes ont fait l’objet d’une revue groupe par groupe avec des agents
Luna, puis d’une relecture croisée. Le critère est la fonction réellement utile
dans l’organisation : missions, compétences, taille, autorité et subordination,
avec des intitulés français et anglais qui correspondent à cette fonction.
La revue a modifié 161 systèmes et 749 fiches de rôle. Le catalogue contient
maintenant 1 731 rôles et 4 959 termes distincts dans le glossaire.

## Corrections principales

- Bande de rue : chef, second, guetteur, gestionnaire des ressources, intermédiaire,
  messager et membre. Les postes militaires ne sont plus imposés par le thème.
- Banque et crédit mutuel : opérations, comptes, paiements, crédit et gouvernance
  des sociétaires remplacent le modèle maître/compagnon/apprenti d’un atelier.
- Renseignement, conseils de défense et anciens combattants : analyse, conseil,
  transmission et soutien aux membres remplacent les échelons de combat copiés.
- Médiation, prison, enquête et appel : les responsabilités judiciaires, de garde,
  de procédure et de représentation sont distinguées.
- Enseignement, bibliothèque, observatoire et soins : les missions décrivent leur
  métier réel ; le médecin soigne, l’astronome observe et l’apothicaire prépare
  les remèdes. Les registres portent sur les patients ou observations concernés.
- Religions : les fonctions des sanctuaires, ermitages, fraternités et guildes
  funéraires sont différenciées. L’empire religieux possède des échelons territoriaux.
- Sociétés clandestines : direction du réseau, responsabilité de cellule,
  renseignement, édition et entraide sont distingués selon le groupe.
- Douze services locaux : eau, irrigation, incendie, travaux, assainissement,
  port, communs, veille de quartier, secours, funérailles, marché et routes.
- Vingt-deux organisations fantastiques : cours, meutes, ateliers, collèges,
  compagnies et réseaux ont leurs fonctions propres au lieu du même ordre de mages.

## Règles du moteur

Une clé lexicale générale n’est conservée que si sa fonction convient au groupe.
Les postes spécialisés utilisent une clé de contexte et un intitulé FR/EN de
repli. Un thème peut ensuite définir cette clé pour lui donner un titre culturel
approprié. Le glossaire conserve ces postes quand on filtre par culture.

La qualité de chef est reconnue par la structure du rôle, indépendamment de sa
clé de titre. Le passage explicite à une organisation horizontale retire cette
position de chef. Le mode autoritaire ajoute une décision interne aux groupes ;
le pouvoir d’édicter des décrets reste réservé aux organisations de gouvernement.

L’API reste en version 2.0. La version de contenu passe à 0.3.0 : certains rôles
des anciens modèles copiés sont remplacés, avec de nouveaux identifiants et clés.
Les identifiants des 242 systèmes et des 67 thèmes sont conservés.

## Vérification

Les tests contrôlent les liens hiérarchiques, les combinaisons système/culture,
les tailles et les transformations de structure/pouvoir. Ils vérifient notamment
les fonctions de la bande dans les 67 cultures et le maintien des véritables
titres militaires dans les flottes. Ils ne constituent pas une preuve
d’exhaustivité historique de chaque tradition.

Les listes déroulantes des deux pages sont remplacées par des sélecteurs
recherchables, avec toutes les options présentes dès l’ouverture, un compteur,
la navigation au clavier et un menu qui reste dans l’écran sur mobile.

Rapports détaillés : [base](audit-base.md), [civique et militaire](audit-civic.md),
[spécialistes](audit-specialist.md), [services locaux](audit-publicworks.md),
[fantastique](audit-fantasy.md).
