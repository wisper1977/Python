"""
Unit 1
Code Your Own: Unit 1
[Madlib]
"""

# Print instructions
print("Let's write a Madlib together!\nA madlib is a short story where you fill in the blanks.\n")

# First sentence
madlib = "Today I went to my favorite Taco Stand called the " + input("Enter a one-syllable adjective: ") + " " + input("Enter a plural Food: ") + "."

# Second sentence
madlib += "Unlike most food stands, they cook and prepare the food in a " + input("Enter something you would ride in: ") + " while you " + input("Enter a verb: ") + " . "

# Third sentence
madlib += "The best thing on the menu is the " + input("Enter a color: ") + " " + input("Enter a noun: ") + ". "

# Fourth sentence
madlib += "Instead of ground beef they fill the taco with " + input("Enter a plural food: ") + ", cheese, and top it off with a salsa made from " + input("Enter a plural food: ") + ". "

# Fifth sentence
madlib += "If that doesn't make your mouth water, then it' just like " + input("Enter a Person: ") + " always says: " + input("Enter a saying: ") + "!\n"

# Print Madlib
print(madlib)
