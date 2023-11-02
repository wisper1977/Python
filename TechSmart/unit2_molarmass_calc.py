# Initialize molar mass
molar_mass = 0

# Process the formula element by element

# First element
element = input("Enter the first element in the formula: ")
count = int(input("Enter the count for the first element (1 if not specified): "))

# Determine the atomic mass for the first element
if element == "H":
    atomic_mass = 1.0079
elif element == "He":
    atomic_mass = 4.0026
elif element == "Li":
    atomic_mass = 6.941
elif element == "Be":
    atomic_mass = 9.0122
elif element == "B":
    atomic_mass = 10.81
elif element == "C":
    atomic_mass = 12.01
elif element == "N":
    atomic_mass = 14.01
elif element == "O":
    atomic_mass = 16.00
elif element == "F":
    atomic_mass = 19.00
elif element == "Ne":
    atomic_mass = 20.18
elif element == "Na":
    atomic_mass = 22.99
elif element == "Mg":
    atomic_mass = 24.31
elif element == "Al":
    atomic_mass = 26.98
elif element == "Si":
    atomic_mass = 28.09
elif element == "P":
    atomic_mass = 30.97
elif element == "S":
    atomic_mass = 32.07
elif element == "Cl":
    atomic_mass = 35.45
elif element == "K":
    atomic_mass = 39.10
elif element == "Ar":
    atomic_mass = 39.95
# Add more elements and their atomic masses here

# Calculate the molar mass for the first element
molar_mass += atomic_mass * count

# Check for a second element and its count
element = input("Enter the second element in the formula (leave empty if none): ")

if element:
    count = int(input("Enter the count for the second element (1 if not specified): "))

    # Determine the atomic mass for the second element
    if element == "H":
        atomic_mass = 1.0079
    elif element == "He":
        atomic_mass = 4.0026
    elif element == "Li":
        atomic_mass = 6.941
    elif element == "Be":
        atomic_mass = 9.0122
    elif element == "B":
        atomic_mass = 10.81
    elif element == "C":
        atomic_mass = 12.01
    elif element == "N":
        atomic_mass = 14.01
    elif element == "O":
        atomic_mass = 16.00
    elif element == "F":
        atomic_mass = 19.00
    elif element == "Ne":
        atomic_mass = 20.18
    elif element == "Na":
        atomic_mass = 22.99
    elif element == "Mg":
        atomic_mass = 24.31
    elif element == "Al":
        atomic_mass = 26.98
    elif element == "Si":
        atomic_mass = 28.09
    elif element == "P":
        atomic_mass = 30.97
    elif element == "S":
        atomic_mass = 32.07
    elif element == "Cl":
        atomic_mass = 35.45
    elif element == "K":
        atomic_mass = 39.10
    elif element == "Ar":
        atomic_mass = 39.95
    # Add more elements and their atomic masses here

    # Calculate the molar mass for the second element
    molar_mass += atomic_mass * count

# Print the calculated molar mass
print("The molar mass of the compound is approximately {:.2f} g/mol.".format(molar_mass))
