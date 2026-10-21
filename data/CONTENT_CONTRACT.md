# Shared content contract for the Rust rewrite

Work only on your assigned JSON content file. Content, not citations. Worldbuilding
themes can freely extrapolate. All text fr/en. JSON UTF-8, arrays at file root.

## Theme files: themes_world.json / themes_fantasy.json

Each record: {"id":"western-europe", "label":{"fr":"Europe de l’Ouest","en":"Western Europe"},
"aliases":["european-organic", "bastide", "western_europe"],
"parent":null, "description":{"fr":"...","en":"..."},
"titles":{"king":{"fr":"Roi","en":"King","native":null,"variants":[]}, ...}}

parent is an optional ID to inherit a themed lexicon. Avoid long parent chains.
aliases must include all assigned city IDs. Feel free to make city ID the theme ID.
Variants: [{"fr":"Reine","en":"Queen","native":null,"qualifier":"feminine"}].
No data field citations/evidence/sources. Add lots of relevant domain-specific titles,
not just monarchs. 65+ title keys per broad theme, extended keys when appropriate.

Core lexical keys to cover with culture-specific terms or creative thematic equivalents:
emperor, king, regent, royal_heir, duke, margrave, count, baron, lord, governor,
head_of_state, head_of_government, minister, councillor, assembly, mayor, deputy,
village_head, elder, judge, magistrate, clerk, treasurer, steward, tax_collector,
ambassador, herald, spymaster, marshal, general, admiral, commander, captain,
lieutenant, sergeant, soldier, guard, quartermaster, scout, high_priest, priest,
abbot, monk, novice, oracle, ritualist, temple_steward, grandmaster, guildmaster,
warden, craft_master, journeyman, apprentice, artisan, merchant, broker,
family_head, matriarch, patriarch, family_manager, clan_head, clan_mother,
lineage_elder, retainer, member, initiate, adept, cult_leader, cell_leader,
messenger, keeper, scholar, teacher, healer, navigator, representative,
chief_engineer, laborer, champion, patron, chancellor, priestess, council_nobles,
elected_leader, assembly_member, secretary, inquisitor, assassin, smuggler,
recruiter, archivist, proselytizer, cantor, sacristan, scribe, seer.

## Systems file: systems.json

Each {"id":"kingdom","family":"political","label":{"fr":"Royaume","en":"Kingdom"},
"aliases":["royaume"],"description":{"fr":"...","en":"..."},
"default_structure":"hierarchical","default_authority":"hereditary",
"related":["province","city"],"roles":[...]}

Structures: hierarchical, horizontal, network, cellular.
Authorities: hereditary, aristocratic, authoritarian, democratic, theocratic,
military, bureaucratic, meritocratic, consensual, personal.

Role {"id":"ruler","key":"king","function":"sovereignty",
"level":0,"importance":100,"scope":"realm","min_size":"tiny",
"reports_to":[],"duties":{"fr":"...","en":"..."},
"powers":["legislate","appoint"],"collective":false,"optional":false}

min_size: tiny, small, medium, large, vast. Query full returns all.
Scopes free semantic strings: realm, province, city, village, organization, unit, cell,
household, network, chapter. Levels 0=highest authority, increasing downwards;
importance 0..100 is relative to the institution. Multiple independent level0 roles
are allowed. A headless horizontal institution does not require a king-like leader.
Reports_to local role IDs, acyclic. Roles may share lexical keys but distinct IDs.
Powers are semantic verbs/IDs, not user-facing prose. Duties are substantial concrete
responsibilities, not 'participate'. Related references must point to actual systems;
you can omit related until all IDs are known.

Aim 100+ substantive systems across politics, local administration, military, religion,
kinship, crafts/economy, justice, education, civic groups, clandestine groups, fantasy.
6-20 roles each; especially full territorial tiers for empire/kingdom/nation, small
rare cult cell with four useful tiny roles, larger religious hierarchies, real corporate
households but no trivial biological family. Generic contracts, themed titles later.
