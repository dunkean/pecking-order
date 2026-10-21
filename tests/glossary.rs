use pecking_order::Engine;
use std::collections::BTreeSet;

#[test]
fn glossary_includes_every_title_variant_and_functional_term() {
    let engine = Engine::embedded().unwrap();
    let glossary = engine.glossary();
    let terms = glossary["terms"].as_array().unwrap();
    assert_eq!(
        terms.len(),
        glossary["counts"]["terms"].as_u64().unwrap() as usize
    );
    let mut represented = BTreeSet::new();
    for term in terms {
        for binding in term["bindings"].as_array().unwrap() {
            represented.insert((
                term["fr"].as_str().unwrap().to_owned(),
                term["en"].as_str().unwrap().to_owned(),
                term["native"].as_str().map(str::to_owned),
                binding["theme"].as_str().map(str::to_owned),
                binding["key"].as_str().unwrap().to_owned(),
            ));
        }
    }
    for theme in &engine.content.themes {
        let lexicon = engine.theme_lexicon(&theme.id).unwrap();
        for (key, value) in lexicon["titles"].as_object().unwrap() {
            let title = &value["title"];
            let mut forms = vec![title];
            forms.extend(title["variants"].as_array().unwrap());
            for form in forms {
                assert!(
                    represented.contains(&(
                        form["fr"].as_str().unwrap().into(),
                        form["en"].as_str().unwrap().into(),
                        form["native"].as_str().map(str::to_owned),
                        Some(theme.id.clone()),
                        key.clone()
                    )),
                    "Missing {}.{key}: {form}",
                    theme.id
                );
            }
        }
    }
    for system in &engine.content.systems {
        for role in &system.roles {
            if let Some(title) = &role.title {
                assert!(represented.contains(&(
                    title.fr.clone(),
                    title.en.clone(),
                    None,
                    None,
                    role.key.clone()
                )));
            }
        }
    }
}

#[test]
fn glossary_preserves_every_actual_role_definition_without_duplicate_title_pairs() {
    let engine = Engine::embedded().unwrap();
    let glossary = engine.glossary();
    let mut definitions = BTreeSet::new();
    for function in glossary["functions"].as_array().unwrap() {
        for usage in function["uses"].as_array().unwrap() {
            definitions.insert((
                usage["system"].as_str().unwrap(),
                usage["role"].as_str().unwrap(),
            ));
            assert!(!usage["duties"]["fr"].as_str().unwrap().is_empty());
        }
    }
    for system in &engine.content.systems {
        for role in &system.roles {
            assert!(definitions.contains(&(system.id.as_str(), role.id.as_str())));
        }
    }
    assert_eq!(
        definitions.len(),
        engine
            .content
            .systems
            .iter()
            .map(|s| s.roles.len())
            .sum::<usize>()
    );
    let mut titles = BTreeSet::new();
    for term in glossary["terms"].as_array().unwrap() {
        assert!(titles.insert((
            term["fr"].as_str(),
            term["en"].as_str(),
            term["native"].as_str()
        )));
    }
    assert_eq!(
        glossary["powers"].as_array().unwrap().len(),
        engine.content.powers.len()
    );
    assert_eq!(
        glossary["systems"].as_array().unwrap().len(),
        engine.content.systems.len()
    );
}
