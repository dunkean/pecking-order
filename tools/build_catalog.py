"""Rebuild the bundled authored catalogue. No network, scraped text or sibling imports.

The small helpers below compose reusable functions into generic institutions. Cultural
bindings replace complete offices and cite narrowly scoped claims. Edit this source and
rebuild; the generated JSON is the distributable, independently readable knowledge base.
"""

import json
from pathlib import Path


def loc(en, fr):
    return {"labels": {"en": en, "fr": fr}}


def evidence(source=None, en="Authored worldbuilding model; not a historical claim.",
             fr="Modèle de worldbuilding conçu pour ce projet ; aucune affirmation historique."):
    return {"status": "source_supported" if source else "generic_model",
            "sources": [source] if source else [], "note": loc(en, fr)}


def title(en, fr, native=None, language=None, forms=None):
    return {"labels": {"en": en, "fr": fr}, "native": native, "language": language,
            "forms": forms or {}, "translation": "gloss" if native else "equivalent"}


def power(action, en, fr, basis="de_jure", source=None, limits=None):
    return {"action": action, "domain": "political", "basis": basis, "scope": loc(en, fr),
            "limits": loc(*(limits or (
                "Only within the organization's remit; external law and other offices may constrain it.",
                "Dans le champ de l’organisation ; le droit extérieur et les autres organes peuvent le limiter."
            ))), "evidence": evidence(source)}


def rule(rid, category, method, en, fr, source=None, **parameters):
    return {"id": rid, "category": category, "method": method, "description": loc(en, fr),
            "parameters": parameters, "evidence": evidence(source)}


def role(rid, function, en, fr, duty_en, duty_fr, action, collective=False, basis="de_jure"):
    return {"id": rid, "function": function, "label": loc(en, fr), "title": title(en, fr),
            "holder": "collective" if collective else "person", "min_holders": 0,
            "max_holders": 1, "duties": loc(duty_en, duty_fr),
            "powers": [power(action, duty_en, duty_fr, basis)], "rules": [],
            "title_evidence": evidence(), "rank": None}


# Roles are functions, not a universal ranking of human societies.
ROLE_ROWS = [
    ("head", "executive", "Leader", "Dirigeant", "Coordinate the institution and enact its decisions.", "Coordonner l’institution et mettre ses décisions en œuvre.", "execute"),
    ("sovereign", "sovereign", "Sovereign", "Souverain", "Exercise the polity's highest recognized office.", "Exercer la plus haute charge reconnue de l’entité politique.", "govern"),
    ("council", "governing_body", "Governing council", "Conseil dirigeant", "Deliberate and authorize collective decisions.", "Délibérer et autoriser les décisions collectives.", "deliberate", True),
    ("assembly", "assembly", "Members' assembly", "Assemblée des membres", "Express members' decisions under the institution's decision rules.", "Exprimer les décisions des membres selon les règles de l’institution.", "decide", True),
    ("elder", "customary_adviser", "Council of elders", "Conseil des anciens", "Advise and transmit customary knowledge.", "Conseiller et transmettre les connaissances coutumières.", "advise", True, "advisory"),
    ("deputy", "deputy", "Deputy", "Adjoint", "Act under an explicit delegation from the executive.", "Agir sur délégation explicite de l’exécutif.", "delegate"),
    ("steward", "administration", "Steward", "Intendant", "Administer assets and organize daily operations.", "Administrer les biens et organiser le fonctionnement quotidien.", "administer"),
    ("treasurer", "finance", "Treasurer", "Trésorier", "Keep accounts and disburse authorized funds.", "Tenir les comptes et verser les fonds autorisés.", "disburse"),
    ("scribe", "records", "Secretary", "Secrétaire", "Keep records and communicate authenticated decisions.", "Conserver les archives et communiquer les décisions authentifiées.", "record"),
    ("judge", "justice", "Adjudicator", "Juge", "Hear cases within a defined jurisdiction.", "Juger les affaires relevant d’une compétence définie.", "adjudicate"),
    ("mediator", "mediation", "Mediator", "Médiateur", "Help parties negotiate a settlement without assumed coercive authority.", "Aider les parties à négocier un accord sans pouvoir coercitif présumé.", "mediate", False, "advisory"),
    ("commander", "command", "Commander", "Commandant", "Direct operations and assign authorized missions.", "Diriger les opérations et assigner les missions autorisées.", "command"),
    ("staff", "planning", "Planning staff", "État-major", "Plan operations and coordinate specialist services.", "Planifier les opérations et coordonner les services spécialisés.", "plan", True, "advisory"),
    ("quartermaster", "logistics", "Quartermaster", "Responsable de la logistique", "Maintain supplies, equipment and transport.", "Gérer les approvisionnements, le matériel et le transport.", "supply"),
    ("veteran", "training", "Senior instructor", "Instructeur principal", "Train members and supervise standards of practice.", "Former les membres et superviser les normes de pratique.", "train"),
    ("members", "membership", "Members", "Membres", "Participate according to membership rights and obligations.", "Participer selon les droits et obligations d’appartenance.", "participate", True),
    ("practitioner", "practice", "Practitioners", "Praticiens", "Carry out the institution's specialist practice.", "Exercer la pratique spécialisée de l’institution.", "practice", True),
    ("novice", "training_member", "Novices", "Novices", "Learn and serve under supervision before full admission.", "Apprendre et servir sous supervision avant l’admission complète.", "learn", True),
    ("ritual", "ritual_authority", "Ritual custodian", "Responsable rituel", "Maintain ceremonies and sacred obligations.", "Préserver les cérémonies et les obligations sacrées.", "officiate", False, "ritual"),
    ("doctrine", "doctrinal_authority", "Doctrinal council", "Conseil doctrinal", "Interpret doctrine and establish teaching standards.", "Interpréter la doctrine et définir les normes d’enseignement.", "interpret", True),
    ("patron", "patronage", "Patron", "Protecteur", "Provide resources and access through a patronage relationship.", "Fournir des ressources et des accès par une relation de patronage.", "sponsor", False, "de_facto"),
    ("custodian", "lineage_custodian", "Lineage custodian", "Gardien de la lignée", "Preserve lineage continuity and recognition of eligible office holders.", "Préserver la continuité de la lignée et la reconnaissance des titulaires admissibles.", "recognize"),
    ("manager", "household_manager", "Estate manager", "Gestionnaire du patrimoine", "Manage the corporate household's shared estate and external affairs.", "Gérer le patrimoine commun de la maison et ses affaires extérieures.", "manage_estate"),
    ("coowners", "property_holders", "Joint property holders", "Codétenteurs du patrimoine", "Hold shared property claims subject to institutional rules.", "Détenir des droits patrimoniaux communs soumis aux règles de l’institution.", "hold_property", True),
    ("heir", "successor", "Designated successor", "Successeur désigné", "Prepare to assume an office; designation alone grants no current executive power.", "Se préparer à reprendre une charge ; la désignation seule ne confère aucun pouvoir exécutif actuel.", "prepare_succession", False, "advisory"),
    ("representatives", "representation", "Delegates", "Délégués", "Represent constituent groups under a defined mandate.", "Représenter les groupes constituants selon un mandat défini.", "represent", True),
    ("inspector", "oversight", "Inspector", "Inspecteur", "Review conduct and compliance without assuming executive command.", "Examiner les pratiques et la conformité sans commandement exécutif présumé.", "inspect"),
    ("master", "craft_authority", "Master", "Maître", "Oversee craft standards, admission and specialist training.", "Superviser les normes du métier, l’admission et la formation spécialisée.", "certify"),
    ("ambassador", "diplomatic_representation", "Envoy", "Émissaire", "Represent a principal in negotiations within a specified mandate.", "Représenter un mandant dans des négociations selon un mandat précis.", "negotiate"),
    ("broker", "exchange", "Broker", "Courtier", "Coordinate exchanges between participants.", "Coordonner les échanges entre participants.", "broker"),
    ("cell", "autonomous_unit", "Autonomous cells", "Cellules autonomes", "Act locally within agreed shared objectives.", "Agir localement selon des objectifs communs convenus.", "act_locally", True),
    ("oracle", "divination", "Oracle", "Oracle", "Interpret signs within the setting's stated cosmology.", "Interpréter les signes selon la cosmologie explicite de l’univers.", "divine", False, "ritual"),
    ("warden", "stewardship", "Warden", "Gardien", "Protect and maintain a shared resource or institutional trust.", "Protéger et entretenir une ressource commune ou un dépôt institutionnel.", "steward_resource"),
]
ROLES = {row[0]: role(*row) for row in ROLE_ROWS}
for rid in ("members", "practitioner", "novice", "coowners", "representatives", "cell"):
    ROLES[rid]["max_holders"] = None


