"""
Unit 4 Project: Contacts

Description:
"""
# Sample user data
contacts = [
    {"name": "John Doe", "phone": "123-456-7890", "address": "123 Main St", "group": "Friends"},
    {"name": "Jane Smith", "phone": "987-654-3210", "address": "456 Elm St", "group": "Family"},
    {"name": "Alice Johnson", "phone": "555-123-4567", "address": "789 Oak St", "group": "Work"},
]

# Function to validate phone numbers
def validate_phone(phone):
    # Check if the phone number has the correct format (XXX-XXX-XXXX)
    if len(phone) != 12:
        return False
    for i in range(12):
        if i in (3, 7):
            if phone[i] != '-':
                return False
        else:
            if not phone[i].isdigit():
                return False
    return True

# Function to add a new contact to the list
def add_contact(name, phone, address, group):
    # Check for duplicate contacts
    for contact in contacts:
        if name.lower() == contact["name"].lower() or phone == contact["phone"]:
            print("Contact already exists.")
            return
    
    if not validate_phone(phone):
        print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
        return
    
    contacts.append({"name": name, "phone": phone, "address": address, "group": group})
    print("Contact added successfully.")

# Function to search for a contact by name
def search_contact(name):
    found_contacts = [contact for contact in contacts if name.lower() in contact["name"].lower()]
    if found_contacts:
        print("\nMatching contacts:")
        for contact in found_contacts:
            print("Name:", contact['name'])
            print("Phone:", contact['phone'])
            print("Address:", contact['address'])
            print("Group:", contact['group'])
    else:
        print("\nNo contacts found for " + name + ".")

# Function to display all contacts
def display_contacts():
    print("\nAll contacts:")
    for contact in contacts:
        print("Name:", contact['name'])
        print("Phone:", contact['phone'])
        print("Address:", contact['address'])
        print("Group:", contact['group'])

# Function to edit a contact
def edit_contact(name):
    for contact in contacts:
        if name.lower() in contact["name"].lower():
            print("\nEditing contact:", contact["name"])
            new_name = input("Enter new name (leave empty to keep the same): ")
            new_phone = input("Enter new phone number (leave empty to keep the same): ")
            new_address = input("Enter new address (leave empty to keep the same): ")
            new_group = input("Enter new group (leave empty to keep the same): ")

            if new_name:
                contact["name"] = new_name
            if new_phone:
                if validate_phone(new_phone):
                    contact["phone"] = new_phone
                else:
                    print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
            if new_address:
                contact["address"] = new_address
            if new_group:
                contact["group"] = new_group

            print("Contact edited successfully.")
            return
    print("\nNo contacts found for " + name + ".")

# Function to delete a contact
def delete_contact(name):
    for contact in contacts:
        if name.lower() in contact["name"].lower():
            print("\nDeleting contact:", contact["name"])
            contacts.remove(contact)
            print("Contact deleted successfully.")
            return
    print("\nNo contacts found for " + name + ".")

# Function to filter contacts by group
def filter_by_group(group):
    filtered_contacts = [contact for contact in contacts if group.lower() == contact["group"].lower()]
    if filtered_contacts:
        print("\nContacts in the group '" + group + "':")
        for contact in filtered_contacts:
            print("Name:", contact['name'])
            print("Phone:", contact['phone'])
            print("Address:", contact['address'])
    else:
        print("\nNo contacts found in the group '" + group + "'.")

# Sample usage
print("Welcome to the Contact Manager!")
while True:
    print("\nOptions:")
    print("1. Add a contact")
    print("2. Search for a contact")
    print("3. Display all contacts")
    print("4. Edit a contact")
    print("5. Delete a contact")
    print("6. Filter contacts by group")
    print("7. Exit")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        name = input("\nEnter the name: ")
        phone = input("Enter the phone number (XXX-XXX-XXXX format): ")
        address = input("Enter the address: ")
        group = input("Enter the group: ")
        add_contact(name, phone, address, group)
    elif choice == "2":
        name = input("\nEnter the name to search: ")
        search_contact(name)
    elif choice == "3":
        display_contacts()
    elif choice == "4":
        name = input("\nEnter the name to edit: ")
        edit_contact(name)
    elif choice == "5":
        name = input("\nEnter the name to delete: ")
        delete_contact(name)
    elif choice == "6":
        group = input("\nEnter the group to filter: ")
        filter_by_group(group)
    elif choice == "7":
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice. Please try again.")
