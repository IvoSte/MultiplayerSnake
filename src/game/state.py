from dataclasses import dataclass
from entities.food import Food

@dataclass
class State:
    game_over: bool
    in_end_screen: bool
    in_pause_menu: bool
    in_options_menu: bool
    in_game: bool
    in_menu: bool
    food: list[Food]