"""Process N8N exported JSON files applying Layer 1 formatting.

This script iterates over a directory containing JSON payloads captured
by the N8N webhook.  Each payload is expected to have the same
structure used by the production webhook where the message data resides
under the ``data`` key.  The formatted messages are stored in a SQLite
database using :class:`SWAILiteManager`.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict

from integrations.database.sqlite_manager import SWAILiteManager
from pipeline.layer1_formatter import Layer1FormatError, format_message


logger = logging.getLogger(__name__)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def process_directory(directory: Path, db_path: Path, force: bool = False) -> None:
    manager = SWAILiteManager(str(db_path))
    for file_path in sorted(directory.glob("*.json")):
        try:
            payload = _load_json(file_path)
            if "data" not in payload:
                raise Layer1FormatError("campo 'data' ausente")
            formatted = format_message(payload["data"])
            row_id = manager.store_message(formatted, overwrite=force)
            if row_id:
                msg = f"✅ processado: {file_path.name} → ID: {row_id}"
            else:
                msg = f"⚠️ já existente: {file_path.name}"
            logger.info(msg)
            print(msg)
        except Exception as exc:  # pragma: no cover - log path
            err = f"❌ erro ao processar {file_path.name}: {exc}"
            logger.error(err)
            print(err)
    manager.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        default="data/n8n_exports",
        help="Diretório com os arquivos JSON exportados pelo N8N",
    )
    parser.add_argument(
        "--db",
        default="data/databases/messages.db",
        help="Caminho do arquivo SQLite que receberá os dados",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocessa mensagens já inseridas",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    process_directory(Path(args.directory), Path(args.db), force=args.force)


if __name__ == "__main__":
    main()
