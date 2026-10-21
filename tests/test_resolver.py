import copy
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from pecking_order import KnowledgeBase
from pecking_order.models import Dataset, Query, Resolution

ROOT = Path(__file__).resolve().parents[1]
KB = KnowledgeBase()


def request(culture="tswana", kind="village_council", scale="local", **extra):
    return {"culture": culture, "organization": {"kind": kind, "scale": scale}, **extra}


@pytest.mark.parametrize("template", KB.data.templates, ids=lambda t: t.id)
def test_every_generic_blueprint_resolves_and_matches_wire_schema(template):
    q = request("*", template.id, template.scales[0], mode="generic")
    response = KB.resolve(q)
    assert response.status == "resolved"
    assert response.blueprint.evidence.status == "generic_model"
    Draft202012Validator(Resolution.model_json_schema()).validate(response.model_dump(mode="json"))
    assert len(response.selected_roles) == len(template.roles)


@pytest.mark.parametrize("culture,kind", [(c.id, b.template) for c in KB.data.cultures
                                         for b in c.bindings])
def test_every_cultural_binding_is_valid_and_exposes_provenance(culture, kind):
    q = request(culture, kind, KB.templates[kind].scales[0])
    response = KB.resolve(q)
    assert response.status == "resolved"
    assert response.sources
    assert response.culture.id == culture
    assert response.blueprint.id == kind
    assert any(r.title_evidence.status == "source_supported" for r in response.blueprint.roles)
    assert all({"en", "fr"} <= r.title.labels.keys() for r in response.blueprint.roles)


@pytest.mark.parametrize("broad", ["hindou", "hindu", "africain", "african", "christian", "japonais"])
def test_broad_context_never_silently_assigned_a_title(broad):
    result = KB.resolve(request(broad))
    assert result.status == "needs_context"
    assert result.blueprint is None
    assert result.candidates


def test_hindu_court_does_not_automatically_get_sultan():
    broad = KB.resolve(request("hindou", "hereditary_monarchy", "polity"))
    assert broad.status == "needs_context"
    raya = KB.resolve(request("vijayanagara", "hereditary_monarchy", "polity", role="sovereign"))
    assert raya.blueprint.roles[0].title.native == "Rāya"
    sultan = KB.resolve(request("deccan", "hereditary_monarchy", "polity", role="sovereign"))
    assert sultan.blueprint.roles[0].title.labels["en"] == "Sultan"


def test_family_is_corporate_not_a_trivial_parent_child_structure():
    result = KB.resolve(request("huf", "corporate_household", "household", role="household_manager"))
    assert result.selected_roles == ["manager"]
    assert result.blueprint.roles[0].title.native == "कर्ता"
    assert not {"father", "mother", "child"} & {r.id for r in result.blueprint.roles}


def test_office_and_rank_are_different_objects():
    result = KB.resolve(request("british army", "army_corps", "regional", role="command"))
    commander = next(r for r in result.blueprint.roles if r.id == "commander")
    assert commander.title.labels["en"] == "Commanding officer"
    assert commander.rank.labels["en"] == "Lieutenant General"


def test_no_single_chief_is_invented_for_a_confederation():
    result = KB.resolve(request("haudenosaunee", "confederation", "polity"))
    roles = {r.id: r for r in result.blueprint.roles}
    assert not {"head", "sovereign"} & roles.keys()
    assert roles["council"].holder == "collective"
    assert roles["representatives"].max_holders == 50
    assert roles["custodian"].max_holders == 49
    assert roles["custodian"].rules[0].parameters["except_office"] == "tadodaho"
    assert not any(r.kind == "reports_to" for r in result.blueprint.relations)


def test_nominal_and_effective_power_can_coexist():
    result = KB.resolve(request("tokugawa", "empire", "imperial"))
    roles = {r.id: r for r in result.blueprint.roles}
    assert roles["sovereign"].title.labels["fr"] == "Empereur"
    assert roles["head"].powers[0].basis == "de_facto"
    assert not any(r.source == "head" and r.target == "sovereign"
                   and r.kind == "reports_to" for r in result.blueprint.relations)


def test_regime_not_inferred_from_religion_or_title():
    q = request("vijayanagara", "hereditary_monarchy", "polity")
    q["organization"]["traits"] = ["authoritarian"]
    assert KB.resolve(q).status == "conflict"


def test_authoritarian_fantasy_adaptation_is_explicit_and_keeps_cultural_title():
    q = request("vijayanagara", "hereditary_monarchy", "polity", mode="inspired")
    q["adaptations"] = [{"kind": "authoritarian", "target_role": "sovereign"}]
    q["organization"]["traits"] = ["authoritarian"]
    result = KB.resolve(q)
    assert result.status == "resolved"
    sovereign = next(r for r in result.blueprint.roles if r.id == "sovereign")
    assert sovereign.title.native == "Rāya"
    assert sovereign.title_evidence.status == "source_supported"
    assert sovereign.powers[-1].evidence.status == "adapted"
    assert not any(r.kind == "checks" and r.target == "sovereign"
                   for r in result.blueprint.relations)


@pytest.mark.parametrize("mode,target", [("historical", "sovereign"),
                                        ("inspired", "council"), ("inspired", "missing")])
def test_invalid_adaptations_are_rejected(mode, target):
    q = request("vijayanagara", "hereditary_monarchy", "polity", mode=mode)
    q["adaptations"] = [{"kind": "authoritarian", "target_role": target}]
    assert KB.resolve(q).status == "conflict"


