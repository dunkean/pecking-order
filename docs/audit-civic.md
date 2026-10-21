# Civic and military content audit

Reviewed on 2026-10-21. This pass covers all 285 roles in the 37 systems in `systems_civic_military.json`, including title semantics, function, authority level, reporting relationships, powers and minimum size. Role IDs and role counts are unchanged.

## Rendering constraint

`Engine::resolve` resolves a role's `key` in the selected theme lexicon before it considers `RoleSpec.title`. Since each theme inherits the generic lexicon, supplying a bilingual `title` while retaining a broad key does not reliably control the displayed title. For posts whose cultural title could be unrelated to the job, this audit assigns a context-specific semantic key and a French/English fallback title. The new keys do not occur in the theme files, so the fallback is used. No theme file or engine code was changed.

## Findings and corrections

- The national system now models the local council as a collective body, with the mayor accountable to it. The regional administrator, election commissioner, auditor general, civil-service commissioner and public advocate have office-specific titles. The advocate recommends remedies instead of holding a power to impose them.
- Army-group through squad systems retain their commanders and military quartermasters. Operations, intelligence, signals and senior-enlisted staff now have rank-neutral titles tied to their duties. A squad's former operations planner is an assistant team leader; small squads can also have intelligence and signals functions. Their roles remain available rather than being removed.
- Naval forces retain genuine captain and quartermaster posts; merchant crews retain the ship master, purser and steward. The boatswain is named as such rather than appearing as a sergeant. Merchant-ship watch and repair titles are clarified, and the cook reports to the ship master, an office present in that system.
- Air-force titles now distinguish air operations, air traffic control and air intelligence. Expedition, raid and protection-detail posts use titles that describe their actual work; an entry specialist is no longer titled an assassin.
- Civic and commercial offices with misleading broad cultural keys now use context-specific titles. This includes public administration and parties, labor organizations, corporations, charter and colonial companies, estate administration, theatre, circus, sports and craft organizations. Industrial-action coordination no longer carries a marshal title or direct strike authority; union counsel and the contract jurist no longer imply that they are independent judges.
- The street gang remains an urban gang, not a civic association. Its roles now read as gang leader, second-in-command, lookout, shared-resource keeper, inter-crew intermediary, courier and gang member. The resource role handles shared cash and supplies and reports to the second; the intermediary negotiates boundaries and truces with rival crews.
- The revolutionary party secretariat and political-party candidate-selection panel are represented as collective bodies. Hierarchy edges across the file now descend to a lower level at each reporting relationship.

## Systems audited

| System ID | Audit result |
|---|---|
| `nation` | Corrected municipal governance and clarified public-office titles and advocate powers. |
| `army_group` | Replaced misleading staff ranks with theater-level functional titles; retained commander and quartermaster. |
| `army_corps` | Clarified staff titles; retained military command and logistics offices. |
| `division` | Clarified staff titles; retained military command and logistics offices. |
| `brigade` | Clarified staff titles; retained military command and logistics offices. |
| `regiment` | Clarified staff titles; retained military command and logistics offices. |
| `battalion` | Clarified staff titles; retained military command and logistics offices. |
| `company` | Clarified staff titles; retained military command and logistics offices. |
| `platoon` | Clarified staff titles; retained military command and logistics offices. |
| `squad` | Reframed operations role as assistant team leader and adjusted small-unit availability. |
| `naval_squadron` | Corrected boatswain title; retained commodore, formation captain and fleet quartermaster. |
| `warship_crew` | Corrected boatswain title; retained the ship captain and other coherent shipboard offices. |
| `merchant_ship_crew` | Clarified boatswain, watch officer and ship carpenter; corrected cook reporting line. |
| `air_force` | Clarified air operations, traffic-control and intelligence titles. |
| `expedition` | Clarified expedition leader, deputy, interpreter and surveyor titles. |
| `raiding_party` | Replaced the unsuitable assassin title for an entry specialist. |
| `bodyguard` | Clarified protection, liaison, route, close-protection, communications and shift-lead titles. |
| `royal_household` | Clarified household superintendent, equerry and wardrobe titles. |
| `royal_court` | All eight roles reviewed; established court titles, powers and reporting lines remain coherent. |
| `diplomatic_mission` | Clarified commercial attaché and mission-security titles. |
| `ministry` | Clarified policy, budget, inspection and regional-liaison offices. |
| `civil_service` | Clarified commission, recruitment, examination and ethics offices. |
| `political_party` | Clarified policy chair, campaign director and candidate-selection panel; panel modeled collectively. |
| `trade_union_federation` | Clarified bargaining, action-coordination, legal-advice and workplace-steward titles; removed judicial/military implications. |
| `corporation` | Clarified board, chief executive, operations, compliance, shareholder and workforce titles. |
| `chartered_company` | Clarified charter board, convoy command and local liaison titles. |
| `colonial_company` | Clarified company direction, contract law, survey, interpreting and charter oversight; jurist advises rather than adjudicates. |
| `estate_administration` | Clarified estate stewardship and works oversight titles. |
| `crime_family` | Clarified consigliere, crew leader and crime-family boss titles. |
| `street_gang` | Restored explicit gang structure and rival-crew intermediation; kept all seven roles. |
| `prison_gang` | Replaced the military quartermaster title for the shared-goods role and clarified mediation. |
| `spy_cell` | Replaced the assassin title for an infiltration role. |
| `revolutionary_party` | Clarified movement offices and modeled the secretariat collectively. |
| `sports_club` | Clarified team-captain, equipment-manager and medic titles. |
| `theatrical_troupe` | Clarified management, artistic direction, stage, performer and booking titles; repaired peer-level reporting. |
| `traveling_circus` | Clarified show, acts, touring, animal-care and supply titles. |
| `artisan_confraternity` | Clarified the craft-dispute adjudicator title and corrected its reporting level. |

## Validation

Parsed the edited JSON and checked that all 37 systems and 285 stable role IDs remain present; bilingual duties and importance values are valid; all reporting targets exist; and every reporting edge points to a strictly lower authority level. Confirmed that context-specific keys with supplied fallbacks do not collide with any world or fantasy theme title key. `git diff --check` passed for the edited data file.
