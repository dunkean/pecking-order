"""Derive coverage and narrow source attribution from the actual distributable pack."""

import json
from pathlib import Path

from pecking_order import KnowledgeBase

root = Path(__file__).resolve().parents[1]
kb = KnowledgeBase()
coverage = kb.catalog()["coverage"]
lines = [
    "# Couverture / Coverage", "",
    "Document généré depuis le catalogue distribué avec `python tools/export_docs.py`.", "",
    (f"**{coverage['generic_templates']} modèles génériques / generic blueprints**, "
    f"**{coverage['cultural_profiles']} profils / profiles**, "
    f"**{coverage['cultural_bindings']} déclinaisons / bindings**, "
    f"**{coverage['sources']} sources**."), "",
    "La couverture des types est large. La couverture historique est initiale et partielle.",
    "Broad institution coverage; initial, partial historical coverage.", "",
    "Un modèle générique est une proposition de worldbuilding, pas une affirmation universelle.",
    "A generic model is an authored worldbuilding proposal, not a universal historical claim.", "",
    "## Modèles réutilisables / Reusable blueprints", "",
    "| ID | Français | English | Domaine / Domain | Échelles / Scales |",
    "|---|---|---|---|---|",
]
for template in kb.data.templates:
    lines.append(f"| `{template.id}` | {template.label.labels['fr']} | "
                 f"{template.label.labels['en']} | {template.domain} | {', '.join(template.scales)} |")
lines += ["", "## Profils documentés / Documented profiles", "",
          "| ID | Contexte / Context | Période / Period | Déclinaisons / Bindings |",
          "|---|---|---|---|"]
for culture in kb.data.cultures:
    lines.append(f"| `{culture.id}` | {culture.label.labels['fr']} / {culture.label.labels['en']} | "
                 f"{culture.period[0]}–{culture.period[1]} | "
                 f"{', '.join('`' + b.template + '`' for b in culture.bindings)} |")
lines += ["", "## Axes de recherche encore ouverts / Further research", "",
          ("Les éléments ci-dessous sont des pistes, pas des données disponibles ni des promesses "
          "d’authenticité. / These are research directions, not available data or claims of authenticity."), "",
          ("- Cours et administrations impériales : traditions chinoises, ottomanes, romaines, "
          "byzantines, persanes et mésoaméricaines, par époque et juridiction."),
          ("- Chefferies, royautés et systèmes sans pouvoir central : profils locaux supplémentaires "
          "en Afrique, Océanie, Asie et dans les Amériques."),
          ("- Institutions religieuses : traditions musulmanes, juives, bouddhiques, hindoues, "
          "chrétiennes orientales et traditions locales, avec leurs propres distinctions."),
          ("- Institutions de métier : corporations historiques hors du modèle londonien contemporain, "
          "guildes marchandes, marchés, compagnies et associations de ressources."),
          ("- Parenté corporative : maisons japonaises, lignages chinois, maisons et clans "
          "matrilinéaires, variantes de la famille indivise selon lieu, école et période."),
          ("- Armées : chaînes de commandement anciennes et modernes, formations navales, "
          "grades, charges, milices, suites et unités irrégulières."),
          ("- Traductions supplémentaires, variantes régionales, titulatures complètes et formules "
          "d’adresse documentées."), "",
          ("Une absence de déclinaison renvoie `unsupported` en mode historique. Les limites "
          "de chaque profil figurent dans les données et dans les sources."), ""]
(root / "docs/coverage.md").write_text("\n".join(lines), encoding="utf-8")

