from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random

# Create Black Magic - DMG
fire = Spell("Fire", 20, 60, "black") # Name, Cost, DMG/Heal, type
fireball = Spell("Fireball", 80, 120, "black")
god_fire = Spell("GodFire", 350, 800, "black")
void = Spell("Void", 600, 1200, "black")
meteor = Spell("Meteor", 50, 120, "black")
end = Spell("End", 100, 300, "black")

# Create White Magic - Heals
cure = Spell("Cure", 60, 100, "white")
hyper_restore = Spell("Hyper Restore", 90, 200, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50) # Name, Type, Description, Prop
super_potion = Item("Super Potion", "potion", "Heals 150 HP", 150)
mana_potion = Item("Mana Potion", "mp_potion", "Restore 50 MP", 50)
magic_potion = Item("Magic Potion", "mp_potion", "Restore 200 MP", 200)
max_potion = Item("Max Potion", "elixir", "Fully restore  HP/MP", 999999)
mega_elixir = Item("Mega Elixir", "elixir", "Fully restore HP/MP for party's members", 999999)

dynamite = Item("Dynamite", "attack", "Hit for 200 HP enemy", 200)

player_spells = [fire, fireball, god_fire, void, cure, hyper_restore]
enemy_spells = [meteor, end]

player_items = [{"item": potion, "quantity": 5}, {"item": super_potion, "quantity": 2},
                {"item": mana_potion, "quantity": 5}, {"item": magic_potion, "quantity": 2},
                {"item": max_potion, "quantity": 1}, {"item": mega_elixir, "quantity": 1},
                {"item": dynamite, "quantity": 1}]

# Instantiate People
player1 = Person("MRX    ", 400, 1, 20, 20, player_spells, player_items) # Name, HP, MP, AD, DF, Magic, Items
player2 = Person("Krypton", 600, 200, 150, 20, player_spells, player_items)
player3 = Person("WhoAmI ", 650, 150, 90, 20, player_spells, player_items)

enemy1 = Person("Draugr   ", 100, 150, 50, 26, enemy_spells, [])
enemy2 = Person("DeathLord", 999, 300, 150, 75, enemy_spells, [])
enemy3 = Person("Draugr   ", 100, 150, 50, 26, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
number_of_players = len(players)
number_of_enemies = len(enemies)
defeated_enemies = 0
defeated_players = 0

print("\n")
print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)
print("\n")

while running:
    print("-----------------------------------")
    print("-----------------------------------")

    print("\n\n")
    print("Name         HP                                       MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        while True:
            player.choose_action()
            choice = input("    Choose action: ")
            try:
                index = int(choice) - 1
                if index > -1 and index < 3:
                    break
                print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)
                continue
            except:
                print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)
                
        if index == 0:
            dmg = player.generate_dmg()
            while True:
                try:
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(dmg)
                    print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + 
                          " for", dmg, "points of health." + bcolors.ENDC)
                    break
                except:
                    print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)


        elif index == 1:
            player.choose_magic()
            
            while True:
                try:
                    magic_choice = int(input("Choose magic (To normal attack press 0): ")) - 1
                    if magic_choice == -1:
                        dmg = player.generate_dmg()
                        enemy = player.choose_target(enemies)
                        enemies[enemy].take_damage(dmg)
                        print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + 
                              " for", dmg, "points of health." + bcolors.ENDC)
                        break
                    spell = player.magic[magic_choice]
                    magic_dmg = spell.generate_damage()
                    current_mp = player.get_mp()

                    if spell.cost > current_mp:
                        print(bcolors.FAIL + "\n Not enough MP \n" + bcolors.ENDC)
                        continue
                    break
                except:
                    print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)

            if not magic_choice == -1:
                player.reduce_mp(spell.cost)
            else:
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
                continue
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + (" ") + spell.name + " deals " + str(
                      magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + (".") + bcolors.ENDC)


        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals you for", str(item.prop), "HP" + bcolors.ENDC)
                continue
            elif item.type == "mp_potion":
                player.restore(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " restore for", str(item.prop), "MP" + bcolors.ENDC)
                continue
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restore HP/MP" + bcolors.ENDC)
                continue
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

        # Check if battle is over - your win
        if enemies[enemy].get_hp() == 0:
            print(enemies[enemy].name.replace(" ", "") + " has died.")
            defeated_enemies += 1
            del enemies[enemy]
            if defeated_enemies == 3:
                print("\n")
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                running = False
                break

    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        
        enemy_choice = random.randrange(0, 2)
        
        for mana in enemy_spells:
            if enemy.get_mp() < mana.cost:
                enemy_choice = 0
                break
        
        if enemy_choice == 0: # Normal attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_dmg()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacked " + players[target].name.replace(":", "") + " for ",
                  enemy_dmg, " points ")
        
        elif enemy_choice == 1: # Magic attack
            spell, magic_dmg = enemy.choose_enemy_spell() 
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + " for " + str(magic_dmg) + bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(
                    magic_dmg) + " points of damage to " +
                      players[target].name.replace(" ", "") + bcolors.ENDC)
            

        # Check if battle is over - your loss
        if players[target].get_hp() == 0:
            print(" " + players[target].name.replace(" ", "") + " has died!")
            defeated_players += 1
            del players[target]
            if defeated_players == number_of_players:
                print("\n")
                print(bcolors.FAIL + "Enemies have defeated you!\n" + bcolors.ENDC)
                running = False
                break
