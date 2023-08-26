"""
Army Combat v1.1
by: Chris Collins
"""
# Import Modules
import random

# Dictionary of rooms and directions
rooms = {
    'Landing Zone': {'South': 'Forest'},
    'Forest': {'South': 'Meadow', 'North': 'Landing Zone', 'East': 'Expansive Forest', 'West': 'Expansive Forest'},
    'Expansive Forest': {'East': 'Forest', 'West': 'Forest'},
    'Meadow': {'North': 'Forest', 'East': 'Expansive Meadow', 'West': 'Expansive Meadow', 'South': 'Desert'},
    'Expansive Meadow': {'East': 'Meadow', 'West': 'Meadow'},
    'Desert': {'North': 'Meadow', 'East': 'Expansive Desert', 'West': 'Expansive Desert', 'South': 'Flats'},
    'Expansive Desert': {'East': 'Desert', 'West': 'Desert'},
    'Flats': {'North': 'Desert'}
}

# Dictionary of items in each room
items = {room: None for room in rooms}

# Dictionary of room descriptions
room_descriptions = {
    'Landing Zone': "You find yourself in a dense forest. The air smells of pine.",
    'Forest': "You are in a dimly lit forest. Tall trees surround you.",
    'Expansive Forest': "The forest continues in all directions. The trees seem endless.",
    'Meadow': "You stand in a serene meadow. The grass sways gently in the wind.",
    'Expansive Meadow': "The meadow stretches as far as you can see. The sun warms your face.",
    'Desert': "The landscape changes to a vast desert. The sand is scorching hot.",
    'Expansive Desert': "The desert seems to go on forever. Heatwaves distort your view.",
    'Flats': "You reach the flats. It's an open and barren expanse."
}

# Separate list for combat events
combat_events = [
    {'event_type': 'combat', 'description': "\nYou encounter hostile creatures!", 'enemy': 'Creatures'},
    {'event_type': 'combat', 'description': "\nA group of bandits attacks!", 'enemy': 'Bandits'},
    # Add more combat events here
]

# Dictionary of random events with descriptions and outcomes
random_events = [
    {'event_type': 'flavor', 'description': "\nYou hear strange noises in the distance."},
    {'event_type': 'flavor', 'description': "\nA mysterious mist envelops the area."},
    {'event_type': 'flavor', 'description': "\nYou stumble upon an old campsite."},
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
    {'name': 'Medpac', 'def': 0, 'att': 0, 'heal': 30}  # Add Medpac to the list
]

# Set Variables
player_health = 100
player_attack = 10
player_defense = 0
collected_items = {}
current_room = "Landing Zone"

# Medpac properties
medpack_heal_amount = 30

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
        for room in rooms if room not in ['Landing Zone', 'Flats']
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
        elif current_room == "Flats":
            print("\nYou are now in the Flats")
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


# Function to display the player's inventory
def show_inventory():
    global collected_items
    print(("-" * 19) + " Inventory " + ("-" * 20))
    for item in collected_items:
        if item == 'Medpac':
            print(item + ": " + str(collected_items[item]['count']) + " (Uses: " + str(collected_items[item]['uses']) + "/3)")
        else:
            print(item)
    print("-" * 50)
    
# Function to collect an item in the current room
def collect_item(room_name):
    """
    Randomly selects an item from possible_items list and returns it.
    Removes the chosen item from possible_items.
    """
    global collected_items, player_attack, player_defense
    collected_item = items[room_name]
    
    item_name = collected_item['name']
    if item_name not in collected_items:
        collected_items[item_name] = {'count': 1, 'uses': collected_item.get('uses', 0)}
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

        action = input("\n[F]ight, [R]un, [U]se Med Pack? ").lower()

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

        # Use medpac       
        elif action == 'u':
            medpack = collected_items.get('Medpac', {'count': 0, 'uses': 0})
            if medpack['count'] > 0 and medpack_uses < 3:
                player_health += medpack_heal_amount
                player_health = min(player_health, 100)
                print("\nYou used a Medpac and gained", medpack_heal_amount, "health.")
                print("New health:", player_health)
                medpack_uses += 1
            elif medpack['count'] == 0:
                print("\nYou don't have a Medpac to use.")
            else:
                print("\nYou have already used this Medpac three times.")

    print("\n" + ("-" * 50))
    return None

# Main Game Play
def main():
    global current_room, collected_items, player_health

    while True:
        try:
            show_instructions()
            initialize_items()
            show_status()

            while current_room != "Flats":
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

            if current_room == "Flats":
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