# kind, domain, bilingual label, scales, roles, traits. Each is a reusable institution,
# never an ethnic stereotype. Scale describes reach, not headcount or a rank.
ROWS = [
    ("hereditary_monarchy", "political", "Hereditary monarchy", "Monarchie héréditaire", "polity regional", "sovereign council steward heir", "hereditary centralized"),
    ("elective_monarchy", "political", "Elective monarchy", "Monarchie élective", "polity imperial", "sovereign council representatives steward", "elective"),
    ("empire", "political", "Imperial polity", "Entité impériale", "imperial", "sovereign council steward commander representatives", "centralized composite"),
    ("traditional_kingship", "political", "Traditional kingship", "Royauté coutumière", "regional polity", "sovereign custodian council ritual", "customary"),
    ("chiefdom", "political", "Chiefdom", "Chefferie", "local district regional", "head elder ritual steward", "customary"),
    ("village_council", "political", "Customary village governance", "Gouvernance villageoise coutumière", "local", "head assembly mediator", "customary consultative"),
    ("city_republic", "political", "City republic", "République urbaine", "local polity", "council head assembly scribe", "collegial"),
    ("representative_republic", "political", "Representative republic", "République représentative", "polity regional", "head council representatives judge", "representative"),
    ("direct_assembly", "political", "Assembly polity", "Entité gouvernée par assemblée", "local polity", "assembly scribe mediator", "collegial direct"),
    ("oligarchy", "political", "Oligarchic government", "Gouvernement oligarchique", "local polity imperial", "council steward commander", "oligarchic"),
    ("military_regime", "political", "Military government", "Gouvernement militaire", "regional polity imperial", "commander staff steward inspector", "military authoritarian"),
    ("theocracy", "political", "Sacral government", "Gouvernement sacral", "polity imperial", "ritual doctrine steward judge", "sacral"),
    ("confederation", "political", "Confederation", "Confédération", "regional polity imperial transregional", "council representatives scribe mediator", "federative collegial"),
    ("federation", "political", "Federation", "Fédération", "polity imperial", "head council representatives judge", "federative"),
    ("segmentary_council", "political", "Segmentary lineage council", "Conseil de lignages segmentaires", "local regional", "elder representatives mediator", "segmentary customary"),
    ("age_grade_governance", "political", "Rotating age-grade government", "Gouvernement tournant par classes d’âge", "local regional polity", "head council assembly elder", "rotating age_grade"),
    ("diaspora_council", "civic", "Diaspora council", "Conseil de diaspora", "local transregional", "council representatives mediator treasurer", "diaspora"),
    ("province", "administrative", "Provincial administration", "Administration provinciale", "district regional", "head steward treasurer judge inspector", "delegated"),
    ("municipality", "administrative", "Municipality", "Municipalité", "local district", "head council scribe treasurer", "territorial"),
    ("palace_bureau", "administrative", "Palace bureau", "Bureau palatial", "local polity imperial", "steward scribe treasurer inspector", "bureaucratic"),
    ("tax_office", "administrative", "Revenue administration", "Administration fiscale", "district regional polity", "head treasurer scribe inspector", "bureaucratic fiscal"),
    ("border_administration", "administrative", "Frontier administration", "Administration frontalière", "district regional", "head commander broker scribe", "frontier delegated"),
    ("army", "military", "Army", "Armée", "regional polity imperial", "commander staff quartermaster inspector", "hierarchical"),
    ("army_corps", "military", "Army corps", "Corps d’armée", "regional polity", "commander staff quartermaster", "hierarchical formation"),
    ("division", "military", "Division", "Division", "regional polity", "commander staff quartermaster", "hierarchical formation"),
    ("brigade", "military", "Brigade", "Brigade", "district regional", "commander deputy quartermaster", "hierarchical formation"),
    ("regiment", "military", "Regiment or battalion", "Régiment ou bataillon", "district regional", "commander deputy veteran quartermaster members", "hierarchical unit"),
    ("company", "military", "Company", "Compagnie", "local district", "commander deputy veteran members", "hierarchical unit"),
    ("warband", "military", "Retinue or warband", "Suite armée ou bande guerrière", "local regional", "commander veteran patron members", "personal_loyalty"),
    ("militia", "military", "Militia", "Milice", "local district", "commander assembly quartermaster members", "territorial"),
    ("mercenary_company", "military", "Mercenary company", "Compagnie mercenaire", "district transregional", "commander council treasurer members", "contractual"),
    ("fleet", "military", "Fleet", "Flotte", "regional transregional", "commander staff quartermaster representatives", "naval hierarchical"),
    ("military_order", "military", "Military religious order", "Ordre militaire religieux", "regional transregional", "master council ritual treasurer novice", "vowed martial"),
    ("religious_hierarchy", "religious", "Religious hierarchy", "Hiérarchie religieuse", "polity transregional", "ritual doctrine steward representatives", "hierarchical sacral"),
    ("diocese", "religious", "Diocese", "Diocèse", "district regional", "ritual council steward treasurer", "territorial sacral"),
    ("parish", "religious", "Local religious community", "Communauté religieuse locale", "local", "ritual council treasurer members", "local sacral"),
    ("temple", "religious", "Temple institution", "Institution de temple", "local regional", "ritual steward treasurer practitioner novice", "sacral"),
    ("monastery", "religious", "Monastery", "Monastère", "local regional", "head council ritual steward novice members", "vowed corporate"),
    ("religious_order", "religious", "Religious order", "Ordre religieux", "regional transregional", "head council ritual representatives novice", "vowed network"),
    ("congregation", "religious", "Congregational community", "Communauté congrégationaliste", "local regional", "assembly ritual steward members", "collegial sacral"),
    ("initiatory_society", "religious", "Initiatory society", "Société initiatique", "local regional", "master council ritual novice", "initiatory"),
    ("shrine_network", "religious", "Shrine network", "Réseau de sanctuaires", "regional transregional", "representatives ritual warden members", "network sacral"),
    ("craft_guild", "economic", "Craft guild", "Guilde artisanale", "local regional", "master council treasurer practitioner novice", "corporate craft"),
    ("merchant_guild", "economic", "Merchant guild", "Guilde marchande", "local transregional", "head council broker treasurer members", "corporate commercial"),
    ("workshop", "economic", "Corporate workshop", "Atelier organisé", "local", "master steward practitioner novice", "craft"),
    ("trade_company", "economic", "Trading company", "Compagnie commerciale", "regional transregional", "council head broker treasurer representatives", "corporate commercial"),
    ("cooperative", "economic", "Cooperative", "Coopérative", "local regional", "assembly head treasurer inspector members", "cooperative"),
    ("irrigation_association", "economic", "Irrigation association", "Association d’irrigation", "local district", "assembly warden ritual members", "commons water"),
    ("commons_association", "economic", "Commons association", "Association de gestion des communs", "local regional", "assembly warden mediator members", "commons"),
    ("caravan", "economic", "Caravan organization", "Organisation caravanière", "regional transregional", "head quartermaster broker commander members", "mobile commercial"),
    ("market_authority", "economic", "Market authority", "Autorité du marché", "local district", "head inspector judge scribe", "commercial regulatory"),
    ("bank", "economic", "Banking house", "Maison bancaire", "local transregional", "head council treasurer scribe inspector", "financial corporate"),
    ("labor_union", "economic", "Labor union", "Syndicat professionnel", "local transregional", "assembly representatives head treasurer", "representative labor"),
    ("corporate_household", "kinship", "Corporate joint household", "Famille indivise à patrimoine commun", "household local", "manager coowners custodian members", "corporate shared_estate"),
    ("lineage", "kinship", "Corporate lineage", "Lignage organisé", "local regional", "custodian elder representatives members", "descent corporate"),
    ("clan", "kinship", "Clan institution", "Institution clanique", "local regional transregional", "custodian representatives ritual members", "descent"),
    ("noble_house", "kinship", "Noble house", "Maison noble", "household regional polity", "head custodian steward heir members", "dynastic corporate"),
    ("royal_dynasty", "kinship", "Royal dynasty", "Dynastie royale", "polity imperial", "custodian council heir members", "dynastic"),
    ("matrilineal_house", "kinship", "Matrilineal corporate house", "Maison matrilinéaire organisée", "household local", "custodian manager elder coowners", "matrilineal corporate"),
    ("adoptive_house", "kinship", "Adoptive corporate house", "Maison organisée par adoption", "household local", "head custodian steward heir", "adoptive corporate"),
    ("marriage_alliance", "kinship", "Inter-house alliance", "Alliance entre maisons", "local regional", "representatives mediator custodian", "affinal network"),
    ("court", "judicial", "Court of justice", "Cour de justice", "local regional polity", "judge scribe inspector members", "judicial"),
    ("customary_tribunal", "judicial", "Customary tribunal", "Tribunal coutumier", "local district", "elder judge mediator scribe", "customary judicial"),
    ("arbitration_body", "judicial", "Arbitration body", "Instance d’arbitrage", "local transregional", "council mediator scribe", "contractual judicial"),
    ("legal_college", "judicial", "College of jurists", "Collège de juristes", "regional transregional", "council master practitioner novice", "collegial scholarly"),
    ("university", "educational", "University corporation", "Corporation universitaire", "local transregional", "head council master representatives novice", "corporate scholarly"),
    ("academy", "educational", "Academy", "Académie", "local transregional", "council head practitioner novice", "collegial scholarly"),
    ("school", "educational", "Institutional school", "École organisée", "local regional", "head master practitioner novice", "scholarly"),
    ("library", "educational", "Library institution", "Institution de bibliothèque", "local regional", "warden scribe practitioner members", "scholarly custodial"),
    ("neighborhood_association", "civic", "Neighborhood association", "Association de quartier", "local", "assembly representatives mediator treasurer", "territorial voluntary"),
    ("fraternity", "civic", "Mutual-aid fraternity", "Confrérie d’entraide", "local regional", "head council treasurer members novice", "mutual_aid"),
    ("age_set", "civic", "Age-set association", "Association de classe d’âge", "local regional", "council veteran members", "age_grade"),
    ("hospital", "civic", "Hospital foundation", "Fondation hospitalière", "local regional", "head steward practitioner treasurer patron", "care charitable"),
    ("festival_society", "civic", "Festival society", "Société de fête", "local regional", "head ritual treasurer members", "ritual voluntary"),
    ("criminal_syndicate", "clandestine", "Criminal syndicate", "Syndicat criminel", "local transregional", "head deputy broker treasurer cell", "clandestine hierarchical"),
    ("secret_society", "clandestine", "Secret society", "Société secrète", "local transregional", "council master ritual novice cell", "clandestine initiatory"),
    ("insurgent_network", "clandestine", "Insurgent network", "Réseau insurgé", "regional transregional", "council cell broker quartermaster", "clandestine network"),
    ("patronage_network", "clandestine", "Patronage network", "Réseau de clientèle", "local transregional", "patron broker members", "informal personal_loyalty"),
    ("embassy", "diplomatic", "Diplomatic mission", "Mission diplomatique", "polity transregional", "ambassador scribe steward members", "delegated diplomatic"),
    ("interstate_league", "diplomatic", "Interstate league", "Ligue entre États", "transregional", "council representatives mediator scribe", "federative diplomatic"),
    ("treaty_commission", "diplomatic", "Treaty commission", "Commission de traité", "regional transregional", "representatives inspector scribe mediator", "diplomatic oversight"),
    ("mage_college", "fantastic", "College of magic", "Collège de magie", "local transregional", "council master practitioner novice inspector", "magical scholarly"),
    ("adventurers_guild", "fantastic", "Adventurers' guild", "Guilde d’aventuriers", "local transregional", "head council broker treasurer members", "contractual adventurous"),
    ("hive_collective", "fantastic", "Hive collective", "Collectif de ruche", "local imperial", "council cell members", "nonhuman collective"),
    ("spirit_court", "fantastic", "Spirit court", "Cour des esprits", "local transregional", "sovereign council oracle ambassador", "nonhuman sacral"),
]


