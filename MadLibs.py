"""
Unit 1
Code Your Own: Unit 1
Madlib
"""

# Print instructions
print("Let's write a Madlib together!\nA madlib is a short story where you fill in the blanks.\n")

# First sentence
madlib = "Today I went to my favorite Taco Stand called the "
madlib += input("Enter a one-syllable adjective: ")
madlib += " "
madlib += input("Enter a plural Food: ")
madlib += ". "

# Second sentence
madlib += "Unlike most food stands, they cook and prepare the food in a "
madlib += input("Enter something you would ride in: ")
madlib += " while you "
madlib += input("Enter a verb: ")
madlib += " . "

# Third sentence
madlib += "The best thing on the menu is the "
madlib += input("Enter a color: ")
madlib += " "
madlib += input("Enter a noun: ")
madlib += ". "

# Fourth sentence
madlib += "Instead of ground beef they fill the taco with "
madlib += input("Enter a plural food: ")
madlib += ", cheese, and top it off with a salsa made from "
madlib += input("Enter a plural food: ")
madlib += ". "

# Fifth sentence
madlib += "If that doesn't make your mouth water, then it' just like "
madlib += input("Enter a Person: ")
madlib += "always says: "
madlib += input("Enter a saying: ")
madlib += "!\n"

# Print Madlib
print(madlib)
