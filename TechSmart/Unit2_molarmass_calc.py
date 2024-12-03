"""
Unit2_MolarMass_Calc

Description:
"""

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
elif element == "Ca":
    atomic_mass = 40.08
elif element == "Sc":
    atomic_mass = 44.96
elif element == "Ti":
    atomic_mass = 47.87
elif element == "V":
    atomic_mass = 50.94
elif element == "Cr":
    atomic_mass = 52.00
elif element == "Mn":
    atomic_mass = 54.94
elif element == "Fe":
    atomic_mass = 55.85
elif element == "Co":
    atomic_mass = 58.93
elif element == "Ni":
    atomic_mass = 58.69
elif element == "Cu":
    atomic_mass = 63.55
elif element == "Zn":
    atomic_mass = 65.38
elif element == "Ga":
    atomic_mass = 69.72
elif element == "Ge":
    atomic_mass = 72.63
elif element == "As":
    atomic_mass = 74.92
elif element == "Se":
    atomic_mass = 78.96
elif element == "Br":
    atomic_mass = 79.90
elif element == "Kr":
    atomic_mass = 83.80
elif element == "Rb":
    atomic_mass = 85.47
elif element == "Sr":
    atomic_mass = 87.62
elif element == "Y":
    atomic_mass = 88.91
elif element == "Zr":
    atomic_mass = 91.22
elif element == "Nb":
    atomic_mass = 92.91
elif element == "Mo":
    atomic_mass = 95.95
elif element == "Tc":
    atomic_mass = 98
elif element == "Ru":
    atomic_mass = 101.07
elif element == "Rh":
    atomic_mass = 102.91
elif element == "Pd":
    atomic_mass = 106.42
elif element == "Ag":
    atomic_mass = 107.87
elif element == "Cd":
    atomic_mass = 112.41
elif element == "In":
    atomic_mass = 114.82
elif element == "Sn":
    atomic_mass = 118.71
elif element == "Sb":
    atomic_mass = 121.76
elif element == "Te":
    atomic_mass = 127.60
elif element == "I":
    atomic_mass = 126.90
elif element == "Xe":
    atomic_mass = 131.29
elif element == "Cs":
    atomic_mass = 132.91
elif element == "Ba":
    atomic_mass = 137.33
elif element == "La":
    atomic_mass = 138.91
elif element == "Ce":
    atomic_mass = 140.12
elif element == "Pr":
    atomic_mass = 140.91
elif element == "Nd":
    atomic_mass = 144.24
elif element == "Pm":
    atomic_mass = 145
elif element == "Sm":
    atomic_mass = 150.36
elif element == "Eu":
    atomic_mass = 151.96
elif element == "Gd":
    atomic_mass = 157.25
elif element == "Tb":
    atomic_mass = 158.93
elif element == "Dy":
    atomic_mass = 162.50
elif element == "Ho":
    atomic_mass = 164.93
elif element == "Er":
    atomic_mass = 167.26
elif element == "Tm":
    atomic_mass = 168.93
elif element == "Yb":
    atomic_mass = 173.05
elif element == "Lu":
    atomic_mass = 174.97
elif element == "Hf":
    atomic_mass = 178.49
elif element == "Ta":
    atomic_mass = 180.95
elif element == "W":
    atomic_mass = 183.84
elif element == "Re":
    atomic_mass = 186.21
elif element == "Os":
    atomic_mass = 190.23
elif element == "Ir":
    atomic_mass = 192.22
elif element == "Pt":
    atomic_mass = 195.08
elif element == "Au":
    atomic_mass = 196.97
elif element == "Hg":
    atomic_mass = 200.59
elif element == "Tl":
    atomic_mass = 204.38
elif element == "Pb":
    atomic_mass = 207.2
elif element == "Bi":
    atomic_mass = 208.98
elif element == "Po":
    atomic_mass = 209
elif element == "At":
    atomic_mass = 210
elif element == "Rn":
    atomic_mass = 222
elif element == "Fr":
    atomic_mass = 223
elif element == "Ra":
    atomic_mass = 226
elif element == "Ac":
    atomic_mass = 227
elif element == "Th":
    atomic_mass = 232.04
elif element == "Pa":
    atomic_mass = 231.04
elif element == "U":
    atomic_mass = 238.03
elif element == "Np":
    atomic_mass = 237
elif element == "Pu":
    atomic_mass = 244
elif element == "Am":
    atomic_mass = 243
elif element == "Cm":
    atomic_mass = 247
elif element == "Bk":
    atomic_mass = 247
elif element == "Cf":
    atomic_mass = 251
elif element == "Es":
    atomic_mass = 252
elif element == "Fm":
    atomic_mass = 257
elif element == "Md":
    atomic_mass = 258
elif element == "No":
    atomic_mass = 259
elif element == "Lr":
    atomic_mass = 262
elif element == "Rf":
    atomic_mass = 267
elif element == "Db":
    atomic_mass = 270
elif element == "Sg":
    atomic_mass = 271
elif element == "Bh":
    atomic_mass = 270
elif element == "Hs":
    atomic_mass = 277
elif element == "Mt":
    atomic_mass = 276
elif element == "Ds":
    atomic_mass = 281
elif element == "Rg":
    atomic_mass = 280
elif element == "Cn":
    atomic_mass = 285
elif element == "Nh":
    atomic_mass = 284
elif element == "Fl":
    atomic_mass = 289
elif element == "Mc":
    atomic_mass = 288
elif element == "Lv":
    atomic_mass = 293
elif element == "Ts":
    atomic_mass = 294
