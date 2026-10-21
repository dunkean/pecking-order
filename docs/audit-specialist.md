# Specialist systems audit

Audited all 30 systems and 120 roles in `data/systems_specialist.json` against `data/CONTENT_CONTRACT.md`, the role model, and engine title resolution. System IDs are unchanged. Duties and powers remain concrete, scoped to each institution, and translated into French and English; no roles were deleted.

## System-by-system record

- `temple_granary_office` — retained all four roles; changed `ration_caller` to a local bilingual ration-clerk title because the theme's `representative` title described the wrong office.
- `sacred_calendar_council` — retained `calendar_circle`, `sky_observer`, `date_recorder`, and `temple_messenger`; collective calendar adoption and supporting observation, records, and notices fit its horizontal council.
- `pilgrimage_wayhouse_network` — retained `route_host`, `house_keeper`, `road_guide`, and `wayhouse_healer`; coordination and local service roles fit a consensual network.
- `procession_company` — retained all four roles; gave `procession_marshal` a local title to disambiguate its event-route and crowd-safety function from generic marshal ranks.
- `vow_renewal_court` — retained `vow_judge`, `vow_registrar`, `vow_witness`, and `vow_mediator`; gave `vow_witness` a local consent-witness title because the theme’s “Delegate” title implied representation rather than witnessing. Review, recording, and dispute mediation form a coherent small court.
- `vow_release_circle` — gave `release_witness` a local closure-witness title because “Elder” implied seniority rather than its witnessing duty. Retained `release_circle`, `oath_keeper`, and `restitution_steward`; the small consensual circle has no individual executive.
- `funerary_boat_brotherhood` — retained `boat_circle`, `funeral_pilot`, `farewell_cantor`, and `boat_keeper`; collective scheduling and vessel, route, and rite duties fit the crew.
- `mortuary_purification_house` — retained `purification_master`, `body_keeper`, `linen_steward`, and `mortuary_scribe`; specialist ritual direction and preparation duties fit the house.
- `ancestor_feast_compact` — changed `house_host` to a local commemorative-host title; this role hosts visiting kin and does not head a family. Retained the council, contributions steward, and name cantor.
- `lineage_memory_archive` — retained `genealogy_keeper`, `lineage_scribe`, `adoption_registrar`, and `memory_reader`; custodianship and the supporting archive roles are coherent for a family repository.
- `diviner_apprentice_house` — retained `divination_tutor`, `instrument_keeper`, `practice_examiner`, and `novice_recorder`; instruction, tools, assessment, and records fit a small school.
- `dream_interpretation_circle` — retained `dream_circle`, `dream_recorder`, `sleep_watcher`, and `ritual_cantor`; peer deliberation, privacy, care, and optional closure rites fit a horizontal circle.
- `itinerant_prophets_movement` — changed `movement_voice` to the specific bilingual title “Movement Preacher” / “Prédicateur du mouvement”; retained the messenger, testimony recorder, and guest keeper. The top role coordinates preaching and travel rather than holding a state or military office.
- `mendicant_preaching_network` — made `fraternity_circle` the level-0 collective and placed `route_preacher` beneath it; the recorder and messenger report to the circle. Changed the preacher to a local itinerant-preacher title. This aligns its reporting with its consensual authority while preserving useful operating roles.
- `mendicant_almonry` — changed `almoner` and `meal_cook` to local titles because the theme keys would render them as a healer and generic laborer. Retained the alms steward and shelter keeper.
- `exorcist_lodge` — gave `lodge_master` a local title rather than using the generic high-priest title; retained case examination, consent-based rites, and follow-up care.
- `possession_witness_circle` — retained all four roles and corrected the French care-companion duty so it no longer contains an English word. Its powers and duties remain focused on impartial records, safety, care, and optional rites.
- `plague_vow_fellowship` — gave `burial_helper` a local funeral-assistant title instead of generic keeper; retained the collective, sickroom visitor, and vigil cantor.
- `epidemic_recovery_house` — gave `meal_keeper` and `return_guide` context-specific bilingual titles because “laborer” and “representative” mislabel cooking and discharge planning. Retained the recovery steward and healer.
- `solar_clock_custodians` — gave `time_caller` a local ritual-time announcer title rather than generic herald; retained technical calibration and recordkeeping roles.
- `astral_calendar_consortium` — retained `calendar_consortium`, `cycle_observer`, `almanac_editor`, and `port_messenger`; a merit-based network governs shared observation and publication.
- `sacred_grove_moot` — gave `grove_warden` a local grove-custodian title to clarify its monitoring and stewardship duties; retained the moot, envoy, and agreement scribe.
- `migration_omen_watch` — retained `migration_circle`, `trail_observer`, `range_messenger`, and `season_scribe`; these are useful observer and warning functions without an imposed command rank.
- `spring_spirit_compact` — retained `spring_compact`, `spring_keeper`, `water_scribe`, and `spirit_mediator`; negotiated access, site care, records, and ritual mediation fit the agreement.
- `pass_shrine_wardens` — gave `pass_warden` a local safety-warden title because the generic French “Prévôt” implied a civic magistrate. Retained `beacon_keeper` and `wayfinder`; replaced `rescue_captain` with a local rescue-coordinator title because this is a safety service role, not a military captaincy.
- `forge_initiation_order` — changed `forge_prior` from generic high priest to “Forge Prior” / “Prieur de la forge”, and `forge_instructor` from generic craft master to an instructor title. Both now name their specific order and teaching functions.
- `communal_oath_hunt` — retained the collective, scout, and catch steward; replaced `hunt_captain` with a local hunt-coordinator title suited to a seasonal consensual group.
- `relic_authentication_chamber` — retained `relic_examiner`, `provenance_scribe`, `relic_custodian`, and `chamber_recorder`; assessment remains distinct from physical custody.
- `roadside_lantern_brotherhood` — retained `lantern_circle`, `lantern_keeper`, `night_guide`, and `hazard_messenger`; these fit the neighborhood lighting and escort service.
- `dream_incubation_sanctuary` — gave `night_watcher` a local “Night Watcher” / “Veilleur de nuit” title rather than a generic warden title; retained the keeper, voluntary dream scribe, and cantor.

## Title-resolution and engine notes

`src/engine.rs` resolves a matching theme lexicon key before `RoleSpec.title`; a local bilingual title only acts as fallback when the key is absent. The 21 context-specific keys above are absent from the theme lexicons, so those fallbacks will actually display. The adjusted consensual network reports to its collective body in source data; network-mode queries clear reporting links by design, while horizontal-mode queries also flatten levels. The engine's authority adaptation only promotes a non-collective level-0 role for an explicit authoritarian hierarchical query.

## Validation

Parsed the file as JSON. A content audit found 30 systems, 120 roles, complete French and English duties, unique role IDs, valid local reporting references, no reporting cycles, and bilingual fallback titles for every role key absent from the theme lexicons.
