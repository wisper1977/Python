"""Basic unit tests for the Player and Item classes.

Run from the project folder with:
python -m unittest discover tests
"""

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.models import Item, Player


class TestPlayer(unittest.TestCase):
    def test_player_starts_with_default_stats(self):
        player = Player()
        self.assertEqual(player.health, 100)
        self.assertEqual(player.attack, 10)
        self.assertEqual(player.defense, 0)

    def test_adding_weapon_increases_attack(self):
        player = Player()
        rifle = Item(name="Rifle", attack=12)
        player.add_item(rifle)
        self.assertEqual(player.attack, 22)
        self.assertIn("Rifle", player.inventory)

    def test_adding_armor_increases_defense(self):
        player = Player()
        vest = Item(name="Flak Vest", defense=20)
        player.add_item(vest)
        self.assertEqual(player.defense, 20)

    def test_healing_item_restores_health(self):
        player = Player()
        player.health = 50
        medpac = Item(name="Medpac", heal=30, max_uses=1, uses_left=1)
        player.add_item(medpac)

        success, message = player.use_healing_item("Medpac")

        self.assertTrue(success)
        self.assertEqual(player.health, 80)
        self.assertIn("restored", message)

    def test_healing_does_not_go_over_max_health(self):
        player = Player()
        player.health = 90
        canteen = Item(name="Canteen", heal=30, max_uses=1, uses_left=1)
        player.add_item(canteen)
        player.use_healing_item("Canteen")
        self.assertEqual(player.health, 100)


if __name__ == "__main__":
    unittest.main()