provenance = [
    "# Provenance", "",
    "## Design source / Source de conception", "",
    ("The user-owned `ttrpg_content_generator/worldbuilder_social_engine_study.md` was read "
    "as the starting brief and archived unchanged under `docs/reference/`. Pecking Order "
    "implements the institutional reference layer, not the entire social simulation described there."),
    ("Le document de l’utilisateur a servi de cadre et est archivé sans modification. "
    "Le projet réalise le référentiel institutionnel, pas la simulation sociale complète."), "",
    "## Authored data / Données éditoriales", "",
    ("Generic templates, translations, explanatory text and code were authored for this project "
    "with AI assistance. They are not a scraped historical dataset. Runtime resolution uses no LLM."),
    ("Les modèles, traductions, explications et le code ont été créés pour ce projet avec une "
    "assistance IA. La résolution n’utilise aucun LLM. Les formes d’origine sont préservées quand "
    "elles sont renseignées ; leur traduction n’établit pas une équivalence de rang."), "",
    ("A source supports only the explicitly scoped claim. Blueprint-level `source_supported` "
    "means that a cultural binding exists; generic offices and powers remain independently "
    "labelled. Source references and short titles are distributed, not downloaded source texts."), "",
    "## Source register / Registre des sources", "",
]
for source in kb.data.sources:
    provenance += [f"### {source.id}", "", f"[{source.title}]({source.url}) — {source.publisher}.",
                   f"Consulté / accessed: {source.accessed}. Locator: {source.locator}.", "",
                   source.supports.labels["fr"], "", source.supports.labels["en"], "",
                   source.limitations.labels["fr"], ""]
(root / "PROVENANCE.md").write_text("\n".join(provenance), encoding="utf-8")

examples = {
    "tswana-village": {"culture": "tswana_bogosi_contemporary",
                        "organization": {"kind": "village_council", "scale": "local"}, "role": "executive"},
    "joint-family": {"culture": "hindu_joint_family_india",
                     "organization": {"kind": "corporate_household", "scale": "household"}},
    "deccan-court": {"culture": "deccan_sultanates",
                     "organization": {"kind": "hereditary_monarchy", "scale": "polity"}},
    "authoritarian-raya": {"culture": "vijayanagara_krishnadevaraya",
                           "organization": {"kind": "hereditary_monarchy", "scale": "polity",
                                            "traits": ["authoritarian"]},
                           "role": "sovereign", "mode": "inspired",
                           "adaptations": [{"kind": "authoritarian", "target_role": "sovereign"}]},
    "broad-african-context": {"culture": "africain", "organization": {
        "kind": "village_council", "scale": "local"}},
    "broad-hindu-context": {"culture": "hindou", "organization": {
        "kind": "hereditary_monarchy", "scale": "polity"}},
    "british-army-corps": {"culture": "british_army_contemporary", "organization": {
        "kind": "army_corps", "scale": "regional"}, "role": "command"},
    "haudenosaunee-council": {"culture": "haudenosaunee_confederacy_reference", "organization": {
        "kind": "confederation", "scale": "polity"}},
    "edo-power": {"culture": "japan_edo_reference", "organization": {
        "kind": "empire", "scale": "imperial"}, "as_of": 1700},
    "generic-king": {"culture": "*", "organization": {
        "kind": "hereditary_monarchy", "scale": "polity"}, "mode": "generic", "locale": "en"},
    "livery-company": {"culture": "london_livery_reference", "organization": {
        "kind": "craft_guild", "scale": "local"}},
    "subak": {"culture": "balinese_subak_reference", "organization": {
        "kind": "irrigation_association", "scale": "local"}},
    "gadaa": {"culture": "oromo_gadaa_reference", "organization": {
        "kind": "age_grade_governance", "scale": "regional"}},
    "asante-kingship": {"culture": "asante_traditional_contemporary", "organization": {
        "kind": "traditional_kingship", "scale": "regional"}},
    "latin-diocese": {"culture": "latin_catholic_canonical", "organization": {
        "kind": "diocese", "scale": "regional"}},
}
folder = root / "examples"
folder.mkdir(exist_ok=True)
for name, query in examples.items():
    (folder / f"{name}.json").write_text(json.dumps(
        {"schema_version": "1.0", "locale": "fr", **query}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
print(f"Exported coverage, provenance and {len(examples)} example requests")
