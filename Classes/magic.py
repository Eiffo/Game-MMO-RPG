import random
from dataclasses import dataclass

@dataclass
class Spell:
    name: str # name of spell
    cost: int # cost of spell(in mana)
    dmg: int # damage dealt to enemies/damage heal to alias
    type: str # type of spell; black: damage dealt, white: HP restore

    def generate_damage(self): # generate damage for spells
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
    