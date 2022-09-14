from .baseMenuView import BaseMenuView, MenuOptionView, TextView
from viewer.colors import Color


class MultiplayerLoadMenuView(BaseMenuView):
    def __init__(self, viewer, menu):
        BaseMenuView.__init__(self, viewer, menu)
        self.text = {}

        self.options = {
            "create room": MenuOptionView(
                menu.options["create room"],
                "Create multiplayer room",
                Color.WHITE.value,
                0.5,
                0.4,
                Color.WHITE.value,
            ),
            "join room": MenuOptionView(
                menu.options["join room"],
                "Join multiplayer room",
                Color.WHITE.value,
                0.5,
                0.5,
                Color.WHITE.value,
            ),
        }
