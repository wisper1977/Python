"""
Army Combat v1.1
by: Chris Collins
"""
# Import Modules
import random

# Dictionary of rooms and directions
rooms = {
    # Starting Zone
    'Landing Zone': {'South': 'Forest'},
    # Forest Level
    'Forest': {'South': 'Meadow', 'North': 'Landing Zone', 'East': 'Forest Glade', 'West': 'Creek Bank'},
    'Forest Glade': {'East': 'Deep Forest', 'West': 'Forest'},
    'Creek Bank': {'East': "Forest", 'West': 'Deep Forest', 'South': 'Winding Brook'},
    'Deep Forest': {'East': 'Creek Bank', 'West': 'Forest Glade'},
    # Meadow Level
    'Meadow': {'North': 'Forest', 'East': 'Grazing Pasture', 'West': 'Winding Brook', 'South': 'Desert'},
    'Winding Brook':{'East': 'Meadow', 'West': 'Verdant Expanse','North': 'Creek Bank', 'South': 'Dried Riverbed'},
    'Grazing Pasture':{'East': 'Verdant Expanse', 'West': 'Meadow'},
    'Verdant Expanse': {'East': 'Winding Brook', 'West': 'Grazing Pasture'},
    # Desert Level
    'Desert': {'North': 'Meadow', 'East': 'Oasis', 'West': 'Dried Riverbed', 'South': 'Flats'},
    'Dried Riverbed':{'East': 'Desert', 'West': 'Scorched Wasteland','North': 'Winding Brook'},
    'Oasis':{'East': 'Scorched Wasteland', 'West': 'Desert'},
    'Scorched Wasteland': {'East': 'Dried Riverbed', 'West': 'Oasis'},
    # Flats Level
    'Flats': {'East': 'Solemn Savannah', 'West': 'Lonely Steppe', 'North': 'Desert', 'South': 'Outlaw Camp'},
    'Lonely Steppe':{'East': 'Flats', 'West': 'Desolate Expanse'},
    'Solemn Savannah':{'East': 'Desolate Expanse', 'West': 'Flats'},
    'Desolate Expanse': {'East': 'Lonely Steppe', 'West': 'Solemn Savannah'},
    # Boss Level
    'Outlaw Camp': {'North': 'Flats'}    
}

# Dictionary of items in each room
items = {room: None for room in rooms}

# Dictionary of room descriptions
room_descriptions = {
    'Landing Zone': "You find yourself amidst a dense and ancient forest. The air is rich with the scent of pine, and beams of sunlight pierce through the thick canopy.",
    'Forest': "You stand in a realm of shadows and whispers. Towering trees with gnarled branches encircle you, creating an otherworldly ambience.",
    'Forest Glade': "Stepping into this secluded glade is like entering a secret haven of tranquility. Sunbeams dance through the emerald foliage, painting patterns of light on the forest floor.",
    'Creek Bank': "At the creek's edge, crystal-clear water flows gently over smooth pebbles. The serene gurgling of the creek blends harmoniously with the rustling leaves.",
    'Deep Forest': "Venturing further into the heart of the forest, you become enveloped in an enigmatic realm. Ancient trees form an intricate maze, and dappled sunlight creates mesmerizing patterns.",
    'Meadow': "The meadow stretches out like an artist's canvas. Wildflowers of every hue sway in unison, their delicate fragrances carried by the breeze.",
    'Winding Brook': "You follow the path of a meandering brook, its babbling melody a soothing accompaniment to your journey. Ferns and mosses thrive in the damp, fertile soil.",
    'Grazing Pasture': "A serene pasture greets you, where contented animals graze peacefully. The distant lowing of cattle and the soft swaying of grass create a serene pastoral symphony.",
    'Verdant Expanse': "You find yourself in a breathtaking verdant expanse. The meadow seems to stretch beyond the horizon, a sea of vibrant green that dances in harmony with the wind.",
    'Desert': "The desert's embrace is both harsh and awe-inspiring. Waves of heat rise from the sun-scorched sand, and the distant horizon shimmers with mirages.",
    'Dried Riverbed': "At the dried riverbed, fractured earth whispers stories of ancient waters. It's a landscape of contrasts, where the memory of flowing rivers meets the arid present.",
    'Oasis': "An oasis of life amidst the desert's desolation. Palm trees sway in the breeze, and the clear pool reflects the vibrant blue sky like a precious gem.",
    'Scorched Wasteland': "The wasteland stretches endlessly, a harsh testament to nature's unforgiving side. Heatwaves distort the air, and the silence is broken only by the distant call of a desert creature.",
    'Flats': "You step onto the flats, an open and barren expanse that stretches as far as the eye can see. The land is still, a canvas awaiting the story of your journey.",
    'Lonely Steppe': "You find yourself on a lonely steppe, the vast open landscape stretching far and wide. The wind carries the scent of earth and grass.",
    'Solemn Savannah': "You enter a solemn savannah, the ground rolling gently under your feet. The stillness of the landscape fills you with a sense of reverence.",
    'Desolate Expanse': "The land before you is desolate and expansive. It's a place of emptiness and solitude, where the horizon seems distant and unreachable.",
    'Outlaw Camp': "You've reached the outlaw camp, a makeshift settlement in the flats. Tents and fires tell tales of lawlessness and danger. Keep your guard up."
}

