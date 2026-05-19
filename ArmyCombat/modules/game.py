"""Main game controller for Army Combat."""

from __future__ import annotations

import copy
import os
import random
from typing import Callable

from .combat import Combat
from .data_loader import (
    load_rooms,
    load_items,
    load_events,
    load_enemies,
    load_difficulties,
    save_game_data,
    load_game_data,
)
from .models import Enemy, Item, Player, Room


class Game:
    """Controls game setup, commands, movement, events, saving, and loading."""

    STARTING_ROOM = "Landing Zone"
    FINAL_ROOM = "Outlaw Camp"

    def __init__(self, get_input: Callable = input):
        self.get_input = get_input
        self.rooms = load_rooms()
        self.base_items = load_items()
        self.events = load_events()
        self.enemy_data = load_enemies()
        self.difficulties = load_difficulties()
        self.difficulty_name = "normal"
        self.difficulty = self.difficulties[self.difficulty_name]
        self.player = Player()
        self.current_room_name = self.STARTING_ROOM
        self.game_over = False

    def clear_screen(self) -> None:
        """Clear the terminal screen when a terminal supports it."""
        if os.name == "nt":
            os.system("cls")
        elif os.environ.get("TERM"):
            os.system("clear")

    def show_title(self) -> None:
        """Show the title and basic instructions."""
        print(r"""
   __    ____  __  __  _  _     ___  _____  __  __  ____    __   ____
  /__\  (  _ \(  \/  )( \/ )   / __)(  _  )(  \/  )(  _ \  /__\ (_  _)
 /(__)\  )   / )    (  \  /   ( (__  )(_)(  )    (  ) _ < /(__)\  )(
(__)(__)(_)\_)(_/\/\_) (__)    \___)(_____)(_/\/\_)(____/(__)(__)(__)
        """)
        print("You have parachuted into a Landing Zone, your equipment is scattered across the map.")
        print("Your objective: collect your gear, survive the map, and defeat the Outlaws.")
        print("Type 'help' at any time to see all commands.")
        print("-" * 50)

    def choose_difficulty(self) -> None:
        """Ask the player to choose a difficulty level."""
        print("Choose difficulty: Easy, Normal, or Hard")
        while True:
            choice = self.get_input("Difficulty: ").strip().lower()
            if choice in self.difficulties:
                self.difficulty_name = choice
                self.difficulty = self.difficulties[choice]
                return
            print("Invalid difficulty. Choose Easy, Normal, or Hard.")

    def new_game(self) -> None:
        """Start a new game."""
        self.rooms = load_rooms()
        self.current_room_name = self.STARTING_ROOM
        self.game_over = False
        self.player.reset(starting_health=self.difficulty["player_health"])
        self.place_random_items()

    def place_random_items(self) -> None:
        """Randomly place available items into rooms."""
        item_pool = [copy.deepcopy(item) for item in self.base_items]
        random.shuffle(item_pool)

        valid_rooms = [
            room for room in self.rooms.values()
            if room.name not in [self.STARTING_ROOM, self.FINAL_ROOM]
        ]
        random.shuffle(valid_rooms)

        for room in valid_rooms:
            room.item = None

        for room, item in zip(valid_rooms, item_pool):
            room.item = item

    def current_room(self) -> Room:
        """Return the current Room object."""
        return self.rooms[self.current_room_name]

    def show_room(self) -> None:
        """Show the player's current location."""
        room = self.current_room()
        print("\n" + "=" * 50)
        print(f"Location: {room.name}")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Attack: {self.player.attack}")
        print(f"Defense: {self.player.defense}")
        print(f"Score: {self.player.score}")
        print("-" * 50)
        print(room.description)

        if room.item:
            print(f"\nYou see a {room.item.name} here. Type 'take' to pick it up.")

        exits = ", ".join(direction.title() for direction in room.available_exits())
        print(f"\nExits: {exits}")
        self.show_command_hint()
        print("=" * 50)

    def show_command_hint(self) -> None:
        """Show a short list of useful commands for the current situation."""
        room = self.current_room()
        movement_commands = room.available_exits()
        action_commands = ["look", "inventory", "stats", "save", "load", "help", "quit"]

        if room.item:
            action_commands.insert(0, "take")

        if self.player.get_healing_items():
            action_commands.insert(1, "use <item name>")

        print("\nCommands you can use:")
        if movement_commands:
            print("  Move: " + ", ".join(movement_commands))
        print("  Other: " + ", ".join(action_commands))

    def show_help(self) -> None:
        """Show available commands."""
        print("\nCommands:")
        print("  move north/east/south/west  - Move in a direction")
        print("  north/east/south/west       - Shortcut for movement")
        print("  n/s/e/w                     - Short movement commands")
        print("  look                        - Show the current room again")
        print("  take                        - Pick up the item in the room")
        print("  inventory or i              - Show inventory")
        print("  stats                       - Show player stats")
        print("  use <item name>             - Use a healing item outside combat")
        print("  save                        - Save the game")
        print("  load                        - Load the saved game")
        print("  help, h, or ?               - Show this command list")
        print("  quit, q, or exit            - Quit the game")
        self.show_command_hint()

    def show_stats(self) -> None:
        """Show player stats."""
        print("\nPlayer Stats")
        print("-" * 50)
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Attack: {self.player.attack}")
        print(f"Defense: {self.player.defense}")
        print(f"Score: {self.player.score}")
        print(f"Difficulty: {self.difficulty_name.title()}")
        print("-" * 50)

    def show_inventory(self) -> None:
        """Show inventory."""
        print("\nInventory")
        print("-" * 50)
        print(self.player.inventory_text())
        print("-" * 50)

    def take_item(self) -> None:
        """Pick up the item in the current room."""
        room = self.current_room()
        if room.item is None:
            print("There is nothing here to take.")
            self.show_command_hint()
            return

        item = room.item
        self.player.add_item(item)
        room.item = None
        print(f"You picked up the {item.name}.")
        if item.attack:
            print(f"Attack increased by {item.attack}.")
        if item.defense:
            print(f"Defense increased by {item.defense}.")
        if item.heal:
            print(f"{item.name} can heal {item.heal} HP and has {item.uses_left} use(s).")
        print("Score +10")
        self.show_command_hint()

    def move_player(self, direction: str) -> None:
        """Move the player in the requested direction."""
        direction = direction.strip().lower()
        room = self.current_room()

        if direction not in room.exits:
            print(f"You cannot move {direction} from here.")
            self.show_command_hint()
            return

        self.current_room_name = room.exits[direction]
        self.clear_screen()
        self.show_room()

        if self.current_room_name == self.FINAL_ROOM:
            self.final_battle()
            return

        self.maybe_trigger_random_event()

    def maybe_trigger_random_event(self) -> None:
        """Roll for a random event after movement."""
        if random.random() > self.difficulty["event_chance"]:
            return

        combat_events = [event for event in self.events if event.get("event_type") == "combat"]
        flavor_events = [event for event in self.events if event.get("event_type") == "flavor"]

        if random.random() < self.difficulty["combat_chance"] and combat_events:
            event = random.choice(combat_events)
        else:
            event = random.choice(flavor_events)

        self.handle_event(event)

    def handle_event(self, event: dict) -> None:
        """Handle one random event."""
        print("\n" + "*" * 50)
        print(event["description"])

        if event.get("event_type") == "combat":
            enemy_name = event.get("enemy", "Enemy")
            result = self.start_combat(enemy_name)
            if result == "lose":
                self.end_game(victory=False)
            elif result == "run":
                print(f"You escaped from the {enemy_name}, but lost 10 score.")

        print("*" * 50)
        if not self.game_over:
            self.show_command_hint()

    def make_enemy(self, enemy_name: str) -> Enemy:
        """Create a new Enemy object by name."""
        data = self.enemy_data.get(enemy_name)
        if data is None:
            return Enemy(name=enemy_name)
        return Enemy.from_dict(
            enemy_name,
            data,
            health_multiplier=self.difficulty["enemy_health_multiplier"],
        )

    def start_combat(self, enemy_name: str) -> str:
        """Start combat against a named enemy."""
        enemy = self.make_enemy(enemy_name)
        combat = Combat(self.player, enemy, get_input=self.get_input)
        return combat.run()

    def final_battle(self) -> None:
        """Run the final battle against the Outlaws."""
        print("\nYou have reached the Outlaw Camp. Prepare for the final battle!")
        result = self.start_combat("Outlaws")
        if result == "win":
            self.end_game(victory=True)
        elif result == "lose":
            self.end_game(victory=False)
        elif result == "run":
            print("You ran away from the Outlaws. The mission failed.")
            self.end_game(victory=False)

    def use_item_command(self, item_name: str) -> None:
        """Use a healing item outside combat."""
        if not item_name:
            print("Use what? Example: use medpac")
            self.show_command_hint()
            return

        matched_name = None
        for inventory_name in self.player.inventory:
            if inventory_name.lower() == item_name.lower():
                matched_name = inventory_name
                break

        if matched_name is None:
            print("You do not have that item.")
            self.show_command_hint()
            return

        success, message = self.player.use_healing_item(matched_name)
        print(message)
        if not success:
            self.show_command_hint()

    def save(self) -> None:
        """Save the current game."""
        room_items = {}
        for room_name, room in self.rooms.items():
            room_items[room_name] = room.item.to_dict() if room.item else None

        data = {
            "difficulty_name": self.difficulty_name,
            "current_room_name": self.current_room_name,
            "player": self.player.to_dict(),
            "room_items": room_items,
        }
        save_game_data(data)
        print("Game saved.")

    def load(self) -> None:
        """Load a saved game."""
        data = load_game_data()
        if data is None:
            print("No saved game was found.")
            self.show_command_hint()
            return

        self.rooms = load_rooms()
        self.difficulty_name = data.get("difficulty_name", "normal")
        self.difficulty = self.difficulties.get(self.difficulty_name, self.difficulties["normal"])
        self.current_room_name = data.get("current_room_name", self.STARTING_ROOM)
        self.player = Player.from_dict(data.get("player", {}))

        for room_name, item_data in data.get("room_items", {}).items():
            if room_name in self.rooms and item_data:
                self.rooms[room_name].item = Item.from_dict(item_data)

        self.game_over = False
        print("Game loaded.")
        self.show_room()

    def process_command(self, command: str) -> None:
        """Read and run one player command."""
        command = command.strip()
        if not command:
            print("Type a command, or type 'help' to see all commands.")
            self.show_command_hint()
            return

        command_lower = command.lower()

        if command_lower in ["help", "h", "?"]:
            self.show_help()
        elif command_lower in ["look", "l"]:
            self.show_room()
        elif command_lower in ["inventory", "i"]:
            self.show_inventory()
        elif command_lower == "stats":
            self.show_stats()
        elif command_lower in ["take", "get", "pick up"]:
            self.take_item()
        elif command_lower == "save":
            self.save()
        elif command_lower == "load":
            self.load()
        elif command_lower in ["quit", "q", "exit"]:
            print("Thanks for playing!")
            self.game_over = True
        elif command_lower.startswith("move "):
            direction = command_lower.replace("move ", "", 1).strip()
            self.move_player(direction)
        elif command_lower in ["north", "south", "east", "west", "n", "s", "e", "w"]:
            shortcuts = {"n": "north", "s": "south", "e": "east", "w": "west"}
            self.move_player(shortcuts.get(command_lower, command_lower))
        elif command_lower.startswith("use "):
            item_name = command[4:].strip()
            self.use_item_command(item_name)
        else:
            print("Unknown command.")
            self.show_command_hint()

    def end_game(self, victory: bool) -> None:
        """End the game and show final score."""
        print("\n" + "=" * 50)
        if victory:
            print("Mission Complete! You defeated the Outlaws and won the game!")
        else:
            print("Mission Failed. Game over.")
        print(f"Final Score: {self.player.score}")
        print(f"Rank: {self.player.rank()}")
        print("=" * 50)
        self.game_over = True

    def run(self) -> None:
        """Main game loop."""
        self.clear_screen()
        self.show_title()
        self.choose_difficulty()
        self.new_game()
        self.show_room()

        while not self.game_over:
            command = self.get_input("\nCommand: ").strip()
            self.process_command(command)


def main() -> None:
    """Program entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
