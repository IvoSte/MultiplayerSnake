from dataclasses import dataclass
from entities.snake import Snake
from viewer.colors import Color, color_from_map, colormaps
from controls.input_controls import Controls, default_player_controls
from game.env_variables import (
    VERZET,
)


class Player:
    def __init__(
        self,
        name="Player",
        snake: Snake = None,
        controls=default_player_controls,
        snake_colormap=None,
    ):
        self.name = name
        self.controls = controls
        self.snake = snake
        self.snake_colormap = snake_colormap
        self.player_statistics: PlayerStatistics = PlayerStatistics()
        self.is_ready = False

    def set_snake(self, snake):
        self.snake = snake

    def to_json(self):
        return {"name": self.name, "is_ready": self.is_ready}

    def report(self):
        print(f"Player report: {self.name}")


@dataclass
class PlayerStatistics:
    wins: int = 0
    games_played: int = 0
    total_score: int = 0
    total_tails_eaten: int = 0
