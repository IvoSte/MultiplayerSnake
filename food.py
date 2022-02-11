class Food:
    
    def __init__(self, pos, gameManager):
        self.pos = pos
        self.gameManager = gameManager

    def attach(self, observer):
        self._gameManager.append(observer)
        
    def notify(self):
        self.gameManager.spawn_food()
            
    def eat(self):
        self.notify()
        del self
    