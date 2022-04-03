from re import S
from entities.agent import Agent

# setup superclass, needs to be filled TODO
class Item(Agent):

    def __init__(self, gameManager):
        #super().__init__()
        self.gameManager = gameManager
        
    def attach(self, observer):
        self._gameManager.append(observer)

    def notify(self):
        pass