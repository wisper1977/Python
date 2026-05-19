"""Basic unit tests for game setup and command hints."""

import unittest
from io import StringIO
from pathlib import Path
import sys
from contextlib import redirect_stdout

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.game import Game
from modules.models import Item


class TestGame(unittest.TestCase):
    def test_game_loads_data(self):
        game = Game(get_input=lambda prompt="": "normal")
        self.assertIn("Landing Zone", game.rooms)
        self.assertIn("normal", game.difficulties)
        self.assertGreater(len(game.base_items), 0)

    def test_command_hint_shows_take_when_item_is_present(self):
        game = Game(get_input=lambda prompt="": "normal")
        room = game.current_room()
        room.item = Item(name="Test Item")

        output = StringIO()
        with redirect_stdout(output):
            game.show_command_hint()

        self.assertIn("take", output.getvalue())
        self.assertIn("help", output.getvalue())


if __name__ == "__main__":
    unittest.main()
