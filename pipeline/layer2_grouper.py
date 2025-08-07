"""Layer 2 grouper for aggregating messages into conversations."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
import logging

from integrations.database.sqlite_manager import SWAILiteManager


logger = logging.getLogger(__name__)

_db_manager: Optional[SWAILiteManager] = None


def configure(manager: SWAILiteManager) -> None:
    """Configure the module with a :class:`SWAILiteManager` instance."""
    global _db_manager
    _db_manager = manager


def _extract_phones(message: Dict[str, Any]) -> tuple[str, str]:
    """Return ``(lead_phone, secretary_phone)`` from a formatted message."""

    sender_type = message.get("sender_type")
    if sender_type == "lead":
        return message.get("sender_phone"), message.get("receiver_phone")
    if sender_type == "secretary":
        return message.get("receiver_phone"), message.get("sender_phone")
    # Default assumption: sender is the lead when type is unknown
    return message.get("sender_phone"), message.get("receiver_phone")


def process_layer2_grouping(formatted_message: Dict[str, Any]) -> Dict[str, Any]:
    """Group messages into conversations based on lead phone and date.

    Parameters
    ----------
    formatted_message:
        Dictionary produced by Layer 1 formatting.

    Returns
    -------
    dict
        Dictionary containing ``status``, ``conversation_id`` and
        ``ready_for_ai`` flag. ``status`` is ``"error"`` when the input is
        malformed.
    """

    if _db_manager is None:
        raise RuntimeError("database manager not configured")

    required = ["message_id", "sender_phone", "receiver_phone", "timestamp"]
    missing = [key for key in required if not formatted_message.get(key)]
    if missing:
        logger.error("campos obrigatórios ausentes: %s", ", ".join(missing))
        return {"status": "error", "conversation_id": None, "ready_for_ai": False}

    lead_phone, secretary_phone = _extract_phones(formatted_message)
    if not lead_phone or not secretary_phone:
        logger.error("números de telefone inválidos")
        return {"status": "error", "conversation_id": None, "ready_for_ai": False}

    timestamp = formatted_message["timestamp"]
    try:
        date_str = datetime.fromisoformat(timestamp).strftime("%Y%m%d")
    except ValueError:
        logger.error("timestamp inválido: %s", timestamp)
        return {"status": "error", "conversation_id": None, "ready_for_ai": False}

    conversation_id = f"{lead_phone}_{date_str}"

    convo = _db_manager.record_conversation_message(
        conversation_id=conversation_id,
        message_id=formatted_message["message_id"],
        lead_phone=lead_phone,
        secretary_phone=secretary_phone,
        timestamp=timestamp,
    )

    return {
        "status": convo["status"],
        "conversation_id": conversation_id,
        "ready_for_ai": convo["message_count"] >= 3,
    }


__all__ = ["configure", "process_layer2_grouping"]

