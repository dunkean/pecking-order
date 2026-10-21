use pecking_order::{Engine, Query};
use serde_json::json;

#[test]
fn every_authored_reporting_edge_points_to_a_senior_role() {
    let engine = Engine::embedded().unwrap();
    for system in &engine.content.systems {
        for role in &system.roles {
            for parent in &role.reports_to {
                let senior = system.roles.iter().find(|r| &r.id == parent).unwrap();
                assert!(
                    senior.level < role.level,
                    "{}.{} (level {}) reports to {} (level {})",
                    system.id,
                    role.id,
                    role.level,
                    parent,
                    senior.level
                );
            }
        }
    }
}

#[test]
fn gang_roles_keep_their_actual_functions_in_every_culture() {
    let engine = Engine::embedded().unwrap();
    for theme in &engine.content.themes {
        let query: Query =
            serde_json::from_value(json!({"system":"street_gang","theme":theme.id})).unwrap();
        let response = engine.resolve(query).unwrap();
        assert_eq!(
            response
                .roles
                .iter()
                .find(|r| r.id == "block_leader")
                .unwrap()
                .title
                .fr,
            "Chef de bande"
        );
        assert_eq!(
            response
                .roles
                .iter()
                .find(|r| r.id == "lookout")
                .unwrap()
                .title
                .en,
            "Lookout"
        );
        for role in &response.roles {
            assert!(
                ![
                    "captain",
                    "quartermaster",
                    "marshal",
                    "general",
                    "sergeant",
                    "lieutenant"
                ]
                .contains(&role.title_key.as_str()),
                "Gang became a military unit in {}",
                theme.id
            );
        }
        let military: Query =
            serde_json::from_value(json!({"system":"naval_fleet","theme":theme.id})).unwrap();
        // Authentic military/naval offices still receive their cultural titles.
        let fleet = engine.resolve(military).unwrap();
        {
            assert!(
                fleet
                    .roles
                    .iter()
                    .any(|r| ["admiral", "captain", "commander"].contains(&r.title_key.as_str()))
            );
        }
    }
}

#[test]
fn unrelated_groups_do_not_share_a_complete_functional_template() {
    let engine = Engine::embedded().unwrap();
    for pair in [
        ["bank", "craft_guild"],
        ["monster_pack", "mage_college"],
        ["underground_press", "spy_ring"],
        ["neighborhood_watch", "public_works_office"],
        ["mediation_circle", "court_of_justice"],
    ] {
        let a = engine
            .content
            .systems
            .iter()
            .find(|s| s.id == pair[0])
            .unwrap();
        let b = engine
            .content
            .systems
            .iter()
            .find(|s| s.id == pair[1])
            .unwrap();
        {
            let functions = |s: &pecking_order::model::System| {
                s.roles
                    .iter()
                    .map(|r| (r.key.clone(), r.function.clone(), r.duties.clone()))
                    .collect::<Vec<_>>()
            };
            assert_ne!(
                functions(a),
                functions(b),
                "Unrelated institutions share the entire template: {pair:?}"
            );
        }
    }
}

#[test]
fn contextual_leadership_obeys_structure_without_giving_a_gang_state_powers() {
    let engine = Engine::embedded().unwrap();
    let query = |extra: &str| -> Query {
        serde_json::from_str(&format!(r#"{{"system":"street_gang",{extra}}}"#)).unwrap()
    };
    let horizontal = engine
        .resolve(query(r#""structure":"horizontal""#))
        .unwrap();
    assert!(
        horizontal
            .roles
            .iter()
            .all(|r| r.level == 0 && r.reports_to.is_empty())
    );
    assert_eq!(
        horizontal
            .roles
            .iter()
            .find(|r| r.id == "block_leader")
            .unwrap()
            .title_key,
        "representative"
    );
    let authoritarian = engine
        .resolve(query(r#""authority":"authoritarian""#))
        .unwrap();
    assert!(
        authoritarian
            .roles
            .iter()
            .all(|r| r.powers.iter().all(|p| p.id != "decree"))
    );
    assert!(
        authoritarian
            .roles
            .iter()
            .find(|r| r.id == "block_leader")
            .unwrap()
            .powers
            .iter()
            .any(|p| p.id == "decide")
    );
}