def edge(source, target, kind, sid=None):
    return {"source": source, "target": target, "kind": kind, "evidence": evidence(sid)}


templates = []
for kind, domain, en, fr, scales, roles, traits in ROWS:
    role_ids = roles.split()
    offices = [json.loads(json.dumps(ROLES[rid])) for rid in role_ids]
    for office in offices:
        for ability in office["powers"]:
            ability["domain"] = domain
        if domain == "clandestine":
            for ability in office["powers"]:
                if ability["basis"] == "de_jure":
                    ability["basis"] = "de_facto"
    relations = []
    executive = next((rid for rid in ("sovereign", "head", "commander", "manager", "master")
                      if rid in role_ids), None)
    if executive and "council" in role_ids:
        relations.append(edge("council", executive, "checks"))
    if executive:
        for rid in ("steward", "treasurer", "scribe", "quartermaster", "deputy", "staff"):
            if rid in role_ids:
                relations.append(edge(rid, executive, "reports_to"))
        if "elder" in role_ids:
            relations.append(edge("elder", executive, "advises"))
    if "assembly" in role_ids and executive:
        relations.append(edge("assembly", executive, "checks"))
    if "novice" in role_ids and "master" in role_ids:
        relations.append(edge("novice", "master", "reports_to"))
    rules = [rule("office_vacancy", "vacancy", "unfilled_slots",
                  "Slots may be vacant; this blueprint does not create or assign people.",
                  "Les charges peuvent être vacantes ; ce modèle ne crée ni n’affecte de personnes.")]
    if "hereditary" in traits.split():
        rules.append(rule("dynastic_eligibility", "succession", "dynastic_selection",
                          "Choose from the eligible dynasty; the precise descent and selection rules must be supplied.",
                          "Choisir dans la dynastie admissible ; les règles de filiation et de sélection restent à préciser."))
    if "elective" in traits.split():
        rules.append(rule("elective_succession", "succession", "election",
                          "The designated electoral body selects the sovereign.",
                          "Le corps électoral désigné choisit le souverain."))
    if "matrilineal" in traits.split():
        rules.append(rule("maternal_descent", "membership", "maternal_line",
                          "Corporate membership follows maternal descent; this does not imply rule by women.",
                          "L’appartenance suit la filiation maternelle ; cela n’implique pas un gouvernement féminin."))
    if "cooperative" in traits.split():
        rules.append(rule("cooperative_vote", "decision", "member_vote",
                          "Voting rights belong to members under an explicit cooperative charter.",
                          "Les membres disposent des droits de vote définis par la charte coopérative."))
    if "shared_estate" in traits.split():
        rules.append(rule("shared_estate", "inheritance", "corporate_property",
                          "Track common assets separately from individual assets; partition requires a specified rule.",
                          "Distinguer les biens communs des biens individuels ; le partage nécessite une règle précise."))
    if kind == "hereditary_monarchy":
        offices[0]["title"] = title("King", "Roi", forms={
            "en": {"feminine": "Queen", "plural": "Monarchs"},
            "fr": {"feminine": "Reine", "plural": "Monarques"}})
    if kind == "empire":
        offices[0]["title"] = title("Emperor", "Empereur", forms={
            "en": {"feminine": "Empress"}, "fr": {"feminine": "Impératrice"}})
    units = []
    children = {"army": "army_corps", "army_corps": "division", "division": "brigade",
                "brigade": "regiment", "regiment": "company", "religious_hierarchy": "diocese",
                "diocese": "parish", "religious_order": "monastery", "empire": "province",
                "noble_house": "corporate_household"}
    if kind in children:
        units.append({"kind": children[kind], "relation": "contains", "min_count": 0,
                      "max_count": None, "note": loc(
                          "Optional model decomposition; actual historical units vary.",
                          "Décomposition facultative du modèle ; les unités historiques varient.")})
    templates.append({"id": kind, "domain": domain, "label": loc(en, fr),
                      "description": loc(
                          f"Reusable {en.lower()} blueprint; offices describe functions and may be combined or vacant.",
                          f"Modèle réutilisable : {fr.lower()} ; les charges décrivent des fonctions cumulables ou vacantes."),
                      "scales": scales.split(), "traits": traits.split(), "roles": offices,
                      "relations": relations, "units": units, "rules": rules,
                      "evidence": evidence()})


