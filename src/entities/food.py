from entities.item import Item
import game


class Food(Item):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pos
        self.color = color
