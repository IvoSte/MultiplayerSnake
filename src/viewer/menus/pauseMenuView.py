from viewer.colors import Color
from .baseMenuView import BaseMenuView, Cursor, MenuOptionView


class PauseMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "unpause": MenuOptionView(
                menu.options["unpause"],
                "Unpause",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
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
            "multiplayer": MenuOptionView(
                menu.options["multiplayer"],
                "Multiplayer (temp)",
                Color.WHITE.value,
                0.5,
                0.8,
                Color.WHITE.value,
            ),
        }