def source(sid, name, publisher, url, locator, supports_en, supports_fr):
    return {"id": sid, "title": name, "publisher": publisher, "url": url,
            "accessed": "2026-10-21", "locator": locator,
            "supports": loc(supports_en, supports_fr), "limitations": loc(
                "Supports only the named claims. Other blueprint fields remain authored models; this is not a complete institutional history.",
                "Étaye uniquement les affirmations nommées. Les autres champs restent des modèles conçus ; ce n’est pas une histoire institutionnelle complète.")}


sources = [
    source("india_vijayanagara", "History of Vijayanagara", "Vijayanagara District, Government of India",
           "https://vijayanagara.nic.in/en/about-district/", "History; rulers named Raya",
           "Vijayanagara political context and attested Raya names.", "Contexte de Vijayanagara et noms de souverains portant Raya."),
    source("met_deccan", "Sultans of Deccan India: Exhibition Galleries", "The Metropolitan Museum of Art",
           "https://www.metmuseum.org/exhibitions/listings/2015/deccan-sultans/exhibition-galleries", "Introduction; five Deccan sultanates",
           "Deccan sultanates and Muslim courtly context; the title sultan.", "Sultanats du Deccan, contexte des cours musulmanes et titre de sultan."),
    source("india_huf", "Section 278C: Offences by Hindu undivided families", "Income Tax Department, Government of India",
           "https://www.incometaxindia.gov.in/w/section-278c-52", "Section 278C(1)-(2)",
           "The term karta and representation of a Hindu undivided family in this statutory provision.",
           "Le terme karta et la représentation d’une famille hindoue indivise dans cette disposition."),
    source("botswana_bogosi", "Bathopele, 7 of 2026", "Government of Botswana",
           "https://www.gov.bw/sites/default/files/2026-06/Bathopele-7-of-2026.pdf", "Page 13; Bogosi and kgotla functions",
           "Dikgosi, customary justice, convening kgotla meetings and community consultation.",
           "Dikgosi, justice coutumière, convocation du kgotla et consultation communautaire."),
    source("unesco_gadaa", "Gada system of the Oromo", "UNESCO Intangible Cultural Heritage",
           "https://ich.unesco.org/en/RL/gadaa-system-an-indigenous-democratic-socio-political-system-of-the-oromo-people-01164", "Description; rotation and classes",
           "Ruling class with chairperson, officials and assembly; rotation every eight years.",
           "Classe dirigeante avec président, responsables et assemblée ; rotation tous les huit ans."),
    source("manhyia", "The Seat of the Asantehene", "Manhyia Palace",
           "https://manhyiapalace.org/", "The Royal Family; Golden Stool and royal lineage",
           "Asantehene and Asantehemaa titles; stewardship of the Golden Stool and royal lineage.",
           "Titres Asantehene et Asantehemaa ; garde du Tabouret d’or et de la lignée royale."),
    source("haudenosaunee", "Government", "Haudenosaunee Confederacy",
           "https://www.haudenosauneeconfederacy.com/government/", "Grand Council; Chiefs; Clan Mothers",
           "Fifty Grand Council chiefs; clan mothers select and can remove chiefs; titles Hoyaneh and Iakoiane.",
           "Cinquante chefs au Grand Conseil ; sélection et révocation des chefs par les mères de clan ; titres Hoyaneh et Iakoiane."),
    source("unesco_subak", "Cultural Landscape of Bali Province", "UNESCO World Heritage Centre",
           "https://whc.unesco.org/en/list/1194", "Brief synthesis; cooperative water management",
           "Subak cooperative irrigation and water-temple context; democratic and egalitarian practices.",
           "Irrigation coopérative subak, temples de l’eau et pratiques démocratiques et égalitaires."),
    source("british_army", "Rank Structure", "The British Army",
           "https://www.army.mod.uk/learn-and-explore/ranks/", "Lieutenant General; Major General; Lieutenant Colonel; Major; Captain; WO1",
           "Typical corps, division, battalion and company commands; distinction between appointment and rank.",
           "Commandement habituel des corps, divisions, bataillons et compagnies ; distinction entre fonction et grade."),
    source("livery", "Livery Roles", "Livery Committee, City of London",
           "https://liverycommittee.org/about/livery-companies-and-guilds/livery-roles/", "Court of Assistants; Role of the Clerk; Master",
           "Master, Wardens, Court of Assistants and Clerk; annual election of the Master.",
           "Master, Wardens, Court of Assistants et Clerk ; élection annuelle du Master."),
    source("vatican_diocese", "Code of Canon Law, canons 460–572", "Holy See",
           "https://www.vatican.va/archive/cod-iuris-canonici/eng/documents/cic_lib2-cann460-572_en.html", "Canons 495-500, 515, 519, 532, 537",
           "Presbyteral council assists the bishop; pastor and parish finance council roles.",
           "Conseil presbytéral assistant l’évêque ; fonctions du curé et du conseil pour les affaires économiques paroissiales."),
    source("met_edo", "Japan, 1600–1800 A.D.", "The Metropolitan Museum of Art",
           "https://www.metmuseum.org/toah/ht/09/eaj.html", "Overview; imperial court, shogunate and daimyo",
           "Nominal imperial authority alongside shogunal political power and daimyo domains.",
           "Autorité impériale nominale, pouvoir politique du shogunat et domaines des daimyo."),
]


