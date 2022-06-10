from entities.item import Item


class Food(Item):
    def __init__(self, game, pos, color):
        super().__init__(game)
        self.pos = pos
        self.color = color

    def notify(self):
        self.game.spawn_food()

    def eat(self):
        self.notify()
        del self

    def spawn(self):
        pass
