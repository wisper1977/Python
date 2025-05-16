"""
Army Combat v1.1.0
by: Chris Collins
"""

# Import Modules
import random, os

# Dictionary of rooms and directions
rooms = {
    'Landing Zone': {
        'description': "You find yourself amidst a dense and ancient forest. The air is rich with the scent of pine, and beams of sunlight pierce through the thick canopy.",
        'South': 'Forest'
    },
    'Forest': {
        'description': "You stand in a realm of shadows and whispers. Towering trees with gnarled branches encircle you, creating an otherworldly ambience.",
        'South': 'Meadow',
        'North': 'Landing Zone',
        'East': 'Forest Glade',
        'West': 'Creek Bank'
    },
    'Forest Glade': {
        'description': "Stepping into this secluded glade is like entering a secret haven of tranquility. Sunbeams dance through the emerald foliage, painting patterns of light on the forest floor.",
        'East': 'Deep Forest',
        'West': 'Forest'
    },
    'Creek Bank': {
        'description': "At the creek's edge, crystal-clear water flows gently over smooth pebbles. The serene gurgling of the creek blends harmoniously with the rustling leaves.",
        'East': "Forest",
        'West': 'Deep Forest',
        'South': 'Winding Brook'
    },
    'Deep Forest': {
        'description': "Venturing further into the heart of the forest, you become enveloped in an enigmatic realm. Ancient trees form an intricate maze, and dappled sunlight creates mesmerizing patterns.",
        'East': 'Creek Bank',
        'West': 'Forest Glade'
    },
    'Meadow': {
        'description': "The meadow stretches out like an artist's canvas. Wildflowers of every hue sway in unison, their delicate fragrances carried by the breeze.",
        'North': 'Forest',
        'East': 'Grazing Pasture',
        'West': 'Winding Brook',
        'South': 'Desert'
    },
    'Winding Brook': {
        'description': "You follow the path of a meandering brook, its babbling melody a soothing accompaniment to your journey. Ferns and mosses thrive in the damp, fertile soil.",
        'East': 'Meadow',
        'West': 'Verdant Expanse',
        'North': 'Creek Bank',
        'South': 'Dried Riverbed'
    },
    'Grazing Pasture': {
        'description': "A serene pasture greets you, where contented animals graze peacefully. The distant lowing of cattle and the soft swaying of grass create a serene pastoral symphony.",
        'East': 'Verdant Expanse',
        'West': 'Meadow'
    },
    'Verdant Expanse': {
        'description': "You find yourself in a breathtaking verdant expanse. The meadow seems to stretch beyond the horizon, a sea of vibrant green that dances in harmony with the wind.",
        'East': 'Winding Brook',
        'West': 'Grazing Pasture'
    },
    'Desert': {
        'description': "The desert's embrace is both harsh and awe-inspiring. Waves of heat rise from the sun-scorched sand, and the distant horizon shimmers with mirages.",
        'North': 'Meadow',
        'East': 'Oasis',
        'West': 'Dried Riverbed',
        'South': 'Flats'
    },
    'Dried Riverbed': {
        'description': "At the dried riverbed, fractured earth whispers stories of ancient waters. It's a landscape of contrasts, where the memory of flowing rivers meets the arid present.",
        'East': 'Desert',
        'West': 'Scorched Wasteland',
        'North': 'Winding Brook'
    },
    'Oasis': {
        'description': "An oasis of life amidst the desert's desolation. Palm trees sway in the breeze, and the clear pool reflects the vibrant blue sky like a precious gem.",
        'East': 'Scorched Wasteland',
        'West': 'Desert'
    },
    'Scorched Wasteland': {
        'description': "The wasteland stretches endlessly, a harsh testament to nature's unforgiving side. Heatwaves distort the air, and the silence is broken only by the distant call of a desert creature.",
        'East': 'Dried Riverbed',
        'West': 'Oasis'
    },
    'Flats': {
        'description': "You step onto the flats, an open and barren expanse that stretches as far as the eye can see. The land is still, a canvas awaiting the story of your journey.",
        'East': 'Solemn Savannah',
        'West': 'Lonely Steppe',
        'North': 'Desert',
        'South': 'Outlaw Camp'
    },
    'Lonely Steppe': {
        'description': "You find yourself on a lonely steppe, the vast open landscape stretching far and wide. The wind carries the scent of earth and grass.",
        'East': 'Flats',
        'West': 'Desolate Expanse'
    },
    'Solemn Savannah': {
        'description': "You enter a solemn savannah, the ground rolling gently under your feet. The stillness of the landscape fills you with a sense of reverence.",
        'East': 'Desolate Expanse',
        'West': 'Flats'
    },
    'Desolate Expanse': {
        'description': "The land before you is desolate and expansive. It's a place of emptiness and solitude, where the horizon seems distant and unreachable.",
        'East': 'Lonely Steppe',
        'West': 'Solemn Savannah'
    },
    'Outlaw Camp': {
        'description': "You've reached the outlaw camp, a makeshift settlement in the flats. Tents and fires tell tales of lawlessness and danger. Keep your guard up.",
        'North': 'Flats'
    }
}

