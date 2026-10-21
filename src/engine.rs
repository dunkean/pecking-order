use crate::model::*;
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet};
use unicode_normalization::{UnicodeNormalization, char::is_combining_mark};

const EMBEDDED: &str = include_str!(concat!(env!("OUT_DIR"), "/catalog.json"));

pub struct Engine {
    pub content: Content,
    system_aliases: BTreeMap<String, usize>,
    theme_aliases: BTreeMap<String, usize>,
    pub(crate) lexicons: Vec<BTreeMap<String, (Title, String)>>,
}

fn normalize(input: &str) -> String {
    input
        .nfkd()
        .filter(|ch| !is_combining_mark(*ch))
        .collect::<String>()
        .to_lowercase()
        .split(|ch: char| !ch.is_alphanumeric())
        .filter(|s| !s.is_empty())
        .collect::<Vec<_>>()
        .join("-")
}

fn content_error(message: impl Into<String>) -> Error {
    let text = message.into();
    error("invalid_content", "content", &text, &text)
}

impl Engine {
    pub fn embedded() -> Result<Self, Error> {
        Self::from_json(EMBEDDED)
    }

    pub fn from_json(data: &str) -> Result<Self, Error> {
        let content: Content = serde_json::from_str(data.trim_start_matches('\u{feff}'))
            .map_err(|e| content_error(e.to_string()))?;
        let mut engine = Self {
            content,
            system_aliases: BTreeMap::new(),
            theme_aliases: BTreeMap::new(),
            lexicons: Vec::new(),
        };
        let mut ids = BTreeSet::new();
        for (i, system) in engine.content.systems.iter().enumerate() {
            if !ids.insert(system.id.clone()) {
                return Err(content_error(format!("Duplicate system: {}", system.id)));
            }
            engine.system_aliases.insert(normalize(&system.id), i);
            for alias in system
                .aliases
                .iter()
                .chain([&system.label.fr, &system.label.en])
            {
                engine.system_aliases.entry(normalize(alias)).or_insert(i);
            }
            validate_system(system)?;
        }
        // Canonical IDs always win over a broad alias.
        for (i, system) in engine.content.systems.iter().enumerate() {
            engine.system_aliases.insert(normalize(&system.id), i);
        }
        for (alias, target) in [
            ("guild", "craft_guild"),
            ("guilde", "craft_guild"),
            ("family", "joint_family"),
            ("famille", "joint_family"),
            ("household", "joint_family"),
            ("religion", "priesthood"),
            ("state", "nation"),
            ("etat", "nation"),
        ] {
            if let Some(&index) = engine.system_aliases.get(&normalize(target)) {
                engine
                    .system_aliases
                    .entry(normalize(alias))
                    .or_insert(index);
            }
        }
        ids.clear();
        for (i, theme) in engine.content.themes.iter().enumerate() {
            if !ids.insert(theme.id.clone()) {
                return Err(content_error(format!("Duplicate theme: {}", theme.id)));
            }
            for alias in theme
                .aliases
                .iter()
                .chain([&theme.id, &theme.label.fr, &theme.label.en])
            {
                engine.theme_aliases.entry(normalize(alias)).or_insert(i);
            }
            if theme.label.fr.is_empty() || theme.label.en.is_empty() {
                return Err(content_error(format!(
                    "Missing theme translation: {}",
                    theme.id
                )));
            }
        }
        for (i, theme) in engine.content.themes.iter().enumerate() {
            engine.theme_aliases.insert(normalize(&theme.id), i);
        }
        for (aliases, target) in [
            (
                vec![
                    "europe de l'ouest",
                    "europe ouest",
                    "western europe",
                    "europe occidentale",
                ],
                "western-europe",
            ),
            (
                vec![
                    "europe de l'est",
                    "europe est",
                    "eastern europe",
                    "europe orientale",
                    "russe",
                    "russian",
                ],
                "eastern-europe",
            ),
            (vec!["hindou", "hindu", "indian", "inde"], "indian-temple"),
        ] {
            if let Some(&index) = engine.theme_aliases.get(&normalize(target)) {
                for alias in aliases {
                    engine
                        .theme_aliases
                        .entry(normalize(alias))
                        .or_insert(index);
                }
            }
        }
        if !engine.theme_aliases.contains_key("generic") {
            return Err(content_error("Missing generic lexicon"));
        }
        for index in 0..engine.content.themes.len() {
            engine
                .lexicons
                .push(engine.build_lexicon(index, &mut BTreeSet::new())?);
        }
        for system in &engine.content.systems {
            for related in &system.related {
                if !engine.system_aliases.contains_key(&normalize(related)) {
                    return Err(content_error(format!(
                        "Unknown related system: {related} ({})",
                        system.id
                    )));
                }
            }
        }
        for city in &engine.content.city_cultures {
            if !engine.theme_aliases.contains_key(&normalize(&city.id)) {
                return Err(content_error(format!(
                    "City culture not covered: {}",
                    city.id
                )));
            }
        }
        Ok(engine)
    }

