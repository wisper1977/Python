
"""Combat system for Army Combat."""

from __future__ import annotations

import random
from typing import Callable

from .models import Player, Enemy


class Combat:
    """Handles one fight between the player and an enemy."""

    def __init__(self, player: Player, enemy: Enemy, get_input: Callable = input):
        self.player = player
        self.enemy = enemy
        self.get_input = get_input

    def run(self) -> str:
        """Run combat and return 'win', 'lose', or 'run'."""
        print(f"\nA {self.enemy.name} is attacking you!")

        while self.player.is_alive() and self.enemy.is_alive():
            self.show_combat_status()
            action = self.get_input("\n[F]ight, [H]eavy attack, [D]efend, [R]un, [U]se item? ").strip().lower()

            if action in ["f", "fight"]:
                self.player_attack(heavy=False)
                if not self.enemy.is_alive():
                    return self.win()
                self.enemy_turn()

            elif action in ["h", "heavy", "heavy attack"]:
                self.player_attack(heavy=True)
                if not self.enemy.is_alive():
                    return self.win()
                self.enemy_turn()

            elif action in ["d", "defend"]:
                print("\nYou take cover and brace for the attack.")
                self.enemy_turn(damage_reduction=0.5)

            elif action in ["r", "run"]:
                self.player.score = max(self.player.score - 10, 0)
                print("\nYou choose to run away.")
                return "run"

            elif action in ["u", "use", "use item"]:
                self.use_healing_item_menu()
                if self.enemy.is_alive():
                    self.enemy_turn()

            else:
                print("Invalid action. Please enter F, H, D, R, or U.")

            if not self.player.is_alive():
                return self.lose()

        return "lose" if not self.player.is_alive() else self.win()

    def show_combat_status(self) -> None:
        """Display current combat stats."""
        print("\n" + "-" * 50)
        print(f"Your health: {self.player.health}/{self.player.max_health}")
        print(f"{self.enemy.name}'s health: {self.enemy.health}")
        print("-" * 50)

    def player_attack(self, heavy: bool = False) -> None:
        """Resolve the player's attack."""
        if heavy:
            if random.random() < 0.35:
                print("\nYour heavy attack missed!")
                return
            damage = random.randint(self.player.attack, max(self.player.attack * 2, self.player.attack))
            self.enemy.health -= damage
            print(f"\nYou hit the {self.enemy.name} with a heavy attack for {damage} damage.")
        else:
            low_damage = max(self.player.attack // 2, 1)
            damage = random.randint(low_damage, self.player.attack)
            self.enemy.health -= damage
            print(f"\nYou dealt {damage} damage to the {self.enemy.name}.")

    def enemy_turn(self, damage_reduction: float = 1.0) -> None:
        """Resolve the enemy's attack."""
        damage = self.enemy.attack_player(self.player, damage_reduction=damage_reduction)
        print(f"The {self.enemy.name} dealt {damage} damage to you.")

    def use_healing_item_menu(self) -> None:
        """Let the player choose a healing item during combat."""
        healing_items = self.player.get_healing_items()
        if not healing_items:
            print("\nYou don't have any healing items to use.")
            return

        print("\nSelect a healing item to use:")
        for index, item in enumerate(healing_items, start=1):
            print(f"{index}. {item.name} - Uses {item.uses_left}/{item.max_uses}, Heals {item.heal} HP")

        choice = self.get_input("Enter item number or name: ").strip()
        selected_item = None

        if choice.isdigit():
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(healing_items):
                selected_item = healing_items[choice_index]
        else:
            for item in healing_items:
                if item.name.lower() == choice.lower():
                    selected_item = item
                    break

        if selected_item is None:
            print("Invalid healing item choice.")
            return

        success, message = self.player.use_healing_item(selected_item.name)
        print("\n" + message)

    def win(self) -> str:
        """Handle combat victory."""
        self.player.score += self.enemy.score_value
        print(f"\nYou defeated the {self.enemy.name}!")
        print(f"Score +{self.enemy.score_value}")
        return "win"

    def lose(self) -> str:
        """Handle combat defeat."""
        print("\nYou have been defeated.")
        return "lose"
