use std::{env, fs, path::PathBuf};

fn main() {
    let mut catalog = serde_json::Map::new();
    for (key, paths) in [
        (
            "systems",
            vec![
                "data/systems.json",
                "data/systems_specialist.json",
                "data/systems_civic_military.json",
            ],
        ),
        (
            "themes",
            vec![
                "data/themes_base.json",
                "data/themes_world.json",
                "data/themes_fantasy.json",
            ],
        ),
        ("city_cultures", vec!["data/city_cultures.json"]),
    ] {
        let mut rows = Vec::new();
        for path in paths {
            println!("cargo:rerun-if-changed={path}");
            let raw =
                fs::read_to_string(path).unwrap_or_else(|e| panic!("Missing content {path}: {e}"));
            let value: serde_json::Value = serde_json::from_str(raw.trim_start_matches('\u{feff}'))
                .unwrap_or_else(|e| panic!("Invalid content in {path}: {e}"));
            rows.extend(value.as_array().expect("Content must be an array").clone());
        }
        catalog.insert(key.into(), rows.into());
    }
    let mut powers = serde_json::Map::new();
    for path in [
        "data/powers_systems.json",
        "data/powers_specialist.json",
        "data/powers_civic_military.json",
        "data/powers_context.json",
        "data/powers.json",
    ] {
        println!("cargo:rerun-if-changed={path}");
        let raw = fs::read_to_string(path)
            .unwrap_or_else(|e| panic!("Missing power glossary {path}: {e}"));
        let value: serde_json::Value =
            serde_json::from_str(raw.trim_start_matches('\u{feff}')).unwrap();
        powers.extend(
            value
                .as_object()
                .expect("Power labels must be an object")
                .clone(),
        );
    }
    catalog.insert("powers".into(), powers.into());
    let destination = PathBuf::from(env::var_os("OUT_DIR").expect("OUT_DIR"));
    fs::write(
        destination.join("catalog.json"),
        serde_json::to_vec(&catalog).unwrap(),
    )
    .unwrap();
}
