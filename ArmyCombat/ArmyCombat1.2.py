"""
ArmyCombat1_2

Description:
"""

import copy
import os
import random


ROOMS = {'Creek Bank': {'East': 'Forest',
                'South': 'Winding Brook',
                'West': 'Deep Forest',
                'description': "At the creek's edge, crystal-clear water flows gently over smooth "
                               'pebbles. The serene gurgling of the creek blends harmoniously with '
                               'the rustling leaves.'},
 'Deep Forest': {'East': 'Creek Bank',
                 'West': 'Forest Glade',
                 'description': 'Venturing further into the heart of the forest, you become '
                                'enveloped in an enigmatic realm. Ancient trees form an intricate '
                                'maze, and dappled sunlight creates mesmerizing patterns.'},
 'Desert': {'East': 'Oasis',
            'North': 'Meadow',
            'South': 'Flats',
            'West': 'Dried Riverbed',
            'description': "The desert's embrace is both harsh and awe-inspiring. Waves of heat "
                           'rise from the sun-scorched sand, and the distant horizon shimmers with '
                           'mirages.'},
 'Desolate Expanse': {'East': 'Lonely Steppe',
                      'West': 'Solemn Savannah',
                      'description': "The land before you is desolate and expansive. It's a place "
                                     'of emptiness and solitude, where the horizon seems distant '
                                     'and unreachable.'},
 'Dried Riverbed': {'East': 'Desert',
                    'North': 'Winding Brook',
                    'West': 'Scorched Wasteland',
                    'description': 'At the dried riverbed, fractured earth whispers stories of '
                                   "ancient waters. It's a landscape of contrasts, where the "
                                   'memory of flowing rivers meets the arid present.'},
 'Flats': {'East': 'Solemn Savannah',
           'North': 'Desert',
           'South': 'Outlaw Camp',
           'West': 'Lonely Steppe',
           'description': 'You step onto the flats, an open and barren expanse that stretches as '
                          'far as the eye can see. The land is still, a canvas awaiting the story '
                          'of your journey.'},
 'Forest': {'East': 'Forest Glade',
            'North': 'Landing Zone',
            'South': 'Meadow',
            'West': 'Creek Bank',
            'description': 'You stand in a realm of shadows and whispers. Towering trees with '
                           'gnarled branches encircle you, creating an otherworldly ambience.'},
 'Forest Glade': {'East': 'Deep Forest',
                  'West': 'Forest',
                  'description': 'Stepping into this secluded glade is like entering a secret '
                                 'haven of tranquility. Sunbeams dance through the emerald '
                                 'foliage, painting patterns of light on the forest floor.'},
 'Grazing Pasture': {'East': 'Verdant Expanse',
                     'West': 'Meadow',
                     'description': 'A serene pasture greets you, where contented animals graze '
                                    'peacefully. The distant lowing of cattle and the soft swaying '
                                    'of grass create a serene pastoral symphony.'},
 'Landing Zone': {'South': 'Forest',
                  'description': 'You find yourself amidst a dense and ancient forest. The air is '
                                 'rich with the scent of pine, and beams of sunlight pierce '
                                 'through the thick canopy.'},
 'Lonely Steppe': {'East': 'Flats',
                   'West': 'Desolate Expanse',
                   'description': 'You find yourself on a lonely steppe, the vast open landscape '
                                  'stretching far and wide. The wind carries the scent of earth '
                                  'and grass.'},
 'Meadow': {'East': 'Grazing Pasture',
            'North': 'Forest',
            'South': 'Desert',
            'West': 'Winding Brook',
            'description': "The meadow stretches out like an artist's canvas. Wildflowers of every "
                           'hue sway in unison, their delicate fragrances carried by the breeze.'},
 'Oasis': {'East': 'Scorched Wasteland',
           'West': 'Desert',
           'description': "An oasis of life amidst the desert's desolation. Palm trees sway in the "
                          'breeze, and the clear pool reflects the vibrant blue sky like a '
                          'precious gem.'},
 'Outlaw Camp': {'North': 'Flats',
                 'description': "You've reached the outlaw camp, a makeshift settlement in the "
                                'flats. Tents and fires tell tales of lawlessness and danger. Keep '
                                'your guard up.'},
 'Scorched Wasteland': {'East': 'Dried Riverbed',
                        'West': 'Oasis',
                        'description': 'The wasteland stretches endlessly, a harsh testament to '
                                       "nature's unforgiving side. Heatwaves distort the air, and "
                                       'the silence is broken only by the distant call of a desert '
                                       'creature.'},
 'Solemn Savannah': {'East': 'Desolate Expanse',
                     'West': 'Flats',
                     'description': 'You enter a solemn savannah, the ground rolling gently under '
                                    'your feet. The stillness of the landscape fills you with a '
                                    'sense of reverence.'},
 'Verdant Expanse': {'East': 'Winding Brook',
                     'West': 'Grazing Pasture',
                     'description': 'You find yourself in a breathtaking verdant expanse. The '
                                    'meadow seems to stretch beyond the horizon, a sea of vibrant '
                                    'green that dances in harmony with the wind.'},
 'Winding Brook': {'East': 'Meadow',
                   'North': 'Creek Bank',
                   'South': 'Dried Riverbed',
                   'West': 'Verdant Expanse',
                   'description': 'You follow the path of a meandering brook, its babbling melody '
                                  'a soothing accompaniment to your journey. Ferns and mosses '
                                  'thrive in the damp, fertile soil.'}}

