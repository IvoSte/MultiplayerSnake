from entities.item import Item
import game

gem_module = lambda: game.event_manager


class Food(Item):
    def __init__(self, game, pos, color):
        super().__init__(game)
        self.game = game
        self.pos = pos
        self.color = color

    def notify(self):
        foodx, foody = self.game.spawn_food()
        gem_module().EventManager.instance.Post(
            gem_module().SpawnFoodEvent((foodx, foody))
        )

    def eat(self):
        self.notify()
        del self

    def spawn(self):
        pass
