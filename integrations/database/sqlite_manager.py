"""SQLite manager used for persisting messages in the SWAI Lite database."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, Optional


class SWAILiteManager:
    """Lightweight wrapper around :mod:`sqlite3`.

    The class is purposely small, providing only the required
    functionality for this project: ensuring the database schema exists
    and inserting formatted messages into the ``messages`` table.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_table()

    def _ensure_table(self) -> None:
        """Create the ``messages`` table if it doesn't exist."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    sender_phone TEXT,
                    receiver_phone TEXT,
                    sender_type TEXT,
                    content TEXT,
                    timestamp TEXT
                )
                """
            )

    def store_message(self, message: Dict[str, Any], overwrite: bool = False) -> Optional[int]:
        """Store a formatted message into the database.

        Parameters
        ----------
        message:
            Dictionary containing the canonical message fields.
        overwrite:
            When ``True`` existing records with the same ``message_id``
            are replaced; otherwise they are left untouched.

        Returns
        -------
        Optional[int]
            The row ID of the inserted (or existing) message. ``None`` is
            returned if insertion was ignored.
        """

        columns = (
            "message_id",
            "sender_phone",
            "receiver_phone",
            "sender_type",
            "content",
            "timestamp",
        )
        values = tuple(message.get(col) for col in columns)

        with self.conn:
            if overwrite:
                cursor = self.conn.execute(
                    """
                    INSERT INTO messages (message_id, sender_phone, receiver_phone, sender_type, content, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(message_id) DO UPDATE SET
                        sender_phone=excluded.sender_phone,
                        receiver_phone=excluded.receiver_phone,
                        sender_type=excluded.sender_type,
                        content=excluded.content,
                        timestamp=excluded.timestamp
                    """,
                    values,
                )
                return cursor.lastrowid

            cursor = self.conn.execute(
                """
                INSERT OR IGNORE INTO messages (message_id, sender_phone, receiver_phone, sender_type, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                values,
            )

            if cursor.rowcount == 0:
                # Record already existed; fetch its ID for reference
                existing = self.conn.execute(
                    "SELECT id FROM messages WHERE message_id = ?",
                    (message["message_id"],),
                ).fetchone()
                return existing["id"] if existing else None

            return cursor.lastrowid

    def close(self) -> None:
        self.conn.close()

