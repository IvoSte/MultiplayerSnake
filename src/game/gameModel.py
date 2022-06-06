from state import State


class GameModel:
    def __init__(self):
        self.players
        # self.snakes
        # self.entities
        # self.food
        self.environment


# What do I want in the game state?
# The game state should be the general handler to know all information about the game
# Like all players' positions, positions of food,
# so, it has all entities. 
# but also be able to derive / update information about the game like
# How many times which player has won.
# It should also be able to package itsself in a tiny format to be sent over the
# internet for multiplayer.
# It is to decouple the GameEngine object and the 'model values'.
