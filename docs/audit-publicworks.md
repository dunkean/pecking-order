# Public works system replacements

Prepared 2026-10-21 as a standalone replacement array for the 12 template systems in `systems.json`. The array is at `../_tmp/publicworks_coherence_replacements.json`; the source `systems.json` was not edited. All 12 system IDs are preserved. The role lists contain 90 total roles, tailored to the service rather than repeating an engineer, warden, delegate, clerk and laborer in every group.

Each replacement keeps the existing system identity and supplies bilingual descriptions and role duties, service-specific functions, authority levels, scopes, size thresholds, reporting lines, powers, collective status and optionality. Existing role IDs are retained where they still describe the post; new IDs identify the distinct specialist jobs. Governance defaults distinguish horizontal user and neighbor bodies, hierarchical municipal services and the distributed road network.

## System-by-system audit

| System ID | Tailored organization |
|---|---|
| `water_board` | Basin users’ council, watermaster, hydraulic engineer, user delegates, gauge keeper, water-rights registrar and maintenance crew. The watermaster applies recorded allocation rights; the council resolves access disputes. |
| `irrigation_council` | Irrigators’ council, rotation watermaster, canal engineer, branch delegates, rotation registrar, canal foreman and ditch crew. Work and user representation are tied to irrigation seasons and canal branches. |
| `fire_watch` | Fire-service committee and chief, prevention inspector, alarm keeper, pump and apparatus keeper, response crew, evacuation lead and incident registrar. Roles cover prevention, alert, suppression, rescue and evacuation. |
| `public_works_office` | Public-works commission and director, civil engineer, surveyor, construction inspector, contracts clerk, site foreman and municipal works crew. The chain connects capital planning to estimates, inspection, procurement and site delivery. |
| `sanitation_board` | Sanitation commission and superintendent, drinking-water analyst, public-health inspector, collection-route manager and crew, outbreak registrar and food inspector. Health sampling, waste removal and outbreak notices have separate responsibilities. |
| `harbor_authority` | Harbor commission and master, pilot, channel engineer, berth registrar, harbor watch and rescue crew, dock foreman and maintenance crew. Duties cover traffic, pilotage, channels, rescue and quay upkeep. |
| `commons_trust` | Commoners’ assembly, commons steward, woodland and grazing wardens, resource recorder, user delegates and regeneration crew. Roles balance customary access, sustainable use, records and seasonal works. |
| `neighborhood_watch` | Neighborhood meeting, volunteer coordinator and walking pairs, accompaniment liaison, alert relay, incident recorder and municipal safety liaison. The network observes and reports, accompanies neighbors and refers hazards to public services. |
| `relief_society` | Members’ assembly, relief coordinator, needs assessor, fund treasurer, stores keeper, distribution lead, care liaison and volunteer registrar. The structure follows needs assessment, aid allocation, delivery and financial accountability. |
| `burial_society` | Members’ assembly, benefits treasurer, member registrar, claims examiner, funeral arranger, bereaved-family contact and funeral-service crew. Posts cover pooled benefits, eligibility, arrangements and family support. |
| `public_market_board` | Market commission and master, stall allocator, weights-and-measures inspector, food inspector, seller delegates, records clerk and cleaning crew. Allocation, fair measures, food safety and market upkeep are distinct functions. |
| `road_wardens` | Network coordinator, route wardens, bridge-and-ford inspector, road surveyor, warning relay, repair foreman and road crew. The network gathers conditions, warns travelers and organizes repairs without a military patrol hierarchy. |

## Validation

Parsed the replacement array and verified its exact 12-system ID set and 90 roles. Every power ID exists in the current power catalogs; role titles and duties have non-empty French and English text; size values and importance bounds are valid; title fallback keys do not collide with world or fantasy lexicons; and every reporting edge references a local role at a strictly lower authority level.

Integration check: the twelve systems expose their core governing and operating roles at tiny complexity too; specialist posts remain gated by increasing size. This preserves non-empty results for every supported size.
