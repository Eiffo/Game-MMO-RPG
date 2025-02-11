from Classes import Person, Spell, Item, bcolors
import random, time


def main():
   
    # Create Black Magic - DMG
    fire = Spell("Fire", 20, 60, "black") # Name, Cost, DMG/Heal, type
    fireball = Spell("Fireball", 80, 120, "black")
    god_fire = Spell("GodFire", 350, 800, "black")
    void = Spell("Void", 600, 1200, "black")
    meteor = Spell("Meteor", 50, 120, "black")
    end = Spell("End", 120, 300, "black")

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

    heroes_spells = [fire, fireball, god_fire, void, cure, hyper_restore]
    enemy_spells = [meteor, end]

    heroes_items = [{"item": potion, "quantity": 5}, {"item": super_potion, "quantity": 2},
                    {"item": mana_potion, "quantity": 5}, {"item": magic_potion, "quantity": 2},
                    {"item": max_potion, "quantity": 1}, {"item": mega_elixir, "quantity": 1},
                    {"item": dynamite, "quantity": 1}]

    # Instantiate People
    hero1 = Person("MRX    ", 100, 1, 80, 20, heroes_spells, heroes_items) # Name, HP, MP, AD, DF, Magic, Items
    hero2 = Person("Krypton", 100, 200, 5, 20, heroes_spells, heroes_items)
    hero3 = Person("WhoAmI ", 100, 150, 10, 20, heroes_spells, heroes_items)

    enemy1 = Person("Draugr   ", 100, 90, 50, 26, enemy_spells, [])
    enemy2 = Person("DeathLord", 999, 240, 150, 75, enemy_spells, [])
    enemy3 = Person("Draugr   ", 100, 90, 50, 26, enemy_spells, [])

    heroes = [hero1, hero2, hero3] # add heroes to list
    enemies = [enemy1, enemy2, enemy3] # add enemies to list

    running = True
    number_of_heroes = len(heroes) # count the number of heroes
    number_of_enemies = len(enemies) # count the number of enemies
    defeated_enemies = 0
    defeated_heroes = 0
    

    print("\n")
    print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)
    print("\n")
    

    while running:        
        print("\n-----------------------------------")
        print("-----------------------------------")

        print("\n\n")
        print("Name         HP                                       MP")

        for hero in heroes:
            hero.get_hero_stats()

        print("\n")

        for enemy in enemies:
            enemy.get_enemy_stats()

        for hero in heroes:
            print("\n\n\n")
            hero.get_hero_stats()
            while True:
                hero.choose_action()
                choice = input("    Choose action: ")
                try:
                    index = int(choice) - 1
                    if index > -1 and index < 3:
                        break
                    print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)
                    continue
                except:
                    print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)
                    
            if index == 0: # Normal attack
                dmg = hero.generate_dmg()
                while True:
                    try:
                        enemy = hero.choose_target(enemies)
                        if enemy == -1:
                            print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC) 
                            continue
                        enemies[enemy].take_damage(dmg)
                        print(bcolors.OKBLUE + "\n" + hero.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + 
                            " for", dmg, "points of health." + bcolors.ENDC)
                        break
                    except:
                        print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)


            elif index == 1: # Magic
                hero.choose_magic()
                
                while True:
                    try:
                        magic_choice = int(input("Choose magic (To normal attack press 0): ")) - 1
                        if magic_choice == -1:
                            dmg = hero.generate_dmg()
                            enemy = hero.choose_target(enemies)
                            enemies[enemy].take_damage(dmg)
                            print(bcolors.OKBLUE + "\n" + hero.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + 
                                " for", dmg, "points of health." + bcolors.ENDC)
                            break
                        spell = hero.magic[magic_choice]
                        magic_dmg = spell.generate_damage()
                        current_mp = hero.get_mp()

                        if spell.cost > current_mp:
                            print(bcolors.FAIL + "\n Not enough MP \n" + bcolors.ENDC)
                            continue
                        break
                    except:
                        print(bcolors.WARNING + "  Wrong index! Try again." + bcolors.ENDC)

                if not magic_choice == -1:
                    hero.reduce_mp(spell.cost)
                else:
                    continue

                if spell.type == "white":
                    hero.heal(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
                    continue
                elif spell.type == "black":
                    enemy = hero.choose_target(enemies)
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + hero.name.replace(" ", "") + (" ") + spell.name + " deals " + str(
                        magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + (".") + bcolors.ENDC)


            elif index == 2: # Items
                while True:
                    hero.choose_item()
                    item_choice = int(input("Choose item: ")) - 1

                    item = hero.items[item_choice]["item"]

                    if hero.items[item_choice]["quantity"] == 0: # check if you have that item in bag
                        print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                    else: break

                hero.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    hero.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " heals you for", str(item.prop), "HP" + bcolors.ENDC)
                    continue
                elif item.type == "mp_potion":
                    hero.restore(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " restore for", str(item.prop), "MP" + bcolors.ENDC)
                    continue
                elif item.type == "elixir":
                    if item.name == "Mega Elixir":
                        for i in heroes:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        hero.hp = hero.maxhp
                        hero.mp = hero.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restore HP/MP" + bcolors.ENDC)
                    continue
                elif item.type == "attack":
                    enemy = hero.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                        "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

            # Check if battle is over - heroes win
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                defeated_enemies += 1
                del enemies[enemy]
                if defeated_enemies == number_of_enemies:
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
                target = random.randrange(0, len(heroes))
                enemy_dmg = enemy.generate_dmg()

                heroes[target].take_damage(enemy_dmg)
                print(enemy.name.replace(" ", "") + " attacked " + heroes[target].name.replace(" ", "") + " for",
                    enemy_dmg, "points ")
            
            elif enemy_choice == 1: # Magic attack
                spell, magic_dmg = enemy.choose_enemy_spell() 
                enemy.reduce_mp(spell.cost)

                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + " for " + str(magic_dmg) + bcolors.ENDC)

                elif spell.type == "black":
                    target = random.randrange(0, len(heroes))
                    heroes[target].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(
                        magic_dmg) + " points of damage to " +
                        heroes[target].name.replace(" ", "") + bcolors.ENDC)
                

            # Check if battle is over - your loss
            if heroes[target].get_hp() == 0:
                print(" " + heroes[target].name.replace(" ", "") + " has died!")
                defeated_heroes += 1
                del heroes[target]
                if defeated_heroes == number_of_heroes:
                    print("\n")
                    print(bcolors.FAIL + "Enemies have defeated you!\n" + bcolors.ENDC)
                    running = False
                    break


if __name__ == "__main__":
    main()
    time.sleep(10)
    