def test_incompatible_succession_adaptations_do_not_accumulate():
    q = request("*", "hereditary_monarchy", "polity", mode="generic")
    q["adaptations"] = [{"kind": "elective_succession", "target_role": "sovereign"}]
    result = KB.resolve(q)
    assert "elective" in result.blueprint.traits
    assert "hereditary" not in result.blueprint.traits
    assert not any(r.method == "dynastic_selection" for r in result.blueprint.rules)
    q["adaptations"].append({"kind": "hereditary_succession", "target_role": "sovereign"})
    assert KB.resolve(q).status == "conflict"


def test_missing_cultural_data_is_explicit_even_in_inspired_mode():
    assert KB.resolve(request("tswana", "craft_guild", "local")).status == "unsupported"
    result = KB.resolve(request("tswana", "craft_guild", "local", mode="inspired"))
    assert result.status == "resolved"
    assert result.blueprint.evidence.status == "adapted"
    assert all(r.title_evidence.status == "generic_model" for r in result.blueprint.roles)
    assert "generic_fallback" in [d.code for d in result.diagnostics]


@pytest.mark.parametrize("locale", ["fr", "en", "fr-CA", "de"])
def test_multilingual_display_and_reported_fallback(locale):
    result = KB.resolve(request(locale=locale))
    assert "Kgosi" in result.display["head.title"]
    assert bool(result.translation_fallbacks) == (locale not in ("fr", "en"))
    assert result.blueprint.roles[0].title.labels.keys() >= {"en", "fr"}


@pytest.mark.parametrize("q,status", [
    (request("unknown"), "unsupported"),
    (request(kind="unknown"), "unsupported"),
    (request(scale="imperial"), "conflict"),
    (request(as_of=1400), "unsupported"),
    (request(mode="generic"), "conflict"),
    (request(role="not_a_role"), "role_not_found"),
])
def test_semantic_failures_have_diagnostics(q, status):
    result = KB.resolve(q)
    assert result.status == status
    assert result.diagnostics


@pytest.mark.parametrize("patch", [
    {"unexpected": True}, {"schema_version": "9.0"}, {"as_of": "2026"},
    {"mode": "guess"}, {"locale": "invalid language"}, {"culture": ""},
    {"organization": {"kind": "village_council", "scale": "local", "ignored": 2}},
])
def test_contract_rejects_unknown_fields_and_type_coercions(patch):
    with pytest.raises(ValidationError):
        Query.model_validate({**request(), **patch})


def test_replay_is_deterministic_and_thread_safe():
    q = request("asante", "traditional_kingship", "regional")
    expected = KB.resolve(q).model_dump_json()
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert all(value == expected for value in pool.map(
            lambda _: KB.resolve(q).model_dump_json(), range(16)))
    mutated = KB.resolve(q)
    mutated.blueprint.roles[0].title.labels["fr"] = "WRONG"
    mutated.culture.label.labels["fr"] = "WRONG"
    mutated.sources[0].title = "WRONG"
    assert KB.resolve(q).model_dump_json() == expected


@pytest.mark.parametrize("mutation", ["unknown_source", "cycle", "unknown_role", "missing_fr", "duplicate_template"])
def test_invalid_knowledge_packs_fail_before_serving(tmp_path, mutation):
    data = KB.data.model_dump(mode="json")
    if mutation == "unknown_source":
        data["templates"][0]["roles"][0]["title_evidence"]["sources"] = ["missing"]
    if mutation == "cycle":
        relation = copy.deepcopy(data["templates"][0]["relations"][0])
        relation.update(source="sovereign", target="steward", kind="reports_to")
        data["templates"][0]["relations"].append(relation)
    if mutation == "unknown_role":
        data["templates"][0]["relations"][0]["target"] = "missing"
    if mutation == "missing_fr":
        del data["templates"][0]["roles"][0]["title"]["labels"]["fr"]
    if mutation == "duplicate_template":
        data["templates"].append(data["templates"][0])
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        KnowledgeBase(path)


def test_checked_in_schemas_match_models():
    for name, model in [("query", Query), ("response", Resolution), ("dataset", Dataset)]:
        schema = json.loads((ROOT / f"schemas/{name}.schema.json").read_text(encoding="utf-8"))
        assert schema == model.model_json_schema()
        Draft202012Validator.check_schema(schema)


def test_catalog_is_reproducible():
    import runpy
    namespace = runpy.run_path(str(ROOT / "tools/build_catalog.py"))
    assert namespace["catalog"] == KB.data.model_dump(mode="json")


@pytest.mark.parametrize("path", sorted((ROOT / "examples").glob("*.json")), ids=lambda p: p.stem)
def test_documented_examples_are_executable(path):
    query = Query.model_validate_json(path.read_text(encoding="utf-8"))
    result = KB.resolve(query)
    assert result.status == ("needs_context" if path.name.startswith("broad-") else "resolved")


def test_openapi_references_resolve():
    document = json.loads((ROOT / "schemas/openapi.json").read_text(encoding="utf-8"))

    def walk(node):
        if isinstance(node, dict):
            if "$ref" in node:
                target = document
                for part in node["$ref"].removeprefix("#/").split("/"):
                    target = target[part]
            for value in node.values():
                walk(value)
        if isinstance(node, list):
            for value in node:
                walk(value)

    walk(document)
    assert document["components"]["schemas"]["Query"]["additionalProperties"] is False
