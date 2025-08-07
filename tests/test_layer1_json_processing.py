"""Tests for processing N8N exported JSON files with Layer 1 formatter."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from integrations.database.sqlite_manager import SWAILiteManager


# Load the processing module dynamically since ``scripts`` is not a package.
MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "process_n8n_json_layer1.py"
spec = importlib.util.spec_from_file_location("process_n8n_json_layer1", MODULE_PATH)
process_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(process_module)  # type: ignore[attr-defined]
process_directory = process_module.process_directory


def _write_json(directory: Path, name: str, obj: dict) -> Path:
    path = directory / name
    path.write_text(json.dumps(obj))
    return path


def _payload(message_id: str, **extra) -> dict:
    data = {
        "id": message_id,
        "timestamp": extra.pop("timestamp", 1),
        "from": extra.pop("sender", "111"),
        "to": extra.pop("receiver", "222"),
        "text": {"body": extra.pop("text", "hello")},
    }
    data.update(extra)
    return {"data": data}


def _db_rows(db_path: Path) -> int:
    manager = SWAILiteManager(str(db_path))
    count = manager.conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    manager.close()
    return count


def test_process_valid_json_saves_to_db(tmp_path: Path) -> None:
    db_path = tmp_path / "db.sqlite"
    _write_json(tmp_path, "msg.json", _payload("abc123", text="oi"))

    process_directory(tmp_path, db_path)

    manager = SWAILiteManager(str(db_path))
    stored = manager.get_message_by_id("abc123")
    manager.close()

    assert stored is not None
    assert stored["content"] == "oi"


def test_process_json_without_data_logs_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db_path = tmp_path / "db.sqlite"
    _write_json(tmp_path, "invalid.json", {"foo": "bar"})

    process_directory(tmp_path, db_path)
    captured = capsys.readouterr()

    assert "campo 'data' ausente" in captured.out
    assert _db_rows(db_path) == 0


def test_process_malformed_json_logs_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db_path = tmp_path / "db.sqlite"
    (tmp_path / "bad.json").write_text("{invalid json")

    process_directory(tmp_path, db_path)
    captured = capsys.readouterr()

    assert "erro ao processar" in captured.out
    assert _db_rows(db_path) == 0


def test_duplicate_messages_not_reprocessed(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db_path = tmp_path / "db.sqlite"
    payload = _payload("dup1")
    _write_json(tmp_path, "msg1.json", payload)
    _write_json(tmp_path, "msg2.json", payload)

    process_directory(tmp_path, db_path)
    captured = capsys.readouterr()

    assert "⚠️ já existente: msg2.json" in captured.out
    assert _db_rows(db_path) == 1


def test_process_multiple_files_with_structure_variations(tmp_path: Path) -> None:
    db_path = tmp_path / "db.sqlite"
    _write_json(tmp_path, "msg1.json", _payload("a1", text="t1"))
    # Body provided directly
    _write_json(tmp_path, "msg2.json", {"data": {"id": "a2", "timestamp": 2, "from": "333", "to": "444", "body": "t2"}})
    # Content key
    _write_json(tmp_path, "msg3.json", {"data": {"id": "a3", "timestamp": 3, "from": "555", "to": "666", "content": "t3"}})

    process_directory(tmp_path, db_path)

    manager = SWAILiteManager(str(db_path))
    assert manager.get_message_by_id("a1")["content"] == "t1"
    assert manager.get_message_by_id("a2")["content"] == "t2"
    assert manager.get_message_by_id("a3")["content"] == "t3"
    manager.close()


@pytest.mark.slow
def test_bulk_processing_performance(tmp_path: Path) -> None:
    db_path = tmp_path / "db.sqlite"
    for i in range(120):
        _write_json(tmp_path, f"msg{i}.json", _payload(f"id{i}", timestamp=100 + i))

    process_directory(tmp_path, db_path)

    assert _db_rows(db_path) == 120

