

class ItemHandler:
    
    def __init__(self, game, evManager):
        self.game = game
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        
        self.to_spawn = []

    def notify(self, event):
        if isinstance(event, events.SpawnItemEvent):
            self.to_spawn.append(event.item)

    def spawn_item(self, item):
        if isinstance(item, Food):
            self.game.model.add_food(item)
        if isinstance(item, PowerUp):
            self.game.model.add_powerup(item)


    def get_random_position(self):
        return (
            round(random.randrange(0, self.game.model.grid_size[0])),
            round(random.randrange(0, self.game.model.grid_size[1])),
        )