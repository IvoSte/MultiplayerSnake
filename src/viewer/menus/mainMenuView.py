from viewer.colors import Color
from .baseMenuView import BaseMenuView, Cursor, MenuOptionView


class MainMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "start": MenuOptionView(
                menu.options["start"],
                "Start",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "options": MenuOptionView(
                menu.options["options"],
                "Options",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
            "credits": MenuOptionView(
                menu.options["credits"],
                "Credits",
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