# Separate list for combat events
combat_events = [
    {'event_type': 'combat', 'description': "\nYou encounter hostile creatures!", 'enemy': 'Creatures'},
    {'event_type': 'combat', 'description': "\nA group of bandits attacks!", 'enemy': 'Bandits'},
    {'event_type': 'combat', 'description': "\nYou encounter a hostile group of looters!", 'enemy': 'Looters'},
    {'event_type': 'combat', 'description': "\nA rival faction ambushes you!", 'enemy': 'Rival Faction'},
    {'event_type': 'combat', 'description': "\nA pack of feral dogs attacks!", 'enemy': 'Feral Dogs'},
]

# Dictionary of random events with descriptions and outcomes
random_events = [
    {'event_type': 'flavor', 'description': "\nYou hear strange noises in the distance."},
    {'event_type': 'flavor', 'description': "\nA mysterious mist envelops the area."},
    {'event_type': 'flavor', 'description': "\nYou stumble upon an old campsite."},
    {'event_type': 'flavor', 'description': "\nYou find a hidden cache of supplies."},
    {'event_type': 'flavor', 'description': "\nA sudden rainstorm forces you to take shelter."},
    {'event_type': 'flavor', 'description': "\nYou come across an abandoned vehicle."},
    {'event_type': 'flavor', 'description': "\nYou discover a torn map with a mysterious location marked."},
    {'event_type': 'flavor', 'description': "\nYou stumble upon a makeshift campfire."},
    # Add more flavor events here
]

# Dictionary for the Outlaws battle
combat_event_outlaws = [
    {'event_type': 'combat', 'description': "\nThe Outlaws have found you!", 'enemy': 'Outlaws'},
    # Add more outlaw-related combat events here if needed
]

# Dictionary of possible items
possible_items = [
    {'name': 'Helmet', 'def': 10, 'att': 0, 'heal': 0},
    {'name': 'Ammo', 'def': 0, 'att': 5, 'heal': 0},
    {'name': 'Rifle', 'def': 0, 'att': 15, 'heal': 0},
    {'name': 'Grenade', 'def': 0, 'att': 10, 'heal': 0},
    {'name': 'Flak Vest', 'def': 20, 'att': 0, 'heal': 0},
    {'name': 'Medpac', 'def': 0, 'att': 0, 'heal': 30, 'max_uses': 1},
    {'name': 'Knife', 'def': 0, 'att': 5, 'heal': 0},
    {'name': 'Energy Drink', 'def': 0, 'att': 0, 'heal': 15, 'max_uses': 2},
    {'name': 'Rucksack', 'def': 0, 'att': 0, 'heal': 0},
    {'name': 'Shovel', 'def': 0, 'att': 0, 'heal': 0},
    {'name': 'Canteen', 'def': 0, 'att': 0, 'heal': 5, 'max_uses': 3},
    # Add more items here
]

# Set Variables
player_health = 100
player_attack = 10
player_defense = 0
collected_items = {}
current_room = "Landing Zone"

