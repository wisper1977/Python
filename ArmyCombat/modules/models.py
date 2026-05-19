"""Core data classes for Army Combat.

This file keeps the game's main objects together:
- Item
- Room
- Enemy
- Player
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
import random


@dataclass
class Item:
    """An item the player can find, equip, or use."""

    name: str
    attack: int = 0
    defense: int = 0
    heal: int = 0
    max_uses: int = 0
    uses_left: int = 0
    count: int = 1

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """Create an Item from dictionary data."""
        max_uses = data.get("max_uses", 0)
        return cls(
            name=data["name"],
            attack=data.get("attack", data.get("att", 0)),
            defense=data.get("defense", data.get("def", 0)),
            heal=data.get("heal", 0),
            max_uses=max_uses,
            uses_left=data.get("uses_left", max_uses),
            count=data.get("count", 1),
        )

    def to_dict(self) -> dict:
        """Convert an Item back into dictionary data for saving."""
        return {
            "name": self.name,
            "attack": self.attack,
            "defense": self.defense,
            "heal": self.heal,
            "max_uses": self.max_uses,
            "uses_left": self.uses_left,
            "count": self.count,
        }

    def is_healing_item(self) -> bool:
        """Return True if this item can heal the player."""
        return self.heal > 0 and self.max_uses > 0

    def can_be_used(self) -> bool:
        """Return True if this item still has uses left."""
        return self.is_healing_item() and self.uses_left > 0

    def use(self) -> int:
        """Use a healing item and return the amount healed."""
        if not self.can_be_used():
            return 0
        self.uses_left -= 1
        return self.heal


@dataclass
class Room:
    """A place on the game map."""

    name: str
    description: str
    exits: Dict[str, str]
    item: Optional[Item] = None

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "Room":
        """Create a Room from dictionary data."""
        exits = {direction.lower(): destination for direction, destination in data.get("exits", {}).items()}
        return cls(name=name, description=data.get("description", ""), exits=exits)

    def available_exits(self) -> list[str]:
        """Return a list of available direction names."""
        return list(self.exits.keys())


@dataclass
class Enemy:
    """An enemy the player can fight."""

    name: str
    health: int = 100
    min_damage: int = 5
    max_damage: int = 15
    score_value: int = 25

    @classmethod
    def from_dict(cls, name: str, data: dict, health_multiplier: float = 1.0) -> "Enemy":
        """Create an Enemy from dictionary data and apply difficulty scaling."""
        scaled_health = int(data.get("health", 100) * health_multiplier)
        return cls(
            name=name,
            health=scaled_health,
            min_damage=data.get("min_damage", 5),
            max_damage=data.get("max_damage", 15),
            score_value=data.get("score_value", 25),
        )

    def is_alive(self) -> bool:
        """Return True if this enemy still has health."""
        return self.health > 0

    def attack_player(self, player: "Player", damage_reduction: float = 1.0) -> int:
        """Attack the player and return the damage dealt."""
        raw_damage = random.randint(self.min_damage, self.max_damage)
        reduced_damage = int(raw_damage * damage_reduction)
        final_damage = max(reduced_damage - player.defense, 0)
        player.take_damage(final_damage)
        return final_damage


@dataclass
class Player:
    """The player character and all stats/inventory."""

    max_health: int = 100
    health: int = 100
    attack: int = 10
    defense: int = 0
    inventory: Dict[str, Item] = field(default_factory=dict)
    score: int = 0

    def reset(self, starting_health: int = 100) -> None:
        """Reset the player for a new game."""
        self.max_health = starting_health
        self.health = starting_health
        self.attack = 10
        self.defense = 0
        self.inventory = {}
        self.score = 0

    def is_alive(self) -> bool:
        """Return True if the player still has health."""
        return self.health > 0

    def take_damage(self, amount: int) -> None:
        """Lower health by damage amount."""
        self.health = max(self.health - amount, 0)

    def heal_player(self, amount: int) -> int:
        """Heal the player and return the actual amount restored."""
        before = self.health
        self.health = min(self.health + amount, self.max_health)
        return self.health - before

    def add_item(self, item: Item) -> None:
        """Add an item to inventory and apply stat bonuses."""
        if item.name in self.inventory:
            existing = self.inventory[item.name]
            existing.count += 1
            existing.uses_left += item.uses_left
        else:
            self.inventory[item.name] = item

        self.attack += item.attack
        self.defense += item.defense
        self.score += 10

    def get_healing_items(self) -> list[Item]:
        """Return healing items that still have uses left."""
        return [item for item in self.inventory.values() if item.can_be_used()]

    def use_healing_item(self, item_name: str) -> tuple[bool, str]:
        """Use a healing item by name."""
        item = self.inventory.get(item_name)
        if item is None:
            return False, "You do not have that item."
        if not item.can_be_used():
            return False, "That item cannot be used or has no uses left."

        heal_amount = item.use()
        actual_heal = self.heal_player(heal_amount)
        return True, f"You used {item.name} and restored {actual_heal} health."

    def inventory_text(self) -> str:
        """Return a formatted inventory string."""
        if not self.inventory:
            return "Your inventory is empty."

        lines = []
        for item in self.inventory.values():
            count_text = f" x{item.count}" if item.count > 1 else ""
            stat_parts = []
            if item.attack:
                stat_parts.append(f"Attack +{item.attack}")
            if item.defense:
                stat_parts.append(f"Defense +{item.defense}")
            if item.heal:
                stat_parts.append(f"Heals {item.heal} HP")
            if item.max_uses:
                stat_parts.append(f"Uses {item.uses_left}/{item.max_uses}")

            details = f" ({', '.join(stat_parts)})" if stat_parts else ""
            lines.append(f"- {item.name}{count_text}{details}")
        return "\n".join(lines)

    def rank(self) -> str:
        """Return a final rank based on score."""
        if self.score >= 300:
            return "Legend"
        if self.score >= 200:
            return "Veteran"
        if self.score >= 100:
            return "Survivor"
        return "Recruit"

    def to_dict(self) -> dict:
        """Convert the player to save-file data."""
        return {
            "max_health": self.max_health,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense,
            "score": self.score,
            "inventory": {name: item.to_dict() for name, item in self.inventory.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a player from save-file data."""
        player = cls(
            max_health=data.get("max_health", 100),
            health=data.get("health", 100),
            attack=data.get("attack", 10),
            defense=data.get("defense", 0),
            score=data.get("score", 0),
        )
        player.inventory = {
            name: Item.from_dict(item_data)
            for name, item_data in data.get("inventory", {}).items()
        }
        return player