    fn build_lexicon(
        &self,
        index: usize,
        path: &mut BTreeSet<usize>,
    ) -> Result<BTreeMap<String, (Title, String)>, Error> {
        if !path.insert(index) {
            return Err(content_error("Cyclic theme inheritance"));
        }
        let theme = &self.content.themes[index];
        let generic = self.theme_aliases["generic"];
        let parent = if let Some(parent) = &theme.parent {
            Some(
                *self
                    .theme_aliases
                    .get(&normalize(parent))
                    .ok_or_else(|| content_error(format!("Unknown theme parent: {parent}")))?,
            )
        } else if index != generic {
            Some(generic)
        } else {
            None
        };
        let mut titles = if let Some(parent) = parent {
            self.build_lexicon(parent, path)?
        } else {
            BTreeMap::new()
        };
        for (key, title) in &theme.titles {
            if title.fr.trim().is_empty() || title.en.trim().is_empty() {
                return Err(content_error(format!("Empty title: {}.{key}", theme.id)));
            }
            titles.insert(key.clone(), (title.clone(), theme.id.clone()));
        }
        path.remove(&index);
        Ok(titles)
    }

    pub fn catalog(&self) -> Value {
        let role_count: usize = self.content.systems.iter().map(|s| s.roles.len()).sum();
        let title_count: usize = self.content.themes.iter().map(|t| t.titles.len()).sum();
        json!({
            "api_version":"2.0", "content_version":env!("CARGO_PKG_VERSION"),
            "counts":{"systems":self.content.systems.len(),"themes":self.content.themes.len(),
                "roles":role_count,"titles":title_count,"city_cultures":self.content.city_cultures.len()},
            "systems":self.content.systems.iter().map(|s| json!({"id":s.id,"family":s.family,
                "label":s.label,"description":s.description,"role_count":s.roles.len(),
                "max_level":s.roles.iter().map(|r|r.level).max().unwrap_or(0),
                "default_structure":s.default_structure,"default_authority":s.default_authority})).collect::<Vec<_>>(),
            "themes":self.content.themes.iter().enumerate().map(|(i,t)|json!({"id":t.id,"label":t.label,
                "description":t.description,"aliases":t.aliases,"parent":t.parent,
                "title_count":t.titles.len(),"effective_title_count":self.lexicons[i].len()})).collect::<Vec<_>>(),
            "city_cultures":self.content.city_cultures,
            "system_aliases":self.system_aliases.iter().map(|(alias,&i)|(alias,&self.content.systems[i].id)).collect::<BTreeMap<_,_>>(),
            "theme_aliases":self.theme_aliases.iter().map(|(alias,&i)|(alias,&self.content.themes[i].id)).collect::<BTreeMap<_,_>>(),
            "sizes":["full","tiny","small","medium","large","vast"],
            "structures":["hierarchical","horizontal","network","cellular"],
            "authorities":["hereditary","aristocratic","authoritarian","democratic","theocratic",
                "military","bureaucratic","meritocratic","consensual","personal"]
        })
    }