EVENTS = [{'description': '\nYou encounter hostile creatures!',
  'enemy': 'Creatures',
  'event_type': 'combat'},
 {'description': '\nA group of bandits attacks!', 'enemy': 'Bandits', 'event_type': 'combat'},
 {'description': '\nYou encounter a hostile group of looters!',
  'enemy': 'Looters',
  'event_type': 'combat'},
 {'description': '\nA rival faction ambushes you!',
  'enemy': 'Rival Faction',
  'event_type': 'combat'},
 {'description': '\nA pack of feral dogs attacks!', 'enemy': 'Feral Dogs', 'event_type': 'combat'},
 {'description': '\nYou hear strange noises in the distance.', 'event_type': 'flavor'},
 {'description': '\nA mysterious mist envelops the area.', 'event_type': 'flavor'},
 {'description': '\nYou stumble upon an old campsite.', 'event_type': 'flavor'},
 {'description': '\nYou find a hidden cache of supplies.', 'event_type': 'flavor'},
 {'description': '\nA sudden rainstorm forces you to take shelter.', 'event_type': 'flavor'},
 {'description': '\nYou come across an abandoned vehicle.', 'event_type': 'flavor'},
 {'description': '\nYou discover a torn map with a mysterious location marked.',
  'event_type': 'flavor'},
 {'description': '\nYou stumble upon a makeshift campfire.', 'event_type': 'flavor'},
 {'description': '\nThe Outlaws have found you!', 'enemy': 'Outlaws', 'event_type': 'combat'}]

POSSIBLE_ITEMS = [{'att': 0, 'def': 10, 'heal': 0, 'name': 'Helmet'},
 {'att': 3, 'def': 0, 'heal': 0, 'name': 'Ammo'},
 {'att': 12, 'def': 0, 'heal': 0, 'name': 'Rifle'},
 {'att': 7, 'def': 0, 'heal': 0, 'max_uses': 2, 'name': 'Grenade'},
 {'att': 0, 'def': 20, 'heal': 0, 'name': 'Flak Vest'},
 {'att': 0, 'def': 0, 'heal': 30, 'max_uses': 1, 'name': 'Medpac'},
 {'att': 4, 'def': 0, 'heal': 0, 'name': 'Knife'},
 {'att': 0, 'def': 0, 'heal': 15, 'max_uses': 2, 'name': 'Energy Drink'},
 {'att': 1, 'def': 5, 'heal': 0, 'name': 'Rucksack'},
 {'att': 2, 'def': 0, 'heal': 0, 'name': 'Shovel'},
 {'att': 0, 'def': 0, 'heal': 5, 'max_uses': 3, 'name': 'Canteen'}]


class Item:
    """Represents one item the player can find or carry."""

    def __init__(self, name, attack=0, defense=0, heal=0, max_uses=0):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.heal = heal
        self.max_uses = max_uses
        self.uses_left = max_uses

    @classmethod
    def from_dictionary(cls, item_data):
        """Creates an Item object from one of the item dictionaries."""
        return cls(
            name=item_data.get("name", "Unknown Item"),
            attack=item_data.get("att", 0),
            defense=item_data.get("def", 0),
            heal=item_data.get("heal", 0),
            max_uses=item_data.get("max_uses", 0)
        )

    def is_healing_item(self):
        return self.heal > 0 and self.max_uses > 0 and self.uses_left > 0

    def use(self):
        """Uses the item once and returns the amount healed."""
        if not self.is_healing_item():
            return 0

        self.uses_left -= 1
        return self.heal