def generate_random_item():
    """
    Randomly selects an item from possible_items list and returns it.
    Removes the chosen item from possible_items.
    """
    if not possible_items:
        return None
    chosen_item = random.choice(possible_items)
    possible_items.remove(chosen_item)
    return chosen_item

def initialize_items():
    """
    Initializes items in each room by generating random items from possible_items.
    """
    global items
    items = {
        room: generate_random_item() if room not in collected_items else collected_items[room]
        for room in rooms if room not in ['Landing Zone', 'Outlaw Camp']
    }
    
# Function to get valid direction input from the user
def get_valid_direction(dir_poss):
    while True:
        direction = input("Type the direction you want to move: ").capitalize()
        if direction in dir_poss:
            return direction
        print("Invalid direction. Choose from:", ", ".join(dir_poss))

# Function to display the game instructions
def show_instructions():
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

# Function to display the player's status
def show_status():
    try:
        global player_health
        print("-" * 50)
        print("Health:", player_health)

        if current_room == "Landing Zone":
            print("\nYou are now in the Landing Zone")
            print("There are no items here.")
        elif current_room == "Outlaw Camp":
            print("\nYou are now entering the Outlaw Camp")
        else:
            print("\nYou are now in the", current_room)
            print("Description:", room_descriptions[current_room])

            if items.get(current_room) and items[current_room]['name'] not in collected_items:
                print("\nThere is a", items[current_room]['name'], "in the room.")
                item_question = input("Would you like to pick up the item (y/n)? ").lower()
                if item_question == "y":
                    collect_item(current_room)

        print("\n" + ("-" * 50))
        show_inventory()  # Display the player's inventory

    except KeyError:
        print("An error occurred while accessing room information.")

# Function to display player's Inventory
def show_inventory():
    global collected_items
    print(("-" * 19) + " Inventory " + ("-" * 20))
    for item_name, item_data in collected_items.items():
        # Check if the item has healing capability
        if item_data.get('heal', 0) > 0:
            # Print the item name and count, if count is greater than 1
            item_count = " x" + str(item_data['count']) if item_data['count'] > 1 else ""
            # Check if the item has been used, and if so, print the number of uses
            print(item_name + item_count + " (Uses: " + str(item_data['uses']) + ")")
        else:
            print(item_name)
            
    print("-" * 50)
        
# Function to use item
def use_item(item_name):
    global collected_items
    item = collected_items.get(item_name)
    
    if item:
        max_uses = next((x['max_uses'] for x in possible_items if x['name'] == item_name), None)
        
        if max_uses:
            # If the item has a usage limit
            current_uses = item.get('uses', 0)
            if current_uses < max_uses:
                # Item can still be used
                item['uses'] = current_uses + 1
                print("You used " + item_name + ". You have " + max_uses - current_uses + " uses left.")
            else:
                print("You have exhausted all uses of " + item_name + ".")
        else:
            # No usage limit, just use the item
            print("You used " + item_name + ".")
    else:
        print("You don't have a " + item_name + " in your inventory.")
    
    print("-" * 50)
    
# Function to collect an item in the current room
def collect_item(room_name):
    global collected_items, player_attack, player_defense
    collected_item = items[room_name]
    
    item_name = collected_item['name']
    if item_name not in collected_items:
        collected_items[item_name] = {
            'count': 1, 
            'uses': collected_item.get('uses', 0),
            'heal': collected_item.get('heal', 0)  # Copy the 'heal' attribute
        }
    else:
        collected_items[item_name]['count'] += 1
        
    print("You picked up a", item_name)
    print("Collected", collected_items[item_name]['count'], item_name + "(s)")
    
    if collected_item['att'] > 0:
        player_attack += collected_item['att']
        print("Attack increased by", collected_item['att'])
    if collected_item['def'] > 0:
        player_defense += collected_item['def']
        print("Defense increased by", collected_item['def'])