elif element == "Og":
    atomic_mass = 294

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
    elif element == "Ca":
        atomic_mass = 40.08
    elif element == "Sc":
        atomic_mass = 44.96
    elif element == "Ti":
        atomic_mass = 47.87
    elif element == "V":
        atomic_mass = 50.94
    elif element == "Cr":
        atomic_mass = 52.00
    elif element == "Mn":
        atomic_mass = 54.94
    elif element == "Fe":
        atomic_mass = 55.85
    elif element == "Co":
        atomic_mass = 58.93
    elif element == "Ni":
        atomic_mass = 58.69
    elif element == "Cu":
        atomic_mass = 63.55
    elif element == "Zn":
        atomic_mass = 65.38
    elif element == "Ga":
        atomic_mass = 69.72
    elif element == "Ge":
        atomic_mass = 72.63
    elif element == "As":
        atomic_mass = 74.92
    elif element == "Se":
        atomic_mass = 78.96
    elif element == "Br":
        atomic_mass = 79.90
    elif element == "Kr":
        atomic_mass = 83.80
    elif element == "Rb":
        atomic_mass = 85.47
    elif element == "Sr":
        atomic_mass = 87.62
    elif element == "Y":
        atomic_mass = 88.91
    elif element == "Zr":
        atomic_mass = 91.22
    elif element == "Nb":
        atomic_mass = 92.91
    elif element == "Mo":
        atomic_mass = 95.95
    elif element == "Tc":
        atomic_mass = 98
    elif element == "Ru":
        atomic_mass = 101.07
    elif element == "Rh":
        atomic_mass = 102.91
    elif element == "Pd":
        atomic_mass = 106.42
    elif element == "Ag":
        atomic_mass = 107.87
    elif element == "Cd":
        atomic_mass = 112.41
    elif element == "In":
        atomic_mass = 114.82
    elif element == "Sn":
        atomic_mass = 118.71
    elif element == "Sb":
        atomic_mass = 121.76
    elif element == "Te":
        atomic_mass = 127.60
    elif element == "I":
        atomic_mass = 126.90
    elif element == "Xe":
        atomic_mass = 131.29
    elif element == "Cs":
        atomic_mass = 132.91
    elif element == "Ba":
        atomic_mass = 137.33
    elif element == "La":
        atomic_mass = 138.91
    elif element == "Ce":
        atomic_mass = 140.12
    elif element == "Pr":
        atomic_mass = 140.91
    elif element == "Nd":
        atomic_mass = 144.24
    elif element == "Pm":
        atomic_mass = 145
    elif element == "Sm":
        atomic_mass = 150.36
    elif element == "Eu":
        atomic_mass = 151.96
    elif element == "Gd":
        atomic_mass = 157.25
    elif element == "Tb":
        atomic_mass = 158.93
    elif element == "Dy":
        atomic_mass = 162.50
    elif element == "Ho":
        atomic_mass = 164.93
    elif element == "Er":
        atomic_mass = 167.26
    elif element == "Tm":
        atomic_mass = 168.93
    elif element == "Yb":
        atomic_mass = 173.05
    elif element == "Lu":
        atomic_mass = 174.97
    elif element == "Hf":
        atomic_mass = 178.49
    elif element == "Ta":
        atomic_mass = 180.95
    elif element == "W":
        atomic_mass = 183.84
    elif element == "Re":
        atomic_mass = 186.21
    elif element == "Os":
        atomic_mass = 190.23
    elif element == "Ir":
        atomic_mass = 192.22
    elif element == "Pt":
        atomic_mass = 195.08
    elif element == "Au":
        atomic_mass = 196.97
    elif element == "Hg":
        atomic_mass = 200.59
    elif element == "Tl":
        atomic_mass = 204.38
    elif element == "Pb":
        atomic_mass = 207.2
    elif element == "Bi":
        atomic_mass = 208.98
    elif element == "Po":
        atomic_mass = 209
    elif element == "At":
        atomic_mass = 210
    elif element == "Rn":
        atomic_mass = 222
    elif element == "Fr":
        atomic_mass = 223
    elif element == "Ra":
        atomic_mass = 226
    elif element == "Ac":
        atomic_mass = 227
    elif element == "Th":
        atomic_mass = 232.04
    elif element == "Pa":
        atomic_mass = 231.04
    elif element == "U":
        atomic_mass = 238.03
    elif element == "Np":
        atomic_mass = 237
    elif element == "Pu":
        atomic_mass = 244
    elif element == "Am":
        atomic_mass = 243
    elif element == "Cm":
        atomic_mass = 247
    elif element == "Bk":
        atomic_mass = 247
    elif element == "Cf":
        atomic_mass = 251
    elif element == "Es":
        atomic_mass = 252
    elif element == "Fm":
        atomic_mass = 257
    elif element == "Md":
        atomic_mass = 258
    elif element == "No":
        atomic_mass = 259
    elif element == "Lr":
        atomic_mass = 262
    elif element == "Rf":
        atomic_mass = 267
    elif element == "Db":
        atomic_mass = 270
    elif element == "Sg":
        atomic_mass = 271
    elif element == "Bh":
        atomic_mass = 270
    elif element == "Hs":
        atomic_mass = 277
    elif element == "Mt":
        atomic_mass = 276
    elif element == "Ds":
        atomic_mass = 281
    elif element == "Rg":
        atomic_mass = 280
    elif element == "Cn":
        atomic_mass = 285
    elif element == "Nh":
        atomic_mass = 284
    elif element == "Fl":
        atomic_mass = 289
    elif element == "Mc":
        atomic_mass = 288
    elif element == "Lv":
        atomic_mass = 293
    elif element == "Ts":
        atomic_mass = 294
    elif element == "Og":
        atomic_mass = 294

    # Calculate the molar mass for the second element
    molar_mass += atomic_mass * count

# Print the calculated molar mass
print("The molar mass of the compound is approximately {:.2f} g/mol.".format(molar_mass))