def cultural_role(base, en, fr, sid, native=None, language=None, duties=None,
                  supported_powers=False, rules=None):
    office = json.loads(json.dumps(ROLES[base]))
    office["title"] = title(en, fr, native, language)
    office["title_evidence"] = evidence(sid)
    if duties:
        office["duties"] = loc(*duties)
        office["powers"] = [power(office["powers"][0]["action"], *duties,
                                  office["powers"][0]["basis"],
                                  source=sid if supported_powers else None)]
    if rules:
        office["rules"] = rules
    return office


def binding(kind, offices, sid, *, remove=(), relations=(), replace=False, rules=(), traits=()):
    domain = next(row[1] for row in ROWS if row[0] == kind)
    for office in offices:
        for ability in office["powers"]:
            ability["domain"] = domain
    return {"template": kind, "roles": offices, "remove_roles": list(remove),
            "relations": list(relations), "replace_relations": replace, "rules": list(rules),
            "traits": list(traits), "evidence": evidence(sid,
                "Cultural binding: only individually cited claims are source-supported; generic offices remain explicit.",
                "Déclinaison culturelle : seules les affirmations citées individuellement sont étayées ; les charges génériques restent explicites.")}


def culture(cid, en, fr, aliases, region_en, region_fr, period, bindings, description=None):
    return {"id": cid, "label": loc(en, fr), "aliases": aliases,
            "region": loc(region_en, region_fr), "period": period,
            "description": loc(*(description or (
                "A bounded reference profile; not a universal description of a people or religion.",
                "Profil de référence délimité ; aucune description universelle d’un peuple ou d’une religion."))),
            "bindings": bindings}


