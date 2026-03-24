-- adventure.pyp
say "=== The Lost Cabin ==="
say "You wake up in a dark, cold cabin. You don't remember how you got here."

set has_key to false
set door_locked to true
set in_cabin to true

while in_cabin:
    say ""
    say "You look around. You see a [door], a [table], and a [window]."
    set choice to ask "What do you want to examine? (or 'quit' to give up): "
    change choice to choice in lowercase

    if choice == "quit":
        say "You close your eyes and give up. Game over."
        stop loop
        
    else if choice == "table":
        if has_key:
            say "The table is empty. You already took the key."
        else:
            say "You find a rusty key on the table! You take it."
            change has_key to true
            
    else if choice == "window":
        say "It's pitch black outside. The glass is too thick to break."
        
    else if choice == "door":
        if door_locked:
            if has_key:
                say "You use the rusty key on the door. It unlocks with a heavy click!"
                change door_locked to false
            else:
                say "The door is locked tight. There's a keyhole, though."
        else:
            say "You push the door open and escape into the night. You survived!"
            change in_cabin to false
            
    else:
        say "I don't understand that. Try typing 'door', 'table', or 'window'."