    pub fn theme_lexicon(&self, name: &str) -> Result<Value, Error> {
        let i = *self
            .theme_aliases
            .get(&normalize(name))
            .ok_or_else(|| self.unknown("theme", name))?;
        let theme = &self.content.themes[i];
        Ok(
            json!({"id":theme.id,"label":theme.label,"description":theme.description,
            "titles":self.lexicons[i].iter().map(|(k,(v,source))|(k,json!({"title":v,"theme":source}))).collect::<BTreeMap<_,_>>()}),
        )
    }

    fn unknown(&self, field: &str, name: &str) -> Error {
        let mut e = error(
            "unknown_selection",
            field,
            &format!("Choix inconnu : {name}"),
            &format!("Unknown selection: {name}"),
        );
        let needle = normalize(name);
        let choices = if field == "system" {
            self.content
                .systems
                .iter()
                .map(|s| RelatedSystem {
                    id: s.id.clone(),
                    label: s.label.clone(),
                })
                .collect::<Vec<_>>()
        } else {
            self.content
                .themes
                .iter()
                .map(|t| RelatedSystem {
                    id: t.id.clone(),
                    label: t.label.clone(),
                })
                .collect()
        };
        e.suggestions = choices
            .into_iter()
            .filter(|c| {
                normalize(&c.id).contains(&needle)
                    || normalize(&c.label.fr).contains(&needle)
                    || normalize(&c.label.en).contains(&needle)
            })
            .take(12)
            .collect();
        e
    }

