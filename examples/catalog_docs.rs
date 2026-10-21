use pecking_order::Engine;
use std::{collections::BTreeSet, fmt::Write, fs};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let engine = Engine::embedded()?;
    let count = &engine.catalog()["counts"];
    let mut text = format!(
        "# Catalogue / Catalogue\n\nGénéré depuis les données embarquées avec `cargo run --example catalog_docs`.\n\n{} systèmes · {} thèmes · {} rôles définis · {} entrées de titres bilingues · {} cultures Magna Urbis.\n\n",
        count["systems"], count["themes"], count["roles"], count["titles"], count["city_cultures"]
    );
    let families: BTreeSet<_> = engine.content.systems.iter().map(|s| &s.family).collect();
    for family in families {
        writeln!(
            text,
            "## {family}\n\n| ID | Français | English | Rôles |\n|---|---|---|---:|"
        )?;
        for system in engine
            .content
            .systems
            .iter()
            .filter(|s| &s.family == family)
        {
            writeln!(
                text,
                "| `{}` | {} | {} | {} |",
                system.id,
                system.label.fr,
                system.label.en,
                system.roles.len()
            )?;
        }
        text.push('\n');
    }
    text.push_str("## Thèmes / Themes\n\n| ID | Français | English | Alias / Magna Urbis | Titres propres |\n|---|---|---|---|---:|\n");
    for theme in &engine.content.themes {
        writeln!(
            text,
            "| `{}` | {} | {} | {} | {} |",
            theme.id,
            theme.label.fr,
            theme.label.en,
            theme.aliases.join(", "),
            theme.titles.len()
        )?;
    }
    text.push_str("\nTous les systèmes se combinent avec tous les thèmes. Les clés absentes d’un lexique thématique utilisent son parent puis le lexique générique.\n\nAll systems combine with all themes. Missing theme terms inherit from a parent, then the generic lexicon.\n");
    fs::create_dir_all("docs")?;
    fs::write("docs/CATALOG.md", text)?;
    Ok(())
}
