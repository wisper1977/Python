"""
Army Combat 1
Created by: Chris Collins
"""

# Dictionary of rooms and directions
rooms = {'Landing Zone': {'South': 'Forest'},
         'Forest': {'South': 'Meadow', 'North': 'Landing Zone', 'East':'Expansive Forest', 'West':'Expansive Forest'},
         'Expansive Forest': {'East': 'Forest', 'West':'Forest'},
         'Meadow': {'North': 'Forest', 'East': 'Expansive Meadow', 'West': 'Expansive Meadow', 'South': 'Desert'},
         'Expansive Meadow': {'East': 'Meadow', 'West':'Meadow'},
         'Desert': {'North': 'Meadow','East':'Expansive Desert', 'West':'Expansive Desert','South': 'Flats'},
         'Expansive Desert': {'East': 'Desert', 'West': 'Desert'},
         'Flats': {'North': 'Desert'}
         }

# Dictionary of items in each room
items = {'Meadow': 'Helmet',
         'Expansive Meadow': 'Ammo',
         'Forest': 'Rifle',
         'Expansive Forest': 'Grenade',
         'Desert': 'Flack Vest',
         'Expansive Desert': 'Medpac'}

# Variable Setup
items_collected = []
current_room = "Landing Zone"
choice = "y"

#function
def get_new_current_room(current_room,move):
    new_current_room = current_room #declaring
    for i in rooms: #loop

        if i == current_room: # if
            if move in rooms[i]: # if
                new_current_room=rooms[i][move] #assigning new_state

def show_instructions():
    #print a main menu and the commands
    print("-------Army Combat--------")
    print("You have parachuted into a Landing Zone, your equipment")
    print("scatterd across the map.")
    print("")
    print("Your Objective: Collect your gear, to attack the Outlaws")
    print("")
    print("Move commands: South, North, East, West")
    print("---------------------------")

def show_status():
    #print character status
    if current_room == "Landing Zone":
        print("")
        print("Inventory: ", items_collected)
        print("")
        print("You are now in the Landing Zone")
        print("There are no items here.")
    elif current_room == "Flats":
        print("")
        print("Inventory: ", items_collected)
        print("")
        print("You are now in the Flats")
    else:
        print("You are now in the " + current_room)
        print("Inventory: ", items_collected)
        print("")
        if items[current_room] == None or items[current_room] in items_collected:
            print("There are no items in this room")
        elif items[current_room] not in items_collected:
            print("You see a", items[current_room])
            print("You found a", items[current_room])
        item_question = input("Would you like to pick item up (y/n)? ")
        if item_question == "y":
            items_collected.append(items[current_room])
    print("---------------------------")

show_instructions() #calling function
show_status()

# Loop for check if the player wants to play again
while choice == "y":

    # Loop for checking if in the flats
    while current_room != "Flats":
        print("")
        temp = rooms[current_room]
        dir_poss = list(temp.keys())
        print('The possible moves are: ', dir_poss)

        direction = input("Type the direction you want to move: ")
        print("")
        direction = direction.capitalize()  # making first character capital remaining lower

        if direction not in dir_poss:
            print("Impassable Mountains loom in front of you.....")
            print("Enter a possible direction from current room")
        else:
            # Checking the directions and corresponding movements
            if direction == "East":
                current_room = rooms[current_room][direction]
                if current_room == 'Flats':
                    break
                else:
                    show_status()
            elif direction == "West":
                current_room = rooms[current_room][direction]
                if current_room == 'Flats':
                    break
                else:
                    show_status()
            elif direction == "North":
                current_room = rooms[current_room][direction]
                if current_room == 'Flats':
                    break
                else:
                    show_status()
            elif direction == "South":
                current_room = rooms[current_room][direction]
                if current_room == 'Flats':
                    break
                else:
                    show_status()
            else:
                print("You entered an invalid direction ", dir_poss)

    # Removing None values from the item collected list
    res = []
    for val in items_collected:
        if val != None:
            res.append(val)

    if len(res) == 6:
        show_status()
        print("Fight Progressing..........")
        print("You defeated the OUTLAWS !!! <3 <3 <3")
    else:
        show_status()
        print("Fight Progressing..........")
        print("You don't have all the items to fight the Outlaws. You have been defeated!")

    print("")
    
    # Continue Game Loop
    choice = input("Do you want play again (y/n): ")
    if choice == 'y':
        current_room = "Landing Zone"
        items_collected = []
        pass
    else:
        print("")
        print("Thanks for playing the Game......")
        break