    pub fn resolve(&self, mut query: Query) -> Result<Response, Error> {
        if query.api_version != "2.0" {
            return Err(error(
                "version",
                "api_version",
                "Utilisez api_version 2.0.",
                "Use api_version 2.0.",
            ));
        }
        if query.members == Some(0) {
            return Err(error(
                "members",
                "members",
                "L’effectif doit être positif.",
                "Member count must be positive.",
            ));
        }
        if query.filter.min_importance.is_some_and(|x| x > 100) {
            return Err(error(
                "importance",
                "filter.min_importance",
                "L’importance va de 0 à 100.",
                "Importance ranges from 0 to 100.",
            ));
        }
        if query.locale.len() > 35
            || query.locale.is_empty()
            || !query
                .locale
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || b == b'-')
        {
            return Err(error(
                "locale",
                "locale",
                "Code de langue invalide.",
                "Invalid language tag.",
            ));
        }
        let system_i = *self
            .system_aliases
            .get(&normalize(&query.system))
            .ok_or_else(|| self.unknown("system", &query.system))?;
        let theme_i = *self
            .theme_aliases
            .get(&normalize(&query.theme))
            .ok_or_else(|| self.unknown("theme", &query.theme))?;
        let system = &self.content.systems[system_i];
        let theme = &self.content.themes[theme_i];
        query.system.clone_from(&system.id);
        query.theme.clone_from(&theme.id);
        let size = if let Some(count) = query.members {
            Size::from_members(count)
        } else {
            query.size
        };
        let structure = query.structure.unwrap_or(system.default_structure);
        let authority = query.authority.unwrap_or(system.default_authority);
        let mut specs = system.roles.clone();
        if query.authority.is_some() {
            for spec in &mut specs {
                adapt_authority(spec, authority, &system.family);
            }
        }
        if [Structure::Horizontal, Structure::Network].contains(&structure) {
            for spec in &mut specs {
                spec.reports_to.clear();
                if structure == Structure::Horizontal {
                    spec.level = 0;
                    spec.powers.retain(|p| {
                        ![
                            "command",
                            "decree",
                            "legislate_unilaterally",
                            "veto",
                            "punish",
                        ]
                        .contains(&p.as_str())
                    });
                    if query.structure == Some(Structure::Horizontal)
                        && system.default_structure != Structure::Horizontal
                        && system.family != "kinship"
                        && executive_key(&spec.key)
                    {
                        spec.key = "representative".into();
                    }
                }
            }
        }
        if authority == Authority::Authoritarian
            && query.authority.is_some()
            && structure == Structure::Hierarchical
            && let Some(head) = specs
                .iter()
                .filter(|s| !s.collective && s.level == 0)
                .max_by_key(|s| s.importance)
                .map(|s| s.id.clone())
        {
            for spec in &mut specs {
                if spec.id != head && spec.level == 0 {
                    spec.level = 1;
                    spec.reports_to = vec![head.clone()];
                }
            }
        }
        let available_role_count = specs.len();
        let lexicon = &self.lexicons[theme_i];
        let search = normalize(&query.filter.text);
        let selected: BTreeSet<String> = specs
            .iter()
            .filter(|r| size == Size::Full || r.min_size <= size)
            .filter(|r| query.filter.max_level.is_none_or(|m| r.level <= m))
            .filter(|r| {
                query
                    .filter
                    .min_importance
                    .is_none_or(|m| r.importance >= m)
            })
            .filter(|r| {
                query.filter.functions.is_empty() || query.filter.functions.contains(&r.function)
            })
            .filter(|r| query.filter.scopes.is_empty() || query.filter.scopes.contains(&r.scope))
            .filter(|r| {
                if search.is_empty() {
                    return true;
                }
                let title = lexicon
                    .get(&r.key)
                    .map(|(t, _)| {
                        format!("{} {} {}", t.fr, t.en, t.native.as_deref().unwrap_or(""))
                    })
                    .or_else(|| r.title.as_ref().map(|t| format!("{} {}", t.fr, t.en)))
                    .unwrap_or_default();
                normalize(&format!("{} {} {} {}", r.id, r.function, r.key, title)).contains(&search)
            })
            .map(|r| r.id.clone())
            .collect();
        let mut roles = Vec::new();
        for spec in &specs {
            if !selected.contains(&spec.id) {
                continue;
            }
            let (title, title_theme) = if let Some((title, origin)) = lexicon.get(&spec.key) {
                (title.clone(), origin.clone())
            } else if let Some(title) = &spec.title {
                (
                    Title::new(title.fr.clone(), title.en.clone()),
                    "functional".into(),
                )
            } else {
                return Err(content_error(format!(
                    "Missing title key: {} ({})",
                    spec.key, system.id
                )));
            };
            let mut parents = BTreeSet::new();
            surviving_parents(spec, &specs, &selected, &mut BTreeSet::new(), &mut parents);
            let powers =
                spec.powers
                    .iter()
                    .map(|id| Power {
                        id: id.clone(),
                        label: self.content.powers.get(id).cloned().unwrap_or_else(|| {
                            Text::new(id.replace('_', " "), id.replace('_', " "))
                        }),
                    })
                    .collect();
            roles.push(Role {
                id: spec.id.clone(),
                function: spec.function.clone(),
                title_key: spec.key.clone(),
                display_title: title.get(&query.locale).into(),
                title,
                level: spec.level,
                importance: spec.importance,
                scope: spec.scope.clone(),
                reports_to: parents.into_iter().collect(),
                duties: spec.duties.clone(),
                display_duties: spec.duties.get(&query.locale).into(),
                powers,
                collective: spec.collective,
                optional: spec.optional,
                selection: selection(authority, spec),
                title_theme,
            });
        }
        roles.sort_by(|a, b| {
            a.level
                .cmp(&b.level)
                .then(b.importance.cmp(&a.importance))
                .then(a.id.cmp(&b.id))
        });
        let mut notes = vec![Text::new(
            "Le niveau indique la place dans cette organisation ; l’importance mesure le poids du rôle, de 0 à 100.",
            "Level is the position within this organization; importance measures the role's weight from 0 to 100.",
        )];
        if query.members.is_some() {
            notes.push(Text::new("L’effectif sélectionne la complexité de la structure ; plusieurs fonctions peuvent être cumulées par une personne.",
            "Headcount selects structural complexity; one person may hold several offices."));
        }
        if structure == Structure::Horizontal {
            notes.push(Text::new("Structure horizontale : les fonctions sont différenciées, sans chaîne de commandement.",
            "Horizontal structure: functions remain distinct without a command hierarchy."));
        }
        let related = system
            .related
            .iter()
            .filter_map(|id| self.system_aliases.get(&normalize(id)))
            .map(|&i| {
                let other = &self.content.systems[i];
                RelatedSystem {
                    id: other.id.clone(),
                    label: other.label.clone(),
                }
            })
            .collect();
        Ok(Response {
            api_version: "2.0".into(),
            content_version: env!("CARGO_PKG_VERSION").into(),
            request: query,
            system: RelatedSystem {
                id: system.id.clone(),
                label: system.label.clone(),
            },
            theme: RelatedSystem {
                id: theme.id.clone(),
                label: theme.label.clone(),
            },
            description: system.description.clone(),
            size,
            structure,
            authority,
            roles,
            available_role_count,
            related,
            notes,
        })
    }
}

