import pygame
from .baseMenuView import BaseMenuView, OptionText, Cursor, MenuOptionView
from viewer.colors import Color


class PostGameMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            # Bit of a hack to have text here, create another dict for this TODO
            "match over": OptionText("Game over!", Color.WHITE.value, 0.45, 0.4),
            "restart": MenuOptionView(
                menu.options["restart"],
                "Restart",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
            "options": MenuOptionView(
                menu.options["options"],
                "Options",
                Color.WHITE.value,
                0.5,
                0.6,
                Color.WHITE.value,
            ),
            "quit": MenuOptionView(
                menu.options["quit"],
                "Quit",
                Color.WHITE.value,
                0.5,
                0.7,
                Color.WHITE.value,
            ),
        }
        self.cursor = Cursor("*", Color.WHITE.value, 0.0, 0.0, -0.05, 0.01)
