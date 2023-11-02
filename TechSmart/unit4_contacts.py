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

        # Check if the phone number has the correct format (XXX-XXX-XXXX)
        if len(phone) != 12:
            print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
        else:
            valid = True
            for i in range(12):
                if i in (3, 7):
                    if phone[i] != '-':
                        valid = False
                        break
                elif not phone[i].isdigit():
                    valid = False
                    break

            if valid:
                # Check for duplicate contacts
                duplicate = False
                for contact in contacts:
                    if name.lower() == contact["name"].lower() or phone == contact["phone"]:
                        print("Contact already exists.")
                        duplicate = True
                        break

                if not duplicate:
                    contacts.append({"name": name, "phone": phone, "address": address, "group": group})
                    print("Contact added successfully")

    elif choice == "2":
        name = input("\nEnter the name to search: ")
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

    elif choice == "3":
        print("\nAll contacts:")
        for contact in contacts:
            print("Name:", contact['name'])
            print("Phone:", contact['phone'])
            print("Address:", contact['address'])
            print("Group:", contact['group'])

    elif choice == "4":
        name = input("\nEnter the name to edit: ")
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
                    # Check if the new phone number has the correct format (XXX-XXX-XXXX)
                    if len(new_phone) != 12:
                        print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
                    else:
                        valid = True
                        for i in range(12):
                            if i in (3, 7):
                                if new_phone[i] != '-':
                                    valid = False
                                    break
                            elif not new_phone[i].isdigit():
                                valid = False
                                break

                        if valid:
                            contact["phone"] = new_phone
                            print("Contact edited successfully.")
                        else:
                            print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
                if new_address:
                    contact["address"] = new_address
                if new_group:
                    contact["group"] = new_group

                print("Contact edited successfully.")
                break
        else:
            print("\nNo contacts found for " + name + ".")

    elif choice == "5":
        name = input("\nEnter the name to delete: ")
        for contact in contacts:
            if name.lower() in contact["name"].lower():
                print("\nDeleting contact:", contact["name"])
                contacts.remove(contact)
                print("Contact deleted successfully.")
                break
        else:
            print("\nNo contacts found for " + name + ".")

    elif choice == "6":
        group = input("\nEnter the group to filter: ")
        filtered_contacts = [contact for contact in contacts if group.lower() == contact["group"].lower()]
        if filtered_contacts:
            print("\nContacts in the group '" + group + "':")
            for contact in filtered_contacts:
                print("Name:", contact['name'])
                print("Phone:", contact['phone'])
                print("Address:", contact['address'])
        else:
            print("\nNo contacts found in the group '" + group + "'.")
            
    elif choice == "7":
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid choice. Please try again.")
