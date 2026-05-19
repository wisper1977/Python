"""Data loading and save-file helpers for Army Combat."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Item, Room


MODULE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODULE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
SAVE_DIR = PROJECT_ROOT / "saves"
SAVE_FILE = SAVE_DIR / "savegame.json"


def load_json(filename: str) -> Any:
    """Load a JSON file from the project's data folder."""
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {filename}. Expected it here: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_rooms() -> dict[str, Room]:
    """Load room data and convert it into Room objects."""
    room_data = load_json("rooms.json")
    return {name: Room.from_dict(name, data) for name, data in room_data.items()}


def load_items() -> list[Item]:
    """Load item data and convert it into Item objects."""
    return [Item.from_dict(item_data) for item_data in load_json("items.json")]


def load_events() -> list[dict]:
    """Load random event data."""
    return load_json("events.json")


def load_enemies() -> dict:
    """Load enemy data."""
    return load_json("enemies.json")


def load_difficulties() -> dict:
    """Load difficulty settings."""
    return load_json("difficulties.json")


def save_game_data(data: dict) -> None:
    """Save the current game state to disk."""
    SAVE_DIR.mkdir(exist_ok=True)
    with SAVE_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_game_data() -> dict | None:
    """Load saved game data if it exists."""
    if not SAVE_FILE.exists():
        return None
    with SAVE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)
