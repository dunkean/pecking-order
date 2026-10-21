use crate::{Engine, model::*};
use serde::Serialize;
use serde_json::{Value, json};
use std::collections::BTreeMap;

#[derive(Clone, Serialize)]
struct Binding {
    theme: Option<String>,
    system: Option<String>,
    key: String,
    form: String,
    parent: Option<Text>,
}

#[derive(Serialize)]
struct Term {
    fr: String,
    en: String,
    native: Option<String>,
    bindings: Vec<Binding>,
}

type TermIndex = BTreeMap<(String, String, Option<String>), Term>;

fn insert(index: &mut TermIndex, fr: &str, en: &str, native: &Option<String>, binding: Binding) {
    let key = (fr.to_owned(), en.to_owned(), native.clone());
    index
        .entry(key)
        .or_insert_with(|| Term {
            fr: fr.into(),
            en: en.into(),
            native: native.clone(),
            bindings: Vec::new(),
        })
        .bindings
        .push(binding);
}

impl Engine {
    /// All effective titles and every authored form, together with the actual role
    /// definitions that use them. Shared spellings retain their distinct contexts.
    pub fn glossary(&self) -> Value {
        let mut index = TermIndex::new();
        let mut variant_bindings = 0usize;
        for (i, theme) in self.content.themes.iter().enumerate() {
            for (key, (title, _)) in &self.lexicons[i] {
                let binding = Binding {
                    theme: Some(theme.id.clone()),
                    system: None,
                    key: key.clone(),
                    form: "primary".into(),
                    parent: None,
                };
                insert(
                    &mut index,
                    &title.fr,
                    &title.en,
                    &title.native,
                    binding.clone(),
                );
                for variant in &title.variants {
                    let mut binding = binding.clone();
                    binding.form = if variant.qualifier.is_empty() {
                        "alternative".into()
                    } else {
                        variant.qualifier.clone()
                    };
                    binding.parent = Some(Text::new(title.fr.clone(), title.en.clone()));
                    insert(
                        &mut index,
                        &variant.fr,
                        &variant.en,
                        &variant.native,
                        binding,
                    );
                    variant_bindings += 1;
                }
            }
        }
        let mut uses: BTreeMap<String, Vec<Value>> = BTreeMap::new();
        for system in &self.content.systems {
            for role in &system.roles {
                uses.entry(role.key.clone()).or_default().push(json!({
                    "system":system.id,"role":role.id,"function":role.function,
                    "family":system.family,"scope":role.scope,"level":role.level,
                    "importance":role.importance,"duties":role.duties,
                    "collective":role.collective,"optional":role.optional,"powers":role.powers
                }));
                if let Some(title) = &role.title {
                    insert(
                        &mut index,
                        &title.fr,
                        &title.en,
                        &None,
                        Binding {
                            theme: None,
                            system: Some(system.id.clone()),
                            key: role.key.clone(),
                            form: "functional".into(),
                            parent: None,
                        },
                    );
                }
            }
        }
        // Include keys present only in a lexicon too; they are content even when no
        // current system assigns the corresponding office.
        for term in index.values() {
            for binding in &term.bindings {
                uses.entry(binding.key.clone()).or_default();
            }
        }
        let generic = self
            .content
            .themes
            .iter()
            .find(|theme| theme.id == "generic");
        let functions: Vec<Value> = uses
            .into_iter()
            .map(|(key, roles)| {
                let label = generic
                    .and_then(|t| t.titles.get(&key))
                    .map(|t| Text::new(t.fr.clone(), t.en.clone()))
                    .or_else(|| {
                        self.content
                            .systems
                            .iter()
                            .flat_map(|s| &s.roles)
                            .find(|r| r.key == key)
                            .and_then(|r| r.title.clone())
                    })
                    .unwrap_or_else(|| Text::new(key.replace('_', " "), key.replace('_', " ")));
                json!({"key":key,"label":label,"uses":roles})
            })
            .collect();
        let terms: Vec<Term> = index.into_values().collect();
        json!({
            "api_version":"2.0","content_version":env!("CARGO_PKG_VERSION"),
            "counts":{"terms":terms.len(),"functions":functions.len(),
                "roles":self.content.systems.iter().map(|s|s.roles.len()).sum::<usize>(),
                "systems":self.content.systems.len(),"themes":self.content.themes.len(),
                "authored_title_entries":self.content.themes.iter().map(|t|t.titles.len()).sum::<usize>(),
                "effective_title_entries":self.lexicons.iter().map(|l|l.len()).sum::<usize>(),
                "variant_bindings":variant_bindings,"powers":self.content.powers.len()},
            "terms":terms,"functions":functions,
            "themes":self.content.themes.iter().map(|t|json!({"id":t.id,"label":t.label,"description":t.description})).collect::<Vec<_>>(),
            "systems":self.content.systems.iter().map(|s|json!({"id":s.id,"label":s.label,"family":s.family,"description":s.description,"role_count":s.roles.len()})).collect::<Vec<_>>(),
            "powers":self.content.powers.iter().map(|(id,label)|json!({"id":id,"label":label})).collect::<Vec<_>>()
        })
    }
}
