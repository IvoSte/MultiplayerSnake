from pygame import Color
import random
from entities.food import Food
from entities.powerup import PowerUp, SpeedPowerUp, GhostPowerUp, ShieldPowerUp


class ItemHandler:
    def __init__(self, game, evManager):
        self.game = game
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.to_spawn = []

    def notify(self, event):
        pass

    def update(self):
        self.spawn_items()
        # self.update_items()

    def create_food(self, pos=None):
        if pos == None:
            pos = self.get_random_position()
        color = Color(0, random.randint(200, 255), 0)
        self.add_item_to_spawn(Food(pos, color))

    def create_powerups(self, amount_per_types: dict):
        for powerup_type_name in amount_per_types:
            if powerup_type_name == "speed":
                powerup_type = SpeedPowerUp
            if powerup_type_name == "ghost":
                powerup_type = GhostPowerUp
            if powerup_type_name == "shield":
                powerup_type = ShieldPowerUp
            for i in range(amount_per_types[powerup_type_name]):
                self.create_powerup(powerup_type=powerup_type)

    def create_powerup(self, pos=None, powerup_type=SpeedPowerUp):
        if pos == None:
            pos = self.get_random_position()
        self.add_item_to_spawn(powerup_type(pos))

    def add_item_to_spawn(self, item):
        self.to_spawn.append(item)

    def spawn_items(self):
        for item in self.to_spawn:
            self.spawn_item(item)
        self.to_spawn = []

    def spawn_item(self, item):
        if isinstance(item, Food):
            self.game.model.add_food(item)
        if isinstance(item, PowerUp):
            self.game.model.add_powerup(item)

    def update_items(self):
        for item in self.game.model.food:
            item.update()
        for item in self.game.model.powerups:
            item.update()

    def get_random_position(self):
        return (
            round(random.randrange(0, self.game.model.grid_size[0])),
            round(random.randrange(0, self.game.model.grid_size[1])),
        )