cultures = []
cultures.append(culture("vijayanagara_krishnadevaraya", "Vijayanagara court, 1509–1529",
                        "Cour de Vijayanagara, 1509–1529", ["vijayanagara", "vijayanagar"],
                        "Southern India", "Inde du Sud", [1509, 1529], [
    binding(kind, [cultural_role("sovereign", "Raya (king)", "Raya (roi)",
                                 "india_vijayanagara", "Rāya", "te")], "india_vijayanagara")
    for kind in ("hereditary_monarchy", "empire")]))
cultures.append(culture("deccan_sultanates", "Deccan sultanate courts, 1500–1687",
                        "Cours des sultanats du Deccan, 1500–1687", ["deccan", "deccan sultanate"],
                        "Deccan, India", "Deccan, Inde", [1500, 1687], [
    binding("hereditary_monarchy", [cultural_role("sovereign", "Sultan", "Sultan", "met_deccan",
                                                   "سلطان", "fa")], "met_deccan")]))
cultures.append(culture("hindu_joint_family_india", "Hindu undivided family, Indian statutory context",
                        "Famille hindoue indivise, contexte statutaire indien", ["huf", "hindu joint family", "famille hindoue indivise"],
                        "India", "Inde", [2025, 2026], [binding("corporate_household", [
    cultural_role("manager", "Karta (family manager)", "Karta (gestionnaire familial)", "india_huf",
                  "कर्ता", "hi", duties=(
                      "Represent the HUF in the cited statutory context; broader estate-management rules need separate legal-school and period research.",
                      "Représenter la famille indivise dans le contexte statutaire cité ; les règles patrimoniales plus larges nécessitent une étude de l’école juridique et de l’époque."),
                  supported_powers=True)], "india_huf")], description=(
                      "A corporate property institution, not a model of every Hindu family. No sex-based eligibility or inheritance law is inferred.",
                      "Institution patrimoniale, pas un modèle de toute famille hindoue. Aucune règle de sexe ou de succession n’est déduite.")))
cultures.append(culture("tswana_bogosi_contemporary", "Tswana bogosi, Botswana reference context",
                        "Bogosi tswana, contexte de référence au Botswana", ["tswana", "batswana", "bogosi"],
                        "Botswana", "Botswana", [2025, 2026], [binding("village_council", [
    cultural_role("head", "Kgosi (chief)", "Kgosi (chef coutumier)", "botswana_bogosi", "Kgosi", "tn",
                  duties=("Convene kgotla meetings and perform recognized customary leadership functions.",
                          "Convoquer le kgotla et exercer les fonctions reconnues de direction coutumière."),
                  supported_powers=True),
    cultural_role("assembly", "Kgotla (community forum)", "Kgotla (assemblée communautaire)",
                  "botswana_bogosi", "Kgotla", "tn",
                  duties=("Provide a forum for community consultation and customary dispute hearing.",
                          "Offrir un lieu de consultation communautaire et d’examen des différends coutumiers."),
                  supported_powers=True)], "botswana_bogosi")]))
