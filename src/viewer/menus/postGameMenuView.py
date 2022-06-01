import pygame
from .baseMenuView import BaseMenuView, OptionText, Cursor
from viewer.colors import Color


class PostGameMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            # Bit of a hack to have text here, create another dict for this TODO
            "match over": OptionText("Game over!", Color.WHITE.value, 0.45, 0.4),
            "restart": OptionText("Restart", Color.WHITE.value, 0.5, 0.5),
            "options": OptionText("Options", Color.WHITE.value, 0.5, 0.6),
            "quit": OptionText("Quit", Color.WHITE.value, 0.5, 0.7),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
