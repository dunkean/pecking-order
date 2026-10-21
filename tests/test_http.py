import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from pecking_order import KnowledgeBase
from pecking_order.server import handler_for


@pytest.fixture(scope="module")
def server():
    instance = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(KnowledgeBase()))
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{instance.server_port}"
    instance.shutdown()
    instance.server_close()
    thread.join()


def post(server, raw, content_type="application/json", origin=None):
    headers = {"Content-Type": content_type}
    if origin:
        headers["Origin"] = origin
    request = Request(server + "/api/resolve", data=raw, headers=headers)
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)
    except HTTPError as exc:
        return exc.code, json.load(exc)


def test_api_and_static_assets(server):
    for path in ("/", "/style.css", "/app.js", "/api/catalog", "/api/sources",
                 "/api/schema/query", "/api/schema/response", "/api/schema/dataset"):
        with urlopen(server + path, timeout=5) as response:
            assert response.status == 200
            assert response.headers["X-Content-Type-Options"] == "nosniff"
    query = {"culture": "tswana", "organization": {"kind": "village_council", "scale": "local"}}
    status, body = post(server, json.dumps(query).encode())
    assert status == 200
    assert body["status"] == "resolved"
    assert body["blueprint"]["roles"][0]["title"]["native"] == "Kgosi"


@pytest.mark.parametrize("raw,status", [(b"not json", 400), (b"[]", 400),
                                        (b'{"culture":42}', 400), (b"\xff", 400),
                                        (b"x" * 32769, 413), (b"", 413)],
                         ids=["syntax", "array", "type", "encoding", "oversized", "empty"])
def test_malformed_and_oversized_input_is_json_error(server, raw, status):
    assert post(server, raw)[0] == status


def test_cross_origin_and_wrong_content_type(server):
    assert post(server, b"{}", origin="https://example.com")[0] == 403
    assert post(server, b"{}", content_type="text/plain")[0] == 415


def test_semantic_failure_is_a_valid_response_not_http_failure(server):
    status, result = post(server, b'{"culture":"africain","organization":{"kind":"village_council","scale":"local"}}')
    assert status == 200
    assert result["status"] == "needs_context"
