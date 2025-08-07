"""Tests for Layer 2 message grouping into conversations."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import time

import pytest

from integrations.database.sqlite_manager import SWAILiteManager
from pipeline import layer2_grouper


def _setup_manager(tmp_path):
    db_path = tmp_path / "db.sqlite"
    manager = SWAILiteManager(str(db_path))
    layer2_grouper.configure(manager)
    return manager


def _msg(idx: int, ts: str, sender: str = "lead") -> dict:
    lead = "111"
    secretary = "222"
    return {
        "message_id": f"m{idx}",
        "sender_phone": lead if sender == "lead" else secretary,
        "receiver_phone": secretary if sender == "lead" else lead,
        "sender_type": sender,
        "timestamp": ts,
    }


def test_three_messages_same_day_single_conversation(tmp_path):
    manager = _setup_manager(tmp_path)
    base = datetime(2025, 8, 6, 10, tzinfo=timezone.utc)
    last_res = None
    for i in range(3):
        ts = (base + timedelta(minutes=5 * i)).isoformat()
        last_res = layer2_grouper.process_layer2_grouping(_msg(i, ts, sender="lead" if i % 2 == 0 else "secretary"))

    conv_id = f"111_{base.strftime('%Y%m%d')}"
    convo = manager.get_conversation(conv_id)
    manager.close()

    assert convo is not None
    assert convo["message_count"] == 3
    assert last_res["ready_for_ai"] is True


def test_messages_on_different_days_create_new_conversations(tmp_path):
    manager = _setup_manager(tmp_path)
    ts1 = datetime(2025, 1, 1, tzinfo=timezone.utc).isoformat()
    ts2 = datetime(2025, 1, 2, tzinfo=timezone.utc).isoformat()
    layer2_grouper.process_layer2_grouping(_msg(1, ts1))
    layer2_grouper.process_layer2_grouping(_msg(2, ts2))
    count = manager.conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    manager.close()
    assert count == 2


def test_message_count_increment(tmp_path):
    manager = _setup_manager(tmp_path)
    ts = datetime(2025, 8, 6, 10, tzinfo=timezone.utc).isoformat()
    layer2_grouper.process_layer2_grouping(_msg(1, ts))
    conv_id = f"111_{datetime.fromisoformat(ts).strftime('%Y%m%d')}"
    assert manager.get_conversation(conv_id)["message_count"] == 1
    layer2_grouper.process_layer2_grouping(_msg(2, ts, sender="secretary"))
    assert manager.get_conversation(conv_id)["message_count"] == 2
    manager.close()


def test_malformed_message_logs_error(tmp_path, caplog):
    manager = _setup_manager(tmp_path)
    caplog.set_level("ERROR")
    result = layer2_grouper.process_layer2_grouping({"message_id": "x"})
    manager.close()
    assert result["status"] == "error"
    assert "campos obrigatórios ausentes" in caplog.text


@pytest.mark.slow
def test_grouping_100_messages_performance(tmp_path):
    manager = _setup_manager(tmp_path)
    base = datetime(2025, 7, 1, 10, tzinfo=timezone.utc)
    start = time.perf_counter()
    for i in range(100):
        ts = (base + timedelta(minutes=i)).isoformat()
        layer2_grouper.process_layer2_grouping(_msg(i, ts))
    duration = time.perf_counter() - start
    conv_id = f"111_{base.strftime('%Y%m%d')}"
    count = manager.get_conversation(conv_id)["message_count"]
    manager.close()

    assert count == 100
    assert duration < 5

