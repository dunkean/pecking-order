"""Explicit compatibility resolution; no probabilistic or language-model guessing."""

import hashlib
import json
import unicodedata
from importlib.resources import files
from pathlib import Path

from .models import (
    Blueprint,
    Candidate,
    CultureContext,
    Dataset,
    Diagnostic,
    EvidenceRef,
    Localized,
    Power,
    Query,
    Resolution,
    Rule,
)


def text(en: str, fr: str) -> Localized:
    return Localized(labels={"en": en, "fr": fr})


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


class KnowledgeBase:
    def __init__(self, path: str | Path | None = None):
        raw = Path(path).read_bytes() if path else files("pecking_order").joinpath(
            "data/catalog.json"
        ).read_bytes()
        self.data = Dataset.model_validate_json(raw)
        canonical = json.dumps(json.loads(raw), sort_keys=True, ensure_ascii=False,
                               separators=(",", ":")).encode()
        self.digest = hashlib.sha256(canonical).hexdigest()
        self.templates = {item.id: item for item in self.data.templates}
        self.cultures = {item.id: item for item in self.data.cultures}
        self.sources = {item.id: item for item in self.data.sources}
        for records, name in [(self.data.templates, "template"),
                              (self.data.cultures, "culture"), (self.data.sources, "source")]:
            if len({item.id for item in records}) != len(records):
                raise ValueError(f"Duplicate {name} IDs")
        self.aliases: dict[str, set[str]] = {}
        for template in self.data.templates:
            for unit in template.units:
                if unit.kind not in self.templates:
                    raise ValueError(f"Unknown child template: {unit.kind}")
        for culture in self.data.cultures:
            for alias in [culture.id, *culture.aliases]:
                self.aliases.setdefault(normalize(alias), set()).add(culture.id)
            for binding in culture.bindings:
                if binding.template not in self.templates:
                    raise ValueError(f"Unknown bound template: {binding.template}")
                self.compose(culture.id, binding.template)
        for alias, ids in self.data.broad_aliases.items():
            if not set(ids) <= self.cultures.keys():
                raise ValueError(f"Unknown culture in broad alias: {alias}")
            self.aliases.setdefault(normalize(alias), set()).update(ids)
        self._check_sources(self.data.model_dump(mode="json"))

    def _check_sources(self, node):
        if isinstance(node, dict):
            if "status" in node and "sources" in node and isinstance(node["sources"], list):
                for sid in node["sources"]:
                    if sid not in self.sources:
                        raise ValueError(f"Unknown source: {sid}")
            for value in node.values():
                self._check_sources(value)
        elif isinstance(node, list):
            for value in node:
                self._check_sources(value)

    def compose(self, culture_id: str, kind: str) -> Blueprint:
        template = self.templates[kind]
        binding = next((b for b in self.cultures[culture_id].bindings if b.template == kind), None)
        if binding is None:
            return template.model_copy(deep=True)
        data = template.model_dump(mode="json")
        role_ids = {r.id for r in template.roles}
        if not set(binding.remove_roles) <= role_ids:
            raise ValueError("Cannot remove an unknown role")
        replacements = {r.id: r.model_dump(mode="json") for r in binding.roles}
        if len(replacements) != len(binding.roles):
            raise ValueError("Duplicate roles in binding")
        roles = {r["id"]: r for r in data["roles"] if r["id"] not in binding.remove_roles}
        roles.update(replacements)
        data["roles"] = list(roles.values())
        relations = [] if binding.replace_relations else [
            r for r in data["relations"]
            if r["source"] in roles and r["target"] in roles
        ]
        relations.extend(r.model_dump(mode="json") for r in binding.relations)
        data["relations"] = relations
        data["rules"].extend(r.model_dump(mode="json") for r in binding.rules)
        data["traits"] = sorted(set(data["traits"]) | set(binding.traits))
        data["evidence"] = binding.evidence.model_dump(mode="json")
        return Blueprint.model_validate_json(json.dumps(data, ensure_ascii=False))

    def catalog(self):
        return {
            "schema_version": "1.0", "kb_version": self.data.version, "kb_digest": self.digest,
            "templates": [{"id": t.id, "label": t.label.model_dump(), "domain": t.domain,
                           "scales": t.scales, "traits": t.traits} for t in self.data.templates],
            "cultures": [{"id": c.id, "label": c.label.model_dump(), "period": c.period,
                          "region": c.region.model_dump(),
                          "supported_kinds": [b.template for b in c.bindings]}
                         for c in self.data.cultures],
            "coverage": {
                "generic_templates": len(self.templates), "cultural_profiles": len(self.cultures),
                "cultural_bindings": sum(len(c.bindings) for c in self.data.cultures),
                "sources": len(self.sources), "historically_exhaustive": False,
                "launch_locales": ["fr", "en"],
            },
            "broad_aliases": self.data.broad_aliases,
        }

    def resolve(self, query: Query | dict) -> Resolution:
        q = query if isinstance(query, Query) else Query.model_validate(query)
        result = Resolution(kb_version=self.data.version, kb_digest=self.digest,
                            request=q, status="unsupported")

        def diagnostic(code, en, fr, fields=()):
            result.diagnostics.append(Diagnostic(code=code, message=text(en, fr),
                                                 fields=list(fields)))

        if q.organization.kind not in self.templates:
            diagnostic("unknown_kind", "Choose a kind from the catalogue.",
                       "Choisissez un type dans le catalogue.", ["organization.kind"])
            return result
        if q.adaptations and q.mode == "historical":
            result.status = "conflict"
            diagnostic("adaptation_in_reference", "Adaptations require inspired or generic mode.",
                       "Les adaptations demandent le mode inspired ou generic.", ["mode"])
            return result
        base = self.templates[q.organization.kind]
        if q.organization.scale not in base.scales:
            result.status = "conflict"
            diagnostic("scale_conflict", "This blueprint does not support the requested scale.",
                       "Ce modèle ne prend pas en charge cette échelle.", ["organization.scale"])
            return result
        if q.mode == "generic":
            if q.culture != "*":
                result.status = "conflict"
                diagnostic("generic_culture", "Generic mode requires culture '*'.",
                           "Le mode générique demande la culture '*'.", ["culture"])
                return result
            blueprint = base.model_copy(deep=True)
            diagnostic("generic_model", "This is an authored generic blueprint.",
                       "Ceci est un modèle générique conçu pour le worldbuilding.")
        else:
            ids = self.aliases.get(normalize(q.culture), set())
            if not ids:
                diagnostic("unknown_culture", "Unknown culture; use a profile ID from the catalogue.",
                           "Culture inconnue ; utilisez un identifiant du catalogue.", ["culture"])
                return result
            candidates = [self.cultures[cid] for cid in sorted(ids)]
            if q.as_of is not None:
                candidates = [c for c in candidates if c.period[0] <= q.as_of <= c.period[1]]
            if not candidates:
                diagnostic("period_not_covered", "This date is outside available profile coverage.",
                           "Cette date est hors de la couverture des profils.", ["as_of"])
                return result
            # Broad words stay ambiguous even if only one demonstration profile is in the KB.
            if len(candidates) > 1 or normalize(q.culture) in self.data.broad_aliases:
                result.status = "needs_context"
                result.candidates = [Candidate(culture=c.id, label=c.label.model_copy(deep=True),
                                               period=c.period,
                                               supported_kinds=[b.template for b in c.bindings])
                                     for c in candidates]
                diagnostic("culture_too_broad", "Choose a specific cultural and institutional context.",
                           "Précisez le contexte culturel et institutionnel.", ["culture"])
                return result
            culture = candidates[0]
            result.culture = CultureContext(id=culture.id, label=culture.label, region=culture.region,
                                            period=culture.period, description=culture.description
                                            ).model_copy(deep=True)
            bound = any(b.template == base.id for b in culture.bindings)
            if not bound and q.mode == "historical":
                diagnostic("binding_missing", "No researched cultural binding for this institution.",
                           "Aucune déclinaison culturelle documentée pour cette institution.")
                return result
            blueprint = self.compose(culture.id, base.id)
            if not bound:
                diagnostic("generic_fallback", "Generic structure; no cultural titles have been inferred.",
                           "Structure générique ; aucun titre culturel n’a été déduit.")
            if q.mode == "inspired":
                # A changed setting remains an adaptation even when titles are source-supported.
                data = blueprint.model_dump(mode="json")
                data["evidence"]["status"] = "adapted"
                blueprint = Blueprint.model_validate_json(json.dumps(data, ensure_ascii=False))
                diagnostic("adaptation", "Worldbuilding adaptation, not a historical reconstruction.",
                           "Adaptation de worldbuilding, pas une reconstitution historique.")
            if q.as_of is None:
                diagnostic("profile_period", "The profile's documented interval is used; no exact year assumed.",
                           "L’intervalle documenté du profil est utilisé ; aucune année précise n’est supposée.")
        seen = set()
        for adaptation in q.adaptations:
            role = next((r for r in blueprint.roles if r.id == adaptation.target_role), None)
            family = "succession" if adaptation.kind.endswith("succession") else adaptation.kind
            key = (adaptation.target_role, family)
            if (role is None or role.holder != "person" or role.max_holders != 1
                    or role.function not in {"executive", "sovereign", "command", "household_manager"}
                    or key in seen):
                result.status = "conflict"
                diagnostic("invalid_adaptation", "Choose one compatible adaptation per individual executive office.",
                           "Choisissez une adaptation compatible par charge exécutive individuelle.",
                           ["adaptations"])
                return result
            seen.add(key)
            ev = EvidenceRef(status="adapted", note=text(
                "Explicit fictional adaptation requested by the caller.",
                "Adaptation fictive demandée explicitement par l’appelant."))
            if adaptation.kind == "authoritarian":
                blueprint.traits = sorted(set(blueprint.traits) | {"authoritarian"})
                blueprint.relations = [r for r in blueprint.relations if not (
                    r.target == role.id and r.kind == "checks")]
                role.powers.append(Power(
                    action="unilateral_internal_decision", domain=blueprint.domain, basis="de_jure",
                    scope=text("Make unilateral decisions within this institution's remit.",
                               "Décider unilatéralement dans le champ de cette institution."),
                    limits=text("Fictional internal authority; does not imply control over external institutions or actual obedience.",
                                "Autorité interne fictive ; ne présume ni contrôle des institutions extérieures ni obéissance réelle."),
                    evidence=ev))
            else:
                method = "election" if adaptation.kind == "elective_succession" else "dynastic_selection"
                # Replace, rather than accumulate, incompatible succession claims.
                role.rules = [r for r in role.rules if r.category not in {"selection", "succession"}]
                blueprint.rules = [r for r in blueprint.rules if r.category not in {"selection", "succession"}]
                blueprint.traits = sorted((set(blueprint.traits) - {"elective", "hereditary"}) | {
                    "elective" if method == "election" else "hereditary"})
                role.rules.append(Rule(
                    id="adapted_succession", category="succession", method=method,
                    description=text(
                        "Fictional succession by election; electorate and eligibility must be specified."
                        if method == "election" else
                        "Fictional succession within a dynasty; descent and eligibility must be specified.",
                        "Succession fictive par élection ; corps électoral et admissibilité à préciser."
                        if method == "election" else
                        "Succession fictive dans une dynastie ; filiation et admissibilité à préciser."),
                    evidence=ev))
            blueprint.evidence = ev
            diagnostic("explicit_adaptation", "Applied adaptation: " + adaptation.kind,
                       "Adaptation appliquée : " + adaptation.kind)
        missing_traits = sorted(set(q.organization.traits) - set(blueprint.traits))
        if missing_traits:
            result.status = "conflict"
            diagnostic("traits_unavailable", "Unsupported traits: " + ", ".join(missing_traits),
                       "Caractéristiques non prises en charge : " + ", ".join(missing_traits),
                       ["organization.traits"])
            return result
        selected = [r.id for r in blueprint.roles if q.role is None or q.role in (r.id, r.function)]
        if not selected:
            result.status = "role_not_found"
            diagnostic("unknown_role", "The requested role is absent; inspect blueprint.roles.",
                       "Le rôle demandé est absent ; consultez blueprint.roles.", ["role"])
        else:
            result.status = "resolved"
        result.blueprint = blueprint
        result.selected_roles = selected
        used_sources = set()

        def collect(node):
            if isinstance(node, dict):
                if "status" in node and isinstance(node.get("sources"), list):
                    used_sources.update(node["sources"])
                for value in node.values():
                    collect(value)
            elif isinstance(node, list):
                for value in node:
                    collect(value)

        collect(blueprint.model_dump(mode="json"))
        result.sources = [self.sources[sid].model_copy(deep=True) for sid in sorted(used_sources)]

        def localized(labels, path):
            for lang in dict.fromkeys([q.locale, q.locale.split("-")[0],
                                       q.fallback_locale, q.fallback_locale.split("-")[0], "en"]):
                if lang in labels:
                    if lang != q.locale:
                        result.translation_fallbacks.append(path)
                    return labels[lang]
            raise ValueError("Missing launch-language translations")

        result.display["organization"] = localized(blueprint.label.labels, "organization")
        for role in blueprint.roles:
            result.display[role.id + ".title"] = localized(role.title.labels, role.id + ".title")
            result.display[role.id + ".duties"] = localized(role.duties.labels, role.id + ".duties")
        return result
