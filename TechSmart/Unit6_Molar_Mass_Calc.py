
import requests

# API endpoint
api_url = "https://api.techsmart.codes/periodic-table/elements"

# Global cache for API data
element_cache = {}

def normalize_chemical_string(chemical_string="", prompt="Enter the chemical string: "):
    """
    Normalizes the input chemical formula by correcting the case of element symbols.
    Args:
        chemical_string (str): The chemical string to normalize.
        prompt (str): Input prompt for user (default provided).
    Returns:
        str: The normalized chemical formula.
    """
    if not chemical_string:
        chemical_string = input(prompt).strip()
    normalized = ""
    for i, char in enumerate(chemical_string):
        if char.isalpha() and char.islower() and (i > 0 and chemical_string[i - 1].isupper()):
            normalized += char.lower()
        elif char.isalpha():
            normalized += char.upper()
        else:
            normalized += char
    return normalized

def parse_chemical_string(chemical_string):
    """
    Parses the chemical string into element symbols and their counts.
    Args:
        chemical_string (str): The chemical string to parse.
    Returns:
        tuple: Lists of element symbols and their corresponding counts.
    """
    element_symbols = []
    element_counts = []
    element_symbol = ""
    count = ""

    for char in chemical_string:
        if char.isalpha():
            if char.isupper():  # New element symbol
                if element_symbol:  # Add previous element
                    element_symbols.append(element_symbol)
                    element_counts.append(int(count) if count else 1)
                element_symbol = char
                count = ""
            else:  # Continue building element symbol
                element_symbol += char
        elif char.isdigit():  # Build count
            count += char

    # Add the last element and count
    if element_symbol:
        element_symbols.append(element_symbol)
        element_counts.append(int(count) if count else 1)

    return element_symbols, element_counts

def fetch_element_data(element):
    """
    Fetches element data from the API or cache.
    Args:
        element (str): The element symbol.
    Returns:
        dict: The element's data.
    """
    global element_cache
    if element in element_cache:
        return element_cache[element]
    
    response = requests.get(api_url + "?symbol=" + element)
    if response.status_code == 200:
        element_data = response.json()
        if element_data:
            element_cache[element] = element_data[0]
            return element_data[0]
    return None

def print_element_details(*args):
    """
    Prints the details of a specific element.
    Args:
        *args: Variable-length argument list containing element details.
    """
    print("\nElement Details:")
    print("  Name: " + args[0])
    print("  Symbol: " + args[1])
    print("  Atomic Mass: " + str(args[2]) + " g/mol")
    print("  State: " + args[3])
    print("  Boiling Point: " + str(args[4]) + " K")
    print("  Electronegativity: " + str(args[5]))
    print("  Density: " + str(args[6]) + " g/cm³")

# Main Program
print("Welcome to the Enhanced Chemical Molar Mass Calculator!\n")
print("Enter the chemical string using element symbols and optional subscripts.")
print("For example, H2O represents water, NaCl represents sodium chloride.\n")
print("Other Commands:")
print("Type 'details <symbol>' for detailed element information (e.g., 'details H').")
print("Type 'exit' to quit the program.")

while True:
    user_input = input("\nEnter your command: ").strip()

    # Exit condition
    if user_input.lower() == "exit":
        print("Thank you for using the Chemical Molar Mass Calculator. Goodbye!")
        break

    # Details command
    if user_input.lower().startswith("details"):
        element_symbol = user_input.split()[-1]
        element_data = fetch_element_data(element_symbol)
        if element_data:
            print_element_details(
                element_data["name"],
                element_data["symbol"],
                element_data["atomicMass"].split("(")[0],
                element_data.get("standardState", "Unknown"),
                element_data.get("boilingPoint", "N/A"),
                element_data.get("electronegativity", "N/A"),
                element_data.get("density", "N/A"),
            )
        else:
            print("Error: No data found for element '" + element_symbol + "'.")
        continue

    # Normalize and parse the chemical string
    chemical_string = normalize_chemical_string(user_input)
    element_symbols, element_counts = parse_chemical_string(chemical_string)

    # Calculate molar mass
    molar_mass = 0
    element_details = []
    for element, count in zip(element_symbols, element_counts):
        element_data = fetch_element_data(element)
        if element_data:
            atomic_mass = float(element_data["atomicMass"].split("(")[0])
            molar_mass += atomic_mass * count
            element_details.append((element_data["name"], element, atomic_mass, count))
        else:
            print("Error: No data found for element '" + element + "'.")
            molar_mass = 0
            break

    # Output results
    if molar_mass > 0:
        print("\nCompound Analysis: " + chemical_string)
        for name, symbol, mass, count in element_details:
            print("  - " + name + " (" + symbol + "): Atomic Mass = " + str(mass) + " x " + str(count))
        print("Total Molar Mass: " + str(round(molar_mass, 2)) + " g/mol.")
    else:
        print("Failed to calculate the molar mass due to errors.")
