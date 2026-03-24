-- contacts.pyp
say "=== Contact Book ==="

set contacts to []

while true:
    say ""
    say "1. Add a Contact"
    say "2. View Contacts"
    say "3. Exit"
    
    set choice to ask "Choose an option (1-3): "
    
    if choice == "3":
        say "Goodbye!"
        stop loop
        
    else if choice == "1":
        set name to ask "Enter name: "
        set phone to ask "Enter phone number: "
        
        -- Create a Map and add it to our List
        set new_contact to {"name": name, "phone": phone}
        add new_contact to contacts
        
        say "Contact for {name} added successfully!"
        
    else if choice == "2":
        say "--- Your Contacts ---"
        if count of contacts == 0:
            say "No contacts found. Try adding some first!"
        else:
            for each person in contacts:
                say person at "name" + " | Phone: " + person at "phone"
        say "---------------------"
        
    else:
        say "Invalid choice. Please type 1, 2, or 3."