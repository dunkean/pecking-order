# Base system and role coherence audit

Reviewed all 175 system records and their 1326 role definitions against `data/CONTENT_CONTRACT.md`, `src/model.rs`, and `src/engine.rs`.

The runtime resolves a role key from the selected theme before trying `role.title`. Context-specific offices therefore use a new `context_*` key and a bilingual fallback title when a generic lexical key would misname the job. No theme files were changed. Duties, powers, reporting chains, levels, importance and size thresholds were reviewed.

## Substantive corrections

- Replaced copied combat ladders in intelligence work, siege engineering, war and siege-defense councils, and a veterans association with the actual analysis, engineering, deliberation and member-support functions those bodies perform. Retained naval and military ranks where those systems really command forces.
- Corrected command seniority in army, militia, garrison, mercenary company, navy and naval fleet; generals and admirals now sit above unit command. Corrected tax-collection, imperial local-government, regency and merchant-guild reporting levels so every parent is strictly senior.
- Replaced craft-school roles inside banks, credit unions and a workers union with finance and labor-relations work. Gave market regulation, shipping, insurance, mining and other firms their own operating functions. Bank staff now report to the operations head; credit-union members govern above operations.
- Replaced redundant gendered authorities copied into family systems with distinct household counsel and succession-record work; the matrilineal house now has a maternal heir. Rebuilt the inheritance court as an actual tribunal.
- Specialized inquiry, mediation, prison administration, appeals and education roles instead of reusing one generic court or school template.
- Reworked shrine, hermitage, mission, lay association, funerary, festival and religious-imperial roles to match their setting. Refuge camps and disaster commissions now coordinate resident services and emergency response rather than using generic association offices.
- Reworked the smuggler and thieves’ guild leaders as chiefs, kept their crew and cache duties distinct, and replaced press and mutual-aid spying offices with editorial and care functions.

## System-by-system record

### political (45)

- `kingdom`: revised `tax_collector`.
- `empire`: revised `district_prefect`, `local_elder`.
- `aristocratic_nation`: revised `regent`.
- `sacred_kingdom`: revised `tax_collector`.
- `refuge_camp`: revised `assembly`, `delegate`, `chair`, `secretary`, `treasurer`, `mediator`, `technical_steward`.
- `disaster_commission`: revised `assembly`, `delegate`, `chair`, `secretary`, `treasurer`, `mediator`, `technical_steward`.
- Reviewed and retained: `democratic_nation`, `federation`, `confederation`, `city_state`, `city`, `village`, `hamlet`, `province`, `frontier_march`, `tributary_realm`, `elective_monarchy`, `principality`, `duchy`, `county`, `barony`, `free_city`, `chartered_town`, `ward`, `rural_district`, `protectorate`, `occupied_territory`, `nomadic_confederation`, `tribal_council`, `island_polity`, `canal_authority`, `crown_council`, `parliament`, `local_council`, `village_federation`, `frontier_settlement`, `city_league`, `republic`, `bureaucratic_state`, `theocracy`, `military_junta`, `revolutionary_council`, `colonial_administration`, `merchant_republic`, `guild_republic`.

### religious (20)

- `mystery_cult`: revised `presiding_minister`, `house_steward`, `care_minister`.
- `religious_empire`: rebuilt its offices around sacred territorial governance, with a sovereign-to-provincial-to-district-to-local chain; the administrative novice now reports to the scribe, while the inquisitor answers to the presiding minister as an independent appellate authority.
- `pilgrimage_shrine`: revised `presiding_minister`, `ritual_leader`, `doctrine_keeper`.
- `oracle_house`: revised `presiding_minister`, `ritual_leader`, `care_minister`.
- `ancestor_shrine`: revised `presiding_minister`, `ritual_leader`, `doctrine_keeper`.
- `hermitage`: revised `presiding_minister`, `ritual_leader`, `care_minister`.
- `mission_station`: revised `presiding_minister`, `ritual_leader`, `doctrine_keeper`.
- `lay_brotherhood`: revised `presiding_minister`, `ritual_leader`, `doctrine_keeper`, `novice`.
- `temple_estate`: revised `presiding_minister`, `house_steward`, `care_minister`.
- `funerary_guild`: revised `presiding_minister`, `ritual_leader`, `house_steward`, `care_minister`.
- `festival_council`: revised `presiding_minister`, `ritual_leader`, `doctrine_keeper`.
- Reviewed and retained: `temple_city`, `cult`, `shamanic_circle`, `priesthood`, `monastery`, `religious_order`, `congregation`, `cult_cell`, `heresy_court`.

### economic (20)

- `merchant_guild`: revised `master`, `journeyman`, `apprentice`, `factor`, `broker`, `accountant`, `guildmaster`, `artisan`.
- `workers_union`: revised `master`, `journeyman`, `apprentice`, `factor`, `broker`, `accountant`, `member`.
- `caravan_company`: revised `master`, `journeyman`, `apprentice`, `smuggler`.
- `trading_company`: revised `master`, `journeyman`, `apprentice`.
- `bank`: revised `master`, `journeyman`, `apprentice`, `factor`, `broker`, `accountant`, `member`.
- `credit_union`: revised `master`, `journeyman`, `apprentice`, `factor`, `broker`, `accountant`, `member`.
- `market_authority`: revised `master`, `journeyman`, `apprentice`.
- `merchant_caravan`: revised `master`, `journeyman`, `apprentice`, `smuggler`.
- `mining_company`: revised `master`, `journeyman`, `apprentice`.
- `shipping_consortium`: revised `master`, `journeyman`, `apprentice`, `admiral`.
- `insurance_house`: revised `master`, `journeyman`, `apprentice`.
- `labor_exchange`: revised `master`, `journeyman`, `apprentice`.
- Reviewed and retained: `craft_guild`, `apprenticeship_workshop`, `cooperative`, `fishing_cooperative`, `farm_collective`, `guild_federation`, `toll_keepers`, `grain_exchange`.

