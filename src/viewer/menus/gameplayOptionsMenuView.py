from viewer.colors import Color
from .baseMenuView import (
    BaseMenuView,
    Cursor,
    MenuOptionView,
)


class GameplayOptionsMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.options = {
            "players": MenuOptionView(
                menu.options["players"],
                "Players",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "time limit": MenuOptionView(
                menu.options["time limit"],
                "Time limit",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
            "countdown": MenuOptionView(
                menu.options["countdown"],
                "Countdown",
                Color.WHITE.value,
                0.5,
                0.6,
                Color.WHITE.value,
            ),
            "tail biting": MenuOptionView(
                menu.options["tail biting"],
                "Tail Biting",
                Color.WHITE.value,
                0.5,
                0.7,
                Color.WHITE.value,
            ),
            "tail stealing": MenuOptionView(
                menu.options["tail stealing"],
                "Tail Stealing",
                Color.WHITE.value,
                0.5,
                0.8,
                Color.WHITE.value,
            ),
            "snake speed": MenuOptionView(
                menu.options["snake speed"],
                "Snake Speed",
                Color.WHITE.value,
                0.5,
                0.9,
                Color.WHITE.value,
            ),
        }
