from dataclasses import dataclass
from entities.food import Food


@dataclass
class State:
    running: bool
    game_over: bool
    game_paused: bool
    in_game: bool
    in_menu: bool
    food: list[Food]
