use pecking_order::{
    Engine, Query, Response,
    model::{Authority, Structure},
};
use serde_json::json;
use std::collections::BTreeSet;

fn resolve(engine: &Engine, value: serde_json::Value) -> Response {
    engine
        .resolve(serde_json::from_value(value).unwrap())
        .unwrap()
}

fn valid_graph(response: &Response) {
    let ids: BTreeSet<_> = response.roles.iter().map(|r| r.id.as_str()).collect();
    for role in &response.roles {
        assert!(
            role.reports_to.iter().all(|id| ids.contains(id.as_str())),
            "Dangling reference: {}",
            role.id
        );
        assert!(!role.reports_to.contains(&role.id));
        assert!(!role.title.fr.is_empty() && !role.title.en.is_empty());
        assert!(role.importance <= 100);
    }
    fn visit(id: &str, response: &Response, path: &mut BTreeSet<String>) {
        assert!(
            path.insert(id.into()),
            "Cycle in {} at {id}",
            response.system.id
        );
        for parent in &response
            .roles
            .iter()
            .find(|r| r.id == id)
            .unwrap()
            .reports_to
        {
            visit(parent, response, path);
        }
        path.remove(id);
    }
    for role in &response.roles {
        visit(&role.id, response, &mut BTreeSet::new());
    }
}

#[test]
fn organization_overrides_never_create_broken_command_graphs() {
    let engine = Engine::embedded().unwrap();
    let catalog = engine.catalog();
    for system in &engine.content.systems {
        for structure in catalog["structures"].as_array().unwrap() {
            for authority in catalog["authorities"].as_array().unwrap() {
                let response = resolve(
                    &engine,
                    json!({"system":system.id,"structure":structure,"authority":authority}),
                );
                valid_graph(&response);
            }
        }
    }
}

#[test]
fn shipped_request_files_run_against_the_embedded_content() {
    let engine = Engine::embedded().unwrap();
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("examples");
    for file in std::fs::read_dir(root).unwrap() {
        let path = file.unwrap().path();
        if path.extension().is_some_and(|value| value == "json") {
            let query = std::fs::read_to_string(&path).unwrap();
            let query: Query = serde_json::from_str(&query).unwrap();
            assert!(
                engine.resolve(query).is_ok(),
                "Failed example {}",
                path.display()
            );
        }
    }
}

#[test]
fn every_system_theme_combination_returns_complete_content() {
    let engine = Engine::embedded().unwrap();
    assert!(engine.content.systems.len() >= 200);
    assert!(engine.content.themes.len() >= 60);
    assert_eq!(engine.content.city_cultures.len(), 41);
    for system in &engine.content.systems {
        for theme in &engine.content.themes {
            let r = resolve(&engine, json!({"system":system.id,"theme":theme.id}));
            assert_eq!(
                r.roles.len(),
                system.roles.len(),
                "{} + {}",
                system.id,
                theme.id
            );
            valid_graph(&r);
        }
    }
}

#[test]
fn every_city_generator_culture_resolves_as_a_theme() {
    let engine = Engine::embedded().unwrap();
    for culture in &engine.content.city_cultures {
        assert!(
            !resolve(&engine, json!({"system":"kingdom","theme":culture.id}))
                .roles
                .is_empty()
        );
    }
}

#[test]
fn aristocratic_nation_changes_titles_not_functional_roles() {
    let engine = Engine::embedded().unwrap();
    let east = resolve(
        &engine,
        json!({"system":"aristocratic_nation","theme":"russian-kremlin"}),
    );
    let west = resolve(
        &engine,
        json!({"system":"aristocratic_nation","theme":"european-organic"}),
    );
    assert_eq!(
        east.roles.iter().map(|r| &r.id).collect::<Vec<_>>(),
        west.roles.iter().map(|r| &r.id).collect::<Vec<_>>()
    );
    let east_head = east.roles.iter().find(|r| r.title_key == "king").unwrap();
    let west_head = west.roles.iter().find(|r| r.title_key == "king").unwrap();
    assert_eq!(east_head.title.fr, "Tsar");
    assert_eq!(west_head.title.en, "King");
    assert_eq!(east_head.level, 0);
    assert!(east.roles.iter().any(|r| r.title_key == "duke"));
    assert!(west.roles.iter().any(|r| r.title_key == "baron"));
}

#[test]
fn tswana_village_includes_both_head_and_assembly() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(&engine, json!({"system":"village","theme":"tswana"}));
    assert!(r.roles.iter().any(|r| r.title.fr.contains("Kgosi")));
    assert!(
        r.roles
            .iter()
            .any(|r| r.title.fr.contains("Kgotla") && r.collective)
    );
    assert!(r.roles.iter().any(|r| r.title_key == "deputy"));
}

#[test]
fn four_person_cult_is_a_usable_cell_not_a_large_temple() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(
        &engine,
        json!({"system":"cult_cell","theme":"chthonic-cult","members":4}),
    );
    assert_eq!(r.roles.len(), 4);
    assert!(r.roles.iter().any(|r| r.title_key == "ritualist"));
    assert!(r.roles.iter().all(|r| !r.duties.fr.is_empty()));
}

