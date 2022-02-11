from dataclasses import dataclass
from food import Food

@dataclass
class State:
    game_over: bool
    in_end_screen: bool
    food: Food