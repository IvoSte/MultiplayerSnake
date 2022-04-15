from viewer.colors import Color, color_from_map, colormaps
from controls.input_controls import Controls, default_player_controls
import pygame
import random
from game.env_variables import (
    BODY_DECAY_RATE,
    DEATH_PUNISHMENT,
    FREEZE_FRAMES_ON_BITTEN,
    FREEZE_FRAMES_ON_EAT,
    SNAKE_SIZE,
    INITIAL_SNAKE_LENGTH,
    SNAKE_SPEED,
    MAX_COLOR_SCALE,
    START_COUNTDOWN,
    TAIL_BITING,
    TAIL_STEALING,
    TICKS_PER_SECOND,
    VERZET,
)


class Player:
    def __init__(self, name="Player", controls=default_player_controls):
        self.name = name
        self.controls = controls

    def report(self):
        print(f"Player report: {self.name}")
        print(
            f"    {self.score = }\n   {self.length = }\n  {self.tails_lost = }\n  {self.tails_eaten = }"
        )