# Function to handle the event in the current room
def handle_random_event(event_list):
    event_info = random.choice(event_list)
    event_type = event_info.get('event_type')
    description = event_info.get('description')

    print("\n" + ("=" * 50))
    print(description)

    if event_type == 'flavor':
        # You can implement additional logic for different flavor events here
        pass
    elif event_type == 'combat':
        enemy_name = event_info.get('enemy')
        combat_result = handle_combat(enemy_name)

        if combat_result == 'win':
            print("\nCongratulations! You defeated the", enemy_name)
        elif combat_result == 'lose':
            print("\nYou were defeated by the", enemy_name + ". Game over.")
        elif combat_result == 'run':
            print("\nYou managed to escape from the", enemy_name)

    print("=" * 50 + "\n")
    
# Function to handle combat encounters
def handle_combat(enemy_name):
    """
    Randomly selects an item from possible_items list and returns it.
    Removes the chosen item from possible_items.
    """
    global player_health, collected_items

    enemy_health = 100
    medpack_uses = 0

    print("\nA " + enemy_name + " is attacking you!")

    while player_health > 0 and enemy_health > 0:
        print("\nYour health:", player_health)
        print(enemy_name + "'s health:", enemy_health)

        action = input("\n[F]ight, [R]un, [U]se Healing Item? ").lower()

        # Fighting
        if action == 'f':
            player_damage = random.randint(10, 20)
            enemy_damage = random.randint(5, 15)

            player_health -= enemy_damage
            enemy_health -= player_damage

            if player_health <= 0:
                print("\nYou have been defeated.")
                return 'lose'

            if enemy_health <= 0:
                print("\nYou defeated the", enemy_name + "!")
                return 'win'

        # Running
        elif action == 'r':
            print("\nYou choose to run away.")
            return 'run'

        # Use healing       
        elif action == 'u':
            healing_items = [item for item in collected_items if 'heal' in collected_items[item] and collected_items[item]['heal'] > 0]
            if not healing_items:
                print("\nYou don't have any healing items to use.")
            else:
                print("\nSelect a healing item to use:")
                for index, item in enumerate(healing_items, start=1):
                    print(str(index) + ". " + item + " (Heals " + str(collected_items[item]['heal']) + " HP)")
                choice = input("Enter the number of the healing item to use: ")
                try:
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(healing_items):
                        healing_item = healing_items[choice_index]
                        heal_amount = collected_items[healing_item]['heal']
                        player_health += heal_amount
                        player_health = min(player_health, 100)
                        collected_items[healing_item]['count'] -= 1
                        print("\nYou used a " + healing_item + " and gained " + str(heal_amount) + " health.")
                        print("New health:", player_health)
                        if collected_items[healing_item]['count'] <= 0:
                            del collected_items[healing_item]
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input. Enter the number of the healing item.")
    
    return None

# Main Game Play
def main():
    global current_room, collected_items, player_health

    while True:
        try:
            show_instructions()
            initialize_items()
            show_status()

            while current_room != "Outlaw Camp":
                dir_poss = list(rooms.get(current_room, {}).keys())
                if not dir_poss:
                    print("You are trapped! No available moves.")
                    break

                print('Possible moves:', ', '.join(dir_poss))
                direction = get_valid_direction(dir_poss)
                current_room = rooms[current_room][direction]
                show_status()

                # Randomly choose between random_events (75% chance) and combat_events (25% chance)
                if random.random() < 0.75:
                    event_list = random_events
                else:
                    event_list = combat_events
                    
                event_result = handle_random_event(event_list)
                if event_result == 'lose':
                    print("You were defeated in combat. Game over.")
                    break

            if current_room == "Outlaw Camp":
                event_result = handle_random_event(combat_event_outlaws)  # Use the combat_event_outlaws list only in Flats
            if event_result == 'lose':
                print("You were defeated in combat. Game over.")
                break

            choice = input("Play again? (y/n): ").lower()
            if choice != 'y':
                print("\nThanks for playing the Game......")
                break

            player_health = 100   # Reset the player's health
            player_attack = 10    # Reset the player's attack
            player_defense = 0    # Reset the player's defense
            current_room = "Landing Zone"
            collected_items = {}
            
            # Reset items in rooms
            initialize_items()  # Add this line to reset the items in rooms

        except (KeyError, KeyboardInterrupt):
            print("Oops! There was an error. Please contact the developer.")
            break
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            break

        current_room = "Landing Zone"
        collected_items = {}
            
if __name__ == "__main__":
    main()
