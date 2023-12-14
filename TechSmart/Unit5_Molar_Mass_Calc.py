
import requests

# Initialize molar mass
molar_mass = 0
current_element = ""
current_count = 0

# Fetch all element data from the Periodic Table API
api_url = "https://periodic-table-elements-info.herokuapp.com/elements/"

parameters = {"payload":{} , "headers":{}}

response = requests.get(api_url, params=parameters)
print(response.text)

if response.status_code == 200:
    elements_data = response.json()['elements']

    # Display instructions to the user
    print("Welcome to the Molar Mass Calculator!")
    print("Enter a chemical formula, and the program will calculate its molar mass.")
    print("Example: H2O, C6H12O6, NaCl")

    # Get input chemical formula
    formula = input("Enter the chemical formula: ")

    # Process the formula character by character
    for char in formula:
        if char.isalpha():
            current_element += char
        elif char.isdigit():
            current_count = current_count * 10 + int(char)
        else:
            # Look up atomic mass when a non-alphabetic character is encountered
            if current_element:
                matching_element = next((elem for elem in elements_data if elem['symbol'] == current_element), None)
                if matching_element:
                    atomic_mass = matching_element.get('atomic_mass')
                    if atomic_mass is not None:
                        molar_mass += atomic_mass * (current_count if current_count else 1)
            current_element = ""
            current_count = 0

    # Check for the last element in the formula
    if current_element:
        matching_element = next((elem for elem in elements_data if elem['symbol'] == current_element), None)
        if matching_element:
            atomic_mass = matching_element.get('atomic_mass')
            if atomic_mass is not None:
                molar_mass += atomic_mass * (current_count if current_count else 1)

    # Print the calculated molar mass
    print("The molar mass of the compound is approximately {:.2f} g/mol.".format(molar_mass))
else:
    print("Failed to fetch element data from the API.")