#[test]
fn joint_family_has_estate_office_and_no_trivial_parent_slots() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(
        &engine,
        json!({"system":"joint_family","theme":"indian-temple"}),
    );
    assert!(r.roles.iter().any(|r| r.title.fr.contains("Karta")));
    assert!(r.roles.iter().any(|r| r.title_key == "family_head"));
    assert!(
        r.roles
            .iter()
            .all(|r| !["father", "mother", "child"].contains(&r.id.as_str()))
    );
    assert!(
        r.roles
            .iter()
            .filter(|r| ["matriarch", "patriarch"].contains(&r.title_key.as_str()))
            .all(|r| r.optional)
    );
}

#[test]
fn size_and_importance_filters_preserve_valid_hierarchy() {
    let engine = Engine::embedded().unwrap();
    for system in &engine.content.systems {
        for size in ["tiny", "small", "medium", "large", "vast"] {
            let r = resolve(&engine, json!({"system":system.id,"size":size}));
            assert!(!r.roles.is_empty(), "Empty {} at {size}", system.id);
            valid_graph(&r);
        }
    }
    let r = resolve(
        &engine,
        json!({"system":"kingdom","filter":{"min_importance":80,"max_level":4}}),
    );
    assert!(r.roles.iter().all(|r| r.importance >= 80 && r.level <= 4));
    valid_graph(&r);
}

#[test]
fn text_filter_matches_bilingual_cultural_title() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(
        &engine,
        json!({"system":"kingdom","theme":"russian-kremlin","filter":{"text":"tsar"}}),
    );
    assert!(!r.roles.is_empty());
    assert!(r.roles.iter().any(|r| r.title.fr == "Tsar"));
    valid_graph(&r);
}

#[test]
fn horizontal_is_actually_horizontal_and_authority_is_expressed() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(
        &engine,
        json!({"system":"craft_guild","theme":"dwarven","structure":"horizontal"}),
    );
    assert_eq!(r.structure, Structure::Horizontal);
    assert!(
        r.roles
            .iter()
            .all(|r| r.level == 0 && r.reports_to.is_empty())
    );
    let r = resolve(
        &engine,
        json!({"system":"kingdom","theme":"western-europe","authority":"democratic"}),
    );
    assert_eq!(r.authority, Authority::Democratic);
    assert!(r.roles.iter().any(|r| r.title_key == "elected_leader"));
    let r = resolve(
        &engine,
        json!({"system":"nation","theme":"russian-kremlin","authority":"authoritarian"}),
    );
    assert!(
        r.roles
            .iter()
            .any(|r| r.powers.iter().any(|p| p.id == "decree"))
    );
    valid_graph(&r);
}

#[test]
fn strict_query_and_useful_errors() {
    assert!(serde_json::from_value::<Query>(json!({"system":"kingdom","ignored":true})).is_err());
    assert!(serde_json::from_value::<Query>(json!({"system":"kingdom","members":"4"})).is_err());
    let engine = Engine::embedded().unwrap();
    let q = serde_json::from_value(json!({"system":"not-a-system"})).unwrap();
    assert_eq!(engine.resolve(q).unwrap_err().field, "system");
    let q = serde_json::from_value(json!({"system":"kingdom","members":0})).unwrap();
    assert_eq!(engine.resolve(q).unwrap_err().code, "members");
}

#[test]
fn everyday_system_and_theme_aliases_work_without_context_gates() {
    let engine = Engine::embedded().unwrap();
    let r = resolve(
        &engine,
        json!({"system":"royaume", "theme":"Europe de l’Est"}),
    );
    assert!(r.roles.iter().any(|r| r.title.fr == "Tsar"));
    let r = resolve(&engine, json!({"system":"famille", "theme":"hindou"}));
    assert_eq!(r.system.id, "joint_family");
    assert!(r.roles.iter().any(|r| r.title.fr.contains("Karta")));
    assert_eq!(
        resolve(&engine, json!({"system":"guild","theme":"dwarven"}))
            .system
            .id,
        "craft_guild"
    );
}

#[test]
fn replay_and_languages_are_stable() {
    let engine = Engine::embedded().unwrap();
    let a = resolve(
        &engine,
        json!({"system":"kingdom","theme":"elven","locale":"fr-CA"}),
    );
    let b = resolve(
        &engine,
        json!({"system":"kingdom","theme":"elven","locale":"en"}),
    );
    assert_eq!(a.roles[0].title, b.roles[0].title);
    assert_eq!(a.roles[0].display_title, a.roles[0].title.fr);
    assert_eq!(b.roles[0].display_title, b.roles[0].title.en);
    let again = engine.resolve(a.request.clone()).unwrap();
    assert_eq!(
        serde_json::to_string(&a).unwrap(),
        serde_json::to_string(&again).unwrap()
    );
}

#[test]
fn every_power_is_translated_and_every_role_duty_is_content() {
    let engine = Engine::embedded().unwrap();
    for system in &engine.content.systems {
        for role in &system.roles {
            for power in &role.powers {
                assert!(
                    engine.content.powers.contains_key(power),
                    "Missing power label {power} in {}",
                    system.id
                );
            }
            assert!(!role.duties.fr.contains("Assure une responsabilité définie"));
        }
    }
}
