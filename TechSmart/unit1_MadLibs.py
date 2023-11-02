# Print instructions
print("Let's write a Madlib together!\nA madlib is a short story where you fill in the blanks.\n")

# Ask for inputs
adjective = input("Enter a one-syllable adjective: ")
food_plural = input("Enter a plural food: ")
vehicle = input("Enter something you would ride in: ")
verb = input("Enter a verb: ")
color = input("Enter a color: ")
noun = input("Enter a noun: ")
food_plural2 = input("Enter a plural food: ")
food_plural3 = input("Enter a plural food: ")
person = input("Enter a person: ")
saying = input("Enter a saying: ")

# Create the Madlib story
madlib = "Today I went to my favorite Taco Stand called the " + adjective + " " + food_plural + "."
madlib += " Unlike most food stands, they cook and prepare the food in a " + vehicle + " while you " + verb + ". "
madlib += "The best thing on the menu is the " + color + " " + noun + ". "
madlib += "Instead of ground beef, they fill the taco with " + food_plural2 + ", cheese, and top it off with a salsa made from " + food_plural3 + ". "
madlib += "If that doesn't make your mouth water, then it's just like " + person + " always says: " + saying + "!\n"

# Print Madlib
print(madlib)
