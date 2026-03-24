-- rpg_battle.pyp
use random
use time

class Fighter:
    has name
    has hp
    has max_hp
    has attack_power

    setup with name, hp, attack_power:
        my name is name
        my max_hp is hp
        my hp is hp
        my attack_power is attack_power

    define is_alive:
        give back my hp > 0

    define take_damage with amount:
        change my hp to my hp - amount
        if my hp < 0:
            change my hp to 0
        say "{my name} takes {amount} damage! (HP: {my hp}/{my max_hp})"

    define attack with target:
        set dmg to random.randint(1, my attack_power)
        say "{my name} attacks {target.name}!"
        target.take_damage(dmg)


say "=== Arena Battle ==="
set player to new Fighter with "Hero", 20, 6
set monster to new Fighter with "Goblin", 15, 4

say "A wild {monster.name} appears!"
say ""

while player.is_alive() and monster.is_alive():
    say "Your HP: {player.hp} | Enemy HP: {monster.hp}"
    set action to ask "Do you want to (a)ttack or (h)eal? "
    
    if action == "a":
        player.attack(monster)
    else if action == "h":
        set heal to random.randint(2, 5)
        change my hp to player.hp + heal
        if player.hp > player.max_hp:
            change player.hp to player.max_hp
        say "{player.name} drinks a potion and heals {heal} HP! (HP: {player.hp}/{player.max_hp})"
    else:
        say "Invalid action! You stumble and miss your turn."

    time.sleep(1)
    
    if monster.is_alive():
        say ""
        say "-- Enemy Turn --"
        monster.attack(player)
    
    say "--------------------------------"
    time.sleep(1)

if player.is_alive():
    say "🎉 You defeated the {monster.name}! You win!"
else:
    say "💀 You were defeated... Game Over."