class Player:
    """Stores player stats and inventory."""

    def __init__(self):
        self.health = 100
        self.attack = 10
        self.defense = 0
        self.inventory = {}

    def is_alive(self):
        return self.health > 0

    def add_item(self, item):
        """Adds an item to inventory and applies attack/defense bonuses."""
        self.inventory[item.name] = item

        self.attack += item.attack
        self.defense += item.defense

        print("You picked up the " + item.name + ".")

        if item.attack > 0:
            print("Attack increased by " + str(item.attack))

        if item.defense > 0:
            print("Defense increased by " + str(item.defense))

        if item.heal > 0:
            print("This item can heal you during combat.")

        if item.max_uses > 0:
            print(item.name + " can be used " + str(item.uses_left) + " time(s).")

    def show_inventory(self):
        print(("-" * 19) + " Inventory " + ("-" * 20))

        if not self.inventory:
            print("Your inventory is empty.")
        else:
            for item in self.inventory.values():
                if item.heal > 0:
                    print(
                        item.name
                        + " (Uses: "
                        + str(item.uses_left)
                        + "/"
                        + str(item.max_uses)
                        + ") (Heals: "
                        + str(item.heal)
                        + " HP)"
                    )
                else:
                    print(item.name)

        print("-" * 50)

    def use_medical_item(self, get_input=input):
        healing_items = [
            item for item in self.inventory.values()
            if item.is_healing_item()
        ]

        if not healing_items:
            print("\nYou don't have any healing items to use.")
            return

        print("\nSelect a healing item to use:")
        for index, item in enumerate(healing_items, start=1):
            print(
                str(index)
                + ". "
                + item.name
                + " (Uses: "
                + str(item.uses_left)
                + "/"
                + str(item.max_uses)
                + ") (Heals "
                + str(item.heal)
                + " HP)"
            )

        choice = get_input("Enter the number of the healing item to use: ")

        try:
            choice_index = int(choice) - 1

            if 0 <= choice_index < len(healing_items):
                healing_item = healing_items[choice_index]
                heal_amount = healing_item.use()

                self.health += heal_amount
                self.health = min(self.health, 100)

                print("\nYou used a " + healing_item.name + " and gained " + str(heal_amount) + " health.")
                print("New health: " + str(self.health))

                if healing_item.uses_left == 0:
                    print("You have used up all the allowed uses for this item.")
            else:
                print("Invalid choice.")

        except ValueError:
            print("Invalid input. Please enter a number.")


