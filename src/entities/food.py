from entities.item import Item

class Food(Item):
    
    def __init__(self, gameEngine, pos, color):
        super().__init__(gameEngine)
        self.pos = pos
        self.color = color

        
    def notify(self):
        self.gameEngine.spawn_food()
            
    def eat(self):
        self.notify()
        del self
    
    def spawn(self):
        pass