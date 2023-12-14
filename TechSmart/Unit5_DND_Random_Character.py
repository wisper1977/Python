import requests
import random

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to fetch data from " + url)
        return None

print("Welcome to the DnD 5e Random Character Generator!")

while True:
    print("\nOptions:")
    print("1. Generate Random Character")
    print("2. Exit")

    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        # Fetch class data
        base_url = "https://www.dnd5eapi.co/api/"
        class_data_response = requests.get(base_url + "classes/")
        
        if class_data_response.status_code == 200:
            class_data = class_data_response.json()
            character_class = random.choice(class_data["results"])
        else:
            print("Error: Unable to fetch class data.")
            continue
        
        # Fetch race data
        race_data_response = requests.get(base_url + "races/")

        if race_data_response.status_code == 200:
            race_data = race_data_response.json()
            character_race = random.choice(race_data["results"])
        else:
            print("Error: Unable to fetch race data.")
            continue

        # Get the race's attribute bonuses
        race_bonuses = character_race.get("ability_bonuses", [])

        # Set initial attribute scores
        attributes = {
            "Strength": 8,
            "Dexterity": 8,
            "Constitution": 8,
            "Intelligence": 8,
            "Wisdom": 8,
            "Charisma": 8
        }

        # Apply race attribute bonuses
        for bonus in race_bonuses:
            attribute_data = fetch_data(base_url + bonus["url"])
            if attribute_data:
                attribute_name = attribute_data["full_name"]
                attributes[attribute_name] += bonus["bonus"]

        # Determine class priorities and distribute points accordingly
        class_attributes = {
            "Barbarian": ["Strength", "Constitution"],
            "Bard": ["Charisma", "Dexterity"],
            "Cleric": ["Wisdom", "Constitution"],
            "Druid": ["Wisdom", "Constitution"],
            "Fighter": ["Strength", "Constitution"],
            "Monk": ["Dexterity", "Wisdom"],
            "Paladin": ["Strength", "Charisma"],
            "Ranger": ["Dexterity", "Wisdom"],
            "Rogue": ["Dexterity", "Charisma"],
            "Sorcerer": ["Charisma", "Constitution"],
            "Warlock": ["Charisma", "Constitution"],
            "Wizard": ["Intelligence", "Constitution"]
        }

        if character_class["name"] in class_attributes:
            priority_attributes = class_attributes[character_class["name"]]
            remaining_points = 27 - len(priority_attributes)

            for attribute in priority_attributes:
                increase_amount = random.randint(1, 5)
                attributes[attribute] += increase_amount
                remaining_points -= increase_amount

        # Fetch all skills at once
        all_skills_response = requests.get(base_url + "skills/")
        if all_skills_response.status_code == 200:
            all_skills_data = all_skills_response.json()
            class_skills = [skill["name"] for skill in all_skills_data["results"] if skill["index"] in character_class.get("proficiencies", [])]
        else:
            print("Error: Unable to fetch skill data.")
            class_skills = []

        # Distribute points to class skills
        if class_skills:
            class_skill_points = random.randint(1, remaining_points)
            for _ in range(class_skill_points):
                random_skill = random.choice(class_skills)
                print("Allocating a point to {}".format(random_skill))
                # You can perform further logic here based on how you want to handle skill points

        while remaining_points > 0:
            random_attribute = random.choice(list(attributes.keys()))
            increase_amount = random.randint(1, min(remaining_points, 5))
            attributes[random_attribute] += increase_amount
            remaining_points -= increase_amount

        print("\nRandomly Generated Character:")
        print("Class: {}".format(character_class["name"]))
        print("Race: {}".format(character_race['name']))
        print("Final Attributes:")
        for attribute, value in attributes.items():
            print("{}: {}".format(attribute, value))
        print("Class Skills:")
        for skill in class_skills:
            print(skill)
    elif choice == '2':
        print("Exiting the character generator. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option (1/2).")