### military (18)

- `army`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `general`, `guard`.
- `militia`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `general`, `guard`.
- `navy`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `admiral`, `navigator`.
- `intelligence_service`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `assassin`.
- `mercenary_company`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `general`, `guard`.
- `siege_train`: revised `captain`, `lieutenant`, `sergeant`, `scout`, `soldier`.
- `garrison`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `general`, `guard`.
- `naval_fleet`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`, `admiral`, `navigator`.
- `war_council`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`.
- `siege_defense_council`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`.
- `veterans_association`: revised `commander`, `captain`, `lieutenant`, `sergeant`, `quartermaster`, `scout`, `soldier`.
- Reviewed and retained: `pirate_flotilla`, `knightly_order`, `border_guard`, `scout_company`, `military_order`, `coast_watch`, `combat_company`.

### kinship (10)

- `joint_family`: revised `matriarch`, `patriarch`.
- `matrilineal_house`: revised `patriarch`.
- `noble_house`: revised `matriarch`, `patriarch`.
- `lineage`: revised `matriarch`, `patriarch`.
- `clan`: revised `matriarch`, `patriarch`.
- `dynasty`: revised `matriarch`, `patriarch`.
- `adoptive_house`: revised `matriarch`, `patriarch`.
- `retainer_household`: revised `matriarch`, `patriarch`.
- `clan_council`: revised `matriarch`, `patriarch`.
- `inheritance_court`: revised `house_head`, `matriarch`, `patriarch`, `lineage_elder`, `house_steward`, `retainer`, `member`.

### judicial (10)

- `guild_court`: revised `magistrate`, `mediator`.
- `inquest_commission`: revised `chief_judge`, `magistrate`, `advocate`, `bailiff`.
- `mediation_circle`: revised `chief_judge`, `magistrate`, `advocate`, `bailiff`.
- `prison_administration`: revised `chief_judge`, `magistrate`, `advocate`, `clerk`, `mediator`, `bailiff`.
- `appeals_court`: revised `chief_judge`, `magistrate`.
- Reviewed and retained: `court_of_justice`, `village_court`, `watch_court`, `arbitration_chamber`, `customary_council`.

### educational (10)

- `academy`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `village_school`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `university`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `scriptorium`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `library`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `guild_school`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `observatory`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `healing_house`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `apprentice_school`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.
- `scholars_circle`: revised `rector`, `faculty`, `scholar`, `librarian`, `apprentice`, `registrar`.

### civic (12)

- Integrated the civic companion audit in `audit-publicworks.md`; all twelve systems received service-specific roles and duties: `water_board`, `irrigation_council`, `fire_watch`, `public_works_office`, `sanitation_board`, `harbor_authority`, `commons_trust`, `neighborhood_watch`, `relief_society`, `burial_society`, `public_market_board`, `road_wardens`.

### clandestine (8)

- `smugglers_ring`: revised `coordinator`, `cell_leader`, `keeper`.
- `thieves_guild`: revised `coordinator`, `cell_leader`, `spymaster`.
- `secret_society`: distinguished society convenor from local cell steward; added the cell reporting chain and tiny-group member threshold. The assassin remains an optional specialist.
- `assassins_order`: distinguished order master from local commission handler; added delegated cell reporting and small-group thresholds.
- `resistance_network`: distinguished network convener from local cell delegate; added cell reporting and resident-sized member thresholds.
- `spy_ring`: distinguished intelligence chief from local cell handler; added checked-reporting chain and tiny-group member threshold.
- `underground_press`: clarified coordinator-to-cell-lead delegation and tiny-group membership alongside editorial roles.
- `mutual_aid_cell`: clarified coordinator-to-cell-lead delegation and tiny-group membership alongside care and supply roles.

### fantastic (22)

- Integrated the fantasy companion audit in `audit-fantasy.md`; all twenty-two systems now have setting-specific offices, duties, powers and reporting chains: `mage_college`, `dragon_court`, `adventuring_company`, `monster_hunters_lodge`, `druid_grove`, `fey_court`, `necromantic_college`, `elemental_conclave`, `dragon_clan`, `adventurers_guild`, `planar_gate_authority`, `golem_workshop`, `dragonflight`, `arcane_registry`, `spirit_court`, `monster_pack`, `relic_custodians`, `witch_coven`, `guild_of_enchanters`, `oracle_network`, `undead_legion`, `demon_pact_court`.

## Structural notes

The current `reports_to` graph has no cycles, unknown role parents or parent edges at the same/lower level; all 1326 roles were checked after the merged civic and fantasy data and final cell-chain corrections. The content loader resolves all related-system references. Power labels for this pass’s new IDs were added to the shared catalog by the root integration. Context-key leaders that need authority adaptation are now recognized by the engine by office identity.

Validation performed: UTF-8 JSON parse and authored reporting-level audit. No commits were made.
