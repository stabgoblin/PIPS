"""Small JSON helpers and the response envelope used across the API."""

import json
from pathlib import Path
from typing import Any, Optional


def load_json(path) -> Optional[Any]:
    path = Path(path)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def ok(message: str, data: Any = None) -> dict:
    return {"status": "ok", "message": message, "data": data}


def pending(message: str, data: Any = None) -> dict:
    return {"status": "pending", "message": message, "data": data}


def error(message: str, data: Any = None) -> dict:
    return {"status": "error", "message": message, "data": data}