fn validate_system(system: &System) -> Result<(), Error> {
    if system.label.fr.is_empty() || system.label.en.is_empty() || system.roles.is_empty() {
        return Err(content_error(format!("Empty system: {}", system.id)));
    }
    let mut ids = BTreeSet::new();
    for role in &system.roles {
        if !ids.insert(&role.id)
            || role.importance > 100
            || role.duties.fr.trim().is_empty()
            || role.duties.en.trim().is_empty()
        {
            return Err(content_error(format!(
                "Invalid role: {}.{}",
                system.id, role.id
            )));
        }
    }
    fn visit(id: &str, system: &System, path: &mut BTreeSet<String>) -> Result<(), Error> {
        if !path.insert(id.into()) {
            return Err(content_error(format!("Reporting cycle in {}", system.id)));
        }
        let role = system
            .roles
            .iter()
            .find(|r| r.id == id)
            .ok_or_else(|| content_error(format!("Unknown parent: {}.{id}", system.id)))?;
        for parent in &role.reports_to {
            visit(parent, system, path)?;
        }
        path.remove(id);
        Ok(())
    }
    for role in &system.roles {
        visit(&role.id, system, &mut BTreeSet::new())?;
    }
    Ok(())
}

fn surviving_parents(
    spec: &RoleSpec,
    all: &[RoleSpec],
    selected: &BTreeSet<String>,
    visited: &mut BTreeSet<String>,
    out: &mut BTreeSet<String>,
) {
    for parent in &spec.reports_to {
        if !visited.insert(parent.clone()) {
            continue;
        }
        if selected.contains(parent) {
            out.insert(parent.clone());
        } else if let Some(role) = all.iter().find(|r| r.id == *parent) {
            surviving_parents(role, all, selected, visited, out);
        }
    }
}

fn executive_key(key: &str) -> bool {
    [
        "king",
        "emperor",
        "head_of_state",
        "head_of_government",
        "elected_leader",
        "guildmaster",
        "grandmaster",
        "cult_leader",
        "cell_leader",
        "family_head",
        "clan_head",
        "mayor",
        "village_head",
        "commander",
    ]
    .contains(&key)
}

fn adapt_authority(role: &mut RoleSpec, authority: Authority, family: &str) {
    let state_head =
        ["king", "emperor", "head_of_state", "elected_leader"].contains(&role.key.as_str());
    if state_head && ["political", "administrative", "government"].contains(&family) {
        role.key = match authority {
            Authority::Democratic | Authority::Consensual => "elected_leader",
            Authority::Theocratic => "high_priest",
            Authority::Military => "marshal",
            Authority::Aristocratic | Authority::Hereditary | Authority::Authoritarian => {
                if role.key == "emperor" {
                    "emperor"
                } else {
                    "king"
                }
            }
            _ => "head_of_state",
        }
        .into();
    }
    if authority == Authority::Aristocratic
        && ["assembly", "councillor"].contains(&role.key.as_str())
        && role.collective
    {
        role.key = "council_nobles".into();
    }
    if authority == Authority::Authoritarian {
        if executive_key(&role.key) && role.level == 0 {
            role.powers.push("decree".into());
        } else {
            role.powers
                .retain(|p| !["veto", "elect_head", "depose"].contains(&p.as_str()));
        }
    }
}