class Combat:
    """Handles one combat encounter."""

    def __init__(self, player, enemy_name, get_action=input):
        self.player = player
        self.enemy_name = enemy_name
        self.enemy_health = 100
        self.get_action = get_action

    def run(self):
        print("\nA " + self.enemy_name + " is attacking you!")

        while self.player.health > 0 and self.enemy_health > 0:
            print("\nYour health: " + str(self.player.health))
            print(self.enemy_name + "'s health: " + str(self.enemy_health))

            action = self.get_action("\n[F]ight, [R]un, [U]se Healing Item? ").lower()

            if action == "f":
                player_damage = random.randint(self.player.attack // 2, self.player.attack)
                enemy_damage = max(random.randint(5, 15) - self.player.defense, 0)

                self.player.health -= enemy_damage
                self.enemy_health -= player_damage

                print("\nYou dealt " + str(player_damage) + " damage to the " + self.enemy_name + ".")
                print("The " + self.enemy_name + " dealt " + str(enemy_damage) + " damage to you.")

                if self.player.health <= 0:
                    print("\nYou have been defeated.")
                    return "lose"

                if self.enemy_health <= 0:
                    print("\nYou defeated the " + self.enemy_name + "!")
                    return "win"

            elif action == "r":
                print("\nYou choose to run away.")
                return "run"

            elif action == "u":
                self.player.use_medical_item(self.get_action)

            else:
                print("Invalid action. Please enter 'F', 'R', or 'U'.")

        return None


class Game:
    """Controls the full game."""

    def __init__(self):
        self.rooms = ROOMS
        self.events = EVENTS
        self.original_possible_items = POSSIBLE_ITEMS
        self.reset_game()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def reset_game(self):
        self.player = Player()
        self.current_room = "Landing Zone"
        self.possible_items = copy.deepcopy(self.original_possible_items)
        self.items = {room: None for room in self.rooms}
        self.initialize_items()

    def generate_random_item(self):
        if not self.possible_items:
            return None

        chosen_item = random.choice(self.possible_items)
        self.possible_items.remove(chosen_item)
        return Item.from_dictionary(chosen_item)

    def initialize_items(self):
        for room in self.rooms:
            if room not in ["Landing Zone", "Outlaw Camp"]:
                self.items[room] = self.generate_random_item()

    def get_valid_direction(self, possible_directions):
        options = [
            direction for direction in possible_directions
            if direction != "description"
        ]

        while True:
            direction = input("Choose a direction to move (" + ", ".join(options) + "): ").capitalize()

            if direction in possible_directions:
                return direction

            print("Invalid direction. Choose from:", ", ".join(options))

    def show_instructions(self):
        print(r""" 
   __    ____  __  __  _  _     ___  _____  __  __  ____    __   ____ 
  /__\  (  _ \(  \/  )( \/ )   / __)(  _  )(  \/  )(  _ \  /__\ (_  _)
 /(__)\  )   / )    (  \  /   ( (__  )(_)(  )    (  ) _ < /(__)\  )(  
(__)(__)(_)\_)(_/\/\_) (__)    \___)(_____)(_/\/\_)(____/(__)(__)(__)
    """)
        print("You have parachuted into a Landing Zone, your equipment")
        print("scattered across the map.")
        print("Your Objective: Collect your gear to attack the Outlaws")
        print("Move commands: South, North, East, West")
        print("-" * 50)

        input("\nPress Enter to start the game...")

    def show_status(self):
        print("-" * 50)
        print("Health: " + str(self.player.health))
        print("Attack: " + str(self.player.attack))
        print("Defense: " + str(self.player.defense))
        print("-" * 50)
        print("You are now in the " + self.current_room)
        print("Description: " + self.rooms[self.current_room].get("description", "No description available."))

        item = self.items.get(self.current_room)

        if item and item.name not in self.player.inventory:
            print("\nThere is a " + item.name + " in the room.")

            while True:
                choice = input("Would you like to pick up the " + item.name + "? (y/n): ").strip().lower()

                if choice in ["y", "n"]:
                    break

                print("Please enter 'y' or 'n'.")

            if choice == "y":
                self.player.add_item(item)
                self.items[self.current_room] = None

        print("-" * 50)
        self.player.show_inventory()

    def get_event_list_for_room(self):
        if random.random() < 0.75:
            filtered_events = [
                event for event in self.events
                if event["event_type"] == "flavor"
            ]
        else:
            filtered_events = [
                event for event in self.events
                if event["event_type"] == "combat"
            ]

        if self.current_room != "Outlaw Camp":
            filtered_events = [
                event for event in filtered_events
                if not (
                    event.get("enemy") == "Outlaws"
                    and event["event_type"] == "combat"
                )
            ]

        return filtered_events

    def handle_random_event(self, event_list):
        while True:
            event_info = random.choice(event_list)
            event_type = event_info.get("event_type")
            description = event_info.get("description")
            enemy_name = event_info.get("enemy")

            if self.current_room == "Outlaw Camp" and event_type == "combat" and enemy_name != "Outlaws":
                continue

            print("\n" + ("=" * 50))
            print(description)

            if event_type == "combat":
                combat_result = Combat(self.player, enemy_name).run()

                if combat_result == "win":
                    print("\nCongratulations! You defeated the " + enemy_name)
                elif combat_result == "lose":
                    print("\nYou were defeated by the " + enemy_name + ". Game over.")
                    return "defeat"
                elif combat_result == "run":
                    print("\nYou managed to escape from the " + enemy_name)

            print("=" * 50 + "\n")
            return None

    def run(self):
        while True:
            self.reset_game()
            self.clear_screen()
            self.show_instructions()
            self.show_status()

            while self.current_room != "Outlaw Camp" and self.player.is_alive():
                room_data = self.rooms.get(self.current_room, {})
                possible_directions = list(room_data.keys())

                if not possible_directions:
                    print("You are trapped! No available moves.")
                    break

                print(
                    "You are in "
                    + self.current_room
                    + ", your possible moves are: "
                    + ", ".join([move for move in possible_directions if move != "description"])
                )

                direction = self.get_valid_direction(possible_directions)
                self.current_room = self.rooms[self.current_room][direction]

                self.clear_screen()
                self.show_status()

                event_list = self.get_event_list_for_room()

                if event_list:
                    event_result = self.handle_random_event(event_list)

                    if event_result == "defeat":
                        break

            if self.current_room == "Outlaw Camp" and self.player.is_alive():
                self.clear_screen()
                print("You have reached the Outlaw Camp. Prepare for the final battle!")
                self.show_status()

                combat_result = Combat(self.player, "Outlaws").run()

                if combat_result == "win":
                    print("Congratulations! You defeated the Outlaws and won the game!")
                elif combat_result == "lose":
                    print("You were defeated by the Outlaws. Game Over.")
                elif combat_result == "run":
                    print("You ran away from the Outlaws... but the game is over now.")

            play_again = input("\nDo you want to play again? (y/n): ").lower()

            if play_again != "y":
                print("Thanks for playing!")
                break


if __name__ == "__main__":
    game = Game()
    game.run()
