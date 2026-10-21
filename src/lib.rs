//! Deterministic institutional content: system + size/organization + cultural theme.
mod engine;
pub mod model;
pub use engine::Engine;
pub use model::{Error, Query, Response};

pub fn resolve_json(request: &str) -> Result<String, Error> {
    let query: Query = serde_json::from_str(request).map_err(|e| {
        model::error(
            "invalid_request",
            "request",
            &format!("Requête JSON invalide : {e}"),
            &format!("Invalid JSON request: {e}"),
        )
    })?;
    let result = Engine::embedded()?.resolve(query)?;
    serde_json::to_string(&result)
        .map_err(|e| model::error("serialization", "response", &e.to_string(), &e.to_string()))
}