fn selection(authority: Authority, role: &RoleSpec) -> Text {
    if role.collective {
        return Text::new(
            "Composition de l’organe selon les règles du groupe.",
            "Body membership follows the group's own rules.",
        );
    }
    if ["novice", "apprentice", "initiate"].contains(&role.key.as_str()) {
        return Text::new(
            "Admission, parrainage et période de formation ou d’initiation.",
            "Admission, sponsorship and a period of training or initiation.",
        );
    }
    if ["royal_heir"].contains(&role.key.as_str()) {
        return Text::new(
            "Reconnaissance au sein de la lignée ou désignation selon les règles de succession.",
            "Recognition within the lineage or designation under succession rules.",
        );
    }
    if [
        "soldier", "guard", "artisan", "laborer", "member", "retainer", "adept",
    ]
    .contains(&role.key.as_str())
    {
        return Text::new(
            "Recrutement, affiliation ou service dû ; obligations et compétences requises par le groupe.",
            "Recruitment, affiliation or owed service; obligations and skills required by the group.",
        );
    }
    if [
        "craft_master",
        "journeyman",
        "teacher",
        "scholar",
        "healer",
        "chief_engineer",
    ]
    .contains(&role.key.as_str())
    {
        return Text::new(
            "Maîtrise reconnue, apprentissage achevé, examen ou désignation professionnelle.",
            "Recognized mastery, completed training, examination or professional appointment.",
        );
    }
    if authority == Authority::Hereditary && !executive_key(&role.key) {
        return Text::new(
            "Nomination par le titulaire compétent, délégation ou attribution par la coutume.",
            "Appointment by the competent officeholder, delegation or assignment by custom.",
        );
    }
    match authority {
        Authority::Hereditary => Text::new(
            "Transmission, désignation ou délégation au sein des lignées reconnues.",
            "Succession, designation or delegation within recognized lineages.",
        ),
        Authority::Aristocratic => Text::new(
            "Choix parmi les maisons, familles ou ordres privilégiés.",
            "Selection among privileged houses, families or estates.",
        ),
        Authority::Authoritarian => Text::new(
            "Désignation et révocation par l’autorité centrale.",
            "Appointment and removal by the central authority.",
        ),
        Authority::Democratic => Text::new(
            "Élection ou mandat délégué par des représentants élus.",
            "Election or a mandate delegated by elected representatives.",
        ),
        Authority::Theocratic => Text::new(
            "Investiture religieuse et reconnaissance par les détenteurs de l’autorité sacrée.",
            "Religious investiture and recognition by holders of sacred authority.",
        ),
        Authority::Military => Text::new(
            "Nomination dans la chaîne de commandement et promotion au mérite militaire.",
            "Appointment within the command chain and promotion for military merit.",
        ),
        Authority::Bureaucratic => Text::new(
            "Nomination administrative, compétence et ancienneté de service.",
            "Administrative appointment, qualification and length of service.",
        ),
        Authority::Meritocratic => Text::new(
            "Compétence démontrée, examen, maîtrise ou réussite reconnue.",
            "Demonstrated competence, examination, mastery or recognized achievement.",
        ),
        Authority::Consensual => Text::new(
            "Consentement des membres, rotation ou délégation révocable.",
            "Members' consent, rotation or revocable delegation.",
        ),
        Authority::Personal => Text::new(
            "Confiance personnelle, fidélité et reconnaissance des membres.",
            "Personal trust, loyalty and recognition by members.",
        ),
    }
}