cultures.append(culture("oromo_gadaa_reference", "Oromo Gadaa, UNESCO reference description",
                        "Gadaa oromo, description de référence UNESCO", ["oromo", "gadaa", "gada"],
                        "Ethiopia", "Éthiopie", [2016, 2026], [binding("age_grade_governance", [
    cultural_role("head", "Chairperson", "Président", "unesco_gadaa",
                  duties=("Chair the ruling class alongside officials and an assembly.",
                          "Présider la classe dirigeante aux côtés des responsables et d’une assemblée."),
                  supported_powers=True),
    cultural_role("assembly", "Assembly", "Assemblée", "unesco_gadaa")], "unesco_gadaa", rules=[
    rule("eight_year_rotation", "tenure", "rotation", "Leadership rotates every eight years.",
         "La direction change tous les huit ans.", "unesco_gadaa", years=8),
    rule("class_membership", "membership", "paternal_class",
         "The UNESCO description records male class membership following fathers; women's consultation is described separately.",
         "La description UNESCO indique l’appartenance masculine suivant les pères ; la consultation des femmes y est décrite séparément.", "unesco_gadaa")])]))
cultures.append(culture("asante_traditional_contemporary", "Asante traditional royal institution",
                        "Institution royale coutumière asante", ["asante", "ashanti"],
                        "Ghana", "Ghana", [2026, 2026], [binding("traditional_kingship", [
    cultural_role("sovereign", "Asantehene (Asante king)", "Asantehene (roi asante)", "manhyia",
                  "Asantehene", "ak", duties=("Hold the Golden Stool in trust.", "Garder le Tabouret d’or en dépôt."),
                  supported_powers=True),
    cultural_role("custodian", "Asantehemaa (queen mother)", "Asantehemaa (reine mère)", "manhyia",
                  "Asantehemaa", "ak", duties=("Act as custodian of the royal lineage.", "Veiller sur la lignée royale."),
                  supported_powers=True)], "manhyia")]))
chief = cultural_role("representatives", "Hoyaneh (chiefs)", "Hoyaneh (chefs)", "haudenosaunee", "Hoyaneh", "und",
                       duties=("Represent clans in the Grand Council and serve their communities.",
                               "Représenter les clans au Grand Conseil et servir les communautés."), supported_powers=True)
chief["holder"] = "person"
chief["max_holders"] = 50
mother = cultural_role("custodian", "Clan mother", "Mère de clan", "haudenosaunee", "Iakoiane", "und",
                       duties=("Select and, after warnings, remove a clan chief under the stated procedures.",
                               "Choisir et, après avertissements, révoquer le chef de clan selon les procédures décrites."), supported_powers=True)
mother["holder"] = "person"
mother["max_holders"] = 49
mother["rules"] = [rule("tadodaho_exception", "selection", "exception",
                       "The Tadodaho has no clan mother; Onondaga chiefs select the candidate, considering clan mothers' advice.",
                       "Le Tadodaho n’a pas de mère de clan ; les chefs onondaga choisissent le candidat en tenant compte de l’avis des mères de clan.",
                       "haudenosaunee", except_office="tadodaho")]
grand = cultural_role("council", "Grand Council", "Grand Conseil", "haudenosaunee",
                      duties=("Resolve shared matters through the Confederacy's council procedures.",
                              "Traiter les affaires communes selon les procédures du Conseil de la Confédération."), supported_powers=True)
grand["rules"] = [rule("grand_council_seats", "membership", "fixed_seats",
                      "The Grand Council has fifty chiefly seats; vacancies are possible.",
                      "Le Grand Conseil compte cinquante sièges de chef ; des vacances sont possibles.",
                      "haudenosaunee", seats=50)]
cultures.append(culture("haudenosaunee_confederacy_reference", "Haudenosaunee Confederacy, self-description",
                        "Confédération haudenosaunee, description propre", ["haudenosaunee"],
                        "Northeastern North America", "Nord-est de l’Amérique du Nord", [2026, 2026], [
    binding("confederation", [grand, chief, mother], "haudenosaunee", remove=["scribe", "mediator"],
            replace=True, relations=[edge("representatives", "council", "member_of", "haudenosaunee"),
                                     edge("custodian", "representatives", "appoints", "haudenosaunee"),
                                     edge("custodian", "representatives", "removes", "haudenosaunee")])]))
cultures.append(culture("balinese_subak_reference", "Balinese subak cooperative context",
                        "Contexte coopératif subak balinais", ["balinese subak", "subak", "subak balinais"],
                        "Bali, Indonesia", "Bali, Indonésie", [2012, 2026], [binding("irrigation_association", [
    cultural_role("assembly", "Farmers' assembly", "Assemblée des cultivateurs", "unesco_subak",
                  duties=("Make cooperative decisions concerning irrigation and cultivation.",
                          "Décider collectivement de l’irrigation et de la culture."), supported_powers=True)
], "unesco_subak")]))
army_bindings = []
for kind, rank_en, rank_fr in [("army_corps", "Lieutenant General", "Lieutenant-général"),
                               ("division", "Major General", "Major-général"),
                               ("brigade", "Brigadier", "Brigadier"),
                               ("regiment", "Lieutenant Colonel", "Lieutenant-colonel"),
                               ("company", "Major", "Major")]:
    commander = cultural_role("commander", "Commanding officer", "Officier commandant", "british_army",
                               duties=("Command this formation or unit in the typical appointment described by the British Army.",
                                       "Commander cette formation ou unité selon l’affectation habituelle décrite par la British Army."),
                               supported_powers=True)
    commander["rank"] = title(rank_en, rank_fr)
    offices = [commander]
    if kind == "company":
        deputy = cultural_role("deputy", "Second-in-command", "Commandant en second", "british_army")
        deputy["rank"] = title("Captain", "Capitaine")
        offices.append(deputy)
    army_bindings.append(binding(kind, offices, "british_army"))
cultures.append(culture("british_army_contemporary", "British Army, typical contemporary appointments",
                        "British Army, affectations contemporaines habituelles", ["british army", "armée britannique"],
                        "United Kingdom", "Royaume-Uni", [2026, 2026], army_bindings,
                        description=("Ranks are kept separate from offices. French names are glosses, not assertions of French-Army equivalence.",
                                     "Les grades sont séparés des fonctions. Les noms français sont des traductions, pas des équivalences avec l’armée française.")))
