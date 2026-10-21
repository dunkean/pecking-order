use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Default, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
pub struct Text {
    pub fr: String,
    pub en: String,
    #[serde(flatten)]
    pub other: BTreeMap<String, String>,
}

impl Text {
    pub fn new(fr: impl Into<String>, en: impl Into<String>) -> Self {
        Self {
            fr: fr.into(),
            en: en.into(),
            other: BTreeMap::new(),
        }
    }

    pub fn get(&self, locale: &str) -> &str {
        match locale.split('-').next().unwrap_or("fr") {
            "fr" => &self.fr,
            "en" => &self.en,
            other => self
                .other
                .get(locale)
                .or_else(|| self.other.get(other))
                .map_or(&self.en, String::as_str),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
pub struct TitleVariant {
    pub fr: String,
    pub en: String,
    #[serde(default)]
    pub native: Option<String>,
    #[serde(default)]
    pub qualifier: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
pub struct Title {
    pub fr: String,
    pub en: String,
    #[serde(default)]
    pub native: Option<String>,
    #[serde(default)]
    pub variants: Vec<TitleVariant>,
    #[serde(flatten)]
    pub other: BTreeMap<String, String>,
}

impl Title {
    pub fn new(fr: impl Into<String>, en: impl Into<String>) -> Self {
        Self {
            fr: fr.into(),
            en: en.into(),
            native: None,
            variants: Vec::new(),
            other: BTreeMap::new(),
        }
    }
    pub fn get(&self, locale: &str) -> &str {
        match locale.split('-').next().unwrap_or("fr") {
            "fr" => &self.fr,
            "en" => &self.en,
            other => self
                .other
                .get(locale)
                .or_else(|| self.other.get(other))
                .map_or(&self.en, String::as_str),
        }
    }
}

#[derive(
    Debug, Clone, Copy, Default, Serialize, Deserialize, JsonSchema, PartialEq, Eq, PartialOrd, Ord,
)]
#[serde(rename_all = "snake_case")]
pub enum Size {
    Tiny,
    Small,
    Medium,
    Large,
    Vast,
    #[default]
    Full,
}

impl Size {
    pub fn from_members(count: u32) -> Self {
        match count {
            0..=5 => Self::Tiny,
            6..=30 => Self::Small,
            31..=300 => Self::Medium,
            301..=10_000 => Self::Large,
            _ => Self::Vast,
        }
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Structure {
    Hierarchical,
    Horizontal,
    Network,
    Cellular,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Authority {
    Hereditary,
    Aristocratic,
    Authoritarian,
    Democratic,
    Theocratic,
    Military,
    Bureaucratic,
    Meritocratic,
    Consensual,
    Personal,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, JsonSchema)]
#[serde(default, deny_unknown_fields)]
pub struct RoleFilter {
    pub text: String,
    pub max_level: Option<u8>,
    pub min_importance: Option<u8>,
    pub functions: Vec<String>,
    pub scopes: Vec<String>,
}

fn locale() -> String {
    "fr".into()
}
fn generic() -> String {
    "generic".into()
}
fn version() -> String {
    "2.0".into()
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Query {
    #[serde(default = "version")]
    pub api_version: String,
    pub system: String,
    #[serde(default = "generic")]
    pub theme: String,
    #[serde(default)]
    pub size: Size,
    #[serde(default)]
    pub members: Option<u32>,
    #[serde(default)]
    pub structure: Option<Structure>,
    #[serde(default)]
    pub authority: Option<Authority>,
    #[serde(default = "locale")]
    pub locale: String,
    #[serde(default)]
    pub filter: RoleFilter,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct RoleSpec {
    pub id: String,
    pub key: String,
    pub function: String,
    pub level: u8,
    pub importance: u8,
    pub scope: String,
    pub min_size: Size,
    #[serde(default)]
    pub reports_to: Vec<String>,
    pub duties: Text,
    pub powers: Vec<String>,
    #[serde(default)]
    pub collective: bool,
    #[serde(default)]
    pub optional: bool,
    #[serde(default)]
    pub title: Option<Text>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct System {
    pub id: String,
    pub family: String,
    pub label: Text,
    #[serde(default)]
    pub aliases: Vec<String>,
    pub description: Text,
    pub default_structure: Structure,
    pub default_authority: Authority,
    #[serde(default)]
    pub related: Vec<String>,
    pub roles: Vec<RoleSpec>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct Theme {
    pub id: String,
    pub label: Text,
    pub aliases: Vec<String>,
    #[serde(default)]
    pub parent: Option<String>,
    pub description: Text,
    pub titles: BTreeMap<String, Title>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct CultureRef {
    pub id: String,
    pub label: String,
    pub fantasy: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Content {
    pub systems: Vec<System>,
    pub themes: Vec<Theme>,
    pub city_cultures: Vec<CultureRef>,
    #[serde(default)]
    pub powers: BTreeMap<String, Text>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct Power {
    pub id: String,
    pub label: Text,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct Role {
    pub id: String,
    pub function: String,
    pub title_key: String,
    pub title: Title,
    pub display_title: String,
    pub level: u8,
    pub importance: u8,
    pub scope: String,
    pub reports_to: Vec<String>,
    pub duties: Text,
    pub display_duties: String,
    pub powers: Vec<Power>,
    pub collective: bool,
    pub optional: bool,
    pub selection: Text,
    pub title_theme: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct RelatedSystem {
    pub id: String,
    pub label: Text,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct Response {
    pub api_version: String,
    pub content_version: String,
    pub request: Query,
    pub system: RelatedSystem,
    pub theme: RelatedSystem,
    pub description: Text,
    pub size: Size,
    pub structure: Structure,
    pub authority: Authority,
    pub roles: Vec<Role>,
    pub available_role_count: usize,
    pub related: Vec<RelatedSystem>,
    pub notes: Vec<Text>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub struct Error {
    pub code: String,
    pub field: String,
    pub message: Box<Text>,
    #[serde(default)]
    pub suggestions: Vec<RelatedSystem>,
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}: {}", self.code, self.message.en)
    }
}
impl std::error::Error for Error {}

pub fn error(code: &str, field: &str, fr: &str, en: &str) -> Error {
    Error {
        code: code.into(),
        field: field.into(),
        message: Box::new(Text::new(fr, en)),
        suggestions: Vec::new(),
    }
}
