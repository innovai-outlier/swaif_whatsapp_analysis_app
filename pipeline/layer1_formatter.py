"""Layer 1 formatter for N8N webhook messages.

This module contains helper utilities to translate raw messages
received from the N8N webhook into a normalized structure that can be
stored into the SWAI Lite database.  The formatter is intentionally
minimal and focuses on the most common fields emitted by WhatsApp
through the official Cloud API.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
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


def _sanitize_phone(raw: Any) -> str | None:
    """Return only the numeric portion of a WhatsApp JID."""

    if raw is None:
        return None
    return str(raw).split("@")[0]


def _generate_message_id(data: Dict[str, Any]) -> str:
    """Generate a deterministic identifier when none is provided."""

    base = "-".join(
        str(data.get(key, ""))
        for key in (
            "sender_raw_data",
            "receiver_raw_data",
            "timestamp",
            "sent_message",
        )
    )
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


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
        dictionary may come directly from the Evolution API webhook used
        in N8N.  When ``id`` is missing a deterministic identifier is
        generated from the message contents.  ``sender_raw_data`` and
        ``receiver_raw_data`` are normalised to phone numbers.
    """

    message_id = data.get("id") or data.get("message_id")
    if not message_id:
        message_id = _generate_message_id(data)

    timestamp = _normalize_timestamp(data.get("timestamp"))

    sender_raw = data.get("sender_raw_data") or data.get("from")
    receiver_raw = data.get("receiver_raw_data") or data.get("to")

    formatted = {
        "message_id": message_id,
        "sender_phone": _sanitize_phone(sender_raw),
        "receiver_phone": _sanitize_phone(receiver_raw),
        "sender_type": data.get("sender_type"),
        "content": data.get("sent_message") or _extract_content(data),
        "timestamp": timestamp,
        "message_type": data.get("message_type"),
    }

    return formatted

