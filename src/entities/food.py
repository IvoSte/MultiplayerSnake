from entities.item import Item
import game

gem_mod = lambda: game.event_manager.EventManager


class Food(Item):
    def __init__(self, game, pos, color):
        super().__init__(game)
        self.game = game
        self.pos = pos
        self.color = color

    def notify(self):
        foodx, foody = self.game.spawn_food()
        gem_mod().instance.Post(gem_mod().SpawnFoodEvent((foodx, foody)))

    def eat(self):
        self.notify()
        del self

    def spawn(self):
        pass