# Dictionary of items in each room
items = {room: None for room in rooms}

# Separate list for combat events
events = [
    {'event_type': 'combat', 'description': "\nYou encounter hostile creatures!", 'enemy': 'Creatures'},
    {'event_type': 'combat', 'description': "\nA group of bandits attacks!", 'enemy': 'Bandits'},
    {'event_type': 'combat', 'description': "\nYou encounter a hostile group of looters!", 'enemy': 'Looters'},
    {'event_type': 'combat', 'description': "\nA rival faction ambushes you!", 'enemy': 'Rival Faction'},
    {'event_type': 'combat', 'description': "\nA pack of feral dogs attacks!", 'enemy': 'Feral Dogs'},
    {'event_type': 'flavor', 'description': "\nYou hear strange noises in the distance."},
    {'event_type': 'flavor', 'description': "\nA mysterious mist envelops the area."},
    {'event_type': 'flavor', 'description': "\nYou stumble upon an old campsite."},
    {'event_type': 'flavor', 'description': "\nYou find a hidden cache of supplies."},
    {'event_type': 'flavor', 'description': "\nA sudden rainstorm forces you to take shelter."},
    {'event_type': 'flavor', 'description': "\nYou come across an abandoned vehicle."},
    {'event_type': 'flavor', 'description': "\nYou discover a torn map with a mysterious location marked."},
    {'event_type': 'flavor', 'description': "\nYou stumble upon a makeshift campfire."},
    {'event_type': 'combat', 'description': "\nThe Outlaws have found you!", 'enemy': 'Outlaws'},
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
event_result = ""

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Function to place items in random rooms
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

# Function to place item in rooms
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
        direction = input("Choose a direction to move: " + ", ".join([move for move in dir_poss if move != 'description']) + ": ").capitalize()
        if direction in dir_poss:
            return direction
        print("Invalid direction. Choose from:", ", ".join([move for move in dir_poss if move != 'description']))

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
    
    input("\nPress Enter to start the game...")

# Function to display the player's status
def show_status():
    try:
        global player_health, player_attack, player_defense, collected_items
        global current_room, rooms, items

        print("-" * 50)
        print("Health: " + str(player_health))
        print("Attack: " + str(player_attack))
        print("Defense: " + str(player_defense))
        print("-" * 50)
        print("You are now in the " + current_room)
        print("Description: " + rooms.get(current_room, {}).get('description', 'No description available.'))

        item = items.get(current_room)
        if item and item['name'] not in collected_items:
            print("\nThere is a " + item['name'] + " in the room.")

            while True:
                choice = input("Would you like to pick up the " + item['name'] + "? (y/n): ").strip().lower()
                if choice in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'.")

            if choice == 'y':
                collected_items[item['name']] = item
                player_attack += item.get('att', 0)
                player_defense += item.get('def', 0)
                print("You picked up the " + item['name'] + ".")

                if 'heal' in item and item['heal'] > 0:
                    print("This item will heal you when used in combat.")

                if 'max_uses' in item:
                    item['uses_left'] = item['max_uses']
                    print(item['name'] + " can be used " + str(item['uses_left']) + " more time(s).")

                if 'max_uses' not in item:
                    del items[current_room]

        print("-" * 50)
        show_inventory()
    except Exception as e:
        print("An error occurred while accessing room information: " + str(e))
        
def show_inventory():
    """Function to display the player's inventory."""
    global collected_items
    print(("-" * 19) + " Inventory " + ("-" * 20))
    if not collected_items:
        print("Your inventory is empty.")
    else:
        for item_name, item in collected_items.items():
            count = item.get('count', 1)
            if item.get('heal', 0) > 0:
                item_count = " x" + str(count) if count > 1 else ""
                if 'uses' in item and item['uses'] > 0:
                    uses_info = " (Uses: {}/{})".format(item['uses'], item.get('max_uses', 1))
                    print("{}{}{} (Heals: {} HP)".format(item_name, item_count, uses_info, item['heal']))
                else:
                    print("{}{} (Heals: {} HP)".format(item_name, item_count, item['heal']))
            else:
                print(item_name)
    print("-" * 50)
            
# Function to collect an item in the current room
def collect_item(room_name):
    global collected_items, player_attack, player_defense
    collected_item = items[room_name]
    
    item_name = collected_item['name']
    if item_name not in collected_items:
        collected_items[item_name] = {
            'count': 1, 
            'max_uses': collected_item.get('max_uses', 0),  # Keep track of the original uses
            'uses': collected_item.get('max_uses', 0),  # Initialize uses with the max_uses value if available
            'heal': collected_item.get('heal', 0)  # Copy the 'heal' attribute
        }
    else:
        collected_items[item_name]['count'] += 1
        collected_items[item_name]['uses'] = collected_items[item_name]['max_uses']
        
    print("You picked up a", item_name)
    print("Collected", collected_items[item_name]['count'], item_name + "(s)")
    
    if collected_item['att'] > 0:
        player_attack += collected_item['att']
        print("Attack increased by", collected_item['att'])
    if collected_item['def'] > 0:
        player_defense += collected_item['def']
        print("Defense increased by", collected_item['def'])

# Use Healing Item
def use_medical_item():
    global player_health, collected_items
     
    # Filter healing items: items must have 'heal' > 0 and 'uses_left' and 'max_uses'
    healing_items = [item for item in collected_items if 'heal' in collected_items[item] and collected_items[item]['heal'] > 0 and 'uses_left' in collected_items[item] and 'max_uses' in collected_items[item]]
     
    if not healing_items:
        print("\nYou don't have any healing items to use.")
        return
    
    print("\nSelect a healing item to use:")
    # Enumerate the healing items and display their stats
    for index, item in enumerate(healing_items, start=1):
        item_data = collected_items[item]
        print("{}. {} (Uses: {}/{}) (Heals {} HP)".format(index, item, item_data['uses_left'], item_data['max_uses'], item_data['heal']))
    
    choice = input("Enter the number of the healing item to use: ")
    try:
        # Check if the user input is valid
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(healing_items):
            healing_item = healing_items[choice_index]
            item_data = collected_items[healing_item]
            
            if item_data['uses_left'] > 0:
                # Apply healing
                heal_amount = item_data['heal']
                player_health += heal_amount
                player_health = min(player_health, 100)  # Ensure health doesn't exceed 100
                item_data['uses_left'] -= 1  # Decrement the remaining uses
                print("\nYou used a {} and gained {} health.".format(healing_item, heal_amount))
                print("New health:", player_health)
                
                if item_data['uses_left'] == 0:
                    print("You have used up all the allowed uses for this item.")
            else:
                print("This item has no remaining uses.")
        else:
            print("Invalid choice. Please select a valid number between 1 and {}".format(len(healing_items)))
    except ValueError:
        print("Invalid input. Please enter a valid number corresponding to the healing item.")
        
# Function to handle the event in the current room
def handle_random_event(event_list, current_room):
    global event_result
    while True:
        event_info = random.choice(event_list)
        event_type = event_info.get('event_type')
        description = event_info.get('description')
        enemy_name = event_info.get('enemy')

        # Skip non-Outlaw events in the Outlaw Camp
        if current_room == "Outlaw Camp" and (event_type == 'combat' and enemy_name != "Outlaws"):
            continue

        print("\n" + ("=" * 50))
        print(description)

        if event_type == 'flavor':
            # Add more logic for flavor events if needed
            pass

        elif event_type == 'combat':
            event_result = handle_combat(enemy_name)

            if event_result == 'win':
                print("\nCongratulations! You defeated the", enemy_name)
            elif event_result == 'lose':
                print("\nYou were defeated by the", enemy_name + ". Game over.")
                return 'defeat'
            elif event_result == 'run':
                print("\nYou managed to escape from the", enemy_name)

        print("=" * 50 + "\n")
        break  # Exit loop after a valid event is handled
    
# Function to handle combat encounters
def handle_combat(enemy_name):
    """
    Handles the combat interaction, including using healing items.
    """
    global player_health, collected_items

    enemy_health = 100

    print("\nA " + enemy_name + " is attacking you!")

    while player_health > 0 and enemy_health > 0:
        print("\nYour health:", player_health)
        print(enemy_name + "'s health:", enemy_health)

        if player_health <= 0:
            print("\nYou have been defeated.")
            replay_game()
            return 'defeat'
        
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

        # Use healing item
        elif action == 'u':
            use_medical_item()  # Call the use_medical_item function to handle healing items.
            
    return None

# Function for replay logic
def reset_game():
    global player_health, player_attack, player_defense
    global collected_items, current_room, items, possible_items

    try:     
        # Reset player stats
        player_health = 100
        player_attack = 10
        player_defense = 0
        collected_items = {}
        current_room = "Landing Zone"
    
        # Reset possible_items to the full list
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
        ]
    
        # Reset items in each room
        items = {room: None for room in rooms}
        initialize_items()
        
    except (KeyError, KeyboardInterrupt):
        print("Oops! There was an error. Please contact the developer.")
        return False
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return False

    return True  # The game should continue
    
