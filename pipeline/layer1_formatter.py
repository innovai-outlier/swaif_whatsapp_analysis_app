"""Layer 1 formatter for N8N webhook messages.

This module contains helper utilities to translate raw messages
received from the N8N webhook into a normalized structure that can be
stored into the SWAI Lite database.  The formatter is intentionally
minimal and focuses on the most common fields emitted by WhatsApp
through the official Cloud API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


class Layer1FormatError(Exception):
    """Raised when the raw message lacks required information."""


def _extract_content(data: Dict[str, Any]) -> str:
    """Return the textual content from a raw message dictionary.

    The WhatsApp webhook may encode the message body in different
    structures depending on its type.  This helper attempts to read the
    message text in a tolerant manner and falls back to an empty string
    when it cannot be determined.
    """

    if "text" in data and isinstance(data["text"], dict):
        return data["text"].get("body", "")
    if "body" in data:
        return str(data["body"])
    if "content" in data:
        return str(data["content"])
    return ""


def _normalize_timestamp(value: Any) -> str:
    """Normalize raw timestamp values to an ISO formatted string."""

    if value is None:
        raise Layer1FormatError("timestamp ausente")

    # Unix timestamps may come as integers or digit strings
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()

    # Attempt to parse ISO formatted strings; if parsing fails, keep raw
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).isoformat()
        except ValueError:
            return value

    raise Layer1FormatError(f"formato de timestamp inválido: {value!r}")


def format_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dictionary with the canonical SWAI message fields.

    Parameters
    ----------
    data:
        Raw message dictionary produced by the N8N webhook.  The
        dictionary **must** contain at least ``id`` and ``timestamp``
        fields.  ``from`` and ``to`` are used to identify sender and
        receiver phone numbers.
    """

    message_id = data.get("id") or data.get("message_id")
    if not message_id:
        raise Layer1FormatError("message_id ausente")

    timestamp = _normalize_timestamp(data.get("timestamp"))

    formatted = {
        "message_id": message_id,
        "sender_phone": data.get("from"),
        "receiver_phone": data.get("to"),
        "sender_type": data.get("sender_type"),
        "content": _extract_content(data),
        "timestamp": timestamp,
    }

    return formatted

