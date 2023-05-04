"""
User-Defined Functions
Coding Exercise: User-Defined Functions
Password Health
"""

#### ---- Setup ---- ####

Statement = {}

#### ---- Get Passwords ---- ####

def get_passwords(file="badpasswords.txt"):

    ### --- opening the file in read mode --- ###
    my_file = open(file, "r")
      
    ### --- reading the file --- ###
    data = my_file.read()
      
    ### --- replacing end splitting the text --- ###
    ### --- when newline ('\n') is seen. --- ###
    data_into_list = data.split("\n")
    return data_into_list
    my_file.close()

#### ---- Password List ---- ####

def passwords_list(list): 

    user_passwords = list.split (",")
    
    return user_passwords
    
#### ---- Simplified Password ---- ####

def simplified_password(passwords):
    
    simplified_passwords = {}

    for password in passwords:
        original_password = password
        
        password = password.lower()
        
    ### ---- END SYMBOL ---- ####
        
        symbols = "!@#$%^&*.?"
        if password[-1] in symbols:
                password = password[:-1]
        
            #### ---- END DIGITS ---- ####
        
        for i in range(1, len(password)):
            if password[i:].isdigit():
                password = password[:i]
        
            #### ---- SYMBOL REPLACEMENT ---- ####
        
        symbol_map = {
            "@": "a",
            "3": "e",
            "#": "h",
            "1": "l",
            "0": "o",
            "$": "s",
            "7": "t"
        }
        
        for symbol, replacement in list(symbol_map.items()):
            password = password.replace(symbol, replacement)
        
        simplified_passwords[original_password] = password

    return simplified_passwords

def strong_password(passwords):

    global Statement    
    
    Len = False
    Cap = False
    Low = False
    Num = False
    Spec = False
    
    ''' Checks whether the string s fits the 
        criteria for a valid password.
    ''' 
    capital = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    lowercase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    number = ['0','1','2','3','4','5','6','7','8','9']
    special = ['@','$','#','!','%']
    
    for password in passwords:
        for character in password:
            if character in capital:
                Cap = True
        
            elif character in lowercase:
                Low = True
        
            elif character in number:
                Num = True
        
            elif character in special:
                Spec = True
                
        if len(password) >= 8:
            Len = True
        
        check = [Cap, Low, Num, Spec, Len]
        
        Statement[password] = check
    
    for key in Statement:
        values = Statement[key]
        count = values.count(True)
        Statement[key] = count
    
#### ---- INPUT ---- ####

## -- Introduction -- ##

print("Check the health of your password by comparing it to common passwords.")
print("Then we will tell how strong your password is, if it is not similiar to a common password.")
print("You may enter multiple values with a comma. Please do not add spaces!")

## -- User input -- ##

user_input = input("What password would you like to check? ")

user_passwords = passwords_list(user_input)

for password in user_passwords:    
    if len(password) <= 3:
        user_passwords.remove(password)
        print("These are your current passwords: " + user_passwords)
        
        user_input = input("Please enter a longer password then " + password + " to check: ")
        user_passwords.append(user_input)
        print("We will check these passwords: " + user_passwords)

print()

## -- Common passwords -- ##

bad_password = get_passwords()

## -- Variations -- ##

simplified_passwords = simplified_password(user_passwords)

strong_passwords = strong_password(user_passwords)

#### ---- OUTPUT ---- ####

## -- Base password -- ##

for password in user_passwords:
    if password in bad_password:
        Statement[password] = 0        
        print("Your password: " + password + " is too common.")

print()

## -- Variations -- ##

for key in simplified_passwords:
    values = simplified_passwords[key]
    
    if values in bad_password:
        Statement[key] = 0 
        print("Your password: " + key + " is too similar to \"" + values + "\".")

print()        

## -- Secure password -- ##

for key in Statement:
    values = Statement[key]
    
    if values <= 2:
        print("Your password: " + key + " is not very secure!")
        
    elif 4 >= values >= 3 :
        print("Your password: " + key + " seems pretty secure!")
        
    elif values == 5:
        print("Your password: " + key + " is very secure!")