# Main Game Play
def main():
    global current_room, collected_items, player_health

    while True:
        try:
            reset_game()
            clear_screen()
            show_instructions()
            show_status()

            while current_room != "Outlaw Camp":
                dir_poss = list(rooms.get(current_room, {}).keys())
                if not dir_poss:
                    print("You are trapped! No available moves.")
                    break

                print('You are in ' + current_room + ', your possible moves are: ' + ', '.join([move for move in dir_poss if move != 'description']))
                direction = get_valid_direction(dir_poss)
                current_room = rooms[current_room][direction]
                clear_screen()
                show_status()

                if random.random() < 0.75:
                    filtered_events = [e for e in events if e['event_type'] == 'flavor']
                else:
                    filtered_events = [e for e in events if e['event_type'] == 'combat']
                
                if current_room != "Outlaw Camp":
                    filtered_events = [
                        e for e in filtered_events
                        if not (e.get('enemy') == 'Outlaws' and e['event_type'] == 'combat')
                    ]
                
                # Call the handler if there are any valid events
                if filtered_events:
                    event_result = handle_random_event(filtered_events, current_room)
                    if event_result == 'defeat':
                        break

            play_again = input("\nDo you want to play again? (y/n): ").lower()
            if play_again == "y":
                reset_game()
                main()  # or however your main loop starts
            else:
                print("Thanks for playing!")

        except (KeyError, KeyboardInterrupt):
            print("Oops! There was an error. Please contact the developer.")
            break
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            break

if __name__ == "__main__":
    main()
