"""Basic unit tests for Enemy."""

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.models import Enemy, Player


class TestEnemy(unittest.TestCase):
    def test_enemy_can_be_scaled_by_difficulty(self):
        enemy_data = {"health": 100, "min_damage": 5, "max_damage": 15, "score_value": 25}
        enemy = Enemy.from_dict("Bandits", enemy_data, health_multiplier=1.5)
        self.assertEqual(enemy.health, 150)

    def test_enemy_attack_cannot_heal_player(self):
        player = Player(defense=100)
        enemy = Enemy(name="Weak Enemy", min_damage=1, max_damage=1)
        damage = enemy.attack_player(player)
        self.assertEqual(damage, 0)
        self.assertEqual(player.health, 100)


if __name__ == "__main__":
    unittest.main()
