import random

class bcolors:  # Create class for colors of font ingame
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:  # Create class of character
    def __init__(self, name, hp, mp, ad, df, magic, items):
        self.name = name  # Name of character
        self.maxhp = hp  # Maximum HP
        self.hp = hp  # Current HP
        self.maxmp = mp  # Maximum MP
        self.mp = mp  # Current MP
        self.adh = ad + 10  # Highest atack damage
        self.adl = ad - 10  # Lowest atack damage
        self.df = df  # Defence; Ignore some damage dealt
        self.magic = magic  # Type of magic
        self.items = items  # Type of item

        # Menu of available actions
        self.actions = ["Attack", "Magic", "Items"]

    def generate_dmg(self):
        gen_dmg = random.randrange(self.adl, self.adh)
        if gen_dmg < 0:
            return 0
        return gen_dmg

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def restore(self, mps):
        self.mp += mps
        if self.mp > self.maxmp:
            self.mp = self.maxmp

    def get_hp(self):  # Return current HP
        return self.hp

    def get_max_hp(self):  # Return maximum HP
        return self.maxhp

    def get_mp(self):  # Return current MP
        return self.mp

    def get_max_mp(self):  # Return maximum MP
        return self.maxmp

    def reduce_mp(self, cost):  # Reducing MP of cost of spell
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.OKBLUE + "\n    ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("         " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + "\n    MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("          " + str(i) + ".", spell.name,
                  "-", str(spell.cost) + " mana")
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKGREEN + "\n    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("         " + str(i) + ".", item["item"].name + " -",
                  item["item"].description, " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target: ")) - 1
        return choice

    def get_enemy_stats(self):

        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 100 / 2

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 10:
            decreased = 10 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(
            "                           __________________________________________________ ")
        print(bcolors.BOLD + self.name + "      " +
              current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|    ")
        

    def get_hero_stats(self):

        hp_bar = ""
        hp_ticks = self.hp / self.maxhp * 100 / 4

        mp_bar = ""
        mp_ticks = self.mp / self.maxmp * 100 / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreasing = 9 - len(hp_string)

            while decreasing > 0:
                current_hp += " "
                decreasing -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreasing = 7 - len(mp_string)

            while decreasing > 0:
                current_mp += " "
                decreasing -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string
            
        

        print(
            "                        _________________________                __________ ")
        print(bcolors.BOLD + self.name + "      " +
              current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|    " +
              current_mp + "   |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        #procent = self.hp / self.maxhp * 100

        # if self.mp < spell.cost or spell.type == "white" and procent > 50:
        #    self.choose_enemy_spell()
        # else:
        return spell, magic_dmg
