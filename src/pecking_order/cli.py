"""CLI: the same request and response contract as Python and HTTP."""

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .models import Dataset, Query, Resolution
from .resolver import KnowledgeBase
from .server import serve


def main():
    # Keep native titles intact in Windows redirected output as well as terminals.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Pecking Order institutional knowledge base")
    parser.add_argument("--data", type=Path, help="Use a complete custom dataset JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog")
    sub.add_parser("validate")
    resolve = sub.add_parser("resolve")
    resolve.add_argument("request", help="JSON file path, or - for standard input")
    schema = sub.add_parser("schema")
    schema.add_argument("model", choices=["query", "response", "dataset"])
    studio = sub.add_parser("studio")
    studio.add_argument("--port", type=int, default=8773)
    args = parser.parse_args()
    try:
        if args.command == "studio":
            serve(args.port, args.data)
            return
        if args.command == "schema":
            output = {"query": Query, "response": Resolution, "dataset": Dataset}[
                args.model].model_json_schema()
        else:
            kb = KnowledgeBase(args.data)
            if args.command == "catalog":
                output = kb.catalog()
            elif args.command == "validate":
                output = {"valid": True, "kb_digest": kb.digest, **kb.catalog()["coverage"]}
            else:
                raw = sys.stdin.read() if args.request == "-" else Path(args.request).read_text(
                    encoding="utf-8-sig")
                output = kb.resolve(Query.model_validate_json(raw)).model_dump(mode="json")
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except (ValidationError, ValueError, OSError) as exc:
        print(json.dumps({"error": "invalid_input", "message": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        raise SystemExit(2) from exc