master = cultural_role("master", "Master", "Maître de la compagnie", "livery", "Master", "en",
                       duties=("Chair the Court of Assistants.", "Présider la Court of Assistants."), supported_powers=True,
                       rules=[rule("annual_master", "tenure", "annual_election", "The Master is elected annually.",
                                   "Le Master est élu annuellement.", "livery", years=1)])
court = cultural_role("council", "Court of Assistants", "Conseil des assistants", "livery", "Court of Assistants", "en",
                      duties=("Manage the Company as its governing body.", "Gérer la compagnie en tant qu’organe dirigeant."), supported_powers=True)
clerk = cultural_role("scribe", "Clerk", "Secrétaire de la compagnie", "livery", "Clerk", "en")
wardens = cultural_role("deputy", "Wardens", "Gardes de la compagnie", "livery", "Wardens", "en")
wardens["max_holders"] = None
cultures.append(culture("london_livery_reference", "London livery company, general reference model",
                        "Compagnie de livrée londonienne, modèle de référence", ["london livery", "livery"],
                        "City of London", "Cité de Londres", [2026, 2026], [binding("craft_guild", [master, court, clerk, wardens], "livery",
    remove=["treasurer", "practitioner", "novice"], replace=True,
    relations=[edge("master", "council", "member_of", "livery"), edge("deputy", "council", "member_of", "livery")])],
    description=("A contemporary livery model; do not project its offices onto every medieval craft guild. Company-specific titles vary.",
                 "Modèle contemporain de livrée ; ne pas le projeter sur toute guilde médiévale. Les titres varient selon la compagnie.")))
vatican_bindings = []
bishop = cultural_role("ritual", "Bishop", "Évêque", "vatican_diocese")
council = cultural_role("council", "Presbyteral council", "Conseil presbytéral", "vatican_diocese",
                        duties=("Assist the bishop in governing the diocese; its vote is consultative except as provided by law.",
                                "Assister l’évêque dans le gouvernement du diocèse ; sa voix est consultative sauf disposition légale."),
                        supported_powers=True)
council["powers"][0]["basis"] = "advisory"
vatican_bindings.append(binding("diocese", [bishop, council], "vatican_diocese", replace=True,
                                relations=[edge("council", "ritual", "advises", "vatican_diocese")]))
pastor = cultural_role("ritual", "Pastor (parish priest)", "Curé", "vatican_diocese",
                       duties=("Exercise parish pastoral care under the diocesan bishop and represent the parish in juridic affairs.",
                               "Exercer la charge pastorale sous l’autorité de l’évêque diocésain et représenter la paroisse dans les affaires juridiques."),
                       supported_powers=True)
finance = cultural_role("council", "Parish finance council", "Conseil pour les affaires économiques", "vatican_diocese",
                        duties=("Assist the pastor in administering parish goods.", "Assister le curé dans l’administration des biens paroissiaux."), supported_powers=True)
finance["powers"][0]["basis"] = "advisory"
vatican_bindings.append(binding("parish", [pastor, finance], "vatican_diocese", replace=True,
                                relations=[edge("council", "ritual", "advises", "vatican_diocese")]))
cultures.append(culture("latin_catholic_canonical", "Latin Catholic canonical institutions",
                        "Institutions canoniques catholiques latines", ["latin catholic", "catholique latin"],
                        "Transregional, Latin Church", "Transrégional, Église latine", [1983, 2026], vatican_bindings))
emperor = cultural_role("sovereign", "Emperor", "Empereur", "met_edo", "天皇", "ja",
                        duties=("Hold nominal imperial authority in the referenced Edo-period account.",
                                "Détenir l’autorité impériale nominale dans la description de l’époque Edo citée."), supported_powers=True)
shogun = cultural_role("head", "Shogun", "Shogun", "met_edo", "将軍", "ja",
                       duties=("Exercise the shogunate's effective political power.", "Exercer le pouvoir politique effectif du shogunat."), supported_powers=True)
shogun["powers"][0]["basis"] = "de_facto"
daimyo = cultural_role("representatives", "Daimyo (domain lords)", "Daimyo (seigneurs de domaines)", "met_edo", "大名", "ja",
                       duties=("Govern domains while owing fealty to the shogun.", "Gouverner les domaines tout en devant fidélité au shogun."), supported_powers=True)
daimyo["holder"] = "person"
cultures.append(culture("japan_edo_reference", "Edo Japan, 1600–1800 reference context",
                        "Japon d’Edo, contexte de référence 1600–1800", ["edo japan", "tokugawa", "japon edo"],
                        "Japan", "Japon", [1600, 1800], [binding("empire", [emperor, shogun, daimyo], "met_edo",
                        remove=["council", "steward", "commander"], replace=True,
                        relations=[edge("representatives", "head", "reports_to", "met_edo")])]))

catalog = {"version": "0.1.0", "templates": templates, "cultures": cultures, "sources": sources,
           "broad_aliases": {
               "hindu": ["vijayanagara_krishnadevaraya", "hindu_joint_family_india", "balinese_subak_reference"],
               "hindou": ["vijayanagara_krishnadevaraya", "hindu_joint_family_india", "balinese_subak_reference"],
               "indian": ["vijayanagara_krishnadevaraya", "deccan_sultanates", "hindu_joint_family_india"],
               "indien": ["vijayanagara_krishnadevaraya", "deccan_sultanates", "hindu_joint_family_india"],
               "african": ["tswana_bogosi_contemporary", "oromo_gadaa_reference", "asante_traditional_contemporary"],
               "africain": ["tswana_bogosi_contemporary", "oromo_gadaa_reference", "asante_traditional_contemporary"],
               "christian": ["latin_catholic_canonical"], "chrétien": ["latin_catholic_canonical"],
               "japanese": ["japan_edo_reference"], "japonais": ["japan_edo_reference"],
           }}


def main():
    root = Path(__file__).resolve().parents[1]
    target = root / "src/pecking_order/data/catalog.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(templates)} generic templates and {len(cultures)} cultural profiles")


if __name__ == "__main__":
    main()
