from dataclasses import dataclass

@dataclass
class Item:
    name: str # name of item
    type: str # type of item; Deal damage, restore HP or MP
    description: str # Short description what item is going to do
    prop: int # number of point to deal/heal/restore
