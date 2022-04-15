from entities.item import Item

class Food(Item):
    
    def __init__(self, gameManager, pos, color):
        super().__init__(gameManager)
        self.pos = pos
        self.color = color

        
    def notify(self):
        self.gameManager.spawn_food()
            
    def eat(self):
        self.notify()
        del self
    
    def spawn(self):
        pass