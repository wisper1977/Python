"""
Unit4_MolarMass_Calc

Description:
"""

# Dictionary mapping elements to their atomic masses
atomic_masses = {
    "H": 1.0079, "He": 4.0026, "Li": 6.941, "Be": 9.0122, "B": 10.81,
    "C": 12.01, "N": 14.01, "O": 16.00, "F": 19.00, "Ne": 20.18,
    "Na": 22.99, "Mg": 24.31, "Al": 26.98, "Si": 28.09, "P": 30.97,
    "S": 32.07, "Cl": 35.45, "K": 39.10, "Ar": 39.95, "Ca": 40.08,
    "Sc": 44.96, "Ti": 47.87, "V": 50.94, "Cr": 52.00, "Mn": 54.94,
    "Fe": 55.85, "Co": 58.93, "Ni": 58.69, "Cu": 63.55, "Zn": 65.38,
    "Ga": 69.72, "Ge": 72.63, "As": 74.92, "Se": 78.96, "Br": 79.90,
    "Kr": 83.80, "Rb": 85.47, "Sr": 87.62, "Y": 88.91, "Zr": 91.22,
    "Nb": 92.91, "Mo": 95.95, "Tc": 98, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91,
    "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93,
    "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21,
    "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209, "At": 210,
    "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.04, "Pa": 231.04,
    "U": 238.03, "Np": 237, "Pu": 244, "Am": 243, "Cm": 247, "Bk": 247,
    "Cf": 251, "Es": 252, "Fm": 257, "Md": 258, "No": 259, "Lr": 262,
    "Rf": 267, "Db": 270, "Sg": 271, "Bh": 270, "Hs": 277, "Mt": 276,
    "Ds": 281, "Rg": 280, "Cn": 285, "Nh": 284, "Fl": 289, "Mc": 288,
    "Lv": 293, "Ts": 294, "Og": 294
}

# Initialize molar mass
molar_mass = 0

#Instructions
print("Welcome to the Chemical Molar Mass Calculator!\n")
print("Enter a chemical string to find it's Molar Mass")
print("Please enter the first Element, then the count of the Element.")
print("You will get an oportuinity to add one more element and count as well.")

# Process the formula element by element
# First element
element = input("Enter the first element in the formula: ")
count = int(input("Enter the count for the first element (1 if not specified): "))

# Determine the atomic mass for the first element
if element in atomic_masses:
    atomic_mass = atomic_masses[element]
else:
    atomic_mass = 0  # Default atomic mass if element not found

# Calculate the molar mass for the first element
molar_mass += atomic_mass * count

# Second element
element = input("Enter the second element in the formula (leave empty if none): ")

if element:
    count = int(input("Enter the count for the second element (1 if not specified): "))

    # Determine the atomic mass for the second element
    if element in atomic_masses:
        atomic_mass = atomic_masses[element]
    else:
        atomic_mass = 0  # Default atomic mass if element not found

    # Calculate the molar mass for the second element
    molar_mass += atomic_mass * count

# Print the calculated molar mass
print("The molar mass of the compound is approximately {:.2f} g/mol.".format(molar_mass))
