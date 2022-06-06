from operator import attrgetter
from entities.player import Player
from entities.snake import Snake
from entities.food import Food
from game.env_variables import (
    NUMBER_OF_PLAYERS,
    GAME_TIMER_SWITCH,
)


class GameModel:
    def __init__(self):
        # Game variables
        self.game_timer: int

        # Entities
        self.players: list[Player] = []
        self.snakes: list[Snake] = []
        self.food: list[Food] = []
        print(self.snakes)

    def set_game_timer(self, time):
        self.game_timer = time

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
    
    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def clear_players(self):
        self.players = []

    def add_snake(self, snake):
        if snake not in self.snakes:
            self.snakes.append(snake)

    def remove_snake(self, snake):
        if snake in self.snakes:
            self.snakes.remove(snake)

    def clear_snakes(self):
        self.snakes = []

    def add_food(self, food):
        if food not in self.food:
            self.food.append(food)

    def remove_food(self, food):
        if food in self.food:
            self.food.remove(food)

    def clear_food(self):
        self.food = []


    def get_final_score(self):
        final_scores = {
            "Most points": max(self.snakes, key=attrgetter("score")),
            "Longest tail": max(self.snakes, key=attrgetter("length")),
            "Tails stolen": max(self.snakes, key=attrgetter("tails_eaten")),
        }
        return final_scores

    def snakes_alive(self) -> int:
        return sum(1 for snake in self.snakes if snake.alive)

    def snakes_lives_left(self) -> int:
        active_lives = self.snakes_alive()
        reserve_lives = sum(snake.lives_left for snake in self.snakes)
        return active_lives + reserve_lives

    def dead_snakes_lives_left(self) -> int:
        return sum(snake.lives_left for snake in self.snakes if not snake.alive)

    def is_game_over(self):
        # In single player the player should be dead and have no lives left.
        # In multiplayer all players but on should be dead and without lives left.
        return (
            # Single player mode where the player is dead
            NUMBER_OF_PLAYERS == 1
            and self.snakes_lives_left() == 0
            # Multi player mode and only one player is alive and none respawning.
            or (
                NUMBER_OF_PLAYERS > 1
                and self.snakes_alive() == 1
                and self.dead_snakes_lives_left() == 0
            )
            # Timer for timed games
            or (GAME_TIMER_SWITCH and self.game_timer <= 0)
        )

    def get_player_from_name(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None


# What do I want in the game state?
# The game state should be the general handler to know all information about the game
# Like all snakes' positions, positions of food,
# so, it has all entities. 
# but also be able to derive / update information about the game like
# How many times which player has won.
# It should also be able to package itsself in a tiny format to be sent over the
# internet for multiplayer.
# It is to decouple the GameEngine object and the 'model values'.
