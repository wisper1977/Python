"""
Do not begin coding.
Instead, fill out the Planning worksheet.
"""

def check_password_strength(password, min_length=8):
    """
    Check the strength of a password.

    Parameters:
    - password (str): The password to be checked.
    - min_length (int): Minimum length required for the password (default is 8).

    Returns:
    - str: A message indicating the strength of the password.
    """
    if len(password) < min_length:
        return "Weak password. Please use a longer password."

    # Check for additional criteria (e.g., uppercase, lowercase, digits)
    criteria_met = check_additional_criteria(password)
    special_char_met = check_special_characters(password)
    
    if not criteria_met:
        return "Weak password. Please include uppercase letters, lowercase letters, and digits."
    
    if not special_char_met:
        return "Weak password. Please include special characters."

    return "Strong password. Good job!"

def check_additional_criteria(password):
    """
    Check additional criteria for password strength.

    Parameters:
    - password (str): The password to be checked.

    Returns:
    - bool: True if additional criteria are met, False otherwise.
    """
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    return has_uppercase and has_lowercase and has_digit

def check_special_characters(password):
    """
    Check if the password contains special characters.

    Parameters:
    - password (str): The password to be checked.

    Returns:
    - bool: True if special characters are present, False otherwise.
    """
    special_characters = "!@#$%^&*()_-+=<>?/{}[]|"
    return any(char in special_characters for char in password)

password = input("Enter your password: ")
min_length = int(input("Enter the minimum password length (press Enter for default): ") or 8)

result = check_password_strength(password, min_length)
print(result)
