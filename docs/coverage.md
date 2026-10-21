# Couverture / Coverage

Document généré depuis le catalogue distribué avec `python tools/export_docs.py`.

**85 modèles génériques / generic blueprints**, **12 profils / profiles**, **18 déclinaisons / bindings**, **12 sources**.

La couverture des types est large. La couverture historique est initiale et partielle.
Broad institution coverage; initial, partial historical coverage.

Un modèle générique est une proposition de worldbuilding, pas une affirmation universelle.
A generic model is an authored worldbuilding proposal, not a universal historical claim.

## Modèles réutilisables / Reusable blueprints

| ID | Français | English | Domaine / Domain | Échelles / Scales |
|---|---|---|---|---|
| `hereditary_monarchy` | Monarchie héréditaire | Hereditary monarchy | political | polity, regional |
| `elective_monarchy` | Monarchie élective | Elective monarchy | political | polity, imperial |
| `empire` | Entité impériale | Imperial polity | political | imperial |
| `traditional_kingship` | Royauté coutumière | Traditional kingship | political | regional, polity |
| `chiefdom` | Chefferie | Chiefdom | political | local, district, regional |
| `village_council` | Gouvernance villageoise coutumière | Customary village governance | political | local |
| `city_republic` | République urbaine | City republic | political | local, polity |
| `representative_republic` | République représentative | Representative republic | political | polity, regional |
| `direct_assembly` | Entité gouvernée par assemblée | Assembly polity | political | local, polity |
| `oligarchy` | Gouvernement oligarchique | Oligarchic government | political | local, polity, imperial |
| `military_regime` | Gouvernement militaire | Military government | political | regional, polity, imperial |
| `theocracy` | Gouvernement sacral | Sacral government | political | polity, imperial |
| `confederation` | Confédération | Confederation | political | regional, polity, imperial, transregional |
| `federation` | Fédération | Federation | political | polity, imperial |
| `segmentary_council` | Conseil de lignages segmentaires | Segmentary lineage council | political | local, regional |
| `age_grade_governance` | Gouvernement tournant par classes d’âge | Rotating age-grade government | political | local, regional, polity |
| `diaspora_council` | Conseil de diaspora | Diaspora council | civic | local, transregional |
| `province` | Administration provinciale | Provincial administration | administrative | district, regional |
| `municipality` | Municipalité | Municipality | administrative | local, district |
| `palace_bureau` | Bureau palatial | Palace bureau | administrative | local, polity, imperial |
| `tax_office` | Administration fiscale | Revenue administration | administrative | district, regional, polity |
| `border_administration` | Administration frontalière | Frontier administration | administrative | district, regional |
| `army` | Armée | Army | military | regional, polity, imperial |
| `army_corps` | Corps d’armée | Army corps | military | regional, polity |
| `division` | Division | Division | military | regional, polity |
| `brigade` | Brigade | Brigade | military | district, regional |
| `regiment` | Régiment ou bataillon | Regiment or battalion | military | district, regional |
| `company` | Compagnie | Company | military | local, district |
| `warband` | Suite armée ou bande guerrière | Retinue or warband | military | local, regional |
| `militia` | Milice | Militia | military | local, district |
| `mercenary_company` | Compagnie mercenaire | Mercenary company | military | district, transregional |
| `fleet` | Flotte | Fleet | military | regional, transregional |
| `military_order` | Ordre militaire religieux | Military religious order | military | regional, transregional |
| `religious_hierarchy` | Hiérarchie religieuse | Religious hierarchy | religious | polity, transregional |
| `diocese` | Diocèse | Diocese | religious | district, regional |
| `parish` | Communauté religieuse locale | Local religious community | religious | local |
| `temple` | Institution de temple | Temple institution | religious | local, regional |
| `monastery` | Monastère | Monastery | religious | local, regional |
| `religious_order` | Ordre religieux | Religious order | religious | regional, transregional |
| `congregation` | Communauté congrégationaliste | Congregational community | religious | local, regional |
| `initiatory_society` | Société initiatique | Initiatory society | religious | local, regional |
| `shrine_network` | Réseau de sanctuaires | Shrine network | religious | regional, transregional |
| `craft_guild` | Guilde artisanale | Craft guild | economic | local, regional |
| `merchant_guild` | Guilde marchande | Merchant guild | economic | local, transregional |
| `workshop` | Atelier organisé | Corporate workshop | economic | local |
| `trade_company` | Compagnie commerciale | Trading company | economic | regional, transregional |
| `cooperative` | Coopérative | Cooperative | economic | local, regional |
| `irrigation_association` | Association d’irrigation | Irrigation association | economic | local, district |
| `commons_association` | Association de gestion des communs | Commons association | economic | local, regional |
| `caravan` | Organisation caravanière | Caravan organization | economic | regional, transregional |
| `market_authority` | Autorité du marché | Market authority | economic | local, district |
| `bank` | Maison bancaire | Banking house | economic | local, transregional |
| `labor_union` | Syndicat professionnel | Labor union | economic | local, transregional |
| `corporate_household` | Famille indivise à patrimoine commun | Corporate joint household | kinship | household, local |
| `lineage` | Lignage organisé | Corporate lineage | kinship | local, regional |
| `clan` | Institution clanique | Clan institution | kinship | local, regional, transregional |
| `noble_house` | Maison noble | Noble house | kinship | household, regional, polity |
| `royal_dynasty` | Dynastie royale | Royal dynasty | kinship | polity, imperial |
| `matrilineal_house` | Maison matrilinéaire organisée | Matrilineal corporate house | kinship | household, local |
| `adoptive_house` | Maison organisée par adoption | Adoptive corporate house | kinship | household, local |
| `marriage_alliance` | Alliance entre maisons | Inter-house alliance | kinship | local, regional |
| `court` | Cour de justice | Court of justice | judicial | local, regional, polity |
| `customary_tribunal` | Tribunal coutumier | Customary tribunal | judicial | local, district |
| `arbitration_body` | Instance d’arbitrage | Arbitration body | judicial | local, transregional |
| `legal_college` | Collège de juristes | College of jurists | judicial | regional, transregional |
| `university` | Corporation universitaire | University corporation | educational | local, transregional |
| `academy` | Académie | Academy | educational | local, transregional |
| `school` | École organisée | Institutional school | educational | local, regional |
| `library` | Institution de bibliothèque | Library institution | educational | local, regional |
| `neighborhood_association` | Association de quartier | Neighborhood association | civic | local |
| `fraternity` | Confrérie d’entraide | Mutual-aid fraternity | civic | local, regional |
| `age_set` | Association de classe d’âge | Age-set association | civic | local, regional |
| `hospital` | Fondation hospitalière | Hospital foundation | civic | local, regional |
| `festival_society` | Société de fête | Festival society | civic | local, regional |
| `criminal_syndicate` | Syndicat criminel | Criminal syndicate | clandestine | local, transregional |
| `secret_society` | Société secrète | Secret society | clandestine | local, transregional |
| `insurgent_network` | Réseau insurgé | Insurgent network | clandestine | regional, transregional |
| `patronage_network` | Réseau de clientèle | Patronage network | clandestine | local, transregional |
| `embassy` | Mission diplomatique | Diplomatic mission | diplomatic | polity, transregional |
| `interstate_league` | Ligue entre États | Interstate league | diplomatic | transregional |
| `treaty_commission` | Commission de traité | Treaty commission | diplomatic | regional, transregional |
| `mage_college` | Collège de magie | College of magic | fantastic | local, transregional |
| `adventurers_guild` | Guilde d’aventuriers | Adventurers' guild | fantastic | local, transregional |
| `hive_collective` | Collectif de ruche | Hive collective | fantastic | local, imperial |
| `spirit_court` | Cour des esprits | Spirit court | fantastic | local, transregional |

