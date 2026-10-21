"""Small loopback-only explorer and JSON API. No external services required."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import urlsplit

from pydantic import ValidationError

from .models import Dataset, Query, Resolution
from .resolver import KnowledgeBase

MAX_BODY = 32_768


def handler_for(kb: KnowledgeBase):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, body, content_type="application/json; charset=utf-8"):
            raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            path = urlsplit(self.path).path
            routes = {
                "/": ("index.html", "text/html; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/style.css": ("style.css", "text/css; charset=utf-8"),
                "/favicon.svg": ("favicon.svg", "image/svg+xml"),
            }
            if path in routes:
                name, mime = routes[path]
                self.send(200, files("pecking_order").joinpath("web", name).read_bytes(), mime)
            elif path == "/api/catalog":
                self.send(200, kb.catalog())
            elif path == "/api/sources":
                self.send(200, [s.model_dump(mode="json") for s in kb.data.sources])
            elif path in ("/api/schema/query", "/api/schema/response", "/api/schema/dataset"):
                model = {"query": Query, "response": Resolution, "dataset": Dataset}[path.rsplit("/", 1)[1]]
                self.send(200, model.model_json_schema())
            else:
                self.send(404, {"error": "not_found"})

        def do_POST(self):
            if urlsplit(self.path).path != "/api/resolve":
                self.send(404, {"error": "not_found"})
                return
            # Reject browser writes from foreign origins. JSON requests require same-origin
            # or no Origin (CLI/server clients). No wildcard CORS headers are emitted.
            origin = self.headers.get("Origin")
            if origin and origin != "http://" + self.headers.get("Host", ""):
                self.send(403, {"error": "foreign_origin"})
                return
            if self.headers.get_content_type() != "application/json":
                self.send(415, {"error": "json_required"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_BODY:
                    self.send(413, {"error": "body_size", "max_bytes": MAX_BODY})
                    return
                query = Query.model_validate_json(self.rfile.read(length))
            except (ValueError, ValidationError) as exc:
                details = exc.errors(include_url=False, include_context=False, include_input=False) if isinstance(
                    exc, ValidationError) else [{"msg": "Invalid content length"}]
                self.send(400, {"error": "invalid_query", "details": details})
                return
            self.send(200, kb.resolve(query).model_dump(mode="json"))

    return Handler


def serve(port=8773, data=None):
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(KnowledgeBase(data)))
    print(f"Pecking Order: http://127.0.0.1:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
