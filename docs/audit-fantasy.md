# Fantasy-system coherence audit

Prepared complete replacement `System` objects for the 22 fantastic systems in `systems.json` that used the same generic arcane six-role bundle. The replacements are in `../_tmp/fantasy_coherence_replacements.json`; the source `systems.json` was not edited by this audit. System IDs, labels, aliases, descriptions, and related-system links are carried forward. The 116 replacement roles use distinct functions and concrete duties; generic arcane-office roles were replaced wherever they did not belong.

## System-by-system record

- `dragon_court` — recast as a consensual moot for brood claims, oaths, tribute accounting, boundary watch, and ratified notices; no archmage or unilateral sovereign.
- `adventuring_company` — made the contract circle the collective authority and assigned mission coordination, scouting, first aid, loot accounting, and equipment custody.
- `monster_hunters_lodge` — built a merit-based lodge around threat identification, bestiary records, hunt dispatch, armory care, field medicine, and tracker training.
- `druid_grove` — kept its horizontal structure and centered roles on harvest agreements, habitat stewardship, local healing, seasonal observation, place-memory, and neighboring communities.
- `fey_court` — kept personal court hierarchy, but replaced arcane roles with pact interpretation, guest hospitality, ritual-debt accounting, court notices, and mortal liaison.
- `necromantic_college` — shifted from generic authoritarian arcana to bureaucratic practice oversight, recorded consent, provenance, authorized spirit communication, containment inspection, and ethical training.
- `elemental_conclave` — kept consensual deliberation and added elemental delegation, balance mediation, planar observation, pact recording, and threshold watch.
- `dragon_clan` — replaced offices with a brood council, egg care, range observation, flight-debt witnesses, hunt scheduling, and genealogy.
- `adventurers_guild` — distinguished the standing guild from a field company through certification, contract review, mission registry, claims adjudication, and common funds.
- `planar_gate_authority` — tailored the bureaucracy to crossing authorization, traveler records, threshold survey, contamination checks, gate engineering, and arrival notices.
- `golem_workshop` — centered roles on construct design, safe binding, testing, materials provenance, certified repair, and apprenticeship under a workshop master.
- `dragonflight` — retained a military hierarchy where it fits, with flight command, wing leadership, aerial reconnaissance and signals, sustainment, and casualty care.
- `arcane_registry` — made the head a registrar and added spell-risk review, pact filing, artifact provenance, hazard inspection, and appeals.
- `monster_pack` — recast its horizontal/personal mismatch as a personal-led pack with tracking, den and young protection, hunt coordination, prey sharing, and injury care.
- `relic_custodians` — tailored the theocratic institution to custody governance, provenance, object care, authorized ritual use, seal inspection, and acolyte training.
- `witch_coven` — kept consensual horizontal governance and assigned teaching, herb care, community-boundary mediation, member care, and shared-knowledge records.
- `guild_of_enchanters` — used craft governance, quality certification, reagent inventory, instruction, defect adjudication, and repair provenance.
- `undead_legion` — retained command hierarchy for a military force, with binding integrity and reliquary sustainment alongside cohort command and signals.
- `demon_pact_court` — made pact adjudication its core, supported by clause review, witness records, obligation valuation, mortal advocacy, and pledge custody.
- `mage_college` — preserved teaching and research while making safety review, library records, transparent sponsorship, and apprenticeship explicit.
- `spirit_court` — replaced the arcane bundle with collective petition hearings, boundary arbitration, living-world liaison, consent witnesses, and place-agreement memory.
- `oracle_network` — made omens explicitly collective and uncertain through shared validation, individual readings, cross-vision comparison, exact records, notices, and seeker counseling.

## Validation

The output is a JSON array of 22 complete system objects and 135 roles. JSON parsing and structural checks passed: all bilingual fields are present, all local reporting references resolve, there are no reporting cycles or duplicate role IDs, and all powers exist in the current `data/powers*.json` catalogs. The 40 custom role keys have bilingual local fallback titles and are absent from the theme lexicons, so theme titles cannot override them. No role-function/power/scope/size signature remains duplicated within the replacement set.
