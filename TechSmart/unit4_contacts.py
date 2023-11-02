"""
Unit 4 Project: Contacts

Description:
"""
# Sample user data as a list of lists
contacts = [
    ["John Doe", "123-456-7890", "123 Main St", "Friends"],
    ["Jane Smith", "987-654-3210", "456 Elm St", "Family"],
    ["Alice Johnson", "555-123-4567", "789 Oak St", "Work"],
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
                    if name.lower() == contact[0].lower() or phone == contact[1]:
                        print("Contact already exists.")
                        duplicate = True
                        break

                if not duplicate:
                    contacts.append([name, phone, address, group])
                    print("Contact added successfully")

    elif choice == "2":
        name = input("\nEnter the name to search: ")
        found_contacts = [contact for contact in contacts if name.lower() in contact[0].lower()]
        if found_contacts:
            print("\nMatching contacts:")
            for contact in found_contacts:
                print("Name:", contact[0])
                print("Phone:", contact[1])
                print("Address:", contact[2])
                print("Group:", contact[3])
        else:
            print("\nNo contacts found for " + name + ".")

    elif choice == "3":
        print("\nAll contacts:")
        for contact in contacts:
            print("Name:", contact[0])
            print("Phone:", contact[1])
            print("Address:", contact[2])
            print("Group:", contact[3])

    elif choice == "4":
        name = input("\nEnter the name to edit: ")
        for contact in contacts:
            if name.lower() in contact[0].lower():
                print("\nEditing contact:", contact[0])
                new_name = input("Enter new name (leave empty to keep the same): ")
                new_phone = input("Enter new phone number (leave empty to keep the same): ")
                new_address = input("Enter new address (leave empty to keep the same): ")
                new_group = input("Enter new group (leave empty to keep the same): ")

                if new_name:
                    contact[0] = new_name
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
                            contact[1] = new_phone
                            print("Contact edited successfully.")
                        else:
                            print("Invalid phone number format. Please use XXX-XXX-XXXX format.")
                if new_address:
                    contact[2] = new_address
                if new_group:
                    contact[3] = new_group

                print("Contact edited successfully.")
                break
        else:
            print("\nNo contacts found for " + name + ".")

    elif choice == "5":
        name = input("\nEnter the name to delete: ")
        for contact in contacts:
            if name.lower() in contact[0].lower():
                print("\nDeleting contact:", contact[0])
                contacts.remove(contact)
                print("Contact deleted successfully.")
                break
        else:
            print("\nNo contacts found for " + name + ".")

    elif choice == "6":
        group = input("\nEnter the group to filter: ")
        filtered_contacts = [contact for contact in contacts if group.lower() == contact[3].lower()]
        if filtered_contacts:
            print("\nContacts in the group '" + group + "':")
            for contact in filtered_contacts:
                print("Name:", contact[0])
                print("Phone:", contact[1])
                print("Address:", contact[2])
        else:
            print("\nNo contacts found in the group '" + group + "'.")

    elif choice == "7":
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid choice. Please try again.")
