import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_emits_utf8_native_titles_when_windows_output_is_legacy_encoded(tmp_path):
    env = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
    completed = subprocess.run(
        [sys.executable, "-m", "pecking_order", "resolve", str(ROOT / "examples/joint-family.json")],
        cwd=tmp_path, env=env, capture_output=True, timeout=20, check=True,
    )
    result = json.loads(completed.stdout.decode("utf-8"))
    assert result["status"] == "resolved"
    assert result["blueprint"]["roles"][0]["title"]["native"] == "कर्ता"


def test_cli_invalid_input_has_nonzero_exit_and_json_error(tmp_path):
    request = tmp_path / "bad.json"
    request.write_text('{"unknown":true}', encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-m", "pecking_order", "resolve", str(request)],
        cwd=tmp_path, capture_output=True, timeout=20, check=False,
    )
    assert completed.returncode == 2
    assert json.loads(completed.stderr.decode("utf-8"))["error"] == "invalid_input"