## Profils documentés / Documented profiles

| ID | Contexte / Context | Période / Period | Déclinaisons / Bindings |
|---|---|---|---|
| `vijayanagara_krishnadevaraya` | Cour de Vijayanagara, 1509–1529 / Vijayanagara court, 1509–1529 | 1509–1529 | `hereditary_monarchy`, `empire` |
| `deccan_sultanates` | Cours des sultanats du Deccan, 1500–1687 / Deccan sultanate courts, 1500–1687 | 1500–1687 | `hereditary_monarchy` |
| `hindu_joint_family_india` | Famille hindoue indivise, contexte statutaire indien / Hindu undivided family, Indian statutory context | 2025–2026 | `corporate_household` |
| `tswana_bogosi_contemporary` | Bogosi tswana, contexte de référence au Botswana / Tswana bogosi, Botswana reference context | 2025–2026 | `village_council` |
| `oromo_gadaa_reference` | Gadaa oromo, description de référence UNESCO / Oromo Gadaa, UNESCO reference description | 2016–2026 | `age_grade_governance` |
| `asante_traditional_contemporary` | Institution royale coutumière asante / Asante traditional royal institution | 2026–2026 | `traditional_kingship` |
| `haudenosaunee_confederacy_reference` | Confédération haudenosaunee, description propre / Haudenosaunee Confederacy, self-description | 2026–2026 | `confederation` |
| `balinese_subak_reference` | Contexte coopératif subak balinais / Balinese subak cooperative context | 2012–2026 | `irrigation_association` |
| `british_army_contemporary` | British Army, affectations contemporaines habituelles / British Army, typical contemporary appointments | 2026–2026 | `army_corps`, `division`, `brigade`, `regiment`, `company` |
| `london_livery_reference` | Compagnie de livrée londonienne, modèle de référence / London livery company, general reference model | 2026–2026 | `craft_guild` |
| `latin_catholic_canonical` | Institutions canoniques catholiques latines / Latin Catholic canonical institutions | 1983–2026 | `diocese`, `parish` |
| `japan_edo_reference` | Japon d’Edo, contexte de référence 1600–1800 / Edo Japan, 1600–1800 reference context | 1600–1800 | `empire` |

## Axes de recherche encore ouverts / Further research

Les éléments ci-dessous sont des pistes, pas des données disponibles ni des promesses d’authenticité. / These are research directions, not available data or claims of authenticity.

- Cours et administrations impériales : traditions chinoises, ottomanes, romaines, byzantines, persanes et mésoaméricaines, par époque et juridiction.
- Chefferies, royautés et systèmes sans pouvoir central : profils locaux supplémentaires en Afrique, Océanie, Asie et dans les Amériques.
- Institutions religieuses : traditions musulmanes, juives, bouddhiques, hindoues, chrétiennes orientales et traditions locales, avec leurs propres distinctions.
- Institutions de métier : corporations historiques hors du modèle londonien contemporain, guildes marchandes, marchés, compagnies et associations de ressources.
- Parenté corporative : maisons japonaises, lignages chinois, maisons et clans matrilinéaires, variantes de la famille indivise selon lieu, école et période.
- Armées : chaînes de commandement anciennes et modernes, formations navales, grades, charges, milices, suites et unités irrégulières.
- Traductions supplémentaires, variantes régionales, titulatures complètes et formules d’adresse documentées.

Une absence de déclinaison renvoie `unsupported` en mode historique. Les limites de chaque profil figurent dans les données et dans les sources.
