import json
from pathlib import Path

from pecking_order.models import Dataset, Query, Resolution

root = Path(__file__).resolve().parents[1] / "schemas"
root.mkdir(exist_ok=True)
for name, model in [("query", Query), ("response", Resolution), ("dataset", Dataset)]:
    (root / f"{name}.schema.json").write_text(
        json.dumps(model.model_json_schema(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

components = {}
for name, model in [("Query", Query), ("Resolution", Resolution), ("Dataset", Dataset)]:
    schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
    for key, value in schema.pop("$defs", {}).items():
        if key in components and components[key] != value:
            raise ValueError(f"Conflicting OpenAPI schema: {key}")
        components[key] = value
    components[name] = schema

openapi = {
    "openapi": "3.1.0",
    "info": {"title": "Pecking Order", "version": "1.0",
             "description": "Bilingual institutional blueprints and culture-scoped titles."},
    "servers": [{"url": "http://127.0.0.1:8773"}],
    "paths": {
        "/api/resolve": {"post": {
            "operationId": "resolveInstitution",
            "requestBody": {"required": True, "content": {"application/json": {
                "schema": {"$ref": "#/components/schemas/Query"}}}},
            "responses": {
                "200": {"description": "Resolution including explicit semantic status.",
                        "content": {"application/json": {"schema": {
                            "$ref": "#/components/schemas/Resolution"}}}},
                **{str(code): {"description": message} for code, message in [
                    (400, "Invalid JSON or request schema"), (403, "Foreign origin"),
                    (413, "Invalid body size; maximum 32768 bytes"),
                    (415, "Content-Type application/json required")
                ]},
            },
        }},
        "/api/catalog": {"get": {"operationId": "getCatalog", "responses": {
            "200": {"description": "Template and culture summaries, compatibility and coverage."}}}},
        "/api/sources": {"get": {"operationId": "getSources", "responses": {
            "200": {"description": "All source metadata.", "content": {"application/json": {
                "schema": {"type": "array", "items": {"$ref": "#/components/schemas/Source"}}}}}}}},
    },
    "components": {"schemas": components},
}
(root / "openapi.json").write_text(json.dumps(openapi, indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8")
